# Calculus for geometry — begin with a change you can measure

## Why you need this primer
A position tells you where an object is. A derivative tells you how its position changes. A Jacobian tells you how several outputs change when several inputs move. We need those ideas to understand tangent vectors, camera sensitivity, and optimization. You do not need to complete an entire analysis textbook before this course, but you must distinguish a definition, a numerical approximation, and a physical assumption.

## 1. A function is a rule, not necessarily a formula
Suppose an ideal object travels according to `x(t)=t²` metres, where t is seconds. At t=2 it is at 4 metres. Between t=2 and t=2.1 its displacement is 0.41 metres, so its average speed over that interval is 4.1 metres per second. The quotient is `(x(t+h)-x(t))/h`.

For this particular function, `( (t+h)² - t² ) / h = 2t+h` for nonzero h. As h approaches zero, that expression approaches 2t. The derivative is therefore `x′(t)=2t`. We have derived the answer algebraically rather than guessed it from a graph. At t=2 the instantaneous velocity is 4 metres per second.

A derivative is a limit. Evaluating one very small h on a computer is an approximation. If h is too large, curvature contaminates the estimate; if it is extremely small, subtracting nearly equal floating-point numbers loses information. Try h values 10⁻¹ through 10⁻¹² and compare to a known analytic derivative before trusting a numerical result.

```python
import numpy as np
f = lambda t: np.sin(t)
t = 0.4
for h in [1e-1, 1e-3, 1e-5, 1e-7, 1e-10]:
    numerical = (f(t+h)-f(t-h))/(2*h)
    print(h, numerical, abs(numerical-np.cos(t)))
```

## 2. Vectors change too
A curve `p(t)=(x(t),y(t),z(t))` has derivative `p′(t)=(x′(t),y′(t),z′(t))`. Each component is differentiated. Its derivative is a tangent vector to the curve. The curve may be restricted to a surface even though its coordinates use three numbers.

For the unit circle, `p(t)=(cos t,sin t)` and `p′(t)=(-sin t,cos t)`. Their dot product is zero. The position points away from the centre; the instantaneous change points along the circle. Moving a finite distance along the straight tangent line leaves the circle. A tangent is a local linear approximation, not the surface itself.

## 3. Partial derivatives and the Jacobian
For a function with several inputs, a partial derivative changes one input while holding the others fixed. If `f(x,y)=x²+y`, the partial derivatives are `∂f/∂x=2x` and `∂f/∂y=1`.

For several outputs, place those derivatives in a matrix. If `F(x,y)=(x²+y,sin y)`, then

```text
J_F(x,y) = [[2x, 1],
            [ 0, cos y]]
```

Rows correspond to outputs; columns correspond to inputs. Near x, a small input change δ gives `F(x+δ) ≈ F(x)+J_F(x)δ`. The approximation need not remain accurate for a large δ.

In a pinhole camera, `u=f X/Z+cx`. Holding f and cx fixed gives `∂u/∂X=f/Z`, `∂u/∂Y=0`, and `∂u/∂Z=-f X/Z²`. Moving the same distance has a different pixel effect at different depths. A sensitivity matrix depends on the point where it is evaluated.

## 4. Chain rule: conversions compose
If y=F(x) and z=G(y), then `J_(G∘F)(x)=J_G(F(x)) J_F(x)` wherever the derivatives exist. Check dimensions before multiplying. An n-dimensional input, m-dimensional intermediate value, and k-dimensional output give matrix shapes `(k,m) @ (m,n) -> (k,n)`.

This is why a chart transition, camera transform, and projection cannot be rearranged casually. The functions must compose in a meaningful order, and their derivatives follow that same dependency.

## 5. Least squares and uncertainty are different questions
Least squares chooses parameters to reduce a sum of squared residuals, such as predicted pixels minus observed pixels. A low training residual does not prove that the camera has correct metric scale, that its parameters are identifiable, or that an independent measurement will agree. Multiple parameter settings can explain the same observations.

For small random input error δ with covariance Σ, the local linear approximation predicts output covariance `J Σ Jᵀ`. This propagation is exact for a linear map and approximate for a nonlinear map. It assumes the relevant error sources and their correlations have been represented. An omitted synchronization error does not magically appear in the covariance.

## 6. Minimum mastery check
Derive the derivative of t² from its difference quotient. Differentiate each component of a circular trajectory. Explain the dimensions of a Jacobian. Derive the three pixel sensitivities above. Explain why a numerical derivative check is not a proof of differentiability. State one reason why small reprojection error can coexist with wrong physical scale.

For a deeper course, use MIT OpenCourseWare 18.02SC Multivariable Calculus. This primer is original explanatory material; it is not that course's notes. Continue to Stage 13 after you can perform the componentwise calculations.
