"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
import hashlib
first=b'prediction=4.0\n';changed=b'prediction=5.0\n'
a=hashlib.sha256(first).hexdigest();b=hashlib.sha256(changed).hexdigest()
assert a!=b and a==hashlib.sha256(first).hexdigest()
print('Unchanged bytes match; changed bytes differ. Correctness is a separate question.')
