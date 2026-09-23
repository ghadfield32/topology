"""Explicit representations; all grids and bandwidths are declared, not learned globally."""
import numpy as np
from scipy.special import ndtr
from .persistence import Interval,persistent_homology,pixel_filtration

FEATURE_NAMES=[f'H{k}_{name}' for k in (0,1) for name in
               ['finite_count','max_lifetime','sum_lifetime','mean_lifetime','sum_squared_lifetime',
                'betti_at_0','betti_at_0.25','betti_at_0.5','betti_at_0.75','betti_at_1']]

def persistence_features(intervals: list[Interval]) -> np.ndarray:
    """20 fixed features. Essential bars excluded from lifetime sums, included in Betti counts."""
    values=[]
    for k in (0,1):
        bars=[b for b in intervals if b.dim==k]
        lengths=np.array([b.lifetime for b in bars if np.isfinite(b.death)])
        values.extend([len(lengths), lengths.max() if len(lengths) else 0.,
                       lengths.sum(), lengths.mean() if len(lengths) else 0.,
                       (lengths**2).sum()])
        values.extend(sum(b.birth<=t<b.death for b in bars) for t in [0,.25,.5,.75,1.])
    return np.asarray(values,dtype=float)

def image_features(image: np.ndarray) -> np.ndarray:
    """Input = 8x8 UCI intensity image with known range 0..16. No fitted parameters."""
    a=np.asarray(image,dtype=float)
    if a.ndim!=2 or not np.isfinite(a).all() or np.any(a<0) or np.any(a>16):
        raise ValueError('Expected finite image intensities in the known range 0..16.')
    intervals=persistent_homology(pixel_filtration(1.-a/16.),max_dim=1)
    return persistence_features(intervals)

def _finite_diagram(diagram):
    d=np.asarray(diagram,dtype=float).reshape(-1,2)
    if not np.isfinite(d).all() or np.any(d[:,1]<d[:,0]):
        raise ValueError('Pass finite birth <= death pairs only; handle essential bars separately.')
    return d

def persistence_landscape(diagram,grid: np.ndarray,levels: int=3) -> np.ndarray:
    """kth largest tent max(0,min(t-b,d-t)), sampled on the caller's grid."""
    d=_finite_diagram(diagram)
    t=np.asarray(grid,dtype=float)
    if t.ndim!=1 or levels<1 or not np.isfinite(t).all():
        raise ValueError('Use a finite 1D grid and positive levels.')
    tents=np.maximum(0,np.minimum(t[None,:]-d[:,0,None],d[:,1,None]-t[None,:]))
    values=np.sort(tents,axis=0)[::-1]
    result=np.zeros((levels,len(t)))
    result[:min(levels,len(d))]=values[:levels]
    return result

def persistence_image(diagram,birth_edges,persistence_edges,sigma: float=.1) -> np.ndarray:
    """Lifetime-weighted Gaussian mass integrated over pixels in (birth,lifetime) coordinates.

    Finite box may exclude mass. This is not an intensity image of the original object.
    """
    d=_finite_diagram(diagram)
    be=np.asarray(birth_edges,dtype=float); pe=np.asarray(persistence_edges,dtype=float)
    if sigma<=0 or not np.isfinite(sigma) or min(len(be),len(pe))<2:
        raise ValueError('Use positive finite sigma and at least two edges per axis.')
    if not np.isfinite(be).all() or not np.isfinite(pe).all() or np.any(np.diff(be)<=0) or np.any(np.diff(pe)<=0):
        raise ValueError('Bin edges must be finite and strictly increasing.')
    result=np.zeros((len(pe)-1,len(be)-1))
    for b,death in d:
        lifetime=death-b
        along_birth=np.diff(ndtr((be-b)/sigma))
        along_lifetime=np.diff(ndtr((pe-lifetime)/sigma))
        result+=lifetime*np.outer(along_lifetime,along_birth)
    return result

def delay_embedding(series: np.ndarray,dimension: int=3,lag: int=1) -> np.ndarray:
    """Forward windows. Prediction users must attach availability to the LAST sample."""
    x=np.asarray(series,dtype=float)
    if x.ndim!=1 or not np.isfinite(x).all() or dimension<1 or lag<1:
        raise ValueError('Use a finite 1D series, positive dimension and positive lag.')
    count=len(x)-(dimension-1)*lag
    if count<=0: raise ValueError('Series is too short for the requested window.')
    return np.column_stack([x[j*lag:j*lag+count] for j in range(dimension)])
