# claims — Physical-claim counterexamples

Read [methods_v7/claims/lesson.md](../../../methods_v7/claims/lesson.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [methods_v7/claims/lab.ipynb](../../../methods_v7/claims/lab.ipynb).

## Actual native experiment

Combine oscillator, constraint and conflicting-gradient controls to examine broad guarantees.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `claims`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

Explicitly manufactured control; no measured payload consumed.

## Run and practice

```
python native_course.py compare --lab claims --output my_work/claims_compare01
python native_course.py prepare --lab claims --output my_work/claims_practice01
```

## Three independent challenges

1. Define the independent observation unit for claims versus counterexamples and identify repeated groups.
2. Change one declared parameter in combine oscillator, constraint and conflicting-gradient controls to examine broad guarantees. and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: An isolated counterexample refutes a universal statement but does not rank every architecture.

## Boundaries and completion

**An isolated counterexample refutes a universal statement but does not rank every architecture.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
