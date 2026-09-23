# Stage 03 workbook — Continuity, equivalence, and the danger of a good-looking plot

## Continuity is a condition on a map between spaces

For f:X→Y, the topological definition requires f⁻¹(V) to be open in X whenever V is open in Y. The topology of both spaces matters. Continuity is not merely a visual property of a curve drawn by a plotting library.

In metric spaces, the ε–δ definition says that outputs can be kept within any requested tolerance by keeping inputs sufficiently close to their center. This formulation and the inverse-image definition agree for metric topologies. Foundation C gives a simple ε–δ proof for multiplication by two. Here we use the open-set form because it generalizes to nonmetric spaces.

## A finite counterexample you can check completely

Take the same underlying set {0,1} twice. Give X the discrete topology containing every subset and Y the indiscrete topology containing only ∅ and {0,1}. The identity map X→Y is continuous: it has only two codomain open sets to pull back, and both inverse images are open in X.

The inverse identity Y→X is not continuous. The codomain open set {0} pulls back to {0}, which is not open in Y. Thus a continuous bijection need not be a homeomorphism. A homeomorphism requires a continuous inverse as well.

The practice notebook tests every open set in this finite example, so the computation exhausts that example's continuity question. It does not prove an arbitrary infinite-space continuity claim.

## Connectedness and paths

A space is connected when it cannot be separated into two disjoint nonempty open subsets whose union is the space. A path from x to y is a continuous map from [0,1] into the space with those endpoints. Path-connectedness requires such a path for every pair. A path-connected space is connected, but the converse can fail in general.

For the finite simplicial complexes and geometric graphs in the executable core, components can be investigated by their adjacency. Do not generalize every graph-search shortcut to arbitrary topological spaces.

A continuous image of a connected space is connected. To prove this, suppose its image had a separation. Pull the two pieces back under the continuous map. The inverse images are disjoint, open, nonempty, and cover the domain, contradicting connectedness. Each adjective matters: nonemptiness follows because the pieces were in the image.

## Compactness is an open-cover property

A space is compact when every open cover has a finite subcover. In Euclidean space, closed and bounded sets are compact; that characterization is not the definition for every topological space. A finite space is compact because, from any cover, one may select an open set for each of its finitely many points.

A continuous image of a compact space is compact: pull an open cover of the image back to the domain, choose a finite subcover there, and push the chosen cover members back into the argument. A Hausdorff space permits any two distinct points to have disjoint neighborhoods. Compact subsets of a Hausdorff space are closed.

Those facts establish an important shortcut: a continuous bijection from a compact space to a Hausdorff space is a homeomorphism. A closed subset of the compact domain is compact; its image is compact and therefore closed in the Hausdorff codomain. The map is closed, making its inverse continuous. The proof atlas supplies the steps in more detail.

## Why projection is not harmless

Projecting `(x,y,z)` to `(x,y)` is continuous. It is not injective: `(0,0,0)` and `(0,0,5)` have the same image. Their original distance is five and their projected distance is zero. A continuity claim alone therefore cannot justify transferring every visible structure in a two-dimensional display back to the original data.

The real-data exercise measures this effect for selected Iris rows. Coordinate projection cannot increase Euclidean pairwise distance because it removes nonnegative squared terms. Yet it can collapse distinctions relevant to a classifier or neighborhood graph.

## What you should produce

Draw the two finite topologies, run the continuity checks, and explain the asymmetry. Prove that a composition of continuous maps is continuous by composing inverse images. Then write one paragraph explaining why the graph-component count in the lab is a property of the constructed threshold graph rather than a count of species.

**Depth boundary:** understanding the proof of compact-to-Hausdorff is required here; mastering all compactness theorems of general topology is a later extension. Sources R1–R3 provide the formal reading route.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/03_lesson.md) · [Worked lab](../notebooks/03_lab.ipynb) · [Your coding notebook](../practice/learner/03_practice.ipynb) · [Reference coding solutions](../practice/03_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
