"""Thirty fully worked coding answers. Attempt learner notebooks first."""
import numpy as np

def centered_rate(f, x, h):
    if not np.isfinite(h) or h<=0: raise ValueError('Positive finite spacing required.')
    return (f(x+h)-f(x-h))/(2*h)

def spring_rhs(z, mass, stiffness):
    z=np.asarray(z,dtype=float)
    if z.shape!=(2,) or not np.isfinite(z).all() or not np.isfinite(mass) or mass<=0 or not np.isfinite(stiffness) or stiffness<0: raise ValueError('Invalid spring state or parameters.')
    return np.array([z[1]/mass,-stiffness*z[0]])

def measured_secant(x0, y0, x1, y1):
    a=np.asarray([x0,y0,x1,y1],dtype=float)
    if not np.isfinite(a).all() or x0==x1: raise ValueError('Finite observations with distinct inputs required.')
    return (y1-y0)/(x1-x0)

def local_quadratic_flow(x, t):
    x=np.asarray(x,dtype=float)
    if not np.isfinite(x).all() or not np.isfinite(t) or np.any(1-t*x<=0):raise ValueError('Outside local flow domain.')
    return x/(1-t*x)

def invert_coupling(Y):
    Y=np.asarray(Y,dtype=float)
    if Y.ndim!=2 or Y.shape[1]!=2 or not np.isfinite(Y).all():raise ValueError('N by 2 finite input required.')
    x=Y[:,0]
    return np.column_stack([x,(Y[:,1]-.5*np.sin(x))*np.exp(-.2*np.tanh(x))])

def coupling_log_density(log_px, x):
    return np.asarray(log_px)-.2*np.tanh(np.asarray(x))

def canonical_momentum(mass, velocity):
    if not np.isfinite(mass) or mass<=0:raise ValueError('Positive mass required.')
    v=np.asarray(velocity,dtype=float)
    if not np.isfinite(v).all():raise ValueError('Finite velocity required.')
    return mass*v

def hamiltonian_from_lagrangian(q, p, mass, stiffness):
    if not np.isfinite([q,p,mass,stiffness]).all() or mass<=0 or stiffness<0:raise ValueError('Invalid inputs.')
    return p*p/(2*mass)+stiffness*q*q/2

def regular_lagrangian_acceleration(L_q, L_vq, L_vv, velocity):
    if not np.isfinite([L_q,L_vq,L_vv,velocity]).all() or abs(L_vv)<1e-12:raise ValueError('Regular finite scalar Lagrangian required.')
    return (L_q-L_vq*velocity)/L_vv

def kick_drift(z, h):
    q,p=np.asarray(z,dtype=float)
    pn=p-h*q
    return np.array([q+h*pn,pn])

def unit_energy(z):
    z=np.asarray(z,dtype=float)
    if z.ndim<1 or z.shape[-1]!=2 or not np.isfinite(z).all():raise ValueError('Finite (...,2) state required.')
    return .5*np.sum(z*z,axis=-1)

def linear_symplectic_error(M):
    M=np.asarray(M,dtype=float)
    if M.ndim!=2 or M.shape[0]!=M.shape[1] or M.shape[0]%2 or not np.isfinite(M).all():raise ValueError('Even finite square map required.')
    d=M.shape[0]//2;I=np.eye(d);Z=np.zeros((d,d));J=np.block([[Z,I],[-I,Z]])
    return np.linalg.norm(M.T@J@M-J)

def affine_correction(z, A, b):
    z=np.asarray(z,dtype=float);A=np.asarray(A,dtype=float);b=np.asarray(b,dtype=float)
    if A.ndim!=2 or z.ndim!=1 or A.shape!=(len(b),len(z)) or np.linalg.matrix_rank(A)<len(b):raise ValueError('Full row rank and compatible dimensions required.')
    return z-A.T@np.linalg.solve(A@A.T,A@z-b)

def circle_newton_step(z):
    z=np.asarray(z,dtype=float);r=z@z
    if z.shape!=(2,) or not np.isfinite(r) or r==0:raise ValueError('Nonzero finite two-vector required.')
    return z-z*(r-1)/(2*r)

def tangent_component(q, v):
    q=np.asarray(q,dtype=float);v=np.asarray(v,dtype=float)
    if q.shape!=v.shape or q.ndim!=1 or not np.isclose(q@q,1):raise ValueError('Unit point and matching vector required.')
    return v-q*(q@v)

def poisson_residual(u_xx, x):
    return -np.asarray(u_xx)-np.pi**2*np.sin(np.pi*np.asarray(x))

