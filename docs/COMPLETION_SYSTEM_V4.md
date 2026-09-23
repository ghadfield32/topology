# Learn, demonstrate, retain, and extend

## One stable course, not an expanding to-do list

The topology foundation is stages 00–12. The geometry continuation is 13–20. Version 4 deepens those same stages. You do not need to finish every advanced paper before solving the next small exercise, and you should not skip assumptions merely because a notebook runs.

The [84-outcome coverage map](COVERAGE_V4.md) is the working definition of scope. Each stage has four specific outcomes. Outcomes are teaching targets; the shipped map does not contain evidence that the learner has met them. The actual full-book audit and major-theorem proof obligations remain separate.

## A repeatable small-session pattern

Begin by recalling yesterday's idea without looking. Name the problem the new concept solves. Read one subsection, then close it and explain its example. Work one calculation before running code. Predict a result, execute it, and account for the difference. Finish with a new problem, not a rereading streak.

A suggested study block allocates about ten minutes to recall, twenty to a new explanation and worked example, twenty to calculation or code, and ten to an independent explanation. This is an adjustable study policy, not a validated optimal schedule or a promise about time to mastery. Split it further when notation or proofs require more effort.

Within a stage, the order is lesson and prerequisite repair, workbook, guided session, original lab, consolidation lab, learner code, conceptual questions, transfer questions, and later recall. You can omit a redundant worked example after independently explaining it, but not an unmet learning outcome. The navigator is a convenience, not a prerequisite-enforcement or grading engine.

## Make the level of assistance visible

“Read” means exposure. “Practiced” means you worked an example, possibly with a solution nearby. “Demonstrated” means a declared independent assessment met the rubric. “Retained” is a log status after the configured delayed exercise; it is not a lifetime property.

Before viewing a solution, write a partial attempt. When stuck, first state the definition you need, then draw a smaller example, then inspect a hint, and only then the solution. After seeing the solution, solve a changed example without it. Label the original attempt as assisted. This avoids treating recognition of an answer as ability to produce one.

## Assessment rubric

Use five dimensions, each scored from zero to four: definition and assumptions; hand reasoning; computation and validation; interpretation and failure cases; independent transfer. Zero means missing, one means a serious misconception, two means partly correct with substantive assistance, three means correct with a minor omission, and four means correct, explicit and independent. Sum out of twenty and multiply by five for a percentage.

The existing proposed progression threshold is 85%. Every critical misconception must also be corrected. Examples include treating every cycle as a nontrivial homology class, using graph-only calculations as full Rips H1, calling predicted geometry calibrated metres, treating row order as time, or treating a later-confirmed event as known at its onset. These mistakes block progression regardless of a numerical average.

For an assessment, use a new example and do not keep reference answers open. A person reviewing the work should inspect the actual proof, assumptions and outputs. The CLI records your declarations; it does not provide that review. Its boolean flags cannot verify honesty or correctness.

## Repair a specific gap

If a definition is wrong, return to one example and one nonexample. If algebra is wrong, reduce the matrix or chain to the smallest failing case. If code disagrees with a hand calculation, inspect the input convention before changing the expected answer. If interpretation is wrong, write a claim weaker than the evidence supports, then state what additional evidence would allow a stronger one.

If a loop disappears unexpectedly, ask whether triangles were inserted and at which values. If a distance estimate is wrong, audit units, coordinate frames and principal points before swapping models. If a detector is late, separate the event's candidate onset from the decision time. This is targeted repair, not restarting all earlier chapters.

## Three depths of completion

**Working foundation:** explain and calculate small examples, execute and inspect the labs, solve the code exercises, and pass independent questions. This supports competent reading and bounded experiments.

**Mathematical depth:** reproduce the elementary proofs in the proof atlases. For larger results such as interval decomposition, the nerve theorem and persistence stability, state precise hypotheses, explain proof structure, and complete the assigned external reading. Do not mark a full proof as completed after seeing a numerical demonstration. The projective-plane supplement adds coefficient sensitivity without pretending to prove the whole cellular-homology framework.

**Independent application:** formulate a question, select a representation, preserve provenance, fit only allowed data, evaluate appropriate holdouts, report failure modes, and defend the conclusion. Re-running the supplied capstone is preparation; a new investigation is a separate requirement. Actual book coverage requires reading the actual book. Advanced topology and vision branches are explicitly subsequent work, not silently claimed completed.

## Preserve a useful evidence record

Use one versioned answer file per attempt. Include the question, your initial reasoning, result, corrections, assistance used, and remaining uncertainty. Store important figures or output tables nearby. An evidence hash checks file integrity, not mathematical truth. Changing the file after recording it should be visible, not concealed.

The log schema remains version 3 for continuity across these 21 stages. The package version is 4.0.0. A fresh shipped log has no attempts. Keep records from earlier releases and the exact relative answer paths. `study.py verify-evidence` reports unchanged, modified, missing, or outside-root paths without modifying any record.

The review-date sequence of 1, 3, 7, 14 and then 30 days is a course policy. The commands compute dates when run; they do not create a scheduled task. Past successful recalls do not exempt you from repairing a newly discovered misconception.

## Continue here or in another chat

Run `python scripts/learn.py handoff`, attach the current answer file and relevant outputs, and identify which stage and exercise you attempted. Ask the reviewer to distinguish a sound argument from a plausible-looking result. A useful review says which line first becomes unsupported and gives a smaller question that repairs it.

The course should accumulate demonstrated understanding and reusable evidence. It should not accumulate unsupported “completed” labels, new architectures, or model downloads that distract from the next teachable problem.
