from pathlib import Path
import json,time
import nbformat
from nbclient import NotebookClient
R=Path(__file__).resolve().parents[1]
rows=[]
sections=json.loads((R/'docs/v7/new_sections.json').read_text())
for s in sections:
 for relative in s['reference_notebooks']:
    p=R/relative;print(relative,flush=True);start=time.perf_counter();doc=nbformat.read(p,as_version=4)
    for c in doc.cells:
     if c.cell_type=='code':c.outputs=[];c.execution_count=None
    try:
     NotebookClient(doc,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(R)}},allow_errors=False).execute()
     nbformat.write(doc,p)
     rows.append({'path':relative,'status':'passed','code_cells':sum(c.cell_type=='code' for c in doc.cells),'png_outputs':sum('image/png' in o.get('data',{}) for c in doc.cells if c.cell_type=='code' for o in c.outputs),'seconds':round(time.perf_counter()-start,3)})
    except Exception as e:
     rows.append({'path':relative,'status':'failed','error':str(e)})
     (R/'reports/v7/new_notebook_execution.json').write_text(json.dumps(rows,indent=2));raise
    (R/'reports/v7/new_notebook_execution.json').write_text(json.dumps(rows,indent=2));print(rows[-1],flush=True)
