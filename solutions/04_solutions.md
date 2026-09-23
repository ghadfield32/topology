# Stage 04 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 04.1

**Question:** List the four group axioms and explain why associativity does not imply commutativity.

**Worked answer:** Closure keeps products in the set; associativity permits regrouping; an identity does nothing; every element has an inverse. Commutativity concerns reversing order, which is a different property and fails for many groups of transformations.

## 04.2

**Question:** For a square, give the inverse of a quarter-turn and the inverse of a reflection.

**Worked answer:** The inverse of a counterclockwise quarter-turn is a clockwise quarter-turn, or three counterclockwise quarter-turns. A reflection is its own inverse.

## 04.3

**Question:** Check the endpoints and fixed-subspace condition of the annulus deformation formula.

**Worked answer:** At t=0 the factor is one. At t=1 it is 1/||x||, placing x on the unit circle. If ||x||=1 the factor stays one. The radius is a convex combination of ||x|| and 1, hence remains in [1,2].

## 04.4

**Question:** Why is the same formula invalid at the center of a disk?

**Worked answer:** It divides by ||x||, which is zero at the origin. This is not a removable implementation inconvenience; the proposed formula is not defined on the full disk.

## 04.5

**Question:** Explain homeomorphism versus homotopy equivalence using the annulus and circle.

**Worked answer:** The annulus retracts onto its central circle, with reverse map inclusion; their composites are homotopic to identities. They are not homeomorphic: an annulus has two-dimensional surface neighborhoods, unlike the circle’s one-dimensional neighborhoods. Establishing such distinctions formally uses suitable invariants or local topology.

## 04.6

**Question:** What are the winding numbers of two forward turns followed by one reverse turn?

**Worked answer:** The net winding number is 2−1=1. Winding numbers add under concatenation and negate under reversal.

## 04.7

**Question:** Why does rotating a digit image not automatically produce a valid same-label training example?

**Worked answer:** The array permutation is a valid mathematical symmetry, but the recognition target can change. Augmentation must preserve the actual task label or explicitly transform it.

## 04.8

**Question:** What can and cannot be concluded when two spaces have equal Betti numbers?

**Worked answer:** Different Betti numbers obstruct homotopy equivalence. Equal Betti numbers alone do not prove homeomorphism or homotopy equivalence; homology is not a complete invariant.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
