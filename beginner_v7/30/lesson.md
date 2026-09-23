# Stage 30 — An independent world-model study: evidence before adoption

## Begin with one question

**When is a scientific learning project ready to defend?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Evidence ledger: links claims to sources, assumptions and tests. Marginal guarantee: averaged over an appropriate sampling process. Independent validation: evidence not used to choose the result.

## Work the example before running it

A final report should identify each important statement as source-derived, analytically established, executed in a declared experiment, or still proposed. The source posts motivate useful ideas, but their strongest statements need explicit assumptions and tests. A benchmark improvement, theorem, plotted trajectory and measured sensor result are not interchangeable evidence.

Consider calibration with only nine error scores. A 99% nominal level needs rank ceil(10×.99)=10, beyond the nine available scores. The conservative interval becomes infinite. Reporting that limit is scientifically stronger than hiding it behind a finite interpolated quantile. Apply the same discipline to missing camera scale, unavailable participant IDs, unrun external comparisons and absent actual-book text.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/30/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
from shape_lab.evidence_v7 import conformal_rank,conformal_radius
assert conformal_rank(9,.01)==10
assert np.isinf(conformal_radius(np.arange(1,10),.01))
print('The requested extreme coverage is uninformative at this calibration size under the stated rule.')
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Choose an independent question using a source with suitable units, identities and a justified reuse license. The ten included industry cases are worked teaching datasets, not infinite fresh holdouts.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

A course completion record is not certification for medicine, structural engineering, production robotics or every open research topic.

## Your independent answer

Which unfinished obligations must remain visible after completing this package’s reference experiments?

<details><summary>Reveal answer criteria after your attempt</summary>

Actual-book reconciliation, deeper theorem proofs where assigned, independent projects, missing external-library comparisons, unrun model inference or paper replications, and domain-specific physical or clinical validation as relevant.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 30 learning section](../../stages/30/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/30.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
