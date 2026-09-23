# Stage 03 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 03.1

**Question:** Prove the composition of two continuous functions is continuous.

**Worked answer:** For U open in the final codomain, g⁻¹(U) is open by continuity of g, then f⁻¹(g⁻¹(U)) is open by continuity of f. This set is the inverse image under the composition.

## 03.2

**Question:** Give a homeomorphism from (0,2) to (5,9) and its inverse.

**Worked answer:** f(x)=2x+5; f⁻¹(y)=(y−5)/2. Each is continuous, and their compositions are identities on the declared intervals.

## 03.3

**Question:** Explain the continuous-bijection counterexample using two finite topologies.

**Worked answer:** The identity from discrete {a,b} to indiscrete {a,b} is continuous because only empty and whole-target inverse images must be checked. The reverse identity fails for the open target singleton {a}.

## 03.4

**Question:** Why does a path-connected space have to be connected?

**Worked answer:** If a separation existed, choose one point in each part and a path between them. Its image would be connected as a continuous image of [0,1], yet would meet both parts of the separation, a contradiction. This uses the standard connectedness of intervals.

## 03.5

**Question:** Use the given cover to show (0,1) is not compact.

**Worked answer:** Each x in (0,1) lies in (1/n,1) for a sufficiently large n. A finite choice has a largest n=N; its union is (1/N,1), so it misses smaller positive points.

## 03.6

**Question:** Explain where compactness and the Hausdorff assumption enter the homeomorphism theorem.

**Worked answer:** Compactness makes closed subsets of the domain compact and their continuous images compact. The Hausdorff assumption makes those compact images closed. Thus the map is closed, which gives continuity of its inverse.

## 03.7

**Question:** Is projection R⁴→R² a homeomorphism? Could its restriction to a particular finite sample be bijective?

**Worked answer:** It is not a homeomorphism of the ambient spaces because it is not injective: changing either discarded coordinate preserves the output. On a particular finite sample it may happen to be injective and hence bijective onto its finite image; that does not recover the missing ambient coordinates.

## 03.8

**Question:** Why can finitely many plotted points not establish continuity of a function on all of R?

**Worked answer:** A function can agree with a continuous function at every sampled point and jump at an unobserved point. A universal claim needs assumptions or a proof beyond finite agreement.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
