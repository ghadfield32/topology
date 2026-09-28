# stage00 — Start here: how to learn, run, and question the results

Read [lessons/00_lesson.md](../../../lessons/00_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/00_lab.ipynb](../../../notebooks/00_lab.ipynb).

## Actual native experiment

Read Seeds measurements, exclude the source ID and class label, calculate column means and class counts.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage00`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/v7/seeds/table.csv`

## Run and practice

```
python native_course.py compare --lab stage00 --output my_work/stage00_compare01
python native_course.py prepare --lab stage00 --output my_work/stage00_practice01
```

## Three independent challenges

1. Reorder the rows and explain which outputs should change.
2. Introduce an empty selected numeric value in a private fixture; specify reject versus exclude.
3. Explain why row count is not a count of independent experiments.

## Boundaries and completion

**Dataset inspection is not a trained classifier or independent learning assessment.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
