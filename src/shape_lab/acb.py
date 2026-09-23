"""Small verified catalog and explicit basketball identity/grain calculations.

Only load_matches uses real provider records. Other functions are general
contract operations, exercised on labeled constructed controls in the lesson.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime
from collections.abc import Mapping, Sequence
import hashlib
import json
import math

def load_matches(directory: Path) -> list[dict]:
    """Verify the bytes before reading the complete ten-game metadata catalog."""
    directory=Path(directory)
    raw=(directory/'matches.json').read_bytes()
    meta=json.loads((directory/'provenance.json').read_text())
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if blob!=meta['source_blob_sha1'] or hashlib.sha256(raw).hexdigest()!=meta['local_sha256']:
        raise ValueError('Source hash mismatch: do not use changed metadata as the verified snapshot.')
    rows=json.loads(raw)
    if len(rows)!=meta['rows'] or len({r['id'] for r in rows})!=len(rows):
        raise ValueError('Row count or game identity mismatch.')
    for r in rows:
        when=datetime.fromisoformat(r['date_time'].replace('Z','+00:00'))
        if when.tzinfo is None:raise ValueError('Scheduled tip-off must be timezone aware.')
        if r['home_team']['id']==r['away_team']['id']:raise ValueError('A team cannot be both opponents.')
        if any(type(r[k]) is not int or r[k]<0 for k in ('home_score','away_score')):
            raise ValueError('Final scores must be nonnegative integers.')
    return rows

def chronological_split(rows: Sequence[Mapping], n_fit: int=6, n_validation: int=2) -> dict[int,str]:
    """Assign games once, not frames; held-out teams may still recur."""
    if type(n_fit) is not int or type(n_validation) is not int or min(n_fit,n_validation)<1:
        raise ValueError('Fit and validation sizes must be positive integers.')
    if len(rows)<=n_fit+n_validation:raise ValueError('At least one game must remain for testing.')
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('Duplicate game IDs.')
    dated=[]
    for r in rows:
        t=datetime.fromisoformat(str(r['date_time']).replace('Z','+00:00'))
        if t.tzinfo is None:raise ValueError('Timezone is required.')
        dated.append((t,r['id']))
    dated.sort()
    # Tied start times cannot be split between partitions without an explicit policy.
    for boundary in (n_fit,n_fit+n_validation):
        if dated[boundary-1][0]==dated[boundary][0]:raise ValueError('Tied timestamps at split boundary.')
    return {id:('fit' if j<n_fit else 'validation' if j<n_fit+n_validation else 'test')
            for j,(_,id) in enumerate(dated)}

def canonical_id(value: int, aliases: Mapping[int,int]) -> int:
    """Resolve an explicit provider alias chain; never infer identity from names."""
    seen=set()
    while value in aliases:
        if value in seen:raise ValueError('Alias cycle; fix the identity mapping first.')
        seen.add(value)
        nxt=aliases[value]
        if nxt==value:return value
        value=nxt
    return value

def team_only_total(rows: Sequence[Mapping], field: str) -> float:
    """Sum team rows, excluding provider season-total rows; counts only, not rates."""
    values=[]
    for r in rows:
        if str(r['team_name']).strip().casefold()=='total':continue
        value=float(r[field])
        if not math.isfinite(value) or value<0:raise ValueError('Counts must be finite and nonnegative.')
        values.append(value)
    return math.fsum(values)
