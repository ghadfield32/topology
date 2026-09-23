# Proof depth and deeper study

This guide tells you what has been established, what you should prove, and where full treatments are still part of the learning task. It is not an assertion that every major theorem is fully proved in the short lessons.

## Proofs to reproduce independently in the core

Inverse images preserve unions/intersections; absolute distance satisfies the metric axioms; squared Euclidean distance fails the triangle inequality; finite distinct metric samples are discrete; compositions of continuous maps are continuous; continuous images preserve connectedness and compactness; a compact-to-Hausdorff continuous bijection is a homeomorphism; the stated annulus homotopy is a deformation retraction; boundary-of-boundary is zero; the Betti rank formula; the finite Euler–Poincaré identity; the square's exact persistence endpoints; and the elementary shifted-sublevel inclusions from a uniform perturbation bound.

For each proof, write assumptions, conclusion, every logical step, and one example showing why an important hypothesis matters. Numerical plots illustrate these proofs but do not replace them.

## A deeper independent check: the persistence rank invariant

Let A⊆B be subcomplexes. Work over one field and embed Cₖ(A) in Cₖ(B) by matching simplex bases. The rank of the induced map Hₖ(A)→Hₖ(B) is

`dim(Zₖ(A) + Bₖ(B)) − dim(Bₖ(B))`.

Why? The image consists of cycles from A viewed modulo boundaries in B. Under the quotient map Cₖ(B)→Cₖ(B)/Bₖ(B), the image of Zₖ(A) is `(Zₖ(A)+Bₖ(B))/Bₖ(B)`. Its dimension is the displayed difference. This is an instance of taking the dimension of a subspace quotient.

Compute a basis for the nullspace of ∂ₖ(A), embed it into Cₖ(B), append columns of ∂ₖ₊₁(B), and subtract the rank of ∂ₖ₊₁(B). That rank must equal the number of barcode intervals born no later than A's threshold and dying after B's threshold. Unlike checking Betti numbers only at individual thresholds, this can detect incorrect persistence pairings with the same dimension sequence.

`tests/test_independent_checks.py` implements this check for several small random filtrations. It uses an independently written full Gauss–Jordan nullspace construction, while some low-level input and rank code is shared. Call this a complementary oracle, not complete independent certification.

## Major theorems: complete statement and proof strategy required

**π₁(S¹) ≅ Z.** Learn path/loop lifting or an equivalent rigorous winding-number argument. Show that winding number is invariant under based homotopy, that every integer is realized, and that equal winding numbers imply equivalent loop classes. Hatcher's fundamental-group introduction supplies a full route. The animated annulus is not a proof of this theorem.

**Compact surface classification.** Learn the exact compactness, connectedness, boundary and orientability distinctions and polygon identifications. Recognize sphere, torus, projective plane, cylinder, Möbius strip and Klein bottle examples. A full classification proof is deeper than the executable core; choose it as an extension with Hatcher and a dedicated surfaces reference.

**Finite interval decomposition.** State the theorem for finite-index, finite-dimensional vector-space representations with compatible forward linear maps. Understand how adapted bases and changes of basis isolate classes by their birth and survival and yield interval summands. The reduction algorithm realizes the required normal-form information. A full uniqueness/existence proof belongs in the ETH persistence reading; do not claim that a successful reduction example proves it for every module.

**Nerve theorem.** State a precise version and verify its cover and intersection hypotheses in each application. Build the homotopy-equivalence intuition through a partition-of-unity/good-cover argument or the finite-convex-cover version. Pairwise intersection graphs alone do not establish all higher intersections.

**Stability.** Prove the shifted-sublevel inclusions first. Then study the algebraic stability/isometry result for the relevant finite constructible modules to connect interleavings to bottleneck matching. Keep continuous tame/q-tame variants separate and state any new hypotheses when moving beyond finite filtrations.

## Advanced bridge, not hidden introductory requirements

Integer homology and torsion; coefficient-change theorems; cohomology and cup products; van Kampen and covering spaces; representative cycles versus cocycles; geometric reconstruction and sampling theorems; distance-to-measure and outlier robustness; zigzag persistence for non-nested changes; multiparameter persistence and its lack of the same universal simple barcode classification; scalable complexes and sparse approximations; differentiable topological losses with approximation/gradient caveats.

For each extension, write its new problem, prerequisite theorem, assumptions, a small exact example and a validation method before selecting software. The current code deliberately stays within its declared finite F₂ setting.

Primary references are R1, R2, R6, R7 and R8 in SOURCES.md. These are reading assignments, not PDFs redistributed inside the archive.
