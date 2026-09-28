# poux_bridge — Poux spatial-AI Stage 01 weighted-streaming bridge

Read [curriculum/extensions/poux_spatial_ai/README.md](../../../curriculum/extensions/poux_spatial_ai/README.md) once, then the [shared language workflow](../LEARNING_PATHS.md). The original worked Python reference is [curriculum/extensions/poux_spatial_ai/bridge.py](../../../curriculum/extensions/poux_spatial_ai/bridge.py).

## Actual native experiment

Combine unequal batches of the existing SPL point excerpt with correct count weights; compare the wrong equal-weight mean.

Dispatch: [Go](../../go/engine/labs.go) and [Rust](../../rust/src/labs.rs), branch `poux_bridge`. Follow the helper calls rather than treating the dispatch file as the whole algorithm.

## Inputs

- `sports_v8/data/spl_selected_frames.json`

## Run and practice

```
python native_course.py compare --lab poux_bridge --output my_work/poux_bridge_compare01
python native_course.py prepare --lab poux_bridge --output my_work/poux_bridge_practice01
```

## Three independent challenges

1. Define the independent observation unit for streaming arithmetic and information and identify repeated groups.
2. Change one declared parameter in combine unequal batches of the existing spl point excerpt with correct count weights and predict its effect before running.
3. Design a comparison that could reject the claimed benefit; explain this limitation: Accumulator streaming is not file-streaming validation; selected-frame mean is not a time-average or release point.

## Boundaries and completion

**Accumulator streaming is not file-streaming validation; selected-frame mean is not a time-average or release point.**

Go/Rust native16 agreement is not a claim of every original Python operation being reproduced. Save your prediction, hand calculation, private code, observed output, controlled change and limitation. Explain what each language made explicit about memory, types, errors and algorithm choice. Delayed recall and independent reasoning remain unassessed until you demonstrate them. See [coverage](../../COVERAGE.md) for the precise scope.
