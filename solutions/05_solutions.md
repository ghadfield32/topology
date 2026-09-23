# Stage 05 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 05.1

**Question:** How many vertices, edges, and triangles occur in a filled triangle?

**Worked answer:** Three vertices, three edges, one filled triangle. The collection has seven nonempty simplices.

## 05.2

**Question:** Calculate the Euler characteristics of a triangle boundary, filled triangle, tetrahedron boundary, and solid tetrahedron.

**Worked answer:** The values are 0, 1, 2, and 1 respectively, from 3−3; 3−3+1; 4−6+4; and 4−6+4−1.

## 05.3

**Question:** What is wrong with storing a triangle but omitting one edge?

**Worked answer:** It violates closure under faces, so the stored collection is not a simplicial complex. The validation function must reject it; calling closure is an explicit repair/construction choice.

## 05.4

**Question:** Explain abstract simplex versus geometric realization.

**Worked answer:** An abstract simplex records a subset of vertex IDs and incidence relationships. A geometric realization assigns actual points and filled convex simplices satisfying intersection conditions.

## 05.5

**Question:** Why do corner-touching foreground pixels connect under this course’s model?

**Worked answer:** Closed squares include their vertices. Two squares sharing a corner have a nonempty intersection and form a connected union. A four-neighbor digital-connectivity convention would encode a different model.

## 05.6

**Question:** Why can a digit label not be used as the exact ground-truth Betti number of its thresholded image?

**Worked answer:** The label is a semantic class. The actual geometry depends on strokes, resolution, threshold and adjacency. It is a potential hypothesis about typical images, not an exact oracle for every image.

## 05.7

**Question:** For a torus with one open disk removed, calculate Euler characteristic using the surface formula.

**Worked answer:** It is orientable with g=1 and b=1, so 2−2−1=−1. Removing the disk adds a boundary component; it is not a closed torus anymore.

## 05.8

**Question:** Explain why a graph containing a triangle and its clique complex can have different topology.

**Worked answer:** The graph may have only three edges and retain a loop. Its clique complex inserts the triangle face because the three vertices are pairwise adjacent, filling that loop.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
