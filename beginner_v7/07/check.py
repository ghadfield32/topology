"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
side=1.;radius=.5;circumradius=side/np.sqrt(3)
assert 2*radius>=side
assert radius<circumradius
print('Pairwise touching radius:',radius,'common-intersection threshold:',circumradius)
