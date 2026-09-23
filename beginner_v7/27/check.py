"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from shape_lab.practice_v7 import gradient_inner_product
g=np.array([1.,0.]);other=-g
assert gradient_inner_product(g,other)==-1.
for a in [-2.,-1.,0.,1.,2.]:
    assert not (a>0 and -a>0)
print('Opposite gradients admit no strictly common first-order descent direction.')
