# Glossary and notation

**Observation.** One item being measured; its definition can change between a point-cloud and a pixel analysis.

**Feature.** A measured or constructed value describing an observation.

**Metric.** A nonnegative, symmetric distance with identity of indiscernibles and the triangle inequality.

**Pseudometric.** A metric-like distance allowing distinct objects to have zero distance.

**Open ball.** Points whose distance from a center is strictly less than a positive radius.

**Topology.** A collection of open sets containing empty and whole sets and closed under arbitrary unions and finite intersections.

**Basis.** Open sets whose unions generate the topology; separately, in linear algebra, an independent spanning collection.

**Subspace topology.** Open sets formed by intersecting ambient open sets with the subset.

**Continuous map.** A function for which inverse images of open sets are open.

**Homeomorphism.** A bijective continuous map with continuous inverse.

**Connected.** Cannot be separated into two disjoint nonempty open parts.

**Path-connected.** Every pair of points can be joined by a continuous interval-valued path into the space.

**Compact.** Every open cover has a finite subcover.

**Hausdorff.** Distinct points have disjoint open neighborhoods.

**Group.** An associative operation with closure, identity and inverses.

**Group action.** A compatible way for group elements to transform another set.

**Homotopy.** A continuous family of maps parameterized by an interval, with specified endpoint maps.

**Homotopy equivalence.** Maps in both directions whose compositions are homotopic to identity maps.

**Deformation retraction.** A homotopy moving a space onto a subspace while fixing that subspace throughout.

**Fundamental group.** Based-loop homotopy classes under concatenation.

**Surface.** A locally two-dimensional manifold, with the declared boundary/separation/countability conditions.

**Orientability.** The ability to make local orientation choices consistently across a manifold.

**Simplex.** A vertex subset, geometrically realized as a filled vertex/edge/triangle/tetrahedron or higher analogue.

**Simplicial complex.** A collection of simplices closed under faces.

**Chain.** A formal linear combination of simplices of one dimension over specified coefficients.

**Boundary map.** The linear operator sending a simplex to its oriented or F₂ codimension-one faces.

**Cycle.** A chain whose boundary is zero.

**Boundary.** A chain in the image of the next-dimensional boundary map.

**Homology.** Cycles modulo boundaries, Hₖ=ker∂ₖ/im∂ₖ₊₁.

**Betti number.** Dimension of a homology vector space over a stated field.

**Euler characteristic.** Alternating finite cell/simplex count; equals the alternating Betti sum in the finite setting.

**Filtration.** A nested family of spaces/complexes indexed by an ordered parameter.

**Rips complex.** A simplex enters when all pairwise vertex distances meet the declared threshold.

**Čech complex.** A simplex records a common intersection of balls under the declared radius convention.

**Alpha complex.** A Delaunay/Voronoi-based construction related to unions of Euclidean balls; verify its filtration units.

**Nerve.** A complex recording nonempty common intersections of members of a cover.

**Persistence module.** Vector spaces with compatible linear maps indexed by the filtration parameter.

**Barcode.** A multiset of persistence intervals, not a unique list of physical object tracks.

**Persistence diagram.** A multiset of birth/death pairs, with explicit handling of essential intervals and the diagonal.

**Essential interval.** An interval not dying in the declared complete filtration; distinguish from survival of a computational cutoff.

**Bottleneck distance.** The minimum largest matching cost between diagrams, with diagonal matches and a stated norm.

**Stability.** Controlled change in a descriptor under a specified class of input perturbations and assumptions.

**Persistence landscape.** Ordered tent-height functions derived from finite persistence intervals.

**Persistence image.** Integrated weighted kernels over a fixed grid in transformed diagram coordinates.

**Mapper.** A cover-and-cluster construction linking nodes that share observations; a displayed graph may be only its 1-skeleton.

**Reeb graph.** Quotient identifying points within connected components of level sets of a function.

**Leakage.** Use of information unavailable in the intended prediction/evaluation setting.

**Holdout exposure.** Having viewed or used final-test results or examples in method design; it limits future independence claims.

## Reading symbols

`∈` belongs to; `⊆` is a subset of; `∩` intersection; `∪` union; `∅` empty set; `∀` for every; `∃` there exists; `→` maps to; `ker` kernel; `im` image; `dim` dimension; `∂` boundary; `β` Betti number; `F₂` two-element field; `[b,d)` includes b but excludes d. The notation `f⁻¹(A)` can mean an inverse image even when no inverse function exists.
