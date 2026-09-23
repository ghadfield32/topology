"""Small, inspectable geometry algorithms for the teaching labs.

Column-vector convention: p_destination = R_destination_source p_source + t.
Point tables use rows, so the vectorized implementation is X @ R.T + t.
Rotations are right-handed; angles are radians; length units come from inputs.
This is not a camera calibration or uncertainty certification service.
"""
from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike, NDArray


def _array(a: ArrayLike, columns: int) -> NDArray[np.float64]:
    x=np.asarray(a,dtype=float)
    if x.ndim!=2 or x.shape[1]!=columns or not np.isfinite(x).all():
        raise ValueError(f'Expected a finite N by {columns} array.')
    return x


def sphere_chart(points: ArrayLike, pole: str='north') -> NDArray[np.float64]:
    """Stereographic chart on S² minus the named pole. Output has two coordinates."""
    p=_array(points,3)
    if pole not in {'north','south'}:raise ValueError('Choose north or south.')
    if not np.allclose(np.linalg.norm(p,axis=1),1,atol=1e-8,rtol=0):
        raise ValueError('Points must lie on the unit sphere.')
    denominator=1-p[:,2] if pole=='north' else 1+p[:,2]
    if np.any(denominator<=1e-12):raise ValueError('This chart excludes its pole; use the other chart.')
    return p[:,:2]/denominator[:,None]


def sphere_unchart(coordinates: ArrayLike, pole: str='north') -> NDArray[np.float64]:
    a=_array(coordinates,2)
    if pole not in {'north','south'}:raise ValueError('Choose north or south.')
    q=(a*a).sum(axis=1);z=(q-1)/(q+1)
    if pole=='south':z=-z
    return np.column_stack((2*a/(q+1)[:,None],z))


def skew(vector: ArrayLike) -> NDArray[np.float64]:
    v=np.asarray(vector,dtype=float)
    if v.shape!=(3,) or not np.isfinite(v).all():raise ValueError('Expected a finite length-3 vector.')
    x,y,z=v
    return np.array([[0,-z,y],[z,0,-x],[-y,x,0.]])


def exp_so3(rotation_vector: ArrayLike) -> NDArray[np.float64]:
    """Rodrigues exponential exp([w]x), with small-angle series near zero."""
    w=np.asarray(rotation_vector,dtype=float);a=skew(w);theta=np.linalg.norm(w)
    if theta<1e-6:
        t2=theta*theta;s=1-t2/6+t2*t2/120;c=.5-t2/24+t2*t2/720
    else:s=np.sin(theta)/theta;c=(1-np.cos(theta))/(theta*theta)
    return np.eye(3)+s*a+c*(a@a)


def _rotation(r: ArrayLike) -> NDArray[np.float64]:
    r=np.asarray(r,dtype=float)
    if r.shape!=(3,3) or not np.isfinite(r).all() or not np.allclose(r.T@r,np.eye(3),atol=1e-7,rtol=0) or not np.isclose(np.linalg.det(r),1,atol=1e-7,rtol=0):
        raise ValueError('Expected a proper rotation: R.T R = I and det R = +1.')
    return r


def make_transform(rotation: ArrayLike, translation: ArrayLike) -> NDArray[np.float64]:
    r=_rotation(rotation);t=np.asarray(translation,dtype=float)
    if t.shape!=(3,) or not np.isfinite(t).all():raise ValueError('Translation must be a finite length-3 vector.')
    out=np.eye(4);out[:3,:3]=r;out[:3,3]=t
    return out


def _transform(t: ArrayLike) -> NDArray[np.float64]:
    t=np.asarray(t,dtype=float)
    if t.shape!=(4,4) or not np.allclose(t[3],[0,0,0,1],atol=1e-12,rtol=0):raise ValueError('Expected a 4 by 4 rigid transform.')
    _rotation(t[:3,:3])
    if not np.isfinite(t).all():raise ValueError('Transform must be finite.')
    return t


def transform_points(transform: ArrayLike, points: ArrayLike) -> NDArray[np.float64]:
    t=_transform(transform);p=_array(points,3)
    return p@t[:3,:3].T+t[:3,3]


def inverse_transform(transform: ArrayLike) -> NDArray[np.float64]:
    t=_transform(transform);r=t[:3,:3]
    return make_transform(r.T,-r.T@t[:3,3])


def _intrinsics(k: ArrayLike) -> NDArray[np.float64]:
    k=np.asarray(k,dtype=float)
    if k.shape!=(3,3) or not np.isfinite(k).all() or k[0,0]<=0 or k[1,1]<=0 or not np.allclose(k[2],[0,0,1]) or abs(np.linalg.det(k))<1e-12:
        raise ValueError('Expected a finite invertible pinhole intrinsic matrix.')
    return k


