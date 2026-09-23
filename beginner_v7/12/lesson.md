# Stage 12 — Capstone: reproduce, defend, transfer, and audit the book

## Begin with one question

**What does completing a capstone require?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Protocol: declared question and procedure. Baseline: a simpler comparison. Provenance: origin and transformations of evidence. Holdout: observations reserved for evaluation.

## Work the example before running it

A capstone is an argument supported by an executable analysis. Begin with a prediction-time question and an observation unit. Specify features, labels, metric, filtration, coefficient field, splitting rule, parameter choices and computational limits. Then compare a simple baseline with the proposed method on equivalent information.

Two rows can be different indices while sharing the same person or physical object. In the exact four-row example below, rows [0,2] and [1,3] are disjoint but both contain kernels A and B. The split is invalid for a new-kernel evaluation. A report that only checks row disjointness has missed the scientific unit. Your capstone should include counterexamples to its own likely failure modes.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/12/check.py
```

The script is short enough to inspect in full:

```python
from shape_lab.evidence_v7 import overlap_report
report=overlap_report({'train':[0,2],'test':[1,3]},['A','A','B','B'])
assert report['row_disjoint'] and not report['unit_disjoint']
print(report)
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Choose one of ten included industry cases as practice, then a genuinely new dataset or question for independent assessment. Repeatedly revisiting the supplied test labels is not a new holdout.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

An empty “notebook ran” checklist does not defend a scientific conclusion. Keep explanations, predictions, wrong turns and exact output evidence.

## Your independent answer

Name five items another learner needs to reproduce your experiment.

<details><summary>Reveal answer criteria after your attempt</summary>

Examples: source/version/hash, feature/target definitions and units, exact split identities, fitted preprocessing and model parameters, random seeds/environment, metric/filtration conventions, code and saved predictions.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 12 learning section](../../stages/12/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/12.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
