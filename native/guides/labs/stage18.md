# stage18 — Make the pipeline efficient without changing the evidence

Read [lessons/18_lesson.md](../../../lessons/18_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/18_lab.ipynb](../../../notebooks/18_lab.ipynb).

## Actual native experiment

Compute whole-stream and count-weighted chunk means on the selected sports point records.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage18`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `sports_v8/data/spl_selected_frames.json`

## Run and practice

```
python native_course.py compare --lab stage18 --output my_work/stage18_compare01
python native_course.py prepare --lab stage18 --output my_work/stage18_practice01
```

## Three independent challenges

1. Combine unequal chunk sizes with counts.
2. Record file decode time separately from numerical kernel time.
3. Design a bounded queue before attempting concurrency; preserve row IDs.

## Boundaries and completion

**The JSON is loaded before accumulation; this is not industrial streaming I/O, a latency benchmark, or big-LiDAR validation.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
