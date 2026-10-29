"""WM04 — collect episodes, keeping successors and both endings.

Rust sibling: `src/dataset.rs`. The `Transition` struct there becomes a frozen dataclass
here; the two endings become an `Enum` there and two booleans here, which is the difference
worth reading.

Rust's `episode_bounds` uses half-open `[start, end)` ranges and slices. Python uses the same
arithmetic so the split cannot drift between the two implementations.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum

from .wm01_state import MAX_STEPS, State
from .wm02_action import Action
from .wm03_simulator import step


class Ending(Enum):
    TERMINATED = "terminated"
    TRUNCATED = "truncated"


@dataclass(frozen=True)
class Transition:
    episode: int
    tick: int
    state: State
    action: Action
    successor: State
    terminated: bool
    truncated: bool

    def visible(self) -> tuple[float, float]:
        return self.state.normalized()

    def visible_delta(self) -> tuple[float, float]:
        now = self.state.normalized()
        nxt = self.successor.normalized()
        return (nxt[0] - now[0], nxt[1] - now[1])


class Rng:
    """Splitmix-style generator, matching the Rust one exactly.

    `numpy.random` would be simpler, but then the two languages would produce different data
    and the comparison would be pointless. This is not a statistical recommendation.
    """

    MASK = (1 << 64) - 1

    def __init__(self, seed: int) -> None:
        self._state = ((seed * 0x9E3779B97F4A7C15) & self.MASK) ^ 0x5DEECE66D1A48FAB

    def next_u64(self) -> int:
        self._state = (self._state + 0x9E3779B97F4A7C15) & self.MASK
        z = self._state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & self.MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & self.MASK
        return z ^ (z >> 31)

    def unit(self) -> float:
        return (self.next_u64() >> 11) / float(1 << 53)

    def range(self, low: float, high: float) -> float:
        return low + (high - low) * self.unit()

    def below(self, bound: int) -> int:
        return self.next_u64() % bound


def initial_state(rng: Rng) -> State:
    return State(
        x=rng.range(-0.05, 0.05),
        v=rng.range(-0.05, 0.05),
        theta=rng.range(-0.05, 0.05),
        omega=rng.range(-0.05, 0.05),
    )


def proportional_controller(state: State, bias: float) -> Action:
    lean = state.theta + 0.5 * state.omega + bias
    return Action.RIGHT if lean > 0 else Action.LEFT


def collect(rng: Rng, episodes: int = 40, max_steps: int = MAX_STEPS,
            exploration: float = 0.25, bias_scale: float = 0.15) -> list[Transition]:
    if episodes <= 0 or max_steps <= 0:
        raise ValueError("episodes and max_steps must be positive")
    if not 0.0 <= exploration <= 1.0:
        raise ValueError("exploration is a probability in [0, 1]")
    if not math.isfinite(bias_scale) or bias_scale < 0:
        raise ValueError("bias_scale must be finite and nonnegative")

    rows: list[Transition] = []
    for episode in range(episodes):
        bias = rng.range(-bias_scale, bias_scale)
        state = initial_state(rng)
        tick = 0
        while tick < max_steps:
            if rng.unit() < exploration:
                action = Action(rng.below(2))
            else:
                action = proportional_controller(state, bias)
            successor = step(state, action)
            tick += 1
            fell = successor.failed()
            out_of_time = (not fell) and tick == max_steps
            rows.append(Transition(
                episode=episode,
                tick=tick - 1,
                state=state,
                action=action,
                successor=successor,
                terminated=fell,
                truncated=out_of_time,
            ))
            state = successor
            if fell or out_of_time:
                break
    return rows


def episode_bounds(rows: list[Transition]) -> list[tuple[int, int]]:
    """Half-open `[start, end)` per episode, so a window can never span two games."""
    bounds: list[tuple[int, int]] = []
    begin = 0
    for index, row in enumerate(rows):
        if row.terminated or row.truncated:
            bounds.append((begin, index + 1))
            begin = index + 1
    if begin < len(rows):
        bounds.append((begin, len(rows)))
    return bounds


def split_episodes(rows: list[Transition], train_fraction: float
                   ) -> tuple[list[Transition], list[Transition]]:
    if not 0.0 < train_fraction < 1.0:
        raise ValueError("train_fraction must be strictly between 0 and 1")
    bounds = episode_bounds(rows)
    if len(bounds) < 2:
        raise ValueError("need at least two episodes to split")
    split = min(max(round(len(bounds) * train_fraction), 1), len(bounds) - 1)
    boundary = bounds[split][0]
    return rows[:boundary], rows[boundary:]


def main() -> None:
    rows = collect(Rng(0), episodes=20, max_steps=500, exploration=0.25, bias_scale=0.15)
    bounds = episode_bounds(rows)
    terminated = sum(1 for row in rows if row.terminated)
    truncated = sum(1 for row in rows if row.truncated)
    print(f"transitions:      {len(rows)}")
    print(f"episodes:         {len(bounds)}")
    print(f"ended by falling: {terminated}")
    print(f"ended by timer:   {truncated}")
    print()
    first = rows[0]
    print("the first record, which keeps seven things:")
    for name in ("episode", "tick", "state", "action", "successor", "terminated", "truncated"):
        print(f"  {name + ':':<13} {getattr(first, name)}")
    print(f"  visible:      {first.visible()}")
    print(f"  delta:        {first.visible_delta()}")
    print()
    last = rows[bounds[0][1] - 1]
    ending = Ending.TERMINATED if last.terminated else Ending.TRUNCATED
    print(f"last transition of episode 0: {ending.value}")
    print(f"  successor still present: {math.isfinite(last.successor.x)}")
    train, holdout = split_episodes(rows, 0.7)
    print()
    print(f"split by episode: train {len(train)} transitions, holdout {len(holdout)}")
    print(f"holdout covers {len({row.episode for row in holdout})} whole episodes")


if __name__ == "__main__":
    main()
