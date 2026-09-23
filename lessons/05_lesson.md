# Stage 05 — Surfaces, simplices, triangulations, and pixel geometry

**Starting point:** Complete the Stage 04 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. A surface is locally two-dimensional
A topological **surface** is locally like an open subset of the plane, with the usual additional separation and countability conditions in the standard definition. A surface with boundary may also have neighborhoods modeled on a half-plane. A boundary is not simply the outline in a drawing: a sphere has no boundary as a surface, even though a projection has a visible outline.

A surface is **orientable** when local orientation choices can be made consistently across it. A Möbius strip obstructs such a global choice. An orientable closed connected surface's **genus** counts its handles. The classification theorem for compact connected surfaces is a substantial result; here we learn its statement and examples rather than pretending an animation proves it.

Under its hypotheses, a closed connected orientable surface of genus g has Euler characteristic 2−2g. A compact connected orientable surface with b boundary components has characteristic 2−2g−b. For the nonorientable connected-sum family with k projective-plane factors and b boundary components it is 2−k−b. These formulas concern different classes of spaces and cannot be used interchangeably without checking orientability and boundary.

The sphere is orientable, closed, and genus zero. The torus surface is orientable, closed, and genus one. A cylinder surface with two boundary circles is orientable. The Möbius strip has one boundary circle and is nonorientable. The Klein bottle is a closed nonorientable surface; a self-intersecting picture in R³ is not its intrinsic definition. Use Hatcher's geometric introduction and the surface discussion to deepen these examples.

## 2. Replace continuous shapes by compatible pieces
A **0-simplex** is a vertex, a **1-simplex** is an edge, a **2-simplex** is a filled triangle, and a **3-simplex** is a filled tetrahedron. A simplex's dimension is one less than its number of vertices. A face is formed by selecting some of its vertices.

An **abstract simplicial complex** is a collection of finite vertex subsets closed under taking faces. Our code stores nonempty simplices only; empty-face bookkeeping is implicit. A **geometric realization** draws compatible simplices in Euclidean space. In a geometric simplicial complex, intersections of simplices must be common faces rather than arbitrary crossings.

A triangulation represents a space as the realization of such a complex, up to homeomorphism. An abstract triangle is recorded as `(0,1,2)`, but those IDs do not by themselves specify physical coordinates. Coordinates can change while the combinatorial incidence information stays the same.

If we include triangle (0,1,2), we must also include its edges and vertices. Three edges around a triangle do not force its interior to exist in an arbitrary complex. In a **clique complex**, by contrast, every clique of the edge graph supplies a simplex by definition. This extra rule is what will distinguish a graph from its Rips complex.

## 3. Count pieces without mistaking the count for a full invariant
For a finite complex, the **Euler characteristic** is the alternating simplex count: vertices minus edges plus triangles minus tetrahedra, and so on. A triangle boundary has 3−3=0. A filled triangle has 3−3+1=1. The boundary of a tetrahedron has 4−6+4=2; including its solid interior gives 4−6+4−1=1.

Euler characteristic is invariant under suitable changes of triangulation of the same space, but the raw number of edges is not. Adding a vertex to subdivide an edge changes two counts that cancel in the alternating sum. A full proof of invariance follows from homology or subdivision theory, not from one successful count.

The Euler number does not reveal every Betti number separately. A connected graph with two loops has characteristic −1; a different complex can have the same alternating sum with other dimensions contributing. We will calculate the more informative homology groups next.

## 4. Pixels need a declared geometric model
An 8×8 intensity array is not automatically a continuous surface. In this course we model each pixel as a **closed square** in a rectangular grid. Selecting pixels at a threshold means taking the union of those closed squares. Squares touching at a corner are therefore connected. This convention is different from a rule that only allows edge-neighbor pixel connections.

We split each selected square into two triangles and include every face. The diagonal is an internal subdivision: both triangles and the diagonal enter at the same filtration value. Thus the union at each threshold is the same geometric pixel region, only triangulated. This allows our simplicial code to analyze the square-pixel model. It is not presented as a newly implemented general-purpose cubical library.

No periodic boundary is imposed and no padded exterior is added. All pixels eventually enter, giving a full rectangular region. If a dark central pixel enters after a ring around it, a loop can disappear then. Choosing opposite intensity conventions reverses the order, so the threshold definition must be explicit.

## 5. Work through a real image
The notebook loads a real **training** digit, thresholds it, constructs its complex, counts simplices, and reports Euler characteristic. It also runs exact triangle and tetrahedron examples. A written 8 does not guarantee two measured holes: handwriting, low resolution, intensity threshold, and corner-touch conventions all matter.

Inspect the complex validator. It rejects missing faces rather than silently inventing them. A separate closure function deliberately adds faces when that is the requested construction. These are different operations, and naming them separately makes the analysis auditable.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**05.1.** How many vertices, edges, and triangles occur in a filled triangle?

**05.2.** Calculate the Euler characteristics of a triangle boundary, filled triangle, tetrahedron boundary, and solid tetrahedron.

**05.3.** What is wrong with storing a triangle but omitting one edge?

**05.4.** Explain abstract simplex versus geometric realization.

**05.5.** Why do corner-touching foreground pixels connect under this course’s model?

**05.6.** Why can a digit label not be used as the exact ground-truth Betti number of its thresholded image?

**05.7.** For a torus with one open disk removed, calculate Euler characteristic using the surface formula.

**05.8.** Explain why a graph containing a triangle and its clique complex can have different topology.

## Mastery gate

Construct valid complexes, distinguish surfaces from solids, and state the exact pixel-connectivity convention.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R2, R7, L3. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/05_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/05_solutions.md`, record what was independent, and continue only when the gate is met.
