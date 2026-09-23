#!/usr/bin/env python3
"""Actually build/run Docker checks when a local daemon exists; never emulate a pass."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--profile',choices=['core','physics','full'],default='core')
    p.add_argument('--output',type=Path)
    p.add_argument('--probe-only',action='store_true')
    a=p.parse_args()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output=(a.output or ROOT/'my_work'/f'docker-check-{stamp}').resolve()
    if output.exists():raise FileExistsError('Verification output already exists.')
    if output.is_relative_to(ROOT) and not output.is_relative_to(ROOT/'my_work'):raise ValueError('Use my_work or an external directory.')
    output.mkdir(parents=True)
    result={'status':'running','profile':a.profile,'commands':[],'image_build':'not_run','container_tests':'not_run','notebook_run':'not_run'}
    def save(): (output/'docker.json').write_text(json.dumps(result,indent=2)+'\n')
    def run(argv,timeout=None):
        logfile=output/f'{len(result["commands"]):02}_command.log'
        env=dict(os.environ,COURSE_PROFILE=a.profile)
        if hasattr(os,'getuid'):env['COURSE_UID']=str(os.getuid());env['COURSE_GID']=str(os.getgid())
        with logfile.open('w') as f:
            try:code=subprocess.run(argv,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=timeout).returncode
            except subprocess.TimeoutExpired:code=124
        result['commands'].append({'argv':argv,'returncode':code,'log':logfile.name});save()
        print(logfile.read_text(errors='replace'),end='');return code
    if not shutil.which('docker'):
        result.update(status='blocked',reason='Docker CLI is not installed; no image or container was tested.');save();print(json.dumps(result,indent=2));return 2
    for cmd in [['docker','version'],['docker','compose','version'],['docker','info']]:
        if run(cmd,30):result.update(status='blocked',reason='Docker client/Compose/daemon readiness failed.');save();return 2
    if a.probe_only:result.update(status='readiness_only',reason='Build and runtime were not requested.');save();return 0
    if not (ROOT/'uv.lock').is_file():
        result.update(status='blocked',reason='Generate and review uv.lock with tools/bootstrap.py before a locked build.');save();return 2
    (ROOT/'my_work').mkdir(exist_ok=True)
    checks=[('compose_config',['docker','compose','config','--quiet']),
            ('image_build',['docker','compose','build','course']),
            ('container_tests',['docker','compose','run','--rm','course','test','--profile',a.profile,'--output',f'/work/docker-tests-{stamp}']),
            ('notebook_run',['docker','compose','run','--rm','course','run','--stage','0','--output',f'/work/docker-stage00-{stamp}'])]
    for label,cmd in checks:
        code=run(cmd)
        result[label]='passed' if code==0 else 'failed';save()
        if code:result.update(status='failed',reason=label+' failed');save();return 2
    result.update(status='passed',scope='Actual image build, selected profile tests and Stage 00 in containers; not all notebooks/platforms.');save();return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,FileExistsError) as e:print(f'NOT COMPLETED: {e}',file=sys.stderr);raise SystemExit(2)
