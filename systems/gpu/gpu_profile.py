"""Inspect transfer, launch and compute separately. CPU results never stand in for CUDA."""
from pathlib import Path
import argparse, csv, json, os, sys, time, hashlib

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',default='.');p.add_argument('--output',required=True);p.add_argument('--device',choices=['cpu','cuda'],default='cpu');p.add_argument('--compile',action='store_true');p.add_argument('--triton',action='store_true');a=p.parse_args()
 out=Path(a.output);out.mkdir(parents=True,exist_ok=False)
 import torch
 if a.device=='cuda' and not torch.cuda.is_available():
  (out/'status.json').write_text(json.dumps({'status':'blocked','reason':'CUDA device unavailable; no GPU measurement performed'},indent=2));return 3
 if a.triton and a.device!='cuda':
  (out/'status.json').write_text(json.dumps({'status':'blocked','reason':'Triton exercise requires CUDA in this teaching path'},indent=2));return 3
 path=Path(a.repo)/'data/raw/iris.csv'
 with path.open()as f:
  rows=list(csv.DictReader(f));cols=['sepal_length_cm','sepal_width_cm','petal_length_cm','petal_width_cm'];flat=[float(r[c])for r in rows for c in cols]
 # Repetition creates a benchmark-sized buffer, not additional independent observations.
 host=torch.tensor(flat*1024,dtype=torch.float32);expected=host.to(torch.float64)*1.25+.5
 start=time.perf_counter();x=host.to(a.device)
 if a.device=='cuda':torch.cuda.synchronize()
 transfer=time.perf_counter()-start
 def operation(z):return z*1.25+.5
 mode='eager'
 if a.compile:operation=torch.compile(operation);mode='torch.compile'
 if a.triton:
  import triton
  import triton.language as tl
  @triton.jit
  def kernel(X,Y,N:tl.constexpr,B:tl.constexpr):
   i=tl.program_id(0)*B+tl.arange(0,B);v=tl.load(X+i,i<N,other=0);tl.store(Y+i,v*1.25+.5,i<N)
  def operation(z):
   y=torch.empty_like(z);kernel[(triton.cdiv(z.numel(),256),)](z,y,z.numel(),256);return y
  mode='triton'
 cold=time.perf_counter();operation(x)
 if a.device=='cuda':torch.cuda.synchronize()
 cold=time.perf_counter()-cold
 for _ in range(3):operation(x)
 if a.device=='cuda':torch.cuda.synchronize();torch.cuda.reset_peak_memory_stats()
 measurements=[]
 for _ in range(20):
  t=time.perf_counter();y=operation(x)
  if a.device=='cuda':torch.cuda.synchronize()
  measurements.append(time.perf_counter()-t)
 activities=[torch.profiler.ProfilerActivity.CPU]
 if a.device=='cuda':activities.append(torch.profiler.ProfilerActivity.CUDA)
 with torch.profiler.profile(activities=activities,record_shapes=True,profile_memory=True)as prof:
  y=operation(x)
  if a.device=='cuda':torch.cuda.synchronize()
 prof.export_chrome_trace(str(out/'trace.json'))
 error=float((y.cpu().to(torch.float64)-expected).abs().max())
 result=dict(status='passed'if error<=1e-5 else'failed',device=a.device,mode=mode,torch=torch.__version__,source=str(path),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),observed_rows=150,buffer_repetitions=1024,buffer_values=len(host),transfer_seconds=transfer,cold_seconds=cold,steady_seconds=measurements,max_abs_error=error,peak_allocated_gpu_bytes=torch.cuda.max_memory_allocated()if a.device=='cuda'else None,limitations=['Microbenchmark, not end-to-end sports pipeline performance.','Repeated rows do not enlarge the observed dataset.','CPU run is not evidence of CUDA/Triton performance.','Steady timings include allocation and explicit synchronization.'])
 (out/'status.json').write_text(json.dumps(result,indent=2));return 0 if result['status']=='passed'else 1
if __name__=='__main__':raise SystemExit(main())
