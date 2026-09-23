"""Synthetic contract fixtures are not VGGT inference results."""
import numpy as np
import pytest
from shape_lab.model_contract import validate_original_vggt, sample_candidate_points


def fixture():
    s,h,w=2,4,6
    return dict(depth=np.ones((1,s,h,w,1)),depth_conf=np.full((1,s,h,w),4.),
                world_points=np.ones((1,s,h,w,3)),world_points_conf=np.full((1,s,h,w),7.),
                images=np.zeros((1,s,3,h,w)),pose_enc=np.zeros((1,s,9)),
                extrinsics=np.tile(np.c_[np.eye(3),np.zeros(3)],(1,s,1,1)),
                intrinsics=np.tile(np.eye(3),(1,s,1,1)))


def test_shapes_and_confidence_not_probability():
    a=fixture();report=validate_original_vggt(a)
    assert report['frames']==2 and report['metric_validated'] is False
    assert report['track_coordinate_dimension'] is None

@pytest.mark.parametrize('key,value',[('depth',np.zeros((1,2,4,6,1))),('world_points',np.full((1,2,4,6,3),np.nan)),('depth_conf',np.ones((2,4,6))),('images',np.full((1,2,3,4,6),2))])
def test_invalid_contract(key,value):
    a=fixture();a[key]=value
    with pytest.raises(ValueError):validate_original_vggt(a)


def test_tracks_are_two_dimensional():
    a=fixture();a.update(track=np.zeros((1,2,3,2)),vis=np.ones((1,2,3)),conf=np.ones((1,2,3)))
    assert validate_original_vggt(a)['track_coordinate_dimension']==2
    a['track']=np.zeros((1,2,3,3))
    with pytest.raises(ValueError):validate_original_vggt(a)


def test_candidate_sampling_preserves_ids_and_cap():
    a=fixture();X,ids=sample_candidate_points(a,frame=1,max_points=5,confidence_quantile=.5)
    assert X.shape==(5,3) and ids.shape==(5,3)
    assert np.all(ids[:,0]==1) and len(np.unique(ids,axis=0))==5
    with pytest.raises(ValueError):sample_candidate_points(a,frame=0,max_points=100)
