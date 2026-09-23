"""Optional, small PyTorch CPU examples, written for inspection rather than speed.

Architecture demos are not reproductions of source-paper benchmarks. Generated
analytic data is explicitly labelled manufactured in every training result.
"""
from __future__ import annotations
from collections.abc import Callable
import copy
import math
import numpy as np
import torch
from torch import nn
from .operators import heat_step


def setup(seed: int=5):
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    return np.random.default_rng(seed)


def mlp(inputs: int,outputs: int,width: int=32):
    return nn.Sequential(nn.Linear(inputs,width),nn.Tanh(),nn.Linear(width,width),nn.Tanh(),nn.Linear(width,outputs))


def hamiltonian_field(H: Callable,z: torch.Tensor,create_graph: bool=True):
    if z.ndim!=2 or z.shape[1]!=2 or not z.requires_grad:raise ValueError('Use [batch,2] (q,p) with requires_grad=True.')
    grad=torch.autograd.grad(H(z).sum(),z,create_graph=create_graph)[0]
    return torch.stack([grad[:,1],-grad[:,0]],dim=1)


def lagrangian_acceleration(L: Callable,z: torch.Tensor):
    """One degree of freedom, autonomous regular L(q,v); no external forces."""
    if z.shape!=(2,):raise ValueError('Single state (q,v) required.')
    z=z.detach().clone().requires_grad_(True)
    grad=torch.autograd.functional.jacobian(L,z,create_graph=True)
    hess=torch.autograd.functional.hessian(L,z,create_graph=True)
    mass=hess[1,1]
    if not torch.isfinite(mass) or abs(float(mass.detach()))<1e-12:raise ValueError('Singular velocity Hessian; regular Lagrangian formula unavailable.')
    return (grad[0]-hess[1,0]*z[1])/mass


def rk4_torch(f: Callable,z0: torch.Tensor,h: float,steps: int):
    """Differentiate through this discrete RK4 program, not an adjoint solver."""
    if not math.isfinite(h) or not isinstance(steps,int) or not 0<=steps<=10000:raise ValueError('Finite h and 0–10000 steps required.')
    z=z0;out=[z];t=0.
    for _ in range(steps):
        a=f(t,z);b=f(t+h/2,z+h*a/2);c=f(t+h/2,z+h*b/2);d=f(t+h,z+h*c)
        z=z+h*(a+2*b+2*c+d)/6;t+=h;out.append(z)
    return torch.stack(out)


def train_mechanics(steps: int=500,seed: int=5):
    """Train an unconstrained scalar H network and a restricted unit-mass L.

Derivative supervision on independently sampled synthetic phase-space points.
The restricted L learns only V(q), so this is not a general LNN benchmark.
"""
    setup(seed)
    train=torch.rand(256,2,dtype=torch.float64)*2.4-1.2
    test=torch.rand(128,2,dtype=torch.float64)*2.4-1.2
    target=torch.stack([train[:,1],-train[:,0]],dim=1)
    truth=torch.stack([test[:,1],-test[:,0]],dim=1)
    H=mlp(2,1).double();V=mlp(1,1).double()
    hopt=torch.optim.Adam(H.parameters(),lr=.003);lopt=torch.optim.Adam(V.parameters(),lr=.003)
    history=[]
    for i in range(steps):
        z=train.detach().clone().requires_grad_(True)
        hp=hamiltonian_field(H,z);hl=(hp-target).square().mean()
        hopt.zero_grad();hl.backward();hopt.step()
        q=train[:,:1].detach().clone().requires_grad_(True)
        acc=-torch.autograd.grad(V(q).sum(),q,create_graph=True)[0]
        ll=(acc+q).square().mean();lopt.zero_grad();ll.backward();lopt.step()
        if i%50==0 or i==steps-1:history.append([i,float(hl.detach()),float(ll.detach())])
    z=test.detach().clone().requires_grad_(True);hp=hamiltonian_field(H,z,False).detach()
    q=test[:,:1].detach().clone().requires_grad_(True);lp=-torch.autograd.grad(V(q).sum(),q)[0].detach()
    return {'H':H,'V':V,'test':test.numpy(),'hnn_prediction':hp.numpy(),'lnn_acceleration':lp.numpy(),
            'history':history,'metrics':{'data_kind':'manufactured unit oscillator derivative samples',
            'seed':seed,'steps':steps,'train_states':256,'test_states':128,
            'hnn_test_derivative_mse':float((hp-truth).square().mean()),
            'restricted_lnn_test_acceleration_mse':float((lp+test[:,:1]).square().mean()),
            'scope':'No measured trajectories; no canonical-coordinate learning; no general-LNN Hessian training.'}}


def train_poisson(steps: int=500,seed: int=5):
    """Actual residual training, strong-form Poisson with hard zero endpoints."""
    setup(seed);net=mlp(1,1).double();opt=torch.optim.Adam(net.parameters(),lr=.003)
    grid=torch.linspace(0,1,65,dtype=torch.float64)[1:-1,None]
    history=[]
    for i in range(steps):
        x=grid.detach().clone().requires_grad_(True)
        u=x*(1-x)*net(x)
        du=torch.autograd.grad(u.sum(),x,create_graph=True)[0]
        ddu=torch.autograd.grad(du.sum(),x,create_graph=True)[0]
        r=-ddu-math.pi**2*torch.sin(math.pi*x);loss=r.square().mean()
        opt.zero_grad();loss.backward();opt.step()
        if i%50==0 or i==steps-1:history.append([i,float(loss.detach())])
    test=torch.linspace(0,1,257,dtype=torch.float64)[:,None].requires_grad_(True)
    u=test*(1-test)*net(test)
    du=torch.autograd.grad(u.sum(),test,create_graph=True)[0]
    ddu=torch.autograd.grad(du.sum(),test)[0]
    residual=-ddu-math.pi**2*torch.sin(math.pi*test)
    truth=torch.sin(math.pi*test);relative=float((torch.linalg.norm(u-truth)/torch.linalg.norm(truth)).detach())
    return {'model':net,'x':test.detach().numpy().ravel(),'prediction':u.detach().numpy().ravel(),'history':history,
            'metrics':{'data_kind':'manufactured boundary-value problem; no observed PDE data',
             'seed':seed,'steps':steps,'collocation_interior':63,'evaluation_points':257,
             'relative_l2_error':relative,'grid_residual_rmse':float(residual.square().mean().sqrt().detach()),
             'endpoint_max_error':float(u[[0,-1]].abs().max().detach()),
             'scope':'Grid diagnostics are not a uniform PDE-error certificate.'}}


