import pytest
import numpy as np
torch=pytest.importorskip('torch')
from shape_lab.physics import neural as n


def test_hamiltonian_derivative_ordering():
    z=torch.tensor([[2.,3.]],dtype=torch.float64,requires_grad=True)
    H=lambda x:.5*(x*x).sum(dim=-1,keepdim=True)
    np.testing.assert_allclose(n.hamiltonian_field(H,z).detach(),[[3.,-2.]])

def test_lagrangian_hessian_formula():
    L=lambda z:z[1]**2-1.5*z[0]**2
    out=n.lagrangian_acceleration(L,torch.tensor([2.,.4],dtype=torch.float64))
    assert float(out.detach())==pytest.approx(-3.)

def test_singular_lagrangian_rejected():
    with pytest.raises(ValueError):n.lagrangian_acceleration(lambda z:z.sum(),torch.tensor([1.,2.],dtype=torch.float64))

def test_differentiable_rk4_gradient():
    rate=torch.tensor(.3,dtype=torch.float64,requires_grad=True)
    end=n.rk4_torch(lambda t,z:-rate*z,torch.ones(1,dtype=torch.float64),.05,20)[-1].sum()
    grad=torch.autograd.grad(end,rate)[0]
    assert float(grad)==pytest.approx(-np.exp(-.3),abs=1e-7)

def test_deeponet_shape():
    model=n.DeepONet(8,rank=4)
    assert model(torch.zeros(3,8),torch.zeros(9,1)).shape==(3,9)

def test_fno_shape_and_finite_gradient():
    model=n.TinyFNO(width=4,modes=4)
    x=torch.randn(3,16);loss=model(x).square().mean();loss.backward()
    assert model(x).shape==(3,16)
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())
