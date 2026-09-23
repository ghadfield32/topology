# The four supplied posts: source claims versus course conclusions

The posts are the requested starting material, not a substitute for definitions, proofs, or measurements. We retain their central questions and terminology. The qualifications below are explicitly added analysis and primary-source research. The ZIP omits LinkedIn navigation, profile details, unrelated comments and scraped images.

## 1. PINN/PIKAN gradient conflict — supplied Jagtap post

**What the attachment says:** residual, boundary and interface objectives can conflict in domain-decomposed physics learning; the authors propose Norm-PCGrad, compare it with PCGrad and ConFIG, and discuss SPINN substitutions. Their reported wins and overhead are benchmark-specific claims.

**What was verified externally:** the matching Menon, Tezaur and Jagtap preprint is arXiv:2609.14841v1, dated 13 September 2026 [NORM]. Its Algorithm 1 projects each gradient against original comparison gradients, then normalizes the resulting rows for Norm-PCGrad. We implement that operation with a documented zero-row convention. The preprint also discusses incorrect interfaces producing trivial solutions; changing gradient aggregation does not repair a wrong physical formulation.

**What our code establishes:** exact two-vector calculations, degenerate opposing vectors, real regression gradients, and a manufactured interface counterexample. No full 2D/3D XPINN, PIKAN, optimizer, hardware or accuracy benchmark is reproduced. The multi-gradient construction is inspected with actual dot products instead of assuming its name is a proof of simultaneous descent. The preprint's broad prose and its more restricted two-gradient analysis must not be conflated.

## 2. Symplectic phase space, constraint manifolds and tensor throughput — supplied Jui post

**What the attachment says:** soft penalties do not guarantee long-horizon physical invariants; symplectic structure, manifold projection, and hardware-aware computation are proposed as alternatives. It additionally claims exact energy conservation at arbitrary rollout lengths, exact manifold correction, and deterministic petascale throughput.

**Our separate mathematical analysis:** for a differentiable autonomous Hamiltonian, its exact continuous flow preserves that Hamiltonian. A symplectic discrete update preserves the symplectic form; it need not preserve the original Hamiltonian exactly. Stage 24 gives a two-number counterexample. A continuous energy claim also depends on the state and forces: friction and forcing change the balance. Atmospheric and fluid models cannot all be treated as finite-dimensional, unforced canonical Hamiltonian systems without specifying their formulation and exchanges.

Use J for the canonical skew matrix and A=DC for the constraint Jacobian. They are different matrices. The correction z-A^T(AA^T)^(-1)C(z) solves the linearized constraint; it is exact for a full-row-rank affine constraint but generally iterative for nonlinear constraints. Stage 25 starts with (2,0) outside the unit circle and obtains (1.25,0), still infeasible. A retraction is not generally an exact geodesic or a symplectic time integrator. Rank loss and failed iterations are surfaced, not silently accepted.

**Unsupported performance inference:** the attachment does not provide reproducible kernel code, hardware, precision, tolerances, batch sizes, full timing boundaries or error comparisons supporting the throughput claim. Matrix multiplication can accelerate parts of a solver; it does not prove that nonlinear solves disappear or that mixed precision preserves the same tolerances. No such GPU result is claimed here.

## 3. HNN versus LNN — supplied Goraeya post

**What the attachment says:** HNNs learn H(q,p); LNNs learn L(q,qdot); Hamilton's and Euler–Lagrange equations generate dynamics; the Legendre transform connects the formulations. It lists PINNs, neural operators, DeepONet, physics-informed transformers, inverse problems, Neural ODEs, FNO, differentiable physics and physics-informed GNNs as learning directions.

**Added assumptions:** p=partial L/partial qdot, not necessarily velocity. Inverting the velocity-to-momentum map requires regularity; constraints may require multipliers or reduced coordinates. An additive constant in H cannot be identified from its derivatives; an arbitrary total time derivative added to L leaves the Euler–Lagrange equations unchanged. A learned structure is not automatically the true measured energy. Time-dependent, dissipative, forced and contact systems need an appropriate extension.

**Implementation depth:** we train a small scalar-H network and a deliberately restricted unit-mass LNN. We test a general one-degree-of-freedom Hessian formula separately, including its singular case. The distinction is visible in the results rather than treating the restricted fit as a reproduction of the LNN paper.

## 4. Smooth charts, diffeomorphisms and vector-field flows — supplied Nicolas/Abeywardana post

**What the attachment says:** charts describe local manifold patches in Euclidean coordinates; smooth overlap maps connect coordinate descriptions; a vector-field flow generates local diffeomorphisms. A comment connects this with normalizing flows.

**Added assumptions:** for smooth vector fields, the local flow exists and is smooth on its domain; existence for every time requires additional completeness conditions. The example x'=x² blows up in finite time for positive initial x. An arbitrary discretization or projection need not be invertible. In a smooth atlas, a transition is psi composed with phi inverse on the shared domain, not equality of coordinate numbers. A perspective image is not an invertible chart of a whole scene.

**Implemented evidence:** local flow and inverse checks, an explicit affine coupling with its log-Jacobian determinant, and round trips on measured Iris features. The transformed observations are constructed data; they do not establish that plant growth followed the chosen flow.

## How to use this audit

Before accepting any claim, write five sentences: what the source actually says; the mathematical assumptions; what experiment we executed; what its result supports; what it does not support. Source claims, mathematical deductions, manufactured tests, empirical results and deployment claims stay separate. See [coverage](COVERAGE.md) for exact implementation depth and [sources](SOURCES.md) for primary readings.

## Revision check for the gradient-surgery paper

The initial worked algorithm was pinned to arXiv:2609.14841v1 (13 September 2026). During the final source check, the current page identified v2 (16 September 2026). Algorithm 1 in [v2](https://arxiv.org/html/2609.14841v2) was rechecked: its Norm-PCGrad branch still normalizes the projected rows before summing. The zero-row policy in this course is explicitly our implementation convention.

The revised paper also compares curvature-aware quasi-Newton optimization, including SSBroyden. That is an additional primary reading, not an executed reproduction here. A quasi-Newton method uses changing gradient information to approximate curvature; it is not another name for a gradient projection. Learn that distinction before comparing runtimes or accuracy across differently configured optimizers. Published benchmark wins remain the authors' results, not universal guarantees or results measured in this package.
