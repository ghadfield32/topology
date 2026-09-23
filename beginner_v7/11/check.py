"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from shape_lab.practice_v7 import fit_scaler,apply_scaler
center,scale=fit_scaler([[0.],[2.]])
assert np.allclose(apply_scaler([[100.]],center,scale),[[99.]])
print('Training mean 1, scale 1; future value becomes 99.')
