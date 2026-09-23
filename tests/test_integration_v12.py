"""Regression tests for actionable course paths and honest acceptance evidence."""
from pathlib import Path
import copy
import json
import sys
import os
import pytest

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / 'curriculum/experiments.json').read_text())['experiments']

@pytest.mark.parametrize('case', CASES, ids=lambda c: c['id'])
def test_every_named_case_exposes_existing_practice(case, tmp_path):
    from shape_lab.practice_workspace import prepare_practice
    assert 'learner' in case and 'answers' in case
    assert (ROOT / case['learner']).is_file()
    assert (ROOT / case['answers']).is_file()
    result = prepare_practice(ROOT, case['id'], tmp_path / case['id'])
    assert result['assessment'] == 'not_assessed'
    assert (tmp_path / case['id'] / 'learner.ipynb').read_bytes() == (ROOT / case['learner']).read_bytes()


def test_installed_wrong_version_is_not_ready(monkeypatch):
    from shape_lab import release
    real = release.md.version
    monkeypatch.setattr(release.md, 'version', lambda name: '0.1.0' if name == 'numpy' else real(name))
    status = release.environment_status(ROOT, 'core')
    assert status['compatible'] is False
    assert any(x['distribution'] == 'numpy' for x in status['incompatible'])
    assert release.validate_course(ROOT, 'core')['status'] == 'failed'


def test_cpu_local_torch_version_compatible(monkeypatch):
    from shape_lab import release
    real=release.md.version
    monkeypatch.setattr(release.md,'version',lambda n:'2.10.0+cpu' if n=='torch' else real(n))
    status = release.environment_status(ROOT, 'physics')
    assert status['compatible'] is True
    assert status['incompatible'] == []


def test_reader_does_not_attach_work_pvc():
    from shape_lab.deployment import resources
    obj = resources('course:12', 'shape-tests')
    dep = next(x for x in obj['items'] if x['kind'] == 'Deployment')
    pod = dep['spec']['template']['spec']
    assert not any('persistentVolumeClaim' in v for v in pod['volumes'])
    assert not any(v['mountPath'] == '/work' for c in pod['containers'] for v in c['volumeMounts'])


@pytest.mark.parametrize('change', ['privileged', 'hostNetwork', 'hostPath', 'root', 'seccomp', 'namespace', 'duplicate'])
def test_kube_policy_catches_unsafe_or_ambiguous_resources(change):
    from shape_lab.deployment import resources, validate_resources
    obj = resources('course:12', 'shape-tests')
    item = next(x for x in obj['items'] if x['kind'] == 'Job')
    pod = item['spec']['template']['spec']
    if change == 'privileged': pod['containers'][0]['securityContext']['privileged'] = True
    elif change == 'hostNetwork': pod['hostNetwork'] = True
    elif change == 'hostPath': pod['volumes'].append({'name': 'host', 'hostPath': {'path': '/'}})
    elif change == 'root': pod['securityContext']['runAsUser'] = 0
    elif change == 'seccomp': pod['securityContext']['seccompProfile'] = {'type': 'Unconfined'}
    elif change == 'namespace': item['metadata']['namespace'] = 'other'
    elif change == 'duplicate': obj['items'].append(copy.deepcopy(item))
    assert validate_resources(obj), change


def good_evidence():
    return ({'profile': 'physics', 'status': 'passed', 'returncode': 0,
             'counts': {'total': 10, 'passed': 8, 'skipped': 2, 'failures': 0, 'errors': 0}},
            {'order': ['notebooks/00_lab.ipynb'], 'passed': 1, 'failed': 0,
             'records': [{'path': 'notebooks/00_lab.ipynb', 'status': 'passed', 'source_code_cells': 2}],
             'source_inputs_unchanged': True, 'required_prior_reports_copied': False})


def test_evidence_requires_child_details_not_just_zero_exit():
    from shape_lab.acceptance import validate_native_evidence
    assert validate_native_evidence({}, {}, 'physics', ['notebooks/00_lab.ipynb'])
    tests, refs = good_evidence()
    assert validate_native_evidence(tests, refs, 'physics', refs['order']) == []


@pytest.mark.parametrize('change', ['profile','skips_full','totals','failed','duplicate','missing','tamper','prior_reports'])
def test_evidence_rejects_contradictions(change):
    from shape_lab.acceptance import validate_native_evidence
    t, r = good_evidence(); profile = 'physics'
    if change == 'profile': t['profile'] = 'core'
    elif change == 'skips_full': profile = t['profile'] = 'full'
    elif change == 'totals': t['counts']['total'] = 999
    elif change == 'failed': r['records'][0]['status'] = 'failed'
    elif change == 'duplicate': r['records'].append(r['records'][0].copy())
    elif change == 'missing': r['records'] = []
    elif change == 'tamper': r['source_inputs_unchanged'] = False
    elif change == 'prior_reports': r['required_prior_reports_copied'] = True
    assert validate_native_evidence(t, r, profile, ['notebooks/00_lab.ipynb'])


def test_kit_has_one_case_practice_route_per_case():
    cases = json.loads((ROOT / 'curriculum/experiments.json').read_text())['experiments']
    assert len({x['learner'] for x in cases}) == len(cases) == 25


