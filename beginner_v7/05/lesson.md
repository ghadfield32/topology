# Stage 05 — Surfaces, simplices, triangulations, and pixel geometry

## Begin with one question

**What changes when a triangular outline is filled?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Simplex: a vertex, edge, triangle or higher-dimensional analogue. Face: a lower-dimensional part. Complex: a compatible collection containing the faces it requires.

## Work the example before running it

Three pairwise edges form a triangular outline. Adding one triangular face fills it. The vertices and edges remain; the two-dimensional simplex is new. An abstract complex records which vertex subsets form simplices, not just a drawing.

A triangle requires all three edges and all three vertices. The closure function intentionally adds required faces when constructing a complex. The validator, by contrast, rejects an incomplete supplied complex. These functions have different contracts: silent repair during validation can hide an upstream bug. A graph alone is not interchangeable with the clique complex that fills its cliques.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/05/check.py
```

The script is short enough to inspect in full:

```python
from shape_lab.algebra import closure,validate_complex
outline=closure([(0,1),(1,2),(0,2)])
filled=closure([(0,1,2)])
assert len(outline)==6 and len(filled)==7
assert (0,1,2) not in outline and (0,1,2) in filled
try:validate_complex([(0,1,2)])
except ValueError:print('Missing faces rejected as expected.')
else:raise AssertionError('Validator accepted missing faces')
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

For a binary digit image, decide whether a foreground pixel represents its center or a closed square. Diagonal contact changes connectivity under different conventions.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Pretty triangulation pictures are not enough: save the actual simplices and the coordinate or pixel convention.

## Your independent answer

How many nonempty faces, including itself, does a tetrahedron contain?

<details><summary>Reveal answer criteria after your attempt</summary>

Four vertices + six edges + four triangles + one tetrahedron =15. Its boundary excludes the final tetrahedron.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 05 learning section](../../stages/05/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/05.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
