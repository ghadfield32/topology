# Missingness, past-only windows and seasonal shape

**Prerequisite route:** Stages 00–03, 07–12 and 18–22. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** The time axis and the missingness mask are part of the dataset.

Start with the [shared beginner data primer](../../docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](../cards/co2.md). Open the [worked lab](../notebooks/co2.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

Take a controlled weekly sequence [10,11,NaN,13,14,15]. Removing NaN makes 11 and 13 appear adjacent. A first-difference computed as if one week separates them is wrong. Keeping the calendar slots allows the window builder to reject unsupported examples rather than silently change their meaning. The notebook writes source indices so every forecast can be traced back to raw measurements.

A training-only local-shape transform subtracts a window's first value from each coordinate. It removes that window's level but retains short-term differences. It is an explicit representation choice, not a recovery of an invariant atmospheric state. A diagram that changes after detrending may be telling you about the preprocessing, not a discovered new physical phenomenon.

## Walk through the real-data experiment


## 1. A blank observation is not zero

The archive has 2,284 weekly date slots but only 2,225 measurements. Fifty-nine missing values remain missing. Dropping them and treating adjacent remaining rows as adjacent weeks would change the time axis. We create source-traceable windows and reject windows that cross a missing measurement or a time gap.

## 2. Define exactly what is being forecast

Each example uses twelve observed past weeks to predict one week ahead. During test evaluation later test predictions may use earlier **observed** test-period readings. This is rolling one-step prediction, not a free-running forecast of the entire future.

Our strict support split drops boundary windows instead of borrowing history across partitions; it is conservative and explicitly different from a less restrictive operational evaluation.

## 3. Inspect trend, gaps, and a delay-space cloud

A delay vector turns a time interval into a point. A loop may reflect seasonal repetition. It is not proof that the scalar series uniquely reconstructs the atmosphere's physical state. The point-cloud sample below is training-only; no test labels decide which diagram to show.

## 4. Diagnose an invalid shortcut

Why is interpolation using readings on both sides of a future gap unavailable for an online forecast? Why should overlapping windows not be treated as independent patients? How would changing the forecast horizon alter the information set?

Further model development needs a new locked protocol; the displayed test results are already exposed. These are historical observations, not a statement of today's atmospheric concentration.

## Save your evidence

Create `my_work/industries/co2.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**co2.Q1.** Why does dropping missing rows distort a fixed weekly lag?

**co2.Q2.** What is the target index for length three, end index two, horizon two?

**co2.Q3.** How does observed-history one-step testing differ from free-running rollout?

**co2.Q4.** Why is a seasonal-looking loop not proof of a reconstructed atmospheric attractor?

## Independent code and delayed recall

Use [your learner notebook](../learner/co2.ipynb), then compare with the [worked answers](../answers/co2.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/co2.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.
