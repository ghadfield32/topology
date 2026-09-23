# Primary resources and reading routes

Reviewed 20 September 2026. External readings are linked, not redistributed. The numerical examples and counterexamples are original course constructions. A linked article is not evidence that we reproduced its experiments.

### NIST — Hahn1 observed copper thermal-expansion data

https://www.itl.nist.gov/div898/strd/nls/data/LINKS/DATA/Hahn1.dat

56-row numeric excerpt; source has 236 observations. Response multiplier not specified.

### HNN — Hamiltonian Neural Networks (2019)

https://arxiv.org/abs/1906.01563

Scalar Hamiltonian and derivative supervision; not a discrete-integrator energy guarantee.

### LNN — Lagrangian Neural Networks (2020)

https://arxiv.org/abs/2003.04630

General Lagrangian formulation; our trained example is deliberately restricted.

### PCGRAD — Gradient Surgery for Multi-Task Learning (2020)

https://arxiv.org/abs/2001.06782

Projection of conflicting gradients; finite-step and multi-gradient behavior must be checked.

### CONFIG — ConFIG: Towards Conflict-free Training of Physics Informed Neural Networks (2024)

https://arxiv.org/abs/2408.11104

Normalized equal-alignment construction; degenerate/incompatible inputs need explicit handling.

### NORM — Tackling Failure Modes of PINNs and PIKANs Using Conflict-Free Gradients (v1, 13 September 2026)

https://arxiv.org/html/2609.14841v1

Preprint benchmarks not replicated here. Algorithm 1 normalizes projected rows before aggregation.

### PINN — Physics Informed Deep Learning — author project

https://maziarraissi.github.io/PINNs/

Physics residual and data formulations; not evidence that arbitrary PINN training succeeds.

### FAIL — Characterizing possible failure modes in physics-informed neural networks (2021)

https://arxiv.org/abs/2109.01050

Failure analysis motivates residual/error checks and conventional baselines.

### SPINN — Separable Physics-Informed Neural Networks (2023)

https://arxiv.org/abs/2306.15969

Per-axis evaluation and forward-mode differentiation; full output/residual accounting remains necessary.

### KAN — KAN: Kolmogorov-Arnold Networks (2024)

https://arxiv.org/abs/2404.19756

Learned univariate edge functions; no complete PIKAN training replication is supplied.

### DEEPONET — Learning nonlinear operators via DeepONet (2019/2021)

https://arxiv.org/abs/1910.03193

Branch/trunk representation; approximation results do not ensure optimization success.

### FNO — Fourier Neural Operator for Parametric Partial Differential Equations (2020)

https://arxiv.org/abs/2010.08895

Learned Fourier-space operator layers; a known FFT heat solver is a different object.

### NODE — Neural Ordinary Differential Equations (2018)

https://arxiv.org/abs/1806.07366

Continuous-state modeling; our differentiable RK4 uses direct discrete backpropagation, not the adjoint method.

### GNS — Learning to Simulate Complex Physics with Graph Networks (2020)

https://arxiv.org/abs/2002.09405

Graph simulation reference; our pair-force example is an algebraic building block, not that model.

### PINNSFORMER — PINNsFormer (2023)

https://arxiv.org/abs/2307.11833

Specific transformer PINN architecture; only the prerequisite attention/constraint experiment is implemented.

### NVP — Density estimation using Real NVP (2016)

https://arxiv.org/abs/1605.08803

Affine coupling and change of variables; our fixed invertible example is not a trained density model.

### CONSTRAINED — Simplifying Hamiltonian and Lagrangian Neural Networks via Explicit Constraints (2020)

https://arxiv.org/abs/2010.13581

Constraint-aware dynamics requires a formulated system; arbitrary projection is not a substitute.

### TONG — David Tong — Classical Dynamics lecture notes

https://www.damtp.cam.ac.uk/user/tong/dynamics.htm

Free deeper-reading destination; use the Lagrangian and Hamiltonian chapters. No page-specific quotation relied on.

## Revision check for the gradient-surgery paper

The initial worked algorithm was pinned to arXiv:2609.14841v1 (13 September 2026). During the final source check, the current page identified v2 (16 September 2026). Algorithm 1 in [v2](https://arxiv.org/html/2609.14841v2) was rechecked: its Norm-PCGrad branch still normalizes the projected rows before summing. The zero-row policy in this course is explicitly our implementation convention.

The revised paper also compares curvature-aware quasi-Newton optimization, including SSBroyden. That is an additional primary reading, not an executed reproduction here. A quasi-Newton method uses changing gradient information to approximate curvature; it is not another name for a gradient projection. Learn that distinction before comparing runtimes or accuracy across differently configured optimizers. Published benchmark wins remain the authors' results, not universal guarantees or results measured in this package.
