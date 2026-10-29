"""WM07 — plan by imagining, and change the goal without refitting.

Rust sibling: `src/planner.rs`. Same goals, same score formula, same unit rule: the park
target is in **metres**, so the comparison happens in metres.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .wm01_state import THETA_LIMIT, X_LIMIT, State
from .wm02_action import Action
from .wm04_dataset import Rng
from .wm05_model import DeltaModel


class GoalKind(Enum):
    BALANCE = "balance"
    PARK = "park"


@dataclass(frozen=True)
class Goal:
    """A goal is a value, not a field on the model. Changing it needs no training."""

    kind: GoalKind
    target_m: float = 0.0

    @classmethod
    def balance(cls) -> "Goal":
        return cls(GoalKind.BALANCE)

    @classmethod
    def park(cls, target_m: float) -> "Goal":
        return cls(GoalKind.PARK, target_m)

    def name(self) -> str:
        return "balance" if self.kind is GoalKind.BALANCE else f"park({self.target_m:.3f} m)"


@dataclass(frozen=True)
class Dream:
    states: list[State]
    failed_at: int | None = None

    def alive_steps(self) -> int:
        return self.failed_at if self.failed_at is not None else len(self.states)

    def last_reachable(self) -> State:
        """The last step *before* a predicted failure. A failed dream cannot come back."""
        reachable = self.alive_steps()
        return self.states[reachable - 1] if reachable > 0 else self.states[0]


def score(goal: Goal, dream: Dream) -> float:
    """Larger is better. Every term is in physical units on purpose.

    `abs()` is not decoration. Without it, a pole leaning *left* contributes a negative
    sum, so `-upright` becomes a positive reward and the planner learns to topple the pole
    in the direction that "scores well". Rust uses `state.theta.abs()`; the two languages
    must agree, and the parity test is what caught this.
    """
    alive_fraction = dream.alive_steps() / max(len(dream.states), 1)
    if goal.kind is GoalKind.BALANCE:
        alive = dream.alive_steps()
        upright = sum(abs(state.theta) / THETA_LIMIT for state in dream.states[:alive]) / max(alive, 1)
        return alive_fraction - upright
    last = dream.last_reachable()
    distance_m = abs(last.x - goal.target_m)
    upright = abs(last.theta) / THETA_LIMIT
    # Scored by where the dream ENDS. Averaging rejects the only manoeuvre that works,
    # because moving a cart-pole right begins by pushing left.
    return alive_fraction - distance_m - 0.5 * upright


def dream(model: DeltaModel, start: State, actions: list[Action]) -> Dream:
    if not actions:
        raise ValueError("a dream needs at least one action")
    states: list[State] = []
    current = start
    failed_at = None
    for action in actions:
        current = model.predict(current, action)
        if current.failed():
            failed_at = len(states)
            states.append(current)
            break
        states.append(current)
    return Dream(states, failed_at)


@dataclass(frozen=True)
class Plan:
    actions: list[Action]
    score: float
    candidates: int


def plan(model: DeltaModel, start: State, goal: Goal, horizon: int, sequences: int,
         rng: Rng) -> Plan:
    """Random search over action sequences. The model is read, never modified."""
    if horizon <= 0 or sequences <= 0:
        raise ValueError("horizon and sequences must be positive")
    best: Plan | None = None
    for _ in range(sequences):
        actions = [Action(rng.below(2)) for _ in range(horizon)]
        value = score(goal, dream(model, start, actions))
        if best is None or value > best.score:
            best = Plan(actions, value, sequences)
    if best is None:
        raise ValueError("no candidate was evaluated")
    return best


def main() -> None:
    from .wm04_dataset import collect, split_episodes
    from .wm05_model import DeltaModel

    rows = collect(Rng(0), episodes=40, max_steps=500, exploration=0.25, bias_scale=0.15)
    train, _ = split_episodes(rows, 0.75)
    model = DeltaModel.fit(train, ridge=1e-6)
    before = model.weights()
    start = State.upright()

    for goal in (Goal.balance(), Goal.park(1.0), Goal.park(0.5)):
        chosen = plan(model, start, goal, horizon=6, sequences=64, rng=Rng(11))
        dreamt = dream(model, start, chosen.actions)
        print(f"goal: {goal.name():<16}  score {chosen.score:>9.4f}"
              f"  alive {dreamt.alive_steps()}/{len(dreamt.states)}"
              f"  final x {dreamt.last_reachable().x:+.4f} m")
        print("  actions:", " ".join(action.name_lower() for action in chosen.actions))
        print(f"  re-scored by this goal: {score(goal, dreamt):.6f}")

    after = model.weights()
    print()
    print(f"coefficients before planning: {before}")
    print(f"coefficients after planning:  {after}")
    print(f"unchanged: {before == after}")
    print()
    print("Changing the goal changed the request, not the fitted physics.")


if __name__ == "__main__":
    main()
