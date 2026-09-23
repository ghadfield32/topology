# Stage 08 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 08.1

**Question:** Explain what the maps in a persistence module add beyond the vector-space dimensions.

**Worked answer:** The maps specify how classes continue, merge into combinations, or disappear. Identity and zero maps between equal-dimensional spaces give different persistence behavior even though the dimension sequence is identical.

## 08.2

**Question:** Write all positive or essential bars for the unit square in H₀ and H₁.

**Worked answer:** H₀: three [0,1) intervals and one [0,∞). H₁: one [1,√2). Zero-length pairs at tied events are omitted.

## 08.3

**Question:** At t=1, t=1.2 and t=√2, what is β₁ under our endpoint convention?

**Worked answer:** It is 1 at t=1, 1 at t=1.2, and 0 at t=√2, since [birth,death) includes its left endpoint and excludes the right.

## 08.4

**Question:** Why can an infinite death mean truncation rather than a permanent feature?

**Worked answer:** The algorithm knows only the supplied simplices and values. A class surviving to the largest computed threshold is unpaired there even if additional later simplices would kill it.

## 08.5

**Question:** What does multiplicity mean in a persistence diagram?

**Worked answer:** More than one interval can have the same birth/death pair. They are separate classes even if a scatter plot draws their points on top of one another.

## 08.6

**Question:** Does a long interval identify one unique physical loop in the original data?

**Worked answer:** No. A homology class contains many cycles differing by boundaries, and barcode bases and representatives need not be unique. Localizing a feature is an additional task.

## 08.7

**Question:** Explain why the pixel filtration has no essential H₁ after all pixels enter.

**Worked answer:** The union becomes the full rectangular image domain, which is contractible. Ordinary homology then has one H₀ class and no positive-dimensional classes.

## 08.8

**Question:** Why must the two real-data examples label their horizontal axes differently?

**Worked answer:** Iris uses a distance-based Rips construction; digits use a normalized intensity sublevel construction. Equal numerical values across those parameters have no intrinsic common geometric meaning.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
