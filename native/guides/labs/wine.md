# wine — Food chemistry and topology

Read [industry/lessons/wine.md](../../../industry/lessons/wine.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [industry/notebooks/wine.ipynb](../../../industry/notebooks/wine.ipynb).

## Actual native experiment

Cultivar classification with native softmax and local topological descriptors.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `wine`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/industries/wine/data.csv`

## Run and practice

```
python native_course.py compare --lab wine --output my_work/wine_compare01
python native_course.py prepare --lab wine --output my_work/wine_practice01
```

## Three independent challenges

1. Define the independent observation unit for chemical profiles and identify repeated groups.
2. Change one declared parameter in cultivar classification with native softmax and local topological descriptors. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: Different split/solver from the original notebook; fixed exposed demonstration only.

## Boundaries and completion

**Different split/solver from the original notebook; fixed exposed demonstration only.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
