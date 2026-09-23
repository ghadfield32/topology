# Stage 01 — Mathematical language, proofs, and linear algebra

## Begin with one question

**Why can the same matrix have different ranks?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Field: the rules for arithmetic. Rank: number of independent directions in a linear map. Kernel: inputs mapped to zero. Proof: an argument covering all stated cases.

## Work the example before running it

Over real numbers, the columns of [[1,1],[1,-1]] are independent: its determinant is -2. Over the two-element field, -1 equals 1, so the columns become identical and the rank is one. Arithmetic is part of the mathematical object, not a cosmetic implementation detail.

The course uses XOR elimination for homology over F2. Do not replace it with floating-point rank on a general binary matrix; real and mod-two dependence can differ. Here you can prove the result by solving the two equations. In F2, (1,1) is a nonzero kernel vector because 1+1=0. In the reals, only the zero vector is in this matrix's kernel. This hand calculation becomes important when boundaries are combined later.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/01/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
from shape_lab.algebra import rank_mod2
A=np.array([[1,1],[1,-1]])
assert np.linalg.matrix_rank(A)==2
assert rank_mod2(A)==1
assert np.all((A @ np.array([1,1])) % 2 == 0)
print('Rank over R: 2; rank over F2: 1.')
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Use two numerical columns from Seeds to practice matrix shape and centering, but do not interpret a label column as a continuous coordinate simply because it is numeric.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Verifying a few numerical examples is not a proof of the rank formula for every complex. Learn the reasoning and then use tests for implementation errors.

## Your independent answer

Over F2, what is 1+1, and what does it imply for adding an edge boundary to itself?

<details><summary>Reveal answer criteria after your attempt</summary>

1+1=0. Adding the same boundary twice cancels it coefficient by coefficient. It does not remove a source observation from a dataset.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 01 learning section](../../stages/01/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/01.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
