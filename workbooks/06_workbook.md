# Stage 06 workbook — Turn a loop into a kernel and a quotient

## Chains are combinations of pieces

Fix a coefficient field. In this course it is F₂, so a k-chain is a selection of k-simplices: each coefficient is zero or one. Adding chains is symmetric difference because repeated pieces cancel. Over other fields, coefficients and orientation signs require different arithmetic.

A boundary map sends each simplex to a sum of its codimension-one faces and extends linearly. An edge has its two vertices as F₂ boundary. A triangle has its three edges. A cycle is a chain with zero boundary. A boundary is a chain that is the boundary of a higher-dimensional chain.

The phrase “every boundary is a cycle” has a proof. In the boundary of a boundary, each codimension-two face appears twice, once for each possible order of deleting the two omitted vertices. Two copies sum to zero over F₂. With oriented integer chains, the paired terms instead have opposite signs. This establishes ∂ₖ∂ₖ₊₁=0.

## Work the triangle from beginning to end

Use vertex order 0,1,2 and edge order 01,12,02. The edge-boundary columns are `(1,1,0)`, `(0,1,1)`, and `(1,0,1)`. Their sum is zero, and two are independent. Thus the edge-boundary matrix has rank two and its three-dimensional input space has a one-dimensional kernel.

For the outline, no two-dimensional simplex is present, so the image of ∂₂ is zero. Homology H₁ is the one-dimensional cycle space modulo zero, giving β₁=1.

For the filled triangle, ∂₂ sends the face to the sum of all three edges. Its image is exactly the one-dimensional cycle space. Quotienting that cycle space by itself gives the zero space, so β₁=0. The edge chain still exists; it is its homology class that becomes trivial.

## Derive the rank formula rather than memorizing it

Let Cₖ have nₖ basis simplices. Rank-nullity gives dim ker∂ₖ=nₖ−rank∂ₖ. Boundary-of-boundary says im∂ₖ₊₁ lies inside ker∂ₖ, so the quotient is defined. The dimension of a finite-dimensional subspace quotient is the difference of dimensions. Therefore βₖ=nₖ−rank∂ₖ−rank∂ₖ₊₁.

Each rank must use the same coefficient field. Replacing binary rank by a floating-point real rank can give a wrong answer even for a zero-one matrix. The new coding practice makes you implement pivot elimination with XOR and compares it on exact examples.

## Ordinary versus reduced homology

The course uses ordinary homology. A single point has β₀=1 because it is one component. Reduced homology removes one global H₀ contribution in nonempty spaces; it is a useful alternative convention, but it is not used in our outputs. Never mix the two conventions when comparing a library's answer to a hand calculation.

For finite complexes, H₀ counts components of the geometric realization. In more general singular-homology settings the relevant count is path components, so avoid an unrestricted statement that every possible notion of connectedness is the same.

## What Betti numbers forget

Betti numbers record dimensions over a chosen field. They do not encode lengths, angles, every fundamental-group relation, or all integer-homology information. Over integers, homology can include torsion, so “rank equals complete homology” is not a general statement. The executable course stays over F₂; the advanced bridge identifies what changes outside that scope.

A two-dimensional homology class is also not defined by visualizing an enclosed region in ordinary three-dimensional space. The general definition is algebraic and works for abstract and higher-dimensional spaces. “Void” is an intuition when an appropriate geometric model supports it.

## Test a real image without inventing an answer

At each requested intensity threshold, construct the declared pixel complex, compute boundary matrices, and calculate β₁. Predict that the full rectangular image at threshold 1 has β₁=0 because all pixels are included. Do not predict that the answer at every intermediate threshold must equal the familiar shape of the numeral: handwriting, low resolution, and the pixel convention can change it.

Save the actual sequence of counts and identify its thresholds. In Stage 08, persistence will retain which classes survive across those thresholds, information that this sequence alone discards.

**Before advancing:** reproduce the triangle matrices, prove boundary-of-boundary, and compute the rank formula on a new small complex. Sources R1, R2, R6, and R7 provide the deeper mathematics.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/06_lesson.md) · [Worked lab](../notebooks/06_lab.ipynb) · [Your coding notebook](../practice/learner/06_practice.ipynb) · [Reference coding solutions](../practice/06_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
