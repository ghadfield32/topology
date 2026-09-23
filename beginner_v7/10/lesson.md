# Stage 10 — Stability, diagram distances, noise, and scientific uncertainty

## Begin with one question

**What does stability protect, and what does it not protect?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Bottleneck distance: smallest worst matching cost, allowing matches to the diagonal. Stability: bounded output change for a specified input perturbation. Significance: a statistical question.

## Work the example before running it

A finite persistence point (1,3) has lifetime two. Matching it to the diagonal costs half its lifetime, one, in the infinity norm. Comparing that diagram with an empty one therefore costs one. Moving it to (1.1,3.1) costs .1 if matched to its counterpart, which is better than deleting both.

This calculation is a distance between descriptors, not a probability that the underlying object is real. Stability theorems have hypotheses about functions, spaces and perturbation norms. Arbitrary preprocessing or a changed sensor can violate the comparison setting. In practice ask three questions separately: did the algorithm execute correctly, is its result stable to the perturbation of interest, and does it support the scientific interpretation?

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/10/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
from shape_lab.persistence import finite_bottleneck
A=np.array([[1.,3.]])
assert np.isclose(finite_bottleneck(A,np.empty((0,2))),1.)
assert np.isclose(finite_bottleneck(A,A+.1),.1)
print('Deletion cost 1.0; matched shift cost 0.1.')
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Use the new Concrete Slump case to distinguish empirical prediction coverage from deterministic stability. These are different promises with different assumptions.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

A stable error can remain wrong. A well-calibrated interval can be too wide to be useful. Measure the property you actually need.

## Your independent answer

What is the diagonal cost for an interval [2,8), and why?

<details><summary>Reveal answer criteria after your attempt</summary>

Three: the diagonal midpoint is (5,5), with max(|2-5|,|8-5|)=3. Half the lifetime minimizes the infinity-norm distance.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 10 learning section](../../stages/10/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/10.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
