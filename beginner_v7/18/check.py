"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import numpy as np
arrivals=np.arange(8)*.033;finish=0.;ages=[]
for arrival in arrivals:
    finish=max(finish,float(arrival))+.06
    ages.append(finish-arrival)
assert ages[-1]>ages[0]
print('Simulated result ages (seconds):',ages)
