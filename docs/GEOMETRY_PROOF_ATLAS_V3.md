# Geometry proof atlas and depth obligations

This supplements the original [proof atlas](PROOF_ATLAS.md). Numerical tests support implementation correctness; the arguments below establish exact identities under their assumptions.

## 1. Sphere chart inverse
Let q=a²+b², x=2a/(1+q), y=2b/(1+q), z=(q-1)/(q+1). Then x²+y²+z²=[4q+(q-1)²]/(1+q)²=1. Also 1-z=2/(1+q), so x/(1-z)=a and y/(1-z)=b. Conversely, substituting chart coordinates of a sphere point away from the north pole recovers it. The denominator never vanishes for finite (a,b), so the inverse is smooth. Repeat with the opposite sign of z for the other chart.

## 2. Transition map on the overlap
For a north-chart coordinate u=(a,b), q=||u||². On the two-chart overlap q>0, because q=0 represents the south pole, which the south chart excludes. Substituting the north inverse into (x/(1+z),y/(1+z)) gives u/q. Applying the same map again returns u. Every component is a rational function with nonzero denominator on this domain, hence smooth. This proves smooth compatibility for these charts, not for every possible chart family.

## 3. Sphere tangent plane
For a differentiable curve p(t) on the unit sphere, differentiate p(t)·p(t)=1 to obtain p(t)·p′(t)=0. Conversely, at a unit point p and vector v perpendicular to p, the curve c(t)=(p+tv)/||p+tv|| is defined near zero, lies on the sphere and has c(0)=p and c′(0)=v. Thus tangent vectors are exactly the perpendicular plane. The Jacobian of a chart inverse maps coordinate velocities into this plane.

## 4. Skew generators and proper rotations
For a skew-symmetric A, exp(A)ᵀ=exp(Aᵀ)=exp(-A), so exp(A)ᵀexp(A)=I. The determinant of exp(tA) is continuous in t, is always ±1 by orthogonality and equals +1 at t=0; it therefore remains +1. For A=[w]× and theta=||w||, the identity A³=-theta²A groups the exponential power series into Rodrigues' formula. The code uses series coefficients near theta=0 to avoid cancellation; it does not divide by theta there.

## 5. Rigid inverse
Multiply [[R,t],[0,1]] by [[Rᵀ,-Rᵀt],[0,1]]. Its upper-left block is RRᵀ=I and its upper-right block is -RRᵀt+t=0. Multiplication in the other order gives the same identity. This derivation requires orthogonal R; the implementation additionally requires det R=+1 for a proper rigid transform.

## 6. Pinhole depth ambiguity
In normalized camera coordinates, projection maps (X,Y,Z) to (X/Z,Y/Z). For every positive a, the point (aX,aY,aZ) has the same projection. Thus one ideal pixel ray alone does not determine depth. Learned priors can select a prediction, but they do not make the underlying observation-to-scene map injective.

## 7. Rectified stereo formula with unequal principal points
For parallel rectified cameras separated by B along x, uL=fX/Z+cxL and uR=f(X-B)/Z+cxR. Subtraction gives d=fB/Z-(cxR-cxL). Writing doffs=cxR-cxL gives Z=fB/(d+doffs), provided the denominator is positive in the front-facing convention. The baseline unit becomes the depth unit. This argument assumes the rectified pinhole model and does not remove distortion from raw photographs.

## 8. Conditional local uncertainty
For Z(d)=fB/(d+doffs), dZ/dd=-fB/(d+doffs)². Linearizing a small zero-mean disparity perturbation yields Var(Z) approximately [fB/(d+doffs)²]² Var(d). Taking square roots gives the SD expression used in the lab. With uncertain calibration or correlated parameters, use a larger Jacobian and covariance: J Sigma Jᵀ. Finite perturbations, biased estimates and model mismatch are outside this one-variable approximation.

## 9. Attention normalization and masking
Subtracting a constant c from every score in a row multiplies numerator and denominator of softmax by exp(-c), leaving weights unchanged. Taking c as the row maximum improves numerical stability. An allowed-position mask sets disallowed weights to zero and normalizes over allowed positions. An entirely masked row has no valid normalization and is rejected. These facts establish an averaging operator, not its ability to infer geometry.

## 10. Similarities and the Rips filtration
A proper rigid transform preserves all Euclidean pairwise distances, so every labeled simplex enters a Rips filtration at the same threshold. A positive uniform scale s multiplies every edge length by s; the maximum edge length of each simplex is also multiplied by s. Under this relabeling of filtration parameter, birth and death coordinates scale by s. This says nothing about invariance under arbitrary non-isometric deformations or changing the sample IDs.

## 11. Prefix causality
The event algorithm updates its state only from observations at or before the current index. Once a decision record is emitted it is not rewritten. By induction on the processed prefix length, processing a prefix yields exactly the decisions from the full sequence whose decision index lies in that prefix. Onset may be earlier than the decision. Missing data resets relevant evidence under this particular policy. The proof is about information availability, not physical event truth.

## Deeper study boundaries
A full theory of smooth manifolds, Riemannian geometry, Lie algebras, bundle adjustment, observability, stochastic estimation, transformer training and dynamic-scene reconstruction is not silently declared complete. For this continuation, you should derive the identities above, state their assumptions, inspect numerical failures and defend an independent analysis. Use the primary source ledger for deeper readings. Full proofs of the spectral/optimization/statistical results behind advanced solvers, and actual model training, are separate extension projects.
