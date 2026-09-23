# Stage 17 beginner workbook

## Work through registration logic
Take four non-collinear points. Apply a known rotation, scale and translation. Use three suitable points to estimate the transform, and evaluate the fourth. Then move only the fourth point. The training residual remains near zero but the held-out error grows. Explain why this is a useful adversarial example.

## Reconnect to Stage 08
Write down the unit-square Rips H₁ interval [1,sqrt(2)). Under scale 3 it becomes [3,3sqrt(2)). Under translation it does not change. Recover both facts numerically and then justify them directly from distances. No topology theorem needs to be guessed from those numerical checks.

## Real-data critique
The lab's cloud came from reference disparity. A transformed copy is not an independent sensor or model. Write that sentence in your results before discussing the residual. This small provenance statement prevents an algebra exercise from being misremembered as successful learned reconstruction.

## Deep route
Derive the centring step and the formula `t=mean(y)-sR mean(x)`. Explain why a reflection must be excluded for camera-frame alignment. Design a failure case in which low nearest-neighbour error hides wrong correspondence. Choose a metric that reveals it.

## Three passes

**Understand:** work the hand example and identify an assumption. **Build:** run the worked lab, predict a change, and implement the coding exercises. **Demonstrate:** answer unfamiliar questions without the solutions and return for delayed recall. Passing reference code does not assess your understanding.
