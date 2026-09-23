# Stage 14 coding solutions

Attempt your learner notebook before opening this file.

## 14.C1 — rigid_inverse

Invert a valid 4×4 rigid transform without using a generic matrix inverse. Inputs in this exercise are already valid rigid transforms.

**Hint:** Transpose R and use -Rᵀt.

```python
def rigid_inverse(transform):
    T=np.asarray(transform,float);out=np.eye(4)
    out[:3,:3]=T[:3,:3].T
    out[:3,3]=-T[:3,:3].T@T[:3,3]
    return out
```

Using -t alone would be wrong unless the rotation leaves that translation unchanged. The full module additionally validates the input transform.

### Checks

```python
from shape_lab.geometry import make_transform,exp_so3
T=make_transform(exp_so3([.2,-.1,.4]),[1,2,3])
assert np.allclose(rigid_inverse(T)@T,np.eye(4))
assert np.allclose(T@rigid_inverse(T),np.eye(4))
```

## 14.C2 — backproject_z

Backproject finite Nx2 pixels and positive camera-axis Z values using an invertible calibrated K. Return camera-frame Nx3 points.

**Hint:** Multiply homogeneous pixels by K inverse, then scale rays to the supplied Z.

```python
def backproject_z(pixels, depths, intrinsics):
    uv=np.asarray(pixels,float);z=np.asarray(depths,float);K=np.asarray(intrinsics,float)
    if uv.ndim!=2 or uv.shape[1]!=2 or z.shape!=(len(uv),) or not np.isfinite(uv).all() or not np.isfinite(z).all() or np.any(z<=0):raise ValueError("Finite pixels and positive Z required.")
    rays=np.column_stack([uv,np.ones(len(uv))])@np.linalg.inv(K).T
    if np.any(np.abs(rays[:,2])<1e-12):raise ValueError("Invalid ray normalization.")
    return rays*(z/rays[:,2])[:,None]
```

Axis depth differs from radial range away from the optical axis. This function does not undistort a raw image.

### Checks

```python
K=np.array([[100,0,50],[0,100,40],[0,0,1.]])
X=backproject_z([[50,40],[100,40]],[2,2],K)
assert np.allclose(X,[[0,0,2],[1,0,2]])
assert not np.allclose(np.linalg.norm(X,axis=1),[2,2])
```

## 14.C3 — proper_rotation

Return a boolean indicating whether a finite 3×3 matrix is a proper rotation to an explicit numerical tolerance.

**Hint:** Both orthogonality and determinant +1 are needed.

```python
def proper_rotation(matrix, atol=1e-8):
    R=np.asarray(matrix,float)
    return bool(R.shape==(3,3) and np.isfinite(R).all() and np.allclose(R.T@R,np.eye(3),atol=atol,rtol=0) and np.isclose(np.linalg.det(R),1,atol=atol,rtol=0))
```

A reflection is orthogonal but has determinant -1. Tolerance-based checking is numerical validation, not a symbolic proof.

### Checks

```python
assert proper_rotation(np.eye(3))
assert not proper_rotation(np.diag([1,1,-1]))
assert not proper_rotation(np.ones((3,3)))
assert not proper_rotation(np.eye(2))
```