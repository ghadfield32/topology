# elnino — Marine climate

Read [industry/lessons/elnino.md](../../../industry/lessons/elnino.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [industry/notebooks/elnino.ipynb](../../../industry/notebooks/elnino.ipynb).

## Actual native experiment

Reshape the monthly historical series and construct leakage-conscious lagged forecasts.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `elnino`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/industries/elnino/data.csv`

## Run and practice

```
python native_course.py compare --lab elnino --output my_work/elnino_compare01
python native_course.py prepare --lab elnino --output my_work/elnino_practice01
```

## Three independent challenges

1. Define the independent observation unit for marine climate and identify repeated groups.
2. Change one declared parameter in reshape the monthly historical series and construct leakage-conscious lagged forecasts. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: No multivariate climate model or chronological-period generality is certified.

## Boundaries and completion

**No multivariate climate model or chronological-period generality is certified.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
