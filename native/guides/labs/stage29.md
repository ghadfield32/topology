# stage29 — Differentiable simulation, graph physics and attention constraints

Read [physics/lessons/29.md](../../../physics/lessons/29.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [physics/notebooks/29_lab.ipynb](../../../physics/notebooks/29_lab.ipynb).

## Actual native experiment

Fit damping through a native differentiable scalar flow and test a row-stochastic mass counterexample.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage29`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage29 --output my_work/stage29_compare01
python native_course.py prepare --lab stage29 --output my_work/stage29_practice01
```

## Three independent challenges

1. Derive the state sensitivity to damping.
2. Check finite differences of the parameter gradient.
3. Explain why row-stochastic attention does not necessarily preserve total mass.

## Boundaries and completion

**No trained physics-informed GNN or transformer, and no real noisy-system identification is claimed.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
