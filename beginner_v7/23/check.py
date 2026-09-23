"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
m,k,q,v=2.,3.,.3,.4
p=m*v;L=.5*m*v*v-.5*k*q*q;H=p*v-L
assert np.isclose(p,.8) and np.isclose(H,.295)
assert np.isclose(H,p*p/(2*m)+.5*k*q*q)
print('Momentum:',p,'Hamiltonian:',H)
