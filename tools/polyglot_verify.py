#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path

def run(cmd, cwd):
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
    return {"cmd":cmd,"cwd":str(cwd),"returncode":p.returncode,"stdout":p.stdout[-12000:],"stderr":p.stderr[-12000:]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--require-rust',action='store_true')
    ap.add_argument('--output',default='reports/v14/polyglot_verification.json')
    ns=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    results={"go":{},"rust":{},"manifest":{}}
    spec=json.loads((root/'polyglot/specs/labs.json').read_text())
    results['manifest']={"labs":len(spec['labs']),"unique":len({x['key'] for x in spec['labs']})}
    go=shutil.which('go')
    if go:
        results['go']['version']=run([go,'version'],root)
        results['go']['tests']=run([go,'test','./...'],root/'polyglot/go')
        ids=run([go,'run','./cmd/shape-go','--list'],root/'polyglot/go')
        results['go']['list']=ids
        smoke=[]
        if ids['returncode']==0:
            for lab in [x for x in ids['stdout'].splitlines() if x.strip()]:
                r=run([go,'run','./cmd/shape-go','--repo','../..','--lab',lab],root/'polyglot/go')
                smoke.append({"lab":lab,"returncode":r['returncode']})
        results['go']['smoke']=smoke
        results['go']['passed']=results['go']['tests']['returncode']==0 and len(smoke)==len(spec['labs']) and all(x['returncode']==0 for x in smoke)
    else:
        results['go']={"passed":False,"blocked":"go not found"}
    cargo=shutil.which('cargo'); rustc=shutil.which('rustc')
    if cargo and rustc:
        results['rust']['version']=run([rustc,'--version'],root)
        results['rust']['tests']=run([cargo,'test'],root/'polyglot/rust')
        ids=run([cargo,'run','--quiet','--bin','shape-rust','--','--list'],root/'polyglot/rust')
        results['rust']['list']=ids
        smoke=[]
        if ids['returncode']==0:
            for lab in [x for x in ids['stdout'].splitlines() if x.strip()]:
                r=run([cargo,'run','--quiet','--bin','shape-rust','--','--repo','../..','--lab',lab],root/'polyglot/rust')
                smoke.append({'lab':lab,'returncode':r['returncode']})
        results['rust']['smoke']=smoke
        results['rust']['passed']=(
            results['rust']['tests']['returncode']==0
            and len(smoke)==len(spec['labs'])
            and all(x['returncode']==0 for x in smoke)
        )
    else:
        results['rust']={"passed":False,"blocked":"rustc/cargo not found; compile via rustup, Docker, or CI"}
    out=root/ns.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(results,indent=2)+"\n")
    print(out)
    print(json.dumps({"go":results['go'].get('passed'),"rust":results['rust'].get('passed'),"labs":results['manifest']['labs']},indent=2))
    ok=results['go'].get('passed',False) and (results['rust'].get('passed',False) or not ns.require_rust)
    return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
