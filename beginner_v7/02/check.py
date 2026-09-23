"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
d=lambda x,y: abs(x-y)
sq=lambda x,y: (x-y)**2
assert d(0,2) <= d(0,1)+d(1,2)
assert sq(0,2) > sq(0,1)+sq(1,2)
print('Squared distance: 4 > 1 + 1, so it is not a metric on R.')
