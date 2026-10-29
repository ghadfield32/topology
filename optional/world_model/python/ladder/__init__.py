"""WM01–WM09 in Python: the same steps, so the comparison is about the languages.

Each module mirrors the Rust module of the same name in `../../rust_ladder/src/`. Same
feature order, same numbers, same tolerances. That is deliberate: if the two disagree on a
number, one of them has a bug, and the disagreement is the lesson.

Python is the *reference* for the mathematics. Rust is the *second implementation*, and its
job is to make ownership, types and explicit error handling visible rather than to be faster.

Run any rung with `python -m ladder.wmNN_name` from `optional/world_model/python`.

Not a second curriculum, and not assessed.
"""
