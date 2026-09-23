# Stage 04 — Groups, symmetries, paths, loops, and homotopy

## Begin with one question

**Can doing two valid symmetries in opposite orders change the result?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Group: a set of composable operations with identity, inverses and associativity. Noncommuting: operation order matters. Homotopy: a continuous deformation of maps.

## Work the example before running it

Rotate a square by a quarter turn, then reflect it across the horizontal axis. Compare reflecting first and rotating second. Each operation preserves the square, but their products differ. A group need not be commutative.

Matrix multiplication represents composition here: the rightmost matrix acts first on a column vector. This convention will matter again in camera transforms. Path concatenation leads to another group idea after passing to homotopy classes of loops. That does not mean ordinary concatenated paths have all group laws literally before equivalence classes are introduced. Draw the loops, explain the equivalence, and only then use the algebraic language.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/04/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
R=np.array([[0,-1],[1,0]])
F=np.diag([1,-1])
assert np.array_equal(R@R@R@R,np.eye(2))
assert not np.array_equal(R@F,F@R)
print('RF=',R@F,'FR=',F@R)
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Rotate a real handwritten-digit image in the existing stage lab. A symmetry of the pixel grid is not automatically a label-preserving symmetry of the classification task.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Do not assume every transformation you can perform should preserve a target label. The observation process and task matter.

## Your independent answer

If A maps camera 1 to camera 2 and B maps camera 2 to world coordinates, which product maps a camera-1 column vector to world?

<details><summary>Reveal answer criteria after your attempt</summary>

B A, since A acts first. Consistent domain/codomain descriptions are stronger than guessing from variable names.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 04 learning section](../../stages/04/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/04.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
