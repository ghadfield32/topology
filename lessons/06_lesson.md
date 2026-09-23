# Stage 06 — Chains, boundaries, homology, and Betti numbers

**Starting point:** Complete the Stage 05 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Turn simplices into algebra
Fix a coefficient field, initially F₂={0,1}. A **k-chain** is a formal sum of k-dimensional simplices with coefficients in the field. Over F₂, adding the same simplex twice cancels it. The chain vector space Cₖ has one basis vector per k-simplex. Its dimension is the number of those simplices, not the number of holes.

The **boundary map** ∂ₖ sends a k-simplex to the sum of its codimension-one faces. Over F₂ no signs are needed. Over other fields, oriented simplices require alternating signs, and reversing orientation negates a simplex. Choosing F₂ makes the arithmetic easier; it does not make coefficient choice universally irrelevant.

For edge [a,b], its boundary over F₂ is a+b. For triangle [a,b,c], its boundary is [a,b]+[a,c]+[b,c]. Apply boundary again: each vertex appears twice, so the result is zero. More generally, each codimension-two face appears twice, yielding `∂ₖ₋₁∂ₖ=0`. With orientation signs, the corresponding pairs have opposite signs.

## 2. Cycles are not necessarily holes
A **cycle** is a chain with zero boundary: `Zₖ=ker ∂ₖ`. A **boundary** is the boundary of some next-dimensional chain: `Bₖ=im ∂ₖ₊₁`. Because boundary-of-boundary is zero, Bₖ is contained in Zₖ.

A cycle around a filled triangle is the boundary of the triangle and is therefore trivial in first homology. The same three-edge cycle without the filled triangle is not the boundary of any available 2-chain. The visual outline alone does not answer whether the cycle represents a hole; the higher-dimensional cells matter.

**Homology** is the quotient `Hₖ=Zₖ/Bₖ`. Two cycles represent the same class when their difference is a boundary. Over a field its dimension is the **Betti number** βₖ. In a finite simplicial complex, β₀ counts components, β₁ counts independent one-dimensional homology classes, and β₂ counts independent two-dimensional classes. Enclosed voids can be a useful picture in familiar embeddings, but that is not the general definition of β₂.

We use ordinary homology. A nonempty connected contractible space has β₀=1, not zero. Reduced homology modifies the zero-dimensional part so that a point has no reduced homology; mixing these conventions causes avoidable disagreements.

## 3. Calculate an entire example by hand
Order triangle vertices as 0,1,2 and edges as 01,02,12. The boundary matrix ∂₁ has columns (1,1,0), (1,0,1), (0,1,1). Its rank over F₂ is two. There are three independent edge coordinates, so its kernel has dimension 3−2=1. The sum of all three edges is the nonzero cycle.

For the unfilled boundary, C₂ is zero and ∂₂ has rank zero. Thus β₁=3−2−0=1. For the filled triangle, ∂₂ has one nonzero column (1,1,1), with rank one. Then β₁=3−2−1=0. In both cases β₀=3−rank(∂₁)=1.

For a general finite complex over a field, rank–nullity yields:

`βₖ = dim(Cₖ) − rank(∂ₖ) − rank(∂ₖ₊₁)`.

Compute both ranks in the same field. A floating-point rank over R is not a substitute for exact elimination over F₂. The function `rank_mod2` uses XOR to perform row operations, and the Stage 01 counterexample demonstrates why this matters.

## 4. Why the checks complement one another
Checking `∂∂=0` verifies an important structural identity. Checking known Betti numbers verifies interpretation and rank calculations. Checking that the alternating Betti sum equals the alternating simplex sum supplies the Euler–Poincaré identity for finite complexes. None alone proves the whole implementation correct, but together they constrain different failure modes.

The equality of alternating sums follows by substituting the rank formula: each boundary rank appears twice with opposite signs and cancels, leaving the alternating chain-space dimensions. This derivation is worth doing on paper rather than memorizing another formula.

Computing H₁ from only edges can overcount loops that triangles would fill. To compute Hₖ for a proposed higher-dimensional complex, include the (k+1)-simplices needed for ∂ₖ₊₁. A graph's homology is valid for the graph; it just need not be the homology of the clique complex you intended to study.

## 5. Real-data calculation and coefficient awareness
Apply the pixel construction to several intensity thresholds of a training digit. Calculate β₀ and β₁. At the final threshold all pixels enter and the rectangular region is contractible, so the expected result is [1,0] for the reported dimensions. At earlier thresholds the outcome is data-dependent.

These are homology values of the specified thresholded pixel model, not a proof of the topology of an ideal handwritten symbol. A low-resolution stroke can join components or close a loop unexpectedly. Include the displayed image, threshold, connectivity convention, and coefficients with the result.

Beyond this stage, learn that integer homology can include torsion, which Betti numbers alone omit. For example, coefficient changes can alter the measured homology of nonorientable spaces. The computational core stays over F₂; the advanced bridge explains what additional theory is needed before generalizing the implementation.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**06.1.** Explain the difference between Cₖ, Zₖ, Bₖ, and Hₖ.

**06.2.** Prove ∂₁∂₂=0 for one triangle and explain the general paired-face argument.

**06.3.** Compute β₀ and β₁ of a four-vertex tree with three edges.

**06.4.** Compute β₀ and β₁ of a connected graph with four vertices and five edges, with no triangles filled.

**06.5.** Explain why adding a triangle can decrease β₁ but never disconnect the existing graph.

**06.6.** Derive the Euler–Poincaré identity using the rank formula.

**06.7.** What extra cells are needed to decide whether a two-dimensional cycle is a boundary?

**06.8.** Why do the results state F₂ and ordinary homology explicitly?

## Mastery gate

Calculate small homology groups by hand, prove boundary-of-boundary, and explain every term in the Betti formula.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R2, R7. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/06_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/06_solutions.md`, record what was independent, and continue only when the gate is met.
