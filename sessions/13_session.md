# Stage 13 guided session — A chart changes coordinates, not the underlying point

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/13_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/13_lab.ipynb). The [original workbook](../workbooks/13_workbook.md) and [worked lab](../notebooks/13_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real stereo-reference directions mapped onto a constructed unit sphere; not a spherical scene claim.

## What you will be able to demonstrate

1. Write the domain restriction of a stereographic chart.
2. Check that chart-to-space-to-chart returns the same point.
3. Construct a tangent vector by removing its radial component.
4. Explain why normalizing scene points does not prove a spherical physical scene.

## What local coordinates buy us
A smooth manifold is locally modeled by ordinary Euclidean coordinates, with smoothly compatible transitions where coordinate patches overlap. A chart maps a patch of the manifold to an open subset of coordinate space. It is not merely any feature extractor: invertibility on the patch and compatibility with the chosen structure matter.

For the unit sphere, stereographic projection from the north pole sends `(x,y,z)` to `(x/(1−z), y/(1−z))`. The north pole is excluded because the denominator is zero. A south-pole chart covers the other missing point. One formula need not work everywhere for the manifold to be well defined.

## Derive a chart transition
If a north-chart coordinate is u=(a,b) and `q=a²+b²`, the reconstructed sphere point is `(2a/(q+1), 2b/(q+1), (q−1)/(q+1))`. Applying the south chart gives `(a/q,b/q)`. This transition excludes q=0, corresponding to the point absent from the overlap. It maps different numerical coordinates to the same sphere point.

The denominator is not an annoying coding detail. It specifies the domain on which the mathematical statement is valid. Near a chart's excluded pole, coordinates can become large even though neighboring sphere points remain nearby in three-dimensional space. Coordinate conditioning and physical proximity are not identical.

## Tangent directions satisfy a constraint
The sphere satisfies `p·p=1`. Differentiate along a curve p(t): `2p·p'=0`. Therefore a tangent velocity v at p is orthogonal to p. Starting with any vector a, remove its radial component: `v=a−(a·p)p`. Then `p·v=0` for a unit p. This is an exact derivation, not a rule inferred from a scatter plot.

## Use real scene data without inventing a manifold claim
The stereo reference supplies reconstructed scene points under its documented calibration. Normalize selected nonzero vectors to unit length; this constructs their directions on the sphere. It deliberately discards range. The experiment tests coordinate changes for those directions, not whether the original scene itself is a sphere or a smooth two-dimensional manifold everywhere.

A camera image also discards depth along viewing rays. It is not generally an invertible chart of an entire three-dimensional scene. This distinction prevents the useful chart analogy from turning into an incorrect reconstruction argument. The next stage develops projection and unprojection with explicit depth and coordinate-frame conventions.

## Predict, execute, and explain

### Step 1

Convert real reference scene points into unit directions, explicitly discarding range.

```python
from shape_lab.stereo import reference_sample, point_cloud
from shape_lab.geometry import sphere_chart, sphere_unchart
_, _, disparity, calibration = reference_sample()
points, rc = point_cloud(disparity, calibration, stride=50)
p = points/np.linalg.norm(points, axis=1, keepdims=True)
p = p[np.abs(p[:,2]) < .99][:40]
assert len(p)>3
print('unit directions:', len(p))
```

### Step 2

Use both charts and recover the same sphere point.

```python
north = sphere_chart(p, 'north'); south = sphere_chart(p, 'south')
assert np.allclose(sphere_unchart(north, 'north'), p)
assert np.allclose(sphere_unchart(south, 'south'), p)
q = np.sum(north*north, axis=1)
assert np.allclose(north/q[:,None], south)
print('maximum round-trip error:', np.max(np.abs(sphere_unchart(north, 'north')-p)))
```

### Step 3

Project arbitrary vectors onto the tangent planes and verify their radial component vanishes.

```python
a = np.random.default_rng(1304).normal(size=p.shape)
v = a - np.sum(a*p, axis=1)[:,None]*p
residual = float(np.max(np.abs(np.sum(p*v, axis=1))))
assert residual < 1e-12
result = {'direction_count': len(p), 'chart_round_trip': 'passed',
          'tangent_orthogonality_max': residual, 'range_retained': False,
          'physical_scene_is_sphere_claimed': False}
```

## Transfer problems — attempt without the solution

### 13.T1

Why does a normalized point cloud lying on S2 not prove that the original scene lay on a sphere?

<details><summary>Reveal reasoning after your attempt</summary>

Normalization constructs unit directions and removes each point’s range. It maps many different physical points on a ray to the same direction.

</details>

### 13.T2

Show that v=a−(a·p)p is tangent at a unit p.

<details><summary>Reveal reasoning after your attempt</summary>

Take the dot product with p: p·v=p·a−(a·p)(p·p)=0 because p·p=1. This matches the derivative of the sphere constraint.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/13_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
