"""Independent educational checks and evidence audits added in version 4.

These algorithms use definitions different from the main reduction routine.
Agreement checks software consistency; it does not certify physical ground truth.
"""
from __future__ import annotations
from hashlib import sha256
from itertools import combinations
from math import isqrt
from pathlib import Path
import numpy as np
from scipy.spatial.distance import cdist
from scipy.stats import binomtest
from .algebra import validate_complex


def pixel_betti_oracle(mask: np.ndarray) -> tuple[int, int]:
    """H0,H1 of a finite union of CLOSED square pixels via connectivity and Euler.

    Corner-touching squares are connected. Count unique square edges/vertices;
    b1=b0-(V-E+F) because a finite planar square complex has H2=0.
    This does not invoke triangulation, matrix rank, or persistence reduction.
    """
    a=np.asarray(mask)
    if a.ndim!=2 or a.dtype!=np.bool_ or not a.size:
        raise ValueError('Provide a nonempty 2D boolean foreground mask.')
    active=set(map(tuple,np.argwhere(a)))
    vertices=set();edges=set()
    for r,c in active:
        corners=((r,c),(r,c+1),(r+1,c+1),(r+1,c))
        vertices.update(corners)
        edges.update(tuple(sorted((corners[i],corners[(i+1)%4]))) for i in range(4))
    remaining=set(active);components=0
    while remaining:
        components+=1;stack=[remaining.pop()]
        while stack:
            r,c=stack.pop()
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    q=(r+dr,c+dc)
                    if q in remaining:remaining.remove(q);stack.append(q)
    euler=len(vertices)-len(edges)+len(active)
    return components,components-euler


def rank_prime(matrix, prime: int=2) -> int:
    """Exact row reduction in a small prime field; bounded educational integers."""
    if isinstance(prime,bool) or not isinstance(prime,(int,np.integer)) or prime<2 or any(prime%k==0 for k in range(2,isqrt(int(prime))+1)) or prime>46337:
        raise ValueError('Choose an integer prime between 2 and 46337.')
    a=np.asarray(matrix)
    if a.ndim!=2 or not np.isfinite(a).all() or np.any(a!=np.floor(a)) or np.any(np.abs(a)>2**52):
        raise ValueError('Provide a finite 2D integer matrix with entries at most 2**52 in magnitude.')
    a=a.astype(np.int64)%prime
    row=0
    for col in range(a.shape[1]):
        pivots=np.flatnonzero(a[row:,col])
        if not len(pivots):continue
        pivot=row+int(pivots[0]);a[[row,pivot]]=a[[pivot,row]]
        a[row]=(a[row]*pow(int(a[row,col]),-1,int(prime)))%prime
        for r in range(row+1,len(a)):
            if a[r,col]:a[r]=(a[r]-a[r,col]*a[row])%prime
        row+=1
        if row==len(a):break
    return row


def oriented_boundary(simplices, dimension: int) -> np.ndarray:
    """Integer boundary in increasing-vertex orientation; ordinary d0 has zero rows."""
    if isinstance(dimension,bool) or not isinstance(dimension,int) or dimension<0:
        raise ValueError('Dimension must be a nonnegative integer.')
    k=validate_complex(simplices)
    rows=[s for s in k if len(s)==dimension] if dimension else []
    columns=[s for s in k if len(s)==dimension+1]
    matrix=np.zeros((len(rows),len(columns)),dtype=np.int64)
    lookup={s:i for i,s in enumerate(rows)}
    if dimension:
        for j,simplex in enumerate(columns):
            for deleted in range(len(simplex)):
                face=simplex[:deleted]+simplex[deleted+1:]
                matrix[lookup[face],j]=(-1)**deleted
    return matrix


