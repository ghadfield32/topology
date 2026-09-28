# stackloss — Manufacturing regression

Read [industry/lessons/stackloss.md](../../../industry/lessons/stackloss.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [industry/notebooks/stackloss.ipynb](../../../industry/notebooks/stackloss.ipynb).

## Actual native experiment

Fit ridge regression to the small observed plant-day table and compare a training-mean baseline.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stackloss`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/industries/stackloss/data.csv`

## Run and practice

```
python native_course.py compare --lab stackloss --output my_work/stackloss_compare01
python native_course.py prepare --lab stackloss --output my_work/stackloss_practice01
```

## Three independent challenges

1. Define the independent observation unit for manufacturing days and identify repeated groups.
2. Change one declared parameter in fit ridge regression to the small observed plant-day table and compare a training-mean baseline. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: Few observations and a random split do not establish future operational forecasting.

## Boundaries and completion

**Few observations and a random split do not establish future operational forecasting.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
