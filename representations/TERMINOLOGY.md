# Terminology map — one entry point, not another required course

Use this index when a term in the supplied notes is unfamiliar. Definitions developed in a lesson are not assigned again as a second chapter. Model-family names below are orientation vocabulary, not a claim that every architecture is implemented or trained.

| Term | Meaning and first distinction | Where to learn/use it |
|---|---|---|
| LinReg, OLS | Linear regression; ordinary least squares minimizes squared residuals under a stated design | Existing regression industry cases; R03 losses |
| LogReg, GLM | Logistic regression models class probabilities; generalized linear models combine a distribution and link | R04 frozen probe; existing classification cases |
| Ridge, Lasso, Elastic Net | L2, L1, and combined parameter penalties | R03; distinguish from embedding regularization |
| SIGReg | Sketched Isotropic Gaussian Regularization | R02 definition and numerical checks |
| MSE, MAE | Mean squared and mean absolute residuals | R03; sensitivity to error magnitude |
| BCE, CE, NLL | Binary/multiclass cross-entropy; negative log likelihood | R03 probability-model distinctions |
| L1, L2, WD | Absolute/squared parameter penalties; weight decay | R03, source audit for AdamW |
| Dropout | Stochastic activation masking in training with a specified inference convention | R03; not automatically label-preserving input masking |
| Embedding, latent, latent space | Internal representation and the space it occupies | R01; no assumed physical units |
| Complete/dimensional collapse | All inputs coincide / representation loses rank | R01–R04 |
| VICReg | Variance-Invariance-Covariance Regularization | R03 numerical implementation, not full training reproduction |
| Barlow Twins | Cross-view cross-correlation objective | R03 |
| Contrastive, positive, negative | Specified pair relationships and separations | R03, false-negative examples |
| InfoNCE, NT-Xent | Related contrastive objective forms; exact denominator matters | R03 code and indexing exercise |
| BYOL | Bootstrap Your Own Latent | R03 mechanism overview, not trained here |
| EMA | Exponential moving average | R03 hand calculation and code |
| Stop-gradient, detach | Value used forward; specified derivative path blocked | R03 finite numerical demonstration |
| Teacher/student, distillation | Roles for producing and fitting targets | R03; teacher update policy must be explicit |
| DINO | Original self-distillation-without-labels method and later family | R03 original-method orientation; no successor training claim |
| SSL | Self-supervised or semi-supervised learning, depending on context | R03: encoder task versus labeled evaluation |
| JEPA | Joint-Embedding Predictive Architecture | R03/R05 context-target structure |
| I-JEPA | Image-region representation prediction | R03 source reading |
| V-JEPA | Video representation prediction; not every mask is causal | R03/R05 time-cutoff reasoning |
| LeJEPA | Latent-Euclidean JEPA, as explicitly named in the checked paper | Source audit; R04 small inspired ablation |
| Normal/Gaussian | Probability family characterized by mean and covariance when jointly Gaussian | R01 |
| Isotropic / standard | Equal directional variance / specifically zero mean and identity covariance | R01 distinction |
| Covariance, whitening | Second moments / fitted transform of those moments | R01, rank assumptions |
| Sketch, random projection | Lower-dimensional directional observation | R02 |
| Cramér–Wold | Characterization via all linear projections of a joint law | R02; finite-sketch limitation |
| Characteristic function | Expected complex exponential; empirical sine/cosine means | R02 |
| Epps–Pulley | Characteristic-function-based normality statistic family | R02; fixed target/convention not a supplied p-value |
| PCA, SVD | Principal components; singular value decomposition | Existing linear-algebra primer and R04 training-only PCA |
| t-SNE, UMAP | Nonlinear visualization/embedding methods with parameter-sensitive geometry | Orientation only; no assumption that distances/topology are preserved |
| AE, VAE | Autoencoder reconstruction; variational latent-variable model | Orientation only; not trained in this expansion |
| RF, DT | Random forest; decision tree | Existing baseline vocabulary; not a new required route |
| GBM, XGB, LGBM | Gradient boosting family and named implementations | Orientation; current software not benchmarked here |
| MLP, CNN, ViT | Dense layers; convolutions; vision transformer | R04 trains an MLP; existing Stage 16 attention |
| RNN, LSTM, GRU | Recurrent model families | Orientation for temporal modeling, not evidence of causal correctness |
| GNN | Graph neural network | Existing Stage 29 structural updates |
| GD, SGD, LR, BP | Gradient descent, stochastic gradient descent, learning rate, backpropagation | Existing differentiation primer; R03–R04 |
| Adam, AdamW | Adaptive optimizers; AdamW decouples weight decay | R04 declared optimizer; source audit |
| ROC/AUC, PR/AP | Threshold-sweep summaries; area under ROC; precision-recall; average precision | Existing evaluation cases; averaging convention must be stated |
| IoU, mAP | Intersection-over-union; mean average precision | Existing CV scope; matching thresholds/classes change meaning |
| R² | Relative squared-error score against a stated mean baseline | Existing regression cases; may be negative on held-out data |
| uv, lock, venv | Dependency tool; resolved graph; local Python environment | Current FIRST_RUN.md |
| Image, container, Pod, Job, PVC | Deployment objects with distinct roles | Current KUBERNETES.md; not mathematical prerequisites |

## Fast retrieval questions
1. Which three meanings of “normalization” have appeared, and which statistics are fitted?
2. Why can an SSL encoder be evaluated with labels without those labels entering pretraining?
3. What is the difference between a low loss, noncollapsed covariance, useful predictions, and calibrated physical output?
4. Which terms above describe concepts only, which have code controls, and which have a trained experiment?

Answer from the canonical lessons, not from the abbreviation alone. See SOURCE_AUDIT.md for the primary readings and corrections to the supplied wording.
