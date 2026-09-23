# Stage 02 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 02.1

**Question:** Check all metric axioms for d(x,y)=|x−y| on R.

**Worked answer:** Absolute values are nonnegative, |x−y|=0 exactly when x=y, |x−y|=|y−x|, and |x−z|=|(x−y)+(y−z)|≤|x−y|+|y−z|.

## 02.2

**Question:** Give a numeric counterexample showing squared Euclidean distance is not a metric.

**Worked answer:** Use 0,1,2: (0−2)²=4 while (0−1)²+(1−2)²=2.

## 02.3

**Question:** List all open sets of the discrete and indiscrete topologies on {0,1}.

**Worked answer:** Discrete: empty, {0}, {1}, {0,1}. Indiscrete: empty and {0,1}. Both satisfy the axioms.

## 02.4

**Question:** Explain why (0,1] is open in the subspace (0,2) or determine that it is not.

**Worked answer:** It is not open. Every subspace neighborhood of 1 includes numbers slightly larger than 1 and less than 2, which are outside (0,1]. The excluded point zero is not the obstacle.

## 02.5

**Question:** Prove every finite set of distinct metric points is discrete.

**Worked answer:** For each x with at least one other point, take half the minimum of its finitely many positive distances to other points. The corresponding ball contains only x. A one-point space is already discrete. Every subset is a union of these open singletons.

## 02.6

**Question:** If two different sample IDs have the same features, is Euclidean distance on IDs a strict metric?

**Worked answer:** It is a pseudometric on the IDs: distinct IDs can have distance zero. On the set of distinct coordinate vectors it is a metric.

## 02.7

**Question:** Explain why equal topology does not imply equal persistence diagrams in distance units.

**Worked answer:** A topology remembers which sets are open, not the numerical thresholds at which edges enter a proximity complex. Uniform scaling preserves topology while scaling all distance-based birth and death values.

## 02.8

**Question:** Run the real-data metric comparison and state which preprocessing decision could change the result.

**Worked answer:** The saved stage report records the actual raw and standardized neighbor selections. Rescaling features, using a different metric, changing the observation unit, or adding labels can change them. Do not invent a universal interpretation from one ranking.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
