# stage14 — Rotations, rigid transforms, and the camera model

Read [lessons/14_lesson.md](../../../lessons/14_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/14_lab.ipynb](../../../notebooks/14_lab.ipynb).

## Actual native experiment

Normalize a quaternion, compute its rotation matrix, and project/unproject a manufactured point with supplied stereo intrinsics.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage14`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/stereo/calibration.json`

## Run and practice

```
python native_course.py compare --lab stage14 --output my_work/stage14_compare01
python native_course.py prepare --lab stage14 --output my_work/stage14_practice01
```

## Three independent challenges

1. Verify R-transpose R=I and determinant +1.
2. Reverse transform composition order and explain the different result.
3. Convert units without accidentally changing dimensionless pixel quantities.

## Boundaries and completion

**Unprojection requires supplied depth. This does not recover depth from a single pixel.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
