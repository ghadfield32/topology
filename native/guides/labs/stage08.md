# stage08 — Persistent homology, persistence modules, and reading diagrams

Read [lessons/08_lesson.md](../../../lessons/08_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/08_lab.ipynb](../../../notebooks/08_lab.ipynb).

## Actual native experiment

Reduce a square and a real-data Rips complex, reporting intervals and independent MST H0 death times.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage08`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/iris.csv`

## Run and practice

```
python native_course.py compare --lab stage08 --output my_work/stage08_compare01
python native_course.py prepare --lab stage08 --output my_work/stage08_practice01
```

## Three independent challenges

1. Predict the square H1 interval [1,sqrt(2)).
2. Explain how multiplicity is preserved in a diagram.
3. Reorder points and compare interval multisets, not simplex IDs.

## Boundaries and completion

**Persistence outside the constructed filtration is unknown; an essential-at-cutoff bar is not eternal truth.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
