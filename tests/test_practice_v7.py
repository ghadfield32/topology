import importlib
import numpy as np
import pytest

def module():
    try: return importlib.import_module('shape_lab.practice_v7')
    except ModuleNotFoundError: pytest.fail('Practice reference functions are not implemented')

def test_table_shape():
    assert module().table_dimensions(np.ones((210,7))) == (210,7)

def test_compactness():
    assert np.allclose(module().compactness(np.array([np.pi]), np.array([2*np.pi])),1)

def test_training_scaling():
    c,s=module().fit_scaler(np.array([[0.,9],[2.,9]]))
    assert np.allclose(c,[1,9]) and np.allclose(s,[1,1])

def test_class_counts():
    assert module().class_counts([3,1,3,2]) == {1:1,2:1,3:2}

def test_absolute_errors():
    assert np.allclose(module().absolute_errors([1,2,3],[2,2,1]),[1,0,2])

def test_interval_bounds():
    lo,hi=module().interval_bounds([2.,5.],3.)
    assert np.allclose(lo,[-1,2]) and np.allclose(hi,[5,8])

def test_empirical_coverage():
    assert module().empirical_coverage([0,1,2],[-1,0,0],[0,1,1]) == 2/3

def test_mean_baseline():
    assert np.allclose(module().mean_baseline([2.,6.],3),[4,4,4])

def test_shared_rows():
    assert module().shared_rows([0,2,3],[1,3,4]) == [3]

def test_shared_units():
    assert module().shared_units([0,2],[1,3],['a','a','b','c']) == ['a']

def test_group_partition():
    a,b=module().partition_by_units(['a','b','a','c'],['b'])
    assert a.tolist()==[1] and b.tolist()==[0,2,3]

def test_apply_scaler():
    assert np.allclose(module().apply_scaler([[6,2]],[2,2],[2,1]),[[2,0]])

def test_energy():
    assert module().oscillator_energy([.96,-.2]) == pytest.approx(.4808)

def test_symplectic_not_energy():
    A=np.array([[.96,.2],[-.2,1.]])
    assert module().symplectic_defect(A)<1e-14
    assert not np.allclose(A.T@A,np.eye(2))

def test_sphere_step():
    x=module().sphere_newton_step([2.,0.])
    assert np.allclose(x,[1.25,0]) and np.dot(x,x)-1 == pytest.approx(.5625)

def test_gradient_conflict():
    assert module().gradient_inner_product([1,0],[-1,0]) == -1

@pytest.mark.parametrize('fn,args',[
 ('compactness',([1],[0])),('fit_scaler',([[np.nan]],)),
 ('table_dimensions',([1,2],)),('absolute_errors',([1],[1,2])),
 ('interval_bounds',([1],-1)),('sphere_newton_step',([0,0],)),
 ('symplectic_defect',(np.eye(3),)),('apply_scaler',([[1]],[0],[0])),
])
def test_invalid(fn,args):
    with pytest.raises(ValueError):getattr(module(),fn)(*args)
