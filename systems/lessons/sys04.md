# sys04 — OpenCV and native computer vision
**Source:** Stage 4. **Prerequisites:** topology geometry Stages 14/15; C++/Python boundary sys02/03.

## Explain the image before the camera
An image has height, width, channel order, dtype and row stride. `cv::Mat` can be a view over another matrix; a rectangular ROI often retains its parent's stride. Its rows need not form one contiguous packed buffer. `clone()` creates owned storage. The Python/OpenCV side checks the same issue with a sliced NumPy image. A correct shape is not enough to establish correct storage or color interpretation.

A world point first changes coordinate frame: Xc=R Xw+t. Perspective projection divides by camera depth. With no distortion, u=fx*Xc/Zc+cx and v=fy*Yc/Zc+cy. Multiple points along one ray can project to the same pixel, so the camera is not a globally invertible chart of the scene. Distortion adds a separate lens model. PnP estimates pose from 3D–2D correspondences under specified intrinsics; triangulation estimates a 3D point from multiple rays, with degenerate/noisy arrangements still possible.

## Implemented checks
`systems/python/opencv_probe.py` loads the retained stereo image and checks a strided ROI against its contiguous copy. A manufactured point (1,2,10) with fx=fy=800 and principal point (320,240) projects to (400,400). The C++ `opencv_probe.cpp` performs the corresponding memory/projection checks when OpenCV development headers and libraries are installed.

Python's `cv2` wheel does not imply that your compiler has the C++ development package. The CMake target uses `find_package(OpenCV REQUIRED COMPONENTS core calib3d)` and must stop if unavailable. In this build the Python side executed, while the C++ development dependency was missing. That is not called cross-language OpenCV agreement.

## Predict, break and apply
Calculate the manufactured pixel by hand. Change focal length, principal point and point depth separately and predict each result. Change the ROI's parent width and inspect stride. Never flatten a strided buffer by assuming width*channels bytes when step says otherwise. Invalid depths and calibration-unit mismatches belong in explicit tests.

Next use the existing Stage 15 stereo experiment for observed imagery and supplied disparity references; do not rebuild a new stereo curriculum here. Record camera conventions, baselines, principal-point offsets, eligible pixels and failures. Feature matching, PnP and triangulation on independent surveyed references are later project obligations. A low reprojection error alone does not certify metric scale or unobserved geometry.

## Exit gate
Explain Mat ownership/view behavior, channels and stride; derive projection; identify information lost through a camera; build both optional paths before claiming equivalence; and distinguish manufactured camera controls from real calibration recovery.
