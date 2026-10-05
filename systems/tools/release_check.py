#!/usr/bin/env python3
"""Check current portal links and loopback serving. No public server or deployment."""
from pathlib import Path
import argparse,hashlib,json,sys,threading,urllib.request,urllib.error
from urllib.parse import urlsplit,unquote
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(ROOT/'src')]
from shape_lab.safe_server import ReaderHandler
from http.server import ThreadingHTTPServer
from functools import partial
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,t,a):
  a=dict(a)
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
  if 'id'in a:self.ids.add(a['id'])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output)
 if out.exists():raise FileExistsError('New output file required')
 pages=[ROOT/'LEARN_TOPOLOGY.html',ROOT/'learning/workbooks/index.html']+list((ROOT/'docs/v17').glob('*.html'))+list((ROOT/'systems').glob('**/*.html'))
 pages=[p for p in pages if not any(s in p.parts for s in ['target','__pycache__'])];count=0;errors=[]
 for p in pages:
  parser=Parser();parser.feed(p.read_text(encoding='utf8'))
  for raw in parser.links:
   u=urlsplit(raw)
   if u.scheme or u.netloc or not u.path:continue
   target=(p.parent/unquote(u.path)).resolve();count+=1
   if not target.is_relative_to(ROOT)or not target.exists():errors.append({'source':p.relative_to(ROOT).as_posix(),'link':raw})
 http={}
 with ThreadingHTTPServer(('127.0.0.1',0),partial(ReaderHandler,directory=str(ROOT)))as server:
  t=threading.Thread(target=server.serve_forever,daemon=True);t.start();port=server.server_port
  for path in ['/LEARN_TOPOLOGY.html','/systems/lessons/sys01.md.html','/systems/evidence/demo/viewer/index.html','/my_work/','/../.git/config','/systems/python/']:
   try:
    with urllib.request.urlopen(f'http://127.0.0.1:{port}'+path,timeout=5)as r:code=r.status
   except urllib.error.HTTPError as e:code=e.code
   http[path]=code
  server.shutdown();t.join()
 expected=[200,200,200,403,403,403]
 result=dict(status='passed'if not errors and list(http.values())==expected else'failed',pages=len(pages),local_targets=count,broken_links=errors,http=http,browser=json.loads((ROOT/'systems/evidence/browser_checks.json').read_text()),scope='static current-route targets, native HTTP and separate rendered-browser checks; actual browser navigation blocked')
 out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return int(result['status']!='passed')
if __name__=='__main__':raise SystemExit(main())
