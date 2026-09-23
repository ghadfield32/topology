# Stage 07 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 07.1

**Question:** At what value does a Rips simplex enter under the declared convention?

**Worked answer:** At the largest pairwise distance among its vertices; vertices enter at zero. The simplex is present whenever all its edges have entered.

## 07.2

**Question:** Why does the equilateral triangle have no positive H₁ Rips bar?

**Worked answer:** All three edges and the filled triangular face enter at ε=1. Any edge-cycle birth and face death at that same value give a zero-length interval, not persistence over an interval of positive length.

## 07.3

**Question:** Derive the two Čech radii for that same triangle.

**Worked answer:** Each pair of equal-radius balls first touches when 2r=1, so r=1/2. The three centers are equilateral; their common circumcenter lies at distance 1/√3, which is the first common triple intersection radius.

## 07.4

**Question:** Prove the elementary inclusions Čech_r⊆Rips_2r⊆Čech_2r in Euclidean space.

**Worked answer:** For a Čech simplex, choose a common intersection point p; each center pair is at most r+r apart. For a Rips simplex of diameter≤2r, choose one center p; it lies within 2r of every center, so it is in the common intersection of the radius-2r balls.

## 07.5

**Question:** Explain the good-cover assumption in a nerve theorem.

**Worked answer:** The nonempty finite intersections must satisfy the theorem’s contractibility requirements, with the appropriate cover hypotheses. An overlap pattern alone need not determine the union’s homotopy type.

## 07.6

**Question:** How many candidate edges and triangles exist for 20 observations?

**Worked answer:** There are choose(20,2)=190 edges and choose(20,3)=1,140 triangles. Including the 20 vertices yields 1,350 candidate simplices through dimension two.

## 07.7

**Question:** Why does reporting H₁ from an edge-only complex answer a different question?

**Worked answer:** An edge-only graph omits triangle boundaries that could make graph cycles trivial in a clique complex. Its homology can be correct for the graph and still wrong for the intended Rips complex.

## 07.8

**Question:** If an alpha value is 4 in squared-radius units, what is the radius? Is this automatically Rips ε=2?

**Worked answer:** The radius is sqrt(4)=2. That conversion only fixes alpha units. It does not make the alpha construction identical to a Rips construction at edge threshold two.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
