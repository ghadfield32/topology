"""Validate declared execution scope without mistaking incomplete logs for success."""
from __future__ import annotations
from collections.abc import Sequence
from pathlib import Path
import html
import json
from typing import Any


def validate_native_evidence(tests: dict, references: dict, profile: str,
                             expected_paths: Sequence[str]) -> list[str]:
    """Consistency validation of locally produced evidence, not proof of authenticity.

    This checks the chosen profile and exact notebook set. It never certifies
    learner mastery, arbitrary third-party logs, clean installs or deployments.
    """
    errors=[]
    if profile not in {'core','physics','full'}:return ['Unknown profile.']
    if tests.get('profile')!=profile:errors.append('Test profile differs from the requested profile.')
    if tests.get('status')!='passed' or tests.get('returncode')!=0:errors.append('Tests did not complete successfully.')
    counts=tests.get('counts',{})
    keys=['total','passed','skipped','failures','errors']
    if not all(type(counts.get(k)) is int and counts[k]>=0 for k in keys):
        errors.append('Missing or invalid test counts.')
    else:
        if counts['total']<1 or counts['passed']<1:errors.append('No passing tests were reported.')
        if counts['total']!=sum(counts[k] for k in keys[1:]):errors.append('Contradictory test totals.')
        if counts['failures'] or counts['errors']:errors.append('JUnit failures/errors remain.')
        if profile=='full' and counts['skipped']:errors.append('Full profile cannot omit skipped checks.')
    records=references.get('records',[])
    paths=[r.get('path') for r in records]
    expected=list(expected_paths)
    if not expected or len(expected)!=len(set(expected)):errors.append('Expected scope must be nonempty and unique.')
    if len(paths)!=len(set(paths)) or set(paths)!=set(expected):errors.append('Executed notebook identities do not match the exact requested scope.')
    if references.get('order')!=expected:errors.append('Execution order differs from the requested dependency order.')
    if any(r.get('status')!='passed' or r.get('source_code_cells',0)<1 for r in records):errors.append('Not every notebook completed its teaching code.')
    if references.get('passed')!=len(expected) or references.get('failed')!=0:errors.append('Notebook success counts are inconsistent or incomplete.')
    if references.get('source_inputs_unchanged') is not True:errors.append('Source inputs were not verified unchanged.')
    if references.get('required_prior_reports_copied') is not False:errors.append('A fresh-input run was not established.')
    return errors


def write_acceptance_page(output: Path, result: dict[str,Any]) -> None:
    """Small dependency-free HTML view linking logs, never embeds credentials."""
    esc=html.escape
    rows=''.join(f'<tr><td>{esc(k)}</td><td>{esc(str(v))}</td></tr>'
                 for k,v in result.get('gates',{}).items())
    links=''.join(f'<p><a href="{esc(p,quote=True)}">{esc(label)}</a></p>' for p,label in [
        ('acceptance.json','Machine-readable acceptance report'),('tests/tests.json','Test counts and profile'),
        ('tests/pytest.log','Complete test log'),('references/execution.json','Every reference execution'),
        ('deploy_static.json','Rendered Kubernetes teaching resources')]
        if (output/p).is_file())
    body=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Course acceptance evidence</title><style>body{{font:18px/1.6 system-ui;max-width:960px;margin:3rem auto;padding:0 1rem}}td{{border-bottom:1px solid #ccc;padding:.6rem}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}a{{text-decoration:underline}}</style>
<h1>Course acceptance</h1><p><strong>{esc(result['status'])}</strong> — {esc(result['scope'])}</p>
<p>Native success does not certify deployment, a fresh installation, or learner mastery.</p><table>{rows}</table>{links}
<h2>Unresolved checks</h2><pre>{esc(json.dumps(result.get('limitations',[]),indent=2))}</pre></html>'''
    (output/'index.html').write_text(body,encoding='utf-8')


def run_acceptance(root: Path, output: Path, profile: str='core', scope: str='first',
                   jobs: int=1, timeout: int=300) -> dict[str,Any]:
    """Run named native gates; never install, deploy, acquire data, or grade learners.

    ``first`` means tests plus the Stage 00 dependency closure; ``all`` means
    tests plus every reference. Kubernetes is rendered/policy-checked only.
    Each child writes independent detailed evidence in this new run directory.
    """
    from .course import prepare_destination,load_catalog,execution_order,run_references
    from .release import environment_status,run_tests,validate_course
    from .deployment import resources,validate_resources
    if scope not in {'first','all'}:raise ValueError('Scope must be first or all.')
    if profile not in {'core','physics','full'}:raise ValueError('Unknown profile.')
    if not 1<=jobs<=4:raise ValueError('Use one to four workers.')
    if scope=='all' and profile=='core':raise ValueError('All references need the physics or full profile.')
    out=prepare_destination(root,output)
    env=environment_status(root,profile)
    result={'release':'12.0.0','status':'running','scope':f'{profile}: tests + {scope} references',
            'profile':profile,'environment':env,'gates':{},'errors':[],
            'learner_assessment':'not_assessed',
            'deployment':{'docker':'not_run','kubernetes':'not_run'},
            'limitations':['No dependency installation is performed by this command.',
                           'Static Kubernetes policy is not API schema, scheduling, storage, or live Job validation.',
                           'Native results do not establish Docker, GPU, another operating system, or learner mastery.']}
    def save():
        (out/'acceptance.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        write_acceptance_page(out,result)
    save()
    try:
        result['gates']['direct_dependency_compatibility']='passed' if env['compatible'] else 'blocked'
        manifest=resources('listening-to-shape:12','shape-acceptance-check',profile)
        (out/'deploy_static.json').write_text(json.dumps(manifest,indent=2)+'\n')
        issues=validate_resources(manifest)
        result['gates']['kubernetes_project_policy']='passed' if not issues else 'failed'
        result['errors'].extend(issues)
        if not env['compatible']:
            result.update(status='blocked');save();return result
        structure=validate_course(root,profile)
        result['gates']['course_structure']=structure['status']
        if structure['status']!='passed':
            result['errors'].append('Course structure is invalid.');result['status']='failed';save();return result
        catalog=load_catalog(root)
        targets=catalog['reference_notebooks'] if scope=='all' else [catalog['stages'][0]['reference_lab']]
        expected=execution_order(root,targets)
        result['expected_reference_paths']=expected
        tests=run_tests(root,out/'tests',profile)
        result['gates']['tests']=tests['status'];save()
        if tests['status']!='passed':result['status']=tests['status'];save();return result
        references=run_references(root,targets,out/'references',jobs,timeout)
        result['gates']['references']='passed' if references['failed']==0 else 'failed'
        issues=validate_native_evidence(tests,references,profile,expected)
        result['errors'].extend(issues)
        result['gates']['evidence_consistency']='passed' if not issues else 'failed'
        result['status']='passed' if not result['errors'] else 'failed'
    except Exception as exc:
        result['status']='failed';result['errors'].append(f'{type(exc).__name__}: {exc}')
        save();raise
    save();return result
