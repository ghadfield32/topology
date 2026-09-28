# stage04 — Groups, symmetries, paths, loops, and homotopy

Read [lessons/04_lesson.md](../../../lessons/04_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/04_lab.ipynb](../../../notebooks/04_lab.ipynb).

## Actual native experiment

Rotate an observed digit and compare its pixels and closed-pixel Betti numbers.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage04`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/digits.npz`
- `data/splits.json`

## Run and practice

```
python native_course.py compare --lab stage04 --output my_work/stage04_compare01
python native_course.py prepare --lab stage04 --output my_work/stage04_practice01
```

## Three independent challenges

1. Specify the rotation index map by hand.
2. Compare a reflection and a rotation for one digit.
3. Explain which transformation of a labeled 6 or 9 could invalidate the label.

## Boundaries and completion

**A geometric invariance is not necessarily a class-label invariance. General homotopy proofs remain written assignments.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
