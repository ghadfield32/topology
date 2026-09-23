"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
nu,t=.1,1.
a1=np.exp(-nu*t);a2=np.exp(-nu*4*t)
assert np.isclose(a2,a1**4)
print('Mode-1 amplitude:',a1,'mode-2 amplitude:',a2)
