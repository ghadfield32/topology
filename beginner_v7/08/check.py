"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from shape_lab.persistence import rips_filtration,persistent_homology,diagram
X=np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]])
D=diagram(persistent_homology(rips_filtration(X,max_homology=1)),1,finite_only=True)
assert D.shape==(1,2) and np.allclose(D[0],[1,np.sqrt(2)])
print('Finite H1 interval:',D[0])
