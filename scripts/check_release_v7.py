"""Structural and provenance audit for v7; not a mathematical certification."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,sys
import nbformat
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from shape_lab.industries import IDS,verify_snapshot
from shape_lab.evidence_v7 import load_snapshot
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
    for a,v in attrs:
        if a in ['href','src'] and v:self.links.append(v)

def check():
 inherited=json.loads((R/'reports/v7/inherited_notebook_execution.json').read_text());new=json.loads((R/'reports/v7/new_notebook_execution.json').read_text())
 assert len(inherited)==99 and len(new)==8
 rows=inherited+new;assert all(x['status']=='passed' for x in rows)
 (R/'reports/v7/notebook_execution.json').write_text(json.dumps(rows,indent=2))
 refs=[];cells=figs=0
 for item in rows:
    p=R/item['path'];b=nbformat.read(p,4);nbformat.validate(b);count=0
    for c in b.cells:
        if c.cell_type!='code':continue
        assert c.execution_count is not None,p
        assert not any(o.output_type=='error' for o in c.outputs),p
        count+=1;figs+=sum('image/png' in o.get('data',{}) for o in c.outputs)
    assert count==item['code_cells'];cells+=count;refs.append({'path':item['path'],'sha256':sha(p),'code_cells':count})
 learner=[*(R/'practice/learner').glob('*.ipynb'),*(R/'physics/practice/learner').glob('*.ipynb'),*(R/'industry/learner').glob('*.ipynb'),*(R/'applications_v7').glob('*/learner.ipynb'),*(R/'methods_v7').glob('*/learner.ipynb')]
 assert len(learner)==43
 for p in learner:
    b=nbformat.read(p,4);nbformat.validate(b)
    assert any('NotImplementedError' in c.source for c in b.cells)
    assert all(c.execution_count is None and not c.outputs for c in b.cells if c.cell_type=='code')
 for n in range(31):
    for relative in [f'stages/{n:02d}/README.md',f'beginner_v7/{n:02d}/lesson.md',f'beginner_v7/{n:02d}/check.py',f'site/v7/beginner_v7/{n:02d}/lesson.html']:assert (R/relative).is_file(),relative
 for name in IDS:verify_snapshot(name)
 for name in ['seeds','concrete_slump']:load_snapshot(name)
 for path,info in json.loads((R/'data/manifest.json').read_text())['files'].items():assert sha(R/path)==info['sha256']
 for name,digest in json.loads((R/'data/stereo/manifest.json').read_text())['files'].items():assert sha(R/'data/stereo'/name)==digest
 for path,manifest in [('data/time_series/sunspots_yearly.csv','data/time_series/manifest.json'),('data/physics/hahn1_excerpt.csv','data/physics/manifest.json')]:assert sha(R/path)==json.loads((R/manifest).read_text())['sha256']
 read=lambda p:json.loads((R/p).read_text())
 coding=sum(len(read(x)) for x in ['practice/activities.json','practice/bridge_exercises.json','physics/practice/activities.json','industry/exercises.json'])+16
 concepts=sum(len(s['exercises']) for s in read('docs/stage_metadata.json')+read('docs/bridge_metadata.json'))+sum(len(s['questions']) for s in read('docs/v5/stage_metadata.json'))+len(read('industry/concept_questions.json'))+24
 recall=len(read('practice/retrieval.json'))+len(read('practice/retrieval_v3.json'))+sum(len(s['recall']) for s in read('docs/v5/stage_metadata.json'))+len(read('industry/retrieval.json'))+12
 assert (coding,concepts,recall)==(159,266,129)
 core=read('progress/learning_log_v5.json');industry=read('progress/industry_log_v6.json');extension=read('progress/v7_extension_checklist.json')
 assert all(not x['attempts'] for x in core['stages'].values()) and all(not x['attempts'] for x in industry['cases'].values())
 assert all(x['status']=='unassessed' for x in extension['sections'].values())
 broken=[];links=0;pages=0
 for p in R.rglob('*.html'):
    if any(x in p.parts for x in ['.venv','.git']):continue
    pages+=1;parser=Links();parser.feed(p.read_text())
    for u in parser.links:
        url=urlsplit(u)
        if url.scheme or url.netloc or not url.path:continue
        links+=1;t=(p.parent/unquote(url.path)).resolve()
        if not t.is_relative_to(R) or not t.exists():broken.append({'page':p.relative_to(R).as_posix(),'url':u})
 fonts=[str(p.relative_to(R)) for p in R.rglob('*') if p.suffix.lower() in {'.ttf','.otf','.woff','.woff2'}]
 report={'status':'passed' if not broken and not fonts else 'failed','core_stages':31,'new_entry_guides':31,'entry_checks':31,'industry_cases':10,'new_methods_labs':2,'reference_notebooks':len(rows),'reference_code_cells':cells,'embedded_png_outputs':figs,'learner_notebooks':len(learner),'coding_exercises':coding,'conceptual_questions':concepts,'delayed_recall_prompts':recall,'earlier_transfer_questions':42,'additional_entry_questions':31,'primers':10,'observed_sources':15,'new_observed_rows':313,'optional_data_plans_not_executed':10,'html_pages':pages,'local_file_link_targets':links,'broken_targets':broken,'font_files':fonts,'preassessed_items':0,'notebooks':refs,'limitations':['File targets checked; fragment-anchor semantics are not exhaustively audited.','External links were not all recrawled.','Hashes do not independently verify numerical transcription against provider bytes.']}
 (R/'reports/v7/release_check.json').write_text(json.dumps(report,indent=2))
 print(json.dumps({k:v for k,v in report.items() if k!='notebooks'},indent=2))
 if report['status']!='passed':raise SystemExit(1)
if __name__=='__main__':check()
