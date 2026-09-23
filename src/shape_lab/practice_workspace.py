"""Create learner-owned practice copies, never overwrite or change assessment."""
from __future__ import annotations
from pathlib import Path
import hashlib,json,shutil
from .course import load_catalog,stage_plan,prepare_destination,inside


def prepare_practice(root: Path,key: str,output: Path) -> dict:
    if str(key).isdigit():
        spec=stage_plan(root,key)
    else:
        items=json.loads((root/'curriculum/experiments.json').read_text())['experiments']
        matches=[x for x in items if x['id']==key and 'learner' in x]
        if not matches:raise ValueError('Use a core stage 0–30 or a case listed by python course.py cases.')
        spec=matches[0]
    src=inside(root,spec['learner']);out=prepare_destination(root,output)
    # A private assignment must be editable even when its reference is read-only.
    shutil.copyfile(src,out/'learner.ipynb')
    (out/'answer.md').write_text(f"# My evidence: {key} — {spec['title']}\n\n## Observation unit and assumptions\n\n## Prediction before code\n\n## Hand calculation\n\n## Observed result and saved run path\n\n## Explanation and counterexample\n\n## What the evidence does not establish\n\n## Delayed recall and unresolved questions\n",encoding='utf-8')
    report={'item':key,'source':spec['learner'],'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
            'lesson':spec['lesson'],'output':str(out),'assessment':'not_assessed'}
    (out/'practice.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
