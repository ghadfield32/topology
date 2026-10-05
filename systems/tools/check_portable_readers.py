#!/usr/bin/env python3
"""Cross-language binary boundary checks using existing built C/Rust executables."""
from pathlib import Path
import argparse,json,struct,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from systems.python.contract import write_binary,read_binary
from systems.python.workflow import new_directory,dump

def main():
 p=argparse.ArgumentParser();p.add_argument('--c',required=True);p.add_argument('--rust',required=True);p.add_argument('--output',required=True);a=p.parse_args();out=new_directory(a.output)
 rows=[dict(frame=2,time=0.,x=1.,y=2.,z=3.,confidence=None),dict(frame=5,time=.1,x=2.,y=4.,z=6.,confidence=.25)]
 valid=out/'valid.bin';write_binary(valid,rows);raw=valid.read_bytes();variants={'valid':raw,'header_short':raw[:7],'bad_magic':b'BADMAGIC'+raw[8:],'truncated':raw[:-1],'trailing':raw+b'x','empty':raw[:8]+struct.pack('<I',0),'count_huge':raw[:8]+struct.pack('<I',2_000_000)}
 def patch(name,offset,fmt,value):
  b=bytearray(raw);struct.pack_into(fmt,b,offset,value);variants[name]=bytes(b)
 patch('bad_flag',16,'<I',2);patch('unknown_nonzero',52,'<d',.1);patch('known_overone',100,'<d',2.);patch('nan_x',28,'<d',float('nan'));patch('negative_time',20,'<d',-1.);patch('duplicate_time',68,'<d',0.);patch('duplicate_id',60,'<I',2)
 records=[]
 for name,content in variants.items():
  path=out/(name+'.bin')
  if name!='valid':path.write_bytes(content)
  try:
   read_binary(path);python_ok=True
  except (ValueError,struct.error):python_ok=False
  assert python_ok==(name=='valid')
  for lang,cmd in [('c',[a.c,str(path)]),('rust',[a.rust,'--binary',str(path)])]:
   r=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
   ok=(r.returncode==0)==python_ok
   if python_ok:
    v=json.loads(r.stdout);ok=ok and v['count']==2 and v['known_confidence']==1 and v['mean']==[1.5,3.,4.5]
   records.append(dict(language=lang,case=name,expected_accept=python_ok,exit_code=r.returncode,passed=ok,stdout=r.stdout,stderr=r.stderr))
 dump(out/'checks.json',dict(status='passed'if all(x['passed']for x in records)else'failed',count=len(records),checks=records))
 return int(not all(x['passed']for x in records))
if __name__=='__main__':raise SystemExit(main())
