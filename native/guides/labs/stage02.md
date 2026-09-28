# stage02 — Closeness, metrics, neighborhoods, and topologies

Read [lessons/02_lesson.md](../../../lessons/02_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/02_lab.ipynb](../../../notebooks/02_lab.ipynb).

## Actual native experiment

Compare L1, L2, and L-infinity distances and radius-graph components on 24 scaled Iris records. Scaling is fitted on the first 90 records.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage02`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/iris.csv`

## Run and practice

```
python native_course.py compare --lab stage02 --output my_work/stage02_compare01
python native_course.py prepare --lab stage02 --output my_work/stage02_practice01
```

## Three independent challenges

1. Derive the squared-distance triangle-inequality counterexample.
2. Scale only one feature and predict its effect on neighbors.
3. Check translation invariance without refitting unrelated preprocessing.

## Boundaries and completion

**This is descriptive geometry of selected feature vectors, not a discovered biological manifold.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
