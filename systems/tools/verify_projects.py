#!/usr/bin/env python3
"""Reproduce the source-mapped project checks. Blocked dependencies never count as passed."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from systems.python.projects import units,prepare,check
from systems.python.workflow import new_directory,dump

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--units',nargs='*');a=ap.parse_args();selected=units()
 if a.units:
  known={u['id']for u in selected}
  if not set(a.units)<=known:raise ValueError('Unknown systems unit')
  selected=[u for u in selected if u['id']in a.units]
 out=new_directory(a.output);records=[]
 for u in selected:
  ws=prepare(u['id'],out/u['id']);run,status=check(ws,ws/'check01');record=json.loads((run/'project_check.json').read_text());records.append(record);print(u['id'],status,flush=True)
 status='failed'if any(x['status']=='failed'for x in records)else'blocked'if any(x['status']=='blocked'for x in records)else'passed'
 result=dict(status=status,requested_units=[u['id']for u in selected],counts={s:sum(x['status']==s for x in records)for s in ['passed','failed','blocked']},records=records,assessment='not_assessed',scope='actual copied project checks; not every advanced assignment or deployment')
 dump(out/'verification.json',result);return 0 if status=='passed'else 3 if status=='blocked'else 1
if __name__=='__main__':raise SystemExit(main())
