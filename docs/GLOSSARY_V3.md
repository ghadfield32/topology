# Geometry glossary — use with the core glossary

**Chart:** a homeomorphism from an open part of a manifold to an open subset of Euclidean space. It is a local coordinate system, not necessarily a camera image.

**Atlas:** a collection of charts covering a manifold. A smooth atlas has smooth transitions on overlaps.

**Tangent vector:** the derivative at a point of a curve through that point, expressed in an appropriate local representation. It represents local motion, not a second point.

**Jacobian:** a matrix of first derivatives expressing a local linear response of outputs to small input changes. Its numerical values depend on coordinates and units.

**SO(3):** the group of real 3×3 orthogonal matrices with determinant +1, representing proper rotations in three dimensions.

**SE(3):** the group of proper rigid motions formed by a rotation and translation. Homogeneous 4×4 matrices encode composition and inversion.

**Quaternion:** a four-component rotation representation subject to unit norm; q and -q represent the same 3D rotation. Library component order must be checked.

**World-to-camera transform:** a map taking coordinates in the chosen world frame to camera-frame coordinates. Its translation column is not generally the world-frame camera center.

**Intrinsic matrix:** a pinhole-camera matrix converting normalized camera coordinates into image coordinates, with focal lengths and principal point in pixels. Distortion and preprocessing require their own treatment.

**Extrinsics:** a rotation and translation defining the relationship between camera and reference frames. Direction conventions must be stated.

**Principal point:** the pixel location of the camera optical-axis projection in the chosen idealized image model. It need not coincide exactly with the array center.

**Rectification:** image transformation that organizes corresponding epipolar lines, commonly into matching rows. Already rectified data does not mean the course estimated rectification.

**Disparity:** horizontal coordinate difference u_left-u_right in the convention used here. Depth also depends on focal length, baseline and the principal-point difference.

**Axis depth:** the Z component in a camera frame. **Range** is Euclidean distance to the camera center; these differ away from the optical axis.

**Baseline:** camera-center separation. A baseline in metres contributes metric information; an unscaled learned translation does not supply measured metres.

**Triangulation:** estimating a 3D point from multiple camera observations and a camera model. Poor geometry, mismatch, timing and noise affect its reliability.

**Cheirality:** the requirement that a reconstructed point lies in front of the relevant cameras under the adopted convention. Small algebraic residual alone does not ensure this.

**Gauge freedom:** a transformation of scene/camera parameters that preserves the observations available to the problem. Extra metric or orientation evidence can fix some freedoms.

**Observability:** whether the available observations constrain a parameter or state distinction. A prior can select an estimate without creating independent observational evidence.

**Similarity registration:** fitting a positive scale, proper rotation and translation to align known correspondences. Fitted anchors and evaluation references must be distinguished.

**Reprojection residual:** image-coordinate difference between an observation and a projected estimate. It is not automatically a metric-distance error or synchronization certificate.

**Holdout:** evidence reserved from fitting and selection for a specified evaluation. Disjoint row IDs alone do not guarantee independent people, scenes or sessions.

**Attention:** weighted aggregation of value vectors based on query/key relationships. A mathematical attention operation alone is not a trained geometric model.

**Frame attention:** in the original VGGT description, token interaction restricted within a frame. **Global attention** permits interaction across frames. These are model-specific design descriptions, not general guarantees of correspondence.

**Point map:** a 3D vector assigned to an image-grid location in a declared reference frame. It can be a model prediction and need not be metric truth.

**Track:** an identified sequence of corresponding observations. Original VGGT's optional track output is 2D image coordinates; 3D trajectory claims need additional geometry and timing evidence.

**Confidence score:** a model-dependent score. Unless calibrated for a stated event, it should not be interpreted as the probability of metric correctness.

**Throughput:** completed work per unit time. **Latency:** duration between explicitly identified input/output boundaries. **Age:** elapsed time since the relevant observation was captured; queued results may be old despite fast final-stage inference.

**Causal detector:** one whose output at a decision time uses only observations available by that time. An earlier estimated onset does not imply the decision was available then.

**Contact hypothesis:** a tentative statement about physical interaction. Proximity, smoothing or temporal consistency alone does not establish observed contact.

**Reference-derived:** calculated from a supplied benchmark reference, such as disparity and calibration. It is not necessarily a separately measured physical holdout.

Definitions align with the primary resources identified in [Sources v3](SOURCES_V3.md); the source ledger separates mathematical background from model-specific conventions.
