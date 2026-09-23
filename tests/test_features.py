import numpy as np
import pytest
from shape_lab.persistence import Interval
from shape_lab.features import persistence_features,persistence_landscape,persistence_image,delay_embedding

def test_features_empty_are_finite():
    f=persistence_features([])
    assert f.shape==(20,)
    assert np.array_equal(f,np.zeros(20))

def test_features_essential_not_in_lifetime_sum():
    b=[Interval(0,0,float('inf'),(0,),None)]
    f=persistence_features(b)
    assert f[0]==0 and f[2]==0
    assert np.all(f[5:10]==1)
    assert np.isfinite(f).all()

def test_landscape_single_tent():
    assert np.array_equal(persistence_landscape([[0,2]],np.array([0,1,2]),1),[[0,1,0]])

def test_landscape_second_level_empty():
    assert np.array_equal(persistence_landscape([[0,2]],np.array([0,1,2]),2)[1],[0,0,0])

def test_image_mass():
    edges=np.linspace(-10,10,11)
    image=persistence_image([[0,2]],edges,edges,.1)
    assert image.shape==(10,10)
    assert image.sum()==pytest.approx(2)

def test_delay_embedding_values():
    assert np.array_equal(delay_embedding(np.arange(6),3,2),[[0,2,4],[1,3,5]])

def test_delay_embedding_rejects_short_input():
    with pytest.raises(ValueError): delay_embedding(np.arange(3),3,2)
