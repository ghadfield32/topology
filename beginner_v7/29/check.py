"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
c,t=.3,2.;h=1e-5
f=lambda value:np.exp(-value*t)
analytic=-t*f(c);numeric=(f(c+h)-f(c-h))/(2*h)
assert np.isclose(analytic,numeric,rtol=1e-8)
print('Sensitivity:',analytic,'finite difference:',numeric)
