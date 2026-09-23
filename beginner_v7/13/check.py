"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
u,v=.3,-.4;r2=u*u+v*v
p=np.array([2*u,2*v,r2-1])/(1+r2)
assert np.isclose(p@p,1.)
assert np.allclose(p[:2]/(1-p[2]),[u,v])
print('Sphere point:',p,'round trip:',p[:2]/(1-p[2]))
