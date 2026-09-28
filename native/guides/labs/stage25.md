# stage25 — Constraints, projections, retractions and rank failure

Read [physics/lessons/25.md](../../../physics/lessons/25.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [physics/notebooks/25_lab.ipynb](../../../physics/notebooks/25_lab.ipynb).

## Actual native experiment

Apply iterative linearized corrections to a sphere constraint and record residual changes.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage25`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage25 --output my_work/stage25_compare01
python native_course.py prepare --lab stage25 --output my_work/stage25_practice01
```

## Three independent challenges

1. Calculate the residual after one step from (2,0).
2. Compare the Newton correction with radial normalization.
3. Construct a singular starting point and reject an unsupported inverse.

## Boundaries and completion

**One correction is not a general exact projection or geodesic; singular constraint Jacobians require an explicit policy.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
