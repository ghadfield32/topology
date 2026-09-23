"""Small transparent evidence checks for teaching; not deployment certification.

No function downloads data. Source tables, preprocessing choices and evaluation
units remain explicit. Conformal guarantees require exchangeable scores and a
fixed fitted predictor; this module cannot establish those assumptions.
"""
from __future__ import annotations
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from itertools import combinations
from pathlib import Path
import hashlib
import json
import numbers
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
IDS = ('seeds', 'concrete_slump')

def canonical_numeric(rows) -> bytes:
    """Ordered rectangular numeric table, insensitive only to decimal formatting.

    Keeps row/column order and precision. The result does not include a header;
    schema semantics must be verified separately. Rejects nonfinite values.
    """
    rows = list(rows)
    if not rows or not hasattr(rows[0], '__len__') or len(rows[0]) == 0:
        raise ValueError('A nonempty rectangular numeric table is required')
    width = len(rows[0]); lines = []
    for row in rows:
        if not hasattr(row, '__len__') or len(row) != width:
            raise ValueError('Ragged table')
        values = []
        for token in row:
            try:
                value = Decimal(str(token))
            except (InvalidOperation, ValueError) as exc:
                raise ValueError(f'Not a decimal number: {token!r}') from exc
            if not value.is_finite():
                raise ValueError('Source values must be finite')
            text = format(value, 'f')
            if '.' in text: text = text.rstrip('0').rstrip('.')
            values.append('0' if value == 0 else text)
        lines.append(','.join(values))
    return ('\n'.join(lines) + '\n').encode('ascii')

def numeric_digest(rows) -> str:
    """SHA-256 of canonical ordered numeric values, not of provider binary bytes."""
    return hashlib.sha256(canonical_numeric(rows)).hexdigest()

def conformal_rank(n: int, alpha: float = .1) -> int:
    """One-based ceil((n+1)*(1-alpha)); n+1 denotes an infinite radius.

    Decimal arithmetic avoids an accidental upward rank jump from a floating
    representation of a nominal decimal alpha. Alpha's string is the contract.
    """
    if isinstance(n, bool) or not isinstance(n, numbers.Integral) or n < 1:
        raise ValueError('n must be a positive integer')
    try:
        a = Decimal(str(alpha))
    except InvalidOperation as exc:
        raise ValueError('alpha must lie strictly between zero and one') from exc
    if not a.is_finite() or not 0 < a < 1:
        raise ValueError('alpha must lie strictly between zero and one')
    return int(((int(n)+1)*(1-a)).to_integral_value(rounding=ROUND_CEILING))

def conformal_radius(scores, alpha: float = .1) -> float:
    """Calibrate symmetric absolute-error intervals without interpolating ranks."""
    s = np.asarray(scores, dtype=float)
    if s.ndim != 1 or len(s) == 0 or not np.isfinite(s).all() or np.any(s < 0):
        raise ValueError('Nonempty finite nonnegative one-dimensional scores required')
    k = conformal_rank(len(s), alpha)
    return float('inf') if k > len(s) else float(np.sort(s)[k-1])

def coverage(y, prediction, radius: float) -> float:
    """Observed fraction in closed symmetric intervals; not a future guarantee."""
    y = np.asarray(y, dtype=float); p = np.asarray(prediction, dtype=float)
    if y.ndim != 1 or p.shape != y.shape or not len(y) or not np.isfinite(y).all() or not np.isfinite(p).all():
        raise ValueError('Equal-length nonempty finite vectors required')
    r = float(radius)
    if np.isnan(r) or r < 0:
        raise ValueError('A nonnegative radius is required; positive infinity is allowed')
    return float(np.mean(np.abs(y-p) <= r))

def overlap_report(partitions: dict, units) -> dict:
    """Audit row and independent-unit overlaps separately; do not repair them.

    Units are identifiers, not evidence that the experiment actually sampled
    independently. Missing unit IDs are rejected. All partition rows must exist.
    """
    u = np.asarray(units, dtype=object)
    if u.ndim != 1 or len(u) == 0 or pd.isna(u).any():
        raise ValueError('Nonempty one-dimensional nonmissing unit IDs required')
    if len(partitions) < 2:
        raise ValueError('At least two partitions are required')
    indices = {}; unitsets = {}
    for name, rows in partitions.items():
        a = np.asarray(rows)
        if a.ndim != 1 or not len(a) or not np.issubdtype(a.dtype,np.integer):
            raise ValueError('Nonempty integer row-index arrays required')
        if min(a) < 0 or max(a) >= len(u) or len(np.unique(a)) != len(a):
            raise ValueError('Out-of-range or repeated partition rows')
        indices[name] = set(map(int,a))
        # Type names prevent integer 1 from colliding with the string "1".
        unitsets[name] = {(type(v).__name__,str(v)) for v in u[a]}
    pairs = {}
    for a,b in combinations(partitions,2):
        shared = unitsets[a] & unitsets[b]
        pairs[f'{a}|{b}'] = {'shared_rows':sorted(indices[a]&indices[b]),
                            'shared_units':[v for _,v in sorted(shared)]}
    return {'row_disjoint':all(not p['shared_rows'] for p in pairs.values()),
            'unit_disjoint':all(not p['shared_units'] for p in pairs.values()),
            'partition_sizes':{k:len(v) for k,v in indices.items()},'pairs':pairs}

def load_snapshot(name: str) -> tuple[pd.DataFrame,dict]:
    """Load and validate a named, immutable teaching snapshot."""
    if name not in IDS:
        raise ValueError(f'Choose a dataset from {IDS}; no synthetic fallback exists')
    folder = ROOT/'data/v7'/name
    meta = json.loads((folder/'metadata.json').read_text())
    for relative, digest in meta['files_sha256'].items():
        path = (ROOT/relative).resolve()
        if not path.is_relative_to(ROOT.resolve()):
            raise ValueError('Manifest path escapes this package')
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f'Changed dataset file: {relative}')
    table = pd.read_csv(folder/'table.csv')
    if table.columns.tolist() != meta['columns'] or len(table) != meta['rows']:
        raise ValueError('Snapshot row count or schema differs from its contract')
    if not np.isfinite(table.to_numpy(dtype=float)).all():
        raise ValueError('Unexpected missing or nonfinite source data')
    return table, meta
