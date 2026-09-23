"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
from shape_lab.evidence_v7 import overlap_report
report=overlap_report({'train':[0,2],'test':[1,3]},['A','A','B','B'])
assert report['row_disjoint'] and not report['unit_disjoint']
print(report)
