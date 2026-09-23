from pathlib import Path
import json,ast
import pytest
import nbformat
R=Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('stage',[f'S{i:02}' for i in range(7)])
def test_stage_teaches_and_has_practice(stage):
    text=(R/'sports_v8/lessons'/f'{stage}.md').read_text()
    assert len(text.split())>=600
    assert '## Exercises' in text and '## Worked answers' in text
    for folder in ['notebooks','practice','solutions']:
        b=nbformat.read(R/f'sports_v8/{folder}/{stage}.ipynb',4)
        assert any(c.cell_type=='markdown' for c in b.cells)
        for c in b.cells:
            if c.cell_type=='code':ast.parse(c.source)
    exercise=nbformat.read(R/f'sports_v8/practice/{stage}.ipynb',4)
    assert sum('raise NotImplementedError' in c.source for c in exercise.cells)==3
    answer=nbformat.read(R/f'sports_v8/solutions/{stage}.ipynb',4)
    assert not any('raise NotImplementedError' in c.source for c in answer.cells if c.cell_type=='code')

def test_core_stage_map_preserves_31_sections():
    rows=json.loads((R/'docs/v8/core_map.json').read_text())
    assert [r['stage'] for r in rows]==list(range(31))
    assert all((R/r['core_lesson']).is_file() for r in rows)

def test_manual_log_starts_unassessed():
    log=json.loads((R/'progress/templates/sports_log_v8.json').read_text())
    assert len(log['stages'])==7
    assert all(s['status']=='unassessed' and not s['attempts'] for s in log['stages'].values())

def test_registry_dates_and_access_not_invented():
    r=json.loads((R/'sports_v8/dataset_registry.json').read_text())
    assert r['checked_on']=='2026-09-21' and len(r['datasets'])==10
    for d in r['datasets']:
        assert all(d.get(key) for key in ['source','license','limits','units','status','split','metrics'])
    assert 'SYNTHETIC' in next(d for d in r['datasets'] if d['id']=='basket_multiview')['kind']
    assert 'not downloaded' in next(d for d in r['datasets'] if d['id']=='openbiomechanics')['status'] or 'not bundled' in next(d for d in r['datasets'] if d['id']=='openbiomechanics')['status']
