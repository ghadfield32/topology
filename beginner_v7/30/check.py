"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from shape_lab.evidence_v7 import conformal_rank,conformal_radius
assert conformal_rank(9,.01)==10
assert np.isinf(conformal_radius(np.arange(1,10),.01))
print('The requested extreme coverage is uninformative at this calibration size under the stated rule.')
