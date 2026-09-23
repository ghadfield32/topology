# Stage 12 — Capstone: reproduce, defend, transfer, and audit the book

**Starting point:** Complete the Stage 11 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Complete a question, not just a notebook
The worked capstone question is: **On the frozen per-image digits split, how do fixed topological summaries compare with raw pixels for recognizing the recorded digit label?** This is deliberately narrower than asking whether topology improves all computer vision.

State the observation unit, input data, labels, hypothesis and evaluation metric before opening the test results. A **baseline** supplies a comparison that could plausibly solve the task without the new technique. Here we include a majority-class classifier, raw pixels, topology alone, and their combination. The same test rows are used for all methods so their errors can be compared directly.

The primary reported metric is accuracy: the fraction of test labels predicted correctly. Also record per-class recall and a confusion matrix, which show which classes are mistaken for which. A single aggregate score can hide differences between common and rare classes. The dataset classes are reasonably represented in the frozen splits, but we still inspect all of them.

## 2. Freeze the procedure before opening the holdout
Stage 11 records the validation-selected regularization value for each representation. For this worked example, refit each selected pipeline on training plus validation rows. Refit the scaler on that combined development set; do not carry over a scaler fitted on the whole dataset. Predict the held-out test rows and record every result together with sample IDs.

The deterministic topology transform uses `f=1−intensity/16`, closed square pixels, a filtration-preserving triangulation, F₂ coefficients, ordinary H₀/H₁, positive finite intervals for lifetime sums, and fixed Betti sample thresholds. The experiment does not tune these choices on test images. Altering them after seeing test results requires treating the existing holdout as exposed and obtaining new evidence.

The bundled 1,797-image collection corresponds to the original UCI test snapshot distributed with scikit-learn. Our internal train/validation/test partition is newly created for learning and lacks writer IDs. Consequently, test accuracy is **image-level accuracy on this split**, not an estimate certified for unseen writers. The official UCI full training set is not bundled and was not secretly substituted.

## 3. Write an evidence-based conclusion
Use a conclusion with this structure: “Under the specified split, representation, model class and preprocessing, method A achieved the recorded result. Relative to the baseline, the observed change was this many correct images. This experiment does not establish these broader claims.” Include worse results and equal results; do not define success as obtaining a topology improvement.

The provided reports contain actual execution outputs, not invented performance targets. Rounded floating-point results can vary slightly with numerical environments. Dataset IDs, splits, counts, exact constructions and major expected behaviors should remain consistent. A discrepancy is a reason to investigate, not overwrite the saved benchmark.

A formal confidence interval or hypothesis test would require additional inferential choices and attention to dependence. Writer-level dependence is not observable here. We therefore avoid presenting a small score difference as statistically significant or as a general performance advantage. The point is a transparent experiment with known limits.

## 4. Your independent capstone
After reproducing the worked example, choose a substantially new task. A sports option is to compare motion-window features with and without topological summaries, splitting by athlete and session and ensuring every feature is available at the prediction cutoff. A reconstruction option is to measure how controlled occlusion or geometric defects change shape descriptors, compared with direct geometric baselines.

These are proposed research designs, not demonstrated benefits for WMS. Begin with well-defined observations, calibrated units, and ground truth appropriate to the target. Homography on a ground plane does not automatically license metric positions of airborne objects; learned monocular depth is not automatically calibrated geometry. Do not feed uncertain geometric outputs into TDA and then interpret a stable diagram as proof that upstream calibration is correct.

Use the independent-capstone protocol in `docs/CAPSTONE_PROTOCOL.md`. It requires a question, observation unit, data provenance, inclusion rules, leakage plan, metric and filtration choices, expected failure modes, frozen evaluation, reproducible code, and a conclusion that could honestly be negative.

## 5. Explain the whole chain without hiding behind software
Your oral defense should connect every step: why this distance; why this complex; why these coefficients; why these dimensions; why this scale; what the diagram records; what it discards; how the representation was chosen; how the test split matches deployment; and what the data cannot answer.

You should be able to compute one small example by hand, trace one reduction, prove boundary-of-boundary is zero, and identify an invalid inference. These demonstrations establish a deeper form of completion than viewing every notebook output. The progress ledger distinguishes reading, guided practice, independent solving and delayed retention.

## 6. Audit the actual book when available
The coverage map aligns the supplied chapter titles to lessons, labs, proof depth and limitations. It does not claim that the unpublished/full book text has been examined. When you have the book, compare each actual section, definition, example and exercise type with the course. Add any missing item to the gap log and work it explicitly. Do not silently mark an unfamiliar argument as “covered” because a chapter title sounds familiar.

Read the author's freely available paper as an example to critique, not as an authority that makes every proposed statistic standard. Record its metric, filtration, evidence and validation. Proposed stability summaries should not be confused with the mathematical stability theorem or with statistical significance.

## 7. What follows the introductory core
The advanced bridge names integer homology and torsion, cohomology and cup products, fundamental-group methods, manifold inference, optimal representatives, robust distance-to-measure constructions, zigzag persistence, multiparameter persistence and differentiable topological learning. These are not all required to master the present scope. Each needs its own assumptions, algorithms and validation.

Finish by solving the final assessment without notes, correcting every critical error, and returning to related questions after a delay. No script should award mastery merely because Python ran. You complete this course by being able to explain, derive, compute, test and appropriately limit its conclusions.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**12.1.** Write the complete worked-capstone question in one sentence without making a broad claim about all computer vision.

**12.2.** Why is it legitimate to refit on training plus validation before the final test?

**12.3.** List the frozen topological construction and feature choices.

**12.4.** Why is the current test not an unseen-writer test?

**12.5.** What must change in the evidence plan after adapting the method to improve a viewed test score?

**12.6.** Propose a subject/session-safe split for a sports-motion study.

**12.7.** Explain why equal Euler characteristic does not establish equal topology.

**12.8.** Name the evidence required to mark this course and the book audit complete.

## Mastery gate

Reproduce and defend the worked capstone, complete an independent application, and retain an explicit book-audit gap log.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: D1, D2, D3, R9, R10. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/12_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/12_solutions.md`, record what was independent, and continue only when the gate is met.
