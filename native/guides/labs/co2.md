# co2 — Atmospheric observations and windows

Read [industry/lessons/co2.md](../../../industry/lessons/co2.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [industry/notebooks/co2.ipynb](../../../industry/notebooks/co2.ipynb).

## Actual native experiment

Build complete past-only six-lag windows, keeping whole windows within chronological partitions.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `co2`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/industries/co2/data.csv`

## Run and practice

```
python native_course.py compare --lab co2 --output my_work/co2_compare01
python native_course.py prepare --lab co2 --output my_work/co2_practice01
```

## Three independent challenges

1. Define the independent observation unit for atmospheric time series and identify repeated groups.
2. Change one declared parameter in build complete past-only six-lag windows, keeping whole windows within chronological partitions. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: Historical data with missingness; no current atmospheric estimate or causal attribution.

## Boundaries and completion

**Historical data with missingness; no current atmospheric estimate or causal attribution.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
