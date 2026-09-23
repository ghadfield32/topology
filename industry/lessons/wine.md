# Chemistry, scale and out-of-sample topological descriptors

**Prerequisite route:** Stages 01–02 and 06–12. Beginners can inspect the data first and return to the advanced parts after the prerequisite stages.

**Central idea:** A good topological experiment must make a descriptor available for a genuinely new query.

Start with the [shared beginner data primer](../../docs/v6/BEGINNER_DATA_PRIMER.md), then the [dataset card](../cards/wine.md). Open the [worked lab](../notebooks/wine.ipynb) only after predicting its first result.

## What you should be able to explain

By the end, identify the observation unit, separate a stored row from an independent example, justify the metric or representation, describe which data fit each transform, calculate the relevant baseline, and reject an unsupported domain claim. Software success and scientific interpretation are assessed separately.

## Work a small example first

Use a hand-checkable geometry before the real chemistry: points at (0,0), (1,0), (1,1), (0,1). Under the edge-distance Rips convention, the perimeter loop is born at 1 and filled when diagonal edges and triangles enter at square-root two. The full small filtration—not a graph without triangles—is required. Multiply all coordinates by two and check the interval scales by two.

Now connect that test to the chemistry. The same idea applies in thirteen standardized coordinates; no two-dimensional picture is required for computation. Each local query complex contains the query and eight fixed-training neighbors. Changes in the reference cloud or standardization alter the question. Reserving reference rows keeps the supervised fitting query from including itself as a training landmark. It costs fitting data, so the raw-feature comparison uses that same reduced fitting set.

## Walk through the real-data experiment


## 1. Distinguish measurement, cultivar and quality

The target identifies three cultivars, not consumer quality or safety. A change from grams to milligrams can alter raw Euclidean distances. Standardization is therefore an explicit modeling choice, fitted on training data only.

Our comparison gives every model the **same supervised fitting rows**. A separate subset of training rows is reserved as a fixed reference cloud.

## 2. Define a descriptor that can be applied to an unseen row

For one query, choose its eight nearest training reference points. Form the nine-point Rips complex through dimension two. Summarize finite H0 merge lengths and H1 lifetimes. The reference set is frozen; test observations never become reference points.

The six numbers are engineered local summaries. They are not a magical recovery of the topology of one vector. Small complete complexes keep the computation inspectable.

## 3. Compare raw, topological, and combined representations

C=1, eight neighbors and thirty anchors are fixed teaching choices—not the outcome of a hidden test-set search. We show validation and test scores separately. A win here would be a result for this one protocol, not evidence that topology is generally superior.

## 4. Check a property, not just a score

Multiplying all standardized coordinates by two should multiply Rips birth/death distances by two. Counts need not be reinterpreted as physical units. The assertion below tests the descriptor contract independently of cultivar prediction. Then explain why arbitrary feature-wise scaling is a different operation.

## Save your evidence

Create `my_work/industries/wine.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.

## Independent conceptual questions

**wine.Q1.** Why is cultivar not an ordinal quality target?

**wine.Q2.** Why are reference rows excluded from supervised fitting rows in this comparison?

**wine.Q3.** Which six descriptor entries should change under uniform scale multiplication?

**wine.Q4.** What new evidence is needed before saying topology improves wine analysis generally?

## Independent code and delayed recall

Use [your learner notebook](../learner/wine.ipynb), then compare with the [worked answers](../answers/wine.ipynb). Do not use the answers as an input to your first attempt. After a delay, explain the observation unit, the main leakage trap, and a result this data cannot establish without reopening the lesson.

## Mastery evidence

Save `my_work/industries/wine.md` with a prediction, a hand calculation, one changed-code experiment, observed output and one limitation. Record the dataset hash and exact source rows you evaluated. To pass, all three coding tasks must run, the four conceptual answers must be correct, and the central leakage/interpretation error must be corrected. An independent delayed explanation—not a checkmark—is the retention evidence.
