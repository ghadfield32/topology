# Stage 25 — Constraints, projections, retractions and rank failure

## Begin with one question

**What problem does one projection step actually solve?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Constraint: an equation defining admissible states. Jacobian: local linear change. Retraction: a local manifold mapping with specified properties. Rank failure: loss of independent constraint information.

## Work the example before running it

For C(x)=x·x-1, linearize at (2,0). The residual is 3 and the Jacobian is (4,0). A minimum-norm correction solving the linearized equation subtracts (.75,0), leaving (1.25,0). Its original nonlinear constraint residual is .5625.

The step improved the residual without eliminating it. Iteration can help near a suitable solution; radial normalization happens to be exact for the sphere away from the origin. Neither method is an exact universal projection onto every nonlinear constraint set. At the origin, this Jacobian cannot determine the needed correction direction. Check rank, residual and physical meaning independently.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/25/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
from shape_lab.practice_v7 import sphere_newton_step
x=sphere_newton_step([2.,0.]);residual=x@x-1
assert np.allclose(x,[1.25,0.]) and np.isclose(residual,.5625)
print('One linearized correction:',x,'remaining residual:',residual)
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Transportation choice probabilities satisfy a sum constraint, but a sum-to-one vector is not automatically calibrated or causally meaningful. Constraint satisfaction is only one evaluation axis.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Enforcing one constraint can disturb another. A geometric projection need not preserve the integrator’s symplectic structure.

## Your independent answer

Why is solving the linearized constraint not the same as solving the nonlinear constraint?

<details><summary>Reveal answer criteria after your attempt</summary>

The Taylor approximation omits higher-order terms. Those terms remain after a finite correction unless the constraint is affine or another special property applies.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 25 learning section](../../stages/25/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/25.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
