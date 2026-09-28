# stage12 — Capstone: reproduce, defend, transfer, and audit the book

Read [lessons/12_lesson.md](../../../lessons/12_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/12_lab.ipynb](../../../notebooks/12_lab.ipynb).

## Actual native experiment

Train native softmax baselines on the supplied digit split: pixels, closed-pixel summaries, and their combination.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage12`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/digits.npz`
- `data/splits.json`

## Run and practice

```
python native_course.py compare --lab stage12 --output my_work/stage12_compare01
python native_course.py prepare --lab stage12 --output my_work/stage12_practice01
```

## Three independent challenges

1. Audit the exact train/validation/test IDs.
2. Derive the cross-entropy gradient and verify a finite difference.
3. Write a conclusion that allows the raw baseline to be best.

## Boundaries and completion

**This new optimizer and seven-feature descriptor do not reproduce the original scikit-learn notebook protocol. The exposed split lacks writer IDs.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
