"""WM06 — one-step error versus free rollout, error **at each depth**.

Rust sibling: `src/rollout.rs`. Same eligible-episode rule, same frozen baseline, so the two
curves must match.
"""
from __future__ import annotations

from dataclasses import dataclass

from .wm04_dataset import Transition, episode_bounds
from .wm05_model import DeltaModel


@dataclass(frozen=True)
class Error:
    position_m: float = 0.0
    angle_rad: float = 0.0

    def __add__(self, other: "Error") -> "Error":
        return Error(self.position_m + other.position_m, self.angle_rad + other.angle_rad)

    def scale(self, factor: float) -> "Error":
        return Error(self.position_m * factor, self.angle_rad * factor)


def _absolute_error(predicted, truth) -> Error:
    return Error(abs(predicted.x - truth.x), abs(predicted.theta - truth.theta))


def one_step_error(model: DeltaModel, rows: list[Transition]) -> Error:
    if not rows:
        raise ValueError("no transitions to evaluate")
    total = Error()
    for row in rows:
        total = total + _absolute_error(model.predict(row.state, row.action), row.successor)
    return total.scale(1.0 / len(rows))


@dataclass(frozen=True)
class RolloutCurve:
    depth: list[int]
    model: list[Error]
    frozen: list[Error]

    def trust_horizon(self, tolerance_m: float, tolerance_rad: float) -> int:
        count = 0
        for error in self.model:
            if error.position_m <= tolerance_m and error.angle_rad <= tolerance_rad:
                count += 1
            else:
                break
        return count

    def deepest_depth_beating_frozen(self) -> int:
        deepest = 0
        for depth, model_error, frozen_error in zip(self.depth, self.model, self.frozen):
            if model_error.angle_rad < frozen_error.angle_rad:
                deepest = depth
            else:
                break
        return deepest


def rollout_curve(model: DeltaModel, rows: list[Transition],
                  bounds: list[tuple[int, int]], horizon: int) -> RolloutCurve:
    """Free rollout error at depth `h`, with the frozen baseline beside it.

    Averaging over steps `1..h` would answer a different question and hide the depth where
    the model falls apart.
    """
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if not rows:
        raise ValueError("no transitions to roll out")
    depths: list[int] = []
    model_errors: list[Error] = []
    frozen_errors: list[Error] = []
    for steps in range(1, horizon + 1):
        model_total = Error()
        frozen_total = Error()
        count = 0
        for begin, end in bounds:
            if end - begin < steps:
                continue
            start = rows[begin].state
            current = start
            for offset in range(steps):
                row = rows[begin + offset]
                current = model.predict(current, row.action)
            truth = rows[begin + steps - 1].successor
            model_total = model_total + _absolute_error(current, truth)
            frozen_total = frozen_total + _absolute_error(start, truth)
            count += 1
        if count == 0:
            raise ValueError(f"no episode is long enough for depth {steps}")
        depths.append(steps)
        model_errors.append(model_total.scale(1.0 / count))
        frozen_errors.append(frozen_total.scale(1.0 / count))
    return RolloutCurve(depths, model_errors, frozen_errors)


def main() -> None:
    from .wm04_dataset import Rng, collect, split_episodes

    rows = collect(Rng(0), episodes=40, max_steps=500, exploration=0.25, bias_scale=0.15)
    train, holdout = split_episodes(rows, 0.75)
    model = DeltaModel.fit(train, ridge=1e-6)
    bounds = episode_bounds(holdout)

    one_step = one_step_error(model, holdout)
    print("teacher-forced (every step starts from reality):")
    print(f"  position error: {one_step.position_m:.6f} m")
    print(f"  angle error:    {one_step.angle_rad:.6f} rad")
    print()

    curve = rollout_curve(model, holdout, bounds, 10)
    print("free rollout (the model eats its own output):")
    print(f"  {'depth':>5}  {'model m':>12}  {'frozen m':>12}  {'model rad':>12}  {'frozen rad':>12}")
    for index, depth in enumerate(curve.depth):
        print(f"  {depth:>5}  {curve.model[index].position_m:>12.6f}"
              f"  {curve.frozen[index].position_m:>12.6f}"
              f"  {curve.model[index].angle_rad:>12.6f}"
              f"  {curve.frozen[index].angle_rad:>12.6f}")
    print()
    print(f"trust horizon (both tolerances): {curve.trust_horizon(0.05, 0.02)}")
    print(f"deepest depth beating the frozen baseline: {curve.deepest_depth_beating_frozen()}")


if __name__ == "__main__":
    main()
