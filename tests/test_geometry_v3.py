import importlib.util
import numpy as np
import pytest
from numpy.testing import assert_allclose
from shape_lab.geometry import (sphere_chart, sphere_unchart, skew, exp_so3, make_transform,
    transform_points, inverse_transform, project, unproject, triangulate_dlt, fit_similarity,
    rotation_error_deg, finite_jacobian)


def test_sphere_charts_roundtrip_and_transition():
    x=np.array([[0.6,0,0.8],[0,1,0],[0.3,0.4,-np.sqrt(.75)]])
    for pole in ['north','south']:
        a=sphere_chart(x,pole)
        assert_allclose(sphere_unchart(a,pole),x,atol=1e-12)
    a=sphere_chart(x,'north'); b=sphere_chart(x,'south')
    assert_allclose(b,a/(a*a).sum(1)[:,None],atol=1e-12)


def test_chart_excludes_pole_and_non_sphere():
    with pytest.raises(ValueError):sphere_chart([[0,0,1]],'north')
    with pytest.raises(ValueError):sphere_chart([[0,0,2]],'south')
    with pytest.raises(ValueError):sphere_chart([[0,0,1]],'other')


@pytest.mark.parametrize('v',[[0,0,0],[1e-10,0,0],[.2,-.3,.7],[0,0,np.pi]])
def test_rotation_exponential_against_scipy(v):
    from scipy.spatial.transform import Rotation
    r=exp_so3(v)
    assert_allclose(r,Rotation.from_rotvec(v).as_matrix(),atol=1e-12)
    assert_allclose(r.T@r,np.eye(3),atol=1e-12)
    assert np.isclose(np.linalg.det(r),1)


def test_skew_cross_product():
    a=np.array([1,2,3]);b=np.array([-2,1,4])
    assert_allclose(skew(a)@b,np.cross(a,b))


def test_transform_composition_and_inverse():
    a=make_transform(exp_so3([.1,.2,0]),[1,2,3]);b=make_transform(exp_so3([0,0,.4]),[-2,0,1])
    p=np.array([[1,3,2],[2,1,8]])
    assert_allclose(transform_points(a@b,p),transform_points(a,transform_points(b,p)))
    assert_allclose(transform_points(inverse_transform(a),transform_points(a,p)),p,atol=1e-12)
    assert_allclose(inverse_transform(a),np.linalg.inv(a),atol=1e-12)
    with pytest.raises(ValueError):make_transform(np.diag([1,1,-1]),[0,0,0])


def test_projection_depth_and_ray_ambiguity():
    k=np.array([[800,0,320],[0,800,240],[0,0,1.]])
    p=np.array([[.2,.3,2.],[-.5,.1,3.]])
    uv,z=project(p,k)
    assert_allclose(unproject(uv,z,k),p)
    assert_allclose(project(4*p,k)[0],uv)
    with pytest.raises(ValueError):project([[0,0,-1]],k)
    with pytest.raises(ValueError):unproject(uv,[1,-1],k)


def test_dlt_recovers_points_with_different_principal_points():
    k1=np.array([[800,0,320],[0,800,240],[0,0,1.]])
    k2=k1.copy();k2[0,2]+=31
    t=make_transform(np.eye(3),[-.2,0,0]);p=np.array([[.2,.1,2],[-.2,-.1,3],[0,0,4.]])
    p1=k1@np.eye(4)[:3];p2=k2@t[:3]
    uv1=project(p,k1)[0];uv2=project(transform_points(t,p),k2)[0]
    xyz=triangulate_dlt(p1,p2,uv1,uv2)
    assert_allclose(xyz,p,atol=1e-11)
    if importlib.util.find_spec('cv2'):
        import cv2
        q=cv2.triangulatePoints(p1,p2,uv1.T,uv2.T);q=(q[:3]/q[3]).T
        assert_allclose(xyz,q,atol=1e-10)


def test_dlt_degenerate_cameras_rejected():
    p=np.eye(4)[:3]
    with pytest.raises(ValueError):triangulate_dlt(p,p,[[0,0]],[[0,0]])


def test_similarity_fit_train_only_and_no_reflection():
    rng=np.random.default_rng(100);x=rng.normal(size=(30,3));r=exp_so3([.2,-.3,.4]);y=2.5*(x@r.T)+[4,-2,3]
    s,rr,t=fit_similarity(x[:10],y[:10])
    assert_allclose(s,2.5);assert_allclose(rr,r,atol=1e-12)
    assert_allclose(s*x[10:]@rr.T+t,y[10:],atol=1e-12)
    assert rotation_error_deg(rr,r)<1e-5
    with pytest.raises(ValueError):fit_similarity([[0,0,0],[1,0,0],[2,0,0]],[[0,0,0],[1,0,0],[2,0,0]])


def test_finite_jacobian():
    j=finite_jacobian(lambda x:np.array([x[0]**2+x[1],np.sin(x[1])]),[2,.3])
    assert_allclose(j,[[4,1],[0,np.cos(.3)]],atol=1e-7)


def test_chart_inverse_analytic_jacobian():
    from shape_lab.geometry import sphere_unchart,finite_jacobian
    a=np.array([.2,-.4]);q=a@a
    for pole,sign in [('south',-1),('north',1)]:
        actual=finite_jacobian(lambda v:sphere_unchart(v[None,:],pole)[0],a)
        expected=np.vstack([2*np.eye(2)/(1+q)-4*np.outer(a,a)/(1+q)**2,sign*4*a/(1+q)**2])
        assert np.allclose(actual,expected,atol=1e-8)
