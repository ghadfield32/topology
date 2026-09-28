# wdbc — Healthcare image-summary classification

Read [industry/lessons/wdbc.md](../../../industry/lessons/wdbc.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [industry/notebooks/wdbc.ipynb](../../../industry/notebooks/wdbc.ipynb).

## Actual native experiment

Classification from image-derived scalar measurements with training-only scaling and local topology.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `wdbc`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/industries/wdbc/data.csv`

## Run and practice

```
python native_course.py compare --lab wdbc --output my_work/wdbc_compare01
python native_course.py prepare --lab wdbc --output my_work/wdbc_practice01
```

## Three independent challenges

1. Define the independent observation unit for healthcare feature records and identify repeated groups.
2. Change one declared parameter in classification from image-derived scalar measurements with training-only scaling and local topology. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: Not the source images, patient-level clinical validation or a diagnostic service.

## Boundaries and completion

**Not the source images, patient-level clinical validation or a diagnostic service.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