def test_acceptance_blocks_full_when_crosschecks_absent(tmp_path, monkeypatch):
    from shape_lab import acceptance, release
    real=release.environment_status
    def missing(root,profile):
        out=real(root,profile);out.update(compatible=False,missing=['ripser','gudhi']);return out
    monkeypatch.setattr(release,'environment_status',missing)
    result=acceptance.run_acceptance(ROOT,tmp_path/'blocked','full','first',1)
    assert result['status']=='blocked'
    assert result['deployment']['docker']=='not_run'
    assert result['deployment']['kubernetes']=='not_run'
    assert (tmp_path/'blocked'/'index.html').is_file()
    assert not (tmp_path/'blocked'/'references').exists()


def test_acceptance_refuses_existing_output(tmp_path):
    from shape_lab.acceptance import run_acceptance
    folder=tmp_path/'old';folder.mkdir();(folder/'answer.txt').write_text('retain')
    with pytest.raises(FileExistsError):run_acceptance(ROOT,folder,'physics','first',1)
    assert (folder/'answer.txt').read_text()=='retain'


def test_acceptance_cli_has_explicit_scope():
    from shape_lab.cli import main
    with pytest.raises(SystemExit) as exc:main(ROOT,['acceptance','--help'])
    assert exc.value.code==0


def test_junit_absent_is_not_a_passing_test_run(tmp_path,monkeypatch):
    from shape_lab import release
    from types import SimpleNamespace
    monkeypatch.setattr(release,'environment_status',lambda *args,**kwargs:{'compatible':True})
    monkeypatch.setattr(release.subprocess,'run',lambda *args,**kwargs:SimpleNamespace(returncode=0))
    result=release.run_tests(ROOT,tmp_path/'empty-report','physics')
    assert result['status']=='failed'
    assert result['returncode']!=0


def test_cluster_marker_carries_detailed_evidence():
    from shape_lab.deployment import resources
    m=resources('course:12','shape-unit','physics')
    job=next(x for x in m['items'] if x['kind']=='Job')
    code=job['spec']['template']['spec']['containers'][0]['command'][-1]
    assert 'validate_native_evidence' in code
    assert 'tests.json' in code and 'execution.json' in code


@pytest.mark.skipif(os.name != 'posix', reason='POSIX directory mode-bit contract; not a Windows filesystem permission model.')
def test_copy_readonly_source_makes_only_workspace_writable(tmp_path):
    from shape_lab.course import copy_inputs
    import stat
    source=tmp_path/'source';source.mkdir();file=source/'lesson.txt';file.write_text('original')
    file.chmod(0o444);source.chmod(0o555)
    dest=tmp_path/'workspace'
    try:
        copy_inputs(source,dest)
        assert dest.stat().st_mode & stat.S_IWUSR
        assert (dest/'lesson.txt').stat().st_mode & stat.S_IWUSR
        assert not file.stat().st_mode & stat.S_IWUSR
        assert not source.stat().st_mode & stat.S_IWUSR
    finally:
        source.chmod(0o755);file.chmod(0o644)


def test_bootstrap_records_timeout_without_fallback(tmp_path,monkeypatch):
    import importlib.util,subprocess
    spec=importlib.util.spec_from_file_location('boot_under_test',ROOT/'tools/bootstrap.py')
    boot=importlib.util.module_from_spec(spec);spec.loader.exec_module(boot)
    root=tmp_path/'project';root.mkdir();out=tmp_path/'setup'
    monkeypatch.setattr(boot,'ROOT',root)
    monkeypatch.setattr(boot.shutil,'which',lambda n:'/usr/bin/uv')
    def timeout(cmd,**kw):raise subprocess.TimeoutExpired(cmd,kw['timeout'])
    monkeypatch.setattr(boot.subprocess,'run',timeout)
    monkeypatch.setattr(sys,'argv',['bootstrap.py','--timeout','1','--output',str(out)])
    assert boot.main()==2
    record=json.loads((out/'setup.json').read_text())
    assert record['status']=='blocked'
    assert record['fresh_dependency_install'] is False
    assert record['commands'][0]['returncode']==124
    assert 'Timed out' in (out/record['commands'][0]['log']).read_text()


def test_private_practice_from_readonly_reference_is_editable(tmp_path):
    import stat
    from shape_lab.practice_workspace import prepare_practice
    root=tmp_path/'course';(root/'curriculum').mkdir(parents=True)
    source=root/'practice.ipynb';source.write_text('{"cells": []}');source.chmod(0o444)
    (root/'lesson.md').write_text('Lesson')
    (root/'curriculum/experiments.json').write_text(json.dumps({'experiments':[{'id':'sample','title':'Sample','learner':'practice.ipynb','lesson':'lesson.md'}]}))
    out=tmp_path/'answer'
    try:
        prepare_practice(root,'sample',out)
        assert (out/'learner.ipynb').stat().st_mode & stat.S_IWUSR
        assert not source.stat().st_mode & stat.S_IWUSR
    finally:source.chmod(0o644)
