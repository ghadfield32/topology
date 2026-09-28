# stage06 — Chains, boundaries, homology, and Betti numbers

Read [lessons/06_lesson.md](../../../lessons/06_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/06_lab.ipynb](../../../notebooks/06_lab.ipynb).

## Actual native experiment

Construct boundary matrices, compute their ranks over F2, verify boundary-of-boundary zero, and inspect digit persistence.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage06`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/digits.npz`
- `data/splits.json`

## Run and practice

```
python native_course.py compare --lab stage06 --output my_work/stage06_compare01
python native_course.py prepare --lab stage06 --output my_work/stage06_practice01
```

## Three independent challenges

1. Prove boundary-of-boundary zero on one oriented triangle.
2. Compute cycle and boundary dimensions before calling rank.
3. Make a one-edge complex and distinguish its cycle space from connected components.

## Boundaries and completion

**The displayed binary matrices use F2, not real signed-boundary homology.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
