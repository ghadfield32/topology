# stage07 — From data to shape: Rips, Čech, alpha, and filtrations

Read [lessons/07_lesson.md](../../../lessons/07_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/07_lab.ipynb](../../../notebooks/07_lab.ipynb).

## Actual native experiment

Build a bounded Rips filtration on selected real measurements and compare exact pairwise/common-intersection thresholds for an equilateral triangle.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage07`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/iris.csv`

## Run and practice

```
python native_course.py compare --lab stage07 --output my_work/stage07_compare01
python native_course.py prepare --lab stage07 --output my_work/stage07_practice01
```

## Three independent challenges

1. Explain why pairwise ball overlap is weaker than common overlap.
2. Derive radius 2/sqrt(3) for the side-two equilateral control.
3. Change the Rips edge cutoff and report surviving-at-cutoff classes separately.

## Boundaries and completion

**No general native Cech/alpha/Delaunay construction is claimed. Top-dimensional truncated-complex classes are not recovered H2 evidence.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
