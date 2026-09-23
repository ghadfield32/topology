# Stage 12 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 12.1

**Question:** Write the complete worked-capstone question in one sentence without making a broad claim about all computer vision.

**Worked answer:** For example: “On the frozen per-image split of the bundled digits snapshot, do the specified F₂ pixel-persistence summaries improve the declared logistic-regression baseline’s held-out image accuracy?” The scope includes the split and method.

## 12.2

**Question:** Why is it legitimate to refit on training plus validation before the final test?

**Worked answer:** The validation stage has finished model-choice work. Refitting the selected procedure uses all development data while the final test remains untouched. The scaler must also be refitted only on development data.

## 12.3

**Question:** List the frozen topological construction and feature choices.

**Worked answer:** Known normalization 1−image/16; closed nonperiodic square pixels; two-triangle subdivision preserving entry values; F₂; ordinary H₀/H₁; positive finite intervals for lifetime sums; fixed Betti thresholds 0,.25,.5,.75,1; 20 declared features; validation selection over the stated C values.

## 12.4

**Question:** Why is the current test not an unseen-writer test?

**Worked answer:** Writer IDs are unavailable in this snapshot. The new partition splits individual images, which may include the same writer on both sides. It is also not the original full UCI train/test experiment.

## 12.5

**Question:** What must change in the evidence plan after adapting the method to improve a viewed test score?

**Worked answer:** The viewed test is now exposed. Record the adaptation and evaluate on a fresh independent set or another justified untouched evaluation design. Reusing the old number as an unbiased final test would overstate the evidence.

## 12.6

**Question:** Propose a subject/session-safe split for a sports-motion study.

**Worked answer:** Keep all windows from an athlete/session together; for unseen-athlete deployment, hold out athletes entirely. Create overlapping windows within the assigned partition and respect feature availability times. Report calibration and labeling provenance.

## 12.7

**Question:** Explain why equal Euler characteristic does not establish equal topology.

**Worked answer:** Euler characteristic is only an alternating sum of Betti numbers, and even all Betti numbers are not a complete topological invariant. Equal summaries can hide substantial structural differences.

## 12.8

**Question:** Name the evidence required to mark this course and the book audit complete.

**Worked answer:** Independent definitions, proofs, hand calculations, executable code, completed checks with honest pending items, held-out interpretation, delayed retention, and an actual section-by-section book coverage audit. Reading alone is not enough.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
