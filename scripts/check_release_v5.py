"""Verify all current stages, reference notebooks, question counts and data hashes."""
from pathlib import Path
import hashlib
import json
import nbformat

R=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads((R/p).read_text())
reference=sorted([*(R/'notebooks').glob('*.ipynb'),*(R/'practice/answers').glob('*.ipynb'),*(R/'consolidation').glob('*.ipynb'),*(R/'physics/notebooks').glob('*.ipynb'),*(R/'physics/practice/answers').glob('*.ipynb')])
learners=sorted([*(R/'practice/learner').glob('*.ipynb'),*(R/'physics/practice/learner').glob('*.ipynb')])
assert len(reference)==83 and len(learners)==31
cells=figures=0; per_notebook={}
for p in reference:
    nb=nbformat.read(p,4);nbformat.validate(nb);count=0
    for cell in nb.cells:
        if cell.cell_type!='code':continue
        assert cell.execution_count is not None,(p,cell.source[:100])
        assert not any(o.output_type=='error' for o in cell.outputs),p
        count+=1
        figures+=sum('image/png' in o.get('data',{}) for o in cell.outputs)
    cells+=count;per_notebook[p.relative_to(R).as_posix()]={'code_cells':count,'sha256':sha(p)}
for p in learners:
    nb=nbformat.read(p,4);nbformat.validate(nb)
    assert any('NotImplementedError' in c.source for c in nb.cells),p
    assert all(c.get('execution_count') is None and not c.get('outputs') for c in nb.cells if c.cell_type=='code'),p
core=read('docs/stage_metadata.json');bridge=read('docs/bridge_metadata.json');physics=read('docs/v5/stage_metadata.json')
assert len(core)+len(bridge)+len(physics)==31
for n in range(31):assert (R/f'stages/{n:02d}/README.md').is_file()
assert all(len(x['questions'])==6 and len(x['recall'])==3 for x in physics)
concepts=sum(len(x['exercises']) for x in core+bridge)+sum(len(x['questions']) for x in physics)
coding=len(read('practice/activities.json'))+len(read('practice/bridge_exercises.json'))+len(read('physics/practice/activities.json'))
recall=len(read('practice/retrieval.json'))+len(read('practice/retrieval_v3.json'))+sum(len(x['recall']) for x in physics)
assert concepts==210 and coding==119 and recall==93
assert len(list((R/'foundations').glob('*.md')))==8
# Check each original data source by its own declared manifest, not regenerated values.
datafiles=[]
for path,info in read('data/manifest.json')['files'].items():
    p=R/path;assert sha(p)==info['sha256'],p;datafiles.append(path)
for name,expected in read('data/stereo/manifest.json')['files'].items():
    p=R/'data/stereo'/name;assert sha(p)==expected,p;datafiles.append(p.relative_to(R).as_posix())
for path,manifest in [('data/time_series/sunspots_yearly.csv','data/time_series/manifest.json'),('data/physics/hahn1_excerpt.csv','data/physics/manifest.json')]:
    assert sha(R/path)==read(manifest)['sha256'],path;datafiles.append(path)
log=read('progress/learning_log_v5.json');assert len(log['stages'])==31
assert all(not s['attempts'] for s in log['stages'].values())
for name,expected in [('reports/notebook_execution.json',21),('reports/practice_execution.json',21),('reports/consolidation_execution_v4.json',21),('reports/physics_execution_v5.json',20)]:
    report=read(name);assert len(report)==expected,(name,len(report))
    assert all(v['status']=='PASSED' and v.get('errors',0)==0 for v in report.values()),name
fonts=[str(p.relative_to(R)) for p in R.rglob('*') if p.suffix.lower() in {'.ttf','.otf','.woff','.woff2'}]
assert not fonts
result={'status':'PASSED','stages':31,'reference_notebooks':len(reference),'executed_reference_code_cells':cells,'embedded_png_outputs':figures,'learner_notebooks_intentionally_unexecuted':len(learners),'coding_exercises':coding,'concept_questions':concepts,'transfer_questions':len(read('practice/transfer_v4.json')),'delayed_recall_questions':recall,'primers':8,'observed_data_sources':5,'data_manifest_files_checked':datafiles,'learner_stages_assessed':0,'font_files':fonts,'notebooks':per_notebook}
(R/'reports/release_v5.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='notebooks'},indent=2))
