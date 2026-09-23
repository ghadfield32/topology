"""Educational PCGrad/Norm-PCGrad and normalized equal-alignment solve.

See sources/v5_sources.json for primary algorithms. No universal common-descent
claim is made for arbitrary multi-gradient inputs. Optimizer descent is -d.
"""
from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike
from .classical import finite


def gradient_matrix(G: ArrayLike):
    G=finite(G)
    if G.ndim!=2 or 0 in G.shape:raise ValueError('Expected nonempty [losses, parameters].')
    return G


def cosines(G: ArrayLike):
    G=gradient_matrix(G);norm=np.linalg.norm(G,axis=1)
    U=np.divide(G,norm[:,None],out=np.zeros_like(G),where=norm[:,None]>0)
    return U@U.T


def pcgrad(G: ArrayLike,normalise: bool=False,seed: int=0):
    """Sequential PCGrad; optional normalization AFTER all projections per row.

Random order is fixed by seed. Reference gradients remain original; projected
copies change. Vanishing projected rows contribute zero (explicit convention).
"""
    G=gradient_matrix(G);P=G.copy();rng=np.random.default_rng(seed)
    for i in range(len(G)):
        for j in rng.permutation(len(G)):
            if i==j:continue
            denom=G[j]@G[j];dot=P[i]@G[j]
            if denom>0 and dot<0:P[i]-=dot/denom*G[j]
    if normalise:
        norms=np.linalg.norm(P,axis=1)
        P=np.divide(P,norms[:,None],out=np.zeros_like(P),where=norms[:,None]>1e-14)
    return P.sum(axis=0)


def config_direction(G: ArrayLike,tol: float=1e-10):
    """Diagnose the ConFIG normalized equal-alignment linear system Uv=1.

Zero rows are excluded from solve and reported. An incompatible system returns
its least-squares diagnostic direction, explicitly marked incompatible rather
than claiming the ConFIG guarantee. Caller must examine flags/dot products.
"""
    G=gradient_matrix(G);norm=np.linalg.norm(G,axis=1);active=norm>tol
    if not np.any(active):
        return {'direction':np.zeros(G.shape[1]),'compatible':False,'strict_common_descent':False,
                'residual':0.,'zero_rows':list(range(len(G))),'dot_products':np.zeros(len(G))}
    U=G[active]/norm[active,None]
    v=np.linalg.lstsq(U,np.ones(len(U)),rcond=None)[0]
    residual=float(np.linalg.norm(U@v-1));nv=np.linalg.norm(v)
    unit=v/nv if nv>tol else np.zeros_like(v)
    direction=unit*float(np.sum(G@unit))
    dots=G@direction
    return {'direction':direction,'compatible':bool(residual<=tol),
            'strict_common_descent':bool(np.all(dots>tol)),
            'residual':residual,'zero_rows':np.flatnonzero(~active).tolist(),'dot_products':dots}
