# Stage 12 workbook — Finish with a defensible experiment and a foundation you can extend

## Reproduction and independent research are different achievements

The worked capstone already includes its test predictions. Recreating them checks that you understand and can execute the supplied protocol. It does not create a new blinded result. Changing model choices after reading those results and reporting the same test set as independent would overstate the evidence.

For an independent capstone, define a new question or obtain genuinely unexamined data with an appropriate split. A new random split of the same already explored examples can be a useful exercise, but it is not automatically an untouched scientific holdout. Report the exposure history.

## Write the protocol before seeing the final result

State what one observation represents and which observations are dependent. Record the data source, permission or license, units, feature definitions, metric, complex, filtration parameter, coefficient field, dimensions, and stopping rule. Identify the baseline and what would count as meaningful added value.

For video, frames from the same person or recording are often related. A frame-level random split can answer a different question from generalization to new people or sessions. For the bundled digits snapshot, writer IDs are unavailable; we therefore state an image-level split and do not claim unseen-writer evaluation.

Separate exploratory choices from fixed evaluation choices. Record how parameters were selected, when the test data were opened, and which results were examined before a later revision. A reproducible log is more informative than a retrospective statement that the method was obvious all along.

## Read the existing result at sample level

The report stores predictions for every one of the 360 test images. Compare where the pixel model and combined model disagree. A four-image net improvement does not tell you whether the models made exactly four different predictions; one may correct several errors and introduce others. The paired-disagreement exercise records both directions.

That comparison still is not a significance claim. A statistical analysis needs its own assumptions about observations, hypothesis selection, multiplicity, and the chosen test. The course does not infer those assumptions from a small percentage difference.

## Make conclusions proportional to the evidence

An acceptable conclusion can say: “On this declared image split, the combined representation classified four more images correctly than pixels alone. This is an observed result of the worked protocol; writer-independent generalization and a general advantage are not established.” A negative or inconclusive result can be equally complete when the method and limitations are well defended.

Avoid claims about causal mechanisms, biological structure, or calibration accuracy from a descriptor alone. In a sports motion project, topology might provide a useful summary, but it does not replace camera calibration, synchronization, anatomical ground truth, or a study of measurement uncertainty.

## Continue learning without rebuilding the course

For each stage, preserve written answers, notebook versions, outputs, and mistakes. Record whether work was guided or independent. After an assessment, revisit unfamiliar questions after a delay. The local learning log links an attempt to a content hash of its evidence file and proposes the next review date.

This is a learning-management convention, not an autonomous agent that knows your abilities. It does not alter the underlying models as you study. The meaningful adaptation happens when you or a tutor inspect the evidence, identify a misconception, assign a targeted exercise, and reassess.

Use the handoff command to generate a progress summary for a new chat. Include the actual answer file when asking for review. “I finished topology” is not enough information to know which definitions or arguments you can reproduce.

## Reconcile the actual book later

This package maps the supplied chapter titles to the original course and additions. It does not contain or reproduce the complete book text. When the text is available, compare each chapter's definitions, examples, exercises, and arguments with your completed work. Mark genuine new material as a gap and give it a specific assignment.

Do not mark an entire chapter mastered merely because its title contains a familiar word. The precise theorem hypotheses, conventions, and examples can differ. The book audit and advanced roadmap keep that uncertainty visible.

## Your final defense

Explain your pipeline from raw observation to conclusion without hiding behind library names. Derive a small homology example by hand, trace a persistence reduction, justify a stability comparison, reproduce the real-data results, and identify what an independent follow-up would need to establish.

**Completion means demonstrated outcomes in the declared introductory scope.** Algebraic topology and modern TDA continue beyond this course. The extension map names the next subjects and prerequisites rather than claiming they were silently mastered by running these notebooks. Sources R1, R2, R7–R10 and the supplied outline guide that continuation.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/12_lesson.md) · [Worked lab](../notebooks/12_lab.ipynb) · [Your coding notebook](../practice/learner/12_practice.ipynb) · [Reference coding solutions](../practice/12_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
