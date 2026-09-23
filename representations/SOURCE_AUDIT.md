# Representation learning: supplied notes, checked sources, and course additions
Checked 2026-09-22. The supplied `Pasted markdown(20260922-060459).md` is the requested conceptual basis. This file distinguishes that material from primary-source verification and original teaching experiments. It does not silently replace the source's claims.

## Primary sources
- Balestriero & LeCun, **LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics**, arXiv:2511.08544v3, November 14, 2025. https://arxiv.org/html/2511.08544v3 . Sections 4–5 supply the SIGReg/projection/statistic construction; Section 3 states the assumptions behind the theoretical claims. Official implementation: https://github.com/galilai-group/lejepa . Not installed or runtime-compared here.
- Bardes, Ponce & LeCun, **VICReg**, https://arxiv.org/abs/2105.04906 . Variance/invariance/covariance construction; the original paper is not a guarantee for every independently modified implementation.
- Zbontar et al., **Barlow Twins**, https://arxiv.org/abs/2103.03230 . Cross-correlation objective.
- Chen et al., **SimCLR**, https://arxiv.org/abs/2002.05709 . Two-view contrastive representation learning.
- Grill et al., **BYOL**, https://arxiv.org/abs/2006.07733 . Online/target learning and EMA updates.
- Caron et al., **DINO**, https://arxiv.org/abs/2104.14294 . Self-distillation with vision transformers.
- Assran et al., **I-JEPA**, https://arxiv.org/abs/2301.08243 . Image-region representation prediction.
- Bardes et al., **Revisiting Feature Prediction for Learning Visual Representations from Video**, https://arxiv.org/abs/2404.08471 . V-JEPA background; masking must not be equated with guaranteed past-only forecasting.
- Loshchilov & Hutter, **Decoupled Weight Decay Regularization**, https://arxiv.org/abs/1711.05101 . Distinguishes decoupled decay from an L2 penalty under adaptive optimization.

## Explicit reconciliations
| Supplied wording / emphasis | Checked qualification or original teaching addition |
|---|---|
| SIGReg means Sketched Isotropic Gaussian Regularization. | Confirmed by the primary LeJEPA paper. It regularizes embeddings; it is not sigmoid regression. |
| LeJEPA is expanded as “Lean JEPA.” | The paper's introduction explicitly names **Latent-Euclidean JEPA** and also calls the method lean. We use its explicit expansion. |
| An isotropic Gaussian is illustrated by N(0,I). | That is the standard target. A Gaussian isotropic about its mean more generally has covariance sigma²I. |
| Each dimension has “useful variance”; spreading gives a “healthy/informative” latent. | Variance and usefulness are separate. R04 includes label-independent Gaussian noise; R01 includes dependent/duplicated coordinates. |
| Whitening gives zero mean and identity covariance. | At the fitted sample, under full-rank and stated denominator conventions. It does not establish Gaussianity or useful semantics. |
| Cramér–Wold motivates repeated 1-D checks. | The characterization concerns all projections of population laws. Finite random directions/frequencies/samples are approximations, not proof or a calibrated p-value. |
| SIGReg prevents collapse. | The paper motivates nondegenerate optima. Our exact zero-cloud control has positive penalty and zero first derivative; no universal training-trajectory claim is made. |
| V-JEPA is expressed as past latents predicting future latents. | This is a proposed causal task, not the definition of every masked-video JEPA setup. R05 requires an explicit time cutoff. |
| EMA, detach, and teacher/student mechanisms help avoid pathological solutions. | Their numerical behavior is demonstrated, but these mechanisms alone do not establish representation quality. |
| SIGReg is related to VICReg, Barlow Twins, BYOL, DINO, and contrastive learning. | R03 compares roles. Only agreement-only and agreement-plus-SIGReg encoders are trained in R04; no full-method benchmarks are claimed. |

## Mathematical fidelity of the teaching implementation
The code implements a single-process, fixed-grid projected characteristic-function discrepancy with a standard Gaussian target. Numpy and Torch values are compared; Torch gradients are checked by finite differences. A different O(N²) Gaussian-integral formula independently checks quadrature on small 1-D samples. The two-view agreement objective and all scale factors are stated explicitly. No paper equation with an unexamined proportionality is silently copied as an exact identity.

The implementation lacks official-library parity tests, distributed synchronization, large-image backbones, original benchmark protocols, and original hyperparameter sweeps. It must not be described as a complete reproduction of LeJEPA or the other papers.

## Evidence levels
1. Supplied notes: topic intent and intuition; not runtime or theorem evidence.
2. Primary paper/docs: source-specific definitions and reported claims.
3. Original derivation: worked counterexamples and identities with stated assumptions.
4. Executed controls: measured numerical results in this package/environment.
5. Domain application: only established when its own independent study runs and passes its predeclared checks.

All historical data licenses and acquisition limitations remain attached to the original snapshots. No new full sports-video, wearable, or tracking data are bundled in this release.
