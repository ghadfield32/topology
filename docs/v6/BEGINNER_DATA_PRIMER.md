# From a table to a defensible experiment

This primer is a bridge, not a prerequisite exam. Read one section when a case uses an unfamiliar word. The original eight mathematical primers remain available in `foundations/`.

## 1. Start with one observation

A table has rows and columns. A row is a storage choice; an **observation unit** says what that row represents in the world. These are not always the same thing. In the transport example four rows describe four choices offered to the same traveler. There are 840 stored alternatives but 210 traveler-level examples. In the marine table one row stores a whole year; twelve columns contain twelve monthly temperatures. Reshaping produces 732 monthly values, not 732 new measurements on top of the original values.

Write this sentence before doing mathematics: “One prediction will be made for ____ using information available at ____.” If you cannot fill it in, you do not yet have a prediction task. It is still possible to explore the data; label that exploration honestly.

A **feature** is an input used to describe an example. A **target** is the outcome you intend to predict. A **group** joins related examples, such as one patient, one athlete, one firm, or one experiment. A **timestamp** describes when an observation applies. Its **availability time** describes when someone could actually have known it. A year-end measurement cannot be used as if it were known at the start of that year.

The data cards document these roles. They also state when a role or unit is unknown. Unknown is useful information: it prevents us from presenting an encoded quantity as an accurately calibrated physical measurement.

## 2. Arrays and shapes without mystery

A NumPy array with shape `(100, 3)` has 100 rows and three columns. By convention in these labs rows represent examples and columns represent features. `x[5]` selects one row; `x[:, 2]` selects the third column. Python indexing starts at zero. `x[[1, 4, 9]]` selects three specified rows. `x.mean(axis=0)` averages down rows and returns one mean per feature. `axis=1` averages across features instead; it answers a different question.

Read every array's shape out loud. If `x` is `(100,3)` and a vector of means is `(3,)`, subtracting those means broadcasts one three-element vector across every row. It does not subtract each example's own mean. The distinction matters for both units and leakage.

A missing numeric value is represented by `NaN`. It is not zero, and it is not a special physical measurement. Some operations propagate it; others skip it. The environmental lab deliberately keeps missing slots, rejects unsupported windows, and records which rows survive. Inspect the denominator of every reported metric.

## 3. Means, scales, and what distance means

For numbers 2, 4, and 6, the mean is `(2+4+6)/3 = 4`. The population standard deviation is `sqrt(((2-4)^2+(4-4)^2+(6-4)^2)/3) = sqrt(8/3)`. Our scaler uses this population convention, `ddof=0`. A sample standard deviation uses another denominator; neither choice should be left implicit.

Standardization converts a feature value `x` to `(x - mean_training) / std_training`. If the training values are 1 and 3, their mean is 2 and their population standard deviation is 1. The standardized values are -1 and 1. A later value 101 becomes 99. It must not change the training mean to make itself look ordinary.

For a constant training column we use a scale of one after subtracting its constant mean. We do not divide by zero. This is a numerical convention, not new information.

Euclidean distance is the square root of the sum of squared coordinate differences. Combining temperature, money and a label code in one distance without thought is not meaningful. A cultivar code of 2 is not physically twice cultivar 1. Standardizing measurable features creates a deliberate relative scale, but it does not establish a unique correct geometry. Correlated or repeated features can still be counted several times. Try adding a duplicate column in a training-only experiment and inspect the change.

## 4. Training, validation, and testing

The training set determines fitted parameters, including preprocessing and reference points. The validation set supports choices such as regularization strength or a decision threshold. A test set is used after the procedure is fixed to estimate performance for the declared population and split design.

In these worked labs the models and main parameters are fixed before the test is displayed. The results are educational demonstrations. Once you have read the outputs, the displayed partition is **exposed**. Repeatedly trying changes until its score improves is not a new independent confirmation.

Split the independent unit. For a new-patient claim, split patients. For a future-time claim, hold out later times. For a new-site claim, hold out sites. If the snapshot has no patient or site identifiers, say that the intended claim is unverified; random row splitting does not create the missing identifiers.

A strict time-window split assigns all measurements contributing to a window and its target to the same partition. This package uses that conservative rule for its new scalar-series labs. It drops some otherwise usable boundary examples. An operational protocol can allow earlier observed history to seed the first future prediction, but that needs a different explicit policy—not an accidental overlap.

## 5. What the models actually do

A linear regression predicts `b + w1*x1 + ... + wp*xp`. Training chooses weights to reduce prediction error on training observations. A ridge regression adds a penalty proportional to the sum of squared weights. It is a regularized predictor, not a physical equation merely because the output has physical units.

A binary logistic model first computes a linear score `s`, then converts it to `1/(1+exp(-s))`. At `s=0` the result is 0.5. The number is a model probability under its fitted assumptions, not a universal guarantee about a future individual. A threshold turns it into a yes/no prediction. We use a fixed 0.5 threshold for the healthcare demonstration, with no recommendation to use it clinically.

