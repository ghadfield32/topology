# Stage 08 — Persistent homology, persistence modules, and reading diagrams

## Begin with one question

**When is a loop born, and what kills it?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Birth/death: parameter values where a class appears and disappears. Barcode: intervals of persistence. Essential/truncated: surviving the supplied filtration, possibly not an infinite extension.

## Work the example before running it

Four unit-square corners have side distances one and diagonal distances sqrt(2). At threshold one the perimeter edges form a loop and no triangular face is available. At sqrt(2), diagonals and the clique simplices enter and fill it. The positive H1 interval is [1,sqrt(2)).

Below one there are four components. Three H0 classes die when the perimeter becomes connected. Which vertex is selected as representative under equal-time ties is not a new scientific feature. The persistence maps matter, not only the Betti count at each separate scale. A finite computation ending before sqrt(2) would leave the loop with an unobserved death, not prove that it lives forever.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/08/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
from shape_lab.persistence import rips_filtration,persistent_homology,diagram
X=np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]])
D=diagram(persistent_homology(rips_filtration(X,max_homology=1)),1,finite_only=True)
assert D.shape==(1,2) and np.allclose(D[0],[1,np.sqrt(2)])
print('Finite H1 interval:',D[0])
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Return to the CO2 delay-coordinate lab only after learning time windows. Filtration scale and chronological time are not the same axis.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

A long bar is not a label such as “healthy,” “causal,” or “physically accurate.” Such interpretation needs independent evidence.

## Your independent answer

If all square coordinates are multiplied by three, what is the H1 interval under the same Euclidean edge convention?

<details><summary>Reveal answer criteria after your attempt</summary>

[3,3sqrt(2)). Pairwise distances all scale by three; the coordinate transformation preserves topology but changes persistence coordinates.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 08 learning section](../../stages/08/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/08.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
