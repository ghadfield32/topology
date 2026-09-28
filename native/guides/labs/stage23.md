# stage23 — Mechanics, Hamiltonian networks and Lagrangian networks

Read [physics/lessons/23.md](../../../physics/lessons/23.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [physics/notebooks/23_lab.ipynb](../../../physics/notebooks/23_lab.ipynb).

## Actual native experiment

Train tanh networks with derivatives obtained by forward second-order jets over a reverse-mode parameter tape. HNN fits both Hamiltonian derivatives; LNN fixes unit mass and learns potential.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage23`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage23 --output my_work/stage23_compare01
python native_course.py prepare --lab stage23 --output my_work/stage23_practice01
```

## Three independent challenges

1. Check one parameter gradient against finite differences.
2. Inspect derivative fit error separately from long-rollout error.
3. Explain which Legendre-transform regularity assumption this restricted model avoids.

## Boundaries and completion

**Manufactured oscillator data and small architectures; no general velocity-dependent Lagrangian, constraint solver, or full-paper replication.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
