"""Execute selected course notebooks with a clean kernel per notebook.

Usage: python scripts/run_notebooks.py --stages 0 1 2
No --stages executes all 21 in order. Outputs replace saved working outputs,
not raw datasets. Read reports/REFERENCE_RESULTS.json for the shipped summary.
"""
from pathlib import Path
import argparse,json,time,sys
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--stages',type=int,nargs='*',default=list(range(21)))
    args=parser.parse_args()
    if any(s not in range(21) for s in args.stages): parser.error('Stages must be in 0..20.')
    report_path=ROOT/'reports/notebook_execution.json'
    report=json.loads(report_path.read_text()) if report_path.exists() else {}
    for stage in args.stages:
        tag=f'{stage:02d}';path=ROOT/'notebooks'/f'{tag}_lab.ipynb'
        print(f'Executing {path.name}',flush=True)
        nb=nbformat.read(path,as_version=4)
        for cell in nb.cells:
            if cell.cell_type=='code': cell.outputs=[];cell.execution_count=None
        start=time.perf_counter()
        try:
            NotebookClient(nb,timeout=240,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
        except Exception as exc:
            report[tag]={'status':'FAILED','error':str(exc),'seconds':time.perf_counter()-start}
            report_path.write_text(json.dumps(report,indent=2))
            raise
        nbformat.write(nb,path)
        report[tag]={'status':'PASSED','code_cells':sum(c.cell_type=='code' for c in nb.cells),
                     'seconds':round(time.perf_counter()-start,3),'errors':0}
        report_path.write_text(json.dumps(report,indent=2))
        print(report[tag],flush=True)

if __name__=='__main__': main()
