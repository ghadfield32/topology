"""Read-only v4 study navigation and evidence integrity. No network or grading."""
from __future__ import annotations
import argparse,json,sys,platform,hashlib,importlib.metadata
from pathlib import Path
from datetime import date
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from shape_lab.learning import read_log,stage_status,due_stages
from shape_lab.audits import verify_evidence


def show(value):
    print(json.dumps(value,indent=2,allow_nan=False))


def doctor():
    basic=json.loads((ROOT/'data/manifest.json').read_text())
    stereo=json.loads((ROOT/'data/stereo/manifest.json').read_text())
    solar=json.loads((ROOT/'data/time_series/manifest.json').read_text())
    expected={k:v['sha256'] for k,v in basic['files'].items() if k.endswith(('iris.csv','digits.npz'))}
    expected['data/stereo/motorcycle.npz']=stereo['files']['motorcycle.npz']
    expected['data/time_series/sunspots_yearly.csv']=solar['sha256']
    files=[]
    for name,digest in expected.items():
        p=ROOT/name
        actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        files.append({'file':name,'status':'matches' if actual==digest else 'missing' if actual is None else 'modified','sha256':actual})
    versions={}
    for name in ('numpy','scipy','pandas','matplotlib','scikit-learn','nbformat','nbclient','pytest','ripser','gudhi'):
        try:versions[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:versions[name]=None
    required=('numpy','scipy','pandas','matplotlib','scikit-learn')
    ok=sys.version_info>=(3,11) and all(versions[k] for k in required) and all(x['status']=='matches' for x in files)
    show({'python':platform.python_version(),'platform':platform.platform(),'network_calls':0,
          'data':files,'packages':versions,'core_ready':ok,
          'scope':'Presence and data-integrity checks only; run pytest for behavioral tests. Optional packages may be absent.'})
    return 0 if ok else 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log',type=Path,default=ROOT/'progress/learning_log_v3.json',help='Existing v3-compatible 21-stage log; never overwritten')
    sub=parser.add_subparsers(dest='command',required=True)
    stage=sub.add_parser('stage');stage.add_argument('number',type=int,choices=range(21))
    sub.add_parser('next');sub.add_parser('verify-evidence');sub.add_parser('doctor')
    args=parser.parse_args()
    if args.command=='doctor':return doctor()
    metadata=json.loads((ROOT/'docs/session_metadata_v4.json').read_text())
    if args.command=='stage':
        s=metadata[args.number]
        show({'stage':s['stage'],'title':s['title'],'focus':s['focus'],'outcomes':s['outcomes'],
              'prerequisites':s['prerequisites'],'session':s['paths']['guided_session'],
              'consolidation':s['paths']['consolidation'],'sequence':s['paths'],
              'data_role':s['data_role'],'automatic_assessment':False})
        return 0
    try:log=read_log(args.log)
    except (OSError,ValueError) as exc:parser.error(str(exc))
    if len(log['stages'])!=21:parser.error('Use the included v2-to-v3 migration for a legacy 13-stage log first.')
    if args.command=='verify-evidence':
        checks=verify_evidence(log,ROOT)
        failures=[x for x in checks if x['status']!='matches']
        show({'checked_files':len(checks),'assessment':'no_recorded_evidence' if not checks else 'integrity_only_not_correctness',
              'records':checks,'problems':len(failures),'log_modified':False})
        return 1 if failures else 0
    needs=[n for n in range(21) if stage_status(log,n)=='needs_review']
    due=due_stages(log,date.today())
    unfinished=[n for n in range(21) if stage_status(log,n) not in {'demonstrated','retained'}]
    selection=needs or due or unfinished
    reason='repair_required' if needs else 'review_due' if due else 'first_unfinished' if unfinished else 'all_declared_demonstrated'
    n=selection[0] if selection else None
    show({'stage':n,'reason':reason,'session':metadata[n]['paths']['guided_session'] if n is not None else None,
          'note':'Based on your recorded declarations, not automatic proof checking. Complete required independent capstones and book audit separately.','log_modified':False})
    return 0

if __name__=='__main__':raise SystemExit(main())
