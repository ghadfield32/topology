# Stage 13 — From topology to smooth manifolds

Local coordinates, tangent directions, and why a camera image is not a global chart.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 01, Stage 02, Stage 03, Stage 04.

## 1. What changes after the topology course?
Topology asks which properties are preserved by an appropriate continuous equivalence. Smooth geometry adds a way to differentiate. A distance or Riemannian metric adds measurements of length and angle. These are related structures, not interchangeable words.

Picture the Earth's surface without assuming geography knowledge: near a point on a sphere, a small patch behaves like a two-dimensional sheet. A single global flat coordinate map cannot describe that entire sphere as one open subset of the plane. Several overlapping patches solve the problem. We do not cut the object into disconnected physical pieces; we change the way we label points.

A topological n-manifold, in the convention used here, is Hausdorff, second countable, and locally homeomorphic to open subsets of Rⁿ. The local requirement explains dimension; the two global conditions rule out pathological spaces. Manifolds with boundary have a different local half-space model. A point cloud from a sensor is not automatically a manifold simply because a smooth surface is an attractive explanation for it.

## 2. Charts and atlases from zero
A chart `(U, φ)` consists of an open region U of the manifold and a homeomorphism φ from U onto an open subset of Rⁿ. Its output is a list of coordinates. An atlas is a collection of charts whose regions cover the manifold.

On an overlap, the same physical point p has two coordinate descriptions: a=φ(p) and b=ψ(p). To convert a into b, first undo φ and then apply ψ:

```text
b = ψ(φ⁻¹(a))
ψ ∘ φ⁻¹ : φ(U ∩ V) → ψ(U ∩ V)
```

The domains matter. This formula is not defined for arbitrary points outside the overlap. A smooth atlas requires smooth transition maps. A smooth structure can be described using a maximal compatible smooth atlas. These definitions are the mathematical foundation of the chart-transition exercise, not a claim about a learned embedding. [G01]

## 3. An explicit sphere calculation
Let p=(x,y,z) be on the unit sphere `x²+y²+z²=1`. Remove the north pole `(0,0,1)`. The north-pole stereographic chart is

```text
φ_N(p) = (x/(1-z), y/(1-z)).
```

For a=(u,v), write q=u²+v². The inverse is

```text
φ_N⁻¹(a) = (2u/(1+q), 2v/(1+q), (q-1)/(1+q)).
```

Check the formula rather than memorize it. The squared norm of the numerator is `4q+(q-1)²=(q+1)²`, so its output lies on the sphere. Substitution into the chart returns u and v. The denominator `1+q` is positive everywhere. The north pole never appears for a finite a, exactly as the chart definition requires.

The south-pole chart uses denominator `1+z` and its inverse negates the final coordinate above. On the overlap, `φ_S(φ_N⁻¹(a))=a/||a||²`, with a≠0. Derive that cancellation by hand. The origin in the north chart describes the south pole, which is excluded by the south chart.

## 4. Tangent vectors are constrained local changes
If a differentiable curve p(t) stays on the sphere, differentiate `p(t)ᵀp(t)=1`. The result is `2p(t)ᵀp′(t)=0`. Thus a tangent vector at p is orthogonal to p:

```text
T_p S² = {v in R³ : pᵀv = 0}.
```

For nonzero tangent v, the curve `cos(t||v||)p + sin(t||v||)v/||v||` remains on the sphere and has initial derivative v. This also shows why the stated tangent plane contains all permissible initial directions, not merely some of them.

A local derivative needs a chart or an equivalent embedded calculation. Our lab compares analytic derivatives to finite differences. That comparison catches coding errors; it does not replace the analytic reasoning or prove smoothness for every input.

## 5. Use the real stereo data without changing its meaning
The notebook turns benchmark-derived 3D points into unit viewing directions `p/||p||`. These directions lie on a sphere by construction. You will map them between charts and recover them. You will also see why a chart near its excluded pole can become numerically awkward.

This does not prove that the original scene is spherical. Normalization deliberately removes distance along the ray. Two objects at different ranges can yield the same direction. The calculation is a real-data example of a coordinate representation, not a discovery of scene topology.

## 6. Why an image is not generally a chart of the whole scene
Perspective projection sends `(X,Y,Z)` to quantities involving X/Z and Y/Z. Multiplying all three coordinates by the same positive number gives the same pixel. Therefore the map is not one-to-one over a three-dimensional scene. Occlusion and limited field of view lose still more information.

A camera may parameterize a suitable visible surface patch under additional conditions, but ordinary projection is not an invertible chart of arbitrary 3D space. Neither manifold terminology nor a transformer removes this ambiguity.

## 7. Keep the hierarchy clear
A topological manifold supplies local topological coordinates. A smooth structure permits derivatives. A Riemannian metric measures tangent-vector lengths. A Lie group combines smooth structure with compatible group operations. Stage 14 uses this last idea for rotations. There is no need to implement a general manifold library before you understand the explicit sphere example.

## Independent conceptual exercises

1. Define a chart, an atlas, and the domain of a transition map.
2. Compute the two chart coordinates of (0.6,0,0.8) and invert them.
3. Prove that the inverse stereographic formula lies on the unit sphere.
4. Derive the equation pᵀv=0 for tangent vectors.
5. Why does normalizing a real point cloud to unit vectors discard depth?
6. Explain why perspective projection is not generally a chart of 3D space.

## Mastery gate

Independently derive a chart round trip and explain the information normalization removes.

Readings: G01, G02. See the [source ledger](../docs/SOURCES_V3.md) for checked links, evidence status and source differences.
