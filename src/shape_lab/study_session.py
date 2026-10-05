"""Compose a beginner session from the existing catalog, without copying theory."""
from __future__ import annotations
import json
from pathlib import Path
import shlex
import sys
from typing import Any
from .course import stage_plan, prepare_destination, inside
from .practice_workspace import prepare_practice
from .result_packet import REFLECTION_FIELDS


def study_item(root: Path, key: str) -> dict[str, Any]:
    key=str(key)
    if key.isdigit():
        entry=dict(stage_plan(root,key))
        entry['source_notebook']=entry['reference_lab']
        entry['selection']=['--stage',str(int(key))]
        entry['item']=entry['id']
    else:
        entries=json.loads(inside(root,'curriculum/experiments.json').read_text())['experiments']
        matched=[e for e in entries if e['id']==key]
        if not matched:
            raise ValueError('Unknown study item; use course.py list or course.py cases.')
        entry=dict(matched[0]);entry['source_notebook']=entry['notebook']
        entry['selection']=['--case',key];entry['item']=key
    return entry


def prepare_study(root: Path, key: str, output: Path) -> dict[str, Any]:
    """Prepare, but do not execute: the learner writes a prediction first.

    Reference execution remains owned by course.py run. Existing progress logs
    are not modified, and self-assessment is never inferred from test success.
    """
    root=Path(root).resolve();entry=study_item(root,key)
    out=prepare_destination(root,output)
    prepare_practice(root,str(key),out/'practice')
    reflection={k:'' for k in REFLECTION_FIELDS}
    (out/'reflection.json').write_text(json.dumps(reflection,indent=2)+'\n',encoding='utf-8')
    (out/'prediction.md').write_text('# My prediction before running code\n\nWhat is one observation? What does the smallest calculation produce?\n\nMy prediction:\n\nMy assumptions:\n\nA controlled change I will try:\n',encoding='utf-8')
    run_args=[sys.executable,str(root/'course.py'),'run',*entry['selection'],'--output',str(out/'run01')]
    report_args=[sys.executable,str(root/'course.py'),'report','--run',str(out/'run01'),
                 '--reflection',str(out/'reflection.json'),'--output',str(out/'report01')]
    gate=entry.get('gate','Explain the data unit, method, baseline, result and at least one unsupported conclusion.')
    scope=entry.get('scope','Original course aligned to the supplied outline, not the publisher book or an independent domain benchmark.')
    prerequisites=entry.get('prerequisites',[])
    text=f'''# Study {entry['item']}: {entry['title']}

This is a session guide, not a second theory lesson. Successful execution is not a mastery assessment.

## 1. Read the one primary lesson

[Open primary lesson]({(root/entry['lesson']).as_uri()})

Prerequisites: {', '.join(prerequisites) if prerequisites else 'Start here; no previous course stage required.'}

Completion target: **{gate}**

The absolute link works in this local checkout. After moving the repository, regenerate a new session;
its source-relative path remains `{entry['lesson']}`.

## 2. Predict and calculate

Edit `prediction.md` before running the reference. Name one observation, explain the units, and work
the smallest example with a pencil or basic arithmetic. A wrong prediction is useful evidence when you
explain its correction. Do not copy the worked answer first.

## 3. Run a fresh reference

Run from your prepared course environment. The argv array below is the exact invocation; `run_command`
in study.json has individual arguments for Windows/editor tooling. Do not include terminal prompt symbols.

```bash
{shlex.join(run_args)}
```

`run01/execution.json` lists the actual kernels and file hashes. `run01/executed/` contains fresh outputs.
Dependencies that require earlier generated results are executed first. Choose `run02` on another attempt;
existing run directories are never overwritten.

## 4. Build independently

Open `practice/learner.ipynb` in Jupyter. Intentionally unfinished functions are assignments. Write your
explanation in `practice/answer.md`. Use [reference answers]({(root/entry['answers']).as_uri()}) only after an attempt.
Return later and solve an unfamiliar variant without the answers open.

## 5. Explain and package your result

Fill every field in `reflection.json`: your question, observation unit, method, interpretation, limitation,
and next experiment. These are learner statements; software checks their presence, not their truth.

```bash
{shlex.join(report_args)}
```

Open `report01/index.html` for a local report with executed code and observed outputs. No upload occurs.
Review personal paths, data rights and claims before choosing to share it. An exposed teaching split is
not a new held-out experiment. A copied data row is not another independent participant.

## Scope of this session

{scope}

## 6. Continue without a reset

Use the existing course learning log to record your attempt and evidence path. Tests do not update your
mastery status. Review the corresponding source audit for supplied claims. Keep this folder when upgrading.
A later explanation must distinguish measurement truth, reproducibility, installation, deployment and learning.
'''
    (out/'START.md').write_text(text,encoding='utf-8')
    result={'item':entry['item'],'title':entry['title'],'lesson':entry['lesson'],
            'source_notebook':entry['source_notebook'],'assessment':'not_assessed',
            'reference_executed':False,'run_command':run_args,'report_command':report_args,
            'output':str(out),'scope':scope}
    (out/'study.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result
