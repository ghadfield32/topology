# Stage 27 — Conflicting gradients, interfaces, separability and PIKANs

## Begin with one question

**Can an optimizer always decrease every objective at once?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Gradient conflict: objective gradients point in opposing directions. Domain decomposition: solving interacting subdomains. Interface condition: compatibility across subdomain boundaries.

## Work the example before running it

If g1=(1,0) and g2=(-1,0), an update -ηd decreases both objectives strictly to first order only when d1>0 and -d1>0. That is impossible. This exact local incompatibility cannot be removed by giving a gradient method a stronger name.

The supplied paper reports Norm-PCGrad improvements on its benchmarks and discusses PINN/PIKAN domain-decomposition failures. Preserve that empirical scope. Tests of small projection operations are not full benchmark replications. Wrong interface conditions, incorrect units or inconsistent boundary constraints must be corrected in the mathematical problem rather than hidden by changing loss weights.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/27/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
from shape_lab.practice_v7 import gradient_inner_product
g=np.array([1.,0.]);other=-g
assert gradient_inner_product(g,other)==-1.
for a in [-2.,-1.,0.,1.,2.]:
    assert not (a>0 and -a>0)
print('Opposite gradients admit no strictly common first-order descent direction.')
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Observed small manufacturing data can teach noisy objectives, but the supplied 2D/3D PDE benchmarks are not reproduced by a 21-row regression table.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Fewer operations for a separable mathematical form do not establish end-to-end hardware speedup at equal accuracy.

## Your independent answer

What evidence is needed to claim one gradient method outperforms another on a new PDE problem?

<details><summary>Reveal answer criteria after your attempt</summary>

A specified PDE/domain/interface setup, matched model capacity/data/compute and tuning policy, held-out solution/residual metrics, repeated runs where appropriate, and reproduced timing rather than copied benchmark headlines.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 27 learning section](../../stages/27/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/27.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
