"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from shape_lab.algebra import rank_mod2
A=np.array([[1,1],[1,-1]])
assert np.linalg.matrix_rank(A)==2
assert rank_mod2(A)==1
assert np.all((A @ np.array([1,1])) % 2 == 0)
print('Rank over R: 2; rank over F2: 1.')
