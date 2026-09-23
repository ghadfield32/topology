from pathlib import Path
import json,runpy
import numpy as np
import pandas as pd
import pytest
from shape_lab.evidence_v7 import load_snapshot,conformal_radius
R=Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('stage',range(31))
def test_entry_calculation(stage):
    runpy.run_path(str(R/f'beginner_v7/{stage:02d}/check.py'),run_name='__main__')

def test_entry_guides_complete():
    rows=json.loads((R/'docs/v7/beginner_map.json').read_text())
    assert [x['stage'] for x in rows]==list(range(31))
    for x in rows:
        assert (R/x['guide']).is_file() and (R/x['check']).is_file()
        assert len(x['explanation'].split())>=70
        assert x['assignment'] and x['answer'] and x['trap']

def test_new_practice_counts():
    q=json.loads((R/'docs/v7/questions.json').read_text())
    assert len(q)==36 and len({x['id'] for x in q})==36
    assert sum(x['kind']=='concept' for x in q)==24
    assert sum(x['kind']=='recall' for x in q)==12

def test_concrete_protocol_separation_and_calibration():
    report=R/'reports/v7/concrete_slump'
    split=pd.read_csv(report/'split.csv');scores=pd.read_csv(report/'calibration.csv')
    pred=pd.read_csv(report/'predictions.csv');metrics=json.loads((report/'results.json').read_text())
    assert split.groupby('split').size().to_dict()=={'calibration':25,'test':26,'train':52}
    assert set(scores.source_id)==set(split.loc[split.split=='calibration','source_id'])
    assert set(pred.source_id)==set(split.loc[split.split=='test','source_id'])
    assert np.isclose(conformal_radius(scores.score.to_numpy(),.1),metrics['radius_mpa'])
    assert np.allclose(pred.upper_mpa-pred.lower_mpa,2*metrics['radius_mpa'])
    assert int(((pred.observed_mpa>=pred.lower_mpa)&(pred.observed_mpa<=pred.upper_mpa)).sum())==metrics['covered_count']

def test_seeds_predictions_and_scope():
    r=R/'reports/v7/seeds';split=pd.read_csv(r/'split.csv');p=pd.read_csv(r/'predictions.csv')
    assert split.groupby('split').size().to_dict()=={'test':42,'train':126,'validation':42}
    for name,group in p.groupby('model'):
        assert set(group.loc[group.split=='test','source_id'])==set(split.loc[split.split=='test','source_id'])
        assert name in {'majority','seven_features','without_compactness'}

def test_leakage_control_is_explicit():
    r=json.loads((R/'reports/v7/leakage/protocol.json').read_text())
    assert 'repeat' in r['copy_rule']
    assert r['audits']['row_split']['row_disjoint'] and not r['audits']['row_split']['unit_disjoint']
    assert r['audits']['unit_split']['unit_disjoint']

def test_source_counterexample_report():
    r=json.loads((R/'reports/v7/claims/results.json').read_text())
    assert np.isclose(r['energy_before'],.5) and np.isclose(r['energy_after'],.4808)
    assert r['symplectic_defect']<1e-14
    assert np.isclose(r['first_projection_residual'],.5625)
    assert r['opposed_gradient_dot']==-1

def test_saved_concrete_fit_reproduces_predictions():
    table,meta=load_snapshot('concrete_slump');r=R/'reports/v7/concrete_slump'
    params=json.loads((r/'fitted_parameters.json').read_text());pred=pd.read_csv(r/'predictions.csv')
    x=table.set_index('source_id').loc[pred.source_id,meta['features']].to_numpy()
    numerical=((x-np.array(params['center']))/np.array(params['scale']))@np.array(params['coef'])+params['intercept']
    assert np.allclose(numerical,pred.predicted_mpa,atol=1e-10)

def test_saved_seed_fit_reproduces_labels():
    table,meta=load_snapshot('seeds');r=R/'reports/v7/seeds'
    models=json.loads((r/'fitted_parameters.json').read_text());pred=pd.read_csv(r/'predictions.csv')
    for name,params in models.items():
        selected=pred.loc[pred.model==name]
        x=table.set_index('source_id').loc[selected.source_id,meta['features']].to_numpy()[:,params['feature_indices']]
        scores=((x-np.array(params['center']))/np.array(params['scale']))@np.array(params['coef']).T+np.array(params['intercept'])
        labels=np.array(params['classes'])[scores.argmax(axis=1)]
        assert np.array_equal(labels,selected.predicted)
