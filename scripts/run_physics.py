"""Execute physics reference notebooks with clean kernels; no downloads.

Default: all ten worked labs and ten answer notebooks. Learner work and progress
logs are never modified. The neural labs require the optional torch dependency.
"""
from pathlib import Path
import argparse,json,time
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stages',type=int,nargs='+',default=list(range(21,31)))
    p.add_argument('--kind',choices=['both','lab','answers'],default='both')
    a=p.parse_args()
    if any(n not in range(21,31) for n in a.stages):p.error('Use stages 21–30.')
    out=ROOT/'reports/physics_execution_v5.json'
    log=json.loads(out.read_text()) if out.exists() else {}
    for n in a.stages:
        for kind in (['lab','answers'] if a.kind=='both' else [a.kind]):
            source=ROOT/(f'physics/notebooks/{n}_lab.ipynb' if kind=='lab' else f'physics/practice/answers/{n}_practice.ipynb')
            key=f'{n}_{kind}';book=nbformat.read(source,4)
            for c in book.cells:
                if c.cell_type=='code':c.outputs=[];c.execution_count=None
            t=time.perf_counter();print('Executing',source.relative_to(ROOT),flush=True)
            try:NotebookClient(book,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
            except Exception as error:
                log[key]={'status':'FAILED','error':str(error)};out.write_text(json.dumps(log,indent=2)+'\n');raise
            nbformat.write(book,source)
            log[key]={'status':'PASSED','seconds':round(time.perf_counter()-t,3),'code_cells':sum(c.cell_type=='code' for c in book.cells),'errors':0}
            out.write_text(json.dumps(log,indent=2)+'\n');print(log[key],flush=True)
if __name__=='__main__':main()
