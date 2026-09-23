# Stage 07 workbook — Choose a construction, then vary its scale

## Data do not come with a unique complex

Begin with a point cloud and a declared distance. At threshold ε, connect points at distance at most ε. This gives a graph. In a Vietoris–Rips complex, add every simplex whose vertices are pairwise connected. The entrance value of a simplex is its diameter, the maximum pairwise vertex distance.

A face is a subset of its coface, so its diameter cannot be larger. Thus faces enter no later than cofaces, creating a filtration: K_a⊆K_b for a≤b. This nesting is a mathematical property to verify, not simply a sequence of datasets with increasing filenames.

## A graph triangle is not automatically a hole

At a threshold where three vertices are pairwise adjacent, the Rips triangle is filled. Its three-edge cycle is therefore a boundary. A graph-only cycle-counting routine would count a cycle that is already trivial in the clique complex. To determine H₁ deaths, include two-dimensional simplices. More generally, Hₖ can be killed by (k+1)-simplices.

The educational enumerator builds through the next dimension and limits candidate counts. For n points, triangle candidates already grow as n choose 3. A small notebook demonstration is not a scalable production engine. Use a specialized library for large clouds after the correctness conventions are aligned.

## Cech asks for a common intersection

For our geometric comparison, use closed Euclidean balls of radius r. A Cech simplex exists when all balls indexed by its vertices have a common point. Pairwise overlap alone does not guarantee that.

Place three points at an equilateral triangle's vertices with side length one. Balls of radius 1/2 meet pairwise but have no common triple intersection. A triple intersection first appears at radius 1/√3, the circumradius. Rips at edge threshold one already fills the triangle because every pair of vertices is joined.

Notice the two parameters: ball radius and edge length. Since two radius-r balls can meet when their centers are up to 2r apart, comparing the same numeral in a Cech radius and a Rips edge threshold is generally not a fair same-scale comparison.

## What a nerve theorem actually contributes

The nerve records nonempty intersections of subfamilies of a cover. Suitable nerve theorems give a homotopy equivalence between the union and the nerve under stated intersection and cover hypotheses. A finite family of compact convex Euclidean sets is a standard setting: every nonempty intersection is convex and therefore contractible.

This does not prove that the union of balls reconstructs an unknown underlying physical object. That extra inference requires sampling, scale, and geometric assumptions. The theorem connects two specified mathematical constructions; it does not make an arbitrary biological interpretation true.

## Alpha complexes use geometry to reduce the representation

Delaunay/alpha constructions provide a Euclidean geometric route related to unions of balls. Their inclusion and parameter definitions differ from simply filling every pairwise clique. The supplied GUDHI alpha script is optional, because that library was unavailable in the build environment.

GUDHI's default alpha values are squared-radius values. Taking a square root can put them into radius units, but this does not magically make a Rips complex identical to an alpha complex. Align construction, field, threshold range, and units before comparing results.

## Real-data work and the meaning of infinity

The Iris exercise deliberately uses twelve specified rows and cutoff 0.5 in the selected feature units. It reports the number of vertices, edges, and triangles. It does not claim that those rows are a representative sample or that the cutoff is biologically optimal.

When a computation stops at a finite cutoff, an unpaired interval may only mean “still present when we stopped.” The algorithm has not observed its future. At the same time, a fully constructed finite Rips filtration at all pairwise distances has a complete simplex structure in the relevant dimensions. State which computation you actually performed.

## Different kinds of filtration parameter

An entrance parameter can be distance, intensity, height, confidence, or chronological time. A time sequence that both adds and removes simplices is not an ordinary nested filtration. Zigzag methods address a different diagram of maps; relabeling a non-nested sequence as ordinary persistence is not a solution.

**Before advancing:** derive the square and equilateral-triangle events, verify face monotonicity, and state the exact parameter convention for your real example. Sources R1, R2, R8, L1, and L2 support these distinctions.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/07_lesson.md) · [Worked lab](../notebooks/07_lab.ipynb) · [Your coding notebook](../practice/learner/07_practice.ipynb) · [Reference coding solutions](../practice/07_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
