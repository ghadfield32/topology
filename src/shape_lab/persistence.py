"""Small, explicit persistent-homology reference implementation.

F2 coefficients; ordinary homology; half-open intervals [birth, death).
Rips scale is maximum pairwise edge length, NOT ball radius.
This intentionally enumerates simplices and is for small educational examples.
"""
from dataclasses import dataclass
from itertools import combinations
from math import comb
from typing import Iterable
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching
from .algebra import Simplex, canonical

Filtration = list[tuple[Simplex, float]]

@dataclass(frozen=True)
class Interval:
    dim: int
    birth: float
    death: float
    birth_simplex: Simplex
    death_simplex: Simplex | None

    @property
    def lifetime(self) -> float:
        return self.death - self.birth


def ordered_filtration(entries: Iterable[tuple[Iterable[int], float]]) -> Filtration:
    """Validate faces, times and uniqueness; impose deterministic tie ordering."""
    values = {}
    for simplex, value in entries:
        s = canonical(simplex)
        v = float(value)
        if not np.isfinite(v):
            raise ValueError('Simplex filtration values must be finite.')
        if s in values:
            raise ValueError(f'Duplicate simplex {s}.')
        values[s] = v
    for s, value in values.items():
        if len(s) > 1:
            for face in combinations(s, len(s) - 1):
                if face not in values:
                    raise ValueError(f'Missing face {face} of {s}.')
                if values[face] > value:
                    raise ValueError('A face cannot appear after its coface.')
    return sorted(values.items(), key=lambda item: (item[1], len(item[0]), item[0]))


def rips_filtration(points: np.ndarray, max_homology: int = 1,
                    max_edge: float = np.inf) -> Filtration:
    """Build through dimension max_homology+1 to allow deaths in reported Hk.

    Duplicate coordinate rows remain distinct labeled observations; their mutual
    dissimilarity is zero. This is a pseudometric on observation IDs. Their
    zero-length merge bars are excluded by the default reporting policy.
    """
    x = np.asarray(points, dtype=float)
    if x.ndim != 2 or not len(x) or not np.isfinite(x).all():
        raise ValueError('Provide a nonempty finite 2D array of points.')
    if max_homology not in (0, 1, 2) or max_edge < 0 or np.isnan(max_edge):
        raise ValueError('Use max_homology 0, 1 or 2 and nonnegative max_edge.')
    largest_size = max_homology + 2
    possible = sum(comb(len(x), size) for size in range(1, min(largest_size, len(x)) + 1))
    if possible > 250_000:
        raise ValueError('Educational enumerator would exceed 250000 candidate simplices. Use fewer points or a production library.')
    d = squareform(pdist(x))
    result = [((i,), 0.) for i in range(len(x))]
    for size in range(2, min(largest_size, len(x)) + 1):
        for s in combinations(range(len(x)), size):
            value = max(d[i, j] for i, j in combinations(s, 2))
            if value <= max_edge:
                result.append((s, float(value)))
    return ordered_filtration(result)


def reduce_boundary(entries: Filtration):
    """Reduce sparse boundary columns by XOR, retaining pivot and operation logs.

    R[j] is the current boundary-column support. low_to_column stores one owner
    of each largest nonzero row. Adding equal-pivot columns cancels that row.
    """
    f = ordered_filtration(entries)
    index = {s: i for i, (s, _) in enumerate(f)}
    reduced: list[set[int]] = []
    low_to_column: dict[int, int] = {}
    operations: list[tuple[int, int]] = []
    for j, (simplex, _) in enumerate(f):
        column = {index[face] for face in combinations(simplex, len(simplex) - 1)} if len(simplex) > 1 else set()
        while column and max(column) in low_to_column:
            owner = low_to_column[max(column)]
            column ^= reduced[owner]
            operations.append((j, owner))
        if column:
            low_to_column[max(column)] = j
        reduced.append(column)
    return f, reduced, low_to_column, operations


