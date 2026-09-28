# stage01 — Mathematical language, proofs, and linear algebra

Read [lessons/01_lesson.md](../../../lessons/01_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/01_lab.ipynb](../../../notebooks/01_lab.ipynb).

## Actual native experiment

Calculate real and F2 rank, construct the augmented Iris column 2*x0-3*x1, and test its null vector.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage01`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/iris.csv`

## Run and practice

```
python native_course.py compare --lab stage01 --output my_work/stage01_compare01
python native_course.py prepare --lab stage01 --output my_work/stage01_practice01
```

## Three independent challenges

1. Derive the null vector before running: the last column is 2*x0-3*x1.
2. Replace a pivot with a nearly dependent value and study tolerance sensitivity.
3. In Go explain outer versus inner slice copies; in Rust explain who owns the elimination matrix.

## Boundaries and completion

**The fixed numerical tolerance is not calibrated biological measurement uncertainty.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
