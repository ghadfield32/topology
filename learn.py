#!/usr/bin/env python3
"""One front door. Existing course.py and native_course.py remain authoritative execution tools."""
from pathlib import Path
import argparse,json,subprocess,sys
from systems.python.workflow import ROOT,new_directory,dump,run_demo
from systems.python.projects import prepare,check,units

def main(argv=None):
 ap=argparse.ArgumentParser(description=__doc__);sp=ap.add_subparsers(dest='command',required=True)
 sp.add_parser('list');sp.add_parser('doctor')
 p=sp.add_parser('show');p.add_argument('unit')
 p=sp.add_parser('session');p.add_argument('--lab',default='stage01');p.add_argument('--output',required=True)
 p=sp.add_parser('project');p.add_argument('--unit',required=True);p.add_argument('--output',required=True)
 p=sp.add_parser('check-project');p.add_argument('--workspace',required=True);p.add_argument('--output',required=True)
 p=sp.add_parser('demo');p.add_argument('--output',required=True)
 p=sp.add_parser('verify-projects');p.add_argument('--output',required=True);p.add_argument('--units',nargs='*')
 p=sp.add_parser('workbooks');p.add_argument('--check',action='store_true')
 a=ap.parse_args(argv)
 try:
  labs=json.loads((ROOT/'native/protocols/labs.json').read_text())['labs']
  if a.command=='list':
   print('TOPOLOGY / EXISTING APPLICATIONS');[print(x['key'],x['title'])for x in labs];print('\nSOURCE-MAPPED ENGINEERING PROJECTS');[print(x['id'],x['title'])for x in units()];return 0
  if a.command=='doctor':
   import shutil
   print(json.dumps({x:shutil.which(x)for x in ['python','uv','go','cargo','rustc','cc','g++','cmake','node','tsc','docker','kubectl','nvcc']},indent=2));print('Availability is not deployment acceptance. No installs performed.');return 0
  if a.command=='show':
   if a.unit.startswith('sys'):path=next(x['lesson']for x in units()if x['id']==a.unit)
   else:path=next(x['lesson']for x in labs if x['key']==a.unit)
   print((ROOT/path).read_text(encoding='utf8'));return 0
  if a.command=='project':out=prepare(a.unit,a.output)
  elif a.command=='check-project':
   out,status=check(a.workspace,a.output);print(out/'project_check.json');return 0 if status=='passed'else 3 if status=='blocked'else 1
  elif a.command=='demo':out=run_demo(a.output)
  elif a.command=='verify-projects':
   cmd=[sys.executable,ROOT/'systems/tools/verify_projects.py','--output',a.output]
   if a.units:cmd+=['--units',*a.units]
   return subprocess.run(cmd,cwd=ROOT).returncode
  elif a.command=='workbooks':
   cmd=[sys.executable,ROOT/'systems/tools/generate_workbooks.py'];
   if a.check:cmd+=['--check']
   return subprocess.run(cmd,cwd=ROOT).returncode
  else:
   lab=next((x for x in labs if x['key']==a.lab),None)
   if lab is None:raise ValueError('Unknown lab')
   out=new_directory(a.output)
   # Native prepare knows how to redirect private Cargo vendor paths and copies actual source.
   subprocess.run([sys.executable,ROOT/'native_course.py','prepare','--lab',a.lab,'--output',out/'native'],cwd=ROOT,check=True)
   if a.lab!='poux_bridge':
    key=str(int(a.lab[5:]))if a.lab.startswith('stage')else a.lab
    subprocess.run([sys.executable,ROOT/'course.py','practice',key,'--output',out/'python'],cwd=ROOT,check=True)
   for name in ['prediction.md','reflection.md']:(out/name).write_text('# '+name[:-3]+'\n\n## Explain\n\n## Predict\n\n## Implement\n\n## Break\n\n## Apply\n\n## What surprised me\n\n## Why it failed\n\n## Comparison to Python\n\n## Limitation\n\n## Next independent problem\n',encoding='utf8')
   dump(out/'session.json',dict(lab=a.lab,assessment='not_assessed',source_lesson=lab['lesson'],native_protocol=lab['native_protocol']))
   (out/'START.md').write_text(f'# {lab["title"]}\n\nRead `{ROOT/lab["lesson"]}` once. Use `native/START.md` for commands that compile your edited native source. Python uses its private learner notebook. Reference runs are separate from your implementation.\n\nExplain → Predict → Implement → Break → Apply. Keep every attempt; no automatic grading.\n')
  print(out/'START.md'if (out/'START.md').exists()else out/'index.html');return 0
 except (OSError,ValueError,StopIteration,RuntimeError,subprocess.SubprocessError)as e:print('ERROR:',e,file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
