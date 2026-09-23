"""Opt-in original VGGT runner: local code + local weights, no auto-downloads.

Source-reviewed adapter; real inference was NOT executed in the course build.
Use a separate environment installed according to the pinned official checkout.
Run --help first. No import of torch or third-party model code is needed for help.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def git(repo:Path,*args:str)->str:
    return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,required=True,help='Local official original facebookresearch/vggt checkout, not Omega.')
    p.add_argument('--expected-commit',required=True,help='Exact full commit SHA; dirty tracked files are rejected.')
    p.add_argument('--checkpoint',type=Path,required=True,help='Existing trusted .pt/.pth state dictionary; never downloaded by this runner.')
    p.add_argument('--state-dict-key',help='Explicit wrapper key only when the local checkpoint requires it.')
    p.add_argument('--images',type=Path,nargs='+',required=True,help='Ordered still-image paths. Decode video frames separately with timestamps.')
    p.add_argument('--queries-npy',type=Path,help='Optional finite Nx2 queries in the FIRST PREPROCESSED image coordinate system.')
    p.add_argument('--max-frames',type=int,default=4,help='Safety cap, 1..32. Not a VRAM-fit guarantee.')
    p.add_argument('--preprocess',choices=['crop','pad'],default='crop')
    p.add_argument('--precision',choices=['auto','float16','bfloat16','float32'],default='auto')
    p.add_argument('--output',type=Path,required=True,help='New output directory; existing paths are never overwritten.')
    p.add_argument('--license-ack',action='store_true',help='Acknowledge reviewing the exact code and checkpoint licences for the intended use.')
    a=p.parse_args()
    if not a.license_ack:p.error('Read the exact code and weights licences, then supply --license-ack.')
    if not 1<=a.max_frames<=32 or len(a.images)>a.max_frames:p.error('Input frame count exceeds the explicit 1..32 cap.')
    if a.output.exists():p.error('Output already exists. Choose a new run directory.')
    a.repo=a.repo.resolve();a.checkpoint=a.checkpoint.resolve();a.images=[x.resolve() for x in a.images]
    if not (a.repo/'vggt/models/vggt.py').is_file():p.error('Expected the original VGGT repository layout.')
    if any(not x.is_file() for x in [a.checkpoint,*a.images]):p.error('A checkpoint or image file is missing.')
    commit=git(a.repo,'rev-parse','HEAD')
    if commit.lower()!=a.expected_commit.lower():p.error(f'Revision mismatch: found {commit}')
    if git(a.repo,'status','--porcelain','--untracked-files=no'):p.error('Tracked repository files are modified; use the intended clean revision.')
    # Offline library modes are additional safeguards, not a sandbox for arbitrary code.
    os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
    sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(a.repo))
    import numpy as np
    import torch
    from shape_lab.model_contract import validate_original_vggt
    from vggt.models.vggt import VGGT
    from vggt.utils.load_fn import load_and_preprocess_images
    from vggt.utils.pose_enc import pose_encoding_to_extri_intri
    if not torch.cuda.is_available():p.error('This opt-in runner requires CUDA. CPU course labs do not.')
    dtype_name=a.precision
    if dtype_name=='auto':dtype_name='bfloat16' if torch.cuda.is_bf16_supported() else 'float16'
    if dtype_name=='bfloat16' and not torch.cuda.is_bf16_supported():p.error('Requested bfloat16 is not supported by this CUDA device.')
    dtype=getattr(torch,dtype_name)
    metadata={'schema':'shape_original_vggt_run_v3','status':'running','model_family':'original_VGGT',
              'code_commit':commit,'repo_origin':git(a.repo,'remote','get-url','origin'),
              'checkpoint':{'name':a.checkpoint.name,'sha256':sha256(a.checkpoint),'state_dict_key':a.state_dict_key},
              'inputs':[{'order':i,'path':str(x),'sha256':sha256(x)} for i,x in enumerate(a.images)],
              'preprocessing':{'function':'load_and_preprocess_images','mode':a.preprocess,'raw_to_processed_mapping_validated':False},
              'precision':dtype_name,'torch':torch.__version__,'device':torch.cuda.get_device_name(0),
              'frame_convention':'first-camera-referenced model world; extrinsics are camera-from-world, OpenCV axes',
              'units':'model-normalized, NOT validated metres','metric_validated':False,
              'license_acknowledged':True,'tracking_requested':a.queries_npy is not None}
    a.output.mkdir(parents=True,exist_ok=False)
    status_path=a.output/'run.json'
    def record():status_path.write_text(json.dumps(metadata,indent=2,allow_nan=False)+'\n')
    record()
    try:
        start=time.perf_counter()
        images=load_and_preprocess_images([str(x) for x in a.images],mode=a.preprocess)
        queries=None
        if a.queries_npy is not None:
            q=np.load(a.queries_npy,allow_pickle=False)
            if q.ndim!=2 or q.shape[1]!=2 or not len(q) or not np.isfinite(q).all():raise ValueError('Queries must be finite nonempty Nx2 preprocessed coordinates.')
            h,w=images.shape[-2:]
            if np.any(q<0) or np.any(q[:,0]>=w) or np.any(q[:,1]>=h):raise ValueError('Query outside the first preprocessed image.')
            queries=torch.from_numpy(q.astype(np.float32)).cuda()
            metadata['query_sha256']=sha256(a.queries_npy)
        metadata['preprocessing_seconds']=time.perf_counter()-start
        state=torch.load(a.checkpoint,map_location='cpu',weights_only=True)
        if a.state_dict_key:state=state[a.state_dict_key]
        model=VGGT();model.load_state_dict(state,strict=True);del state
        model=model.eval().cuda();images=images.cuda()
        torch.cuda.synchronize();torch.cuda.reset_peak_memory_stats()
        t0=time.perf_counter()
        with torch.inference_mode(),torch.autocast(device_type='cuda',dtype=dtype,enabled=dtype_name!='float32'):
            predictions=model(images,query_points=queries)
        torch.cuda.synchronize()
        metadata['model_forward_seconds']=time.perf_counter()-t0
        metadata['peak_allocated_bytes_model_and_forward']=torch.cuda.max_memory_allocated()
        metadata['peak_reserved_bytes_model_and_forward']=torch.cuda.max_memory_reserved()
        ext,K=pose_encoding_to_extri_intri(predictions['pose_enc'],images.shape[-2:])
        keys=['pose_enc','depth','depth_conf','world_points','world_points_conf','images','track','vis','conf']
        arrays={k:predictions[k].detach().float().cpu().numpy() for k in keys if k in predictions}
        arrays['extrinsics']=ext.detach().float().cpu().numpy();arrays['intrinsics']=K.detach().float().cpu().numpy()
        contract=validate_original_vggt(arrays)
        output=a.output/'predictions.npz';np.savez_compressed(output,**arrays)
        metadata.update(status='completed_contract_check_only',contract=contract,predictions_sha256=sha256(output))
        metadata['timing_excludes']=['weight loading','CPU export','file compression','camera capture','display','benchmark registration']
        record();print(json.dumps(metadata,indent=2))
    except Exception as exc:
        metadata.update(status='failed',error_type=type(exc).__name__,error=str(exc));record();raise

if __name__=='__main__':main()
