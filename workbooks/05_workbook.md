# Stage 05 workbook — Build a shape from pieces before counting it

## What a simplex is

A vertex is a zero-dimensional simplex, an edge is one-dimensional, a filled triangle is two-dimensional, and a filled tetrahedron is three-dimensional. In a geometric realization, the vertices defining a simplex are affinely independent. Abstractly, a simplex is a finite set of vertex labels, and a complex is a collection closed under taking faces.

An abstract complex records which pieces are present without requiring a particular drawing. Its geometric realization can require more ambient dimensions than the original measurement plot. For example, a complete graph on the corners of a planar square induces higher Rips simplices; drawing every straight-line simplex over the square does not automatically produce a valid nonoverlapping geometric realization in that plane.

This distinction prevents a common inference error: the point coordinates define distances and a proximity complex, but the abstract complex is not simply the ink visible in one projection.

## Enumerate a triangle carefully

The filled triangle on vertices {0,1,2} has three vertices, three edges, and one face: seven stored nonempty simplices. The outline has the same vertices and edges but no two-dimensional face. Both can contain a triangular-looking drawing, yet their homology will differ.

The filled tetrahedron has four vertices, six edges, four triangular faces, and one three-dimensional simplex. Its boundary omits only that final solid simplex. The boundary is a sphere-like surface; the filled object is contractible. The difference is not captured by seeing that both have triangular faces.

The face validator deliberately rejects a triangle whose required edges or vertices are absent. A closure function, in contrast, deliberately adds missing faces. Use the right operation: validation should not quietly repair a malformed input when you are trying to catch a pipeline bug.

## Euler characteristic as a first summary

Compute χ=V−E+F−T+… . The triangle outline gives 3−3=0; the filled triangle gives 3−3+1=1. The tetrahedron boundary gives 4−6+4=2; the solid gives 4−6+4−1=1.

These values summarize the complex but do not completely classify every space. Even Betti numbers will be incomplete invariants. A single matching integer is weaker still. In the homology stage we prove why the alternating simplex count equals the alternating Betti-number count for finite complexes over a field.

## Surfaces and the meaning of a boundary

A surface locally resembles a plane, or a half-plane near a boundary point when surfaces with boundary are allowed. A sphere and torus surface are closed surfaces without boundary. A cylinder surface and a Möbius strip have boundary. “Closed” in the phrase closed surface conventionally means compact without boundary; it is not merely a synonym for any closed subset of ambient space.

Orientability asks whether local orientation choices can be made consistently across the surface. The Möbius strip gives a standard nonorientable example. A global classification of compact connected surfaces requires careful hypotheses, not just drawing a few familiar objects. The core course introduces those distinctions; the full classification proof is an explicit deeper assignment.

Keep a torus surface separate from a solid torus. The surface supports two independent first-homology directions, while the solid torus has the homotopy type of a circle. “One donut hole” is too ambiguous to define the homology groups.

## Real images are also modeling choices

The executable image model treats each pixel as a closed square cell. Two filled pixels meeting only at a corner are therefore connected. Other digital-image conventions may use four-neighbor adjacency or treat pixels as vertex samples. Those choices can give different components and holes.

We split each square into two triangles. Each enters at the square's entrance value. Shared edges and vertices receive the earliest value of incident triangles. At any threshold the triangulated object is the same union of closed squares, expressed with simplicial pieces. This is a filtration-preserving subdivision, not a method for recovering a physical three-dimensional surface from an image.

The Stage 05 practice constructs this object for a real training digit and verifies its face closure. Identify the input image, threshold, foreground convention, and connectivity model before explaining the output.

**Before advancing:** construct the outline and filled triangle from memory, state what changes, and explain why a graph's cycles do not automatically describe the homology of its clique complex. Sources R1, R2, R7, and L3 provide the formal context and image-model comparison.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/05_lesson.md) · [Worked lab](../notebooks/05_lab.ipynb) · [Your coding notebook](../practice/learner/05_practice.ipynb) · [Reference coding solutions](../practice/05_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
