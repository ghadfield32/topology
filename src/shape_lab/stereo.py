"""Calibrated stereo examples using an attributed Middlebury sample.

Disparity d = u_left - u_right. doffs = cx_right - cx_left.
Depth Z = f * baseline / (d + doffs). The packaged baseline is in metres.
"""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
from .geometry import unproject

ROOT=Path(__file__).resolve().parents[2]


def reference_sample():
    """Return copies of the bundled real stereo data and calibration metadata."""
    folder=ROOT/'data/stereo'
    with np.load(folder/'motorcycle.npz',allow_pickle=False) as z:
        left=z['left'].copy();right=z['right'].copy();d=z['disparity_px'].copy()
    c=json.loads((folder/'calibration.json').read_text())
    return left,right,d,c


def depth_from_disparity(disparity,focal_px:float,baseline:float,doffs_px:float=0):
    if not np.isfinite([focal_px,baseline,doffs_px]).all() or focal_px<=0 or baseline<=0:
        raise ValueError('Focal length and baseline must be finite and positive.')
    d=np.asarray(disparity,float);den=d+doffs_px
    out=np.full(d.shape,np.nan,dtype=float)
    valid=np.isfinite(d)&(den>0)
    np.divide(focal_px*baseline,den,out=out,where=valid)
    return out


def point_cloud(disparity,calibration:dict,stride:int=1):
    """Return sampled camera-frame XYZ and source [row,column] IDs; never fill missing depth."""
    d=np.asarray(disparity,float)
    if d.ndim!=2 or not isinstance(stride,int) or stride<1:raise ValueError('Need a 2D disparity map and positive integer stride.')
    rows,cols=np.mgrid[0:d.shape[0]:stride,0:d.shape[1]:stride]
    rc=np.column_stack([rows.ravel(),cols.ravel()]);z=depth_from_disparity(d[rows,cols].ravel(),calibration['focal_px'],calibration['baseline_m'],calibration['doffs_px'])
    good=np.isfinite(z);k=np.asarray(calibration['K_left'],float)
    return unproject(rc[good,::-1],z[good],k),rc[good]


def grayscale(image):
    a=np.asarray(image,float)
    if a.ndim==3 and a.shape[2]==3:a=a.mean(2)
    if a.ndim!=2 or not np.isfinite(a).all():raise ValueError('Expected a finite grayscale or RGB image.')
    return a


def sparse_sad(left,right,rows_columns,max_disparity:int=128,radius:int=3):
    """Independent integer-disparity sum-absolute-difference baseline.

    No reference disparity is an input. Search only the same scanline in this
    *already rectified* pair. Equal costs choose the smaller disparity. A zero
    margin signals ambiguity; this margin is NOT a calibrated probability.
    Border requests receive NaN. No subpixel refinement or occlusion solver.
    """
    l=grayscale(left);r=grayscale(right);rc=np.asarray(rows_columns)
    if l.shape!=r.shape or rc.ndim!=2 or rc.shape[1]!=2 or not np.issubdtype(rc.dtype,np.integer):raise ValueError('Matching image shapes and integer N by 2 row/column coordinates required.')
    if not isinstance(max_disparity,int) or max_disparity<0 or not isinstance(radius,int) or radius<1:raise ValueError('Disparity must be nonnegative integer and patch radius positive integer.')
    pred=np.full(len(rc),np.nan);margin=np.full(len(rc),np.nan)
    for i,(row,col) in enumerate(rc):
        if row<radius or row>=l.shape[0]-radius or col<radius or col>=l.shape[1]-radius:continue
        patch=l[row-radius:row+radius+1,col-radius:col+radius+1]
        ds=np.arange(min(max_disparity,int(col)-radius)+1)
        # Assemble candidate patches on the same epipolar line; no ground truth here.
        patches=np.stack([r[row-radius:row+radius+1,col-int(d)-radius:col-int(d)+radius+1] for d in ds])
        costs=np.mean(np.abs(patches-patch),axis=(1,2));order=np.argsort(costs,kind='stable')
        pred[i]=ds[order[0]]
        margin[i]=costs[order[1]]-costs[order[0]] if len(ds)>1 else 0
    return pred,margin


def disparity_metrics(prediction,reference,bad_threshold_px:float=2):
    p=np.asarray(prediction,float);r=np.asarray(reference,float)
    if p.shape!=r.shape or not np.isfinite(bad_threshold_px) or bad_threshold_px<0:raise ValueError('Matching arrays and nonnegative finite threshold required.')
    eligible=np.isfinite(r);good=eligible&np.isfinite(p);n=int(good.sum());den=int(eligible.sum())
    err=np.abs(p[good]-r[good])
    return {'eligible':den,'evaluated':n,'coverage':n/den if den else None,
            'mean_absolute_error_px':float(err.mean()) if n else None,
            'median_absolute_error_px':float(np.median(err)) if n else None,
            'bad_fraction':float(np.mean(err>bad_threshold_px)) if n else None,
            'bad_threshold_px':float(bad_threshold_px)}
