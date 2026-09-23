# Stage 00 — Start here: how to learn, run, and question the results

## Begin with one question

**What is one observation, and how is it stored?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Observation: one recorded object or event. Feature: an input measurement. Target: an outcome or category. Array axis: one direction in an organized collection.

## Work the example before running it

Start with a single kernel. Seven feature values describe it; they are not seven separate kernels. Put 210 kernels underneath one another and you obtain a 210-by-7 feature table. The source file also contains a target and our generated row ID, so its full table has nine columns. Selecting the seven inputs is a scientific choice, not just slicing an array.

In Python, `table[features]` selects the named fields and `.shape` returns two integers. The first counts rows; the second counts selected fields. Printing the first five rows gives examples, not proof of all 210 rows. The loader also checks local file hashes and schema. It does not independently certify source transcription or biological validity. Numbers can be stored correctly and still be interpreted incorrectly.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/00/check.py
```

The script is short enough to inspect in full:

```python
from shape_lab.evidence_v7 import load_snapshot
from shape_lab.practice_v7 import table_dimensions
table, meta = load_snapshot('seeds')
assert table_dimensions(table[meta['features']]) == (210, 7)
assert table.shape == (210, 9)
print('210 observations; 7 selected features; 1 label and 1 source ID excluded.')
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Open the new Seeds case and the retained healthcare case. Both use extracted image measurements; neither bundles the original acquisition images. Explain that difference before discussing computer vision.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Running a notebook is not an independent answer. Write a prediction first and preserve it even when the code disproves it.

## Your independent answer

For 52 mixtures and seven ingredients, state the feature-array dimensions. Would three measured outputs count as three additional mixtures?

<details><summary>Reveal answer criteria after your attempt</summary>

The input shape is (52,7). Three output columns describe each same mixture, so they do not increase the number of mixtures.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 00 learning section](../../stages/00/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/00.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
