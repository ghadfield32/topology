"""Execute reference industry notebooks, never the unfinished learner assignments."""
from pathlib import Path
import argparse, json, time, traceback
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--answers',action='store_true');args=parser.parse_args()
    paths=sorted((ROOT/'industry/notebooks').glob('*.ipynb'))
    if args.answers:paths+=sorted((ROOT/'industry/answers').glob('*.ipynb'))
    outcomes=[]
    for path in paths:
        start=time.perf_counter();nb=nbformat.read(path,as_version=4)
        try:
            NotebookClient(nb,timeout=240,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}},allow_errors=False).execute()
            nbformat.write(nb,path);item={'path':str(path.relative_to(ROOT)),'status':'executed','seconds':time.perf_counter()-start,'code_cells':sum(c.cell_type=='code' for c in nb.cells)}
            print(item,flush=True)
        except Exception as exc:
            item={'path':str(path.relative_to(ROOT)),'status':'failed','error':str(exc)};traceback.print_exc()
        outcomes.append(item)
    (ROOT/'reports/v6/industry_execution.json').write_text(json.dumps(outcomes,indent=2))
    if any(x['status']!='executed' for x in outcomes):raise SystemExit(1)
if __name__=='__main__':main()
