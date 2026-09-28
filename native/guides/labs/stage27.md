# stage27 — Conflicting gradients, interfaces, separability and PIKANs

Read [physics/lessons/27.md](../../../physics/lessons/27.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [physics/notebooks/27_lab.ipynb](../../../physics/notebooks/27_lab.ipynb).

## Actual native experiment

Calculate gradient dot products, conflict projections and normalization on exact vector controls.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage27`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage27 --output my_work/stage27_compare01
python native_course.py prepare --lab stage27 --output my_work/stage27_practice01
```

## Three independent challenges

1. Show that opposite nonzero gradients have no common strict first-order descent direction.
2. Check what happens to a zero projected vector.
3. Separate an incorrect interface condition from an optimization conflict.

## Boundaries and completion

**The original Norm-PCGrad, ConFIG, SPINN, XPINN and PIKAN studies are not reproduced in full.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
