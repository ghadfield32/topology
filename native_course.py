#!/usr/bin/env python3
"""Build/run native learning experiments; never substitute a Python computation for a native lab.

The Python course remains canonical. This runner tests new common Go/Rust teaching
protocols. Agreement here does not certify all original Python-notebook operations.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, html, importlib.util, json, math, os
from pathlib import Path
import shutil, subprocess, sys, time

ROOT=Path(__file__).resolve().parent
LANGUAGES=('go','rust')

def read_json(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write_json(p,v): Path(p).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def digest(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def available_labs(root=ROOT):return read_json(root/'native/protocols/labs.json')['labs']
def new_directory(p):
    p=Path(p)
    if p.exists() or p.is_symlink():raise FileExistsError(f'Choose a NEW output directory: {p}')
    p.parent.mkdir(parents=True,exist_ok=True);p.mkdir();return p.resolve()
def compare_values(a,b,atol=1e-8,rtol=1e-7):
    errs=[];count=0;maximum=0.
    def visit(x,y,path):
        nonlocal count,maximum
        if isinstance(x,bool) or isinstance(y,bool):
            if type(x)!=type(y) or x!=y:errs.append((path,x,y))
        elif isinstance(x,(int,float)) and isinstance(y,(int,float)):
            count+=1;d=abs(x-y);maximum=max(maximum,d)
            if (isinstance(x,int) and isinstance(y,int) and x!=y) or not math.isfinite(d) or d>atol+rtol*max(abs(x),abs(y)):errs.append((path,x,y))
        elif isinstance(x,dict) and isinstance(y,dict):
            if x.keys()!=y.keys():errs.append((path,sorted(x),sorted(y)))
            for k in sorted(x.keys()&y.keys()):visit(x[k],y[k],f'{path}.{k}')
        elif isinstance(x,list) and isinstance(y,list):
            if len(x)!=len(y):errs.append((path,len(x),len(y)))
            for i,(u,v) in enumerate(zip(x,y)):visit(u,v,f'{path}[{i}]')
        elif x!=y:errs.append((path,x,y))
    visit(a,b,'$')
    return dict(passed=not errs,numeric_values_compared=count,max_absolute_difference=maximum,
                abs_tolerance=atol,rel_tolerance=rtol,discrepancy_count=len(errs),discrepancies=errs[:25])
def validate_result(result,key,language):
    if not isinstance(result,dict) or result.get('schema')!='shape.native.v16':raise ValueError('Wrong result schema')
    if result.get('lab')!=key or result.get('language')!=language or result.get('status')!='completed':raise ValueError('Wrong/missing result identity or status')
    metrics=result.get('metrics')
    if not isinstance(metrics,dict) or not metrics or set(metrics)<= {'implemented','rows','columns'}:raise ValueError('No substantive experiment result')
    if not isinstance(result.get('inputs'),dict):raise ValueError('Missing input audit')
    json.dumps(result,allow_nan=False)
def audit_registry(root=ROOT):
    records=[]
    for row in read_json(root/'native/data_registry.json')['files']:
        p=(root/row['path']).resolve()
        try:p.relative_to(root.resolve())
        except ValueError:raise ValueError('Dataset registry path escapes root')
        ok=p.is_file() and p.stat().st_size==row['bytes'] and digest(p)==row['sha256']
        records.append({'path':row['path'],'passed':ok})
    return {'passed':bool(records) and all(x['passed']for x in records),'files':records}
def fingerprints(root=ROOT):
    paths=set(row['path'] for row in read_json(root/'native/data_registry.json')['files'])
    paths.update(['polyglot/specs/labs.json','curriculum/catalog.json','native_course.py','native/data_registry.json','native/python/data_audit.py','native/python/scientific_checks.py'])
    for folder in ['native/go','native/rust/src','native/rust/.cargo','native/protocols']:
        for p in (root/folder).rglob('*'):
            if p.is_file() and p.suffix in ['.go','.rs','.toml','.json','.mod']:paths.add(p.relative_to(root).as_posix())
    paths.update(['native/rust/Cargo.toml','native/rust/Cargo.lock'])
    return {p:digest(root/p)for p in sorted(paths)}
def source_id(lang,root=ROOT):
    paths=list((root/'native'/lang).rglob('*.go'if lang=='go'else '*.rs'))
    if lang=='rust':paths=[p for p in paths if 'vendor'not in p.parts]
    paths.extend([root/'native'/lang/('go.mod'if lang=='go'else'Cargo.toml')])
    if lang=='rust':paths.extend([root/'native/rust/Cargo.lock',root/'native/rust/.cargo/config.toml'])
    h=hashlib.sha256()
    for p in sorted(paths):h.update(p.relative_to(root).as_posix().encode());h.update(p.read_bytes())
    return h.hexdigest()
def command(cmd,cwd,log,env=None,timeout=900):
    start=time.monotonic()
    try:
        p=subprocess.run([str(x)for x in cmd],cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
        record={'command':[str(x)for x in cmd],'cwd':str(cwd),'exit_code':p.returncode,'seconds':time.monotonic()-start,'stdout':p.stdout,'stderr':p.stderr}
    except (OSError,subprocess.TimeoutExpired) as e:
        record={'command':[str(x)for x in cmd],'cwd':str(cwd),'exit_code':-1,'seconds':time.monotonic()-start,'error':str(e),'stdout':'','stderr':''}
    write_json(log,record)
    if record['exit_code']!=0:raise RuntimeError(f'Command failed; inspect {log}')
    return record

def build(lang,out,root=ROOT,force=False):
    tool=shutil.which('go' if lang=='go' else 'cargo')
    if not tool:raise RuntimeError(f'{lang} compiler unavailable; see native/guides/SETUP.md')
    cache=root/'my_work/native_build'/lang;cache.mkdir(parents=True,exist_ok=True)
    exe=cache/('shape-'+lang+('.exe'if os.name=='nt'else''));stamp=cache/'build.json'
    signature=source_id(lang,root)
    version=command([tool,'version'] if lang=='go' else [tool,'--version'],root,out/(lang+'_version.json'),timeout=30)['stdout'].strip()
    key={'source_sha256':signature,'compiler':version,'platform':sys.platform}
    if not force and exe.is_file() and stamp.is_file() and read_json(stamp).get('key')==key and read_json(stamp).get('binary_sha256')==digest(exe):
        write_json(out/(lang+'_build_reuse.json'),{'status':'verified_cache','key':key,'binary_sha256':digest(exe)});return exe
    env=os.environ.copy();env['PYTHONUTF8']='1'
    if lang=='go':
        env['GOTOOLCHAIN']='local';env['GOWORK']='off'
        cmd=[tool,'build','-trimpath','-o',str(exe),'./cmd/shape-go']
    else:
        env['CARGO_TARGET_DIR']=str(cache/'target');env['CARGO_NET_OFFLINE']='true'
        cmd=[tool,'build','--offline','--locked','--release']
    command(cmd,root/'native'/lang,out/(lang+'_build.json'),env=env)
    if lang=='rust':shutil.copy2(cache/'target/release'/exe.name,exe)
    write_json(stamp,{'key':key,'binary_sha256':digest(exe),'created_at':now()})
    return exe

def unit_tests(lang,out,root=ROOT):
    tool=shutil.which('go'if lang=='go'else'cargo')
    if not tool:raise RuntimeError(f'{lang} compiler absent')
    env=os.environ.copy();env['GOTOOLCHAIN']='local';env['GOWORK']='off';env['CARGO_TARGET_DIR']=str(root/'my_work/native_build/rust/target');env['CARGO_NET_OFFLINE']='true'
    cmd=[tool,'test','-count=1','-json','./...'] if lang=='go'else[tool,'test','--offline','--locked']
    record=command(cmd,root/'native'/lang,out/(lang+'_tests.json'),env=env)
    if lang=='go':
        events=[json.loads(line)for line in record['stdout'].splitlines() if line.strip()];passed=sum(x.get('Action')=='pass' and 'Test'in x for x in events)
    else:
        import re
        passed=sum(int(x)for x in re.findall(r'test result: ok\. (\d+) passed',record['stdout']))
    if passed<=0:raise RuntimeError('Empty native test suite is not acceptance')
    return {'language':lang,'passed':passed,'exit_code':record['exit_code']}

def execute_lab(lang,key,exe,out,root=ROOT):
    folder=out/lang;folder.mkdir(exist_ok=True)
    record=command([exe,'--repo',root,'--lab',key],root,folder/(key+'.execution.json'),timeout=300)
    result=json.loads(record['stdout']);validate_result(result,key,lang)
    for path,info in result['inputs'].items():
        full=(root/path).resolve();full.relative_to(root.resolve())
        if not full.is_file() or digest(full)!=info['sha256']:raise ValueError('Consumed source hash mismatch: '+path)
    write_json(folder/(key+'.json'),result)
    return result

def run_labs(languages,keys,out,root=ROOT):
    before=fingerprints(root);runs={};comparisons=[]
    binaries={lang:build(lang,out,root)for lang in languages}
    for key in keys:
        runs[key]={}
        for lang in languages:
            print(f'{lang}: {key}',flush=True);runs[key][lang]=execute_lab(lang,key,binaries[lang],out,root)
        if len(languages)==2:
            go,rust=runs[key]['go'],runs[key]['rust']
            c=compare_values(go['metrics'],rust['metrics']);c['lab']=key
            c['input_hashes_identical']=go['inputs']==rust['inputs']
            c['passed']=c['passed']and c['input_hashes_identical'];comparisons.append(c)
    after=fingerprints(root)
    result={'schema':'shape.native.run.v16','created_at':now(),'languages':list(languages),'expected_labs':keys,
      'completed':{lang:[k for k in keys if lang in runs[k]]for lang in languages},
      'source_inputs_unchanged':before==after,'source_fingerprints':before,'comparisons':comparisons,
      'status':'passed'if before==after and all(c['passed']for c in comparisons)else'failed',
      'scope':'new shared native teaching protocols; NOT all 133 original Python notebook protocols',
      'original_notebook_parity':'not_certified','docker_runtime':'not_run','kubernetes_runtime':'not_run',
      'identity':run_identity(languages,binaries,before)}
    write_json(out/'execution.json',result)
    return result

def run_identity(languages,binaries,fingerprints_map):
    """Bind which source, which binaries and which inputs produced this run.

    This is what lets a later reader tell a current run from a stale one instead
    of trusting whichever evidence file happens to be newest on disk.
    """
    import hashlib as _h
    return {
        'protocol':'native16',
        'runner_schema':'shape.native.run.v16',
        'languages':{
            lang:{'source_sha256':source_id(lang,ROOT),
                  'binary_sha256':digest(binaries[lang])if Path(binaries[lang]).is_file()else None}
            for lang in languages},
        'input_fingerprints_sha256':_h.sha256(
            json.dumps(fingerprints_map,sort_keys=True).encode()).hexdigest(),
        'input_file_count':len(fingerprints_map),
    }

def load_oracle(root=ROOT):
    spec=importlib.util.spec_from_file_location('shape_native_decoder_oracle',root/'native/python/data_audit.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def verify_data(langs,out,root=ROOT,fixtures=False):
    oracle=load_oracle(root);before=audit_registry(root)
    if not before['passed']:raise ValueError('Registered dataset hash mismatch')
    paths=[r['path']for r in read_json(root/'native/data_registry.json')['files']]
    if fixtures:paths=[p.relative_to(root).as_posix()for p in sorted((root/'native/tests/fixtures').iterdir()) if not p.name.startswith('invalid_')]
    records=[]
    for lang in langs:
        exe=build(lang,out,root)
        for path in paths:
            expected=oracle.decode(root,path)
            p=subprocess.run([str(exe),'--repo',str(root),'--decode',path],capture_output=True,text=True,encoding='utf8',timeout=90)
            r={'language':lang,'path':path,'exit_code':p.returncode}
            if p.returncode:r.update(passed=False,error=p.stderr[-1500:])
            else:r.update(oracle.differences(expected,json.loads(p.stdout)))
            records.append(r)
        if fixtures:
            for pth in sorted((root/'native/tests/fixtures').glob('invalid_*')):
                p=subprocess.run([str(exe),'--repo',str(root),'--decode',pth.relative_to(root).as_posix()],capture_output=True,text=True,encoding='utf8',timeout=30)
                records.append({'language':lang,'path':pth.relative_to(root).as_posix(),'expected':'reject','passed':p.returncode!=0,'exit_code':p.returncode})
    result={'status':'passed'if all(r['passed']for r in records)else'failed','checks':records,'checks_count':len(records),'full_value_equality':True,'numeric_values_compared':sum(r.get('numeric_values_compared',0)for r in records),'sources_unchanged':before==audit_registry(root)}
    if not result['sources_unchanged']:result['status']='failed'
    write_json(out/('reader_fixtures.json'if fixtures else'data_comparison.json'),result);return result

def report_page(out,title,status):
    links=[]
    for p in sorted(out.rglob('*.json')):
        if 'target'not in p.parts:links.append(f'<li><a href="{html.escape(p.relative_to(out).as_posix())}">{html.escape(p.relative_to(out).as_posix())}</a></li>')
    text=f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{html.escape(title)}</title><style>body{{font:18px/1.55 system-ui;max-width:1000px;margin:40px auto;padding:0 20px}}a{{overflow-wrap:anywhere}} code{{font-size:.85em}}</style><h1>{html.escape(title)}</h1><p>Status: <strong>{html.escape(status)}</strong></p><p>These records concern native v16 protocols. A native pass does not certify original-notebook equivalence, deployment, scientific meaning, or learner mastery.</p><ul>{''.join(links)}</ul>'''
    (out/'index.html').write_text(text,encoding='utf8')

def prepare(key,out,root=ROOT):
    entry=next(r for r in available_labs(root)if r['key']==key)
    for lang in LANGUAGES:
        dest=out/lang
        shutil.copytree(root/'native'/lang,dest,ignore=shutil.ignore_patterns('vendor','target','__pycache__'))
        if lang=='rust':
            (dest/'.cargo').mkdir(exist_ok=True)
            (dest/'.cargo/config.toml').write_text('[source.crates-io]\nreplace-with = "vendored-sources"\n[source.vendored-sources]\ndirectory = '+json.dumps(str(root/'native/rust/vendor'))+'\n',encoding='utf8')
        for p in dest.rglob('*'):
            if p.is_file():p.chmod(p.stat().st_mode|0o200)
    spec=read_json(root/'native/protocols/labs.json');details=next(r for r in spec['labs']if r['key']==key)
    directions=f'''# {key}: private native practice

You are copying **worked source**, not receiving an assessed submission. Read the primary lesson once at `{root/entry['lesson']}`. The native guide is `{root/'native/guides/labs'/f'{key}.md'}`.

## Independent challenges
'''+'\n'.join(f'{i+1}. {x}'for i,x in enumerate(details['challenges']))+f'''

## Run your edits

From the `go` subdirectory:
```
go test -count=1 ./...
go run ./cmd/shape-go --repo "{root}" --lab {key}
```
From the `rust` subdirectory (Cargo config points at the unchanged course vendor directory):
```
cargo test --offline --locked
cargo run --offline --locked --release --bin shape-rust -- --repo "{root}" --lab {key}
```
Compare predictions and explanations, not just the exit code. The borrowed Cargo source path is machine-specific; recreate this practice copy after moving the parent course. Do not commit private answers blindly.
'''
    (out/'START.md').write_text(directions,encoding='utf8')
    (out/'answer.md').write_text('# My independent evidence\n\n## Question\n\n## Prediction and hand calculation\n\n## Go choices and errors\n\n## Rust ownership and errors\n\n## Output and controlled change\n\n## Limitation\n\n## Work that required help\n\n## Delayed recall\n',encoding='utf8')
    write_json(out/'study.json',{'lab':key,'created_at':now(),'assessment':'not_assessed','source_fingerprints':fingerprints(root)})

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    sp=ap.add_subparsers(dest='command',required=True)
    sp.add_parser('list');sp.add_parser('doctor')
    p=sp.add_parser('show');p.add_argument('lab')
    for name in ['build','test']:
        p=sp.add_parser(name);p.add_argument('--lang',choices=['go','rust','all'],default='all');p.add_argument('--output',required=True)
    for name in ['run','compare']:
        p=sp.add_parser(name);p.add_argument('--lang',choices=['go','rust','all'],default='all');g=p.add_mutually_exclusive_group(required=True);g.add_argument('--lab');g.add_argument('--all',action='store_true');p.add_argument('--output',required=True)
    p=sp.add_parser('prepare');p.add_argument('--lab',required=True);p.add_argument('--output',required=True)
    p=sp.add_parser('verify');p.add_argument('--output',required=True);p.add_argument('--require-original-parity',action='store_true');p.add_argument('--science',action='store_true')
    p=sp.add_parser('data');p.add_argument('action',choices=['list','verify']);p.add_argument('--lang',choices=['go','rust','all'],default='all');p.add_argument('--output')
    a=ap.parse_args(argv)
    try:
        items=available_labs();keys=[r['key']for r in items]
        if a.command=='list':
            for r in items:print(r['key'].ljust(16),r['title'])
            return 0
        if a.command=='doctor':
            print(json.dumps({'python':sys.version,'go':shutil.which('go'),'cargo':shutil.which('cargo'),'rustc':shutil.which('rustc'),'registry':audit_registry(),'docker_runtime':'not_probed','kubernetes_runtime':'not_probed'},indent=2));return 0
        if a.command=='data' and a.action=='list':
            for r in read_json(ROOT/'native/data_registry.json')['files']:print(r['format'].ljust(6),r['path'],r['bytes'])
            return 0
        if a.command=='show':
            if a.lab not in keys:raise ValueError('Unknown lab')
            print((ROOT/'native/guides/labs'/f'{a.lab}.md').read_text(encoding='utf8'));return 0
        key=getattr(a,'lab',None)
        if key and key not in keys:raise ValueError(f'Unknown lab: {key}')
        if not getattr(a,'output',None):raise ValueError('--output requires a new directory')
        out=new_directory(a.output)
        langs=LANGUAGES if getattr(a,'lang','all')=='all' else(a.lang,)
        if a.command=='prepare':prepare(key,out);status='prepared_not_assessed'
        elif a.command=='build':
            for lang in langs:build(lang,out,force=True)
            status='passed'
        elif a.command=='test':
            results=[unit_tests(lang,out)for lang in langs];write_json(out/'test_summary.json',results);status='passed'
        elif a.command in ['run','compare']:
            if a.command=='compare'and len(langs)!=2:raise ValueError('compare requires both native languages')
            result=run_labs(langs,keys if a.all else[key],out);status=result['status']
        elif a.command=='data':status=verify_data(langs,out)['status']
        else:
            if a.require_original_parity:raise RuntimeError('Original 133-notebook native equivalence is NOT certified; see native/COVERAGE.md')
            tests=[unit_tests(l,out)for l in LANGUAGES]
            runs=run_labs(LANGUAGES,keys,out);data=verify_data(LANGUAGES,out);fixtures=verify_data(LANGUAGES,out,fixtures=True)
            science={'status':'not_run'}
            if a.science:
                command([sys.executable,ROOT/'native/python/scientific_checks.py','--repo',ROOT,'--runs',out,'--output',out/'scientific_checks.json'],ROOT,out/'scientific_checks_execution.json',timeout=300)
                science=read_json(out/'scientific_checks.json')
            status='passed'if all(r['status']=='passed'for r in[runs,data,fixtures]) and science['status']in ['passed','not_run']else'failed'
            write_json(out/'acceptance.json',{'status':status,'scope':'native-16 shared teaching protocols','tests':tests,'lab_count':len(keys),'data_checks':data['checks_count'],'fixture_checks':fixtures['checks_count'],'scientific_checks':science['status'],'original_notebook_parity':'not_certified','python_reference_replay':'not_run','docker_runtime':'not_run','kubernetes_runtime':'not_run'})
        report_page(out,'Native course evidence',status);print(out/'index.html');return 0 if status in ['passed','prepared_not_assessed']else 1
    except (ValueError,RuntimeError,OSError,subprocess.SubprocessError)as e:
        print(f'ERROR: {e}',file=sys.stderr)
        if 'out'in locals():write_json(out/'failure.json',{'status':'failed','error':str(e),'time':now()})
        return 1
if __name__=='__main__':raise SystemExit(main())
