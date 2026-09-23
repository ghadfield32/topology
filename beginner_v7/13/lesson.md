# Stage 13 — From topology to smooth manifolds

## Begin with one question

**How can two coordinate systems describe the same point?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Manifold: a space locally described by Euclidean coordinates under specified regularity. Chart: a local coordinate map. Transition: one chart followed by another chart inverse. Tangent: a local direction.

## Work the example before running it

Latitude-longitude intuition is useful, but start with a sphere and an explicit formula. A stereographic inverse sends planar coordinates (u,v) to (2u,2v,u²+v²-1)/(1+u²+v²). At (u,v)=(0,0), it gives the south pole. The missing north pole explains why this one chart does not cover the whole sphere.

Substituting the resulting coordinates into u=x/(1-z), v=y/(1-z) returns the same local coordinates. The round trip tests one representation pair. A chart is not a photograph of an arbitrary 3D scene: perspective projection loses depth along a ray. Smooth coordinate transitions preserve the underlying point, not identical coordinate numbers.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/13/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
u,v=.3,-.4;r2=u*u+v*v
p=np.array([2*u,2*v,r2-1])/(1+r2)
assert np.isclose(p@p,1.)
assert np.allclose(p[:2]/(1-p[2]),[u,v])
print('Sphere point:',p,'round trip:',p[:2]/(1-p[2]))
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

The retained stage maps directions derived from real stereo references onto a constructed sphere. That construction is not evidence that the original scene is a sphere.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Local invertibility should not be upgraded to global invertibility. Always state the excluded set and chart domain.

## Your independent answer

Why does this inverse chart fail to recover finite (u,v) at the north pole?

<details><summary>Reveal answer criteria after your attempt</summary>

The denominator 1-z is zero at z=1. The north pole is outside this chart and needs another patch.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 13 learning section](../../stages/13/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/13.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