def h0_merge_times(points) -> np.ndarray:
    """Sorted Euclidean MST edge weights via dense Prim, including zero merges.

    Finite H0 death times equal these edge weights for a complete Rips filtration
    with all vertices born at zero. Drop zero weights ONLY when matching the
    course's positive-persistence reporting policy. Input limited to 500 points.
    """
    x=np.asarray(points,dtype=float)
    if x.ndim!=2 or not 1<=len(x)<=500 or x.shape[1]<1 or not np.isfinite(x).all():
        raise ValueError('Provide 1..500 finite points with at least one coordinate.')
    distances=cdist(x,x)
    used=np.zeros(len(x),bool);best=np.full(len(x),np.inf);best[0]=0
    weights=[]
    for step in range(len(x)):
        i=int(np.argmin(np.where(used,np.inf,best)))
        if step:weights.append(float(best[i]))
        used[i]=True;best=np.minimum(best,distances[i])
    return np.sort(weights)


def paired_accuracy_audit(truth, prediction_a, prediction_b, *, resamples: int=4000, seed: int=2026) -> dict:
    """Exploratory paired image-level comparison of already-exposed predictions.

    Resample paired correctness differences, not each model independently.
    The two-sided exact binomial test conditions on discordant outcomes.
    Its inferential interpretation requires an appropriate independent sampling
    unit and no selection on this holdout. This helper cannot establish either.
    """
    y=np.asarray(truth);a=np.asarray(prediction_a);b=np.asarray(prediction_b)
    if y.ndim!=1 or len(y)==0 or a.shape!=y.shape or b.shape!=y.shape:
        raise ValueError('Need nonempty, equally shaped 1D label arrays, aligned by sample ID.')
    for v in (y,a,b):
        if np.issubdtype(v.dtype,np.number) and not np.isfinite(v).all():raise ValueError('Labels cannot contain NaN or infinity.')
    if isinstance(resamples,bool) or not isinstance(resamples,int) or not 10<=resamples<=100_000:
        raise ValueError('Use 10..100000 bootstrap resamples.')
    ca=a==y;cb=b==y;diff=cb.astype(float)-ca.astype(float)
    a_only=int(np.sum(ca&~cb));b_only=int(np.sum(cb&~ca));discord=a_only+b_only
    p=float(binomtest(b_only,discord,.5,alternative='two-sided').pvalue) if discord else 1.
    rng=np.random.default_rng(seed);means=[]
    # Batch the resampling so memory does not grow with the requested count.
    for start in range(0,resamples,200):
        idx=rng.integers(0,len(y),size=(min(200,resamples-start),len(y)))
        means.extend(diff[idx].mean(axis=1))
    interval=np.quantile(means,[.025,.975]).tolist()
    return {'sample_count':len(y),'accuracy_a':float(ca.mean()),'accuracy_b':float(cb.mean()),
            'difference_b_minus_a':float(diff.mean()),'a_only_correct':a_only,'b_only_correct':b_only,
            'both_correct':int(np.sum(ca&cb)),'both_wrong':int(np.sum(~ca&~cb)),
            'exact_discordance_pvalue':p,'paired_percentile_interval':interval,
            'resamples':resamples,'seed':seed,'confidence_level':.95,
            'status':'exploratory_on_exposed_predictions',
            'limitations':'Image-level independence assumed, not established; no writer IDs; no fresh holdout or selection correction. Interval conditions on fixed fitted predictions.'}


def verify_evidence(log: dict, root: Path) -> list[dict]:
    """Read-only integrity check; never grades answers or changes recorded history."""
    root=Path(root).resolve();result=[]
    for stage,entry in sorted(log['stages'].items()):
        for i,attempt in enumerate(entry['attempts']):
            path=(root/attempt['evidence']).resolve()
            if not path.is_relative_to(root):status='outside_root'
            elif not path.is_file():status='missing'
            elif sha256(path.read_bytes()).hexdigest()!=attempt['evidence_sha256']:status='modified'
            else:status='matches'
            result.append({'stage':stage,'attempt_index':i,'evidence':attempt['evidence'],'status':status})
    return result
