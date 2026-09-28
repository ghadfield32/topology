# leakage — Identity leakage controls

Read [methods_v7/leakage/lesson.md](../../../methods_v7/leakage/lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [methods_v7/leakage/lab.ipynb](../../../methods_v7/leakage/lab.ipynb).

## Actual native experiment

Copy observed Seeds rows three times and contrast row versus source-group partitions.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `leakage`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/v7/seeds/table.csv`

## Run and practice

```
python native_course.py compare --lab leakage --output my_work/leakage_compare01
python native_course.py prepare --lab leakage --output my_work/leakage_practice01
```

## Three independent challenges

1. Define the independent observation unit for constructed leakage control and identify repeated groups.
2. Change one declared parameter in copy observed seeds rows three times and contrast row versus source-group partitions. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: Copies are constructed records, not newly observed independent kernels.

## Boundaries and completion

**Copies are constructed records, not newly observed independent kernels.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
