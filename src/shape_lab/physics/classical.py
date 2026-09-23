"""Small exact examples. Ordering is always (q_1,...,q_d,p_1,...,p_d).

These routines demonstrate mathematical properties, not a calibrated model of
an athlete or the atmosphere. Every public routine rejects non-finite inputs.
"""
from __future__ import annotations
from collections.abc import Callable
import numpy as np
from numpy.typing import ArrayLike, NDArray


def finite(x: ArrayLike) -> NDArray[np.float64]:
    a=np.asarray(x,dtype=float)
    if not np.isfinite(a).all(): raise ValueError('Inputs must be finite.')
    return a


def canonical_matrix(d: int) -> NDArray:
    if not isinstance(d,int) or d<1: raise ValueError('Positive integer dimension required.')
    I=np.eye(d); Z=np.zeros((d,d))
    return np.block([[Z,I],[-I,Z]])


def symplectic_defect(M: ArrayLike) -> float:
    M=finite(M)
    if M.ndim!=2 or M.shape[0]!=M.shape[1] or M.shape[0]%2: raise ValueError('Even square matrix required.')
    J=canonical_matrix(M.shape[0]//2)
    return float(np.linalg.norm(M.T@J@M-J))


def energy(z: ArrayLike) -> NDArray | float:
    """Dimensionless unit-mass, unit-stiffness oscillator Hamiltonian."""
    z=finite(z)
    if z.ndim<1 or z.shape[-1]!=2: raise ValueError('Last axis must be (q,p).')
    return .5*np.sum(z*z,axis=-1)


def oscillator_matrix(h: float,method: str='exact') -> NDArray:
    h=float(finite(h))
    if method=='exact':return np.array([[np.cos(h),np.sin(h)],[-np.sin(h),np.cos(h)]])
    if method=='euler':return np.array([[1.,h],[-h,1.]])
    if method=='symplectic_euler':return np.array([[1-h*h,h],[-h,1.]])
    if method=='verlet':return np.array([[1-h*h/2,h],[-h*(1-h*h/4),1-h*h/2]])
    if method=='midpoint':
        A=canonical_matrix(1)
        return np.linalg.solve(np.eye(2)-.5*h*A,np.eye(2)+.5*h*A)
    raise ValueError('Use exact/euler/symplectic_euler/verlet/midpoint.')


def oscillator_rollout(z0: ArrayLike,h: float,steps: int,method: str='exact') -> NDArray:
    if not isinstance(steps,int) or not 0<=steps<=100000:raise ValueError('Use 0–100000 integer steps.')
    z0=finite(z0)
    if z0.shape!=(2,):raise ValueError('z0 must be a two-vector.')
    M=oscillator_matrix(h,method); out=np.empty((steps+1,2));out[0]=z0
    for i in range(steps):out[i+1]=M@out[i]
    if not np.isfinite(out).all():raise FloatingPointError('Rollout overflow; reduce horizon or step.')
    return out


def integrate_rk4(f: Callable,z0: ArrayLike,h: float,steps: int,t0: float=0.) -> NDArray:
    z=finite(z0).copy();h=float(finite(h));t=float(finite(t0))
    if z.ndim!=1 or not isinstance(steps,int) or not 0<=steps<=100000:raise ValueError('Use a vector and bounded integer steps.')
    out=[z.copy()]
    def rhs(t,z):
        a=finite(f(t,z))
        if a.shape!=z.shape:raise ValueError('Right-hand side changed the state shape.')
        return a
    for _ in range(steps):
        a=rhs(t,z);b=rhs(t+h/2,z+h*a/2);c=rhs(t+h/2,z+h*b/2);d=rhs(t+h,z+h*c)
        z=z+h*(a+2*b+2*c+d)/6;t+=h;out.append(z.copy())
    return finite(out)


def quadratic_flow(x: ArrayLike,t: float) -> NDArray:
    """Flow of x'=x², restricted to the connected maximal-time domain of x0."""
    x=finite(x); t=float(finite(t));den=1-t*x
    if np.any(den<=0):raise ValueError('Time crosses a finite-time singularity: require 1-t*x>0.')
    return x/den


def coupling(X: ArrayLike) -> tuple[NDArray,NDArray]:
    """Affine coupling F(x,y)=(x,exp(s(x))*y+b(x)); returns log |det DF|."""
    X=finite(X)
    if X.ndim!=2 or X.shape[1]!=2:raise ValueError('N by 2 array required.')
    s=.2*np.tanh(X[:,0]);b=.5*np.sin(X[:,0])
    return np.column_stack([X[:,0],np.exp(s)*X[:,1]+b]),s


def coupling_inverse(Y: ArrayLike) -> NDArray:
    Y=finite(Y)
    if Y.ndim!=2 or Y.shape[1]!=2:raise ValueError('N by 2 array required.')
    return np.column_stack([Y[:,0],(Y[:,1]-.5*np.sin(Y[:,0]))*np.exp(-.2*np.tanh(Y[:,0]))])
