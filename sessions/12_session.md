# Stage 12 guided session — Interpret a small improvement with paired evidence

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/12_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/12_lab.ipynb). The [original workbook](../workbooks/12_workbook.md) and [worked lab](../notebooks/12_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Actual saved handwriting predictions from an already-exposed image-level holdout; exploratory analysis only.

## What you will be able to demonstrate

1. Construct the paired correctness table for two models on the same observations.
2. Distinguish percentage points, counts, and conditional inferential quantities.
3. Calculate an exploratory exact discordance test and paired bootstrap interval.
4. Explain why reanalyzing an exposed holdout cannot create a fresh confirmatory test.

## Begin with the actual disagreement pattern
Suppose two models classify the same observations. Every record belongs to one of four groups: both correct, only A correct, only B correct, or both wrong. The difference in accuracy is `(B-only − A-only)/n`. The two total accuracies do not tell you this whole pattern.

The preserved handwriting experiment reports 347 correct pixel-only predictions and 351 correct combined predictions on 360 images. The net change is four. Reading its sample-level predictions reveals seven newly correct outcomes and three newly incorrect ones. This is more informative than saying that the combined system is simply better on four images.

## Derive the conditional test
Under the null hypothesis that the two directions of discordance are equally likely, and under suitable independent sampling, the number of B-only outcomes among the discordant records follows a binomial distribution with success probability one-half. Condition on the observed number of disagreements. For seven B-only and three A-only outcomes, the two-sided exact binomial calculation gives 0.34375.

This is not the probability that the null hypothesis is true. It is a tail calculation under the stated null and sampling assumptions. It does not establish no effect, and it does not supply a correction for repeatedly trying representations on an exposed test partition.

## Resample the paired differences
For each image define a difference: +1 when B alone is correct, -1 when A alone is correct, and 0 otherwise. A paired bootstrap resamples these image-level differences and recalculates their average. Resampling the two models independently would discard the pairing and answer a different uncertainty question.

The supplied percentile interval is conditional on the fixed fitted predictions and the assumed image-level resampling unit. It does not include all uncertainty from model selection or retraining. The dataset lacks writer identifiers, so independent-writer inference is unavailable. A future sports dataset with multiple clips per person or session would require a grouping-aware design rather than treating every frame as independent.

## Keep the experiment's status honest
These predictions were already exposed in v3. The new calculation is an exploratory audit of that worked example, not a new blinded experiment. Its value is pedagogical: understand uncertainty, pairing, units, and what was actually gained or lost.

A rigorous next study would specify the feature pipeline, model-selection procedure, independent sampling unit, primary metric, and uncertainty method before evaluating a genuinely new holdout. A statistically interesting output would still need practical relevance and domain-specific failure analysis. The independent capstone asks you to articulate those choices rather than chase a threshold such as p<0.05.

## Predict, execute, and explain

### Step 1

Read the actual saved predictions. Row IDs must be unique so each image contributes one paired outcome.

```python
import pandas as pd
from shape_lab.audits import paired_accuracy_audit
predictions = pd.read_csv(ROOT/'reports/stage_12/test_predictions.csv')
assert predictions.sample_id.is_unique
report = paired_accuracy_audit(predictions.true_label, predictions.pixels, predictions.combined,
                               resamples=4000, seed=2026)
print(json.dumps(report, indent=2))
```

### Step 2

Derive the net improvement from the discordant counts, not from rounded percentages.

```python
net = report['b_only_correct'] - report['a_only_correct']
assert net == 4
assert np.isclose(net/report['sample_count'], report['difference_b_minus_a'])
print('newly correct:', report['b_only_correct'], 'newly wrong:', report['a_only_correct'])
print('difference (percentage points):', 100*report['difference_b_minus_a'])
print('exploratory interval (percentage points):', 100*np.array(report['paired_percentile_interval']))
```

### Step 3

Save the status and assumptions with the numbers. A p-value is not a proof of either equality or superiority.

```python
assert report['a_only_correct']==3 and report['b_only_correct']==7
assert report['exact_discordance_pvalue']==.34375
result = report
result['models'] = ['pixels', 'combined']
result['new_confirmatory_holdout'] = False
```

## Transfer problems — attempt without the solution

### 12.T1

Two model comparisons have the same net gain of four. Must their paired uncertainty calculations agree?

<details><summary>Reveal reasoning after your attempt</summary>

No. Four gains and zero losses differ from 54 gains and 50 losses. Their discordance totals, conditional test distributions, and paired resampling distributions differ.

</details>

### 12.T2

What would make a future follow-up confirmatory rather than another reanalysis of this example?

<details><summary>Reveal reasoning after your attempt</summary>

Freeze the study choices before inspecting genuinely new evaluation data, use a defensible sampling and split unit, and report the declared metrics and uncertainty without selecting a favorable outcome after the fact.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/12_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
