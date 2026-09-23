# Stage 09 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 09.1

**Question:** Trace the last edge column in the triangle-boundary example until it reduces to zero.

**Worked answer:** Start with {1,2}. XOR with {0,2} gives {0,1}. XOR with {0,1} gives the empty set. This is the cycle birth, subject to the later coface-pairing step.

## 09.2

**Question:** Why must faces precede cofaces at tied filtration values?

**Worked answer:** The filtration order must be compatible with inclusion. The boundary matrix needs each simplex’s faces available earlier; otherwise the matrix does not encode the required ordered chain complex.

## 09.3

**Question:** What does a zero reduced column mean, and how is its death found?

**Worked answer:** It creates a class in the simplex’s dimension. Search whether its column index is the low row of a later reduced nonzero column. That later simplex supplies the death; absence of a pair gives infinite death within the input filtration.

## 09.4

**Question:** Why is adding columns by ordinary integer addition wrong over F₂?

**Worked answer:** Over F₂, 1+1=0. Ordinary integer addition produces 2 instead of cancellation. XOR or arithmetic modulo two is required.

## 09.5

**Question:** Which parameters must match before comparing two library diagrams?

**Worked answer:** Coefficient field, Rips distance versus radius convention, chosen complex, maximum homology dimension with sufficient cofaces, cutoff, treatment of infinite and zero-length intervals, and numerical comparison tolerance.

## 09.6

**Question:** Explain why a graph-only calculation can create a false infinite H₁ bar.

**Worked answer:** A graph cycle can be killed by a triangle in the intended clique complex. Omitting all triangles removes the possible death operation, leaving a class that should not survive.

## 09.7

**Question:** What evidence do the independent H₀ merge calculation and direct Betti checks add?

**Worked answer:** H₀ union-find checks merge scales using a different algorithm. Direct ranks check the number of live classes at event scales. Some common input construction remains shared, so the checks do not eliminate every common-mode error.

## 09.8

**Question:** Open the optional library-check report and explain the difference between SKIPPED and PASSED.

**Worked answer:** SKIPPED means the required execution did not happen, for example because a package was unavailable. It supplies no evidence of agreement. PASSED means the named assertions were actually executed and succeeded.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
