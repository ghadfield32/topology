import json
import numpy as np
import pandas as pd
import pytest
from shape_lab.explore import explore_csv


def make_csv(tmp_path,values):
    p=tmp_path/'input.csv';pd.DataFrame(values).to_csv(p,index=False);return p


def test_square_csv_has_exact_h1(tmp_path):
    p=make_csv(tmp_path,{'x':[0,1,1,0],'y':[0,0,1,1],'label':['a']*4})
    r=explore_csv(p,['x','y'],4,7,'none','Generated square control','metres')
    assert r['sample_count']==4
    assert r['source_note']=='Generated square control'
    assert r['scope']=='exploratory_only'
    d=r['diagrams']['H1'];assert len(d)==1
    assert np.allclose(d[0],[1,np.sqrt(2)])
    assert len(r['input_sha256'])==64
    json.dumps(r,allow_nan=False)


def test_csv_deterministic_sampling_and_translation(tmp_path):
    rng=np.random.default_rng(17);x=rng.normal(size=(30,3))
    p=make_csv(tmp_path,dict(zip(['a','b','c'],x.T)))
    a=explore_csv(p,['a','b','c'],10,19,'none','synthetic test','unitless')
    b=explore_csv(p,['a','b','c'],10,19,'none','synthetic test','unitless')
    assert a==b


@pytest.mark.parametrize('columns,scale', [([], 'none'),(['missing'],'none'),(['x','x'],'none'),(['x'],'nonsense')])
def test_invalid_configuration(tmp_path,columns,scale):
    p=make_csv(tmp_path,{'x':[0,1]})
    with pytest.raises(ValueError):explore_csv(p,columns,5,1,scale,'test','units')


def test_missing_data_rejected(tmp_path):
    p=make_csv(tmp_path,{'x':[0,np.nan],'y':[1,2]})
    with pytest.raises(ValueError):explore_csv(p,['x','y'],5,1,'none','test','units')


def test_text_feature_rejected(tmp_path):
    p=make_csv(tmp_path,{'x':['a','b']})
    with pytest.raises(ValueError):explore_csv(p,['x'],5,1,'none','test','units')


def test_constant_standardized_feature_rejected(tmp_path):
    p=make_csv(tmp_path,{'x':[1,1,1]})
    with pytest.raises(ValueError):explore_csv(p,['x'],5,1,'standard','test','units')


def test_sample_limit_and_provenance_required(tmp_path):
    p=make_csv(tmp_path,{'x':[0,1]})
    for count,note,units in [(200,'test','units'),(0,'test','units'),(2,'','units'),(2,'test','')]:
        with pytest.raises(ValueError):explore_csv(p,['x'],count,1,'none',note,units)
