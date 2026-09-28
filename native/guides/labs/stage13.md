# stage13 — From topology to smooth manifolds

Read [lessons/13_lesson.md](../../../lessons/13_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/13_lab.ipynb](../../../notebooks/13_lab.ipynb).

## Actual native experiment

Calculate a stereographic sphere chart and its inverse on manufactured points.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage13`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage13 --output my_work/stage13_compare01
python native_course.py prepare --lab stage13 --output my_work/stage13_practice01
```

## Three independent challenges

1. Name the chart domain and codomain precisely.
2. Move toward the excluded pole and inspect conditioning.
3. Derive one Jacobian entry and compare a centered difference.

## Boundaries and completion

**The excluded pole remains excluded. Perspective cameras are not invertible charts of a full 3D scene.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
