"""WM02 — represent the allowed actions.

Rust sibling: `src/action.rs`, an `enum` with an exhaustive `match`.

The Python version is an `Enum`, and it is *almost* the same idea. The difference is who
checks it: Rust refuses to compile a `match` that forgets a case, and refuses to construct an
action from an integer that is not 0 or 1. Python's `Enum` prevents the bad integer at run
time, which is later, but still better than a bare `int`.
"""
from __future__ import annotations

from enum import IntEnum

MAGNITUDE = 10.0


class Action(IntEnum):
    """Two shoves, no third option. The integer value is the recorded index."""

    LEFT = 0
    RIGHT = 1

    def force(self) -> float:
        # No exhaustive `match` in Python: this is a lookup, and adding a variant without
        # updating it raises KeyError at run time rather than failing to compile.
        return _FORCES[self]

    def name_lower(self) -> str:
        return self.name.lower()


_FORCES = {Action.LEFT: -MAGNITUDE, Action.RIGHT: MAGNITUDE}


def from_index(index: int) -> Action:
    try:
        return Action(index)
    except ValueError as error:
        raise ValueError(f"action index {index} is not 0 or 1") from error


def main() -> None:
    for action in Action:
        print(f"{action.name_lower():<6} {action.force():>5.0f} N  (index {int(action)})")
    print()
    print("An action is what you can do now. A goal is what you want. They are different")
    print("kinds of thing, and encoding both as integers loses that distinction.")
    print()
    print("Recovering an action from a recorded index:")
    for index in range(3):
        try:
            print(f"  {index} -> {from_index(index).name_lower()}")
        except ValueError as problem:
            print(f"  {index} -> rejected: {problem}")


if __name__ == "__main__":
    main()
