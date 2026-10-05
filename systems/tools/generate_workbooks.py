#!/usr/bin/env python3
"""Generate navigation workbooks; never own the curriculum or private learner work."""
from pathlib import Path
import argparse,hashlib,html,json
ROOT=Path(__file__).resolve().parents[2]
def cell(kind,text):
 v={'cell_type':kind,'id':hashlib.sha256((kind+text).encode()).hexdigest()[:12],'metadata':{},'source':text}
 if kind=='code':v.update(execution_count=None,outputs=[])
 return v
LOCATE="""from pathlib import Path
import sys, json
ROOT = next((p for p in (Path.cwd(), *Path.cwd().parents) if (p / 'systems/catalog.json').exists() and (p / 'native/protocols/labs.json').exists()), None)
if ROOT is None:
    raise RuntimeError('Open this workbook inside the extracted course repository.')
sys.path.insert(0, str(ROOT))
print('Course:', ROOT)
print('Interpreter:', sys.executable)
"""
def notebook(cells,role):
 return json.dumps({'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3 — explicit orchestration','language':'python','name':'python3'},'language_info':{'name':'python'},'shape_role':role,'assessment':'not_assessed'},'cells':cells},indent=1)+'\n'
def render(root=ROOT):
 result={};labs=json.loads((root/'native/protocols/labs.json').read_text())['labs'];units=json.loads((root/'systems/catalog.json').read_text())['units']
 for lab in labs:
  key=lab['key']
  for lang in ['python','go','rust']:
   lead=f"# {lab['title']} — {lang}\n\nOne mathematical lesson: `{lab['lesson']}`. Read it once. This is a reference-execution interface, not a completed independent assignment.\n\n**Explain → Predict → Implement → Break → Apply.** Write your prediction before executing. The kernel is Python; {('the original Python experiment does the computation' if lang=='python'else 'the compiled '+lang+' program does the computation')}.\n\n**Protocol boundary:** {lab['original_scope_gaps']}"
   cells=[cell('markdown',lead),cell('code',LOCATE),cell('markdown','## Fresh execution\nThis creates a new run and never searches for old results. It may take longer when the original experiment rebuilds prerequisites. The complete stdout and stderr remain in its command record.'),cell('code',f"from systems.python.notebook_runner import run_reference, read_metrics\nsummary = run_reference({key!r}, {lang!r})\nprint(json.dumps(summary, indent=2))"),cell('code',"metrics = read_metrics(summary)\nprint(json.dumps(metrics, indent=2)[:24000])\nprint('Full values are retained in the output files; printing is truncated only for readability.')"),cell('markdown','## Independent work\nUse `python learn.py session --lab '+key+' --output my_work/'+key+'_attempt01` to obtain private projects. Native source edits must be compiled from the copied workspace, not the reference root.\n\n'+ '\n'.join(str(i+1)+'. '+x for i,x in enumerate(lab['challenges']))+'\n\nRecord what required help; no automatic mastery credit. Compare protocols before comparing scores.')]
   result[f'learning/workbooks/{lang}/{key}.ipynb']=notebook(cells,lang+' reference orchestration')
 for u in units:
  key=u['id'];text=f"# {u['title']}\n\nRead `{u['lesson']}`. This notebook prepares a real project, then builds and checks that copy. Work in the editor and terminal; return here to analyze evidence. Optional dependencies may be BLOCKED and are never counted as passed."
  cells=[cell('markdown',text),cell('code',LOCATE),cell('code',f"import uuid\nfrom systems.python.projects import prepare, check\nworkspace = prepare({key!r}, ROOT / 'my_work' / ({key!r} + '_' + uuid.uuid4().hex))\nprint((workspace / 'START.md').read_text())"),cell('markdown','## Pause to edit the private project\nPredict an output and attempt an independent change. Running the unmodified reference remains guided practice.'),cell('code',"result, status = check(workspace, workspace / 'attempt01')\nprint((result / 'project_check.json').read_text())\nif status == 'failed':\n    raise RuntimeError('Project failed; inspect its logs.')\nif status == 'blocked':\n    print('Dependency gate blocked. This is NOT an implementation pass.')"),cell('markdown','## Reflect\nExplain the result, one expected failure, the resource/ownership choices, the same-data connection, and one unsupported conclusion. Save them in the workspace answer.md.')]
  result[f'learning/workbooks/systems/{key}.ipynb']=notebook(cells,'project integration '+key)
 rows=''.join('<tr><td>'+html.escape(l['key'])+'</td><td>'+html.escape(l['title'])+'</td>'+''.join('<td><a href="'+lang+'/'+l['key']+'.ipynb">'+lang+'</a></td>'for lang in ['python','go','rust'])+'</tr>'for l in labs)
 result['learning/workbooks/index.html']='<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>One lesson, actual language projects</title><style>body{font:17px/1.6 system-ui;max-width:1100px;margin:40px auto;padding:16px}td{padding:7px;border-bottom:1px solid #ccc}a{overflow-wrap:anywhere}</style><h1>Language workbooks</h1><p>57 units, three interfaces each. Python executes the canonical experiment; Go and Rust execute their declared native16 protocols. Every interface starts a new run. Files are opened in Jupyter/VS Code, not rendered as interactive browser lessons. <a href="../../LEARN_TOPOLOGY.html">Course home</a></p><table>'+rows+'</table><h2>Engineering projects</h2>'+''.join('<p><a href="systems/'+u['id']+'.ipynb">'+html.escape(u['title'])+'</a></p>'for u in units)
 return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--root',type=Path,default=ROOT);a=p.parse_args();items=render(a.root);mismatches=[]
 for path,text in items.items():
  dest=a.root/path
  if a.check:
   if not dest.exists()or dest.read_text(encoding='utf8')!=text:mismatches.append(path)
  else:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text,encoding='utf8')
 print(json.dumps(dict(files=len(items),notebooks=sum(x.endswith('.ipynb')for x in items),mismatches=mismatches),indent=2))
 return int(bool(mismatches))
if __name__=='__main__':raise SystemExit(main())
