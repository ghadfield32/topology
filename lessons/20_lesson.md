# Stage 20 — Independent spatial capstone and continuing mastery

One evidence chain from observations to a justified conclusion.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 12, Stage 13, Stage 14, Stage 15, Stage 16, Stage 17, Stage 18, Stage 19.

## 1. The capstone is a new question, not another rerun
The supplied notebooks are demonstrations with visible answers. Finishing them gives practice, not an independent result. For your own capstone, select a question whose answer is not already exposed by the reference notebook. Start small enough that an incorrect assumption can be found and corrected.

A suitable first spatial question is: “On a measured static scene, does a learned proposal improve reconstruction or initialization compared with the calibrated baseline under a declared error and coverage requirement?” A topology-focused alternative is: “Does this descriptor add information beyond simpler geometric features under independent evaluation?” Either can legitimately end in a negative result.

## 2. Write the protocol before examining the final outcome
Specify the observation unit, capture conditions, camera model, clock assumptions, coordinate frame, metric units, calibration references, registration anchors, holdouts, masks, selection rules, metrics and thresholds. Name which data may fit parameters and which must remain untouched until evaluation.

Also state the claim you are not making. A static-scene result is not a fast-motion sports result. A small CPU transformation benchmark is not live application latency. A learned latent representation is not a calibrated map. A stable topological feature is not a semantic object label.

## 3. Use a declared sequence of acceptance tests
First establish the numerical contracts: dimensions, units, transforms, finite values and identities. Then test geometric consistency such as reprojection. Then test independent measured references. Finally evaluate generalization across independent scenes or sessions when that is the intended claim. A later test does not erase a failed earlier assumption.

The package's final bridge notebook builds an evidence summary from the executed stage reports. It checks those reports are present and states the scope of their results. It does not turn every source status into a green production acceptance badge. GPU inference and real hand–ball annotation remain unexecuted requirements until supplied.

## 4. A practical static-scene collection
Choose an object or room with visible stationary landmarks and measured distances. Capture overlapping views with a fixed documented camera mode. Preserve original images, image sizes and timestamps. Reserve some measurements from all fitting steps. Record measurement uncertainty and repeat a small subset to expose mistakes.

Start without moving people. Once static geometry is supported, introduce a stationary person, then controlled slow movement, occlusion and fast motion as separate experiments. Each new condition changes the assumptions. The attachment's staged integration boundary is retained: learned output is a proposal evaluated within the existing metric state, not a replacement world definition.

## 5. Evaluate a model without losing reproducibility
Record the exact repository revision, checkpoint hash, model family, preprocessing, precision, device, head selection, input order and image hashes. Preserve raw predictions separately from registered/refined outputs. An unknown checkpoint or unrecorded image crop makes later comparison unreliable even if the diagram looks familiar.

The included optional runner creates prediction arrays and provenance for the original VGGT API. It does not automatically align those results to metre ground truth. Registration and holdout measurement are explicit subsequent steps. The normal course notebooks do not invoke that runner.

## 6. Learning continues through evidence, not an expanding to-do list
Keep the original 00–12 core in sequence. Append 13–20 only when their prerequisites are understood. Use the progress log to distinguish practiced, independently demonstrated, retained and needing review. A demonstrated stage can later require review; this is not failure of the system but a more accurate description of learning.

The review intervals are a course policy, not a personalized scientifically optimal schedule. No timer runs in the background. The CLI prints due items when you call it. Record actual attempts and attach evidence files rather than writing future completion dates.

## 7. What “complete” can reasonably mean
Completion means all agreed outcomes have evidence: definitions, hand calculations, elementary proofs, algorithms, real-data interpretation, independent work and delayed recall. It does not mean every branch of mathematics or every deployment is mastered forever.

The actual book has not been read in full. Its supplied section titles remain an audit map. When you obtain the text, check its definitions, examples, arguments and exercises against this course and record any gaps. Do not infer full chapter coverage from a similar title.

## 8. Where to deepen next
For pure mathematics, continue with covering spaces, fuller surface classification, cohomology and more of algebraic topology. For TDA, study statistical inference, sampling guarantees and multiparameter persistence. For geometry, deepen differential geometry, bundle adjustment, robust estimation and observability. For systems, study synchronization, uncertainty-aware fusion and causal event evaluation.

Those are explicit next tracks with prerequisites. They are not hidden prerequisites that block finishing the agreed introductory course, and they are not claims that a few extra notebooks exhaust the fields.

## Independent conceptual exercises

1. Formulate a falsifiable spatial-reconstruction or TDA question.
2. Which evidence must be reserved from registration and parameter selection?
3. Why is the reference notebook not an independent capstone?
4. Name the required model and input provenance for a reproducible run.
5. What changes when moving from static reconstruction to live interaction detection?
6. What is still required to claim coverage of the actual book?

## Mastery gate

Defend an independent protocol and retain an honest list of external experiments and book-audit work still required.

Readings: U01, T01, V04. See the [source ledger](../docs/SOURCES_V3.md) for checked links, evidence status and source differences.