def hard_zero_ansatz(x, network_values):
    x=np.asarray(x,dtype=float);v=np.asarray(network_values,dtype=float)
    if x.shape!=v.shape or not np.isfinite(v).all():raise ValueError('Matching finite arrays required.')
    return x*(1-x)*v

def relative_error(prediction, reference):
    p=np.asarray(prediction,dtype=float);r=np.asarray(reference,dtype=float)
    if p.shape!=r.shape or not np.isfinite(p).all() or not np.isfinite(r).all() or np.linalg.norm(r)==0:raise ValueError('Matching finite arrays and nonzero reference required.')
    return np.linalg.norm(p-r)/np.linalg.norm(r)

def project_conflict(g_i, g_j):
    a=np.asarray(g_i,dtype=float).copy();b=np.asarray(g_j,dtype=float)
    if a.shape!=b.shape or a.ndim!=1 or not np.isfinite(a).all() or not np.isfinite(b).all():raise ValueError('Matching finite vectors required.')
    denom=b@b;dot=a@b
    return a-dot/denom*b if denom>0 and dot<0 else a

def normalised_projected_sum(rows):
    P=np.asarray(rows,dtype=float)
    if P.ndim!=2 or not np.isfinite(P).all():raise ValueError('Finite matrix required.')
    norm=np.linalg.norm(P,axis=1)
    return np.divide(P,norm[:,None],out=np.zeros_like(P),where=norm[:,None]>1e-14).sum(axis=0)

def linear_mse_gradient(X, y, theta):
    X=np.asarray(X,dtype=float);y=np.asarray(y,dtype=float);theta=np.asarray(theta,dtype=float)
    if X.ndim!=2 or len(X)==0 or X.shape!=(len(y),len(theta)):raise ValueError('Compatible nonempty regression arrays required.')
    return 2*X.T@(X@theta-y)/len(X)

def heat_multipliers(k, nu, time, length=1.):
    if not np.isfinite([nu,time,length]).all() or nu<0 or time<0 or length<=0:raise ValueError('Invalid heat parameters.')
    k=np.asarray(k,dtype=float)
    return np.exp(-nu*(2*np.pi*k/length)**2*time)

def branch_trunk_product(branch, trunk):
    b=np.asarray(branch);t=np.asarray(trunk)
    if b.ndim!=2 or t.ndim!=2 or b.shape[1]!=t.shape[1]:raise ValueError('Shared feature dimension required.')
    return b@t.T

def disjoint_function_splits(train_ids, validation_ids, test_ids):
    groups=[list(train_ids),list(validation_ids),list(test_ids)]
    sets=[set(x) for x in groups]
    return all(len(s)==len(g)>0 for s,g in zip(sets,groups)) and not any(sets[i]&sets[j] for i in range(3) for j in range(i))

def balanced_pair_update(nodes, i, j, message):
    a=np.asarray(nodes,dtype=float).copy();v=np.asarray(message,dtype=float)
    if not 0<=i<len(a) or not 0<=j<len(a) or i==j or a.shape[1:]!=v.shape:raise ValueError('Valid endpoints and message shape required.')
    a[i]+=v;a[j]-=v
    return a

def attention_invariants(A):
    A=np.asarray(A,dtype=float)
    if A.ndim!=2 or A.shape[0]!=A.shape[1] or not np.isfinite(A).all():raise ValueError('Finite square matrix required.')
    return {'constant':bool(np.allclose(A.sum(axis=1),1)), 'total':bool(np.allclose(A.sum(axis=0),1))}

def sensitivity_check(f, parameter, epsilon):
    if not np.isfinite(epsilon) or epsilon<=0:raise ValueError('Positive finite epsilon required.')
    return (f(parameter+epsilon)-f(parameter-epsilon))/(2*epsilon)

def evidence_digest(path):
    from hashlib import sha256
    from pathlib import Path
    return sha256(Path(path).read_bytes()).hexdigest()

def heldout_mae(prediction, reference):
    p=np.asarray(prediction,dtype=float);r=np.asarray(reference,dtype=float)
    if p.shape!=r.shape or p.size==0 or not np.isfinite(p).all() or not np.isfinite(r).all():raise ValueError('Matching finite nonempty arrays required.')
    return float(np.mean(np.abs(p-r)))

def first_unfinished(stage_statuses):
    for key in sorted(stage_statuses,key=int):
     if stage_statuses[key] not in {'demonstrated','retained'}:return int(key)
    return None
