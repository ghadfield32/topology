# stage03 — Continuity, homeomorphisms, connectedness, and compactness

Read [lessons/03_lesson.md](../../../lessons/03_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/03_lab.ipynb](../../../notebooks/03_lab.ipynb).

## Actual native experiment

Enumerate topologies on a labeled three-element set and count collisions after projecting Iris to two columns.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage03`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/iris.csv`

## Run and practice

```
python native_course.py compare --lab stage03 --output my_work/stage03_compare01
python native_course.py prepare --lab stage03 --output my_work/stage03_practice01
```

## Three independent challenges

1. Explain why there are eight subsets before enumerating candidate families.
2. Construct a projection that is not injective.
3. Prove the inverse-image intersection identity without relying on a finite test.

## Boundaries and completion

**Finite exhaustive checks do not prove an arbitrary continuity or compactness theorem.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
