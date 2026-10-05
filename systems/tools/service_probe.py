#!/usr/bin/env python3
"""Exercise HTTP -> bounded Go worker -> actual native Go Stage01 -> JSON. Loopback only."""
from pathlib import Path
import argparse,json,os,signal,socket,subprocess,sys,time,urllib.request,urllib.error
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from systems.python.workflow import new_directory,command,dump
import native_course

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=new_directory(a.output)
 native=native_course.build('go',out);exe=out/('job-service.exe'if os.name=='nt'else'job-service')
 command(['go','build','-o',exe,'./cmd/job-service'],ROOT/'systems/go_service',out/'service_build.json')
 with socket.socket()as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
 log=(out/'service.log').open('w');proc=subprocess.Popen([str(exe),'--repo',str(ROOT),'--binary',str(native),'--listen',f'127.0.0.1:{port}'],stdout=log,stderr=subprocess.STDOUT)
 base=f'http://127.0.0.1:{port}'
 def request(path,data=None,method=None):
  req=urllib.request.Request(base+path,data=json.dumps(data).encode()if data is not None else None,method=method,headers={'Content-Type':'application/json'})
  with urllib.request.urlopen(req,timeout=5)as r:return r.status,json.load(r)
 try:
  for _ in range(100):
   try:status,health=request('/health');break
   except (OSError,urllib.error.URLError):time.sleep(.05)
  else:raise RuntimeError('Service did not start')
  code,job=request('/jobs',{'lab':'stage01'});assert code==202
  for _ in range(200):
   _,value=request('/jobs/'+job['id'])
   if value['status']not in ['queued','running']:break
   time.sleep(.05)
  assert value['status']=='succeeded',value
  result=value['result'];native_course.validate_result(result,'stage01','go')
  for path,info in result['inputs'].items():assert native_course.digest(ROOT/path)==info['sha256']
  try:request('/jobs',{'lab':'unrecognized'});raise AssertionError('Unknown lab accepted')
  except urllib.error.HTTPError as e:assert e.code==400
  dump(out/'result.json',dict(status='passed',scope='actual loopback HTTP/native integration, not deployed service',job=value,health=health,assessment='not_assessed'))
 finally:
  proc.terminate()
  try:proc.wait(timeout=10)
  except subprocess.TimeoutExpired:proc.kill();proc.wait()
  log.close();dump(out/'shutdown.json',dict(exit_code=proc.returncode,terminated_by_harness=True))
 return 0
if __name__=='__main__':raise SystemExit(main())
