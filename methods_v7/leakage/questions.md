# Concepts, transfer and delayed recall

Answer before revealing the criteria. These are not automatically graded.

## leakage.Q1

How many observed kernels are there after making three copies of each row?

<details><summary>Answer criteria</summary>

Still 210. The 630 software rows include constructed copies, not independent new observations.

</details>

## leakage.Q2

Can row indices be disjoint while source kernels overlap?

<details><summary>Answer criteria</summary>

Yes. Separate copies have different row indices but the same source ID; compare those identities explicitly.

</details>

## leakage.Q3

Why can one-nearest-neighbor benefit strongly from duplicates?

<details><summary>Answer criteria</summary>

An exact training copy is at distance zero from a test copy; this rewards memorization of the same evidence rather than transfer to a new kernel.

</details>

## leakage.Q4

Why not repair the audit by generating unique IDs for every copy?

<details><summary>Answer criteria</summary>

That changes the meaning of the unit key and conceals the problem. Unit identity must reflect the independent object under evaluation.

</details>

## leakage.Q5

What remains invariant under a consistent positive column rescaling followed by training standardization?

<details><summary>Answer criteria</summary>

For the same training rows, the standardized numerical arrays agree up to floating-point error. The statement does not extend to arbitrary nonlinear changes.

</details>

## leakage.Q6

What group would matter for a deployment on previously unseen camera sessions?

<details><summary>Answer criteria</summary>

Session identity and, as appropriate, participant/site identity and timing support. A row-only split cannot establish that independence.

</details>

## leakage.R1 — delayed recall

Without reopening the lab, answer and invent one contrasting example: How many observed kernels are there after making three copies of each row?

<details><summary>Criteria</summary>

Still 210. The 630 software rows include constructed copies, not independent new observations. A correct contrasting example must change a relevant assumption, not merely a numerical constant.

</details>

## leakage.R2 — delayed recall

Without reopening the lab, answer and invent one contrasting example: Why can one-nearest-neighbor benefit strongly from duplicates?

<details><summary>Criteria</summary>

An exact training copy is at distance zero from a test copy; this rewards memorization of the same evidence rather than transfer to a new kernel. A correct contrasting example must change a relevant assumption, not merely a numerical constant.

</details>

## leakage.R3 — delayed recall

Without reopening the lab, answer and invent one contrasting example: What group would matter for a deployment on previously unseen camera sessions?

<details><summary>Criteria</summary>

Session identity and, as appropriate, participant/site identity and timing support. A row-only split cannot establish that independence. A correct contrasting example must change a relevant assumption, not merely a numerical constant.

</details>
