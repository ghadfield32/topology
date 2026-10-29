"""WM03 — calculate one simulator step.

Rust sibling: `src/simulator.rs`, which returns `Result<State, String>`.

The equations are identical. What differs is how the bad case is expressed: Python raises,
Rust returns a value the caller must handle.
"""
from __future__ import annotations

import math

from .wm01_state import (
    DT,
    GRAVITY,
    HALF_LENGTH,
    MASS_CART,
    MASS_POLE,
    MAX_STEPS,
    State,
)
from .wm02_action import Action


def advance_position(position: float, velocity: float, dt: float) -> float:
    for name, value in (("position", position), ("velocity", velocity), ("dt", dt)):
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
    if dt <= 0:
        raise ValueError("dt must be positive")
    return position + velocity * dt


def step(state: State, action: Action) -> State:
    """One explicit-Euler step.

    Hand check, from rest and upright with a right push: `x` stays 0, `v` becomes 0.1951,
    `theta` stays 0, `omega` becomes -0.2927. Position and angle use the *old* velocities.

    Note `state.omega * state.omega` rather than `state.omega ** 2`. In Python those two are
    not always the same `float`: `**` goes through `pow`, which rounds differently from the
    multiply for about 0.06% of doubles. In a chaotic system one unit in the last place
    grows into a visibly different trajectory within a few hundred steps, so the two
    languages must use the *same* operation. Rust has the same distinction
    (`f64::powi` versus `*`), and `simulator.rs` also uses `*`.
    """
    total_mass = MASS_CART + MASS_POLE
    sin_theta, cos_theta = math.sin(state.theta), math.cos(state.theta)
    force = action.force()

    temp = (force + MASS_POLE * HALF_LENGTH * state.omega * state.omega * sin_theta) / total_mass
    angular_acceleration = (GRAVITY * sin_theta - cos_theta * temp) / (
        HALF_LENGTH * (4.0 / 3.0 - MASS_POLE * cos_theta * cos_theta / total_mass)
    )
    acceleration = temp - MASS_POLE * HALF_LENGTH * angular_acceleration * cos_theta / total_mass

    return State(
        x=state.x + DT * state.v,
        v=state.v + DT * acceleration,
        theta=state.theta + DT * state.omega,
        omega=state.omega + DT * angular_acceleration,
    )


def main() -> None:
    print(f"one position update: {advance_position(1.0, 0.4, 0.02)}")
    print(f"  by hand: 1.0 + 0.4 * 0.02 = {1.0 + 0.4 * 0.02}")
    print()
    for action in Action:
        nxt = step(State.upright(), action)
        print(f"from rest, push {action.name_lower():<5} -> x {nxt.x:+.6f}  v {nxt.v:+.6f}"
              f"  theta {nxt.theta:+.6f}  omega {nxt.omega:+.6f}")
    print()
    state = State.upright()
    survived = 0
    for _ in range(MAX_STEPS):
        action = Action.RIGHT if state.theta + 0.5 * state.omega > 0 else Action.LEFT
        state = step(state, action)
        survived += 1
        if state.failed():
            break
    print(f"hand controller survived {survived} of {MAX_STEPS} steps")
    print(f"final state: {state}")
    print()
    try:
        advance_position(0.0, 0.0, 0.0)
    except ValueError as problem:
        print(f"Rejected dt: {problem}")


if __name__ == "__main__":
    main()
