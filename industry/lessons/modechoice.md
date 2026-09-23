# Choice sets, group splits and fair baselines

**Prerequisite route:** Stages 00–03, 07–12 and 19. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** The physical or decision-making unit must survive reshaping and splitting.

Start with the [shared beginner data primer](../../docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](../cards/modechoice.md). Open the [worked lab](../notebooks/modechoice.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

With 210 travelers and four alternatives each, the array has 840 alternative records. A person-level prediction requires selecting one of the four modes once for each traveler. A split after pivoting gives one independent choice set per row. A split before pivoting could put part of a person's choice set into the fitting data and another part into the test data.

Cheapest offered mode is a concrete baseline, not an assumption that price alone determines behavior. Waiting time, travel time, income and unobserved preferences can matter. Our classifier does not estimate an intervention effect from changing a ticket price. The source sampled choices disproportionately; a probability distribution in this sample is not a population market-share forecast.

## Walk through the real-data experiment


## 1. Reconstruct the choice set

Each traveler has four alternatives. Randomly splitting the 840 rows could put the same traveler into training and test. Instead, pivot to 210 person-level examples. Include offered waiting times, prices, in-vehicle times and income. Exclude the target and party size whose availability is tied to the chosen mode. We also exclude generalized cost because it is constructed from other cost/time terms.

## 2. Establish person-level baselines

This simple multinomial classifier treats each traveler's thirteen offered attributes as predictors. It is not the same model as a conditional-logit utility model. We compare it with the training-majority mode and the cheapest offered mode. All return exactly one choice per traveler.

## 3. Inspect sample geometry without inventing market shares

The study deliberately oversamples some modes. Prediction fractions are not population transport shares, and learned probabilities are not automatically population-calibrated. A topology diagram summarizes offered attributes in the chosen standardized metric; it does not recover the real road network.

## 4. Transfer the grouping lesson

In sports, several shots can belong to one athlete; in healthcare, several images can belong to one patient; in manufacturing, many overlapping windows can come from one run. Choose the independent unit before creating a split.

Explain why a predicted change under a modified ticket price is not a validated causal effect. What sampling weights, policy experiment, or external evidence would be needed?

## Save your evidence

Create `my_work/industries/modechoice.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**modechoice.Q1.** Why do 840 records not imply 840 independent decisions?

**modechoice.Q2.** Why exclude `choice` and the potentially post-choice `psize` from features?

**modechoice.Q3.** How can probabilities sum to one and still be uncalibrated for a population?

**modechoice.Q4.** What is analogous to traveler grouping in sports and healthcare?

## Independent code and delayed recall

Use [your learner notebook](../learner/modechoice.ipynb), then compare with the [worked answers](../answers/modechoice.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/modechoice.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.
