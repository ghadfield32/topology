# modechoice — Traveler-level choice sets

Read [industry/lessons/modechoice.md](../../../industry/lessons/modechoice.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [industry/notebooks/modechoice.ipynb](../../../industry/notebooks/modechoice.ipynb).

## Actual native experiment

Train a conditional choice softmax while keeping complete alternative sets grouped by traveler.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `modechoice`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `data/industries/modechoice/data.csv`

## Run and practice

```
python native_course.py compare --lab modechoice --output my_work/modechoice_compare01
python native_course.py prepare --lab modechoice --output my_work/modechoice_practice01
```

## Three independent challenges

1. Define the independent observation unit for grouped transport alternatives and identify repeated groups.
2. Change one declared parameter in train a conditional choice softmax while keeping complete alternative sets grouped by traveler. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: Choice-based sampling and unidentified population parameters limit interpretation.

## Boundaries and completion

**Choice-based sampling and unidentified population parameters limit interpretation.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
