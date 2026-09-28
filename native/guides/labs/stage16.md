# stage16 — Attention and VGGT, from pixels to proposed geometry

Read [lessons/16_lesson.md](../../../lessons/16_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/16_lab.ipynb](../../../notebooks/16_lab.ipynb).

## Actual native experiment

Compute scaled dot-product attention from selected feature vectors and inspect row-normalized weights.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage16`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/iris.csv`

## Run and practice

```
python native_course.py compare --lab stage16 --output my_work/stage16_compare01
python native_course.py prepare --lab stage16 --output my_work/stage16_practice01
```

## Three independent challenges

1. Derive the dimensions of QK-transpose and attention*V.
2. Change an input token and inspect the affected outputs.
3. Explain why normalized weights are not physical conservation or metric calibration.

## Boundaries and completion

**No VGGT, Omega, pretrained image model, or video tracking inference is run by this unit.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
