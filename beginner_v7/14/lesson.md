# Stage 14 — Rotations, rigid transforms, and the camera model

## Begin with one question

**How do you know a matrix is a valid rotation?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

SO(3): orthogonal 3x3 matrices with determinant +1. Rigid transform: rotation plus translation. Frame: coordinate reference. Intrinsics: pixel projection parameters.

## Work the example before running it

A rotation preserves lengths and orientation: R^T R=I and det(R)=1. Nine arbitrary numbers do not generally satisfy these equations. A rigid transform then maps a point p to Rp+t. Its inverse is R^T(p-t), not R^T p-t unless a special coincidence holds.

For a quarter turn around the z-axis and translation (1,2,3), point (1,0,0) becomes (1,3,3). Applying the inverse returns (1,0,0). These are constructed coordinates with a declared common unit, not measured metre accuracy. A camera projection adds another mapping and discards information; testing transform inverses cannot by itself validate calibration.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/14/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
R=np.array([[0.,-1,0],[1,0,0],[0,0,1]])
t=np.array([1.,2.,3.]);p=np.array([1.,0.,0.]);q=R@p+t
assert np.allclose(R.T@R,np.eye(3)) and np.isclose(np.linalg.det(R),1.)
assert np.allclose(q,[1,3,3]) and np.allclose(R.T@(q-t),p)
print('Forward:',q,'inverse:',R.T@(q-t))
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Use calibrated stereo observations for physical reconstruction, not the Nile series or arbitrary tabular coordinates. The general lesson of units transfers; the camera model does not.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

A matrix with determinant one alone is not necessarily a rotation in three dimensions. Orthogonality must also be checked.

## Your independent answer

What additional check rejects a shear matrix with determinant one as a rotation?

<details><summary>Reveal answer criteria after your attempt</summary>

R^T R=I. A nontrivial shear changes lengths and angles and fails this orthogonality condition.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 14 learning section](../../stages/14/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/14.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
