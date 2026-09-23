"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
x=np.array([0.,1.,2.]);y=2*x+3
A=np.column_stack([x,np.ones(len(x))]);scale,offset=np.linalg.lstsq(A,y,rcond=None)[0]
prediction=scale*3+offset
assert np.allclose([scale,offset],[2,3]) and np.isclose(prediction,9.)
print('Fitted scale/offset:',scale,offset,'held-out prediction:',prediction)
