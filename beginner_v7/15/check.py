"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
f,B,d,offset=1000.,.1,20.,5.
Z=lambda disparity: f*B/(disparity+offset)
sensitivity=-f*B/(d+offset)**2
h=1e-4;finite_difference=(Z(d+h)-Z(d-h))/(2*h)
assert np.isclose(Z(d),4.) and np.isclose(sensitivity,-.16)
assert np.isclose(sensitivity,finite_difference)
print('Depth:',Z(d),'local metres/pixel:',sensitivity)
