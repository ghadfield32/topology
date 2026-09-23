"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from shape_lab.practice_v7 import symplectic_defect,oscillator_energy
h=.2;A=np.array([[1-h*h,h],[-h,1.]])
assert symplectic_defect(A)<1e-14
assert np.isclose(oscillator_energy(A@np.array([1.,0.])),.4808)
print('Symplectic condition passes; exact-energy condition does not.')
