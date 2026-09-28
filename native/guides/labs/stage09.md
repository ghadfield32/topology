# stage09 — Implement persistence, trace the algorithm, and test it independently

Read [lessons/09_lesson.md](../../../lessons/09_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/09_lab.ipynb](../../../notebooks/09_lab.ipynb).

## Actual native experiment

Execute sparse F2 boundary-column reduction and compare H0 intervals with a separate Prim spanning-tree implementation.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage09`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/iris.csv`

## Run and practice

```
python native_course.py compare --lab stage09 --output my_work/stage09_compare01
python native_course.py prepare --lab stage09 --output my_work/stage09_practice01
```

## Three independent challenges

1. Trace every XOR operation on a small filtration.
2. Build a malformed filtration and explain the rejected invariant.
3. Compare with the retained Python implementation and explain shared-bug risk.

## Boundaries and completion

**This educational enumerator caps input and simplex counts; it is not a replacement for an optimized large-scale persistence library.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
