# Stage 06 — Chains, boundaries, homology, and Betti numbers

## Begin with one question

**Why are cycles not automatically nontrivial holes?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Chain: a weighted combination of simplices. Cycle: a chain with zero boundary. Boundary: the boundary of a higher-dimensional chain. Homology: cycles modulo boundaries.

## Work the example before running it

A loop around a triangle has zero boundary because each endpoint cancels over F2. If the triangular face is absent, that loop is not the boundary of a two-chain in the complex. If the face is present, the same loop is its boundary. Homology identifies such boundaries with zero.

For finite complexes over a field, beta_k = number of k-simplices - rank(d_k) - rank(d_{k+1}). The boundary-of-boundary identity ensures the image of d_{k+1} lies inside the kernel of d_k, so the quotient makes sense. This is not a count of every visibly closed walk: many walks represent the same class or represent zero.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/06/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
from shape_lab.algebra import closure,boundary_matrix,betti_numbers
outline=closure([(0,1),(1,2),(0,2)]);filled=closure([(0,1,2)])
assert betti_numbers(outline,1)==[1,1]
assert betti_numbers(filled,1)==[1,0]
assert np.all((boundary_matrix(filled,1)@boundary_matrix(filled,2))%2==0)
print('Outline beta=[1,1]; filled beta=[1,0]; boundary of boundary is zero.')
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Threshold a real digit image in the retained lab. Its homology describes the chosen image complex, not a universal property of every handwritten instance of the class.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Homology depends on the space and coefficient system you selected. Equal Betti numbers do not generally prove two spaces homeomorphic.

## Your independent answer

Why must triangles be included when computing Rips H1 even if you only want one-dimensional output?

<details><summary>Reveal answer criteria after your attempt</summary>

Two-simplices can make one-cycles into boundaries and kill H1 classes. Output dimension and construction dimension are different requirements.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 06 learning section](../../stages/06/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/06.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
