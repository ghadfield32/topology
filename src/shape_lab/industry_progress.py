"""Separate, self-reported eight-case learning log; core stage history is untouched.

Single writer. No automatic grading, networking, reminders, or synchronization.
The familiar assessment policy is reused from the core course, not a new claim
that scores or hashes establish mathematical correctness.
"""
from __future__ import annotations
from datetime import date
from hashlib import sha256
from pathlib import Path
import json, math
from .industries import IDS
from . import learning


def new_log() -> dict:
    return {'schema_version':6,'track':'industry','scope':'Self-reported evidence, not automated grading.',
            'cases':{k:{'attempts':[]} for k in IDS}}


def _view(log:dict, case:str)->dict:
    if case not in IDS or case not in log.get('cases',{}):
        raise ValueError('Unknown industry case.')
    return {'stages':{'00':log['cases'][case]}}


def status(log:dict,case:str)->str:
    return learning.stage_status(_view(log,case),0)


def next_review(log:dict,case:str)->date|None:
    return learning.next_review(_view(log,case),0)


def record(log:dict,case:str,kind:str,score:float,evidence:str,root:Path,day:date,
           independent:bool=False,critical_clear:bool=False,note:str='')->None:
    learning.record(_view(log,case),0,kind,score,evidence,root,day,independent,critical_clear,note)


def read_log(path:Path)->dict:
    log=json.loads(Path(path).read_text())
    if log.get('schema_version')!=6 or log.get('track')!='industry' or set(log.get('cases',{}))!=set(IDS):
        raise ValueError('Expected the eight-case v6 industry log; core logs are separate.')
    for case in IDS:
        attempts=log['cases'][case].get('attempts')
        if not isinstance(attempts,list):raise ValueError('Attempt history must be a list.')
        previous=date.min
        for a in attempts:
            try:
                when=date.fromisoformat(a['date']);digest=a['evidence_sha256']
                valid=(a['kind'] in learning.KINDS and math.isfinite(a['score']) and 0<=a['score']<=100
                       and isinstance(a['independent'],bool) and isinstance(a['critical_clear'],bool)
                       and isinstance(a['evidence'],str) and isinstance(digest,str) and len(digest)==64
                       and all(c in '0123456789abcdef' for c in digest))
            except (KeyError,TypeError,ValueError) as exc:raise ValueError('Malformed industry attempt.') from exc
            if not valid or when<previous:raise ValueError('Invalid or unordered industry history.')
            previous=when
    return log


def write_log(log:dict,path:Path)->None:
    learning.write_log(log,path)


def initialize(path:Path)->None:
    """Create a new empty record, refusing replacement of existing user work."""
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as f:
        json.dump(new_log(),f,indent=2);f.write('\n')


def verify_evidence(log:dict,root:Path)->list[dict]:
    root=Path(root).resolve();rows=[]
    for case,body in log['cases'].items():
        for i,a in enumerate(body['attempts']):
            p=(root/a['evidence']).resolve()
            if not p.is_relative_to(root):s='outside_root'
            elif not p.is_file():s='missing'
            else:s='unchanged' if sha256(p.read_bytes()).hexdigest()==a['evidence_sha256'] else 'changed'
            rows.append({'case':case,'attempt':i+1,'evidence':a['evidence'],'status':s})
    return rows
