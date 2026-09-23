"""Small, inspectable tools for the cross-industry learning laboratories.

These functions validate data boundaries; they are not clinical, financial,
industrial-control, or climate forecasting software. No function fetches data.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from .persistence import rips_filtration, persistent_homology

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'industries'
IDS = ('wdbc','wine','stackloss','grunfeld','co2','nile','elnino','modechoice')


def check_sha256(path: Path, expected: str) -> bool:
    """Fail closed rather than silently analyze changed source observations."""
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f'SHA-256 hash mismatch: {path}; expected {expected}, got {actual}')
    return True


def verify_snapshot(name: str) -> bool:
    if name not in IDS:
        raise ValueError(f'Unknown dataset ID {name!r}; choose from {IDS}')
    meta = json.loads((DATA / name / 'metadata.json').read_text())
    check_sha256(ROOT / meta['data_file'], meta['data_sha256'])
    check_sha256(ROOT / meta['source_file'], meta['source_sha256'])
    return True


def load_dataset(name: str) -> tuple[pd.DataFrame, dict]:
    verify_snapshot(name)
    meta = json.loads((DATA / name / 'metadata.json').read_text())
    table = pd.read_csv(ROOT / meta['data_file'])
    if len(table) != meta['rows'] or list(table.columns) != meta['columns']:
        raise ValueError('Snapshot schema or row count differs from its recorded contract')
    return table, meta


def _groups(values) -> tuple[np.ndarray, np.ndarray]:
    a = np.asarray(values)
    if a.ndim != 1 or pd.isna(a).any():
        raise ValueError('Group/time identifiers must be one-dimensional and nonmissing')
    unique = np.unique(a)
    if len(unique) < 5:
        raise ValueError('At least five distinct groups/times are needed for this 60/20/20 teaching split')
    return a, unique


def _partition(a, unique) -> dict[str, np.ndarray]:
    first, second = int(.6 * len(unique)), int(.8 * len(unique))
    return {key: np.flatnonzero(np.isin(a, group)) for key, group in zip(
        ('train','validation','test'), (unique[:first],unique[first:second],unique[second:]))}


def group_split(groups, seed: int = 6) -> dict[str, np.ndarray]:
    """Split unique groups, not their rows. No stratification is implied."""
    a, unique = _groups(groups)
    return _partition(a, np.random.default_rng(seed).permutation(unique))


def ordered_split(times) -> dict[str, np.ndarray]:
    """Chronological 60/20/20 partition; tied timestamps remain together."""
    a, unique = _groups(times)
    return _partition(a, unique)


def _matrix(x) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    if a.ndim != 2 or min(a.shape) == 0 or not np.isfinite(a).all():
        raise ValueError('Expected a nonempty finite two-dimensional numeric matrix')
    return a


@dataclass(frozen=True)
class TrainScaler:
    mean: np.ndarray
    scale: np.ndarray

    @classmethod
    def fit(cls, training_values) -> 'TrainScaler':
        x = _matrix(training_values)
        scale = x.std(axis=0, ddof=0)
        return cls(x.mean(axis=0), np.where(scale == 0, 1., scale))

    def transform(self, values) -> np.ndarray:
        x = _matrix(values)
        if x.shape[1] != len(self.mean):
            raise ValueError('Feature count differs from the training matrix')
        return (x - self.mean) / self.scale


@dataclass(frozen=True)
class WindowBatch:
    x: np.ndarray
    y: np.ndarray
    start: np.ndarray
    end: np.ndarray
    target: np.ndarray


def past_windows(values, times, length: int, horizon: int = 1, expected_step=None) -> WindowBatch:
    """Construct windows with explicit source positions and no future features.

    NaNs, infinities, or irregular steps anywhere from window start through its
    target invalidate that example. Target position is end + horizon. Timestamps
    are numeric here (e.g. days, months, years); convert dates explicitly first.
    """
    v, t = np.asarray(values, dtype=float), np.asarray(times, dtype=float)
    if v.ndim != 1 or t.shape != v.shape or not np.isfinite(t).all():
        raise ValueError('Values and finite numeric times must be aligned vectors')
    if isinstance(length, bool) or int(length) != length or length < 1:
        raise ValueError('length must be a positive integer')
    if isinstance(horizon, bool) or int(horizon) != horizon or horizon < 1:
        raise ValueError('horizon must be a positive integer')
    length, horizon = int(length), int(horizon)
    if np.any(np.diff(t) <= 0):
        raise ValueError('Times must increase strictly; duplicates are not silently aggregated')
    if expected_step is not None and (not np.isfinite(expected_step) or expected_step <= 0):
        raise ValueError('expected_step must be finite and positive')
    x, y, starts, ends, targets = [], [], [], [], []
    for end in range(length - 1, len(v) - horizon):
        start, target = end - length + 1, end + horizon
        if not np.isfinite(v[start:target+1]).all():
            continue
        if expected_step is not None and not np.allclose(np.diff(t[start:target+1]),expected_step,rtol=0,atol=1e-9):
            continue
        x.append(v[start:end+1]); y.append(v[target]); starts.append(start); ends.append(end); targets.append(target)
    return WindowBatch(np.array(x, dtype=float).reshape(-1,length), np.array(y, dtype=float),
        np.array(starts,dtype=int), np.array(ends,dtype=int), np.array(targets,dtype=int))


def assign_windows(batch: WindowBatch, raw_split: dict) -> dict[str,np.ndarray]:
    """Strict split: every source position, including the target, stays inside.

    This is more conservative than using known pre-test history for a test
    prediction. It is intentional: overlapping supports cannot cross partitions.
    """
    sets = {k:set(np.asarray(v,dtype=int)) for k,v in raw_split.items()}
    keys = list(sets)
    if any(sets[keys[i]] & sets[keys[j]] for i in range(len(keys)) for j in range(i)):
        raise ValueError('Raw partition indices overlap')
    return {k:np.array([i for i,(a,b) in enumerate(zip(batch.start,batch.target))
            if set(range(int(a),int(b)+1)) <= allowed],dtype=int) for k,allowed in sets.items()}


def mst_lengths(points) -> np.ndarray:
    """Kruskal's algorithm, retaining zero-length edges between duplicate rows."""
    x = _matrix(points); n = len(x); parent = list(range(n))
    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    edges = sorted((float(np.linalg.norm(x[i]-x[j])),i,j) for i in range(n) for j in range(i))
    out = []
    for d,i,j in edges:
        a,b = root(i),root(j)
        if a != b:
            parent[a] = b; out.append(d)
            if len(out) == n-1: break
    return np.asarray(out,dtype=float)


