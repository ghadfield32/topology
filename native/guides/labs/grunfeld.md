# grunfeld — Firm-year panel measurements

Read [industry/lessons/grunfeld.md](../../../industry/lessons/grunfeld.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [industry/notebooks/grunfeld.ipynb](../../../industry/notebooks/grunfeld.ipynb).

## Actual native experiment

Construct within-firm lagged observations and temporal partitions for ridge prediction.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `grunfeld`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/industries/grunfeld/data.csv`

## Run and practice

```
python native_course.py compare --lab grunfeld --output my_work/grunfeld_compare01
python native_course.py prepare --lab grunfeld --output my_work/grunfeld_practice01
```

## Three independent challenges

1. Define the independent observation unit for firm-year panels and identify repeated groups.
2. Change one declared parameter in construct within-firm lagged observations and temporal partitions for ridge prediction. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: Repeated firm identity is intentional; no causal investment claim.

## Boundaries and completion

**Repeated firm identity is intentional; no causal investment claim.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
