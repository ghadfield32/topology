# Stage 23 — Mechanics, Hamiltonian networks and Lagrangian networks

## Begin with one question

**When are momentum and velocity different numbers?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Lagrangian: a function of position and velocity. Momentum: derivative of L with respect to velocity. Hamiltonian: the Legendre-transformed function when the transformation is regular.

## Work the example before running it

For L(q,v)=m v²/2-k q²/2 with positive mass, momentum is p=m v. When m=2 and v=.4, p=.8, not .4. The Hamiltonian computed as pv-L is m v²/2+k q²/2. For q=.3 and k=3 it is .295.

Recovering v from p requires an invertible relation. In more general learned Lagrangians, the velocity Hessian may be singular or ill-conditioned. A constrained or dissipative system may require additional structure. The retained small LNN example is explicitly restricted; it is not a full reproduction of every general Lagrangian architecture.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/23/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
m,k,q,v=2.,3.,.3,.4
p=m*v;L=.5*m*v*v-.5*k*q*q;H=p*v-L
assert np.isclose(p,.8) and np.isclose(H,.295)
assert np.isclose(H,p*p/(2*m)+.5*k*q*q)
print('Momentum:',p,'Hamiltonian:',H)
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Manufactured oscillator trajectories make dynamics derivatives testable. Static Stackloss measurements are an analogy for regression, not evidence of an unmeasured mechanical Hamiltonian.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Automatic differentiation computes derivatives of the implemented function; it does not prove the learned function is the true physical energy.

## Your independent answer

What property of the map from velocity to momentum matters for an ordinary Legendre transform back to velocity?

<details><summary>Reveal answer criteria after your attempt</summary>

Local invertibility/regularity, typically a nonsingular velocity Hessian. Singular constrained cases require additional treatment.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 23 learning section](../../stages/23/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/23.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
