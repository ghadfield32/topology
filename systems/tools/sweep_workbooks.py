#!/usr/bin/env python3
"""Execute generated reference interfaces in fresh kernels, recording every result."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,sys,tempfile,time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from systems.python.workflow import new_directory,dump

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--keys',nargs='*');ap.add_argument('--languages',nargs='+',choices=['python','go','rust'],default=['python','go','rust']);a=ap.parse_args()
 import nbformat
 from nbclient import NotebookClient
 from jupyter_client import KernelManager
 from jupyter_client.kernelspec import KernelSpecManager
 labs=json.loads((ROOT/'native/protocols/labs.json').read_text())['labs'];keys=[x['key']for x in labs]
 if a.keys:
  if not set(a.keys)<=set(keys):raise ValueError('Unknown lab key')
  keys=a.keys
 out=new_directory(a.output);expected=[(k,l)for k in keys for l in a.languages];results=[]
 inputpaths=[ROOT/'learning/workbooks'/l/(k+'.ipynb')for k,l in expected]
 before={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in inputpaths}
 with tempfile.TemporaryDirectory(prefix='shape17_kernel_') as t:
  kdir=Path(t)/'shape17';kdir.mkdir();dump(kdir/'kernel.json',dict(argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],display_name='Verified active Python',language='python',env={'PYTHONUTF8':'1'}))
  for index,(key,lang) in enumerate(expected):
   src=ROOT/'learning/workbooks'/lang/(key+'.ipynb');dest=out/lang/(key+'.ipynb');dest.parent.mkdir(parents=True,exist_ok=True);nb=nbformat.read(src,as_version=4)
   begin=time.perf_counter();r=dict(lab=key,language=lang,source=src.relative_to(ROOT).as_posix())
   try:
    km=KernelManager(kernel_name='shape17',kernel_spec_manager=KernelSpecManager(kernel_dirs=[t]))
    NotebookClient(nb,km=km,timeout=1800,resources={'metadata':{'path':str(ROOT)}},allow_errors=False).execute()
    code=[c for c in nb.cells if c.cell_type=='code'];errors=[o for c in code for o in c.get('outputs',[])if o.output_type=='error']
    r.update(status='passed'if not errors and all(c.execution_count is not None for c in code)else'failed',code_cells=len(code))
   except Exception as e:r.update(status='failed',error=str(e)[-5000:])
   finally:
    # Supplying a KernelManager makes nbclient treat its lifetime as caller-owned.
    # The caller therefore closes EVERY kernel, including failures.
    if 'km' in locals():
     try:km.shutdown_kernel(now=True)
     except Exception:pass
     try:km.cleanup_resources()
     except Exception:pass
   r['seconds']=time.perf_counter()-begin;nbformat.write(nb,dest);r['notebook']=dest.relative_to(out).as_posix();results.append(r)
   dump(out/'execution.json',dict(status='running',expected=len(expected),completed=len(results),results=results,assessment='not_assessed'))
   print(f'{index+1}/{len(expected)} {key} {lang} {r["status"]}',flush=True)
 after={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in inputpaths};status='passed'if all(r['status']=='passed'for r in results)and before==after else'failed'
 dump(out/'execution.json',dict(status=status,expected=len(expected),completed=len(results),results=results,source_inputs_unchanged=before==after,source_hashes=before,python=sys.version,assessment='not_assessed',scope='fresh notebook interfaces, original Python computations and native16 protocols; NOT full scientific parity'))
 return int(status!='passed')
if __name__=='__main__':raise SystemExit(main())
