# Stage 10 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 10.1

**Question:** Find the bottleneck distance between a one-point diagram {(0,4)} and the empty diagram.

**Worked answer:** The cost is half the lifetime, so two. The best diagonal match is (2,2).

## 10.2

**Question:** Compare diagrams {(0,2)} and {(0.1,2.1)}: exhibit a matching of cost 0.1.

**Worked answer:** Match the two off-diagonal points directly. Both birth and death change by 0.1, so the maximum-norm cost is 0.1. Matching them separately to the diagonal costs at least one and is worse.

## 10.3

**Question:** Prove the sublevel-set inclusions from a uniform filtration-value bound δ.

**Worked answer:** For any simplex with f(σ)≤t, g(σ)≤f(σ)+δ≤t+δ. Reverse the roles for the other inclusion. The induced homology maps give the corresponding shift relationships.

## 10.4

**Question:** Why does a pixel perturbation bound also bound the minimum value on shared faces?

**Worked answer:** If |a_i−b_i|≤δ for all incident values, then min a_i≤min b_i+δ and min b_i≤min a_i+δ. Thus their minima differ by at most δ.

## 10.5

**Question:** Why are essential bars rejected by our finite-only distance function?

**Worked answer:** Infinity is not a finite coordinate and cannot be matched to the diagonal at finite cost. Silently removing such bars changes the problem. An extended-diagram method must specify their matching policy.

## 10.6

**Question:** Explain why a long barcode interval is not a statistical p-value.

**Worked answer:** Lifetime is a geometric/algebraic property of a declared filtration. A p-value needs a test statistic and a null distribution under stated assumptions. A long interval supplies neither by itself.

## 10.7

**Question:** Give an example where frame-level random splits would exaggerate model generalization.

**Worked answer:** Adjacent frames from one motion capture can be nearly identical. Training on some and testing on neighboring frames leaks session-specific information. Splitting by recording or participant better matches many deployment questions.

## 10.8

**Question:** What does the Stage 10 corruption experiment establish and not establish?

**Worked answer:** It checks descriptor sensitivity and a fixed-grid stability bound under the declared bounded perturbation. It does not establish unseen-writer robustness, causal meaning, general statistical significance, or superiority to a baseline.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
