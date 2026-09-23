"""Repository contract tests: synthetic controls, not claimed deployment evidence."""
from pathlib import Path
import ast
import importlib.util
import json
import os
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]

def test_runtime_module_exists():
    assert (ROOT / 'src/shape_lab/runtime.py').is_file(), 'Explicit kernel/runtime provenance is required.'

def test_runner_module_exists():
    assert (ROOT / 'src/shape_lab/release.py').is_file(), 'Release evidence must distinguish unavailable checks.'

def test_kernel_spec_uses_active_python(tmp_path):
    from shape_lab.runtime import write_kernel_spec
    directory = write_kernel_spec(tmp_path, sys.executable)
    spec = json.loads((directory / 'kernel.json').read_text())
    assert spec['argv'][0] == sys.executable
    assert spec['argv'][1:] == ['-m', 'ipykernel_launcher', '-f', '{connection_file}']
    assert spec['language'] == 'python'

def test_runtime_probe_checks_executable_and_workspace(tmp_path):
    from shape_lab.runtime import validate_kernel_provenance
    workspace = tmp_path / 'course'; (workspace / 'src/shape_lab').mkdir(parents=True)
    record = {'python_executable': sys.executable, 'shape_lab_origin': str(workspace/'src/shape_lab/__init__.py')}
    assert validate_kernel_provenance(record, sys.executable, workspace) == record
    with pytest.raises(ValueError, match='interpreter'):
        validate_kernel_provenance({**record, 'python_executable': '/wrong/python'}, sys.executable, workspace)
    with pytest.raises(ValueError, match='copied source'):
        validate_kernel_provenance({**record, 'shape_lab_origin': '/other/shape_lab/__init__.py'}, sys.executable, workspace)

def test_copy_excludes_secrets_and_build_products(tmp_path):
    from shape_lab.course import copy_inputs
    source = tmp_path/'source'; source.mkdir()
    for name in ['.env', '.env.local', 'token.pem']:
        (source/name).write_text('private')
    for name in ['dist', '.uv-cache', 'node_modules']:
        p=source/name; p.mkdir(); (p/'private.txt').write_text('private')
    (source/'.env.example').write_text('EXAMPLE=not-a-secret')
    (source/'lesson.md').write_text('keep')
    copy_inputs(source,tmp_path/'copy')
    target=tmp_path/'copy'
    assert (target/'lesson.md').exists()
    assert (target/'.env.example').exists()
    for name in ['.env','.env.local','token.pem','dist','.uv-cache','node_modules']:
        assert not (target/name).exists(), name

@pytest.mark.skipif(os.name == 'nt', reason='POSIX symlink creation control')
def test_copy_rejects_external_symlink(tmp_path):
    from shape_lab.course import copy_inputs
    source=tmp_path/'source'; source.mkdir(); outside=tmp_path/'outside.txt'; outside.write_text('private')
    (source/'escape.txt').symlink_to(outside)
    with pytest.raises(ValueError, match='symlink'):
        copy_inputs(source,tmp_path/'copy')

def test_core_catalog_preserved():
    from shape_lab.course import load_catalog
    catalog=load_catalog(ROOT)
    assert len(catalog['stages']) == 31
    assert len({x['lesson'] for x in catalog['stages']}) == 31
    assert len(catalog['reference_notebooks']) == 133

def test_fingerprint_tracks_inputs_not_outputs(tmp_path):
    from shape_lab.runtime import fingerprint_inputs
    for d in ['src/shape_lab','data','progress','my_work']:(tmp_path/d).mkdir(parents=True)
    (tmp_path/'src/shape_lab/a.py').write_text('x=1\n')
    (tmp_path/'data/a.csv').write_text('x\n1\n')
    (tmp_path/'progress/log.json').write_text('{}')
    before=fingerprint_inputs(tmp_path)
    (tmp_path/'my_work/output.json').write_text('{"result":1}')
    assert fingerprint_inputs(tmp_path)==before
    (tmp_path/'data/a.csv').write_text('x\n2\n')
    assert fingerprint_inputs(tmp_path)!=before

def test_profile_full_is_strict_not_silent_skip():
    from shape_lab.release import required_distributions
    assert {'ripser','gudhi','torch'} <= set(required_distributions('full'))
    assert 'torch' not in required_distributions('core')
    with pytest.raises(ValueError): required_distributions('unknown')

def test_dataset_catalog_paths_resolve():
    p=ROOT/'curriculum/experiments.json'
    assert p.is_file()
    data=json.loads(p.read_text())
    keys=[x['id'] for x in data['experiments']]
    assert len(keys)==len(set(keys))
    for x in data['experiments']:
        assert (ROOT/x['notebook']).is_file()
        assert (ROOT/x['lesson']).is_file()
        assert x['scope'] and x['data_status']

