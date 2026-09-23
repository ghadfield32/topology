"""Run selected v4 consolidation notebooks. No model or dataset downloads.

python scripts/run_consolidation.py --stages 0 1 2
Omit --stages for all 21 in order. Stage 20 reads the preceding saved reports.
This writes reference evidence only; it never writes learning-log attempts.
"""
from pathlib import Path
import argparse, json, time
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stages',type=int,nargs='+',default=list(range(21)))
    args=parser.parse_args()
    if any(n not in range(21) for n in args.stages):parser.error('Stages must be 0..20.')
    path=ROOT/'reports/consolidation_execution_v4.json'
    log=json.loads(path.read_text()) if path.exists() else {}
    for n in args.stages:
        tag=f'{n:02d}';source=ROOT/f'consolidation/{tag}_lab.ipynb'
        notebook=nbformat.read(source,4)
        for c in notebook.cells:
            if c.cell_type=='code':c.outputs=[];c.execution_count=None
        start=time.perf_counter();print('Executing consolidation',tag,flush=True)
        try:
            NotebookClient(notebook,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
        except Exception as error:
            log[tag]={'status':'FAILED','error':str(error)}
            path.write_text(json.dumps(log,indent=2)+'\n');raise
        nbformat.write(notebook,source)
        log[tag]={'status':'PASSED','seconds':round(time.perf_counter()-start,3),
                  'code_cells':sum(c.cell_type=='code' for c in notebook.cells),'errors':0}
        path.write_text(json.dumps(log,indent=2)+'\n')
        print(log[tag],flush=True)
if __name__=='__main__':main()
