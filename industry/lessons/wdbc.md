# Cell-image measurements and honest classification

**Prerequisite route:** Stages 00–03 and 07–12. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** A medical-sounding name does not turn a teaching classifier into a medical device.

Start with the [shared beginner data primer](../../docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](../cards/wdbc.md). Open the [worked lab](../notebooks/wdbc.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

For a hand calculation, consider a controlled confusion matrix with 90 benign and 10 malignant examples. A rule calling everything benign gets 90 correct, but malignant recall is zero. Balanced accuracy is (1 + 0)/2 = 0.5. This is an invented arithmetic control, not a result measured on this dataset. Compare it with the real confusion matrix produced by the notebook. Explicitly say which is which.

The original measured features describe variation among cell nuclei. Our standardized point cloud compares image summaries; we never reconstruct actual three-dimensional cells. Computing homology after projecting to two coordinates answers a question about that projection. It can merge or separate structures that differ in the original feature space. Test a controlled projection before interpreting a real plot.

## Walk through the real-data experiment


## 1. Define the independent example before fitting

Each row summarizes nuclei in a digitized fine-needle-aspirate image. These are not raw images. The sklearn snapshot lacks the original identifiers, so we cannot verify a patient-disjoint or hospital-disjoint test. We map **malignant to 1** explicitly. No threshold or model in this lesson is a clinical recommendation.

Predict: which columns would leak the answer or identify a row rather than measure the specimen?

## 2. Establish a fixed, explainable baseline

A logistic model maps a linear score to a number between zero and one. That number is not automatically calibrated for a new hospital. We fix C=1 before viewing validation or test results. Accuracy can hide unequal class performance, so we also report balanced accuracy, a confusion matrix, and ROC AUC. All preprocessing parameters come from training rows.

## 3. Ask a topological question at the correct level

Now study the geometry of a fixed small training cohort. A persistence diagram belongs to this point cloud and its metric; it is not a separate diagnostic test for each row. A loop can reflect sampling, correlated features or preprocessing. Selecting the most dramatic diagram after inspecting labels would be exploratory selection, not an independent discovery.

## 4. Stop before an unsupported conclusion

**Answer independently:** (a) Why does a row-disjoint test not establish patient independence here? (b) Why does zero training error not prove a clinically usable system? (c) What additional identifiers and validation cohorts would be required?

Do not improve the reported test score by repeatedly trying features. Any further search needs a newly protected evaluation. The source card records the original source and reuse conditions.

## Save your evidence

Create `my_work/industries/wdbc.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**wdbc.Q1.** Explain why `label == 0` means positive malignancy in this loader but is not a universal label convention.

**wdbc.Q2.** Draw a confusion matrix for an always-benign classifier and calculate both ordinary and balanced accuracy.

**wdbc.Q3.** Identify the absent identifiers that prevent verifying a hospital-level or patient-level holdout.

**wdbc.Q4.** Explain why a cohort persistence diagram is not one diagnosis per row.

## Independent code and delayed recall

Use [your learner notebook](../learner/wdbc.ipynb), then compare with the [worked answers](../answers/wdbc.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/wdbc.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.
