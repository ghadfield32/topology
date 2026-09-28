# acb — ACB 2025–26 source and identity readiness

Read [sports_v9/lesson.md](../../../sports_v9/lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [sports_v9/notebooks/acb_readiness.ipynb](../../../sports_v9/notebooks/acb_readiness.ipynb).

## Actual native experiment

Read the ten-game source catalog, retain chronology and explicit competition identifiers.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `acb`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `sports_v9/data/matches.json`

## Run and practice

```
python native_course.py compare --lab acb --output my_work/acb_compare01
python native_course.py prepare --lab acb --output my_work/acb_practice01
```

## Three independent challenges

1. Define the independent observation unit for basketball metadata and identify repeated groups.
2. Change one declared parameter in read the ten-game source catalog, retain chronology and explicit competition identifiers. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: Metadata is not full tracking/events/season aggregates; no hidden acquisition occurs.

## Boundaries and completion

**Metadata is not full tracking/events/season aggregates; no hidden acquisition occurs.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
