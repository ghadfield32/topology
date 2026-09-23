# Methods lab — Read a scientific claim, then test exactly what it says

## Four kinds of statement

A source can motivate an idea without proving it. Keep four labels separate: **source claim**, **mathematical statement with assumptions**, **original worked calculation**, and **measured experiment**. This lesson uses the supplied posts about symplectic structure, projection and PINN gradient conflicts as prompts. The source audit records their scope. We do not rewrite the posts as if their authors had supplied our qualifications.

The symplectic post asserts exact energy conservation across arbitrary rollout steps and describes one algebraic correction as restricting updates to a physical constraint manifold. The gradient-conflict post reports Norm-PCGrad advantages on its selected benchmarks. The HNN/LNN post links formulations through the Legendre transform. The manifold post describes local charts and smooth transitions. These are the supplied sources' positions; the calculations below are original educational checks, not reproductions of their empirical studies.

## Continuous dynamics and discrete updates are not the same object

For canonical coordinates z=(q,p), let J=[[0,1],[-1,0]] and dynamics z_dot=J grad H. For differentiable, time-independent H and an exact solution, the chain rule gives dH/dt = grad(H)^T J grad(H)=0 because J is skew-symmetric. Explicit time dependence or external dissipative forces change the claim. A floating-point integrator is a discrete map approximating a trajectory; it needs its own analysis.

Take H=(q²+p²)/2, nondimensional unit-oscillator variables. Kick then drift:

p_new = p - h q; q_new = q + h p_new.

At (q,p)=(1,0), h=0.2 gives p_new=-0.2 and q_new=0.96. Energy changes from 0.5 to (0.96²+0.2²)/2=0.4808. The map A=[[1-h²,h],[-h,1]] nevertheless satisfies A^T J A=J. Thus being symplectic does not imply exact conservation of this H at every step. The lab checks both identities separately and plots a longer trajectory, without calling nondimensional values joules or seconds.

## A single linearized correction can leave a residual

For C(x)=x^T x-1, the desired set is the unit sphere. Its Jacobian is 2x^T. The minimum-norm linearized correction is x_new=x-((x^T x-1)/(2x^T x))x when x is nonzero. At x=(2,0), it gives (1.25,0). The new constraint residual is 1.25²-1=0.5625, not zero. It has solved the first-order approximation, not the original nonlinear equation exactly.

Iteration can reduce the residual; radial normalization x/||x|| is exact for this particular sphere away from zero. Neither fact makes one formula an exact universal projection for every constraint. At zero the Jacobian is rank deficient. The reference function raises a clear error instead of inventing a direction. At arbitrary constraints, rank, convergence region, metric and desired conservation properties must be examined independently.

## Conflicting objectives do not always admit simultaneous improvement

For two losses with gradients g1=(1,0) and g2=(-1,0), their inner product is -1. A small update -ηd decreases both to first order only if g1·d>0 and g2·d>0. These conditions contradict each other. No gradient-surgery algorithm can produce a direction satisfying both strict inequalities in this example. An optimizer may choose a compromise or stall; it does not remove mathematical incompatibility.

The supplied Norm-PCGrad preprint's reported improvements are benchmark-specific. Our small example is not a performance comparison between PCGrad, Norm-PCGrad and ConFIG. The existing Stage 27 covers their operations and interface-condition issues. [Primary preprint](https://arxiv.org/abs/2609.14841).

## Turn the lesson into a claim ledger

For each future paper, save its exact source/version, the proposed guarantee, assumptions, the implemented object, the test, and its scope. Distinguish a model's learned vector field from the numerical solver and the hardware implementation. Timing one matrix multiplication does not establish end-to-end latency; matching a drawing does not establish camera calibration. Those topics are developed in the retained geometry stages.

The lab also loads observed Seeds measurements to compare two homeomorphic rectangle controls and the source's compactness feature. This is a real-data bridge, not evidence that wheat obeys Hamiltonian dynamics. Use observed data when the scientific question fits; use an exact manufactured counterexample when falsifying a universal mathematical claim.

To pass, derive each counterexample on paper, run it, explain the variable and unit conventions, and rewrite your own conclusion so it says no more than the calculation supports. A numerical test supports a calculation; it is not a substitute for a general proof.

[Claim audit](../../docs/v7/SOURCE_AUDIT.md) · [Worked lab](lab.ipynb) · [Learner coding](learner.ipynb) · [Reference answers](answers.ipynb) · [Questions](questions.md)
