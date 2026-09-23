"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
from shape_lab.evidence_v7 import load_snapshot
from shape_lab.practice_v7 import table_dimensions
table, meta = load_snapshot('seeds')
assert table_dimensions(table[meta['features']]) == (210, 7)
assert table.shape == (210, 9)
print('210 observations; 7 selected features; 1 label and 1 source ID excluded.')
