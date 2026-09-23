# Stage 11 — Worked solutions

Read after an independent attempt. These answer this course’s original exercises, not graded exercises from an external course.

## 11.1

**Question:** Calculate a tent function for [0,2) at t=0, 0.5, 1, 1.5 and 2.

**Worked answer:** The values are 0, 0.5, 1, 0.5, 0. Each is max(0,min(t,2−t)). It rises to the midpoint and falls back to zero.

## 11.2

**Question:** Explain the coordinate systems of an original digit image, a persistence diagram, and a persistence image.

**Worked answer:** The original image has spatial row/column coordinates with intensity values. The diagram has birth/death coordinates with interval multiplicity. The persistence image usually uses birth/lifetime coordinates with integrated weighted kernel mass.

## 11.3

**Question:** Why can a finite-interval count be unstable even when the diagram is stable?

**Worked answer:** Arbitrarily short bars near the diagonal can appear or disappear under small perturbations. The bottleneck cost can be tiny while the raw number of finite bars changes. A stable input descriptor does not make every discontinuous downstream statistic stable.

## 11.4

**Question:** What is the role of each of training, validation and test data?

**Worked answer:** Training fits parameters; validation selects among declared choices; test evaluates the finalized procedure. Repeatedly choosing based on test scores turns test into another validation set.

## 11.5

**Question:** Why is fitting a standardizer on all images before splitting a leakage problem?

**Worked answer:** The test distribution influences the learned means and scales used to train the model. Fitting transformations only on training rows better matches how unseen inputs are processed in deployment.

## 11.6

**Question:** Explain every step of the scalar-lens Mapper construction.

**Worked answer:** Choose a lens; cover its range; select observations in each cover element; cluster them in the chosen feature space; make a node per cluster; connect nodes sharing original sample IDs. Report cover and clustering parameters.

## 11.7

**Question:** When is the forward delay vector (x_t,x_(t+2),x_(t+4)) available?

**Worked answer:** Only at t+4, when the last value has arrived. Attributing the full vector to time t as immediately available would introduce future information.

## 11.8

**Question:** Why would equal or worse performance from topology still be an informative result?

**Worked answer:** It identifies a limit of the method for that question and provides a valid baseline comparison. The goal is to learn whether shape descriptors add useful information, not guarantee a positive result.

## Delayed retrieval

In several days, change one number or assumption in two exercises and solve them without reading this file. Explain how the answer changes and why. Record the new questions and your reasoning in the learner ledger.
