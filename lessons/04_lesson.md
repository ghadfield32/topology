# Stage 04 — Groups, symmetries, paths, loops, and homotopy

**Starting point:** Complete the Stage 03 mastery gate first, or use its worked solutions to close a specific gap.

**Learning cycle:** understand → define → work by hand → predict → run → critique → retrieve later.

## 1. Combining operations
A **group** is a set with an operation satisfying closure, associativity, an identity, and inverses. Associativity says `(ab)c=a(bc)`, not `ab=ba`. A group is abelian when the latter commutativity property also holds.

The integers under addition form a group. Positive integers under addition do not: there is no additive identity inside the set and no additive inverses. A square's symmetries form another group under composition. Rotating by a quarter-turn four times restores the square; reflecting twice restores it. A rotation followed by a reflection need not equal the reverse order.

A **group action** describes how a group operates on another set. The identity must leave every object unchanged, and composing group elements must agree with successive actions. A **homomorphism** preserves the group operation. Its kernel contains elements mapped to the identity; this resembles the zero-output kernel of a linear map, but the identity need not be written zero.

In the notebook, quarter-turns and reflections act on the array positions of a real digit image. These are exact pixel permutations, so composition can be checked without interpolation. They preserve the multiset of intensities, but they need not preserve the semantic digit label. A rotated 6 is a reminder that mathematical symmetry and task invariance are different requirements.

## 2. Deforming maps, not tearing spaces
A **homotopy** between maps f,g:X→Y is a continuous map H:X×[0,1]→Y with H(x,0)=f(x) and H(x,1)=g(x). The extra parameter is the deformation stage. It must be continuous jointly, not merely a set of unrelated pictures.

A disk contracts to its center by H(x,t)=(1−t)x. A **contractible** space has its identity map homotopic to a constant map. A **deformation retraction** moves a space onto a subspace while fixing every point of that subspace throughout the deformation.

Take the closed annulus A={x in R²: 1≤||x||≤2}. Define `H(x,t)=((1−t)+t/||x||)x`. Its radius is `(1−t)||x||+t`, which stays between one and two. At t=0 it is x; at t=1 it lies on the unit circle; points already on the unit circle stay fixed. Division is safe because the annulus excludes the origin. This is a deformation retraction onto the circle.

Two spaces are **homotopy equivalent** if there are maps in both directions whose compositions are homotopic to the respective identity maps. The maps need not be inverse bijections. The annulus and circle are homotopy equivalent but not homeomorphic. Homotopy equivalence preserves less information than homeomorphism, which is precisely why some calculations become easier.

## 3. Loops become an algebraic object
A **based loop** starts and ends at a specified basepoint. We can traverse one loop and then another. Raw concatenation has timing choices, so the group is defined on suitable homotopy classes of based loops, not on unprocessed parametrized curves.

The **fundamental group** π₁(X,x₀) consists of these classes. The constant loop gives the identity; reversing a loop gives its inverse. A space is **simply connected** when it is path-connected and every loop can contract, equivalently its fundamental group is trivial.

For the circle, based loops have an integer winding number. One counterclockwise turn represents +1, one clockwise turn −1, and going around twice +2. The fundamental group is isomorphic to the integers under addition. The disk has trivial fundamental group. The nontrivial circle result needs an argument, such as a lifting or winding-number proof; counting turns in a sampled animation alone is not that proof. Hatcher's introductory fundamental-group material supplies the deeper treatment.

A torus surface has two independent directions for loops, unlike the loose “one hole” language often used for a doughnut. Its first homology over a field has dimension two. A solid torus is a different object and has the homotopy type of a circle. Always declare whether you mean a surface or a filled solid.

## 4. From loops to homology
Homology will be easier to compute than the fundamental group, but it can lose information. In the figure-eight graph, traversing loop a then loop b differs in the fundamental group from traversing b then a. First homology records the abelianized information: the totals along the independent loops. This motivates why a numerical invariant can be useful without completely describing a space.

Do not infer “same shape” from equal values of a single invariant. If an invariant differs, it can disprove a proposed equivalence. If it agrees, other differences may remain. We will repeatedly use this one-way logic.

## 5. What to do in the lab
Verify the square-symmetry identities on an asymmetric training image. Numerically check the annulus deformation at a grid of times and display two stages. State which facts were proved algebraically in the lesson and which were merely sampled by the program. The real image teaches group actions; the synthetic annulus teaches homotopy. Neither is a reconstruction algorithm for an arbitrary camera scene.

## Independent exercises

Do these before reading the worked solutions. A copied solution is not an independent pass.

**04.1.** List the four group axioms and explain why associativity does not imply commutativity.

**04.2.** For a square, give the inverse of a quarter-turn and the inverse of a reflection.

**04.3.** Check the endpoints and fixed-subspace condition of the annulus deformation formula.

**04.4.** Why is the same formula invalid at the center of a disk?

**04.5.** Explain homeomorphism versus homotopy equivalence using the annulus and circle.

**04.6.** What are the winding numbers of two forward turns followed by one reverse turn?

**04.7.** Why does rotating a digit image not automatically produce a valid same-label training example?

**04.8.** What can and cannot be concluded when two spaces have equal Betti numbers?

## Mastery gate

Explain and check a group action, verify a deformation retraction, and distinguish loop classes from raw paths.

Explain one limitation and solve a new variant after a delay. Suggested progression threshold: 85% on the local knowledge check, with every critical error corrected. This is a course rubric, not accreditation.

## Free readings and attribution

Source IDs: R1, R6, R7. See `docs/SOURCES.md` for direct official links and assigned topics. The exposition, examples, code, and solutions here are original course material, not copied textbook chapters.

## Run and continue

Open `notebooks/04_lab.ipynb`. Its saved outputs are also readable from the browser reader. After the lab, compare with `solutions/04_solutions.md`, record what was independent, and continue only when the gate is met.
