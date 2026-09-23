# Stage 01 workbook — The mathematical objects under the code

## Start from a function, not from a formula to memorize

A function assigns exactly one output to each input in its domain. For f(x)=x² on the real line, inputs −2 and 2 both produce 4. That does not make f invalid; functions need not be one-to-one. The function is onto the nonnegative reals but not onto the entire real line. The codomain is therefore part of its definition.

An inverse image works even when an inverse function does not. To find f⁻¹((1,4)), solve 1<x²<4. This means 1<|x|<2, giving two intervals: (−2,−1) and (1,2). The parentheses exclude endpoints because the target interval excludes 1 and 4. A finite-domain code version can check particular integers, but it is not an enumeration of these infinitely many real inputs.

## Work through logic one step at a time

Suppose a statement says every row has a finite value. Its negation is that at least one row has a nonfinite value. It is not that every row is nonfinite. A single offending row is enough to refute the first claim. Conversely, checking the 150 included rows establishes a statement about that finite file, not about every future dataset a function might receive.

To prove a subset claim, pick an arbitrary member of the first set and reason toward membership in the second. To prove equality, establish both inclusions. To prove a universal implication false, find one input satisfying its assumptions but failing its conclusion. These patterns recur in continuity proofs, filtration validation, and software tests.

## Quotients are controlled forgetting

Integers with the same remainder modulo three form equivalence classes. Reflexivity follows because x−x=0 is divisible by three. Symmetry follows because if x−y is divisible by three, so is its negative. Transitivity follows by adding x−y and y−z. The quotient treats all values in one class as the same new object.

Later, a cycle and that cycle plus a boundary will count as the same homology class. The quotient is not numerical division of a curve length by an area. It is an algebraic way to say which differences should be ignored while preserving meaningful operations.

## A matrix example you should calculate yourself

Let A=[[1,1],[0,0]]. An input `(x,y)` becomes `(x+y,0)`. Outputs occupy the horizontal line, so the image has dimension one. Inputs sent to zero satisfy x+y=0 and form the line `(t,−t)`, so the kernel also has dimension one. The two input dimensions equal rank one plus nullity one.

Now change the scalar arithmetic to F₂. Only zero and one remain, with 1+1=0. A matrix of zeroes and ones can have a different rank over this field than over the reals. In the practice notebook you inspect a three-by-three example of real rank three but F₂ rank two. You will later implement binary elimination rather than incorrectly using a real-valued rank function.

A chain basis is a list of simplices, not a list of spatial coordinate axes. When a triangle has three edges, its edge-chain space has dimension three even though the drawn triangle lies on a two-dimensional page. Keep ambient dimension, simplex dimension, and chain-space dimension separate.

## Connect this to measured data without pretending it proves theorems

The real-data tasks compute a finite label preimage, multiply a small measurement matrix by a selection vector, and center the Iris features. Subtracting the same mean vector from each observation preserves all pairwise differences. You can prove this directly: `(x−μ)−(y−μ)=x−y`.

An observed numerical rank can depend on floating-point tolerance. That is different from exact rank over F₂. State which calculation you performed. A matrix describing the observed flowers is not a proof that all possible flowers lie in the same subspace.

## Reading code with types

`set` stores unique values; a dictionary associates keys to values. A list of lists can represent a matrix. `zip` pairs corresponding entries, while `sum` adds their contributions. In a function's assumptions, “matching lengths” matters: Python zip stops at the shorter input rather than proving that lengths matched.

Your five coding activities are small enough to trace line by line. Do not replace mathematical reasoning with a large library call until you can state what the call should calculate. Then use the library as a comparison, not a substitute for understanding the contract.

**Before advancing:** explain a preimage, an equivalence class, a kernel, and the role of a scalar field without reading the definitions. Use Foundation C or D when a gap appears. Sources R4–R6 are the primary deeper references.

## Work through this stage in three passes

**Pass A — Understand:** read this workbook and the core lesson. Define the new terms in your own words and work one small example by hand.

**Pass B — Implement:** inspect the original real-data lab, predict its outputs, then complete the five new coding activities without opening the answer notebook. Use the visible tests and add one new test.

**Pass C — Defend and retain:** solve the original exercises, explain one failed alternative, and answer the three new retrieval prompts after a delay. Record assistance honestly. A passed program does not prove an essay or theorem.

**Next files:** [Core lesson](../lessons/01_lesson.md) · [Worked lab](../notebooks/01_lab.ipynb) · [Your coding notebook](../practice/learner/01_practice.ipynb) · [Reference coding solutions](../practice/01_solutions.md) · [Retrieval prompts](../practice/retrieval.md).
