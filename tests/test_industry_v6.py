"""Contracts for leakage-aware cross-industry teaching utilities."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from shape_lab.industries import (load_dataset,verify_snapshot,group_split,ordered_split,
    TrainScaler,past_windows,assign_windows,mst_lengths,local_topology,choice_table,
    best_mean_change,seasonal_means)

ROOT=Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('name,n',[('wdbc',569),('wine',178),('stackloss',21),('grunfeld',220),('co2',2284),('nile',100),('elnino',61),('modechoice',840)])
def test_snapshots(name,n):
    df,meta=load_dataset(name);assert len(df)==n;assert meta['data_kind']=='observed';assert verify_snapshot(name)
    assert set(x['name'] for x in meta['schema'])==set(df)

def test_missing_is_not_zero():
    d,_=load_dataset('co2');assert d.co2.isna().sum()==59;assert (d.co2==0).sum()==0

def test_unknown_id_rejected():
    with pytest.raises(ValueError):load_dataset('../wine')

def test_loader_returns_independent_data():
    a,_=load_dataset('wine');a.iloc[0,1]=0;b,_=load_dataset('wine');assert b.iloc[0,1]!=0

def test_checksum_tamper(tmp_path):
    d=tmp_path/'file.csv';d.write_text('a\n1\n')
    from shape_lab.industries import check_sha256
    with pytest.raises(ValueError,match='hash'):check_sha256(d,'0'*64)

def test_group_split_has_no_overlap():
    g=np.repeat(np.arange(20),4);s=group_split(g,seed=6)
    assert [len(s[k]) for k in ['train','validation','test']]==[48,16,16]
    sets=[set(g[v]) for v in s.values()]
    assert not(sets[0]&sets[1] or sets[0]&sets[2] or sets[1]&sets[2])
    assert sorted(np.concatenate(list(s.values())))==list(range(len(g)))
    for k in s:np.testing.assert_array_equal(s[k],group_split(g,seed=6)[k])

def test_ordered_split_keeps_equal_times_together():
    t=np.repeat(np.arange(20),3);s=ordered_split(t)
    assert max(t[s['train']])<min(t[s['validation']])<min(t[s['test']])

@pytest.mark.parametrize('bad',[[1,1],[1,np.nan,2,3,4],[1,2,3,4]])
def test_bad_group_inputs(bad):
    with pytest.raises(ValueError):group_split(bad)

def test_scaler_uses_training_only():
    fit=TrainScaler.fit([[1,5],[3,5]])
    np.testing.assert_allclose(fit.transform([[1,5],[3,5]]),[[-1,0],[1,0]])
    np.testing.assert_allclose(fit.transform([[101,5]]),[[99,0]])
    np.testing.assert_allclose(fit.mean,[2,5]);np.testing.assert_allclose(fit.scale,[1,1])

@pytest.mark.parametrize('x',[[],[[1,np.nan]],[[1,np.inf]]])
def test_scaler_rejects_bad(x):
    with pytest.raises(ValueError):TrainScaler.fit(x)

def test_windows_are_past_only_and_traceable():
    x=np.arange(20,dtype=float);b=past_windows(x,np.arange(20),length=3,horizon=2,expected_step=1)
    np.testing.assert_array_equal(b.x[0],[0,1,2]);assert b.y[0]==4
    assert b.end[0]==2 and b.target[0]==4 and b.start[0]==0
    x[4]=999;bb=past_windows(x,np.arange(20),3,2,expected_step=1)
    np.testing.assert_array_equal(b.x[0],bb.x[0]);assert bb.y[0]==999

def test_windows_do_not_bridge_gap_or_nan():
    vals=np.arange(10,dtype=float);vals[4]=np.nan
    t=np.array([0,1,2,3,4,5,6,20,21,22]);b=past_windows(vals,t,3,expected_step=1)
    assert list(b.target)==[3]

def test_windows_never_cross_partition_support():
    b=past_windows(np.arange(50.),np.arange(50),4,expected_step=1)
    raw=ordered_split(np.arange(50));out=assign_windows(b,raw)
    for key,inds in out.items():
        allowed=set(raw[key]);assert len(inds)>0
        for j in inds:assert set(range(b.start[j],b.target[j]+1))<=allowed

@pytest.mark.parametrize('t',[[0,0,1,2],[0,2,1,3]])
def test_unsorted_times_rejected(t):
    with pytest.raises(ValueError):past_windows(np.arange(4),t,2)

def test_mst_zero_edges_and_square():
    np.testing.assert_allclose(mst_lengths([[0,0],[1,0],[1,1],[0,1]]),[1,1,1])
    np.testing.assert_allclose(mst_lengths([[0],[0],[1]]),[0,1])
    assert mst_lengths([[1,2]]).size==0

def test_mst_and_persistence_agree():
    from shape_lab.persistence import rips_filtration,persistent_homology
    x=np.random.default_rng(8).normal(size=(12,3))
    bars=persistent_homology(rips_filtration(x,max_homology=0),max_dim=0,include_zero=True)
    np.testing.assert_allclose(mst_lengths(x),sorted(z.death for z in bars if np.isfinite(z.death)))

def test_descriptor_is_finite_and_permutation_consistent_without_ties():
    rng=np.random.default_rng(34);anchors=rng.normal(size=(14,3));q=rng.normal(size=(2,3))
    a=local_topology(q,anchors,k=6);b=local_topology(q,anchors[::-1],k=6)
    assert a.shape==(2,6) and np.isfinite(a).all();np.testing.assert_allclose(a,b)

def test_descriptor_scale_effect_is_explained():
    rng=np.random.default_rng(2);a=rng.normal(size=(10,2));q=rng.normal(size=(1,2))
    x=local_topology(q,a,k=6);y=local_topology(q*2,a*2,k=6)
    np.testing.assert_allclose(y[:,[0,1,2,4,5]],2*x[:,[0,1,2,4,5]])
    np.testing.assert_allclose(y[:,3],x[:,3])

def test_choice_rows_form_unique_sets():
    d,_=load_dataset('modechoice');x,y,ids,features=choice_table(d)
    assert x.shape==(210,13);assert y.shape==(210,);assert len(set(ids))==210
    assert set(y)=={1,2,3,4};assert all('choice' not in c and 'psize' not in c and 'gc' not in c for c in features)

def test_choice_duplicate_or_missing_selected_rejected():
    d,_=load_dataset('modechoice')
    with pytest.raises(ValueError):choice_table(pd.concat([d,d.iloc[[0]]],ignore_index=True))
    d.loc[d.individual==1,'choice']=0
    with pytest.raises(ValueError):choice_table(d)

def test_change_point_has_exact_control():
    k,loss=best_mean_change(np.r_[np.zeros(8),np.ones(8)],min_segment=3)
    assert k==8 and loss==0

def test_seasonal_climatology_is_fitted_only_to_inputs():
    months=np.tile(np.arange(1,13),2);y=months.astype(float)
    m=seasonal_means(y,months);np.testing.assert_allclose(m,np.arange(1,13))
    with pytest.raises(ValueError):seasonal_means([1],[1])
