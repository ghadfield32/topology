"""Release-only v3 audit: structure, source linkage, execution and clean learner state.

Use pytest during learning. This script intentionally requires pristine learner
notebooks and an unassessed default log in the distributed reference package.
"""
from pathlib import Path
import json,hashlib,re
import nbformat
import check_package
ROOT=Path(__file__).resolve().parents[1]

def main():
    check_package.main()  # all local HTML targets, preserved core and no font files
    core=json.loads((ROOT/'docs/stage_metadata.json').read_text())
    bridge=json.loads((ROOT/'docs/bridge_metadata.json').read_text())
    coverage=json.loads((ROOT/'docs/coverage_v3.json').read_text())
    code=json.loads((ROOT/'practice/activities.json').read_text())+json.loads((ROOT/'practice/bridge_exercises.json').read_text())
    recall=json.loads((ROOT/'practice/retrieval.json').read_text())+json.loads((ROOT/'practice/retrieval_v3.json').read_text())
    assert len(coverage)==21 and [s['stage'] for s in coverage]==list(range(21))
    assert len(code)==89 and len({a['id'] for a in code})==89
    assert len(recall)==63 and len({a['id'] for a in recall})==63
    assert sum(len(s['exercises']) for s in core+bridge)==150
    source_ids={s['id'] for s in json.loads((ROOT/'docs/sources_v3.json').read_text())}
    for s in bridge:
        assert set(s['readings'])<=source_ids
        assert len(s['exercises'])==len(s['answers'])==6
    cells=0;learner_cells=0;notebook_count=0
    for item in coverage:
        n=item['stage'];tag=f'{n:02d}'
        for key in ['core','workbook','lab','practice','reference_answers']:
            assert (ROOT/item[key]).is_file(),item[key]
        assert (ROOT/f'stages/{tag}/README.md').is_file()
        assert sum(a['stage']==n for a in code)==(5 if n<13 else 3)
        assert sum(a['stage']==n for a in recall)==3
        for field in ['lab','reference_answers','practice']:
            nb=nbformat.read(ROOT/item[field],4);nbformat.validate(nb)
            cc=[c for c in nb.cells if c.cell_type=='code']
            if field=='practice':
                assert all(c.execution_count is None and not c.outputs for c in cc)
                assert sum('raise NotImplementedError' in c.source for c in cc)==(5 if n<13 else 3)
                learner_cells+=len(cc)
            else:
                notebook_count+=1;cells+=len(cc)
                assert all(c.execution_count is not None for c in cc)
                assert not any(o.output_type=='error' for c in cc for o in c.outputs)
                assert not any('raise NotImplementedError' in c.source for c in cc)
        result=json.loads((ROOT/f'reports/stage_{tag}/results.json').read_text())
        assert isinstance(result,dict)
    for name in ['notebook_execution.json','practice_execution.json']:
        evidence=json.loads((ROOT/'reports'/name).read_text())
        assert set(evidence)=={f'{n:02d}' for n in range(21)}
        assert all(e['status']=='PASSED' for e in evidence.values())
    progress=json.loads((ROOT/'progress/learning_log_v3.json').read_text())
    assert len(progress['stages'])==21 and all(not s['attempts'] for s in progress['stages'].values())
    assert not json.loads((ROOT/'progress/book_audit.json').read_text())['verified_full_book']
    # Only the bundled data is asserted; this is not an Internet availability check.
    manifest=json.loads((ROOT/'data/stereo/manifest.json').read_text())
    for name,digest in manifest['files'].items():
        assert hashlib.sha256((ROOT/'data/stereo'/name).read_bytes()).hexdigest()==digest
    assert json.loads((ROOT/'reports/stage_16/results.json').read_text())['VGGT_inference_executed'] is False
    assert json.loads((ROOT/'reports/stage_19/results.json').read_text())['real_event_precision'] is None
    result={'status':'PASSED','stages':21,'core_stages':13,'applied_geometry_stages':8,
            'foundation_primers':len(list((ROOT/'foundations').glob('*.md'))),'conceptual_exercises':150,
            'coding_exercises':89,'delayed_recall_questions':63,'executed_reference_notebooks':notebook_count,
            'executed_reference_code_cells':cells,'intentional_unexecuted_learner_notebooks':21,
            'unexecuted_learner_code_cells':learner_cells,'stage_figures':len(list((ROOT/'reports').glob('stage_*/*.png'))),
            'learner_stages_assessed':0,'VGGT_inference_executed':False,'full_book_text_audited':False}
    (ROOT/'reports/v3_content_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
