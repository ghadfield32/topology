"""Clean-kernel execution of every reference notebook; learner work excluded."""
from pathlib import Path
import json,time,traceback
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
PATTERNS=['notebooks/*.ipynb','practice/answers/*.ipynb','consolidation/*.ipynb','physics/notebooks/*.ipynb','physics/practice/answers/*.ipynb','industry/notebooks/*.ipynb','industry/answers/*.ipynb']
def main():
    paths=[p for pattern in PATTERNS for p in sorted(ROOT.glob(pattern))]
    results=[];output=ROOT/'reports/v6/all_notebook_execution.json'
    for i,p in enumerate(paths):
        b=nbformat.read(p,4)
        for c in b.cells:
            if c.cell_type=='code':c.outputs=[];c.execution_count=None
        start=time.perf_counter();print(f'{i+1}/{len(paths)} {p.relative_to(ROOT)}',flush=True)
        try:
            NotebookClient(b,timeout=240,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}},allow_errors=False).execute()
            nbformat.write(b,p)
            result={'path':str(p.relative_to(ROOT)),'status':'passed','code_cells':sum(c.cell_type=='code' for c in b.cells),'png_outputs':sum('image/png' in o.get('data',{}) for c in b.cells if c.cell_type=='code' for o in c.outputs),'seconds':round(time.perf_counter()-start,3)}
        except Exception as e:
            traceback.print_exc();result={'path':str(p.relative_to(ROOT)),'status':'failed','error':str(e)}
        results.append(result);output.write_text(json.dumps(results,indent=2));print(result,flush=True)
    if any(r['status']!='passed' for r in results):raise SystemExit(1)
if __name__=='__main__':main()
