# stage30 — An independent world-model study: evidence before adoption

Read [physics/lessons/30.md](../../../physics/lessons/30.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [physics/notebooks/30_lab.ipynb](../../../physics/notebooks/30_lab.ipynb).

## Actual native experiment

Run trained damping and nonlinear-constraint controls as executable prerequisites for a separately designed observed-system study.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage30`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage30 --output my_work/stage30_compare01
python native_course.py prepare --lab stage30 --output my_work/stage30_practice01
```

## Three independent challenges

1. Freeze the question, data split and metric before the final experiment.
2. Document where the proposed physical law can fail.
3. Report a negative result without changing the claimed task afterward.

## Boundaries and completion

**Passing these controls does not complete an independent world-model research project.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