def local_topology(queries, anchors, k: int = 8) -> np.ndarray:
    """Six descriptors of query + k training-only reference observations.

    Columns: mean/std/max finite H0 lifetime, positive H1 count, max/sum H1
    lifetime. H0 is computed through an MST, H1 through a full Rips 2-skeleton.
    This is an engineered local summary, NOT homology of one measurement row.
    Ties select lexicographically by anchor coordinates (then input index).
    """
    q,a = _matrix(queries), _matrix(anchors)
    if q.shape[1] != a.shape[1] or not 2 <= k <= min(len(a),32):
        raise ValueError('Match dimensions and use 2 <= k <= min(anchor count,32)')
    result = []
    for query in q:
        selected = sorted(range(len(a)),key=lambda i:(float(np.linalg.norm(a[i]-query)),tuple(a[i]),i))[:k]
        cloud = np.vstack((query,a[selected])); h0 = mst_lengths(cloud)
        bars = persistent_homology(rips_filtration(cloud,max_homology=1),max_dim=1)
        lives = np.array([b.lifetime for b in bars if b.dim==1 and np.isfinite(b.death)],dtype=float)
        result.append([h0.mean(),h0.std(),h0.max(),len(lives),lives.max() if len(lives) else 0.,lives.sum()])
    return np.array(result,dtype=float)


def choice_table(table: pd.DataFrame) -> tuple[np.ndarray,np.ndarray,np.ndarray,list[str]]:
    """Turn four alternatives per traveler into one supervised example.

    Restrict features to offered wait/time/cost and income. Do not use choice,
    generalized cost (duplicate construction) or post-choice-sensitive party size.
    """
    needed = {'individual','mode','choice','ttme','invc','invt','hinc'}
    if not needed <= set(table): raise ValueError(f'Missing columns: {needed-set(table)}')
    if table[['individual','mode','choice']].isna().any().any(): raise ValueError('Missing choice identifiers')
    rows,y,ids = [],[],[]
    for person,group in table.groupby('individual',sort=True):
        g = group.sort_values('mode')
        if len(g)!=4 or list(g['mode'])!=[1,2,3,4] or not g.choice.isin([0,1]).all() or g.choice.sum()!=1:
            raise ValueError('Each traveler needs four unique alternatives and exactly one selected mode')
        if g.hinc.nunique()!=1: raise ValueError('Income must agree across the same traveler')
        rows.append(g[['ttme','invc','invt']].to_numpy(dtype=float).ravel().tolist()+[float(g.hinc.iloc[0])])
        y.append(int(g.loc[g.choice==1,'mode'].iloc[0])); ids.append(person)
    names = [f'mode{m}_{f}' for m in range(1,5) for f in ('ttme','invc','invt')] + ['income']
    return _matrix(rows),np.array(y,dtype=int),np.array(ids),names


def best_mean_change(values, min_segment: int = 5) -> tuple[int,float]:
    """Retrospective least-squares two-mean split; no causal interpretation."""
    y = np.asarray(values,dtype=float)
    if y.ndim!=1 or not np.isfinite(y).all() or min_segment<1 or len(y)<2*min_segment:
        raise ValueError('Finite vector with two sufficiently large segments required')
    candidates = [(float(np.sum((y[:k]-y[:k].mean())**2)+np.sum((y[k:]-y[k:].mean())**2)), k)
                  for k in range(min_segment,len(y)-min_segment+1)]
    loss,k = min(candidates)
    return k,loss


def seasonal_means(values, months) -> np.ndarray:
    y,m = np.asarray(values,dtype=float),np.asarray(months)
    if y.ndim!=1 or m.shape!=y.shape or not np.isfinite(y).all() or set(m)!=(set(range(1,13))):
        raise ValueError('Aligned finite observations containing all twelve month labels are required')
    return np.array([y[m==month].mean() for month in range(1,13)])
