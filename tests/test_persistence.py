import numpy as np
import pytest
from shape_lab.algebra import betti_numbers
from shape_lab.persistence import rips_filtration, persistent_homology, ordered_filtration, finite_bottleneck, pixel_filtration

SQUARE=np.array([[0,0],[1,0],[1,1],[0,1]],dtype=float)

def dgm(f,k):
    return sorted((b.birth,b.death) for b in persistent_homology(f,max_dim=k) if b.dim==k)

def test_square_bar():
    assert np.allclose(dgm(rips_filtration(SQUARE),1), [[1,np.sqrt(2)]])

def test_square_h0():
    bars=dgm(rips_filtration(SQUARE),0)
    assert bars == [(0,1),(0,1),(0,1),(0,np.inf)]

def test_full_triangle_no_positive_h1():
    x=np.array([[0,0],[1,0],[0,1]])
    assert dgm(rips_filtration(x),1)==[]

def test_permutation_translation_rotation():
    a=dgm(rips_filtration(SQUARE),1)
    for x in [SQUARE[[2,0,3,1]], SQUARE+25, SQUARE @ np.array([[0,-1],[1,0]])]:
        assert np.allclose(a,dgm(rips_filtration(x),1))

def test_scale_equivariance():
    assert np.allclose(dgm(rips_filtration(SQUARE*3),1),np.array(dgm(rips_filtration(SQUARE),1))*3)

def test_duplicate_observations_allowed_and_zero_bars_not_reported():
    assert dgm(rips_filtration(np.array([[0.],[0.],[1.]])),0)==[(0,1),(0,np.inf)]

def test_truncated_loop_has_infinite_endpoint_but_not_full_filtration_essential():
    assert dgm(rips_filtration(SQUARE,max_edge=1.1),1)==[(1,np.inf)]

def test_faces_precede_cofaces_at_ties():
    f=ordered_filtration([((0,1),0),((1,),0),((0,),0)])
    assert f==[((0,),0),((1,),0),((0,1),0)]

@pytest.mark.parametrize('f', [[((0,),2),((1,),0),((0,1),1)], [((0,1),1)], [((0,),0),((0,),0)], [((0,),float('nan'))]])
def test_bad_filtrations_rejected(f):
    with pytest.raises(ValueError): ordered_filtration(f)

def test_betti_from_intervals_matches_direct_ranks():
    x=np.random.default_rng(5).normal(size=(7,2))
    f=rips_filtration(x)
    bars=persistent_homology(f,max_dim=1)
    for t in sorted(set(v for _,v in f)):
        b=betti_numbers([s for s,v in f if v<=t],max_dim=1)
        assert b == [sum(z.dim==k and z.birth<=t<z.death for z in bars) for k in (0,1)]

@pytest.mark.parametrize('a,b,expected', [([],[],0), ([[0,2]],[],1), ([[0,2]],[[.1,2.1]],.1), ([[0,2],[0,2]],[[0,2]],1)])
def test_bottleneck(a,b,expected):
    assert finite_bottleneck(a,b)==pytest.approx(expected)

def test_bottleneck_rejects_infinity():
    with pytest.raises(ValueError): finite_bottleneck([[0,np.inf]],[])

def test_pixel_ring_bar_and_full_grid():
    values=np.zeros((3,3)); values[1,1]=1
    f=pixel_filtration(values)
    assert dgm(f,1)==[(0,1)]
    assert betti_numbers([s for s,_ in f])==[1,0,0]

def test_pixels_touching_at_corner_are_connected():
    values=np.array([[0,1],[1,0]])
    f=pixel_filtration(values)
    assert betti_numbers([s for s,t in f if t<=0],max_dim=1)==[1,0]

def test_pixel_h1_stability_on_same_grid():
    rng=np.random.default_rng(42)
    a=rng.uniform(size=(4,4)); b=a+rng.uniform(-.04,.04,size=(4,4))
    assert finite_bottleneck(dgm(pixel_filtration(a),1), dgm(pixel_filtration(b),1)) <= np.max(abs(a-b))+1e-12
