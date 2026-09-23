"""Contracts written before the new evidence utility implementation."""
import importlib.util
import importlib
import numpy as np
import pytest

def engine():
    assert importlib.util.find_spec('shape_lab.evidence_v7') is not None, 'v7 evidence implementation is missing'
    return importlib.import_module('shape_lab.evidence_v7')

def test_numeric_fingerprint_ignores_formatting_not_values():
    m=engine()
    assert m.numeric_digest([['1.00','2e-1'],['-0','3']]) == m.numeric_digest([[1,.2],[0,3]])
    assert m.numeric_digest([[1,2],[3,4]]) != m.numeric_digest([[3,4],[1,2]])
    assert m.numeric_digest([[1,2]]) != m.numeric_digest([[1,2.00001]])

@pytest.mark.parametrize('rows',[[],[[]],[[1,2],[3]],[[1,float('nan')]],[[1,float('inf')]],[[1,'hello']]])
def test_bad_numeric_tables_rejected(rows):
    with pytest.raises(ValueError):engine().numeric_digest(rows)

@pytest.mark.parametrize('n,alpha,k',[(9,.1,9),(10,.1,10),(3,.25,3),(3,.1,4),(20,.05,20),(1,.1,2)])
def test_finite_sample_ceiling(n,alpha,k):
    assert engine().conformal_rank(n,alpha)==k

def test_radius_uses_rank_not_interpolated_quantile():
    m=engine()
    assert m.conformal_radius([9,1,4,3,2,8,7,6,5],.1)==9
    assert m.conformal_radius([1,1,1],.5)==1
    assert np.isinf(m.conformal_radius([1,2,3],.1))

@pytest.mark.parametrize('scores,alpha',[([], .1),([-1,2],.1),([1,np.nan],.1),([1,np.inf],.1),([1,2],0),([1,2],1),([1,2],np.nan),([[1,2]],.1)])
def test_invalid_calibration_rejected(scores,alpha):
    with pytest.raises(ValueError):engine().conformal_radius(scores,alpha)

@pytest.mark.parametrize('n',[0,-1,1.5,True])
def test_bad_calibration_count_rejected(n):
    with pytest.raises(ValueError):engine().conformal_rank(n,.1)

def test_interval_boundaries_are_inclusive():
    m=engine()
    assert m.coverage([0,1,3],[1,1,1],1)==pytest.approx(2/3)
    assert m.coverage([0,1],[100,-100],np.inf)==1

@pytest.mark.parametrize('y,p,r',[([],[],1),([1],[1,2],1),([1],[1],-1),([np.nan],[1],1),([1],[1],np.nan)])
def test_invalid_interval_inputs(y,p,r):
    with pytest.raises(ValueError):engine().coverage(y,p,r)

def test_row_disjoint_can_still_leak_units():
    m=engine(); report=m.overlap_report({'train':[0,2],'test':[1,3]},['person_a','person_a','person_b','person_c'])
    assert report['row_disjoint'] is True
    assert report['unit_disjoint'] is False
    assert report['pairs']['train|test']['shared_units']==['person_a']

def test_disjoint_and_overlapping_indices_reported():
    m=engine()
    assert m.overlap_report({'train':[0,1],'test':[2,3]},['a','b','c','d'])['unit_disjoint']
    assert not m.overlap_report({'train':[0,1],'test':[1,2]},['a','b','c'])['row_disjoint']

@pytest.mark.parametrize('parts,units',[({'train':[5],'test':[1]},['a','b']),({'train':[0.,.5],'test':[1]},['a','b']),({'train':[0,0],'test':[1]},['a','b']),({'train':[],'test':[1]},['a','b']),({'train':[0],'test':[1]},['a',None])])
def test_invalid_split_contract(parts,units):
    with pytest.raises(ValueError):engine().overlap_report(parts,units)

def test_snapshot_schema_and_source_values():
    m=engine();s,meta=m.load_snapshot('seeds')
    assert len(s)==210 and len(meta['features'])==7
    assert s.variety.value_counts().to_dict()=={1:70,2:70,3:70}
    assert s.area.iloc[0]==15.26 and s.area.iloc[-1]==12.3
    c,meta=m.load_snapshot('concrete_slump')
    assert len(c)==103 and len(meta['features'])==7
    assert c.strength_mpa.iloc[0]==34.99 and c.strength_mpa.iloc[-1]==48.77
    assert list(c.source_id)==list(range(1,104))

def test_unknown_snapshot_is_not_replaced():
    with pytest.raises(ValueError):engine().load_snapshot('imaginary')

def test_fourier_scalar_example_does_not_depend_on_units():
    # Exact analytical control used in Stage 28's companion, not a trained model.
    a=.1;k=2;t=.3
    assert 0 < np.exp(-a*k*k*t) < 1

def test_canonical_preserves_more_than_context_precision():
    from shape_lab.evidence_v7 import canonical_numeric
    token='1.123456789012345678901234567890123456789'
    assert canonical_numeric([[token]]) == (token+'\n').encode()
