"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
R=np.array([[0,-1],[1,0]])
F=np.diag([1,-1])
assert np.array_equal(R@R@R@R,np.eye(2))
assert not np.array_equal(R@F,F@R)
print('RF=',R@F,'FR=',F@R)
