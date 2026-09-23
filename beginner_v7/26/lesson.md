# Stage 26 — Physics-informed learning and inverse problems

## Begin with one question

**Can a function satisfy a differential equation but violate its boundary conditions?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

PINN: a network trained with differential-equation and other residuals. Collocation: locations where residuals are checked. Boundary condition: required behavior at the domain boundary.

## Work the example before running it

On [0,1], u=x(1-x) satisfies -u''=2 and u(0)=u(1)=0. Adding a constant five leaves the second derivative unchanged, so v=u+5 satisfies the same interior equation but violates both boundary values. Interior residual alone cannot identify the desired solution.

The lesson separates data, PDE, boundary and interface objectives. A small loss at sampled collocation points is not an exact theorem on an entire domain. Compare with an analytic or conventional numerical reference when one exists, and report held-out residuals and solution error. The retained Poisson PINN trains on a manufactured problem with a known solution; it is not a claim of industrial material-law recovery.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/26/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
u=lambda x:x*(1-x)
v=lambda x:u(x)+5
h=1e-3;x=.4
second=lambda f:(f(x+h)-2*f(x)+f(x-h))/h**2
assert np.isclose(-second(u),2.,atol=1e-6)
assert np.isclose(-second(v),2.,atol=1e-6)
assert u(0)==0 and v(0)==5
print('Same interior equation; different boundary values.')
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Concrete strength prediction is observed-data regression. Without a specified physical field, domain and equation, it is not transformed into a PINN merely by adding a regularization term.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Physics in the loss is not a guarantee that optimization found a physically valid or unique solution.

## Your independent answer

What extra information rules out u+5 in the worked boundary-value problem?

<details><summary>Reveal answer criteria after your attempt</summary>

The zero boundary conditions. They distinguish the desired solution from constant-shift alternatives with the same second derivative.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 26 learning section](../../stages/26/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/26.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
