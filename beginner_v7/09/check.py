"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from shape_lab.persistence import persistent_homology,reduce_boundary
F=[((0,),0.),((1,),0.),((0,1),1.)]
bars=persistent_homology(F,max_dim=0)
assert len(bars)==2
assert sorted(b.death for b in bars)==[1.,np.inf]
f,columns,pairs,trace=reduce_boundary(F)
assert len(pairs)==1
print('Finite component death at 1; one surviving component. Pairs:',pairs)
