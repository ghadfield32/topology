# Stage 13 beginner workbook

## Work the same point in two coordinate systems
Start with p=(0.6,0,0.8). Its north coordinates are (3,0), while its south coordinates are (1/3,0). The numerical labels differ but the point does not. Apply both inverse maps and compare the recovered three numbers.

Now perturb north coordinates by (0.01,0). Does the same 0.01 increment in the south chart produce the same change on the sphere? No: coordinates are not automatically lengths. Compute the two resulting 3D changes. This is a concrete motivation for a metric tensor, whose full treatment is beyond the bridge.

## Predict, run, explain
Before running the lab, predict which pole gives large north-chart coordinates. Then plot the measured viewing directions in both charts. Read array shapes: N×3 directions become N×2 coordinates. Recover the original N×3 array and state what the maximum error measures.

## Debugging challenge
Replace `1-z` with `1+z` in only the forward north chart. Round-trip tests should fail. Explain why seeing an attractive scatterplot would not expose that error reliably.

## Deep route
Differentiate the inverse chart explicitly. Verify its two Jacobian columns are tangent by taking their dot products with the sphere point. Derive the transition Jacobian `I/q - 2aaᵀ/q²` away from a=0. Compare with a finite difference at a nonzero point. A successful check is local numerical evidence, not a theorem inferred from a plot.

## Three passes

**Understand:** work the hand example and identify an assumption. **Build:** run the worked lab, predict a change, and implement the coding exercises. **Demonstrate:** answer unfamiliar questions without the solutions and return for delayed recall. Passing reference code does not assess your understanding.
