"""Inspectable single-process representation-learning mathematics.

Original educational implementation, not the official LeJEPA package. The fixed
frequency grid is quadrature, not a calibrated statistical hypothesis test.
No function silently normalizes away the mean/variance that SIGReg should see.
"""
from __future__ import annotations
import numpy as np


def matrix(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 2 or min(x.shape) < 1 or x.shape[0] < 2 or not np.isfinite(x).all():
        raise ValueError('Need a finite N by D matrix, N >= 2 and D >= 1.')
    return x


def covariance(x: np.ndarray) -> np.ndarray:
    x = matrix(x)
    c = x - x.mean(axis=0)
    return c.T @ c / (len(x) - 1)


def fit_whitener(x: np.ndarray, relative_tolerance: float = 1e-10) -> tuple[np.ndarray, np.ndarray]:
    """Fit full-rank ZCA whitening on training data only (sample covariance)."""
    x = matrix(x)
    if relative_tolerance <= 0:
        raise ValueError('Tolerance must be positive.')
    values, vectors = np.linalg.eigh(covariance(x))
    if values.min() <= relative_tolerance * max(float(values.max()), 1.):
        raise ValueError('Covariance is rank deficient or ill-conditioned; choose a lower-dimensional model explicitly.')
    return x.mean(axis=0), (vectors * (1 / np.sqrt(values))) @ vectors.T


def effective_rank(x: np.ndarray) -> float:
    """Entropy effective rank of sample covariance; the constant cloud has rank 0."""
    values = np.maximum(np.linalg.eigvalsh(covariance(x)), 0)
    if values.sum() <= np.finfo(float).tiny:
        return 0.
    p = values / values.sum()
    p = p[p > 1e-15]
    return float(np.exp(-np.sum(p * np.log(p))))


def unit_directions(dimension: int, count: int, seed: int) -> np.ndarray:
    if dimension < 1 or count < 1:
        raise ValueError('Dimension and direction count must be positive.')
    a = np.random.default_rng(seed).normal(size=(dimension, count))
    return a / np.linalg.norm(a, axis=0, keepdims=True)


def empirical_cf(samples: np.ndarray, frequencies: np.ndarray) -> np.ndarray:
    x, t = np.asarray(samples, float), np.asarray(frequencies, float)
    if x.ndim != 1 or not len(x) or t.ndim != 1 or not np.isfinite(x).all() or not np.isfinite(t).all():
        raise ValueError('Finite one-dimensional samples and frequency grid required.')
    return np.exp(1j * x[:, None] * t[None, :]).mean(axis=0)


def projected_gaussian_score(z: np.ndarray, directions: np.ndarray,
                             frequencies: np.ndarray | None = None) -> float:
    """N * average_a integral |ECF_a(t)-exp(-t²/2)|² exp(-t²/2) dt.

    Default 17 equally spaced frequencies in [-5,5]. Check finer grids when
    comparing values. This finite score is neither a p-value nor a proof of normality.
    """
    z = matrix(z)
    a = np.asarray(directions, float)
    if a.ndim != 2 or a.shape[0] != z.shape[1] or a.shape[1] < 1 or not np.isfinite(a).all():
        raise ValueError('Directions must be a finite D by M matrix.')
    if not np.allclose(np.linalg.norm(a, axis=0), 1, atol=1e-8):
        raise ValueError('Every projection direction must have unit norm.')
    t = np.linspace(-5, 5, 17) if frequencies is None else np.asarray(frequencies, float)
    if t.ndim != 1 or len(t) < 2 or not np.isfinite(t).all() or not np.all(np.diff(t) > 0):
        raise ValueError('Frequencies must be a finite strictly increasing grid.')
    phase = (z @ a)[:, :, None] * t[None, None, :]
    real = np.cos(phase).mean(axis=0)
    imag = np.sin(phase).mean(axis=0)
    target = np.exp(-.5 * t * t)
    discrepancy = ((real - target)**2 + imag**2) * target
    return float(len(z) * np.trapezoid(discrepancy, t, axis=-1).mean())


def epps_pulley_exact(x: np.ndarray) -> float:
    """Independent Gaussian-integral identity, O(N²), for tiny 1-D controls.

    It uses the specified standard-normal target WITHOUT fitted centering/scaling.
    The closed form corresponds to integrating over all real frequencies.
    """
    x = np.asarray(x, float)
    if x.ndim != 1 or len(x) < 2 or not np.isfinite(x).all():
        raise ValueError('Need at least two finite scalar observations.')
    pairs = np.exp(-.5 * (x[:, None] - x[None, :])**2).mean()
    cross = np.exp(-x*x/4).mean()
    return float(len(x) * (np.sqrt(2*np.pi)*pairs - 2*np.sqrt(np.pi)*cross + np.sqrt(2*np.pi/3)))


def _torch_pair(a, b):
    import torch
    if a.ndim != 2 or a.shape != b.shape or a.shape[0] < 2 or a.shape[1] < 1:
        raise ValueError('Two matching B by D views with B >= 2 are required.')
    if not torch.isfinite(a).all() or not torch.isfinite(b).all():
        raise ValueError('Embeddings must be finite.')


def sigreg_torch(z, directions, frequencies=None):
    """Differentiable counterpart of projected_gaussian_score. No DDP reduction."""
    import torch
    _torch_pair(z, z)
    a = torch.as_tensor(directions, dtype=z.dtype, device=z.device)
    if a.ndim != 2 or a.shape[0] != z.shape[1] or a.shape[1] < 1:
        raise ValueError('Directions must have shape D by M.')
    if not torch.allclose(a.norm(dim=0), torch.ones(a.shape[1],dtype=z.dtype,device=z.device), atol=1e-6):
        raise ValueError('Directions must have unit norm.')
    t = torch.linspace(-5,5,17,dtype=z.dtype,device=z.device) if frequencies is None else torch.as_tensor(frequencies,dtype=z.dtype,device=z.device)
    if t.ndim != 1 or t.numel()<2 or not torch.isfinite(t).all() or not torch.all(t[1:]>t[:-1]):
        raise ValueError('Finite increasing frequency grid required.')
    phase = (z @ a).unsqueeze(-1) * t
    target = torch.exp(-.5*t*t)
    discrepancy = ((phase.cos().mean(dim=0)-target).square() + phase.sin().mean(dim=0).square())*target
    return z.shape[0]*torch.trapezoid(discrepancy,t,dim=-1).mean()


def vicreg_loss(a, b, invariance_weight=25., variance_weight=25., covariance_weight=1.):
    """Two-view VICReg-style loss with stated sample-covariance convention."""
    import torch
    _torch_pair(a,b)
    inv=(a-b).square().mean()
    var=sum(torch.relu(1-torch.sqrt(x.var(dim=0,unbiased=True)+1e-4)).mean() for x in [a,b])/2
    cov=a.new_zeros(())
    for x in [a,b]:
        c=x-x.mean(0);c=c.T@c/(len(x)-1)
        off=c-torch.diag(torch.diag(c))
        cov=cov+off.square().sum()/a.shape[1]
    return invariance_weight*inv+variance_weight*var+covariance_weight*cov


def barlow_loss(a, b, redundancy_weight=.005):
    """Cross-correlation objective with population-variance standardization."""
    import torch
    _torch_pair(a,b)
    a=(a-a.mean(0))/torch.sqrt(a.var(0,unbiased=False)+1e-5)
    b=(b-b.mean(0))/torch.sqrt(b.var(0,unbiased=False)+1e-5)
    c=a.T@b/len(a);diagonal=torch.diag(c)
    return (diagonal-1).square().sum()+redundancy_weight*(c-torch.diag(diagonal)).square().sum()


def info_nce(a,b,temperature=.2):
    """Symmetric two-view NT-Xent form: no self-pairs in the denominator."""
    import torch
    import torch.nn.functional as F
    _torch_pair(a,b)
    if temperature<=0: raise ValueError('Temperature must be positive.')
    z=F.normalize(torch.cat([a,b]),dim=1)
    logits=z@z.T/temperature
    logits=logits.masked_fill(torch.eye(len(z),dtype=torch.bool,device=z.device),float('-inf'))
    target=(torch.arange(len(z),device=z.device)+len(a))%len(z)
    return F.cross_entropy(logits,target)


def ema(old,new,tau: float):
    if not 0<=tau<=1:raise ValueError('EMA coefficient must be in [0,1].')
    if old.shape!=new.shape:raise ValueError('EMA parameters must match.')
    return tau*old+(1-tau)*new


def assert_disjoint(*partitions) -> None:
    seen=set()
    for partition in partitions:
        ids=set(np.asarray(partition).tolist())
        if seen & ids:raise ValueError('Identity overlap across partitions.')
        seen.update(ids)
