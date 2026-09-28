# stage10 — Stability, diagram distances, noise, and scientific uncertainty

Read [lessons/10_lesson.md](../../../lessons/10_lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [notebooks/10_lab.ipynb](../../../notebooks/10_lab.ipynb).

## Actual native experiment

Perturb the same observed image intensity function and measure diagram bottleneck distances in H0/H1.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage10`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/raw/digits.npz`
- `data/splits.json`

## Run and practice

```
python native_course.py compare --lab stage10 --output my_work/stage10_compare01
python native_course.py prepare --lab stage10 --output my_work/stage10_practice01
```

## Three independent challenges

1. Derive the sup-norm perturbation bound.
2. Compare a diagram with the empty diagram, accounting for diagonal matching.
3. Explain why unequal essential-class counts lead to infinite extended distance.

## Boundaries and completion

**The same-complex sublevel-set bound does not validate arbitrary preprocessing, correspondence, or semantic significance.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
