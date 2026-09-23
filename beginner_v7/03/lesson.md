# Stage 03 — Continuity, homeomorphisms, connectedness, and compactness

## Begin with one question

**Why is a continuous bijection not always a homeomorphism?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Preimage: inputs mapped into a set. Continuity: preimages of open sets are open. Homeomorphism: a bijection continuous in both directions.

## Work the example before running it

Take the same two points {0,1} with two topologies. The discrete topology declares every subset open. A coarser topology declares only the empty set, {1}, and the whole set open. The identity from the discrete space to the coarser space is continuous because each preimage is open in the discrete domain.

The inverse identity is not continuous: the set {0} is open in its codomain but not in its domain. No coordinates moved, yet the topological structures differ. This is why the inverse-continuity condition matters. The finite checker below exhausts this particular example; it is not a general automatic theorem prover for arbitrary spaces. Later compactness and Hausdorff assumptions give useful sufficient conditions for continuous bijections to be homeomorphisms.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/03/check.py
```

The script is short enough to inspect in full:

```python
empty=frozenset();whole=frozenset({0,1})
discrete={empty,frozenset({0}),frozenset({1}),whole}
coarse={empty,frozenset({1}),whole}
identity_continuous=lambda domain,codomain: all(U in domain for U in codomain)
assert identity_continuous(discrete,coarse)
assert not identity_continuous(coarse,discrete)
print('The identity is a continuous bijection in one direction, not a homeomorphism.')
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Projection of seven real measurement columns onto two plotted columns can discard information. A visually tidy scatterplot does not establish invertibility of that projection.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

A plot may suggest a map but does not specify its domain, codomain or topologies. State those before checking continuity.

## Your independent answer

What extra condition on the inverse is required in the definition of homeomorphism?

<details><summary>Reveal answer criteria after your attempt</summary>

The inverse must be continuous. Merely existing as a set-theoretic inverse is insufficient.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 03 learning section](../../stages/03/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/03.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
