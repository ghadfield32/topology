# stage15 — Measured stereo, calibration, and uncertainty

Read [lessons/15_lesson.md](../../../lessons/15_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/15_lab.ipynb](../../../notebooks/15_lab.ipynb).

## Actual native experiment

Decode real RGB PNGs and NPZ reference disparity natively, run 5x5 SAD on 80 requested pixels, and compare eligible predictions.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage15`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/stereo/calibration.json`
- `data/stereo/left.png`
- `data/stereo/motorcycle.npz`
- `data/stereo/right.png`

## Run and practice

```
python native_course.py compare --lab stage15 --output my_work/stage15_compare01
python native_course.py prepare --lab stage15 --output my_work/stage15_practice01
```

## Three independent challenges

1. Compare requested, eligible, and successful measurement counts.
2. Remove the principal-point correction only in a private control.
3. Report mean, median and bad-pixel rate instead of one favorable summary.

## Boundaries and completion

**This is an intentionally weak local matcher, not full-image reconstruction, calibration recovery, or uncertainty-certified depth.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
