# stage11 — Useful representations, Mapper, time windows, and honest machine learning

Read [lessons/11_lesson.md](../../../lessons/11_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/11_lab.ipynb](../../../notebooks/11_lab.ipynb).

## Actual native experiment

Construct a Mapper nerve from a scalar lens, overlapping cover, and radius-connected clusters of Iris samples.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage11`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/iris.csv`

## Run and practice

```
python native_course.py compare --lab stage11 --output my_work/stage11_compare01
python native_course.py prepare --lab stage11 --output my_work/stage11_practice01
```

## Three independent challenges

1. Change only cover overlap and retain every other parameter.
2. Construct an edge from overlap in observation IDs.
3. Explain why a pretty Mapper graph alone does not establish predictive utility.

## Boundaries and completion

**Mapper is not persistent homology; no equivalence to an underlying Reeb graph is certified.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
