"""Read-only stage navigation and evidence checks for the complete 31-stage course."""
from pathlib import Path
import argparse,sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from shape_lab.learning import read_log,stage_status

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--log',type=Path,default=ROOT/'progress/learning_log_v5.json')
    sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('stage');s.add_argument('number',type=int,choices=range(31))
    sub.add_parser('next');sub.add_parser('verify-evidence')
    a=p.parse_args()
    if a.command=='stage':
        n=a.number;print(ROOT/f'stages/{n:02d}/README.md')
        if n>=21:print(ROOT/f'physics/notebooks/{n:02d}_lab.ipynb')
        else:print(ROOT/f'notebooks/{n:02d}_lab.ipynb')
        return
    log=read_log(a.log)
    if a.command=='next':
        for key in sorted(log['stages']):
            if stage_status(log,int(key)) not in {'demonstrated','retained'}:
                print(f'Stage {int(key):02d}: {stage_status(log,int(key))} — {ROOT/f"stages/{key}/README.md"}');return
        print('All included stages declared demonstrated/retained. This is not an independent grade.');return
    problems=[];checked=0
    for key,item in log['stages'].items():
        for attempt in item['attempts']:
            checked+=1;path=(ROOT/attempt['evidence']).resolve()
            if not path.is_relative_to(ROOT) or not path.is_file():problems.append(f'{key}: missing/invalid evidence {attempt["evidence"]}')
            elif hashlib.sha256(path.read_bytes()).hexdigest()!=attempt['evidence_sha256']:problems.append(f'{key}: changed evidence {attempt["evidence"]}')
    print(json.dumps({'evidence_records_checked':checked,'issues':problems,'grades_verified':False},indent=2))
    if problems:raise SystemExit(1)
if __name__=='__main__':main()
