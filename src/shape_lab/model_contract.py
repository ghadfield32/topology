"""Original VGGT output-shape checks; NOT a model-accuracy or metric-validity check.

Uses the public original VGGT model interface inspected on 2026-09-20. Omega is
not accepted through this interface. Confidence scores are not probabilities.
"""
from __future__ import annotations
import numpy as np


def validate_original_vggt(arrays: dict) -> dict:
    required={'depth','depth_conf','world_points','world_points_conf','images','pose_enc','extrinsics','intrinsics'}
    missing=required-set(arrays)
    if missing:raise ValueError(f'Missing original VGGT output keys: {sorted(missing)}')
    x={k:np.asarray(arrays[k]) for k in required}
    images=x['images']
    if images.ndim!=5 or images.shape[0]!=1 or images.shape[2]!=3 or min(images.shape)<=0:
        raise ValueError('Expected one batch of RGB images [1,S,3,H,W].')
    _,s,_,h,w=images.shape
    expected={'images':(1,s,3,h,w),'pose_enc':(1,s,9),'depth':(1,s,h,w,1),
              'depth_conf':(1,s,h,w),'world_points':(1,s,h,w,3),
              'world_points_conf':(1,s,h,w),'extrinsics':(1,s,3,4),'intrinsics':(1,s,3,3)}
    for k,shape in expected.items():
        if x[k].shape!=shape or not np.issubdtype(x[k].dtype,np.number) or not np.isfinite(x[k]).all():
            raise ValueError(f'{k} must be a finite numeric array with shape {shape}.')
    if np.any(images<0) or np.any(images>1):raise ValueError('RGB values must be in [0,1].')
    if np.any(x['depth']<=0):raise ValueError('Expected positive optical-axis depth predictions.')
    R=x['extrinsics'][0,:,:,:3]
    if not np.allclose(np.swapaxes(R,-1,-2)@R,np.eye(3),atol=1e-3,rtol=0) or not np.allclose(np.linalg.det(R),1,atol=1e-3,rtol=0):
        raise ValueError('Camera rotations are not numerically proper rotations.')
    K=x['intrinsics'][0]
    if np.any(K[:,0,0]<=0) or np.any(K[:,1,1]<=0) or not np.allclose(K[:,2,:],[0,0,1],atol=1e-5,rtol=0):
        raise ValueError('Invalid camera intrinsic convention.')
    track_dim=None;tracking={'track','vis','conf'}&set(arrays)
    if tracking:
        if tracking!={'track','vis','conf'}:raise ValueError('Tracking requires track, vis and conf together.')
        track=np.asarray(arrays['track'])
        if track.ndim!=4 or track.shape[:2]!=(1,s) or track.shape[-1]!=2 or not np.isfinite(track).all():
            raise ValueError('Original VGGT tracks must be finite [1,S,N,2] image coordinates, not 3D points.')
        for k in ['vis','conf']:
            a=np.asarray(arrays[k])
            if a.shape!=track.shape[:-1] or not np.isfinite(a).all():raise ValueError(f'Invalid {k} shape or values.')
        track_dim=2
    return {'model_family':'original_VGGT','batch_size':1,'frames':s,'height':h,'width':w,
            'track_coordinate_dimension':track_dim,'contract_valid':True,'metric_validated':False,
            'confidence_is_probability':False,'units':'model-normalized; not established as metres'}


def sample_candidate_points(arrays:dict,frame:int=0,max_points:int=32,confidence_quantile:float=.5):
    """Deterministic small sample with [frame,row,col] IDs, for exploratory TDA.

    A within-frame confidence quantile is a selection rule, not a calibrated
    reliability cutoff. No merging, deduplication or physical scale fitting.
    """
    report=validate_original_vggt(arrays)
    if not isinstance(frame,int) or frame not in range(report['frames']):raise ValueError('Frame index is out of range.')
    if not isinstance(max_points,int) or max_points<1 or max_points>64:raise ValueError('Choose 1..64 points for the educational enumerator.')
    if not np.isfinite(confidence_quantile) or not 0<=confidence_quantile<=1:raise ValueError('Quantile must be between zero and one.')
    confidence=np.asarray(arrays['world_points_conf'])[0,frame]
    mask=confidence>=np.quantile(confidence,confidence_quantile)
    rc=np.argwhere(mask)
    if not len(rc):raise ValueError('No eligible points under the declared rule.')
    pick=np.linspace(0,len(rc)-1,min(max_points,len(rc)),dtype=int);rc=rc[pick]
    xyz=np.asarray(arrays['world_points'])[0,frame,rc[:,0],rc[:,1]]
    ids=np.column_stack([np.full(len(rc),frame),rc])
    return xyz,ids
