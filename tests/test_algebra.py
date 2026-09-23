import numpy as np
import pytest
from shape_lab.algebra import rank_mod2, closure, validate_complex, boundary_matrix, betti_numbers, euler_characteristic

@pytest.mark.parametrize('a,rank', [([[1,1,0],[1,0,1],[0,1,1]],2), ([[0,0],[0,0]],0), ([[1,0],[0,1]],2), (np.empty((0,3),dtype=int),0)])
def test_binary_rank(a,rank):
    assert rank_mod2(np.array(a)) == rank

@pytest.mark.parametrize('facets,expected', [([(0,),(1,),(2,)], [3]), ([(0,1),(1,2)], [1,0]), ([(0,1),(1,2),(0,2)], [1,1]), ([(0,1,2)], [1,0,0]), ([(0,1,2),(0,1,3),(0,2,3),(1,2,3)], [1,0,1]), ([(0,1,2,3)], [1,0,0,0])])
def test_known_betti(facets,expected):
    assert betti_numbers(closure(facets)) == expected

@pytest.mark.parametrize('facets', [[(0,1,2)],[(0,1,2,3)],[(0,1,2),(1,2,3)],[(0,1),(1,2)]])
def test_boundary_squared_and_euler(facets):
    s=closure(facets)
    for k in range(1,max(map(len,s))):
        assert not np.any((boundary_matrix(s,k-1) @ boundary_matrix(s,k)) % 2)
    b=betti_numbers(s)
    assert euler_characteristic(s) == sum((-1)**i*x for i,x in enumerate(b))

def test_missing_face_rejected():
    with pytest.raises(ValueError, match='face'):
        validate_complex([(0,),(1,),(0,1,2)])

def test_repeated_vertex_rejected():
    with pytest.raises(ValueError):
        closure([(0,0,1)])

def test_empty_complex():
    assert betti_numbers([]) == []
    assert euler_characteristic([]) == 0
