# Stage 06 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 06.1

**Question:** Explain the difference between Cₖ, Zₖ, Bₖ, and Hₖ.

**Worked answer:** Cₖ is every formal k-chain. Zₖ consists of chains killed by the boundary map. Bₖ consists of boundaries of (k+1)-chains. Hₖ identifies cycles differing by a boundary. Cₖ is not the homology group.

## 06.2

**Question:** Prove ∂₁∂₂=0 for one triangle and explain the general paired-face argument.

**Worked answer:** The triangle boundary is ab+ac+bc. Taking boundary gives a+b+a+c+b+c=0 over F₂. In general every codimension-two face arises through exactly two codimension-one faces; their contributions cancel.

## 06.3

**Question:** Compute β₀ and β₁ of a four-vertex tree with three edges.

**Worked answer:** The graph is connected, so β₀=1. A tree has no independent cycles; rank ∂₁=3 and β₁=3−3=0.

## 06.4

**Question:** Compute β₀ and β₁ of a connected graph with four vertices and five edges, with no triangles filled.

**Worked answer:** Rank ∂₁=4−1=3. With five edges and no 2-simplices, β₁=5−3=2. β₀=1.

## 06.5

**Question:** Explain why adding a triangle can decrease β₁ but never disconnect the existing graph.

**Worked answer:** If the attaching triangular cycle represented a nonzero H₁ class, its new face makes it a boundary. Adding cells cannot remove existing paths, so it cannot split a connected component. A face does not always decrease β₁ if its boundary was already trivial.

## 06.6

**Question:** Derive the Euler–Poincaré identity using the rank formula.

**Worked answer:** Substitute βₖ=nₖ−rₖ−rₖ₊₁ into Σ(-1)ᵏβₖ. The rank terms cancel after an index shift; r₀=0 in ordinary homology and the next map above the complex is zero. What remains is Σ(-1)ᵏnₖ.

## 06.7

**Question:** What extra cells are needed to decide whether a two-dimensional cycle is a boundary?

**Worked answer:** We need 3-chains and ∂₃. A tetrahedron boundary has a 2-cycle; adding the solid tetrahedron makes that cycle a boundary.

## 06.8

**Question:** Why do the results state F₂ and ordinary homology explicitly?

**Worked answer:** Changing the field can change ranks and lose or reveal information related to torsion. Reduced versus ordinary homology changes dimension-zero conventions. Stating both is necessary for comparable results.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
