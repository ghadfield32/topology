"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from shape_lab.persistence import finite_bottleneck
A=np.array([[1.,3.]])
assert np.isclose(finite_bottleneck(A,np.empty((0,2))),1.)
assert np.isclose(finite_bottleneck(A,A+.1),.1)
print('Deletion cost 1.0; matched shift cost 0.1.')
