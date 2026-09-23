# Concepts, transfer and delayed recall

Answer before revealing the criteria. These are not automatically graded.

## concrete_slump.Q1

Why exclude source_id, slump and flow from these predictors?

<details><summary>Answer criteria</summary>

The ID is not a causal ingredient, and slump/flow are measured responses unavailable under the chosen pre-measurement task. Another task may use them only after documenting availability.

</details>

## concrete_slump.Q2

For 25 calibration errors and α=0.1, which sorted value is used?

<details><summary>Answer criteria</summary>

ceil(26×0.9)=24, one-based: Python index 23. No interpolated quantile is used.

</details>

## concrete_slump.Q3

Why might a small calibration set return an infinite radius?

<details><summary>Answer criteria</summary>

The finite-sample corrected rank can be n+1 at an extreme target coverage. A finite maximum would not implement the chosen conservative rank rule.

</details>

## concrete_slump.Q4

Does 90% nominal marginal coverage guarantee this particular recipe?

<details><summary>Answer criteria</summary>

No. The guarantee averages over calibration and test sampling under its assumptions. It does not give pointwise conditional coverage for every recipe.

</details>

## concrete_slump.Q5

Why is a wide interval potentially unhelpful even with high coverage?

<details><summary>Answer criteria</summary>

Coverage alone can be achieved by nearly uninformative sets. Width in MPa and consequences of uncertainty must be reported too.

</details>

## concrete_slump.Q6

Does a random row permutation prove exchangeability?

<details><summary>Answer criteria</summary>

No. It does not erase dependence, collection shifts, or missing physical batch identities. The protocol is an educational within-collection study.

</details>

## concrete_slump.R1 — delayed recall

Without reopening the lab, answer and invent one contrasting example: Why exclude source_id, slump and flow from these predictors?

<details><summary>Criteria</summary>

The ID is not a causal ingredient, and slump/flow are measured responses unavailable under the chosen pre-measurement task. Another task may use them only after documenting availability. A correct contrasting example must change a relevant assumption, not merely a numerical constant.

</details>

## concrete_slump.R2 — delayed recall

Without reopening the lab, answer and invent one contrasting example: Why might a small calibration set return an infinite radius?

<details><summary>Criteria</summary>

The finite-sample corrected rank can be n+1 at an extreme target coverage. A finite maximum would not implement the chosen conservative rank rule. A correct contrasting example must change a relevant assumption, not merely a numerical constant.

</details>

## concrete_slump.R3 — delayed recall

Without reopening the lab, answer and invent one contrasting example: Does a random row permutation prove exchangeability?

<details><summary>Criteria</summary>

No. It does not erase dependence, collection shifts, or missing physical batch identities. The protocol is an educational within-collection study. A correct contrasting example must change a relevant assumption, not merely a numerical constant.

</details>