def persistent_homology(entries: Filtration, max_dim: int = 1,
                        include_zero: bool = False) -> list[Interval]:
    """Return intervals for the supplied filtration, not an imagined continuation.

    An infinite death can mean surviving the supplied truncation. Callers must
    report the largest computed scale and maximal simplex dimension.
    """
    if max_dim < 0:
        raise ValueError('max_dim must be nonnegative.')
    f, reduced, pairs, _ = reduce_boundary(entries)
    intervals = []
    for birth, col in enumerate(reduced):
        if col:
            continue
        simplex, b = f[birth]
        dim = len(simplex) - 1
        if dim > max_dim:
            continue
        death = pairs.get(birth)
        d = f[death][1] if death is not None else np.inf
        if include_zero or d > b:
            intervals.append(Interval(dim, b, d, simplex, f[death][0] if death is not None else None))
    return sorted(intervals, key=lambda x: (x.dim, x.birth, x.death, x.birth_simplex))


def diagram(intervals: list[Interval], dim: int, finite_only: bool = False) -> np.ndarray:
    return np.array([(b.birth, b.death) for b in intervals if b.dim == dim
                     and (not finite_only or np.isfinite(b.death))], dtype=float).reshape(-1, 2)


def finite_bottleneck(a, b) -> float:
    """Exact finite-diagram bottleneck by threshold perfect matching, with diagonal.

    Essential intervals are rejected, not silently removed. Empty diagrams and
    multiplicities are supported. Intended only for small diagrams.
    """
    a = np.asarray(a, dtype=float).reshape(-1, 2)
    b = np.asarray(b, dtype=float).reshape(-1, 2)
    for x in (a, b):
        if not np.isfinite(x).all() or np.any(x[:, 1] < x[:, 0]):
            raise ValueError('Only finite birth <= death pairs are supported.')
    m, n = len(a), len(b)
    if m + n == 0:
        return 0.
    costs = np.full((m + n, m + n), np.inf)
    if m and n:
        costs[:m, :n] = np.max(abs(a[:, None, :] - b[None, :, :]), axis=2)
    for i in range(m):
        costs[i, n + i] = (a[i, 1] - a[i, 0]) / 2
    for j in range(n):
        costs[m + j, j] = (b[j, 1] - b[j, 0]) / 2
    costs[m:, n:] = 0.
    candidates = np.unique(costs[np.isfinite(costs)])
    lo, hi = 0, len(candidates) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        graph = csr_matrix(costs <= candidates[mid])
        matching = maximum_bipartite_matching(graph, perm_type='column')
        if np.all(matching >= 0):
            hi = mid
        else:
            lo = mid + 1
    return float(candidates[lo])


def pixel_filtration(values: np.ndarray) -> Filtration:
    """Triangulate CLOSED square pixels, preserving their sublevel-set filtration.

    A pixel with value v enters at v. Both triangles enter at v; every face gets
    the minimum value of incident triangles. This is a filtration-preserving
    triangulation of the union of closed square cells. Corner-touching pixels
    are connected. No padded exterior or periodic boundary is assumed.
    """
    a = np.asarray(values, dtype=float)
    if a.ndim != 2 or not a.size or not np.isfinite(a).all():
        raise ValueError('A nonempty finite 2D array of pixel values is required.')
    rows, cols = a.shape
    values_by_simplex = {}
    def vertex(r, c):
        return r * (cols + 1) + c
    for r in range(rows):
        for c in range(cols):
            nw, ne = vertex(r, c), vertex(r, c + 1)
            sw, se = vertex(r + 1, c), vertex(r + 1, c + 1)
            for triangle in ((nw, ne, se), (nw, sw, se)):
                for size in (1, 2, 3):
                    for face in combinations(sorted(triangle), size):
                        values_by_simplex[face] = min(values_by_simplex.get(face, np.inf), float(a[r, c]))
    return ordered_filtration(values_by_simplex.items())
