"""Exact entry check; not a substitute for a proof or a real-data experiment."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))
empty=frozenset();whole=frozenset({0,1})
discrete={empty,frozenset({0}),frozenset({1}),whole}
coarse={empty,frozenset({1}),whole}
identity_continuous=lambda domain,codomain: all(U in domain for U in codomain)
assert identity_continuous(discrete,coarse)
assert not identity_continuous(coarse,discrete)
print('The identity is a continuous bijection in one direction, not a homeomorphism.')
