# Stage 15 conceptual solutions

Attempt the lesson questions first. These are answer criteria, not scores assigned to your work.

## 1. Derive Z=fB/(d+doffs) from the two pixel equations.

Subtract the projections: d=fB/Z-doffs. Rearrangement gives d+doffs=fB/Z and therefore the stated expression.

## 2. Calculate why the principal-point offset cannot be omitted here.

For d=40, the denominators are 71.086 and 40. Omitting the offset enlarges the depth by a factor 71.086/40 for the same f and B.

## 3. Which inputs does the SAD predictor receive, and which are reserved for evaluation?

Images, pixel coordinates, patch radius and maximum disparity enter prediction. Reference disparity is supplied only afterward to the error calculation.

## 4. What is the difference between DLT and nonlinear reprojection refinement?

DLT solves homogeneous linear equations with an algebraic least-squares criterion. Refinement optimizes a chosen nonlinear residual, often image reprojection error.

## 5. Derive the local depth uncertainty for a fixed calibrated stereo model.

The derivative is -fB/(d+doffs)², giving the first-order standard-deviation approximation |derivative|σ_d under the stated fixed-parameter assumption.

## 6. Why does a low reprojection residual not establish correct synchronization or scale?

Geometry can fit an incorrectly scaled scene, and inconsistent timestamps can produce a different plausible geometry. Independent scale and timing evidence address claims the residual alone does not.
