"""Small sports teaching calculations with explicit units and information limits.

Inputs are measured/estimated coordinates only when their data card says so.
These helpers do not certify contact, release, clinical joint angles or ground truth.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import hashlib
import io
import json
import numpy as np
import pandas as pd
from .persistence import rips_filtration, persistent_homology, diagram


def to_metres(values, unit: str) -> np.ndarray:
    """Convert international feet/inches or metres; never guess an unknown unit."""
    factors = {'ft': .3048, 'in': .0254, 'm': 1.}
    if unit not in factors:
        raise ValueError('Supported explicit units: ft, in, m.')
    x = np.asarray(values, dtype=float)
    if not np.isfinite(x).all():
        raise ValueError('Length values must be finite; mask missing values first.')
    return x * factors[unit]


def frame_times(frames, fps: float) -> np.ndarray:
    """Ideal sample clock, not a measured exposure/PTS or wall-clock timestamp."""
    f = np.asarray(frames, dtype=float)
    if (f.ndim != 1 or not len(f) or not np.isfinite(f).all()
            or np.any(f < 0) or np.any(f != np.floor(f))
            or np.any(np.diff(f) <= 0) or not np.isfinite(fps) or fps <= 0):
        raise ValueError('Use increasing nonnegative integer frame IDs and positive fps.')
    return f / fps


def joint_angles(a, b, c) -> np.ndarray:
    """Unsigned angle ABC in degrees [0,180]; not an anatomical Euler convention."""
    a, b, c = (np.asarray(x, dtype=float) for x in (a, b, c))
    if (a.shape != b.shape or a.shape != c.shape or a.ndim != 2 or a.shape[1] != 3
            or not all(np.isfinite(x).all() for x in (a, b, c))):
        raise ValueError('Use equal finite arrays with shape (n,3).')
    u, v = a-b, c-b
    norms = np.linalg.norm(u, axis=1)*np.linalg.norm(v, axis=1)
    if np.any(norms <= 1e-15):
        raise ValueError('Coincident landmarks do not define an angle.')
    return np.degrees(np.arccos(np.clip(np.einsum('ij,ij->i',u,v)/norms,-1,1)))


def interval_velocities(frames, xyz_m, fps: float, max_gap_frames: int = 1):
    """Secant average velocity over accepted intervals. Gaps/missing values -> NaN.

    Returns (velocity, accepted); row i spans input i to i+1. Values are not
    instantaneous derivatives; max_gap_frames is an explicit analysis policy.
    """
    t = frame_times(frames, fps)
    x = np.asarray(xyz_m, dtype=float)
    if x.shape != (len(t),3) or len(t)<2:
        raise ValueError('Use at least two frames and an (n,3) coordinate array.')
    if (not np.isfinite(max_gap_frames) or max_gap_frames < 1
            or int(max_gap_frames) != max_gap_frames):
        raise ValueError('max_gap_frames must be a positive integer.')
    valid = (np.diff(np.asarray(frames))<=max_gap_frames)
    valid &= np.isfinite(x[:-1]).all(axis=1)&np.isfinite(x[1:]).all(axis=1)
    velocity = np.full((len(t)-1,3), np.nan)
    velocity[valid] = np.diff(x,axis=0)[valid]/np.diff(t)[valid,None]
    return velocity, valid


@dataclass(frozen=True)
class VerticalFit:
    t0: float
    z0: float
    v0: float
    g: float
    residual_rmse_m: float
    fit_rows: int
    fixed_gravity: bool

    def predict(self, times) -> np.ndarray:
        u=np.asarray(times,dtype=float)-self.t0
        if not np.isfinite(u).all():raise ValueError('Finite prediction times required.')
        return self.z0+self.v0*u-.5*self.g*u*u


def fit_vertical(times_s, z_m, gravity: float | None = None) -> VerticalFit:
    """Fit z=z0+v0*(t-t0)-g/2*(t-t0)^2; never infer a release label.

    Freely fitted g is a coefficient, not an independently measured gravity.
    No physical constraints are imposed on its sign. Fixed g is an assumption.
    """
    t,z=np.asarray(times_s,float),np.asarray(z_m,float)
    if (t.ndim!=1 or z.shape!=t.shape or len(t)<3 or not np.isfinite(t).all()
            or not np.isfinite(z).all() or np.any(np.diff(t)<=0)):
        raise ValueError('At least three increasing finite times and matched heights required.')
    if gravity is not None and (not np.isfinite(gravity) or gravity<=0):
        raise ValueError('A fixed gravity must be finite and positive.')
    u=t-t[0]
    if gravity is None:
        coef,_,rank,_=np.linalg.lstsq(np.column_stack([u*0+1,u,u*u]),z,rcond=None)
        if rank!=3:raise ValueError('Rank deficient quadratic fit.')
        z0,v0,quadratic=coef;g=-2*quadratic
    else:
        coef,_,rank,_=np.linalg.lstsq(np.column_stack([u*0+1,u]),z+.5*gravity*u*u,rcond=None)
        if rank!=2:raise ValueError('Rank deficient fixed-gravity fit.')
        z0,v0=coef;g=gravity
    pred=z0+v0*u-.5*g*u*u
    return VerticalFit(float(t[0]),float(z0),float(v0),float(g),float(np.sqrt(np.mean((pred-z)**2))),len(t),gravity is not None)


def causal_hold(times, values, queries, max_age: float):
    """Past-only sample hold; returns held values and source row (-1 unavailable).

    This creates a derived estimate, not a new observed frame. Queries need not
    be sorted. A source at exactly the query time is available under this model.
    """
    t,v,q=np.asarray(times,float),np.asarray(values,float),np.asarray(queries,float)
    if (t.ndim!=1 or not len(t) or v.ndim!=1 or v.shape!=t.shape or q.ndim!=1
            or not all(np.isfinite(x).all() for x in (t,v,q))
            or np.any(np.diff(t)<=0) or not np.isfinite(max_age) or max_age<0):
        raise ValueError('Finite increasing source times, scalar values, queries and nonnegative max_age required.')
    idx=np.searchsorted(t,q,side='right')-1
    safe=np.maximum(idx,0)
    ok=(idx>=0)&(q-t[safe]<=max_age)
    return np.where(ok,v[safe],np.nan),np.where(ok,idx,-1)


def fit_standardize(values, fit_rows):
    """Fit population mean/std only on declared rows; constant features use scale1."""
    x=np.asarray(values,float);i=np.asarray(fit_rows)
    if (x.ndim!=2 or not np.isfinite(x).all() or i.ndim!=1 or not len(i)
            or not np.issubdtype(i.dtype,np.integer) or np.any(i<0) or np.any(i>=len(x))
            or len(set(i.tolist()))!=len(i)):
        raise ValueError('Finite matrix and unique valid integer fitting rows required.')
    mean=x[i].mean(axis=0);scale=x[i].std(axis=0)
    scale=np.where(scale==0,1.,scale)
    return (x-mean)/scale,mean,scale


def group_partition(groups, train_groups, validation_groups, test_groups):
    """Explicit complete disjoint group assignment. A row is not an independent person."""
    g=np.asarray(groups)
    sets=[set(x) for x in (train_groups,validation_groups,test_groups)]
    if (g.ndim!=1 or not len(g) or not all(sets)
            or any(sets[i]&sets[j] for i in range(3) for j in range(i+1,3))
            or set(g.tolist())!=set.union(*sets)):
        raise ValueError('Nonempty, disjoint group sets must exactly cover the observed IDs.')
    return {name:np.flatnonzero(np.isin(g,list(ids))) for name,ids in zip(('train','validation','test'),sets)}


def cloud_diagrams(points):
    """F2 Rips H0/H1, full finite edge scale, through triangles; ordinary homology."""
    bars=persistent_homology(rips_filtration(points,max_homology=1),max_dim=1)
    return {k:diagram(bars,k) for k in (0,1)}


def tracking_cloud(player_data, detected_only: bool=True):
    """SkillCorner-format XY adapter. Detected means provider flag, not ground truth.

    No full-match tracking file is bundled or executed. The adapter is tested
    on manufactured schema fixtures; actual data acquisition is separate.
    """
    ids=[];points=[];seen=set()
    for row in player_data:
        ident=row['player_id']
        if ident in seen:raise ValueError('Duplicate player ID in one frame.')
        seen.add(ident)
        if not isinstance(row['is_detected'],bool):raise ValueError('Boolean detected flag required.')
        if detected_only and not row['is_detected']:continue
        p=[row['x'],row['y']]
        if not np.isfinite(np.asarray(p,dtype=float)).all():raise ValueError('Selected XY coordinates must be finite.')
        ids.append(ident);points.append(p)
    return np.asarray(points,float).reshape(-1,2),np.asarray(ids)


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def check_payload(data: bytes, expected_blob: str | None=None, max_bytes: int=10_000_000):
    if not data or len(data)>max_bytes:raise ValueError('Empty or oversized source payload.')
    if data.startswith(b'version https://git-lfs.github.com/spec/'):
        raise ValueError('Git LFS pointer received, not the dataset bytes.')
    if expected_blob is not None and git_blob_sha1(data)!=expected_blob:
        raise ValueError('Source revision differs from the recorded Git blob. Review before accepting.')
    return True


def verify_local_data(root: Path):
    d=Path(root)/'sports_v8/data';m=json.loads((d/'manifest.json').read_text())
    out=[]
    for source in m['sources']:
        path=d/source['file']
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        out.append({'id':source['id'],'ok':digest==source['local_sha256'],'sha256':digest})
    return out


def load_sports(root: Path):
    if not all(r['ok'] for r in verify_local_data(root)):
        raise ValueError('Local sports excerpt hash mismatch. Inspect changes before analysis.')
    d=Path(root)/'sports_v8/data'
    return json.loads((d/'spl_selected_frames.json').read_text()),pd.read_csv(d/'skillcorner_selected_profiles.csv')


def compare_spl(local, source):
    """Compare excerpt to supplied original JSON. Revision check is separate."""
    pairs=(('sampling_rate','sampling_rate'),('session','trial_date'),('participant_id','participant_id'),('trial_id','trial_id'))
    if any(local[a]!=source[b] for a,b in pairs):raise ValueError('SPL metadata mismatch.')
    frames={r['frame']:r for r in source['tracking']}
    count=0
    for record in local['records']:
        r=frames[record['frame']]
        if r['time']!=record['source_time']:raise ValueError('SPL source clock mismatch.')
        for name in ['ball','right_shoulder','right_elbow','right_wrist']:
            original=r['data']['ball'] if name=='ball' else r['data']['player'][name.upper()]
            if not np.allclose(original,record[name],rtol=1e-12,atol=1e-12):
                raise ValueError(f'SPL numeric mismatch: frame {record["frame"]}, {name}.')
            count+=3
    for a,b in [('result','result'),('landing_x','landing_x'),('landing_y','landing_y'),('entry_angle_deg','entry_angle')]:
        if a in local and local[a]!=source[b]:raise ValueError(f'SPL result metadata mismatch: {a}.')
    return {'frames':len(local['records']),'numeric_values':count,'equal':True}


def compare_skillcorner(local: pd.DataFrame, source: pd.DataFrame):
    selected=source.iloc[local.source_row.to_numpy(dtype=int)-1]
    for column in local.columns:
        if column=='source_row':continue
        a,b=local[column].to_numpy(),selected[column].to_numpy()
        equal=np.array_equal(a,b) if a.dtype.kind in 'OUS' else np.allclose(a.astype(float),b.astype(float),rtol=1e-12,atol=1e-12,equal_nan=True)
        if not equal:raise ValueError(f'SkillCorner numeric/text mismatch: {column}.')
    return {'rows':len(local),'columns':len(local.columns)-1,'equal':True}