For multiple categories, the model produces one probability per category and they sum to one. It predicts the category with largest probability. A multiclass model of a traveler's complete feature vector is not the same statistical model as a conditional-logit choice model over alternatives. This course labels its simpler construction rather than borrowing a more sophisticated name.

## 6. Measure error in understandable units

Suppose the observed values are `[10,12]` and predictions are `[11,8]`. Errors are `[1,-4]`. Mean absolute error is `(1+4)/2 = 2.5`. Root mean squared error is `sqrt((1+16)/2) = sqrt(8.5)`, about 2.915. Both retain the target's unit; RMSE gives larger errors more influence. A negative prediction can still be physically impossible even when average error is small. Add a domain check instead of hiding that problem inside a mean.

Accuracy is the number of correct classifications divided by the number evaluated. If 95 of 100 examples belong to one class, always predicting that class obtains 95% accuracy while missing the other class entirely. **Balanced accuracy** averages recall across classes. Recall for a class is the fraction of its actual examples found. A binary confusion matrix records true-negative, false-positive, false-negative, and true-positive counts under an explicit class order. Changing which class is “positive” changes interpretation.

ROC AUC summarizes ranking behavior across thresholds. It does not establish good probability calibration or a useful operational threshold. A calibration claim needs additional evaluation, an appropriate population, and enough data. In healthcare it also needs clinical and safety review well beyond this course.

A baseline is a deliberately simple rule: last reading, training mean, training-majority class, or a calendar-month average. A complex model that does not improve the relevant baseline may still teach you something, but complexity is not itself a result.

## 7. Build shape at the right level

A row containing thirteen chemistry measurements is a point in a chosen thirteen-dimensional feature space. A collection of rows forms a point cloud. The topology of that cloud is not automatically a property of each individual row.

To produce a per-query descriptor, the wine lab defines a reference cloud from training rows, selects the eight closest reference observations to a new query, and computes a small filtration on those nine points. It records exactly which rows formed the reference and reserves different training rows for fitting the classifier. Query observations never silently join the reference pool.

The resulting descriptor has six entries: three summaries of finite H0 lifetimes, the number of positive finite H1 intervals, and the maximum and total H1 lifetime. The small complexes include triangles, so triangular loops may be filled. H0 can be independently checked with a minimum spanning tree. Essential classes, coefficient field, zero-lifetime conventions, distance scale and maximum simplex dimension are all part of the calculation.

This is an engineered feature, not an assertion that a wine has six intrinsic topological properties. Its value must be compared with simpler features on the same fitting and evaluation examples.

## 8. Time windows, horizons, and future information

For observations `[a,b,c,d,e]`, a length-three window `[a,b,c]` with horizon two predicts `e`, not `d`. Its last feature occurs at position two; its target is at position four. Changing `e` must not change `[a,b,c]`. The unit tests check this contract.

A **rolling one-step** test allows each later prediction to use earlier actual readings that have already arrived. A **free-running rollout** feeds the model's own predictions back as future inputs. These differ fundamentally. Strong one-step performance cannot be presented as proof of stable long rollouts.

A delay embedding uses several past values as coordinates. Repetition can create loop-like geometry. The general conditions for recovering an underlying dynamical system are substantive mathematical assumptions; a noisy, seasonally forced scalar dataset does not prove them by producing an attractive plot.

## 9. Why real observations and manufactured controls coexist

Real datasets show missingness, incomplete metadata, dependence, sampling bias, and model mismatch. Manufactured problems let us know exact answers, such as a sphere constraint, a harmonic oscillator, or a prescribed PDE solution. They serve complementary roles.

A neural network trained on simulated heat fields has executed a learning experiment, but it has not been validated on a real building. An observed temperature series does not supply every boundary condition required by the heat equation. Your four source posts are retained as claims in the earlier source audit; the new industry observations do not retroactively verify those claims.

Keep four labels separate: source statement, mathematical result under stated assumptions, our executed experiment, and an untested application proposal. These labels are more informative than calling everything “physics informed.”

## 10. Finish with an evidence file

For one experiment, write: question; observation unit; data version and hash; features available at prediction time; independent unit and split; fitted transforms; baseline; model; metrics and denominators; surprising errors; limits; next experiment. Link the output CSV and code you actually ran.

A passing software test means the asserted property held for its tested inputs. It does not mean you understand its proof, that all cases are covered, or that a system is safe to deploy. An assessment asks you to explain and transfer the idea without copying. A delayed assessment asks whether you retained it. Preserve both kinds of evidence.

**Mini-check:** explain why 840 alternatives can yield 210 predictions, why a missing CO2 value is not zero, why a test-set mean is not a training parameter, and why a persistence loop is not a diagnosis. Then open the first case that matches your current stage.
