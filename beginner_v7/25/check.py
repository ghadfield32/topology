"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from shape_lab.practice_v7 import sphere_newton_step
x=sphere_newton_step([2.,0.]);residual=x@x-1
assert np.allclose(x,[1.25,0.]) and np.isclose(residual,.5625)
print('One linearized correction:',x,'remaining residual:',residual)
