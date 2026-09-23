# Stage 19 — From geometry to cautious interaction hypotheses

## Begin with one question

**When does a live detector actually know an event occurred?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Onset: candidate beginning. Confirmation: when sufficient evidence has arrived. Visibility: whether the required observation is available. Causal processing: uses past/present only.

## Work the example before running it

Assume a toy detector requires three consecutive visible distances below .1. Observed distances [.2,.08,.07,.06] begin satisfying the condition at index one, but confirmation is unavailable until index three. With .02-second spacing, confirmation follows candidate onset by .04 seconds.

Recording index one as onset is compatible with an online detector only if the output also records that it was emitted at index three. Otherwise a hindsight label is disguised as a zero-latency live decision. Proximity alone does not prove contact, controlled possession or release. Occlusion and tracking identities must remain part of the evidence.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/19/check.py
```

The script is short enough to inspect in full:

```python
distances=[.2,.08,.07,.06];dt=.02
run=0;confirmed=None;onset=None
for i,d in enumerate(distances):
    run=run+1 if d<.1 else 0
    if run==3:
        confirmed=i;onset=i-2;break
assert onset==1 and confirmed==3
assert abs((confirmed-onset)*dt-.04)<1e-12
print('Candidate onset:',onset,'confirmation:',confirmed,'delay:',.04)
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

The retained temporal labs use manufactured controls and historical time series. Real basketball contact labels and synchronized observations are an independent-data obligation, not supplied by this toy signal.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

A filled-in or smoothed track must not be relabeled as direct observation. Separate observed, interpolated and inferred evidence.

## Your independent answer

How should a missing required observation affect a three-consecutive-visible-samples rule?

<details><summary>Reveal answer criteria after your attempt</summary>

Under that explicit rule it breaks the visible run. A different missing-data policy must be declared and validated, not silently substituted.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 19 learning section](../../stages/19/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/19.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
