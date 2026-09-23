"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
from shape_lab.algebra import closure,validate_complex
outline=closure([(0,1),(1,2),(0,2)])
filled=closure([(0,1,2)])
assert len(outline)==6 and len(filled)==7
assert (0,1,2) not in outline and (0,1,2) in filled
try:validate_complex([(0,1,2)])
except ValueError:print('Missing faces rejected as expected.')
else:raise AssertionError('Validator accepted missing faces')
