"""Portable observed-trajectory contract, not a dump of a C struct.

Header: 8-byte SHPTRJ01, little-endian uint32 count.
Record: uint32 frame, uint32 flags, then five binary64 values (t,x,y,z,confidence).
Coordinates are metres. flags=0 means confidence unknown and stored value must be 0;
flags=1 means the confidence value is present in [0,1]. No source confidence is invented.
"""
from __future__ import annotations
from pathlib import Path
import hashlib, json, math, struct
MAGIC=b'SHPTRJ01'
HEADER=struct.Struct('<8sI')
RECORD=struct.Struct('<IIddddd')
MAX_ROWS=1_000_000

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def _number(x):
    return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)

def validate_rows(rows):
    if not isinstance(rows,list) or not 1<=len(rows)<=MAX_ROWS:raise ValueError('Invalid record count')
    previous_frame=-1; previous_t=-math.inf
    for r in rows:
        if not isinstance(r,dict):raise ValueError('Record must be an object')
        frame=r.get('frame');t=r.get('time')
        if type(frame) is not int or not 0<=frame<=0xffffffff or frame<=previous_frame:raise ValueError('Frames must be increasing uint32 IDs')
        if not _number(t) or t<0 or t<=previous_t:raise ValueError('Time must be finite, nonnegative, increasing')
        if any(not _number(r.get(k)) for k in ('x','y','z')):raise ValueError('Nonfinite/missing position')
        c=r.get('confidence')
        if c is not None and (not _number(c) or not 0<=c<=1):raise ValueError('Invalid confidence')
        previous_frame,previous_t=frame,t

def write_binary(path,rows):
    validate_rows(rows)
    data=bytearray(HEADER.pack(MAGIC,len(rows)))
    for r in rows:
        c=r.get('confidence')
        data.extend(RECORD.pack(r['frame'],int(c is not None),r['time'],r['x'],r['y'],r['z'],0. if c is None else c))
    with Path(path).open('xb') as f:f.write(data)

def read_binary(path):
    p=Path(path);size=p.stat().st_size
    if size<HEADER.size or size>HEADER.size+MAX_ROWS*RECORD.size:raise ValueError('Invalid byte count')
    with p.open('rb') as f:
        magic,n=HEADER.unpack(f.read(HEADER.size))
        if magic!=MAGIC or not 1<=n<=MAX_ROWS or size!=HEADER.size+n*RECORD.size:raise ValueError('Header/count/size mismatch')
        rows=[]
        for _ in range(n):
            frame,flag,t,x,y,z,c=RECORD.unpack(f.read(RECORD.size))
            if flag not in (0,1) or (flag==0 and c!=0) or not math.isfinite(c):raise ValueError('Invalid confidence flag')
            rows.append(dict(frame=frame,time=t,x=x,y=y,z=z,confidence=c if flag else None))
    validate_rows(rows);return rows

def export_spl(repo):
    repo=Path(repo);rel='sports_v8/data/spl_selected_frames.json';p=repo/rel
    registry=json.loads((repo/'native/data_registry.json').read_text())['files']
    expected=next(r['sha256'] for r in registry if r['path']==rel)
    if sha256(p)!=expected:raise ValueError('Registered SPL excerpt changed')
    raw=json.loads(p.read_text(encoding='utf8'));fps=raw['sampling_rate']
    if raw['xyz_unit']!='ft' or not _number(fps) or fps<=0:raise ValueError('Unsupported units/clock')
    rows=[]
    for r in raw['records']:
        if len(r['ball'])!=3:raise ValueError('Expected 3D ball coordinates')
        x,y,z=(float(v)*.3048 for v in r['ball'])
        rows.append(dict(frame=r['frame'],time=r['frame']/fps,x=x,y=y,z=z,confidence=None))
    validate_rows(rows)
    return rows,dict(path=rel,sha256=expected,participant=raw['participant_id'],trial=raw['trial_id'],
        position_status='derived_unit_conversion_of_selected_source_tracking',
        time_status='ideal frame/sample-rate clock; not synchronized camera PTS',
        confidence_status='not supplied; preserved unknown',independent_trials=1)

def predict(position,velocity,dt,gravity=9.81):
    if len(position)!=3 or len(velocity)!=3 or not all(_number(x) for x in [*position,*velocity,dt,gravity]) or dt<0 or gravity<=0:
        raise ValueError('Finite 3D states, nonnegative dt and positive gravity required')
    out=[position[0]+velocity[0]*dt,position[1]+velocity[1]*dt,position[2]+velocity[2]*dt-.5*gravity*dt*dt]
    if not all(_number(v)for v in out):raise ValueError('Prediction overflow')
    return out

def validate_payload(v):
    if not isinstance(v,dict) or v.get('schema')!='shape.systems.trajectory.v1' or v.get('units')!='m':raise ValueError('Wrong schema/units')
    for name in ('observed','predicted'):
        rows=v.get(name)
        if not isinstance(rows,list) or not rows or len(rows)>MAX_ROWS:raise ValueError('Missing trajectory')
        last=-math.inf
        for p in rows:
            if not isinstance(p,dict) or any(not _number(p.get(k)) for k in ('time','x','y','z')):raise ValueError('Invalid point')
            if p['time']<=last:raise ValueError('Unordered trajectory')
            c=p.get('confidence')
            if c is not None and (not _number(c)or not 0<=c<=1):raise ValueError('Invalid confidence')
            last=p['time']
    if not isinstance(v.get('metadata'),dict) or not isinstance(v['metadata'].get('limitations'),list) or not all(isinstance(x,str)for x in v['metadata']['limitations']):raise ValueError('Missing limitations')
    return v
