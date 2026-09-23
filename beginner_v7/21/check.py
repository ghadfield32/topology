"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
t=2.;h=1e-3
estimate=((t+h)**2-(t-h)**2)/(2*h)
assert np.isclose(estimate,4.)
print('Central difference for t² at t=2:',estimate)
