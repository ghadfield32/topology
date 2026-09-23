from pathlib import Path
import json
import nbformat
import pytest
ROOT=Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('stage',range(21))
def test_consolidation_code_is_valid_python(stage):
    notebook=nbformat.read(ROOT/f'consolidation/{stage:02d}_lab.ipynb',4)
    for index,c in enumerate(notebook.cells):
        if c.cell_type=='code':compile(c.source,f'{stage:02d}/cell-{index}','exec')


def test_v4_objectives_questions_and_links():
    meta=json.loads((ROOT/'docs/session_metadata_v4.json').read_text())
    assert [s['stage'] for s in meta]==list(range(21))
    assert sum(len(s['outcomes']) for s in meta)==84
    assert sum(len(s['transfer']) for s in meta)==42
    for s in meta:
        assert len(s['outcomes'])==4 and len(s['transfer'])==2
        assert all(p<s['stage'] for p in s['prerequisites'])
        for p in s['paths'].values():assert (ROOT/p).is_file(),p
        assert s['data_role']


def test_historical_time_series_manifest():
    from hashlib import sha256
    import pandas as pd
    folder=ROOT/'data/time_series'
    manifest=json.loads((folder/'manifest.json').read_text())
    path=folder/'sunspots_yearly.csv'
    assert sha256(path.read_bytes()).hexdigest()==manifest['sha256']
    frame=pd.read_csv(path)
    assert frame.shape==(309,2)
    assert frame.YEAR.tolist()==list(range(1700,2009))
    assert frame.notna().all().all()
