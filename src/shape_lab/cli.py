"""One course route: no downloads without an explicit setup request."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
from .course import load_catalog,stage_plan,run_references
from .release import validate_course,environment_status,verify_manifest,run_tests

def main(root: Path, argv: list[str]|None=None) -> int:
    p=argparse.ArgumentParser(description='Listening to Shape: read, practice, run and verify without changing source data.')
    sub=p.add_subparsers(dest='command',required=True)
    for name in ['list','next','cases','handoff','datasets','init']:sub.add_parser(name)
    for name in ['stage','check']:
        a=sub.add_parser(name);a.add_argument('stage',type=int,choices=range(31))
    for name in ['doctor','verify']:
        a=sub.add_parser(name);a.add_argument('--profile',choices=['core','physics','full'],default='core')
        if name=='verify':a.add_argument('--integrity',action='store_true')
    a=sub.add_parser('test');a.add_argument('--profile',choices=['core','physics','full'],default='core');a.add_argument('--output',type=Path,required=True)
    a=sub.add_parser('run');g=a.add_mutually_exclusive_group(required=True)
    g.add_argument('--stage',type=int,choices=range(31));g.add_argument('--all',action='store_true');g.add_argument('--acb',action='store_true');g.add_argument('--case')
    a.add_argument('--output',type=Path,required=True);a.add_argument('--jobs',type=int,default=1,choices=range(1,5))
    a.add_argument('--timeout',type=int,default=300)
    a=sub.add_parser('acceptance');a.add_argument('--profile',choices=['core','physics','full'],default='core');a.add_argument('--references',choices=['first','all'],default='first');a.add_argument('--jobs',type=int,choices=range(1,5),default=1);a.add_argument('--timeout',type=int,default=300);a.add_argument('--output',type=Path,required=True)
    a=sub.add_parser('practice');a.add_argument('item');a.add_argument('--output',type=Path,required=True)
    a=sub.add_parser('serve');a.add_argument('--port',type=int,default=8000)
    a=sub.add_parser('setup');a.add_argument('--profile',choices=['core','physics','full'],default='core')
    args=p.parse_args(argv)
    def show(obj):print(json.dumps(obj,indent=2))
    if args.command=='acceptance':
        from .acceptance import run_acceptance
        d=run_acceptance(root,args.output,args.profile,args.references,args.jobs,args.timeout);show(d);return int(d['status']!='passed')
    elif args.command=='practice':
        from .practice_workspace import prepare_practice
        show(prepare_practice(root,args.item,args.output))
    elif args.command=='init':
        from .runtime import initialize_progress
        show({'created':initialize_progress(root),'existing_records':'preserved','learner_assessment':'not_assessed'})
    elif args.command=='list':
        print('\n'.join(f"{s['id']} {s['title']}" for s in load_catalog(root)['stages']))
    elif args.command=='stage':show(stage_plan(root,args.stage))
    elif args.command=='check':return subprocess.run([sys.executable,str(root/f'beginner_v7/{args.stage:02}/check.py')],cwd=root).returncode
    elif args.command=='doctor':
        d=environment_status(root,args.profile);show(d);return int(not d['compatible'])
    elif args.command=='verify':
        d=validate_course(root,args.profile)
        if args.integrity:
            d['archive_integrity']=verify_manifest(root)
            if d['archive_integrity']['status']!='passed':d['status']='failed'
        show(d);return int(d['status']!='passed')
    elif args.command=='test':
        d=run_tests(root,args.output,args.profile);show(d);return int(d['returncode'])
    elif args.command=='run':
        if args.all:targets=load_catalog(root)['reference_notebooks']
        elif args.acb:targets=['sports_v9/notebooks/acb_readiness.ipynb']
        elif args.case:
            cases=json.loads((root/'curriculum/experiments.json').read_text())['experiments']
            match=[x for x in cases if x['id']==args.case]
            if not match:raise ValueError('Unknown case; use python course.py cases.')
            targets=[match[0]['notebook']]
        else:targets=[stage_plan(root,args.stage)['reference_lab']]
        d=run_references(root,targets,args.output,args.jobs,args.timeout)
        print(json.dumps({'passed':d['passed'],'failed':d['failed'],'source_inputs_unchanged':d['source_inputs_unchanged'],
                          'report':str(args.output/'execution.json')},indent=2));return int(bool(d['failed']))
    elif args.command=='cases':
        for e in json.loads((root/'curriculum/experiments.json').read_text())['experiments']:
            print(f"{e['id']:22} {e['title']} | {e['data_status']}")
    elif args.command=='datasets':print((root/'docs/release/DATA_AND_SPORTS.md').read_text())
    elif args.command=='serve':
        if not 1024<=args.port<=65535:raise ValueError('Use a local port between 1024 and 65535.')
        from .safe_server import serve
        serve(root,args.port)
    elif args.command=='setup':return subprocess.run([sys.executable,str(root/'tools/bootstrap.py'),'--profile',args.profile],cwd=root).returncode
    elif args.command=='next':
        from .learning import read_log,new_log,stage_status
        path=root/'progress/learning_log_v5.json';log=read_log(path) if path.exists() else new_log(stage_count=31)
        for s in load_catalog(root)['stages']:
            state=stage_status(log,int(s['id']))
            if state not in ('retained','demonstrated'):
                show(dict(stage=s['id'],title=s['title'],recorded_status=state,lesson=s['lesson'],
                          next_command=f"python course.py run --stage {int(s['id'])} --output my_work/stage{s['id']}_attempt01",
                          notice='Learner evidence is self-recorded, not an independent assessment.'));break
        else:print('Review delayed recall and independent capstone evidence.')
    elif args.command=='handoff':return subprocess.run([sys.executable,str(root/'scripts/learn.py'),'handoff'],cwd=root).returncode
    return 0
