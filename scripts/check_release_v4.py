"""Release-only structural audit. Does not assess learner answers or physical accuracy."""
from pathlib import Path
import hashlib,json,platform,importlib.metadata
import nbformat
from IPython.core.inputtransformer2 import TransformerManager
import check_package
R=Path(__file__).resolve().parents[1]

def main():
    check_package.main()
    meta=json.loads((R/'docs/session_metadata_v4.json').read_text())
    assert len(meta)==21 and [x['stage'] for x in meta]==list(range(21))
    assert sum(len(x['outcomes']) for x in meta)==84
    transfer=json.loads((R/'practice/transfer_v4.json').read_text())
    assert len(transfer)==42 and len({x['id'] for x in transfer})==42
    core=json.loads((R/'docs/stage_metadata.json').read_text())
    bridge=json.loads((R/'docs/bridge_metadata.json').read_text())
    assert sum(len(x['exercises']) for x in core+bridge)==150
    coding=json.loads((R/'practice/activities.json').read_text())+json.loads((R/'practice/bridge_exercises.json').read_text())
    assert len(coding)==89 and len({x['id'] for x in coding})==89
    recall=json.loads((R/'practice/retrieval.json').read_text())+json.loads((R/'practice/retrieval_v3.json').read_text())
    assert len(recall)==63
    executed=0;cells=0;figures=0
    for s in meta:
        n=s['stage']
        for p in s['paths'].values():assert (R/p).is_file(),p
        for folder,name in [('notebooks',f'{n:02d}_lab.ipynb'),('consolidation',f'{n:02d}_lab.ipynb'),('practice/answers',f'{n:02d}_practice.ipynb')]:
            nb=nbformat.read(R/folder/name,4);nbformat.validate(nb)
            cc=[c for c in nb.cells if c.cell_type=='code']
            assert all(c.execution_count is not None for c in cc),(folder,n)
            assert not any(o.output_type=='error' for c in cc for o in c.outputs)
            assert not any('raise NotImplementedError' in c.source for c in cc)
            for c in cc:compile(TransformerManager().transform_cell(c.source),f'{folder}/{name}','exec')
            executed+=1;cells+=len(cc)
            figures+=sum('image/png' in o.get('data',{}) for c in cc for o in c.outputs)
        nb=nbformat.read(R/f'practice/learner/{n:02d}_practice.ipynb',4)
        cc=[c for c in nb.cells if c.cell_type=='code']
        assert all(c.execution_count is None and not c.outputs for c in cc)
        assert sum('raise NotImplementedError' in c.source for c in cc)==(5 if n<13 else 3)
        record=json.loads((R/f'reports/consolidation_v4/{n:02d}.json').read_text())
        assert record['stage']==n and record['execution_role']=='reference_consolidation' and record['data_role']
    for path in ['notebook_execution.json','practice_execution.json','consolidation_execution_v4.json']:
        e=json.loads((R/'reports'/path).read_text())
        assert set(e)=={f'{n:02d}' for n in range(21)}
        assert all(v['status']=='PASSED' for v in e.values())
    base=json.loads((R/'data/manifest.json').read_text())
    for path,entry in base['files'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==entry['sha256']
    stereo=json.loads((R/'data/stereo/manifest.json').read_text())
    for path,digest in stereo['files'].items():assert hashlib.sha256((R/'data/stereo'/path).read_bytes()).hexdigest()==digest
    solar=json.loads((R/'data/time_series/manifest.json').read_text())
    assert hashlib.sha256((R/'data/time_series/sunspots_yearly.csv').read_bytes()).hexdigest()==solar['sha256']
    log=json.loads((R/'progress/learning_log_v3.json').read_text())
    assert len(log['stages'])==21 and all(not s['attempts'] for s in log['stages'].values())
    assert json.loads((R/'progress/book_audit.json').read_text())['verified_full_book'] is False
    assert json.loads((R/'reports/stage_16/results.json').read_text())['VGGT_inference_executed'] is False
    assert json.loads((R/'reports/stage_19/results.json').read_text())['real_event_precision'] is None
    env={'python':platform.python_version(),'platform':platform.platform(),'packages':{}}
    for name in ['numpy','scipy','pandas','matplotlib','scikit-learn','pytest','nbformat','nbclient','mistune','statsmodels','ripser','gudhi']:
        try:env['packages'][name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:env['packages'][name]=None
    (R/'reports/environment_v4.json').write_text(json.dumps(env,indent=2)+'\n')
    result={'status':'PASSED','version':'4.0.0','stages':21,'guided_sessions':21,'consolidation_notebooks':21,
            'explicit_outcomes':84,'conceptual_exercises':150,'additional_transfer_questions':42,'coding_exercises':89,
            'delayed_recall_questions':63,'foundation_primers':len(list((R/'foundations').glob('*.md'))),
            'executed_reference_notebooks':executed,'executed_reference_code_cells':cells,
            'embedded_reference_figures':figures,'intentional_learner_notebooks':21,'datasets':4,
            'learner_stages_assessed':0,'full_book_text_audited':False,'VGGT_inference_executed':False,
            'physical_holdout_validated':False,'real_sports_event_labels_evaluated':False}
    (R/'reports/v4_content_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
