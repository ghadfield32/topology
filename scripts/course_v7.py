"""Read-only navigator and exact entry checks. Does not mark learner completion."""
from pathlib import Path
import argparse,json,runpy,sys
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'src'))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('start',help='Print the offline reader and first-session paths')
    stage=sub.add_parser('stage',help='Show an entry guide and full stage');stage.add_argument('number',type=int,choices=range(31))
    case=sub.add_parser('case',help='Show one new application or methods lab');case.add_argument('name',choices=['seeds','concrete_slump','leakage','claims'])
    checks=sub.add_parser('check',help='Run exact entry checks; this is not assessment');checks.add_argument('which',choices=['all']+[str(i) for i in range(31)])
    sub.add_parser('verify-new-data',help='Check the two new local snapshots only; no remote download')
    a=p.parse_args()
    if a.command=='start':print(R/'START_HERE.html');print(R/'docs/v7/START.md')
    elif a.command=='stage':
        print(R/f'beginner_v7/{a.number:02d}/lesson.md');print(R/f'stages/{a.number:02d}/README.md');print('Read, predict, calculate, run, explain; record your own evidence.')
    elif a.command=='case':
        cases=json.loads((R/'docs/v7/new_sections.json').read_text());c=next(x for x in cases if x['id']==a.name)
        print(R/c['path']/'lesson.md');print(R/c['path']/'lab.ipynb');print(R/c['learner_notebook'])
    elif a.command=='verify-new-data':
        from shape_lab.evidence_v7 import load_snapshot
        for name in ['seeds','concrete_slump']:
            table,meta=load_snapshot(name);print(name,table.shape,'local hashes/schema passed; independent provider-byte comparison NOT claimed')
    elif a.command=='check':
        stages=range(31) if a.which=='all' else [int(a.which)]
        for n in stages:
            print(f'\nStage {n:02d}')
            runpy.run_path(str(R/f'beginner_v7/{n:02d}/check.py'),run_name='__main__')
        print('\nRequested reference checks passed. No learner assessment was recorded.')
if __name__=='__main__':main()
