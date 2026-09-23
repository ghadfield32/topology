# Stage 03 — Continuity, homeomorphisms, connectedness, and compactness

**Starting point:** Complete the Stage 02 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Continuity is about the relationship between neighborhoods
A map f:X→Y is **continuous** when the inverse image of every open subset of Y is open in X. This general definition does not require distances. For metric spaces it agrees with the familiar epsilon–delta formulation: near each input x, sufficiently small input changes keep the output within any requested positive tolerance of f(x).

The order of the quantifiers matters. The output tolerance is requested first, then an input tolerance must be supplied; it may depend on x. Uniform continuity asks for one input tolerance that works everywhere for each requested output tolerance. We introduce it here to avoid confusing pointwise control with global control.

For f(x)=3x+2 on R, `|f(x)-f(y)|=3|x-y|`. Given an output tolerance ε, choosing δ=ε/3 works at every x. For the general topological proof that compositions preserve continuity, use `(g∘f)⁻¹(U)=f⁻¹(g⁻¹(U))`: first g gives an open inverse image, then f does.

## 2. Invertibility is not enough for topological equivalence
A **homeomorphism** is a bijection that is continuous in both directions. It identifies spaces with the same topological structure. It need not preserve distances, angles or area. The map f:(0,1)→(2,5), f(x)=3x+2, is a homeomorphism with inverse (y−2)/3.

A continuous bijection need not have a continuous inverse. A tiny example avoids difficult calculus: put the discrete topology on {a,b} as the domain and the indiscrete topology on the same set as codomain. The identity function is bijective and continuous in the forward direction. Its inverse is not continuous because a singleton open in the discrete target has a singleton inverse image that is not open in the indiscrete source.

Our finite-topology code checks this example exhaustively. This example is not a claim that all finite spaces are discrete. Only finite subspaces of metric spaces with distinct points were shown discrete in Stage 02; arbitrary topological spaces need not be metrizable.

## 3. Connectedness and paths
A space is **connected** when it cannot be split into two nonempty disjoint open subsets whose union is the whole space. A **path** from x to y is a continuous map from [0,1] to the space with endpoints x and y. A space is **path-connected** when every pair can be joined by such a path.

Path-connected implies connected, but the converse is false for general spaces. For finite simplicial complexes the component picture is especially concrete: connectedness and path-connectedness agree, and components can be found by the edge graph. This useful computational fact must not be promoted to a theorem about every possible topological space.

The continuous image of a connected space is connected. To see why, suppose the image had a separation into two disjoint nonempty relatively open sets. Their inverse images would separate the original space. That contradicts connectedness.

## 4. Compactness is not merely “small”
A space is **compact** if every open cover admits a finite subcover. A cover is a collection whose union contains the space. Compactness does not mean a set has finitely many points. The closed interval [0,1] is compact in the usual topology. The open interval (0,1) is not: the sets `(1/n,1)` for n≥2 cover it, but a finite selection misses points sufficiently near zero.

In Euclidean space, compactness is equivalent to being closed and bounded. That equivalence has hypotheses: it is not a definition valid for every metric space. A **Hausdorff** space allows any two distinct points to be separated by disjoint open neighborhoods. Metric spaces are Hausdorff: sufficiently small balls around two distinct points are disjoint.

A continuous map sends compact spaces to compact spaces because inverse images turn an open cover of the image into one of the domain. A compact subset of a Hausdorff space is closed. Combining these facts gives an important theorem: a continuous bijection from a compact space to a Hausdorff space is a homeomorphism. Indeed, images of closed sets in the compact domain are compact and hence closed in the target. Thus the inverse is continuous.

To deepen the last argument, prove the supporting facts: closed subsets of compact spaces are compact by adding their open complement to a cover; compact subsets of Hausdorff spaces are closed by separating an outside point from each point of the compact subset and extracting finitely many neighborhoods.

## 5. The real-data bridge: transformations versus projections
On Iris measurements, translation is an invertible continuous map of the ambient Euclidean space and preserves distances. An invertible diagonal rescaling is also a homeomorphism of the ambient space but usually changes distances. Projection from four coordinates to two is continuous but is not an invertible map of R⁴ onto R².

The notebook checks distances before and after a translation, compares rescaling, and displays a two-feature projection. These computations illustrate algebraic facts about our particular data. They do not prove continuity on an infinite domain. Moreover, every function from a finite discrete sample is continuous, so using only those samples to certify a meaningful ambient continuity claim would be vacuous.

Use a plot to suggest a question, then use a definition or theorem to answer it. When a projection appears to join two groups, investigate whether the lost coordinates distinguish them rather than declaring that the original geometry changed.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**03.1.** Prove the composition of two continuous functions is continuous.

**03.2.** Give a homeomorphism from (0,2) to (5,9) and its inverse.

**03.3.** Explain the continuous-bijection counterexample using two finite topologies.

**03.4.** Why does a path-connected space have to be connected?

**03.5.** Use the given cover to show (0,1) is not compact.

**03.6.** Explain where compactness and the Hausdorff assumption enter the homeomorphism theorem.

**03.7.** Is projection R⁴→R² a homeomorphism? Could its restriction to a particular finite sample be bijective?

**03.8.** Why can finitely many plotted points not establish continuity of a function on all of R?

## Mastery gate

Give correct map definitions and prove the basic continuity and compactness consequences with their hypotheses.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R2, R3. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/03_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/03_solutions.md`, record what was independent, and continue only when the gate is met.
