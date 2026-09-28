# stage21 — Rates, equations, units and what data can identify

Read [physics/lessons/21.md](../../../physics/lessons/21.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [physics/notebooks/21_lab.ipynb](../../../physics/notebooks/21_lab.ipynb).

## Actual native experiment

Fit a small observed copper-response ridge baseline and check analytic-versus-finite-difference derivatives.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `stage21`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/physics/hahn1_excerpt.csv`

## Run and practice

```
python native_course.py compare --lab stage21 --output my_work/stage21_compare01
python native_course.py prepare --lab stage21 --output my_work/stage21_practice01
```

## Three independent challenges

1. Vary finite-difference step and explain truncation versus rounding.
2. State the predictor units and which response convention is unresolved.
3. Design two parameter choices that observations cannot distinguish.

## Boundaries and completion

**The copper excerpt is not a PDE field dataset; a regression slope is not automatically an identified physical parameter.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
