"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
distances=[.2,.08,.07,.06];dt=.02
run=0;confirmed=None;onset=None
for i,d in enumerate(distances):
    run=run+1 if d<.1 else 0
    if run==3:
        confirmed=i;onset=i-2;break
assert onset==1 and confirmed==3
assert abs((confirmed-onset)*dt-.04)<1e-12
print('Candidate onset:',onset,'confirmation:',confirmed,'delay:',.04)
