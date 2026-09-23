"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
R=np.array([[0.,-1,0],[1,0,0],[0,0,1]])
t=np.array([1.,2.,3.]);p=np.array([1.,0.,0.]);q=R@p+t
assert np.allclose(R.T@R,np.eye(3)) and np.isclose(np.linalg.det(R),1.)
assert np.allclose(q,[1,3,3]) and np.allclose(R.T@(q-t),p)
print('Forward:',q,'inverse:',R.T@(q-t))
