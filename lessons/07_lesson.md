# Stage 07 — From data to shape: Rips, Čech, alpha, and filtrations

**Starting point:** Complete the Stage 06 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. A point cloud does not dictate a unique complex
To analyze measurements, first choose what a point represents and what distance compares two points. Then choose how nearby points create edges, triangles and higher simplices. Different constructions can be reasonable for different questions. The resulting complex is part of the model, not something observed directly by the camera or measurement instrument.

A **filtration** is a nested family: when the parameter increases, previously included simplices remain included. For finite computations we can record each simplex with its first appearance value. A face must appear no later than a simplex containing it. Equal appearance times are allowed, but a valid reduction order must put faces before their cofaces.

The filtration parameter could be distance, intensity, density-derived value, or time in a suitable nested construction. A sequence of video frames with features appearing and disappearing is not automatically a filtration. Ordinary one-parameter persistence needs inclusions; methods such as zigzag persistence handle other kinds of changes but are outside the executable core.

## 2. Our Rips convention, stated exactly
The Vietoris–Rips complex at ε contains a finite vertex subset precisely when every pair in it is at distance at most ε. Equivalently, its diameter is at most ε. Vertices enter at zero; each higher simplex enters at the length of its longest edge. We call ε the **edge-distance parameter**, not a ball radius.

This is a clique complex. Once three vertices are pairwise joined, the triangular face is present; once four are pairwise joined, the tetrahedral simplex is present if we are building to that dimension. To compute H₁ we build through triangles. To compute H₂ we build through tetrahedra. Omitting such simplices can create artificial surviving classes.

Worked example: three points forming an equilateral triangle of side one. In our Rips convention all edges and the filled triangle enter together at ε=1. There is no positive-length H₁ interval. A sequential implementation might temporarily show a cycle between inserting edges and face at the same numerical value. Its zero-length interval is not a feature present over a nonzero scale range.

## 3. Čech: common intersections are stronger than pairwise ones
For equal-radius closed Euclidean balls of radius r around points, the Čech complex contains a simplex when the entire collection of balls has a common intersection. Pairwise overlap gives edges but need not give a higher-dimensional common intersection.

For the equilateral triangle of side one, pairs of balls first meet at r=1/2. All three first meet at the circumradius r=1/√3. Thus there is a scale range in which the Čech complex contains the three edges without the filled triangle. This is a useful contrast with Rips, not a contradiction: the construction and parameter convention differ.

In Euclidean space, with our conventions, `Čech_r ⊆ Rips_(2r) ⊆ Čech_(2r)`. The first inclusion follows because two centers sharing a point in their radius-r balls are at most 2r apart. For the second, choose one vertex of a Rips simplex; it is at most 2r from every center and lies in their radius-2r balls. Stronger dimension-dependent bounds exist, but these elementary inclusions already show why factors of two must be tracked.

The **nerve** of a cover records which subcollections have nonempty common intersections. A version of the nerve theorem says that a suitable finite good cover, whose nonempty finite intersections are contractible, has a nerve homotopy equivalent to its union. One standard setting uses open good covers; finite covers by closed convex subsets of Euclidean space also have a nerve result. Do not apply the theorem to arbitrary disconnected intersections merely because you have a graph of overlaps.

## 4. Alpha complexes and geometric efficiency
An alpha complex uses a Delaunay/Voronoi construction to represent unions of Euclidean balls more economically than a full Čech enumeration in favorable dimensions. Voronoi cells associate locations with nearest sites; their dual Delaunay structure records adjacency. Intersecting balls with appropriate Voronoi regions leads to the alpha construction.

Its exact filtration values and numerical handling require care. GUDHI's default alpha values are squared radii, not our Rips edge lengths. Comparing a number from one axis directly with the other would mix both units and constructions. The optional script provides an alpha demonstration when GUDHI is installed; this optional result is not claimed as executed in the shipped report.

The core notebook demonstrates the triangle's Čech scales analytically and computationally and constructs Rips filtrations with our explicit code. This is enough to learn the distinction without inventing an untested general-purpose alpha implementation.

## 5. Real-data construction and cost
We use a fixed small subset of Iris observations for the educational Rips builder. Its vertices are flower samples, not individual measurements. All selected feature columns enter Euclidean distance, and the report states their scale. Class labels are not included in the coordinates.

For n points, possible k-simplices number `choose(n,k+1)`. Even H₁ can require enumerating `choose(n,3)` triangles. The code deliberately caps candidate counts and asks for smaller samples or a specialized library rather than freezing a beginner's computer. Small samples are a teaching convenience; they do not establish topology of the full population.

At several thresholds, compare graph components and complex homology. Predict the expected nesting before execution. If a threshold removes an edge while claiming to increase the same filtration parameter, something in the construction or preprocessing has changed and must be investigated.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**07.1.** At what value does a Rips simplex enter under the declared convention?

**07.2.** Why does the equilateral triangle have no positive H₁ Rips bar?

**07.3.** Derive the two Čech radii for that same triangle.

**07.4.** Prove the elementary inclusions Čech_r⊆Rips_2r⊆Čech_2r in Euclidean space.

**07.5.** Explain the good-cover assumption in a nerve theorem.

**07.6.** How many candidate edges and triangles exist for 20 observations?

**07.7.** Why does reporting H₁ from an edge-only complex answer a different question?

**07.8.** If an alpha value is 4 in squared-radius units, what is the radius? Is this automatically Rips ε=2?

## Mastery gate

Specify and implement a valid filtration, distinguish Rips/Čech/alpha, and justify parameter units and dimension limits.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R2, R8, L1, L2. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/07_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/07_solutions.md`, record what was independent, and continue only when the gate is met.
