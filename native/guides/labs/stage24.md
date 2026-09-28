# stage24 — Symplectic integration, energy, phase and long rollouts

Read [physics/lessons/24.md](../../../physics/lessons/24.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [physics/notebooks/24_lab.ipynb](../../../physics/notebooks/24_lab.ipynb).

## Actual native experiment

Compare explicit Euler, symplectic Euler, Verlet, implicit midpoint and RK4 for the same harmonic oscillator.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage24`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage24 --output my_work/stage24_compare01
python native_course.py prepare --lab stage24 --output my_work/stage24_practice01
```

## Three independent challenges

1. Derive the first symplectic Euler step.
2. Compare phase error and energy error separately.
3. Increase the step size until a method fails and report it honestly.

## Boundaries and completion

**Symplecticity and exact energy conservation are different; a harmonic control does not validate arbitrary dissipative systems.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
