# Monthly climate records and delay representations

**Prerequisite route:** Stages 01–03, 07–12, 21–22 and 28. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** A calendar baseline makes the representation and evaluation more interpretable.

Start with the [shared beginner data primer](../../docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](../cards/elnino.md). Open the [worked lab](../notebooks/elnino.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

Suppose the mean January temperature in the chosen training years is 24 degrees C. A January observation of 25.5 has an anomaly of +1.5 degrees relative to that baseline. This controlled arithmetic does not assert that all published climate anomaly products use our baseline. In the notebook the twelve training monthly means are calculated and saved explicitly.

The monthly long view is derived by a fixed column order; alphabetically sorting month names would scramble chronology. After reshaping, the window constructor uses an integer month index. A temperature in one regional record is not a spatial field. Operator training needs varying input functions or conditions with corresponding solution functions, so the optional field-simulation path is separate from this observed scalar time-series exercise.

## Walk through the real-data experiment


## 1. Reshape without changing time

The original rows contain years and twelve named month columns. We create a long table ordered January through December for each year. This adds no observations: 61 annual rows become 732 monthly values. The signal is regional mean SST in degrees Celsius, not an anomaly until we subtract a declared baseline.

## 2. Compare a seasonal forecast, persistence, and learned lags

The seasonal baseline predicts the training average for the target month. Persistence predicts the last observed temperature. Ridge predicts from twelve observed lags. Each makes a different assumption. All test windows remain inside the test period and predict one month ahead using observed history.

## 3. Visualize anomalies and training delay topology

Subtracting a seasonal mean is not harmless by default: the reference period is part of the definition. A baseline fit on all years would use future distribution information. We keep the training baseline fixed. A short delay cloud is an exploratory summary, not a recovered global climate manifold or a climate neural operator.

## 4. Distinguish one series from an operator dataset

An operator-learning study needs multiple input functions or conditions and corresponding solution fields, with function-level splits. This single regional series is not equivalent to many independent PDE trajectories. The core manufactured heat-operator examples and optional simulated field datasets serve a different role.

Independent task: explain how changing the climatology fit period can change the apparent anomalies without changing any original observations.

## Save your evidence

Create `my_work/industries/elnino.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**elnino.Q1.** Why must the reference period accompany an anomaly value?

**elnino.Q2.** Why is alphabetical month ordering wrong?

**elnino.Q3.** Can the same 732 values become independent PDE solutions just by creating windows?

**elnino.Q4.** Why must we compare last value and monthly climatology before more complicated models?

## Independent code and delayed recall

Use [your learner notebook](../learner/elnino.ipynb), then compare with the [worked answers](../answers/elnino.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/elnino.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.
