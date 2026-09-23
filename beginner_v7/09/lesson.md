# Stage 09 — Implement persistence, trace the algorithm, and test it independently

## Begin with one question

**What is a reduction algorithm actually checking?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Boundary column: encoded boundary of one simplex. Pivot: largest nonzero row in a reduced column. XOR: addition over F2. Pairing: birth/death relation from reduction.

## Work the example before running it

Take two vertices born at zero and their connecting edge born at one. Initially there are two components; after the edge, one remains. The boundary column of the edge has two nonzero vertex rows. Its pivot pairs one vertex class with that edge. One H0 interval is [0,1); another persists in the supplied filtration.

For larger examples, adding a previous column with the same pivot cancels that pivot. Repeat until the column is zero or has a new pivot. Store the operation trace so you can follow the algorithm rather than trust a barcode drawing. Faces must appear no later than cofaces; ties are ordered compatibly. Verify exact examples and boundary identities before benchmarking runtime.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/09/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
from shape_lab.persistence import persistent_homology,reduce_boundary
F=[((0,),0.),((1,),0.),((0,1),1.)]
bars=persistent_homology(F,max_dim=0)
assert len(bars)==2
assert sorted(b.death for b in bars)==[1.,np.inf]
f,columns,pairs,trace=reduce_boundary(F)
assert len(pairs)==1
print('Finite component death at 1; one surviving component. Pairs:',pairs)
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

The manufacturing Stackloss case has few observations. That makes intermediate arrays inspectable but does not excuse fitting and reporting on the same rows.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Two libraries can share assumptions or conventions. Agreement helps, but independent hand calculations remain necessary; missing optional checks remain missing.

## Your independent answer

What must you record when one implementation includes zero-length bars and another omits them?

<details><summary>Reveal answer criteria after your attempt</summary>

The policy and tie convention, then compare equivalent positive-length outputs or intentionally align the policies. Do not count the display difference as physical disagreement.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 09 learning section](../../stages/09/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/09.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
