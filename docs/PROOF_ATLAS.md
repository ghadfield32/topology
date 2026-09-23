# Proof atlas: know what is proved and what is illustrated

These arguments are original explanations, not excerpts from the book. Definitions and standard results align with the references in [Sources](SOURCES.md), especially Hammack (R4), Morris (R3), Hatcher (R7), Tinarrage (R1), ETH (R2), and Chazal–Michel (R8). A program checks cases; a proof establishes a stated conclusion from stated hypotheses.

## 1. Inverse images preserve intersections — complete proof

Let f:X→Y and A,B⊆Y. An arbitrary x∈X belongs to f⁻¹(A∩B) exactly when f(x)∈A∩B. By the definition of intersection this means f(x)∈A and f(x)∈B. By the definition of inverse image this means x∈f⁻¹(A) and x∈f⁻¹(B), which means x∈f⁻¹(A)∩f⁻¹(B). Every membership condition is equivalent, so the sets are equal. Neither injectivity nor surjectivity was required. To practice, replace intersection by union and then by complement relative to the declared spaces.

## 2. A finite set of distinct metric points is discrete — complete proof

Let X be finite with metric d. If X has one point, {x}=X is open. Otherwise, fix x∈X. All finitely many numbers d(x,y), y≠x, are positive. Their minimum m is positive. The open ball of radius m/2 about x contains x and no other point. Thus each singleton is open. Any subset is a union of singletons, hence is open. The empty case is also discrete. This concerns the finite sample's own topology, not an inferred continuous object behind it. The proof fails for infinitely many points because a positive minimum need not exist.

## 3. Compositions of continuous maps are continuous — complete proof

Take continuous f:X→Y and g:Y→Z. For any open O⊆Z, g⁻¹(O) is open in Y. Therefore f⁻¹(g⁻¹(O)) is open in X. But this set equals (g∘f)⁻¹(O). Since this works for every open O, the composition is continuous. Record the domain of each intermediate set: many incorrect proofs confuse an image with an inverse image.

## 4. Continuous images of connected spaces are connected — complete proof

Suppose X is connected and f:X→Y is continuous. Use the subspace topology on f(X). If f(X) were the union of disjoint, nonempty, relatively open sets U and V, their inverse images would be disjoint nonempty open sets in X covering X. They are nonempty because every element of f(X) has a preimage. This contradicts connectedness. So f(X) is connected. We are not asserting that all of Y is connected unless f is onto Y.

## 5. Compact-to-Hausdorff continuous bijections — complete proof with lemmas

**Claim:** a continuous bijection f:X→Y from compact X to Hausdorff Y is a homeomorphism.

First, closed subsets A of a compact space are compact: add X\A to an open cover of A, select a finite subcover of X, then discard X\A. Relative open sets can be written as intersections with open sets of X, which justifies using an ambient cover.

Second, continuous images of compact spaces are compact: pull an open cover of the image back to the domain, select finitely many preimages covering the domain, and push that finite selection back to the image.

Third, a compact subset C of a Hausdorff space Y is closed. For y∉C and each c∈C, choose disjoint open neighborhoods U_c of c and V_c of y. Finitely many U_c cover C. Their corresponding finitely many V_c have an open intersection V containing y, disjoint from C. Thus every y∉C has a neighborhood outside C, so Y\C is open.

Now any closed A⊆X is compact, f(A) is compact, and therefore f(A) is closed in Y. The inverse map g=f⁻¹ exists by bijectivity. For each closed A⊆X, g⁻¹(A)=f(A) is closed, so g is continuous using the closed-set characterization of continuity. Both f and g are continuous; f is a homeomorphism. Notice why a bare continuous bijection was insufficient.

## 6. Annulus retracting onto a circle — complete construction

Let A={x∈R²:1≤||x||≤2}. Define H(x,t)=((1−t)+t/||x||)x for t∈[0,1]. The denominator never vanishes on A. All operations are continuous there. Its norm is (1−t)||x||+t, between 1 and 2, so H stays in A. At t=0 it is x; at t=1 it is x/||x|| on the unit circle. If ||x||=1, H(x,t)=x for every t. Thus this is a strong deformation retraction. A picture alone would not check these four conditions. It does not produce a homeomorphism: collapsing radial segments loses injectivity.

## 7. Boundary of boundary is zero — complete simplicial argument

For an oriented k-simplex [v₀,…,v_k], its boundary is the alternating sum of faces obtained by deleting one vertex. Applying boundary again deletes two different vertices. For every pair i<j, the same codimension-two face appears twice: delete i then the shifted position j−1, or delete j then i. The signs are (−1)^(i+j−1) and (−1)^(i+j), which cancel. Every term belongs to one such pair, so ∂²=0. Extend linearly to all chains. Over F₂, signs disappear but two equal terms sum to zero. For k=1 the next boundary is ∂₀=0 under ordinary homology; k=0 also gives zero. This proves im ∂_(k+1)⊆ker ∂_k and makes the quotient H_k legitimate.

## 8. Betti formula and Euler–Poincaré — complete finite-dimensional derivation

