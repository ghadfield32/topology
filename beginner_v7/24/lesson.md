# Stage 24 — Symplectic integration, energy, phase and long rollouts

## Begin with one question

**Does preserving symplectic structure preserve the exact energy value each step?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Symplectic: preserving the canonical two-form. Energy: the specified Hamiltonian value. Phase error: timing or angular error along a trajectory. Stability region: step/system conditions.

## Work the example before running it

For the unit oscillator, kick-drift symplectic Euler is A=[[1-h²,h],[-h,1]]. With h=.2 it preserves A^T J A=J, but at state (1,0) energy changes from .5 to .4808. Both statements can be true at once.

The source post made a stronger discrete-step energy claim. We preserve it as an attributed claim and supply this separate original counterexample. The useful long-time properties of particular symplectic methods have hypotheses; they do not imply exact energy, exact phase or unconditional stability for arbitrary step sizes and learned models. The full stage compares several maps and reports those properties separately.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/24/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
from shape_lab.practice_v7 import symplectic_defect,oscillator_energy
h=.2;A=np.array([[1-h*h,h],[-h,1.]])
assert symplectic_defect(A)<1e-14
assert np.isclose(oscillator_energy(A@np.array([1.,0.])),.4808)
print('Symplectic condition passes; exact-energy condition does not.')
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

The marine-climate series can motivate long-horizon evaluation, but this manufactured oscillator is not an atmospheric or ocean model. Do not transfer conservation claims without a governing model.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Volume preservation is not synonymous with symplecticity in every dimension; exact energy is another distinct property.

## Your independent answer

Why should an evaluation report both trajectory error and energy error?

<details><summary>Reveal answer criteria after your attempt</summary>

A trajectory can remain near an energy level while accumulating phase or state error. Conversely, energy changes can be physically appropriate in a driven or dissipative system.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 24 learning section](../../stages/24/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/24.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
