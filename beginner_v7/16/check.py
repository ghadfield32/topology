"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
scores=np.array([0.,0.]);weights=np.exp(scores-scores.max());weights/=weights.sum()
values=np.array([[1.,0.],[0.,2.]])
output=weights@values
assert np.allclose(weights,[.5,.5]) and np.allclose(output,[.5,1.])
print('Weights:',weights,'weighted values:',output)
