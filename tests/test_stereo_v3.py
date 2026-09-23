import numpy as np
import pytest
from numpy.testing import assert_allclose
from shape_lab.stereo import depth_from_disparity, reference_sample, sparse_sad, disparity_metrics, point_cloud


def test_disparity_offset_and_units():
    z=depth_from_disparity(np.array([10.,20.,np.nan,np.inf,-31.086]),994.978,.193001,31.086)
    assert_allclose(z[:2],.193001*994.978/(np.array([10,20])+31.086))
    assert np.isnan(z[2:]).all()
    assert z[0]<.193001*994.978/10
    with pytest.raises(ValueError):depth_from_disparity([10],100,0,0)


def test_reference_shape_calibration_and_cloud():
    l,r,d,c=reference_sample()
    assert l.shape==r.shape==(500,741,3)
    assert d.shape==(500,741)
    assert c['length_unit']=='metre'
    cloud,rc=point_cloud(d,c,stride=20)
    assert cloud.shape[1]==3 and rc.shape[1]==2
    assert np.isfinite(cloud).all() and (cloud[:,2]>0).all()


def test_sad_recovers_exact_integer_shift_without_ground_truth_input():
    rng=np.random.default_rng(10);l=rng.normal(size=(20,50));r=np.zeros_like(l);r[:,:-5]=l[:,5:]
    rc=np.array([[6,20],[12,30]])
    pred,margin=sparse_sad(l,r,rc,max_disparity=10,radius=2)
    assert_allclose(pred,5);assert (margin>0).all()


def test_sad_border_is_missing_not_zero():
    a=np.ones((10,12))
    p,_=sparse_sad(a,a,np.array([[0,0],[5,5]]),max_disparity=4,radius=2)
    assert np.isnan(p[0])
    with pytest.raises(ValueError):sparse_sad(a,a,np.array([[1,1]]),-1,1)


def test_metrics_coverage_and_empty_denominator():
    m=disparity_metrics(np.array([1,3,np.nan]),np.array([1,1,2]))
    assert m['evaluated']==2 and m['eligible']==3 and np.isclose(m['coverage'],2/3)
    assert m['mean_absolute_error_px']==1
    m=disparity_metrics([np.nan],[1]);assert m['mean_absolute_error_px'] is None and m['coverage']==0
