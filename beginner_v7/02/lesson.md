# Stage 02 — Closeness, metrics, neighborhoods, and topologies

## Begin with one question

**What must a distance function satisfy?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Metric: a nonnegative, symmetric distance separating distinct points and satisfying the triangle inequality. Neighborhood: nearby points defined by the chosen space.

## Work the example before running it

For points 0,1,2 on a line, ordinary distances are 1,1 and 2. Squaring them gives 1,1 and 4. The alleged direct distance 4 is now greater than 1+1, so squared distance violates the triangle inequality. A formula useful in an optimization loss is not automatically a metric.

A metric gives open balls. These give a topology: a way to specify neighborhoods and continuous maps. In a finite distinct point sample with Euclidean distance, each point can be isolated by a sufficiently small ball. That finite topology is discrete. TDA does not magically discover a continuous circle inside the finite topology; it constructs complexes using distances at larger scales. Keep the sample, metric, complex and inferred underlying object separate.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/02/check.py
```

The script is short enough to inspect in full:

```python
d=lambda x,y: abs(x-y)
sq=lambda x,y: (x-y)**2
assert d(0,2) <= d(0,1)+d(1,2)
assert sq(0,2) > sq(0,1)+sq(1,2)
print('Squared distance: 4 > 1 + 1, so it is not a metric on R.')
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Compare raw and standardized Seeds distances. Their neighborhoods answer different questions. Source area and length units are unresolved, so do not invent a physical metric.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

A triangle-inequality check on one sample can falsify a metric claim, but passing a finite sample is not a universal proof.

## Your independent answer

Would multiplying every distance by a fixed positive constant preserve the metric axioms? Explain rather than sample.

<details><summary>Reveal answer criteria after your attempt</summary>

Yes. Nonnegativity, symmetry and zero separation remain; multiplying both sides of every triangle inequality by the same positive constant preserves it.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 02 learning section](../../stages/02/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/02.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
