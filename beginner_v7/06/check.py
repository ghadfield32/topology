"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from shape_lab.algebra import closure,boundary_matrix,betti_numbers
outline=closure([(0,1),(1,2),(0,2)]);filled=closure([(0,1,2)])
assert betti_numbers(outline,1)==[1,1]
assert betti_numbers(filled,1)==[1,0]
assert np.all((boundary_matrix(filled,1)@boundary_matrix(filled,2))%2==0)
print('Outline beta=[1,1]; filled beta=[1,0]; boundary of boundary is zero.')
