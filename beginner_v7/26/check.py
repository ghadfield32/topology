"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
u=lambda x:x*(1-x)
v=lambda x:u(x)+5
h=1e-3;x=.4
second=lambda f:(f(x+h)-2*f(x)+f(x-h))/h**2
assert np.isclose(-second(u),2.,atol=1e-6)
assert np.isclose(-second(v),2.,atol=1e-6)
assert u(0)==0 and v(0)==5
print('Same interior equation; different boundary values.')
