# Retrospective change and forward evaluation

**Prerequisite route:** Stages 02, 07–12, 19 and 21. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** A detected change is a descriptive result until its cause is independently established.

Start with the [shared beginner data primer](../../docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](../cards/nile.md). Open the [worked lab](../notebooks/nile.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

For a controlled signal of eight zeros followed by eight ones, the split before the first one yields two constant segments and zero within-segment squared error. The unit test checks that exact result. A real river series has nonzero noise and dependence. Searching many cut points makes the chosen one look better by construction; the winner is not itself a significance test.

The model uses annual total volume, not instantaneous water speed or discharge. To convert volume to average rate you would need an explicit duration and consistent units. Even then you would not know subannual peaks or extreme-event timing. Such missing resolution matters for operational infrastructure decisions; it cannot be repaired by using a more expressive neural architecture.

## Walk through the real-data experiment


## 1. Define volume and chronology

The measurements are annual river volumes, in units of 100 million cubic metres. A volume is not a flow rate in cubic metres per second. There are one hundred years, not one hundred independent river systems. First partition years, then construct windows inside each partition.

## 2. Find a descriptive change using training years only

We fit two constant means and choose the split with smallest within-segment squared error. The selected split is retrospective within the training period. A low error does not explain the cause, prove a change is significant, or justify moving a dam. Many candidate splits were inspected; ordinary one-test reasoning would ignore that search.

## 3. Keep a forward prediction question separate

The change-point fit is not automatically a forecasting model. Here we independently compare last value, a fixed training mean, and a ridge model of five past annual readings. No causality or physical conservation law is enforced by any of them.

## 4. Identify what would be required for physics

A hydrological conservation model needs more than this scalar annual series: specify inflows, outflows, storage, rainfall, spatial boundaries and uncertainty. The manufactured PDE examples in the core course have these assumptions by construction; this observational series does not magically inherit them.

Transfer exercise: write one descriptive claim supported by the plot and one causal claim that it cannot support.

## Save your evidence

Create `my_work/industries/nile.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**nile.Q1.** Why is the two-mean search retrospective?

**nile.Q2.** How does annual volume differ from instantaneous discharge?

**nile.Q3.** Why must the change point be selected without reading the future evaluation years?

**nile.Q4.** Which missing quantities prevent this one series from specifying a full hydrology PDE?

## Independent code and delayed recall

Use [your learner notebook](../learner/nile.ipynb), then compare with the [worked answers](../answers/nile.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/nile.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.
