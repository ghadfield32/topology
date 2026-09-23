# Evidence and uncertainty from zero

## A number needs an object, a unit, and a moment of availability

“30” could be a class code, a time in seconds, a strength in MPa or a row number. Before writing a model, say what it measures. A prediction-time feature must actually be available when the prediction is requested. The result of a laboratory test cannot quietly become an input to a model advertised as making a prediction before that test.

A label is not always a physical quantity. The Seeds integers 1, 2 and 3 are categories. Their ordering is not a measured distance. The Concrete Slump strength output is a physical response in MPa, so an error of 3 MPa has a unit; a classification error does not use the same measure.

## Mean, error, and a simple baseline

The mean of 20, 30 and 40 is 30. A constant predictor trained on those three outcomes predicts 30 for every future case. Its usefulness is not sophistication; it establishes what a method must improve upon. Fit it on the training outcomes, not all outcomes.

If predictions are 22, 25 and 43 for true values 20, 30 and 40, residuals y-prediction are -2, 5 and -3. Absolute errors are 2, 5 and 3. Mean absolute error is 10/3. Root mean squared error is sqrt((4+25+9)/3), about 3.559. Both keep the target's unit, but RMSE places greater emphasis on larger errors. Calculate them directly before importing a metric function.

A low average can hide a severe tail. Keep per-observation errors and report the denominator. For classification, 38 correct predictions out of 42 gives about 90.48%; the remaining four errors still need interpretation. Accuracy does not encode asymmetric costs or unknown population prevalence.

## Fitting and evaluation are different operations

Training chooses model parameters. Validation can choose hyperparameters or compare alternatives. Calibration, in the interval example, uses a fixed model's additional error observations to choose a radius. Testing evaluates the fixed procedure. Using the same outcomes repeatedly for all of those tasks can make a result look better than it generalizes.

A preprocessing mean is a fitted parameter. A selected persistence-image grid can also be fitted. A diagram threshold chosen after examining the final test labels is a selection decision. Write every such choice into the protocol. Use fixed choices for the small demonstration; use nested or otherwise appropriately separated selection when a real project requires tuning.

## Rank is not an interpolated quantile

Sort nine calibration errors [1,2,3,4,5,6,7,8,9]. At nominal error rate .2, the split-conformal order is ceil((9+1)×.8)=8, so choose error eight. This example defines an order statistic directly. A software quantile routine has a convention; interpolating between neighbors does not necessarily implement the intended rank.

A 99% nominal level would require rank ten, beyond the available nine errors. Our conservative construction returns infinity. It is deliberately uninformative rather than quietly reporting an unjustified finite endpoint. The function uses a decimal alpha contract to avoid an accidental ceiling jump caused only by binary floating-point representation.

## Where the coverage guarantee comes from

For a predictor fixed independently of calibration/test observations, assume their scores are exchangeable. Imagine sorting n calibration scores and one future score together. With no ties, the future score has a symmetric rank among n+1 positions. Choosing k=ceil((n+1)(1-alpha)) covers at least k/(n+1) of those ranks; conservative tie handling retains the lower-bound guarantee. This is a probability averaged over the sampling of calibration and future observations. It does not force every finite test set or every particular recipe to attain that fraction.

This is an original compact derivation and implementation guide for the split-conformal rank rule. The primary reference is Angelopoulos and Bates, [A Gentle Introduction to Conformal Prediction](https://arxiv.org/abs/2107.07511), particularly the coverage discussion and proof appendix. More advanced procedures for time dependence, group-specific guarantees or distribution shift require their own assumptions and constructions; the simple rule does not automatically solve those settings.

Randomly permuting rows is not proof of exchangeability. Hidden batches, families, patients, seasons or repeated experiments may remain dependent or shifted. In the concrete table, authenticated batch/time identities are absent. The interval lab demonstrates the method and its empirical result, not a guaranteed industrial recipe policy.

## Marginal, conditional and empirical are different words

Marginal coverage averages over a specified sampling process. Conditional coverage would condition on a feature value or subgroup; the simple marginal statement does not give all such guarantees. Empirical coverage is the fraction inside intervals in a particular finite sample. A test set of 26 has coarse steps of 1/26, about 3.85 percentage points. Observing 25/26 is not the same claim as a precisely known 96.15% future coverage probability.

Interval width measures how informative the set is. An infinite interval covers all finite outcomes but says almost nothing. Even a statistically valid procedure may be too broad for a useful decision. Describe both coverage and width, then seek domain-specific validation rather than certifying safety from this notebook.

## Correct rows can still leak information

Make two software copies of each of two kernels, giving rows A1,A2,B1,B2. Training on A1,B1 and testing on A2,B2 shares no row indices but shares both source kernels. An exact-copy nearest neighbor can look excellent without handling a new object. The manufactured-copy lab preserves source IDs so the problem is visible.

The appropriate group depends on the future question: kernel, plant, farm, patient, camera session or PDE initial condition. Grouping by source row cannot establish an unseen-farm evaluation when farm identities are absent. Time windows also have support intervals; overlapping inputs or future-derived labels can cross a nominal split.

## Keep four evidence levels visible

A source claim is what a post or paper asserts. A mathematical conclusion follows from a specified argument and assumptions. A computed result describes the implementation and experiment actually run. A deployment conclusion requires additional evidence about the intended environment and consequences. Do not replace any one with another.

Finish by explaining one example from each level. Then show how a result could be repeatable, numerically stable and still interpreted incorrectly. The methods case on source claims provides worked counterexamples rather than asking you to memorize a warning.