def test_no_unsubstantiated_lock_claim():
    p=ROOT/'docs/release/ENVIRONMENT_STATUS.json'
    assert p.is_file()
    obj=json.loads(p.read_text())
    if not (ROOT/'uv.lock').exists():
        assert obj['uv_lock']['status'] != 'passed'
    assert obj['docker_build']['status'] in {'passed','blocked','not_run'}

def test_deployment_assets_exist():
    for name in ['Dockerfile','compose.yaml','.dockerignore','.gitignore','.python-version',
                 '.github/workflows/course-ci.yml','tools/bootstrap.py','tools/docker_verify.py','course.py']:
        assert (ROOT/name).is_file(), name

def test_docker_uses_locked_sync_and_no_auth_bypass():
    text=(ROOT/'Dockerfile').read_text()
    assert 'uv sync --locked' in text
    assert 'USER student' in text
    compose=(ROOT/'compose.yaml').read_text()
    assert '127.0.0.1:' in compose
    assert 'token=' not in compose and 'disable_check_xsrf' not in compose

def test_git_excludes_secrets_work_and_venvs():
    text=(ROOT/'.gitignore').read_text()
    for entry in ['.venv/','.env','my_work/','*.pem']:
        assert entry in text

def test_python_floor_matches_supported_course_version():
    import tomllib
    obj=tomllib.loads((ROOT/'pyproject.toml').read_text())
    assert obj['project']['requires-python'] == '>=3.13,<3.14'
    assert (ROOT/'.python-version').read_text().strip()=='3.13.5'

def test_bootstrap_has_explicit_offline_reuse_not_false_isolation():
    text=(ROOT/'tools/bootstrap.py').read_text()
    assert '--reuse-installed' in text
    assert 'system-site-packages' in text
    assert 'not a fresh dependency install' in text.lower()

def test_explicit_reuse_records_nested_environment_paths(tmp_path):
    from shape_lab.runtime import write_reuse_sites
    source=tmp_path/'outer-venv'/'site-packages'
    marker=write_reuse_sites(tmp_path,[str(source)])
    text=marker.read_text()
    assert 'import sys;' in text
    assert ast.literal_eval(text.split('=',1)[1].strip())==[str(source)]
    metadata=json.loads((tmp_path/'shape_reuse_installed.json').read_text())
    assert metadata['independent_install'] is False
    assert metadata['source_site_paths']==[str(source)]

def test_normal_setup_rejects_an_inherited_diagnostic_environment(tmp_path):
    from shape_lab.runtime import assert_clean_setup_target
    venv=tmp_path/'.venv'; site=venv/'lib/python3.13/site-packages'; site.mkdir(parents=True)
    (site/'shape_reuse_installed.json').write_text('{"independent_install": false}')
    with pytest.raises(ValueError,match='diagnostic'):
        assert_clean_setup_target(venv)
    (site/'shape_reuse_installed.json').unlink()
    (venv/'pyvenv.cfg').write_text('include-system-site-packages = true\n')
    with pytest.raises(ValueError,match='site-packages'):
        assert_clean_setup_target(venv)
    (venv/'pyvenv.cfg').write_text('include-system-site-packages = false\n')
    assert assert_clean_setup_target(venv) is None

def test_fingerprint_includes_tools_and_scripts(tmp_path):
    from shape_lab.runtime import fingerprint_inputs
    (tmp_path/'tools').mkdir();(tmp_path/'scripts').mkdir()
    (tmp_path/'tools/setup.py').write_text('x=1')
    (tmp_path/'scripts/run.py').write_text('x=2')
    assert set(fingerprint_inputs(tmp_path)) == {'tools/setup.py','scripts/run.py'}

def test_git_preserves_data_snapshot_bytes():
    text=(ROOT/'.gitattributes').read_text()
    for entry in ['data/** -text','sports_v8/data/** -text','sports_v9/data/** -text']:
        assert entry in text

def test_progress_initialization_preserves_existing_work(tmp_path):
    from shape_lab.runtime import initialize_progress
    templates=tmp_path/'progress/templates';templates.mkdir(parents=True)
    (templates/'learning_log_v5.json').write_text('{"stages": {}}')
    assert initialize_progress(tmp_path)==['progress/learning_log_v5.json']
    path=tmp_path/'progress/learning_log_v5.json';path.write_text('{"my_answer":1}')
    assert initialize_progress(tmp_path)==[]
    assert path.read_text()=='{"my_answer":1}'

def test_all_catalog_reference_inputs_are_fingerprinted():
    from shape_lab.runtime import fingerprint_inputs
    paths=set(fingerprint_inputs(ROOT))
    refs=set(json.loads((ROOT/'curriculum/catalog.json').read_text())['reference_notebooks'])
    assert refs <= paths
