# Stage 04 workbook — Algebra from doing one movement after another

## A group starts with operations you can compose

Rotate a square by a quarter-turn and then by another quarter-turn. The result is a half-turn. A full turn acts like doing nothing. A clockwise quarter-turn undoes a counterclockwise quarter-turn. These operations motivate identity, composition, and inverses.

A group requires closure under the operation, associativity, an identity, and an inverse for every element. Commutativity is not required. For a square's rotations and reflections, the order can matter. The permutation exercise represents a transformation by where it sends the four vertex labels; p after q is encoded by p[q[i]]. Reversing the convention without saying so changes the calculation.

An action connects an abstract group to a space or a set of data objects. Applying four quarter-turns to an image restores the array exactly. This is an action of the cyclic group of order four. It does not prove that rotating a handwritten digit preserves its label. Task meaning and transformation algebra are separate.

## A path is not just a drawn line

A path is a continuous map γ:[0,1]→X. Different parameterizations can trace the same visible route at different speeds. A loop begins and ends at the same point. To compare based loops, hold their basepoint fixed while deforming one continuously into another.

A homotopy between maps f,g:X→Y is a continuous H:X×[0,1]→Y with H(x,0)=f(x) and H(x,1)=g(x). The extra parameter describes the deformation, not necessarily physical clock time.

For based loops, concatenation traverses the first loop and then the second. The reverse path provides an inverse after passing to based homotopy classes; the constant loop provides the identity. Concatenation of parameterized paths is not literally the same function under every parenthesization, but the appropriate homotopies establish associativity of the classes. This is why the quotient step matters in the fundamental group.

## Homeomorphism is stronger than homotopy equivalence

A homeomorphism is an invertible continuous map with continuous inverse. A homotopy equivalence allows the inverse composites to be homotopic to the identity rather than exactly equal.

Consider the closed annulus A={x in ℝ²:1≤||x||≤2}. Let H(x,t)=((1−t)+t/||x||)x. Its radius is `(1−t)||x||+t`, which remains in [1,2]. At t=0 it returns x; at t=1 it reaches the unit circle. Points already on the unit circle remain fixed. The formula is continuous on this domain because ||x|| is never zero. Thus it gives a deformation retraction to the circle.

The annulus and circle have the same homotopy type, but they are not homeomorphic. The retraction collapses radial information; it is not a bijection. The numerical tests illustrate the endpoints and fixed-circle condition, while the formula and domain argument justify the continuous deformation.

## Loop order carries information

In a formal free-group word model, a and b represent two generators, and A and B their inverses. Adjacent inverse pairs cancel: `abBA` reduces to the empty word. The word `abAB` does not cancel by those rules. The corresponding commutator is nontrivial in a free group, illustrating information that a simple count of two loop directions misses.

This is a model to study, not an algorithm for recognizing the fundamental group of an arbitrary point cloud. Establishing π₁ of a space requires mathematical arguments about its loops and homotopies. For the circle, a full proof of π₁(S¹)≅ℤ uses a rigorous winding or lifting argument; the broader reading guide identifies that deeper assignment.

## What the real image experiment means

Run the exact quarter-turn action on one training image. Compare restored arrays after four turns and after composition of two turns. Then state what was verified: arithmetic and array-transformation identities. Do not state that a biological motion or a digit label is invariant unless the application supports that claim.

When considering rotations of sports motion data, distinguish camera-coordinate changes from changes in the physical movement or its outcome. A mathematically available symmetry is not automatically an appropriate nuisance transformation to remove.

**Before advancing:** explain the four group axioms, demonstrate noncommuting transformations, and verify the annulus formula by hand. Sources R1, R6, and R7 supply the deeper algebra and topology; this course's code illustrates only the explicitly stated finite and geometric examples.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/04_lesson.md) · [Worked lab](../notebooks/04_lab.ipynb) · [Your coding notebook](../practice/learner/04_practice.ipynb) · [Reference coding solutions](../practice/04_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
