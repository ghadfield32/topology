# Stage 07 — From data to shape: Rips, Čech, alpha, and filtrations

## Begin with one question

**Do pairwise intersections guarantee a common intersection?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Filtration: nested spaces indexed by a parameter. Rips complex: all vertex sets whose pairwise distances satisfy the threshold. Čech complex: common intersections of balls.

## Work the example before running it

Place three centers at the corners of an equilateral triangle with side length one. Balls of radius one half touch pairwise. Yet there is no point shared by all three: the circumradius is 1/sqrt(3), approximately .577, which exceeds .5. Pairwise proximity and common intersection encode different conditions.

For Rips with edge threshold one, the triangle enters because all three edges exist. For a Čech construction using radius-.5 balls, the corresponding face does not. The parameter units and factor-of-two conventions must be stated before comparing the two. GUDHI alpha filtrations additionally use a squared-radius convention by default; matching raw numeric thresholds across constructions would be misleading.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/07/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
side=1.;radius=.5;circumradius=side/np.sqrt(3)
assert 2*radius>=side
assert radius<circumradius
print('Pairwise touching radius:',radius,'common-intersection threshold:',circumradius)
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Build a Rips filtration on a small, declared subset of standardized Seeds or Wine measurements. Their mixed feature geometry is not a measured spatial reconstruction.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Increasing a proximity threshold eventually connects everything; connectivity at one large scale alone is not a discovery.

## Your independent answer

Why must an alpha filtration value of 4 not automatically be read as radius 4?

<details><summary>Reveal answer criteria after your attempt</summary>

Under squared-radius convention it represents radius 2 in the same underlying coordinate units. Check the library’s exact convention.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 07 learning section](../../stages/07/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/07.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
