# Foundation C — How to build and check a proof

A proof is an argument establishing a precisely stated conclusion from stated assumptions. It is not a sequence of impressive symbols. It is not the same as a calculation on one dataset, and it is not replaced by a plot that looks convincing.

## Start with a claim you can unpack

Consider: if A is a subset of B, then the inverse image of A under f is a subset of the inverse image of B under f.

**Objects:** f is a function from X to Y; A and B are subsets of Y. **Assumption:** A⊆B. **Conclusion:** f⁻¹(A)⊆f⁻¹(B). To prove one set is contained in another, take an arbitrary element of the first and establish that it belongs to the second.

Take any x∈f⁻¹(A). The definition of inverse image says f(x)∈A. The subset assumption then gives f(x)∈B. The inverse-image definition gives x∈f⁻¹(B). Because x was arbitrary, every element of the first set belongs to the second. That is the complete argument.

Notice which direction the reasoning travels. Starting with an element of f⁻¹(B) would not prove the requested inclusion. Choosing only a convenient x would not cover every element.

## A proof of equality needs both inclusions

To prove f⁻¹(A∩B)=f⁻¹(A)∩f⁻¹(B), follow membership:

x∈f⁻¹(A∩B) exactly when f(x)∈A∩B. That is equivalent to f(x)∈A and f(x)∈B. Those are equivalent to x∈f⁻¹(A) and x∈f⁻¹(B), or membership in the intersection of the two inverse images. Each step is reversible, so it proves both inclusions.

For unions, replace “and” with “or.” For an indexed union, replace “or” by “there exists an index.” These identities later make inverse-image continuity compatible with the axioms of a topology.

## Quantifiers control the difficulty

“Every positive radius contains another sample” is a different claim from “some positive radius contains another sample.” Negating the first produces “there exists a positive radius containing no other sample.” Do not replace it by the stronger statement that no radius contains another sample.

In continuity at x, for every desired output tolerance ε there must exist an input tolerance δ that works for all sufficiently close inputs. The chosen δ can depend on ε and the center x. Swapping the quantifiers can change the statement. Uniform continuity asks for one δ that works across all centers for a given ε; ordinary pointwise continuity does not require that.

For f(x)=2x on the real line, choose δ=ε/2. If |x−y|<δ, then |f(x)−f(y)|=2|x−y|<ε. This establishes the required implication, not merely a graph-based impression.

## Disprove with one counterexample

Squared distance on the real line gives d(0,2)=4, while d(0,1)+d(1,2)=1+1=2. The triangle inequality would require 4≤2, which is false. That single triple disproves the universal claim that squared distance is a metric.

The same strategy helps software testing, but the conclusions differ. A failing test disproves a universal correctness claim for the code on its declared domain. Passing a finite test suite generally does not prove code correctness on all possible inputs. A mathematical proof can establish a theorem for infinitely many cases when the reasoning genuinely covers them.

## Contrapositive and contradiction

The contrapositive of “P implies Q” is “not Q implies not P.” They are logically equivalent. The converse “Q implies P” is not automatically equivalent. For example, a distance-preserving bijection of metric spaces is a homeomorphism; being a homeomorphism does not make every numerical distance equal.

In a contradiction proof, assume the negation of the conclusion together with the original hypotheses and derive an impossibility. State the contradiction explicitly. “This feels impossible” is not a final step. A valid contradiction may be a violated metric axiom, an impossible strict inequality, or two inconsistent values for a defined quantity.

## How to critique your own proof

Underline every statement using “clearly,” “obviously,” or “therefore.” Replace it with the missing definition or reason. Check that every variable has a declared domain. Check that divisions use nonzero denominators. Check the boundary case: empty set, isolated vertex, zero-dimensional vector space, or equal birth/death values.

A homotopy formula that divides by ||x|| must exclude x=0 or justify a continuous extension there. A stability argument needs two functions on the same relevant domain, not unrelated images of different sizes without an alignment map. Small domain mistakes can invalidate a sophisticated-looking argument.

## From guided solution to independent evidence

First read one proof and annotate why each line follows. Close it and reproduce the argument without copying. Then change one assumption and decide whether the result remains true. Finally solve an analogous but unfamiliar problem. Recognizing the published solution is a useful intermediate state, not independent mastery.

For a written submission, use headings: **Claim; Assumptions; Definitions used; Argument; Edge case or counterexample; What this does not prove.** Save it in `my_work/`. That file, not the fact that you opened the lesson, is the learning evidence.

**Primary follow-up:** R4 and R3 in [Sources](../docs/SOURCES.md). Further original worked proofs appear in [Proof atlas](../docs/PROOF_ATLAS.md).
