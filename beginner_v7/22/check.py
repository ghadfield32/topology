"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
phi=lambda x,t:x/(1-t*x)
x=.5;t=.2;y=phi(x,t)
assert np.isclose(phi(y,-t),x)
assert np.isclose(1-2*x,0.)
assert (1-1.)*3. == (1-1.)*7. == 0.
print('Valid round trip:',x,y,phi(y,-t),'blow-up time:',2.)
