# concrete_slump — Materials measurements and intervals

Read [applications_v7/concrete_slump/lesson.md](../../../applications_v7/concrete_slump/lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [applications_v7/concrete_slump/lab.ipynb](../../../applications_v7/concrete_slump/lab.ipynb).

## Actual native experiment

Train a ridge predictor and calibrate finite-sample absolute-residual intervals on separate rows.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `concrete_slump`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/v7/concrete_slump/table.csv`

## Run and practice

```
python native_course.py compare --lab concrete_slump --output my_work/concrete_slump_compare01
python native_course.py prepare --lab concrete_slump --output my_work/concrete_slump_practice01
```

## Three independent challenges

1. Define the independent observation unit for materials measurements and identify repeated groups.
2. Change one declared parameter in train a ridge predictor and calibrate finite-sample absolute-residual intervals on separate rows. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: Marginal illustrative coverage is not conditional coverage for every recipe or future batch.

## Boundaries and completion

**Marginal illustrative coverage is not conditional coverage for every recipe or future batch.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
