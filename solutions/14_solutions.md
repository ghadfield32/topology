# Stage 14 conceptual solutions

Attempt the lesson questions first. These are answer criteria, not scores assigned to your work.

## 1. Explain the meaning of T_BA and compose T_CB with T_BA.

T_BA maps A coordinates into B. T_CB T_BA maps A into C, as the adjacent labels indicate.

## 2. Derive the rigid-transform inverse and camera-centre formula.

Solving p_B=Rp_A+t gives p_A=Rᵀp_B-Rᵀt. Setting p_camera=0 gives the world camera centre -Rᵀt.

## 3. Why is det R=+1 necessary in addition to RᵀR=I?

Orthogonality also permits reflections with determinant -1. Proper rotations preserve orientation.

## 4. Project (0.2,0.1,2) with f=800 and principal point (320,240).

u=800(0.2/2)+320=400 and v=800(0.1/2)+240=280.

## 5. Distinguish optical-axis depth, radial range, and disparity.

Z depth is the camera z coordinate; range is Euclidean distance to the centre; disparity is a difference of pixel columns in a rectified pair.

## 6. Explain which parameters must change when a calibrated image is cropped.

Pixel coordinates and intrinsics must use the cropping transform. Physical camera pose does not change; the exact convention of any resize must also be recorded.
