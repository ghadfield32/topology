# stage28 — Functions to functions: DeepONet, Fourier operators and baselines

Read [physics/lessons/28.md](../../../physics/lessons/28.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [physics/notebooks/28_lab.ipynb](../../../physics/notebooks/28_lab.ipynb).

## Actual native experiment

Train a small DeepONet and a three-mode spectral multiplier plus bias on manufactured periodic heat solutions.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage28`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage28 --output my_work/stage28_compare01
python native_course.py prepare --lab stage28 --output my_work/stage28_practice01
```

## Three independent challenges

1. Derive the heat attenuation of each Fourier mode.
2. Hold out whole functions, not random points from the same function.
3. Compare both learners with an exact operator and a zero/persistence baseline.

## Boundaries and completion

**The spectral learner is one real Fourier layer, not a multilayer FNO benchmark; function-level split and architecture differences remain explicit.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
