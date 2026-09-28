# stage17 — Register, validate, and ask topology the right question

Read [lessons/17_lesson.md](../../../lessons/17_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/17_lab.ipynb](../../../notebooks/17_lab.ipynb).

## Actual native experiment

Recover a known similarity transformation by Horn quaternion alignment; fit 12 points and evaluate 12 different points.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage17`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab stage17 --output my_work/stage17_compare01
python native_course.py prepare --lab stage17 --output my_work/stage17_practice01
```

## Three independent challenges

1. Recover scale, proper rotation and translation separately.
2. Use collinear points to investigate identifiability.
3. Keep registration fitting references out of the evaluation set.

## Boundaries and completion

**These points and transformation are manufactured controls, not independent surveyed coordinates.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
