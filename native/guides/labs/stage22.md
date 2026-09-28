# stage22 — Smooth flows, coordinate changes and invertible networks

Read [physics/lessons/22.md](../../../physics/lessons/22.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [physics/notebooks/22_lab.ipynb](../../../physics/notebooks/22_lab.ipynb).

## Actual native experiment

Evaluate and invert the exact local flow of x-prime=x-squared before its blow-up time.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage22`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage22 --output my_work/stage22_compare01
python native_course.py prepare --lab stage22 --output my_work/stage22_practice01
```

## Three independent challenges

1. Derive x(t)=x0/(1-t*x0).
2. Explain the maximal time domain for positive x0.
3. Compare exact-flow invertibility with an arbitrary numerical step.

## Boundaries and completion

**This is not a general ODE solver or trained normalizing-flow model.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