class DeepONet(nn.Module):
    """Branch sensors times coordinate-dependent trunk basis, scalar output."""
    def __init__(self,sensors: int,rank: int=16):
        super().__init__();self.branch=mlp(sensors,rank,48);self.trunk=mlp(1,rank,48)
        self.bias=nn.Parameter(torch.zeros(()));self.rank=rank
    def forward(self,u,x):
        return self.branch(u)@self.trunk(x).T/math.sqrt(self.rank)+self.bias


class SpectralLayer(nn.Module):
    def __init__(self,width: int,modes: int):
        super().__init__();self.modes=modes
        self.weight=nn.Parameter(torch.randn(width,width,modes,dtype=torch.cfloat)/width)
    def forward(self,x):
        xf=torch.fft.rfft(x,dim=-1);m=min(self.modes,xf.shape[-1])
        out=torch.zeros(x.shape[0],x.shape[1],xf.shape[-1],device=x.device,dtype=xf.dtype)
        out[:,:,:m]=torch.einsum('bim,iom->bom',xf[:,:,:m],self.weight[:,:,:m])
        return torch.fft.irfft(out,n=x.shape[-1],dim=-1)


class TinyFNO(nn.Module):
    """Two Fourier+pointwise layers. Educational periodic 1D FNO variant."""
    def __init__(self,width: int=8,modes: int=8):
        super().__init__();self.lift=nn.Conv1d(1,width,1)
        self.spectral=nn.ModuleList([SpectralLayer(width,modes) for _ in range(2)])
        self.local=nn.ModuleList([nn.Conv1d(width,width,1) for _ in range(2)])
        self.readout=nn.Conv1d(width,1,1)
    def forward(self,u):
        x=self.lift(u[:,None,:])
        for spectral,local in zip(self.spectral,self.local):x=torch.nn.functional.gelu(spectral(x)+local(x))
        return self.readout(x)[:,0,:]


def heat_family(count: int,n: int,seed: int=5):
    rng=np.random.default_rng(seed);x=np.arange(n)/n
    coeff=rng.normal(size=(count,7))
    u=coeff[:,0,None]*.3
    u=np.repeat(u,n,axis=1)
    for k in range(1,4):
        u+=coeff[:,2*k-1,None]*np.sin(2*np.pi*k*x)/k
        u+=coeff[:,2*k,None]*np.cos(2*np.pi*k*x)/k
    return x,u.astype('float32'),heat_step(u,.03,.15).astype('float32')


def train_operators(steps: int=400,seed: int=5):
    """Fixed-period, fixed-time heat family; split by entire input function."""
    setup(seed);x,u,y=heat_family(160,32,seed)
    u=torch.from_numpy(u);y=torch.from_numpy(y);coords=torch.from_numpy(x.astype('float32')[:,None])
    splits={'train':slice(0,96),'validation':slice(96,128),'test':slice(128,160)}
    predictions={};metrics={};histories={}
    for name,model in [('DeepONet',DeepONet(32)),('FNO',TinyFNO())]:
        opt=torch.optim.Adam(model.parameters(),lr=.003);best=float('inf');state=None;best_step=0;history=[]
        for i in range(steps):
            pred=model(u[:96],coords) if name=='DeepONet' else model(u[:96])
            loss=(pred-y[:96]).square().mean();opt.zero_grad();loss.backward();opt.step()
            if i%25==0 or i==steps-1:
                with torch.no_grad():
                    pv=model(u[96:128],coords) if name=='DeepONet' else model(u[96:128])
                    val=float((pv-y[96:128]).square().mean())
                history.append([i,float(loss.detach()),val])
                if val<best:best=val;state=copy.deepcopy(model.state_dict());best_step=i
        model.load_state_dict(state)
        with torch.no_grad():pred=model(u[128:],coords) if name=='DeepONet' else model(u[128:])
        predictions[name]=pred.numpy();histories[name]=history
        metrics[name]={'test_mse':float((pred-y[128:]).square().mean()),'validation_mse':best,'selected_step':best_step,
                       'parameter_tensor_elements':sum(p.numel() for p in model.parameters()),
                       'real_scalar_degrees_of_freedom':sum(p.numel()*(2 if p.is_complex() else 1) for p in model.parameters())}
    metrics['identity_baseline_test_mse']=float((u[128:]-y[128:]).square().mean())
    metrics['analytic_heat_reference_mse']=0.
    return {'x':x,'input_test':u[128:].numpy(),'target_test':y[128:].numpy(),'predictions':predictions,'histories':histories,
            'metrics':{'data_kind':'manufactured periodic Fourier heat family', 'seed':seed,'steps_per_model':steps,
             'split_functions':{'train':96,'validation':32,'test':32},'grid_points':32,
             'nu':.03,'time':.15,'models':metrics,
             'scope':'Not a benchmark replication, grid-transfer test, climate model, or measured diffusion validation.'}}
