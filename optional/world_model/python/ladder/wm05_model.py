"""WM05 — fit the same five-feature linear delta model.

Rust sibling: `src/model.rs`. Same features in the same order, same ridge, same
partial-pivoting solve, so the coefficients must agree to floating-point precision.
"""
from __future__ import annotations

import math

from .wm01_state import THETA_LIMIT, X_LIMIT, State, from_normalized
from .wm02_action import Action
from .wm04_dataset import Transition

FEATURES = 5
OUTPUTS = 2


def features(state: State, action: Action) -> list[float]:
    nx, ntheta = state.normalized()
    return [
        nx,
        ntheta,
        1.0 if action is Action.RIGHT else 0.0,
        1.0 if action is Action.LEFT else 0.0,
        1.0,
    ]


def _solve(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting, mirroring the Rust routine."""
    n = FEATURES
    a = [row[:] for row in matrix]
    b = rhs[:]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(a[row][column]))
        if abs(a[pivot][column]) < 1e-12:
            raise ValueError("normal equations are singular; collect more varied data or use ridge")
        a[column], a[pivot] = a[pivot], a[column]
        b[column], b[pivot] = b[pivot], b[column]
        diagonal = a[column][column]
        for row in range(column + 1, n):
            factor = a[row][column] / diagonal
            if factor == 0.0:
                continue
            for k in range(column, n):
                a[row][k] -= factor * a[column][k]
            b[row] -= factor * b[column]
    solution = [0.0] * n
    for row in range(n - 1, -1, -1):
        total = b[row]
        for k in range(row + 1, n):
            total -= a[row][k] * solution[k]
        solution[row] = total / a[row][row]
    if any(not math.isfinite(value) for value in solution):
        raise ValueError("the fit produced non-finite coefficients")
    return solution


class DeltaModel:
    """A fitted linear delta model. It owns its coefficients and nothing else."""

    def __init__(self, coefficients: list[list[float]], ridge: float, samples: int) -> None:
        self.coefficients = coefficients
        self.ridge = ridge
        self.samples = samples

    @classmethod
    def fit(cls, training: list[Transition], ridge: float = 1e-6) -> "DeltaModel":
        if not training:
            raise ValueError("no transitions to fit")
        if not math.isfinite(ridge) or ridge < 0:
            raise ValueError("ridge must be finite and nonnegative")
        gram = [[0.0] * FEATURES for _ in range(FEATURES)]
        rhs = [[0.0] * FEATURES for _ in range(OUTPUTS)]
        for row in training:
            x = features(row.state, row.action)
            for i in range(FEATURES):
                for j in range(FEATURES):
                    gram[i][j] += x[i] * x[j]
            target = row.visible_delta()
            for output in range(OUTPUTS):
                for i in range(FEATURES):
                    rhs[output][i] += x[i] * target[output]
        for i in range(FEATURES):
            gram[i][i] += ridge
        coefficients = [_solve(gram, rhs[output]) for output in range(OUTPUTS)]
        return cls(coefficients, ridge, len(training))

    def predict(self, state: State, action: Action) -> State:
        x = features(state, action)
        now = state.normalized()
        next_visible = [
            now[output] + sum(c * f for c, f in zip(self.coefficients[output], x))
            for output in range(OUTPUTS)
        ]
        x_position, theta = from_normalized((next_visible[0], next_visible[1]))
        # Velocities are reported unchanged: this model cannot observe them.
        return State(x=x_position, v=state.v, theta=theta, omega=state.omega)

    def weights(self) -> list[float]:
        return [value for row in self.coefficients for value in row]


def normalized_limits() -> tuple[float, float]:
    return (X_LIMIT, THETA_LIMIT)


def main() -> None:
    from .wm04_dataset import Rng, collect, split_episodes
    from .wm03_simulator import step

    rows = collect(Rng(0), episodes=40, max_steps=500, exploration=0.25, bias_scale=0.15)
    train, holdout = split_episodes(rows, 0.75)
    model = DeltaModel.fit(train, ridge=1e-6)
    print(f"fitted on {model.samples} borrowed transitions")
    print(f"ridge: {model.ridge}")
    print("coefficients (output x feature):")
    for output, row in enumerate(model.coefficients):
        label = "cart position" if output == 0 else "pole angle  "
        print(f"  {label}: {row}")
    print()
    model_error = 0.0
    simulator_error = 0.0
    sample = holdout[:500]
    for row in sample:
        predicted = model.predict(row.state, row.action)
        reference = step(row.state, row.action)
        model_error += abs(predicted.theta - row.successor.theta)
        simulator_error += abs(reference.theta - row.successor.theta)
    print("mean |theta| error over 500 held-out steps:")
    print(f"  fitted model:  {model_error / len(sample):.6f} rad")
    print(f"  simulator:     {simulator_error / len(sample):.6f} rad  (the truth, so ~0)")
    print()
    probe = State(x=0.7, v=1.2, theta=0.05, omega=-0.4)
    print(f"probe state:   {probe}")
    print(f"model says:    {model.predict(probe, Action.RIGHT)}")
    print("note: velocities are reported unchanged, because this model cannot observe them.")


if __name__ == "__main__":
    main()
