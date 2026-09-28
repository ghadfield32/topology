# nile — Water-infrastructure time series

Read [industry/lessons/nile.md](../../../industry/lessons/nile.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [industry/notebooks/nile.ipynb](../../../industry/notebooks/nile.ipynb).

## Actual native experiment

Use six past annual measurements for chronological ridge forecasts and compare a mean baseline.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `nile`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/industries/nile/data.csv`

## Run and practice

```
python native_course.py compare --lab nile --output my_work/nile_compare01
python native_course.py prepare --lab nile --output my_work/nile_practice01
```

## Three independent challenges

1. Define the independent observation unit for water time series and identify repeated groups.
2. Change one declared parameter in use six past annual measurements for chronological ridge forecasts and compare a mean baseline. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: Volume units and annual aggregation matter; predictive change does not establish cause.

## Boundaries and completion

**Volume units and annual aggregation matter; predictive change does not establish cause.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
