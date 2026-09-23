# Stage 15 — Measured stereo, calibration, and uncertainty

## Begin with one question

**Why can a small disparity error produce a large depth error?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Disparity: horizontal correspondence difference under a rectified convention. Baseline: camera separation. Principal point: intrinsic reference pixel. Sensitivity: derivative of output to input.

## Work the example before running it

Under the retained stereo convention, Z=fB/(d+delta_cx). Let f=1000 pixels, B=.1 metres, d=20 pixels and delta_cx=5 pixels. Depth is 100/25=4 metres. Omitting the offset would give five metres, a 25% error in this constructed example.

Differentiating gives dZ/dd=-fB/(d+delta_cx)². At our values it is -.16 metres per pixel. This is a local sensitivity, not a universal constant or a complete uncertainty budget. Calibration, synchronization, rectification, occlusion and correspondence failures can all contribute. Validate the forward model and actual measured conventions before propagating a single noise term.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/15/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
f,B,d,offset=1000.,.1,20.,5.
Z=lambda disparity: f*B/(disparity+offset)
sensitivity=-f*B/(d+offset)**2
h=1e-4;finite_difference=(Z(d+h)-Z(d-h))/(2*h)
assert np.isclose(Z(d),4.) and np.isclose(sensitivity,-.16)
assert np.isclose(sensitivity,finite_difference)
print('Depth:',Z(d),'local metres/pixel:',sensitivity)
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

The Middlebury case contains observed stereo images and supplied reference disparity. Its convention is documented. Manufactured perturbations are labeled as tests, not new measurements.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Low reprojection error alone can coexist with wrong scale or a weakly constrained configuration. Use independent measured holdouts.

## Your independent answer

What happens to depth sensitivity as a positive disparity denominator approaches zero?

<details><summary>Reveal answer criteria after your attempt</summary>

Its magnitude grows without bound in this idealized formula. This exposes poor depth conditioning and does not justify reporting arbitrarily confident distant geometry.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 15 learning section](../../stages/15/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/15.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
