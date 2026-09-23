"""Educational scaled dot-product attention. This is not VGGT or pretrained inference."""
from __future__ import annotations
import numpy as np


def attention(query,key,value,mask=None):
    q=np.asarray(query,float);k=np.asarray(key,float);v=np.asarray(value,float)
    if q.ndim!=2 or k.ndim!=2 or v.ndim!=2 or q.shape[1]!=k.shape[1] or k.shape[0]!=v.shape[0] or not q.shape[1]:raise ValueError('Expected Q[N,d], K[M,d], V[M,v].')
    if not all(np.isfinite(a).all() for a in (q,k,v)):raise ValueError('Attention inputs must be finite.')
    scores=q@k.T/np.sqrt(q.shape[1]);allowed=np.ones(scores.shape,bool) if mask is None else np.asarray(mask,bool)
    if allowed.shape!=scores.shape or not allowed.any(axis=1).all():raise ValueError('Each query needs at least one permitted key.')
    scores=np.where(allowed,scores,-np.inf);scores-=scores.max(axis=1,keepdims=True)
    weights=np.exp(scores);weights/=weights.sum(axis=1,keepdims=True)
    return weights@v,weights


def frame_mask(frame_ids):
    ids=np.asarray(frame_ids)
    if ids.ndim!=1:raise ValueError('Frame IDs must be a vector.')
    return ids[:,None]==ids[None,:]


def patch_tokens(image,patch_size:int=8):
    """Flatten nonoverlapping patches; retain source top-left row/column IDs.

    Trailing partial patches are explicitly dropped. No learned DINO embedding,
    positional encoding, training, confidence calibration, or geometry prediction.
    """
    a=np.asarray(image,float)
    if a.ndim not in (2,3) or not np.isfinite(a).all() or not isinstance(patch_size,int) or patch_size<=0:raise ValueError('Finite 2D/3D image and positive integer patch size required.')
    tokens=[];rc=[]
    for row in range(0,a.shape[0]-patch_size+1,patch_size):
        for col in range(0,a.shape[1]-patch_size+1,patch_size):
            tokens.append(a[row:row+patch_size,col:col+patch_size].ravel());rc.append((row,col))
    if not tokens:raise ValueError('Image must contain at least one complete patch.')
    return np.asarray(tokens),np.asarray(rc,dtype=int)
