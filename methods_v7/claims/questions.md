# Concepts, transfer and delayed recall

Answer before revealing the criteria. These are not automatically graded.

## claims.Q1

Compute the first symplectic Euler state and energy for the worked oscillator.

<details><summary>Answer criteria</summary>

From (1,0), h=.2: p_new=-.2, q_new=.96, H_new=.4808, not .5.

</details>

## claims.Q2

What does A.T J A=J establish here, and what does it not establish?

<details><summary>Answer criteria</summary>

It establishes the canonical symplectic matrix condition for this linear update. It does not establish exact conservation of the chosen H for every step.

</details>

## claims.Q3

Why does the sphere correction yield residual .5625?

<details><summary>Answer criteria</summary>

At (2,0), the linearized correction subtracts (.75,0), leaving (1.25,0); 1.25²-1=.5625.

</details>

## claims.Q4

Why is the sphere correction undefined at the origin?

<details><summary>Answer criteria</summary>

The constraint Jacobian is zero and its required rank condition fails; there is no unique direction supplied by this formula.

</details>

## claims.Q5

Can a direction decrease objectives with opposite gradients strictly to first order?

<details><summary>Answer criteria</summary>

No. Requiring g·d>0 and -g·d>0 simultaneously is contradictory.

</details>

## claims.Q6

Does the new lab reproduce Norm-PCGrad benchmark superiority?

<details><summary>Answer criteria</summary>

No. It tests small operations and counterexamples. The paper’s selected-domain benchmark results remain attributed external findings, not reproduced here.

</details>

## claims.R1 — delayed recall

Without reopening the lab, answer and invent one contrasting example: Compute the first symplectic Euler state and energy for the worked oscillator.

<details><summary>Criteria</summary>

From (1,0), h=.2: p_new=-.2, q_new=.96, H_new=.4808, not .5. A correct contrasting example must change a relevant assumption, not merely a numerical constant.

</details>

## claims.R2 — delayed recall

Without reopening the lab, answer and invent one contrasting example: Why does the sphere correction yield residual .5625?

<details><summary>Criteria</summary>

At (2,0), the linearized correction subtracts (.75,0), leaving (1.25,0); 1.25²-1=.5625. A correct contrasting example must change a relevant assumption, not merely a numerical constant.

</details>

## claims.R3 — delayed recall

Without reopening the lab, answer and invent one contrasting example: Does the new lab reproduce Norm-PCGrad benchmark superiority?

<details><summary>Criteria</summary>

No. It tests small operations and counterexamples. The paper’s selected-domain benchmark results remain attributed external findings, not reproduced here. A correct contrasting example must change a relevant assumption, not merely a numerical constant.

</details>
