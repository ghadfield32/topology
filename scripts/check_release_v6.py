"""Verify delivered file structure, executed references, data and local HTML targets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,sys
import nbformat
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from shape_lab.industries import IDS,verify_snapshot
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for a,v in attrs:
            if a in ['href','src'] and v:self.links.append(v)

def check():
    rows=json.loads((R/'reports/v6/all_notebook_execution.json').read_text())
    assert len(rows)==99 and all(x['status']=='passed' for x in rows)
    refs=[];cells=figs=0
    for item in rows:
        p=R/item['path'];nb=nbformat.read(p,4);nbformat.validate(nb)
        count=0
        for c in nb.cells:
            if c.cell_type!='code':continue
            assert c.execution_count is not None,p
            assert not any(o.output_type=='error' for o in c.outputs),p
            count+=1;figs+=sum('image/png' in o.get('data',{}) for o in c.outputs)
        assert count==item['code_cells'];cells+=count
        refs.append({'path':item['path'],'code_cells':count,'sha256':sha(p)})
    learner=[*(R/'practice/learner').glob('*.ipynb'),*(R/'physics/practice/learner').glob('*.ipynb'),*(R/'industry/learner').glob('*.ipynb')]
    assert len(learner)==39
    for p in learner:
        nb=nbformat.read(p,4);nbformat.validate(nb)
        assert any('NotImplementedError' in c.source for c in nb.cells)
        assert all(c.execution_count is None and not c.outputs for c in nb.cells if c.cell_type=='code')
    for n in range(31):
        for p in [R/f'stages/{n:02d}/README.md',R/f'industry/stage_guides/{n:02d}.md',R/f'site/v6/stages/{n:02d}.html']:assert p.is_file(),p
    for name in IDS:
        verify_snapshot(name)
        for p in [R/f'industry/lessons/{name}.md',R/f'industry/cards/{name}.md',R/f'industry/answers/{name}.md',R/f'reports/v6/industries/{name}/results.json']:assert p.is_file(),p
    # Original observed source integrity remains independently specified.
    for path,info in json.loads((R/'data/manifest.json').read_text())['files'].items():assert sha(R/path)==info['sha256']
    for name,digest in json.loads((R/'data/stereo/manifest.json').read_text())['files'].items():assert sha(R/'data/stereo'/name)==digest
    for path,manifest in [('data/time_series/sunspots_yearly.csv','data/time_series/manifest.json'),('data/physics/hahn1_excerpt.csv','data/physics/manifest.json')]:assert sha(R/path)==json.loads((R/manifest).read_text())['sha256']
    read=lambda path:json.loads((R/path).read_text())
    coding=sum(len(read(x)) for x in ['practice/activities.json','practice/bridge_exercises.json','physics/practice/activities.json','industry/exercises.json'])
    concepts=sum(len(s['exercises']) for s in read('docs/stage_metadata.json')+read('docs/bridge_metadata.json'))+sum(len(s['questions']) for s in read('docs/v5/stage_metadata.json'))+len(read('industry/concept_questions.json'))
    recall=len(read('practice/retrieval.json'))+len(read('practice/retrieval_v3.json'))+sum(len(s['recall']) for s in read('docs/v5/stage_metadata.json'))+len(read('industry/retrieval.json'))
    assert (coding,concepts,recall)==(143,242,117)
    assert len(list((R/'foundations').glob('*.md')))==8 and (R/'docs/v6/BEGINNER_DATA_PRIMER.md').exists()
    core=json.loads((R/'progress/learning_log_v5.json').read_text());ind=json.loads((R/'progress/industry_log_v6.json').read_text())
    # Reference release logs must remain empty; learners maintain their own copies.
    assert len(core['stages'])==31 and all(not x['attempts'] for x in core['stages'].values())
    assert len(ind['cases'])==8 and all(not x['attempts'] for x in ind['cases'].values())
    optional=json.loads((R/'optional/industry_datasets_v6.json').read_text())
    assert len(optional)==10 and all(x['status']=='Not downloaded, not bundled, not executed' for x in optional)
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
    result={'status':'passed' if not broken and not fonts else 'failed','core_stages':31,'industry_cases':8,'reference_notebooks':99,'reference_code_cells':cells,'embedded_png_outputs':figs,'learner_notebooks':len(learner),'new_coding_exercises':24,'total_coding_exercises':143,'new_conceptual_questions':32,'total_conceptual_questions':242,'existing_transfer_questions':42,'total_delayed_recall_prompts':117,'primers':9,'included_observed_sources':13,'new_normalized_rows':sum(json.loads((R/f'data/industries/{k}/metadata.json').read_text())['rows'] for k in IDS),'optional_data_plans_not_executed':10,'html_pages':pages,'local_file_link_targets':links,'broken_targets':broken,'font_files':fonts,'preassessed_core_or_industry_items':0,'notebooks':refs}
    (R/'reports/v6/release_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='notebooks'},indent=2))
    if result['status']!='passed':raise SystemExit(1)
if __name__=='__main__':check()