def project(camera_points: ArrayLike, intrinsics: ArrayLike) -> tuple[NDArray,NDArray]:
    """Undistorted pinhole projection. Reject points on or behind the focal plane."""
    p=_array(camera_points,3);k=_intrinsics(intrinsics)
    if np.any(p[:,2]<=0):raise ValueError('Every projected point must have positive camera Z.')
    h=p@k.T
    return h[:,:2]/h[:,2,None],p[:,2].copy()


def unproject(pixels_uv: ArrayLike, depth_z: ArrayLike, intrinsics: ArrayLike) -> NDArray:
    """Backproject optical-axis depth Z (not radial range) into the camera frame."""
    uv=_array(pixels_uv,2);z=np.asarray(depth_z,dtype=float);k=_intrinsics(intrinsics)
    if z.shape!=(len(uv),) or not np.isfinite(z).all() or np.any(z<=0):raise ValueError('One finite positive Z depth is required per pixel.')
    rays=np.column_stack((uv,np.ones(len(uv))))@np.linalg.inv(k).T
    return rays*z[:,None]


def triangulate_dlt(p1: ArrayLike,p2: ArrayLike,uv1: ArrayLike,uv2: ArrayLike) -> NDArray:
    """Linear DLT from matching undistorted pixels and 3x4 projection matrices.

    Solves an algebraic least-squares objective, not a full reprojection-error
    optimization. Callers must separately check cheirality and uncertainty.
    """
    a=np.asarray(p1,float);b=np.asarray(p2,float);x=_array(uv1,2);y=_array(uv2,2)
    if a.shape!=(3,4) or b.shape!=(3,4) or not np.isfinite(a).all() or not np.isfinite(b).all() or x.shape!=y.shape:
        raise ValueError('Need two finite 3x4 matrices and paired N by 2 observations.')
    if np.linalg.matrix_rank(a)<3 or np.linalg.matrix_rank(b)<3:raise ValueError('Projection matrices must have rank 3.')
    out=[]
    for u,v in zip(x,y):
        rows=np.stack([u[0]*a[2]-a[0],u[1]*a[2]-a[1],v[0]*b[2]-b[0],v[1]*b[2]-b[1]])
        if np.linalg.matrix_rank(rows)<3:raise ValueError('Degenerate rays do not determine a unique finite point.')
        _,_,vh=np.linalg.svd(rows);h=vh[-1]
        if abs(h[3])<1e-12:raise ValueError('Triangulated point is at or too near infinity.')
        out.append(h[:3]/h[3])
    return np.asarray(out,dtype=float).reshape(-1,3)


def fit_similarity(source: ArrayLike,target: ArrayLike) -> tuple[float,NDArray,NDArray]:
    """Fit Y = s X R.T + t to known paired references, with s>0 and det R=+1.

    No correspondence discovery, robust outlier removal or holdout selection.
    Non-collinear paired anchors are required. Fit only on registration anchors.
    """
    x=_array(source,3);y=_array(target,3)
    if x.shape!=y.shape or len(x)<3:raise ValueError('At least three paired 3D points are required.')
    xc=x-x.mean(0);yc=y-y.mean(0)
    if np.linalg.matrix_rank(xc)<2 or np.linalg.matrix_rank(yc)<2:raise ValueError('Registration anchors must not be collinear.')
    h=yc.T@xc/len(x);u,d,vh=np.linalg.svd(h)
    signs=np.ones(3);signs[-1]=np.linalg.det(u@vh)
    r=u@np.diag(signs)@vh
    s=float(np.dot(d,signs)/np.mean((xc*xc).sum(1)))
    if s<=0:raise ValueError('Positive scene scale could not be estimated.')
    t=y.mean(0)-s*r@x.mean(0)
    return s,r,t


def rotation_error_deg(a: ArrayLike,b: ArrayLike) -> float:
    r=_rotation(a).T@_rotation(b)
    return float(np.degrees(np.arccos(np.clip((np.trace(r)-1)/2,-1,1))))


def finite_jacobian(function,point: ArrayLike,step: float=1e-6) -> NDArray:
    """Central finite difference. Agreement is numerical evidence, not a proof."""
    x=np.asarray(point,float)
    if x.ndim!=1 or not np.isfinite(x).all() or not np.isfinite(step) or step<=0:raise ValueError('Finite vector and positive step required.')
    columns=[]
    for j in range(len(x)):
        e=np.zeros_like(x);e[j]=step
        columns.append((np.atleast_1d(function(x+e))-np.atleast_1d(function(x-e)))/(2*step))
    return np.column_stack(columns)
