# Firm panels, timestamps and prediction availability

**Prerequisite route:** Stages 00–03, 10–12, 19 and 21. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** Two records from the same company are not two independently sampled companies.

Start with the [shared beginner data primer](../../docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](../cards/grunfeld.md). Open the [worked lab](../notebooks/grunfeld.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

Write two records for one imagined firm: year t has investment 100, year t+1 has investment 120. A last-investment baseline predicts 100 for the later record and incurs absolute error 20. That arithmetic says nothing about causality. A fitted coefficient using capital and value may capture association, firm scale or missing covariates.

Our panel shift happens within each firm. A shift on the entire concatenated table would accidentally use the last record of one company as the previous record for another. This is a silent data-engineering failure that can survive model training. Compare same-firm chronological evaluation with leaving entire firms out; the latter tests a different generalization question. Publication delays and later accounting revisions are not in this snapshot, so the availability assumption stays qualified.

## Walk through the real-data experiment


## 1. Respect the panel structure

A panel repeatedly observes the same entity. This table contains eleven firms, with annual records over twenty years. We create prior-year predictors within each firm. In particular, same-year year-end market value is not available at the beginning of that year.

This is an explicitly simplified availability assumption: the notebook does not contain publication-time or revision-vintage data.

## 2. Compare with doing almost nothing

The last observed investment value is a serious baseline. A pooled ridge model shares one relationship across firms; it does not imply that all firms have the same structural mechanism. Both MAE and RMSE retain the source monetary scale. We do not invent a million-dollar multiplier.

## 3. Look at errors by firm instead of hiding them in an average

A low pooled error can hide a poorly modeled firm. The following view is a descriptive breakdown of this exposed test set, not a basis for tuning firm-specific models against it. A new-firm claim would require a different, entity-disjoint evaluation.

## 4. Separate prediction from intervention

No fitted coefficient here is a causal effect of increasing a firm's equipment. The data contain selection, omitted variables, repeated firms, and historical accounting conventions.

Exercise: design two different tests—future years of known firms and years from previously unseen firms. Explain why these answer different questions, and why revised financial data complicate a genuine real-time historical simulation.

## Save your evidence

Create `my_work/industries/grunfeld.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**grunfeld.Q1.** Why is a shift within firm necessary?

**grunfeld.Q2.** Why is same-year year-end value unavailable for a start-of-year forecast?

**grunfeld.Q3.** What does a known-firm future-year test not establish?

**grunfeld.Q4.** Does a capital coefficient identify the causal effect of buying equipment?

## Independent code and delayed recall

Use [your learner notebook](../learner/grunfeld.ipynb), then compare with the [worked answers](../answers/grunfeld.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/grunfeld.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.
