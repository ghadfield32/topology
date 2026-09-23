import numpy as np
import pytest
from shape_lab.physics import classical as c, constraints as p, gradients as g, operators as o


def test_symplectic_is_not_exact_energy():
    M = c.oscillator_matrix(.2, 'symplectic_euler')
    assert c.symplectic_defect(M) < 1e-12
    z = M @ np.array([1., 0.])
    assert c.energy(z) == pytest.approx(.4808)
    assert c.energy(z) != pytest.approx(.5)

@pytest.mark.parametrize('method', ['exact', 'symplectic_euler', 'verlet', 'midpoint'])
def test_linear_symplectic_maps(method):
    M = c.oscillator_matrix(.1, method)
    assert np.linalg.det(M) == pytest.approx(1)
    assert c.symplectic_defect(M) < 1e-12

def test_volume_is_not_symplectic_in_four_dimensions():
    M = np.diag([2., .5, 1., 1.])
    assert np.linalg.det(M) == pytest.approx(1)
    assert c.symplectic_defect(M) > .1

def test_explicit_euler_grows_energy():
    Z = c.oscillator_rollout([1., 0.], .1, 200, 'euler')
    assert c.energy(Z[-1]) > 3

def test_flow_domain_and_inverse():
    x=np.array([-.2, .3])
    np.testing.assert_allclose(c.quadratic_flow(c.quadratic_flow(x,.5),-.5),x)
    with pytest.raises(ValueError): c.quadratic_flow(2., .5)
    with pytest.raises(ValueError): c.quadratic_flow(2., 1.)

def test_coupling_inverse_and_logdet():
    X = np.array([[.1, 2.], [-.4, 1.]])
    Y, ld = c.coupling(X)
    np.testing.assert_allclose(c.coupling_inverse(Y), X)
    np.testing.assert_allclose(ld, .2*np.tanh(X[:,0]))

def test_rk4_convergence():
    f=lambda t,z: np.array([z[1],-z[0]])
    expected=np.array([np.cos(1),-np.sin(1)])
    a=c.integrate_rk4(f,[1,0],.1,10)[-1]
    b=c.integrate_rk4(f,[1,0],.05,20)[-1]
    assert np.linalg.norm(a-expected) > 10*np.linalg.norm(b-expected)

def test_nonlinear_projection_is_not_one_step_exact():
    z=p.constraint_correction(np.array([2.,0.]),np.array([3.]),np.array([[4.,0.]]))
    np.testing.assert_allclose(z,[1.25,0])
    assert z@z-1 == pytest.approx(.5625)

def test_sphere_iteration_and_affine_projection():
    z, history=p.project_sphere([2.,.2])
    assert abs(z@z-1)<1e-10
    assert len(history)>1
    z=p.project_affine([3.,4.],[[1.,1.]],[1.])
    assert sum(z)==pytest.approx(1.)

def test_singular_projection_rejected():
    with pytest.raises(ValueError): p.project_sphere([0.,0.])
    with pytest.raises(ValueError): p.project_affine([1,2],[[1,1],[2,2]],[1,2])

def test_retraction_tangent_contract():
    out=p.sphere_retraction([1,0],[0,.1])
    assert np.linalg.norm(out)==pytest.approx(1)
    with pytest.raises(ValueError):p.sphere_retraction([1,0],[.1,0])

@pytest.mark.parametrize('normalise',[False,True])
def test_pair_pcgrad_is_nondestructive(normalise):
    G=np.array([[1.,0.],[-1.,1.]])
    d=g.pcgrad(G,normalise=normalise,seed=0)
    assert np.all(G@d>=-1e-12)

def test_opposed_gradients_no_strict_descent():
    G=np.array([[1.,0.],[-1.,0.]])
    np.testing.assert_allclose(g.pcgrad(G,normalise=True),[0,0])
    result=g.config_direction(G)
    assert not result['compatible']
    assert not result['strict_common_descent']

def test_config_compatible_and_scale():
    G=np.array([[2.,0.],[0.,1.]])
    result=g.config_direction(G)
    assert result['compatible'] and result['strict_common_descent']
    np.testing.assert_allclose(result['direction'],[1.5,1.5])

def test_zero_gradient_is_reported():
    result=g.config_direction([[0,0],[1,0]])
    assert not result['strict_common_descent']
    assert result['zero_rows']==[0]

def test_heat_preserves_mean_and_damps_nonconstant_modes():
    x=np.arange(32)/32
    u=2+np.sin(2*np.pi*x)
    v=o.heat_step(u,.03,.1)
    assert v.mean()==pytest.approx(2.)
    np.testing.assert_allclose(v,2+np.exp(-.03*(2*np.pi)**2*.1)*np.sin(2*np.pi*x))
    assert np.linalg.norm(v-2)<np.linalg.norm(u-2)

def test_poisson_baseline_converges():
    x,u=o.poisson_fd(31)
    x2,u2=o.poisson_fd(63)
    assert np.max(abs(u2-np.sin(np.pi*x2))) < .3*np.max(abs(u-np.sin(np.pi*x)))

def test_pair_forces_and_rotation():
    X=np.array([[0.,0.],[1.,0.],[0.,1.]])
    F=o.pair_forces(X,[(0,1,2.),(1,2,1.)])
    np.testing.assert_allclose(F.sum(axis=0),0,atol=1e-12)
    R=np.array([[0.,-1.],[1.,0.]])
    np.testing.assert_allclose(o.pair_forces(X@R.T,[(0,1,2.),(1,2,1.)]),F@R.T)

def test_attention_rows_are_not_mass_conservation():
    A=np.array([[1.,0.],[1.,0.]])
    assert np.allclose(A.sum(axis=1),1)
    assert (A@np.array([1.,0.])).sum()==2
    np.testing.assert_allclose(o.mean_correct(A@np.array([1.,0.]),.5).mean(),.5)

@pytest.mark.parametrize('call',[
 lambda:c.oscillator_matrix(float('nan'),'exact'),
 lambda:c.oscillator_rollout([1,2],.1,-1),
 lambda:g.pcgrad([[np.nan,0],[1,0]]),
 lambda:o.heat_step([1,2],-.1,.2),
 lambda:o.poisson_fd(0),
])
def test_invalid_inputs_fail_loudly(call):
    with pytest.raises((ValueError,TypeError)):call()