For a finite chain complex over a field, rank–nullity gives dim ker ∂_k = dim C_k − rank ∂_k. Since boundaries form a subspace of cycles, dim H_k = dim ker ∂_k − dim im ∂_(k+1). Combining yields the formula used in the code.

Write c_k=dim C_k, b_k=dim H_k, r_k=rank ∂_k. Then c_k=b_k+r_k+r_(k+1). In the alternating finite sum Σ(−1)^k c_k, the r_k terms cancel adjacent r_(k+1) terms. The endpoint ranks vanish because there are no chains beyond the finite endpoints. Therefore Σ(−1)^k c_k=Σ(−1)^k b_k. This identity is a useful implementation invariant, not proof that two complexes sharing Euler characteristic are equivalent.

## 9. A square's Rips barcode in dimension one — complete small example

Use four unit-square corners with Euclidean distance and edge-distance threshold ε. Before ε=1, only vertices exist. From 1 inclusive to √2 exclusive, the four sides form one cycle and there are no triangles. Its edge boundary has rank three, so β₁=4−3=1. At √2, both diagonals enter; every vertex set becomes a simplex in the full Rips complex. It is a filled tetrahedron, so H₁ is zero. Including triangles already suffices to kill H₁; the three-simplex is needed for correct higher-dimensional conclusions. Thus the sole positive-length H₁ interval is [1,√2). Vertex labels or display layout do not alter the distances.

## 10. Distance to the persistence diagonal — complete calculation

For birth≤death, a diagonal point is (t,t). Its L∞ distance to (birth,death) is max(|birth−t|,|death−t|). By the triangle inequality, death−birth≤|death−t|+|t−birth|≤2 times that maximum. Every match costs at least (death−birth)/2. Choosing t=(birth+death)/2 attains the lower bound. This is the diagonal-matching cost used by the finite bottleneck implementation. It is not the Euclidean diagonal distance, which would use a different norm.

## 11. Why a uniform perturbation gives shifted inclusions — complete first step

Let f,g:X→R satisfy |f(x)−g(x)|≤δ for all x. If x lies in {f≤a}, then g(x)≤f(x)+δ≤a+δ. Hence {f≤a}⊆{g≤a+δ}. Exchanging f and g gives the reverse shifted inclusion. Applying homology gives compatible shifted maps between persistence modules. The full passage from this interleaving to a bottleneck bound uses additional algebraic results; the inclusion argument alone is not a complete proof of diagram stability.

For our executed image experiment, the domain is one fixed finite grid, with the same cell/subdivision rules and coefficient field. Every top-cell value changes by at most δ; a shared face's minimum incident value also changes by at most δ. The hypotheses therefore transfer to the finite simplicial filtrations we actually compute. Different resampling, masks, image dimensions, or point-cloud metrics require a new argument.

## 12. Major theorems: exact learning obligations, not hidden claims of full proofs

**Finite persistence decomposition.** A finite sequence of finite-dimensional vector spaces over a field with linear maps decomposes as a direct sum of interval representations. Its multiset of intervals is unique up to order. You must define an interval representation, work a finite example, explain why maps matter, and outline compatible-basis construction. The general existence/uniqueness proof is assigned to the formal course notes; the small reduction lab illustrates it but does not replace that proof. Extending a finite sequence constantly or by zero changes the interpretation of terminal bars.

**Sublevel-set stability.** For an appropriate tame setting (in particular finite, compatible piecewise-linear filtrations on one fixed finite complex), the bottleneck distance between same-degree diagrams of f and g is at most ||f−g||∞. Compare essential classes consistently. We execute a finite H₁ check; our finite-only matching routine is not an implementation for arbitrary infinite bars. You must state the domain, tameness/finite assumptions, homology field and dimension, diagram convention, and the role of interleavings. Full algebraic stability is assigned to ETH and the TDA survey.

**Nerve theorem, safe version.** For a finite good open cover of a suitable space, such as a finite open cover of a paracompact Hausdorff space with every nonempty finite intersection contractible, the nerve has the homotopy type of the union. You must define the nerve and a good cover, check common intersections rather than pairwise overlap, and recognize that closed-ball variants need their applicable version of the theorem. Euclidean Čech constructions have standard convex-cover versions; do not infer them from an unqualified slogan about arbitrary covers. Full construction of the homotopy equivalence is a deeper reading assignment.

**Homotopy invariance.** Homotopic maps induce the same map on homology, and homotopy-equivalent spaces have isomorphic homology. The bridge is a chain homotopy, not equality of coordinate arrays. Read the prism-operator argument in the algebraic-topology reference, state ∂P+P∂=g#−f#, and explain how it implies equality on homology. Constructing that operator is an extension after the core boundary proofs.

## 13. Where to go deeper without breaking the foundation

After mastery of the core, study integer coefficients and torsion; the cellular chain complex; fundamental groups and covering spaces; homology/cohomology duality; geometric inference under sampling assumptions; statistical inference for persistence; and only then multiparameter persistence or learned topological representations. These are substantive extensions. A short archive should not certify them after a vocabulary paragraph. Use [DEEPENING_PROOFS.md](DEEPENING_PROOFS.md) and the actual-book audit to record unfinished obligations rather than concealing them.
