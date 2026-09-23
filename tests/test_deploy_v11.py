"""Static/fixture checks are not substitutes for a Kubernetes API or runtime."""
from pathlib import Path
import importlib.util
import json
import pytest
ROOT=Path(__file__).resolve().parents[1]

def test_deployment_module_exists():
    assert importlib.util.find_spec('shape_lab.deployment') is not None

def test_resources_have_least_privilege_and_unique_output():
    from shape_lab.deployment import resources,validate_resources
    manifest=resources('example/course:11','shape-lesson11','core')
    assert validate_resources(manifest)==[]
    job=next(x for x in manifest['items'] if x['kind']=='Job')
    pod=job['spec']['template']['spec'];container=pod['containers'][0]
    assert pod['automountServiceAccountToken'] is False
    assert container['securityContext']['readOnlyRootFilesystem'] is True
    assert container['securityContext']['allowPrivilegeEscalation'] is False
    assert pod['restartPolicy']=='Never' and job['spec']['backoffLimit']==0
    assert 'metadata.uid' in json.dumps(container['env'])
    assert not any(x['spec'].get('type') in ['LoadBalancer','NodePort'] for x in manifest['items'] if x['kind']=='Service')

@pytest.mark.parametrize('namespace',['default','kube-system','bad/name','UPPER','-bad','x'*64])
def test_unsafe_namespace_rejected(namespace):
    from shape_lab.deployment import resources
    with pytest.raises(ValueError):resources('course:11',namespace,'core')

def test_static_policy_catches_privilege_regression():
    from shape_lab.deployment import resources,validate_resources
    manifest=resources('course:11','shape-lesson11','core')
    job=next(x for x in manifest['items'] if x['kind']=='Job')
    job['spec']['template']['spec']['containers'][0]['securityContext']['allowPrivilegeEscalation']=True
    assert validate_resources(manifest)

def test_missing_tool_report_not_success(monkeypatch,tmp_path):
    from shape_lab.deployment import preflight
    monkeypatch.setattr('shape_lab.deployment.shutil.which',lambda _:None)
    report=preflight('kind-shape-learning')
    assert report['status']=='blocked' and report['cluster_verified'] is False

def test_context_guard():
    from shape_lab.deployment import preflight
    with pytest.raises(ValueError,match='kind-'):preflight('production')

def test_server_module_exists():
    assert importlib.util.find_spec('shape_lab.safe_server') is not None

@pytest.mark.parametrize('url',['/.git/config','/my_work/answers.txt','/progress/log.json','/.env','/foo/../.git/config','/%2e%2e/.env','/private.pem'])
def test_private_reader_paths_rejected(url,tmp_path):
    from shape_lab.safe_server import public_path
    assert public_path(tmp_path,url) is None

def test_reader_public_lesson_and_external_symlink(tmp_path):
    from shape_lab.safe_server import public_path
    (tmp_path/'lesson.md').write_text('public')
    assert public_path(tmp_path,'/lesson.md?x=1')==tmp_path/'lesson.md'
    outside=tmp_path.parent/'secret.txt';outside.write_text('private')
    try:(tmp_path/'link.txt').symlink_to(outside)
    except OSError:pytest.skip('Host disallows symlinks')
    assert public_path(tmp_path,'/link.txt') is None

def test_practice_copy_preserves_original_and_refuses_overwrite(tmp_path):
    from shape_lab.practice_workspace import prepare_practice
    before=(ROOT/'representations/learner/r01.ipynb').read_bytes()
    out=tmp_path/'practice'
    report=prepare_practice(ROOT,'r01',out)
    assert (out/'learner.ipynb').read_bytes()==before and (out/'answer.md').exists()
    assert report['assessment']=='not_assessed'
    with pytest.raises(FileExistsError):prepare_practice(ROOT,'r01',out)
    assert (ROOT/'representations/learner/r01.ipynb').read_bytes()==before

def test_representation_sources_and_controls_are_in_run_fingerprint():
    from shape_lab.runtime import fingerprint_inputs
    fp=fingerprint_inputs(ROOT)
    assert 'representations/lessons/R01.md' in fp
    assert 'deploy/kubernetes/resources.json' in fp
