# Stage 14 guided session — Make camera equations reversible only when the information exists

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/14_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/14_lab.ipynb). The [original workbook](../workbooks/14_workbook.md) and [worked lab](../notebooks/14_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real calibrated stereo-reference points plus a hand-checkable pinhole control.

## What you will be able to demonstrate

1. Name the source and destination frame of a rigid transformation.
2. Distinguish optical-axis depth from radial distance.
3. Project and unproject real reference points using the same calibration.
4. Explain why a round-trip check is not independent measurement validation.

## Coordinates belong to a frame
The same physical point has different coordinates in different frames. Write a rigid transformation as `p_B=R_BA p_A+t_BA`. The subscripts name where coordinates come from and where they go. With column vectors, composition is `T_CA=T_CB T_BA`: the rightmost transform acts first. Point tables in our NumPy implementation use row vectors, so the equivalent batch operation is `X @ R.T + t`.

A rotation must satisfy `R.T R=I` and determinant +1. Orthogonality alone allows reflections with determinant -1. A general matrix with nine freely fitted entries is not automatically a rotation. The course's rotation functions check these constraints rather than interpreting every three-by-three array as an orientation.

## Work one pinhole example
For a point `(X,Y,Z)` in the camera frame, with Z>0, the undistorted pinhole rule is `u=fx X/Z+cx` and `v=fy Y/Z+cy`. Let fx=fy=1000 pixels, principal point `(320,240)`, and point `(0.2,0.1,2)` metres. Its pixel is `(420,290)`.

The point `(0.4,0.2,4)` projects to the same pixel. Projection has lost range. With Z=2 supplied, unprojection returns the first point. With Z=4 supplied, it returns the second. The radial distance of the first point is `sqrt(0.2²+0.1²+2²)`, which is slightly larger than Z. Confusing radial range with optical-axis depth creates a systematic error away from the image center.

## Test what should be reversible
A rigid transform has an inverse: rotation transpose and translated origin `−R.T t`. Apply a transform and its inverse to real reference points and check their recovery. Then project those points and unproject with the same supplied Z. The coordinates should return within numerical tolerance.

These are consistency tests using the same assumptions in both directions. A wrong focal length used consistently can still make a project/unproject round trip pass. Independent calibration requires information not constructed by the same equations, such as appropriately separated measured landmarks or known held-out distances.

The real stereo pair is already rectified. These tests do not model lens distortion, rolling shutter, unsynchronized motion, or unknown camera calibration. Those are separate problems and the optional model workflow does not erase them. Always state which camera model, length unit, pixel convention, and timestamp apply before interpreting a reconstruction.

## Predict, execute, and explain

### Step 1

Use a hand-checkable pinhole example to expose ambiguity along one ray.

```python
from shape_lab.geometry import project, unproject, exp_so3, make_transform, transform_points, inverse_transform
K = np.array([[1000.,0,320],[0,1000,240],[0,0,1.]])
pair = np.array([[.2,.1,2.],[.4,.2,4.]])
uv, z = project(pair, K)
assert np.allclose(uv, [[420,290],[420,290]])
assert np.allclose(unproject(uv, z, K), pair)
print('same pixels, different depths:', uv, z)
```

### Step 2

Run the same consistency checks on a sample from the real stereo reference.

```python
from shape_lab.stereo import reference_sample, point_cloud
_, _, disparity, calibration = reference_sample()
X, rc = point_cloud(disparity, calibration, stride=60)
uv, z = project(X, calibration['K_left'])
assert np.allclose(uv, rc[:,::-1])
assert np.allclose(unproject(uv, z, calibration['K_left']), X)
T = make_transform(exp_so3([.1,-.2,.05]), [.3,.2,-.1])
restored = transform_points(inverse_transform(T), transform_points(T, X))
assert np.allclose(restored, X)
```

### Step 3

Report the numerical residual and the limits of the claim.

```python
result = {'reference_points': len(X),
          'rigid_round_trip_max_m': float(np.max(np.linalg.norm(restored-X, axis=1))),
          'projection_round_trip': 'passed', 'depth_type': 'optical-axis Z',
          'independent_calibration_validated': False}
```

## Transfer problems — attempt without the solution

### 14.T1

Can a wrong intrinsic matrix pass a project/unproject round trip?

<details><summary>Reveal reasoning after your attempt</summary>

Yes. Using the same invertible but incorrect matrix in both directions can cancel the error algebraically. Independent physical calibration needs separate evidence.

</details>

### 14.T2

What distinguishes a reflection matrix from a proper rotation when both satisfy R.T R=I?

<details><summary>Reveal reasoning after your attempt</summary>

Their determinants: a proper rotation has +1; a reflection-type orthogonal transform has -1 and reverses orientation.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/14_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
