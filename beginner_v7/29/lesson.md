# Stage 29 — Differentiable simulation, graph physics and attention constraints

## Begin with one question

**What exactly does differentiating through a simulator give you?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Sensitivity: derivative of output with respect to a parameter. Differentiable simulation: propagating derivatives through implemented operations. Identifiability: uniqueness supported by observations.

## Work the example before running it

For x(t)=exp(-ct), derivative with respect to damping c is -t exp(-ct). At c=.3,t=2 this is about -1.098. A central difference in c checks the implementation locally. The derivative concerns this specified model; it does not establish that the physical system actually obeys exponential decay.

Differentiating through a discrete solver returns sensitivities of that discretization. Tolerance, truncation, contact discontinuities and parameterization can matter. A successful gradient check is necessary evidence for many implementations, but it is not proof that an inverse problem is identifiable or that optimization found the intended parameters.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/29/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
c,t=.3,2.;h=1e-5
f=lambda value:np.exp(-value*t)
analytic=-t*f(c);numeric=(f(c+h)-f(c-h))/(2*h)
assert np.isclose(analytic,numeric,rtol=1e-8)
print('Sensitivity:',analytic,'finite difference:',numeric)
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

The observed material regression and manufactured damping identification remain distinct experiments. A graph’s zero total exchange test does not establish physical correctness of every local flux.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

An exactly conserved global sum can conceal wrong spatial transport. Check the local solution and boundary conditions too.

## Your independent answer

What does disagreement between automatic differentiation and a well-conditioned finite-difference check suggest?

<details><summary>Reveal answer criteria after your attempt</summary>

A possible implementation, convention, differentiation-path or numerical-step issue that needs investigation. It does not by itself identify which method is wrong.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 29 learning section](../../stages/29/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/29.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
