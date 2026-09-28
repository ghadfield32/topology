# stage20 — Independent spatial capstone and continuing mastery

Read [lessons/20_lesson.md](../../../lessons/20_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/20_lab.ipynb](../../../notebooks/20_lab.ipynb).

## Actual native experiment

Combine registration controls with derived SPL arm and motion summaries while keeping their source frames distinct.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage20`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `sports_v8/data/spl_selected_frames.json`

## Run and practice

```
python native_course.py compare --lab stage20 --output my_work/stage20_compare01
python native_course.py prepare --lab stage20 --output my_work/stage20_practice01
```

## Three independent challenges

1. Write an observation-to-claim table.
2. Identify which coordinate frames cannot be combined without registration.
3. Predeclare a useful baseline and a result that would reject the proposed method.

## Boundaries and completion

**Independent static-scene acquisition, camera calibration, and physical holdouts remain the learner capstone.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
