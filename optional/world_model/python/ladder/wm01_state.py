"""WM01 — represent the world with a dataclass (Python's answer to a `struct`).

Rust sibling: `src/state.rs`. Same constants, same field names.

The difference worth noticing: an ordinary Python annotation is **not** a compile-time
constraint. `State(x="zero")` runs happily until something tries to add it. `dataclass` gives
you the naming and the printing, not the checking.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

DT = 0.02
GRAVITY = 9.8
MASS_CART = 1.0
MASS_POLE = 0.1
HALF_LENGTH = 0.5
FORCE_MAG = 10.0
X_LIMIT = 2.4
THETA_LIMIT = 12.0 * 2.0 * math.pi / 360.0  # 0.20943951023931953
MAX_STEPS = 500


@dataclass(frozen=True)
class State:
    """The complete four-number state.

    Frozen because a state is a value: two transitions should never share a mutable object
    and quietly affect each other. Rust gets the same guarantee from `Copy` on four `f64`.
    """

    x: float
    v: float
    theta: float
    omega: float

    def __post_init__(self) -> None:
        # Python has no compiler checking this, so it has to be written down. Rust's `new`
        # does the same job with the same rule.
        for name, value in (("x", self.x), ("v", self.v),
                            ("theta", self.theta), ("omega", self.omega)):
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite, got {value}")

    @classmethod
    def upright(cls) -> "State":
        return cls(x=0.0, v=0.0, theta=0.0, omega=0.0)

    def visible(self) -> tuple[float, float]:
        """The two numbers a camera could report: where, never how fast."""
        return (self.x, self.theta)

    def failed(self) -> bool:
        """Ended by falling. The step limit is a different fact and is not decided here."""
        return abs(self.x) > X_LIMIT or abs(self.theta) > THETA_LIMIT

    def normalized(self) -> tuple[float, float]:
        return (self.x / X_LIMIT, self.theta / THETA_LIMIT)


def from_normalized(values: tuple[float, float]) -> tuple[float, float]:
    return (values[0] * X_LIMIT, values[1] * THETA_LIMIT)


def main() -> None:
    state = State(x=0.0, v=0.0, theta=0.02, omega=0.0)
    print(f"position:          {state.x} m")
    print(f"velocity:          {state.v} m/s")
    print(f"angle:             {state.theta} rad")
    print(f"angular velocity:  {state.omega} rad/s")
    print()
    print(f"Failing if |x| > {X_LIMIT} m or |theta| > {THETA_LIMIT} rad")
    print(f"failed right now:  {state.failed()}")
    print()
    (x, theta) = state.visible()
    print(f"visible (camera):  x = {x} m, theta = {theta} rad")
    print(f"normalized:        {state.normalized()}")
    print()
    moving = State(x=0.0, v=1.7, theta=0.02, omega=-2.5)
    print("another state with the same visible pair:")
    print(f"  visible:         {moving.visible()}")
    print(f"  full state:      {moving}")
    print(f"  states equal?    {state == moving}")
    print()
    print("Why this matters: two worlds can look identical in two numbers and behave")
    print("differently under the same action. That is the reason the article needs memory,")
    print("and the reason this ladder starts with the complete state instead.")


if __name__ == "__main__":
    main()
