# seeds — Agriculture feature-space geometry

Read [applications_v7/seeds/lesson.md](../../../applications_v7/seeds/lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [applications_v7/seeds/lab.ipynb](../../../applications_v7/seeds/lab.ipynb).

## Actual native experiment

Classify measured kernel profiles; compare ordinary features and local shape summaries.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `seeds`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/v7/seeds/table.csv`

## Run and practice

```
python native_course.py compare --lab seeds --output my_work/seeds_compare01
python native_course.py prepare --lab seeds --output my_work/seeds_practice01
```

## Three independent challenges

1. Define the independent observation unit for agricultural kernels and identify repeated groups.
2. Change one declared parameter in classify measured kernel profiles and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: A feature-space loop is not a physical hole in a kernel.

## Boundaries and completion

**A feature-space loop is not a physical hole in a kernel.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
