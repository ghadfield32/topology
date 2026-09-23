"""Exact/finite-difference reference operators and conservative graph examples."""
from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike
from .classical import finite


def heat_step(u: ArrayLike,nu: float,t: float,length: float=1.):
    u=finite(u);nu=float(finite(nu));t=float(finite(t));length=float(finite(length))
    if u.ndim<1 or u.shape[-1]<2 or nu<0 or t<0 or length<=0:raise ValueError('Invalid periodic heat parameters.')
    k=2*np.pi*np.fft.rfftfreq(u.shape[-1],d=length/u.shape[-1])
    return np.fft.irfft(np.fft.rfft(u,axis=-1)*np.exp(-nu*k*k*t),n=u.shape[-1],axis=-1)


def poisson_fd(n: int):
    """Solve -u''=pi² sin(pi x), zero endpoints, on n interior points."""
    if not isinstance(n,int) or not 1<=n<=2048:raise ValueError('Use 1–2048 interior points.')
    x=np.linspace(0,1,n+2);h=1/(n+1)
    from scipy.linalg import solve_banded
    A=np.zeros((3,n));A[0,1:]=-1;A[1]=2;A[2,:-1]=-1
    interior=solve_banded((1,1),A,h*h*np.pi**2*np.sin(np.pi*x[1:-1]))
    return x,np.r_[0,interior,0]


def pair_forces(X: ArrayLike,edges):
    """Undirected zero-rest-length Hooke interactions; each edge listed once."""
    X=finite(X)
    if X.ndim!=2 or 0 in X.shape:raise ValueError('Expected node coordinates [nodes,dimension].')
    F=np.zeros_like(X);seen=set()
    for i,j,k in edges:
        if not isinstance(i,int) or not isinstance(j,int) or i==j or min(i,j)<0 or max(i,j)>=len(X):
            raise ValueError('Invalid edge endpoints.')
        pair=tuple(sorted((i,j)))
        if pair in seen:raise ValueError('Duplicate undirected edge.')
        seen.add(pair);k=float(finite(k))
        if k<0:raise ValueError('Nonnegative stiffness required.')
        force=k*(X[j]-X[i]);F[i]+=force;F[j]-=force
    return F


def mean_correct(u: ArrayLike,target_mean: float):
    u=finite(u);target_mean=float(finite(target_mean))
    if u.size==0:raise ValueError('Nonempty array required.')
    return u-u.mean()+target_mean


def separable_grid(x_factors: ArrayLike,y_factors: ArrayLike):
    """Sum_r a_r(x)b_r(y). Axis evaluation can be small; output still nx*ny."""
    A=finite(x_factors);B=finite(y_factors)
    if A.ndim!=2 or B.ndim!=2 or A.shape[1]!=B.shape[1]:raise ValueError('Expected [nx,rank] and [ny,rank].')
    return A@B.T
