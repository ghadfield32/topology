# Sources, attribution and evidence status — version 3

Web sources below were inspected on **September 20, 2026**. URLs pointing to `main`, `stable` or `rolling` can change. A future model run must record the exact code revision and checkpoint hash, not cite this retrieval date as a version lock.

## U01 — User-supplied WMS geometry and CV discussion

[User-supplied WMS geometry and CV discussion](../sources/user_supplied_geometry_context.md)

User-provided context, preserved unchanged. Statements about prior watches are historical source statements; no watch was modified during this build. Industry benchmarks and contact claims remain unverified unless separately identified.

## T01 — ETH Zürich Introduction to Topological Data Analysis, 2026

[ETH Zürich Introduction to Topological Data Analysis, 2026](https://ti.inf.ethz.ch/ew/courses/TDA26/index.html)

Primary free course. Core mathematical foundations, homology, persistence, point-cloud complexes, stability and Mapper. Existing core lessons retain their own source ledger.

## T02 — Raphaël Tinarrage: TDA with Persistent Homology

[Raphaël Tinarrage: TDA with Persistent Homology](https://raphaeltinarrage.github.io/EMAp.html)

Primary teaching course: lectures, exercises and practical tutorials. Use as the main guided external sequence, not an additional mandatory full textbook.

## G01 — Manifolds.jl: atlases and charts

[Manifolds.jl: atlases and charts](https://juliamanifolds.github.io/Manifolds.jl/stable/features/atlases/)

Primary documentation for chart transitions and derivatives. The course sphere-chart examples and proofs are original derivations, not executed Julia code.

## G02 — Modern Robotics: rotation matrices

[Modern Robotics: rotation matrices](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-2-1-rotation-matrices-part-1-of-2/)

Primary free video/text introduction to SO(3). Learn representation constraints before treating rotations as matrix entries.

## G03 — SciPy Rotation reference

[SciPy Rotation reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html)

Official API reference. Our Rodrigues implementation is compared with the locally installed SciPy; the web latest version is not assumed installed.

## G04 — Ceres Solver: manifolds and quaternion conventions

[Ceres Solver: manifolds and quaternion conventions](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html)

Official documentation. Local parameterization/manifold interfaces and quaternion storage conventions. No Ceres optimization was executed here.

## G05 — Modern Robotics: homogeneous transforms

[Modern Robotics: homogeneous transforms](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/)

Primary free explanation of frame transforms, composition and inversion.

## G06 — OpenCV camera-calibration and 3D-reconstruction reference

[OpenCV camera-calibration and 3D-reconstruction reference](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)

Official reference for projection, intrinsics, distortion, calibration and triangulation. OpenCV triangulation crosscheck runs only when the locally available library is present; check the test report.

## G07 — OpenCV camera-calibration tutorial

[OpenCV camera-calibration tutorial](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)

Official practical route for real board calibration. The notebook linear known-camera-coordinate example is not a substitute for full calibration, distortion fitting or capture-quality control.

## D04 — scikit-image stereo_motorcycle dataset documentation

[scikit-image stereo_motorcycle dataset documentation](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.stereo_motorcycle)

Primary package documentation for the local downsampled Middlebury images, disparity and calibration. Runtime observed image arrays (500,741,3), disparity (500,741). The page documents a disparity shape with an extra channel; this discrepancy is stated rather than copied into code.

## D05 — Middlebury 2014 scene calibration documentation

[Middlebury 2014 scene calibration documentation](https://vision.middlebury.edu/stereo/data/scenes2014/)

Primary source for doffs=cx_right-cx_left, baseline units and Z=fB/(d+doffs). Raw reference includes nonfinite entries; actual loaded contents determine masks.

## D06 — scikit-image license

[scikit-image license](https://scikit-image.org/docs/stable/license.html)

Official package license page. The locally installed distribution license and data provenance are retained in data/stereo. No new blanket rights claim is made for arbitrary external datasets.

## V01 — VGGT official project

[VGGT official project](https://vgg-t.github.io/)

Primary project overview. The architecture connects within-frame and cross-frame evidence; proposed sector uses are not accepted as application validation.

## V02 — Original VGGT paper, version 1

[Original VGGT paper, version 1](https://arxiv.org/html/2503.11651v1)

Primary paper. First-camera geometry convention, scale normalization, centered-principal-point assumption, architecture and limitations. These statements apply to the cited original paper, not automatically to successors.

## V03 — Original VGGT model output contract

[Original VGGT model output contract](https://github.com/facebookresearch/vggt/blob/main/vggt/models/vggt.py)

Official source inspected 2026-09-20. RGB input, camera encoding, depth, point maps and optional 2D image tracks. Our adapter is source-reviewed and shape-tested with synthetic fixtures; trained inference was not executed.

## V04 — Original VGGT repository README

[Original VGGT repository README](https://github.com/facebookresearch/vggt/blob/main/README.md)

Primary setup, camera conventions and licensing guidance. Code and checkpoint permissions differ; the separate commercial checkpoint is not interchangeable licensing evidence for the original weights. Review exact files and weights at the revision used.

## V05 — VGGT-Omega official project

[VGGT-Omega official project](https://vggt-omega.github.io/)

Primary successor project. Register-based exchange and reduced training memory are reported by authors, not reproduced here. Project update is dated September 18, 2026.

## V06 — VGGT-Omega official repository

[VGGT-Omega official repository](https://github.com/facebookresearch/vggt-omega)

Primary code and checkpoint guidance. README dates the training/reproduction announcement September 8, 2026, unlike the project site. This date disagreement remains unresolved in this package. Omega uses a separate API and is not accepted by the original-VGGT adapter.

## V07 — Original VGGT preprocessing source

[Original VGGT preprocessing source](https://github.com/facebookresearch/vggt/blob/main/vggt/utils/load_fn.py)

Official crop/pad preprocessing implementation, including dimension adjustments. Processed pixels must not be joined directly to raw reference pixels without a checked mapping.

## V08 — Original VGGT pose decoding source

[Original VGGT pose decoding source](https://github.com/facebookresearch/vggt/blob/main/vggt/utils/pose_enc.py)

Official camera-encoding conversion used by the optional original-model adapter.

## S01 — ROS2 sensor_msgs_py point-cloud utilities

[ROS2 sensor_msgs_py point-cloud utilities](https://github.com/ros2/common_interfaces/blob/rolling/sensor_msgs_py/sensor_msgs_py/point_cloud2.py)

Primary structured-array and equally-typed-array access. Adopt the data-layout lesson, not a claim of executing ROS2 or PointPillars in this course.

## S02 — PyTorch CUDA synchronization

[PyTorch CUDA synchronization](https://docs.pytorch.org/docs/2.14/generated/torch.cuda.synchronize.html)

Official device synchronization reference for measuring completed GPU work. CUDA timing is not executed by the CPU teaching labs.

## S03 — PyTorch local checkpoint loading

[PyTorch local checkpoint loading](https://docs.pytorch.org/docs/2.14/generated/torch.load.html)

Official torch.load reference; restricted weights_only loading is used, without silently enabling unrestricted pickle fallback. A trusted local file and exact code revision are still required.

## Evidence labels used throughout
**Source-derived:** attributed to the supplied document, paper, official documentation or dataset provider. **Derived mathematics:** our worked algebra under stated assumptions; elementary proofs are provided. **Executed experiment:** outputs actually computed from the bundled arrays or clearly identified generated controls. **Proposed experiment:** instructions for future execution, never populated with invented measurements.

## Specific discrepancies and boundaries
The user-supplied source reports the Omega announcement on September 18. The official project page agrees; the official README says September 8. We preserve both, without guessing which is the underlying release date. A checkpoint must be identified by hash/revision and intended benchmark role.

The scikit-image page's declared disparity shape includes a third dimension, while the actual provided disparity array is two-dimensional. The loader and tests use the observed shape. The raw array contains NaN and positive infinity; these are explicitly excluded from numerical depth calculations.

Reported ROS2 and PointPillars timing numbers and human-object interaction prototype observations in the supplied text were not reproduced. They motivate profiling and event-validation exercises, not claims about this package's hardware or basketball accuracy.

No actual book text was acquired or audited. The retained book-coverage map follows the supplied contents only. External books, videos, papers, official model code and model weights are linked rather than redistributed.

## Free resource route
For topology, use Tinarrage as the primary teaching sequence and ETH as the formal reference. The original sources ledger links proof, linear algebra and topology texts. For geometry, use Modern Robotics for transforms, the Ceres docs for local parameterizations and OpenCV for calibration. Read the original VGGT paper only after projection, calibration and uncertainty are intelligible. Treat Omega as a subsequent research-comparison exercise, not a prerequisite to understanding shape.
