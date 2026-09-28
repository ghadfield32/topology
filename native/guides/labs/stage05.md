# stage05 — Surfaces, simplices, triangulations, and pixel geometry

Read [lessons/05_lesson.md](../../../lessons/05_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/05_lab.ipynb](../../../notebooks/05_lab.ipynb).

## Actual native experiment

Construct triangular and tetrahedral boundaries/interiors and compute their ordinary F2 Betti numbers; inspect an observed pixel complex.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage05`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/digits.npz`
- `data/splits.json`

## Run and practice

```
python native_course.py compare --lab stage05 --output my_work/stage05_compare01
python native_course.py prepare --lab stage05 --output my_work/stage05_practice01
```

## Three independent challenges

1. Remove a required face and predict the validation error.
2. Explain how adding a triangular face changes H1.
3. Contrast a tetrahedron boundary with a filled tetrahedron.

## Boundaries and completion

**Surface-classification proofs and arbitrary mesh reconstruction are not implemented by this small complex builder.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
