"""Local, self-reported evidence log. Never infer mastery from executed notebooks.

The review schedule is a course policy (1, 3, 7, 14, then 30 days), not a
scientifically optimal personal-memory model. No background tasks or network.
"""
from __future__ import annotations
from datetime import date, timedelta
from hashlib import sha256
import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any

PASS_SCORE = 85
REVIEW_DAYS = (1, 3, 7, 14, 30)
KINDS = {'practice', 'assessment', 'recall'}


def new_log(stage_count: int = 13) -> dict[str, Any]:
    if stage_count not in (13,21,31):
        raise ValueError('Choose 13 legacy stages, 21 geometry stages or 31 version-5 stages.')
    return {'schema_version': {13:2,21:3,31:5}[stage_count], 'course_version': {13:'2.0.0',21:'3.0.0',31:'5.0.0'}[stage_count],
            'scope': 'Self-reported learning evidence; not accreditation or automated proof checking.',
            'stages': {f'{n:02d}': {'attempts': []} for n in range(stage_count)}}


def _attempts(log: dict, stage: int) -> list[dict]:
    if not isinstance(stage,int) or f'{stage:02d}' not in log.get('stages',{}):
        raise ValueError('Stage must be an integer included in this learning log.')
    return log['stages'][f'{stage:02d}']['attempts']


def _qualifies(event: dict) -> bool:
    return event['score'] >= PASS_SCORE and event['independent'] and event['critical_clear']


def record(log: dict, stage: int, kind: str, score: float, evidence: str,
           root: Path, day: date, independent: bool = False,
           critical_clear: bool = False, note: str = '') -> None:
    attempts = _attempts(log, stage)
    if kind not in KINDS or not math.isfinite(score) or not 0 <= score <= 100:
        raise ValueError('Use practice/assessment/recall and a finite score between 0 and 100.')
    if not isinstance(day, date):
        raise ValueError('A calendar date is required.')
    if attempts and day < date.fromisoformat(attempts[-1]['date']):
        raise ValueError('Dates cannot reorder this stage\'s existing history.')
    root = Path(root).resolve()
    path = (root / evidence).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('Evidence must be an existing file inside the course directory.')
    attempts.append({'date': day.isoformat(), 'kind': kind, 'score': float(score),
                     'independent': bool(independent), 'critical_clear': bool(critical_clear),
                     'evidence': path.relative_to(root).as_posix(),
                     'evidence_sha256': sha256(path.read_bytes()).hexdigest(), 'note': note})


def stage_status(log: dict, stage: int) -> str:
    attempts = _attempts(log, stage)
    if not attempts:
        return 'not_started'
    status = 'practicing'
    first_demonstrated = None
    for event in attempts:
        if event['kind'] == 'practice':
            continue
        when = date.fromisoformat(event['date'])
        if event['kind'] == 'assessment' and _qualifies(event):
            first_demonstrated = first_demonstrated or when
            status = 'demonstrated'
        elif event['kind'] == 'recall' and first_demonstrated and _qualifies(event):
            status = 'retained' if (when - first_demonstrated).days >= 7 else 'demonstrated'
        elif first_demonstrated:
            status = 'needs_review'
    return status


def next_review(log: dict, stage: int) -> date | None:
    evaluated = [a for a in _attempts(log, stage) if a['kind'] in {'assessment', 'recall'}]
    if not evaluated:
        return None
    last = evaluated[-1]
    if not _qualifies(last):
        delay = 1
    else:
        successful_recalls = sum(a['kind'] == 'recall' and _qualifies(a) for a in evaluated)
        delay = REVIEW_DAYS[min(successful_recalls, len(REVIEW_DAYS) - 1)]
    return date.fromisoformat(last['date']) + timedelta(days=delay)


def due_stages(log: dict, day: date) -> list[int]:
    return [int(n) for n in sorted(log['stages']) if (due := next_review(log, int(n))) is not None and due <= day]


def write_log(log: dict, path: Path) -> None:
    """Atomic single-writer update. Keep your own backups before a course upgrade."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(log, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    tmp.replace(path)


def read_log(path: Path) -> dict:
    log = json.loads(Path(path).read_text(encoding='utf-8'))
    count={2:13,3:21,5:31}.get(log.get('schema_version'))
    if count is None or set(log.get('stages', {})) != {f'{n:02d}' for n in range(count)}:
        raise ValueError('Expected a valid version-2, version-3 or version-5 learning log, not a browser export.')
    for n in range(count):
        attempts = _attempts(log, n)
        if not isinstance(attempts, list):
            raise ValueError('Attempt history must be a list.')
        previous = date.min
        for a in attempts:
            try:
                when = date.fromisoformat(a['date'])
                valid = (a['kind'] in KINDS and math.isfinite(a['score']) and 0 <= a['score'] <= 100
                         and isinstance(a['independent'], bool) and isinstance(a['critical_clear'], bool)
                         and isinstance(a['evidence'], str) and len(a['evidence_sha256']) == 64)
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError('Malformed attempt record.') from exc
            if not valid or when < previous:
                raise ValueError('Invalid or unordered attempt history.')
            previous = when
    return log


def migrate_v2_to_v3(log: dict) -> dict:
    """Copy all legacy attempts into a new log; never reset or invent evidence."""
    if log.get('schema_version')!=2 or set(log.get('stages',{}))!={f'{n:02d}' for n in range(13)}:
        raise ValueError('Only a version-2 log can be migrated by this function.')
    result=new_log(stage_count=21)
    for n in range(13):result['stages'][f'{n:02d}']=deepcopy(log['stages'][f'{n:02d}'])
    result['migration']={'from_version':'2.0.0','policy':'Existing attempts copied verbatim; added stages unassessed.'}
    return result


def migrate_to_v5(log: dict) -> dict:
    """Copy a validated legacy log; all added stages remain unassessed.

    The CLI calls read_log before this function. Existing evidence paths/hashes
    are unchanged; copy their files separately into the same relative paths.
    """
    count={2:13,3:21}.get(log.get('schema_version'))
    if count is None or set(log.get('stages',{}))!={f'{n:02d}' for n in range(count)}:
        raise ValueError('Only a 13- or 21-stage legacy log can be migrated.')
    result=new_log(31)
    for n in range(count):result['stages'][f'{n:02d}']=deepcopy(log['stages'][f'{n:02d}'])
    result['migration']={'from_schema':log['schema_version'], 'previous_course_version':log.get('course_version'),
                        'prior_migration':deepcopy(log.get('migration')),
                        'policy':'Attempts and evidence references copied verbatim; added stages unassessed.'}
    return result
