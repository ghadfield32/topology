# Stage 14 — Rotations, rigid transforms, and the camera model

A point must carry its frame, units, and projection convention.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 13.

## 1. Start with a coordinate frame
A coordinate frame specifies an origin and three directed axes. The same point has different numbers in two frames. The point does not move merely because we change its coordinates. Confusing an active motion of an object with a passive change of coordinates is a common source of inverses in the wrong place.

Our convention is explicit: `p_B = R_BA p_A + t_BA`, using column vectors. `T_BA` means “coordinates in B from coordinates in A.” The code stores N points as rows, so it calculates `points @ R.T + t`. The transpose is an implementation consequence of the table layout, not a different rotation convention.

## 2. Valid rotations cannot be arbitrary matrices
A proper three-dimensional rotation satisfies `RᵀR=I` and `det R=+1`. Orthogonality preserves dot products and lengths. The positive determinant excludes reflections. The set of these matrices is SO(3). Although a matrix contains nine entries, a rotation has three local degrees of freedom. [G02]

Take a quarter turn around z. It maps (1,0,0) to (0,1,0) in our right-handed convention. Apply a turn about x and then a turn about z; reverse their order. You will usually obtain different results. Matrix multiplication is not generally commutative.

## 3. From a local rotation vector to a valid matrix
A rotation vector w points along a rotation axis and has magnitude θ equal to the angle in radians. Define `[w]×` so that `[w]×v=w×v`. Rodrigues' formula is

```text
R = I + (sin θ / θ)[w]× + ((1-cos θ)/θ²)[w]×².
```

At zero, the limiting coefficients are 1 and 1/2. The implementation uses short Taylor expansions near zero to avoid numerical cancellation. You will compare it with SciPy's rotation-vector implementation and check both orthogonality and determinant. [G03]

A small update may be multiplied on the left or right; these express changes in different frames. Always name the convention. Adding independent values to nine matrix entries does not preserve SO(3).

## 4. Quaternions do not remove conventions
A unit quaternion is another rotation representation. q and -q describe the same rotation, so Euclidean differences between quaternion components can mislead. Libraries differ on scalar-first `(w,x,y,z)` versus scalar-last `(x,y,z,w)` ordering. Ceres explicitly distinguishes its quaternion layouts. [G04]

Our numerical labs use rotation matrices and vectors. The quaternion reading is a representation audit, not a claim that all quaternion conventions are interchangeable. For two valid rotations, the relative rotation angle can be computed from the trace of `R₁ᵀR₂`; clamp the cosine argument to [-1,1] for floating-point roundoff.

## 5. Translation and homogeneous transforms
A rigid transform belongs to SE(3) and can be written

```text
T_BA = [[R_BA, t_BA],
        [0 0 0, 1]].
```

Composition follows the labels: `T_CA = T_CB T_BA`. The inverse is `[[Rᵀ,-Rᵀt],[0,1]]`. Derive it by solving `p_B=Rp_A+t` for p_A. Translation is not simply negated unless the rotation is identity. [G05]

If a camera uses extrinsics `p_camera=R p_world+t`, its centre in world coordinates is `C=-Rᵀt`. The extrinsic translation is not the camera centre. The lab checks this relationship with a real benchmark-derived cloud and a deliberately chosen frame change.

## 6. The pinhole camera from similar triangles
A point with camera coordinates `(X,Y,Z)` and positive Z projects as

```text
u = fx X/Z + cx
v = fy Y/Z + cy.
```

The intrinsic matrix K contains focal lengths in pixels and a principal point. Here u means column and v means row. The camera axes are x right, y down, z forward. The matrix formula is `λ[u,v,1]ᵀ=K[X,Y,Z]ᵀ`. [G06]

Backprojection needs depth. If the depth means camera-axis Z, multiply `K⁻¹[u,v,1]ᵀ` by Z. If a sensor instead supplies radial distance to the camera centre, the ray must be normalized before multiplication. Interchanging those definitions creates systematic off-axis errors.

## 7. Pixels change when preprocessing changes
Cropping or resizing images changes pixel coordinates. For a declared image-coordinate affine map A, the corresponding intrinsics transform as `K′=AK`. Actual resizing libraries may use different pixel-centre conventions; record the precise transform, not just the new width. Extrinsics do not change merely because an image is cropped.

Lens distortion is separate from the ideal pinhole model. A raw fisheye image is not an undistorted pinhole image. Our reference pair is already rectified; the lab does not demonstrate raw-camera distortion calibration. The OpenCV calibration resource is the practical next reading for estimating intrinsic and distortion parameters. [G07]

## 8. The scale ambiguity you must remember
Projection of p and projection of sp agree for any positive scalar s. If camera translations and scene points scale together, the image evidence can remain identical. Recovering metre units needs an appropriate measured baseline, landmark distance, or another trusted scale cue. A predicted depth map is not a measured ruler.

## Independent conceptual exercises

1. Explain the meaning of T_BA and compose T_CB with T_BA.
2. Derive the rigid-transform inverse and camera-centre formula.
3. Why is det R=+1 necessary in addition to RᵀR=I?
4. Project (0.2,0.1,2) with f=800 and principal point (320,240).
5. Distinguish optical-axis depth, radial range, and disparity.
6. Explain which parameters must change when a calibrated image is cropped.

## Mastery gate

Demonstrate frame round trips and identify a projection ambiguity without a library.

Readings: G02, G03, G04, G05, G06, G07. See the [source ledger](../docs/SOURCES_V3.md) for checked links, evidence status and source differences.
