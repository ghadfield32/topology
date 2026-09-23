"""Navigate the optional case track and preserve evidence without changing core logs."""
from pathlib import Path
from datetime import date
import argparse,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from shape_lab import industries as ds, industry_progress as ip

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--log',type=Path,default=R/'progress/industry_log_v6.json')
    sub=p.add_subparsers(dest='action',required=True)
    for name in ['list','verify','status','verify-evidence','handoff','init']:sub.add_parser(name)
    s=sub.add_parser('case');s.add_argument('name',choices=ds.IDS)
    s=sub.add_parser('record');s.add_argument('name',choices=ds.IDS)
    s.add_argument('--kind',choices=['practice','assessment','recall'],required=True)
    s.add_argument('--score',type=float,required=True);s.add_argument('--evidence',required=True)
    s.add_argument('--date',type=date.fromisoformat,default=date.today());s.add_argument('--independent',action='store_true')
    s.add_argument('--critical-clear',action='store_true');s.add_argument('--note',default='')
    a=p.parse_args()
    if a.action=='list':
        for item in json.loads((R/'data/industries/catalog.json').read_text())['datasets']:
            print(f'{item["id"]:12} {item["rows"]:5} rows | {item["sector"]} | {item["title"]}')
    elif a.action=='case':
        print(f'Read industry/lessons/{a.name}.md\nData card industry/cards/{a.name}.md\nRun industry/notebooks/{a.name}.ipynb\nPractice industry/learner/{a.name}.ipynb\nAnswers industry/answers/{a.name}.ipynb')
    elif a.action=='verify':
        for name in ds.IDS:ds.verify_snapshot(name);print(name,': normalized and source hashes verified')
    elif a.action=='init':ip.initialize(a.log);print('Created empty industry log; no existing file replaced.')
    else:
        log=ip.read_log(a.log)
        if a.action=='record':
            ip.record(log,a.name,a.kind,a.score,a.evidence,R,a.date,a.independent,a.critical_clear,a.note)
            ip.write_log(log,a.log);print('Self-reported attempt recorded. This is not automated grading.')
        elif a.action=='verify-evidence':
            rows=ip.verify_evidence(log,R);print(json.dumps(rows,indent=2))
            if any(x['status']!='unchanged' for x in rows):return 1
        elif a.action=='status':
            for name in ds.IDS:print(name,ip.status(log,name),'next review:',ip.next_review(log,name))
        elif a.action=='handoff':
            print('# Industry learning handoff\nCore 31-stage log remains separate. No grade inferred from reference execution.')
            for name in ds.IDS:
                print(f'\n## {name}: {ip.status(log,name)}')
                for x in log['cases'][name]['attempts'][-2:]:print(x['date'],x['kind'],x['score'],x['evidence'],x.get('note',''))
    return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError) as e:print(f'Error: {e}',file=sys.stderr);raise SystemExit(2)
