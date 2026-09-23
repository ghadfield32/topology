# Materials case — A prediction needs an error range and a meaning

## Begin with the observation

A mixture is specified by quantities of ingredients. A laboratory test measures its responses. This source records 103 concrete-mixture tests with seven ingredient quantities and three outputs. Ingredients are given in kilograms in one cubic metre of concrete; slump and flow are centimetres; compressive strength is MPa at 28 days. This is the **Concrete Slump Test** dataset, not the separate 1,030-row concrete-strength dataset. [Provider and DOI](https://archive.ics.uci.edu/dataset/182/concrete+slump+test).

Our task is to predict the 28-day strength from the seven ingredients. The source row ID is an identifier, not an ingredient. Slump and flow are measured responses; they are excluded from the chosen pre-measurement prediction task. Including a column because it improves a score is not a substitute for establishing that it would be available at decision time.

## What a baseline means

A constant training-mean predictor ignores ingredients. It answers: how well can we do using only the typical training response? A ridge regression predicts an intercept plus a weighted sum of standardized ingredient quantities. Its penalty discourages very large fitted coefficients. Our fixed regularization value is 10, chosen for this teaching protocol before results are shown, not reported as optimal.

Suppose measured strengths are 20, 30 and 40, while a model predicts 22, 25 and 43. Absolute errors are 2, 5 and 3 MPa; their mean is 10/3 MPa. Squared-error metrics punish the error of five more strongly, but they answer a different question. We report MAE and RMSE with the target unit. Neither metric is a certification that a structure can safely use the material.

## Why training, calibration and testing are different

The lab uses a fixed random ordering: 52 training rows fit the scaler and model, 25 calibration rows set the error radius, and 26 test rows assess the fixed procedure. The model is not refitted after calibration. We do not reuse calibration rows for tuning the model or choosing the score. Test outcomes are used only for the final reported diagnostics.

The source describes 78 initial and 25 later observations, but the table does not supply authenticated dates or batch IDs. We therefore label the random mixture-level split as an educational protocol, not a proven temporal, new-batch or exchangeable deployment design. Randomly shuffling a dataset does not create independence that the collection process lacked.

## Derive the calibration radius by ranks

For the fitted predictor f, each calibration error is s_i = |y_i - f(x_i)|. At nominal error rate α, use the one-based rank

k = ceil((n_cal + 1)(1 - α)).

Sort calibration errors and take the k-th value. If k exceeds n_cal, use an infinite radius rather than inventing an unsupported finite extreme quantile. For n_cal=25 and α=0.1, k=24. Python's zero-based index is therefore 23. We select an order statistic directly; interpolating between values is not the same rule.

For a hand example with nine sorted errors 1,2,…,9 and α=0.2, k=ceil(10×0.8)=8. A prediction of 30 receives [22,38]. At α=0.1 the radius is nine. Requesting 99% nominal coverage with only nine calibration points needs rank ten and yields an uninformative infinite interval under this conservative construction. This illustrates a sample-size limitation, not a software failure.

Under exchangeability of calibration and future scores for a predictor fixed independently of them, the rank argument gives finite-sample **marginal** coverage. It does not say every recipe, subgroup or realized test set has exactly the nominal coverage. Distribution shift and dependent batches require additional reasoning. [Primary tutorial, including proof and limitations](https://arxiv.org/abs/2107.07511). This package adds the worked arithmetic and a real-data implementation; it does not reproduce that tutorial's experiments.

## Test usefulness as well as coverage

A radius of a million MPa would cover these observed outcomes but be useless. Report interval width alongside empirical coverage. Inspect errors for individual held-out mixtures, but label any subgroup discovered after looking at them as exploratory. Our symmetric intervals may have negative lower bounds; those are retained and discussed rather than silently clipped. Known physical constraints can justify a different set construction, but that choice must be stated before interpreting its coverage.

The notebook draws intervals centered on the fixed test predictions. The x-axis orders points by predicted strength, not time. Sorting for a plot is not a chronological analysis. It saves row IDs, predictions, bounds, coverage flags, calibration scores, rank and radius so you can verify the whole calculation.

## What you may conclude

You may report this model's errors and this interval procedure's empirical coverage on these declared rows. You may not infer engineering fitness, plant-wide safety, causal ingredient effects, or future-batch coverage from this example. A learned coefficient is not a controlled experimental intervention.

To pass, calculate an order statistic by hand, distinguish calibration from model fitting, trace one interval to its source row, explain marginal versus conditional coverage, and identify the batch information that an independent industrial study would need.

[Data card](../../data/v7/concrete_slump/metadata.json) · [Worked lab](lab.ipynb) · [Your coding exercises](learner.ipynb) · [Reference answers](answers.ipynb) · [Questions and answers](questions.md)
