# Small-sample process monitoring

**Prerequisite route:** Stages 01–02, 10–12, 21 and 26–27. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** A small observational table is useful for learning model fragility, not certifying a reactor.

Start with the [shared beginner data primer](../../docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](../cards/stackloss.md). Open the [worked lab](../notebooks/stackloss.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

Calculate an ordinary mean and one residual before running Ridge. If a source-scale observation is 20 and a prediction is 15, the signed residual observed minus predicted is 5; its absolute error is 5. Do not convert it to kilograms or a flow rate without a documented unit relationship. When a label uses an encoded percentage, keep the encoding explicit in plots.

The source row order is preserved for a simple train/validation/test demonstration. Missing timestamps prevent claiming a faithfully reconstructed future operating shift. The leave-one-training-row-out exercise asks how much individual observations influence a prediction. It does not increase the number of independent experiments. A large neural network might memorize these rows; that is not evidence of an identifiable physical state or safe control behavior.

## Walk through the real-data experiment


## 1. Read the encoded variables

There are only twenty-one plant records. Exact dates and instrument metadata are absent. We preserve source row order, but do not call it a verified future-production timeline. Stack loss uses the documented encoded response scale; other ambiguous units are not invented. We hold out rows to demonstrate the procedure, not certify a plant-control system.

## 2. Investigate how fragile the fitted coefficients are

Leave out one **training** row, refit both scaling and model on the remaining training rows, then predict that omitted row. This is a sensitivity exercise, not an additional independent test set. A large change caused by a single row matters when the whole training set has fourteen observations.

## 3. Compare geometry with process meaning

Build a small training point-cloud diagram. The distances join observations with similar standardized process values. The diagram does not enforce a mass-balance law. A scalar residual model is not a reconstructed reactor, and correlation cannot determine whether changing a control knob causes the predicted change.

## 4. Define a responsible next experiment

Specify the missing timestamps, calibration units, actuator limits, safe excitation protocol, and independently recorded future runs before proposing a physics-informed model. Do not pretend that the eight new datasets supply the boundary conditions for every PDE in the course.

Transfer questions: why might a neural network fit these rows and still be useless? Which quantities would a defensible conservation-law experiment need to measure?

## Save your evidence

Create `my_work/industries/stackloss.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**stackloss.Q1.** Why must the holdout be described as source-order rather than a verified operational-time split?

**stackloss.Q2.** What changes when scaling is refit in each leave-one-out training fold?

**stackloss.Q3.** Why can a PINN with a wrong boundary condition still produce low training error?

**stackloss.Q4.** List four observations needed for an independently testable plant conservation model.

## Independent code and delayed recall

Use [your learner notebook](../learner/stackloss.ipynb), then compare with the [worked answers](../answers/stackloss.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/stackloss.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.
