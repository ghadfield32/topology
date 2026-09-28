# stage26 — Physics-informed learning and inverse problems

Read [physics/lessons/26.md](../../../physics/lessons/26.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [physics/notebooks/26_lab.ipynb](../../../physics/notebooks/26_lab.ipynb).

## Actual native experiment

Train a native scalar Poisson PINN with hard endpoint factors and compare its solution with the manufactured analytic sine solution.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage26`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage26 --output my_work/stage26_compare01
python native_course.py prepare --lab stage26 --output my_work/stage26_practice01
```

## Three independent challenges

1. Derive the forcing and boundary conditions.
2. Test second derivatives independently before training.
3. Compare residual, solution error, and a finite-difference baseline.

## Boundaries and completion

**Not an inverse real-data PDE, multidomain solver, or full PIKAN/XPINN benchmark.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
