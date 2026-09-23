"""Local course progress. See `python scripts/learn.py --help`. No network calls."""
from pathlib import Path
from datetime import date
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from shape_lab.learning import new_log, record, stage_status, next_review, due_stages, write_log, read_log


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--log',type=Path,default=ROOT/'progress/learning_log_v5.json')
    s=p.add_subparsers(dest='command',required=True)
    s.add_parser('status');s.add_parser('due');s.add_parser('handoff')
    r=s.add_parser('record')
    r.add_argument('--stage',type=int,required=True)
    r.add_argument('--kind',choices=['practice','assessment','recall'],required=True)
    r.add_argument('--score',type=float,required=True)
    r.add_argument('--evidence',required=True,help='Existing path relative to course root')
    r.add_argument('--date',type=date.fromisoformat,default=date.today(),help='ISO date; defaults to local today')
    r.add_argument('--independent',action='store_true')
    r.add_argument('--critical-clear',action='store_true')
    r.add_argument('--note',default='')
    a=p.parse_args()
    log=read_log(a.log) if a.log.exists() else new_log(stage_count=31)
    if a.command=='record':
        if a.date>date.today():p.error('Do not record a future learning attempt.')
        try:record(log,a.stage,a.kind,a.score,a.evidence,ROOT,a.date,a.independent,a.critical_clear,a.note)
        except ValueError as e:p.error(str(e))
        write_log(log,a.log)
        print(f'Stage {a.stage:02d}: {stage_status(log,a.stage)}. Evidence recorded, not independently certified.')
    elif a.command=='due':
        due=due_stages(log,date.today())
        print('Due stages: '+(', '.join(f'{n:02d}' for n in due) or 'none. Begin your next unfinished stage.'))
    elif a.command=='status':
        for n in map(int,sorted(log['stages'])):print(f'{n:02d}  {stage_status(log,n):15s}  next review: {next_review(log,n) or "not scheduled"}')
    else:
        print('# Continue my Listening to Shape course\n\nUse the included stages and my evidence; do not assume prior mastery.')
        for n in map(int,sorted(log['stages'])):
            attempts=log['stages'][f'{n:02d}']['attempts']
            print(f'\nStage {n:02d}: {stage_status(log,n)}')
            if attempts:
                e=attempts[-1]
                print(f'Latest: {e["kind"]}, {e["score"]}/100, {e["date"]}; evidence: {e["evidence"]}; note: {e["note"]}')
        print('\nAsk me to explain the next unfamiliar concept, review my work, and repair gaps before advancing.')

if __name__=='__main__':main()
