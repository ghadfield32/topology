"""Fresh, explicit reference runs. Python kernels orchestrate; native binaries compute."""
from pathlib import Path
import json,os,sys,uuid
from .workflow import ROOT,command,dump

def labs():return json.loads((ROOT/'native/protocols/labs.json').read_text(encoding='utf8'))['labs']
def commands(key,language,out):
 if key not in {x['key']for x in labs()}:raise ValueError('Unknown lab')
 if language in ['go','rust']:
  return [sys.executable,str(ROOT/'native_course.py'),'run','--lang',language,'--lab',key,'--output',str(out)]
 if language!='python':raise ValueError('Unknown language')
 if key=='poux_bridge':return [sys.executable,str(ROOT/'curriculum/extensions/poux_spatial_ai/bridge.py'),'--repo',str(ROOT),'--output',str(out)]
 return [sys.executable,str(ROOT/'course.py'),'run','--stage'if key.startswith('stage')else'--case',str(int(key[5:]))if key.startswith('stage')else key,'--output',str(out)]

def run_reference(key,language):
 parent=ROOT/'my_work/learning_references';parent.mkdir(parents=True,exist_ok=True)
 identity=key+'-'+language+'-'+uuid.uuid4().hex
 out=parent/identity;log=parent/(identity+'.command.json')
 r=command(commands(key,language,out),ROOT,log,timeout=1800)
 manifests=[str(p.relative_to(out))for p in out.rglob('*.json')if not any(s in p.parts for s in ['target','workspace','source'])]
 summary=dict(lab=key,language=language,exit_code=r['exit_code'],output=str(out),command_log=str(log),assessment='not_assessed',json_artifacts=manifests[:100],scope='Python executes the original reference. Go/Rust execute native16 protocols; see coverage differences.')
 dump(out/'learning_summary.json',summary)
 return summary

def read_metrics(summary):
 out=Path(summary['output']);key=summary['lab'];lang=summary['language']
 if lang in ['go','rust']:
  r=json.loads((out/lang/(key+'.json')).read_text());return dict(metrics=r['metrics'],inputs=r['inputs'])
 candidates=[p for p in out.rglob('results.json')if 'workspace'not in p.parts]
 if candidates:return {p.relative_to(out).as_posix():json.loads(p.read_text())for p in candidates}
 return {'notice':'Inspect the canonical executed notebook and its experiment artifacts in the explicit output directory.'}
