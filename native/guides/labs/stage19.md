# stage19 — From geometry to cautious interaction hypotheses

Read [lessons/19_lesson.md](../../../lessons/19_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/19_lab.ipynb](../../../notebooks/19_lab.ipynb).

## Actual native experiment

Execute a past-only sample-hold rule on a labeled manufactured event sequence with stale-data rejection.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage19`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage19 --output my_work/stage19_compare01
python native_course.py prepare --lab stage19 --output my_work/stage19_practice01
```

## Three independent challenges

1. Create a hand-near-ball hard negative.
2. Move a future observation and verify it cannot change a past-only decision.
3. Track onset time separately from confirmation time.

## Boundaries and completion

**Proximity and a threshold crossing do not prove possession or contact; no observed event precision/recall benchmark is claimed.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
