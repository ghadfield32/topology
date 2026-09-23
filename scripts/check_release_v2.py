"""Release-only checks. Do not use this to grade a learner's edited notebooks/log.

The ordinary pytest suite permits completed learner exercises. This shipping audit
requires the distribution's learner state to be pristine and references executed.
"""
from pathlib import Path
import json
import nbformat
import check_package
ROOT=Path(__file__).resolve().parents[1]

def main():
    check_package.main()
    activities=json.loads((ROOT/'practice/activities.json').read_text())
    retrieval=json.loads((ROOT/'practice/retrieval.json').read_text())
    coverage=json.loads((ROOT/'docs/coverage_v2.json').read_text())
    assert len(activities)==65 and len({a['id'] for a in activities})==65
    assert len(retrieval)==39 and len({a['id'] for a in retrieval})==39
    assert len(coverage)==13
    worked=learner=0
    for n in range(13):
        tag=f'{n:02d}'
        assert sum(a['stage']==n for a in activities)==5
        assert sum(a['stage']==n for a in retrieval)==3
        for field in ['core','workbook','lab','practice','reference_answers']:
            assert (ROOT/coverage[n][field]).is_file(),field
        assert (ROOT/f'stages/{tag}/README.md').is_file()
        for kind,path in [('worked',f'notebooks/{tag}_lab.ipynb'),('worked',f'practice/answers/{tag}_practice.ipynb'),('learner',f'practice/learner/{tag}_practice.ipynb')]:
            nb=nbformat.read(ROOT/path,4);nbformat.validate(nb)
            cells=[c for c in nb.cells if c.cell_type=='code']
            if kind=='worked':
                worked+=len(cells)
                assert all(c.execution_count is not None for c in cells)
                assert not any(o.output_type=='error' for c in cells for o in c.get('outputs',[]))
            else:
                learner+=len(cells)
                assert all(c.execution_count is None and not c.get('outputs',[]) for c in cells)
                assert sum('raise NotImplementedError' in c.source for c in cells)==5
    log=json.loads((ROOT/'progress/learning_log_v2.json').read_text())
    assert all(not x['attempts'] for x in log['stages'].values())
    assert json.loads((ROOT/'progress/book_audit.json').read_text())['verified_full_book'] is False
    for name in ['notebook_execution.json','practice_execution.json']:
        records=json.loads((ROOT/'reports'/name).read_text())
        assert len(records)==13 and all(v['status']=='PASSED' for v in records.values())
    result={'status':'PASSED','core_lessons':13,'beginner_workbooks':13,'foundation_primers':4,
            'conceptual_exercises':102,'coding_exercises':65,'retrieval_questions':39,
            'executed_reference_notebooks':26,'executed_reference_code_cells':worked,
            'intentional_learner_notebooks':13,'unexecuted_learner_code_cells':learner,
            'learner_stages_assessed':0,'full_book_verified':False}
    (ROOT/'reports/v2_content_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
