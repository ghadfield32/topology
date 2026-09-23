"""Finite simplicial homology over F2. Clear reference code, not a fast engine.

A simplex is a sorted nonempty tuple of distinct integer vertex IDs.
We use ordinary, not reduced, homology. Empty simplex is not stored.
"""
from itertools import combinations
from typing import Iterable
import numpy as np

Simplex = tuple[int, ...]

def canonical(simplex: Iterable[int]) -> Simplex:
    s = tuple(simplex)
    if not s or len(s) != len(set(s)):
        raise ValueError('A simplex needs distinct vertices and cannot be empty.')
    if not all(isinstance(v, (int, np.integer)) for v in s):
        raise ValueError('Vertex IDs must be integers.')
    return tuple(sorted(int(v) for v in s))

def closure(facets: Iterable[Iterable[int]]) -> list[Simplex]:
    """Include every nonempty face of the supplied simplices."""
    result = set()
    for facet in facets:
        s = canonical(facet)
        for size in range(1, len(s) + 1):
            result.update(combinations(s, size))
    return sorted(result, key=lambda s: (len(s), s))

def validate_complex(simplices: Iterable[Iterable[int]]) -> list[Simplex]:
    """Reject missing faces rather than silently repairing user input."""
    original = [canonical(s) for s in simplices]
    if len(original) != len(set(original)):
        raise ValueError('Duplicate simplices are not permitted.')
    present = set(original)
    for s in original:
        if len(s) > 1:
            for face in combinations(s, len(s) - 1):
                if face not in present:
                    raise ValueError(f'Missing face {face} of simplex {s}.')
    return sorted(present, key=lambda s: (len(s), s))

def rank_mod2(matrix: np.ndarray) -> int:
    """Gaussian elimination using XOR; not real-valued numerical rank."""
    a = np.asarray(matrix)
    if a.ndim != 2 or not np.all(np.isfinite(a)) or not np.all(a == np.floor(a)):
        raise ValueError('A finite integer-valued matrix is required.')
    a = (a.astype(np.int64) % 2).astype(np.uint8)
    row = 0
    for col in range(a.shape[1]):
        candidates = np.flatnonzero(a[row:, col])
        if not len(candidates):
            continue
        pivot = row + int(candidates[0])
        a[[row, pivot]] = a[[pivot, row]]
        # Eliminating below the pivot is sufficient for rank.
        for r in np.flatnonzero(a[row + 1:, col]) + row + 1:
            a[r] ^= a[row]
        row += 1
        if row == a.shape[0]:
            break
    return row

def boundary_matrix(simplices: Iterable[Iterable[int]], k: int) -> np.ndarray:
    """Matrix d_k: C_k -> C_(k-1); d_0 has zero rows in ordinary homology."""
    if k < 0:
        raise ValueError('k must be nonnegative.')
    s = validate_complex(simplices)
    columns = [x for x in s if len(x) == k + 1]
    rows = [x for x in s if len(x) == k] if k else []
    a = np.zeros((len(rows), len(columns)), dtype=np.int64)
    row_index = {face: i for i, face in enumerate(rows)}
    if k:
        for j, simplex in enumerate(columns):
            for face in combinations(simplex, k):
                a[row_index[face], j] = 1
    return a

def betti_numbers(simplices: Iterable[Iterable[int]], max_dim: int | None = None) -> list[int]:
    s = validate_complex(simplices)
    actual_dim = max((len(x) - 1 for x in s), default=-1)
    limit = actual_dim if max_dim is None else max_dim
    if limit < -1:
        raise ValueError('max_dim must be nonnegative, or omitted.')
    return [sum(len(x) == k + 1 for x in s)
            - rank_mod2(boundary_matrix(s, k))
            - rank_mod2(boundary_matrix(s, k + 1)) for k in range(limit + 1)]

def euler_characteristic(simplices: Iterable[Iterable[int]]) -> int:
    return sum((-1) ** (len(s) - 1) for s in validate_complex(simplices))
