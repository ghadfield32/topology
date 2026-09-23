#!/usr/bin/env python3
"""Resolve and sync a real uv environment, or explicitly audit installed dependencies.

--reuse-installed is an offline diagnostic mode, not a fresh dependency install.
Normal setup never falls back to that mode silently. Output is an evidence folder.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from shape_lab.release import EXTRAS

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',choices=list(EXTRAS),default='core')
    parser.add_argument('--reuse-installed',action='store_true',help='Explicit offline diagnostic, not a fresh dependency install.')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--timeout',type=int,default=900,help='Maximum seconds per uv or validation command; default 900.')
    args=parser.parse_args()
    if args.timeout<1:parser.error('--timeout must be positive.')
    uv=shutil.which('uv')
    if uv is None:
        print('uv is missing. Install the pinned tool: python -m pip install uv==0.10.0',file=sys.stderr);return 2
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output=(args.output or ROOT/'my_work'/f'setup-{stamp}').resolve()
    if output.exists():raise FileExistsError('Setup output exists; use a new directory.')
    if output.is_relative_to(ROOT) and not output.is_relative_to(ROOT/'my_work'):
        raise ValueError('Setup outputs belong under my_work or outside the repository.')
    output.mkdir(parents=True)
    record={'profile':args.profile,'mode':'reuse_installed_not_independent' if args.reuse_installed else 'uv_resolved_install',
            'fresh_dependency_install':False,'commands':[],'status':'running'}
    def save(): (output/'setup.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    def run(cmd: list[str]) -> int:
        log=output/f'{len(record["commands"]):02}_command.log'
        print('+ '+' '.join(cmd),flush=True)
        with log.open('w',encoding='utf-8') as stream:
            try:code=subprocess.run(cmd,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=args.timeout).returncode
            except subprocess.TimeoutExpired:
                code=124;stream.write(f'\nTimed out after {args.timeout} seconds. No fallback environment selected.\n')
            except OSError as exc:
                code=2;stream.write(f'\nCould not execute command: {exc}\n')
        print(log.read_text(encoding='utf-8',errors='replace'),end='',flush=True)
        record['commands'].append({'argv':cmd,'returncode':code,'log':log.name,'timeout_seconds':args.timeout});save()
        return code
    save()
    venv_existed=(ROOT/'.venv').exists()
    record['venv_existed_before_setup']=venv_existed
    if not args.reuse_installed:
        from shape_lab.runtime import assert_clean_setup_target
        try: assert_clean_setup_target(ROOT/'.venv')
        except ValueError as exc:
            record.update(status='blocked',reason=str(exc));save();return 2
    if args.reuse_installed:
        print('DIAGNOSTIC: reuses installed system site-packages; this is not a fresh dependency install.',flush=True)
        if (ROOT/'.venv').exists():
            record.update(status='blocked',reason='Refusing to replace an existing .venv in diagnostic mode.');save();return 2
        commands=[[uv,'venv','--offline','--system-site-packages','--python',sys.executable,str(ROOT/'.venv')]]
        python=ROOT/'.venv'/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
        commands.append([uv,'pip','install','--offline','--no-deps','--no-build-isolation','--python',str(python),'-e','.'])
    else:
        commands=[[uv,'lock','--check']] if (ROOT/'uv.lock').exists() else [[uv,'lock']]
        cmd=[uv,'sync','--locked']
        for extra in EXTRAS[args.profile]:cmd+=['--extra',extra]
        commands.append(cmd)
        python=ROOT/'.venv'/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
    for index,cmd in enumerate(commands):
        if run(cmd)!=0:
            record.update(status='blocked',reason='A required uv step did not complete. No fallback environment was silently selected.');save();return 2
        if args.reuse_installed and index==0:
            # include-system-site-packages alone points at the *base interpreter*,
            # not the currently active outer venv. Record that explicit reuse.
            import site
            from shape_lab.runtime import write_reuse_sites
            purelib=Path(subprocess.check_output([str(python),'-c',
                "import sysconfig; print(sysconfig.get_path('purelib'))"],text=True).strip())
            active=[p for p in site.getsitepackages() if Path(p).is_dir()]
            write_reuse_sites(purelib,active)
            record['inherited_site_paths']=active;save()
    rc=run([str(python),str(ROOT/'course.py'),'verify','--profile',args.profile])
    if rc==0: rc=run([str(python),str(ROOT/'course.py'),'init'])
    record.update(status='passed' if rc==0 else 'failed',fresh_dependency_install=(not args.reuse_installed and not venv_existed and rc==0),
                  notice='This setup check is separate from unit tests, notebook execution and Docker verification.')
    save();print('Setup evidence:',output)
    return 0 if rc==0 else 2
if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,FileExistsError) as e:print(f'NOT COMPLETED: {e}',file=sys.stderr);raise SystemExit(2)
