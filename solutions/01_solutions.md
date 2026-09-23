# Stage 01 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 01.1

**Question:** Find f⁻¹([1,9]) for f(x)=x² on R. Explain the endpoints.

**Worked answer:** The inverse image is [-3,-1] ∪ [1,3]. Solving 1≤x²≤9 yields 1≤|x|≤3, and equality is allowed.

## 01.2

**Question:** Negate: “For every radius r>0 there exists a sample with property P(r).”

**Worked answer:** There exists a radius r>0 for which no sample has P(r). The quantifiers both reverse and the inner property is negated.

## 01.3

**Question:** Prove f⁻¹(A ∩ B)=f⁻¹(A) ∩ f⁻¹(B).

**Worked answer:** x belongs to the left side exactly when f(x) is in both A and B; that is equivalent to x belonging to both inverse images. The equivalence proves both inclusions.

## 01.4

**Question:** Prove that congruence modulo three is an equivalence relation.

**Worked answer:** a−a=0 is divisible by 3. If a−b=3k, then b−a=−3k. If a−b=3k and b−c=3l, then a−c=3(k+l). These prove reflexivity, symmetry and transitivity.

## 01.5

**Question:** Find the kernel and image of [[1,2],[2,4]] over R.

**Worked answer:** The map sends (x,y) to (x+2y)(1,2). Its image is span{(1,2)} and its kernel is span{(-2,1)}. Rank and nullity are both one.

## 01.6

**Question:** Explain why the binary three-by-three matrix in the lesson has different ranks over R and F₂.

**Worked answer:** Over F₂, row 3 equals row 1 plus row 2, while the first two are independent, so rank is two. Over R its determinant is -2, not zero, so rank is three. The scalar arithmetic changes linear dependence.

## 01.7

**Question:** Why does having four measured columns not prove that a biological population is a four-dimensional manifold?

**Worked answer:** Four columns specify an ambient representation. They do not establish local Euclidean structure, intrinsic dimension, sampling adequacy, or absence of constraints and noise.

## 01.8

**Question:** Explain the difference between a list of observations with duplicates and the set of distinct measurement vectors.

**Worked answer:** The list preserves measurement multiplicity and sample identity. The set collapses equal vectors. Zero feature distance between distinct observation IDs is possible; later we describe this as a pseudometric on IDs.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
