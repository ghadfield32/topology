"""Fresh clean-kernel executions; learner notebooks are deliberately excluded."""
from pathlib import Path
import json,time,sys
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
def paths_for(mode):
    if mode=='sports':return sorted((ROOT/'sports_v8/notebooks').glob('*.ipynb'))+sorted((ROOT/'sports_v8/solutions').glob('*.ipynb'))
    patterns=['notebooks/*.ipynb','practice/answers/*.ipynb','consolidation/*.ipynb','physics/notebooks/*.ipynb','physics/practice/answers/*.ipynb','industry/notebooks/*.ipynb','industry/answers/*.ipynb','applications_v7/*/lab.ipynb','applications_v7/*/answers.ipynb','methods_v7/*/lab.ipynb','methods_v7/*/answers.ipynb']
    return sorted(set(p for pat in patterns for p in ROOT.glob(pat)))
def main(mode):
    paths=paths_for(mode);records=[]
    target=ROOT/f'reports/v8/{mode}_notebook_execution.json'
    for i,p in enumerate(paths):
        print(f'{i+1}/{len(paths)} {p.relative_to(ROOT)}',flush=True)
        b=nbformat.read(p,4)
        for c in b.cells:
            if c.cell_type=='code':c.outputs=[];c.execution_count=None
        t=time.perf_counter()
        try:
            NotebookClient(b,timeout=240,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}},allow_errors=False).execute()
            nbformat.write(b,p)
            record={'path':str(p.relative_to(ROOT)),'status':'passed','code_cells':sum(c.cell_type=='code' for c in b.cells),'png_outputs':sum('image/png' in out.get('data',{}) for c in b.cells if c.cell_type=='code' for out in c.outputs),'elapsed_seconds':round(time.perf_counter()-t,3)}
        except Exception as e:
            record={'path':str(p.relative_to(ROOT)),'status':'failed','error':str(e)}
        records.append(record);target.write_text(json.dumps(records,indent=2)+'\n')
        print(record['status'],flush=True)
    if any(r['status']=='failed' for r in records):raise SystemExit(1)
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'sports')
