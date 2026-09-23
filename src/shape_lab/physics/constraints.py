"""Constraint corrections; no assertion that arbitrary projections are symplectic."""
from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike
from .classical import finite


def constraint_correction(z: ArrayLike,C: ArrayLike,A: ArrayLike):
    """One linearized minimum-norm correction; A is DC(z), not symplectic J."""
    z=finite(z);C=finite(C);A=finite(A)
    if z.ndim!=1 or C.ndim!=1 or A.shape!=(len(C),len(z)) or len(C)<1:
        raise ValueError('Expected z[n], C[m], DC[m,n].')
    if np.linalg.matrix_rank(A)<len(C):raise ValueError('Constraint Jacobian is not full row rank.')
    return z-A.T@np.linalg.solve(A@A.T,C)


def project_affine(z: ArrayLike,A: ArrayLike,b: ArrayLike):
    z=finite(z);A=finite(A);b=finite(b)
    if A.ndim!=2 or z.ndim!=1 or b.ndim!=1 or A.shape!=(len(b),len(z)):
        raise ValueError('Incompatible affine constraint dimensions.')
    return constraint_correction(z,A@z-b,A)


def project_sphere(z: ArrayLike,tol: float=1e-12,max_iter: int=40):
    z=finite(z).copy()
    if z.ndim!=1 or len(z)<2 or not np.isfinite(tol) or tol<=0 or max_iter<1:raise ValueError('Invalid sphere projection parameters.')
    if np.linalg.norm(z)==0:raise ValueError('Sphere constraint has a rank-zero Jacobian at the origin.')
    history=[]
    for _ in range(max_iter):
        r=float(z@z-1);history.append(abs(r))
        if abs(r)<=tol:return z,history
        z=constraint_correction(z,[r],2*z[None,:])
    raise RuntimeError('Projection did not converge to the requested residual tolerance.')


def sphere_retraction(q: ArrayLike,v: ArrayLike):
    q=finite(q);v=finite(v)
    if q.ndim!=1 or q.shape!=v.shape or not np.isclose(q@q,1) or not np.isclose(q@v,0):
        raise ValueError('q must be unit length and v tangent at q.')
    z=q+v
    return z/np.linalg.norm(z)
