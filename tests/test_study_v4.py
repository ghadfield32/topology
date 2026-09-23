from pathlib import Path
import subprocess,sys,json,hashlib
import pytest
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts/study.py'

def cli(*args,cwd=None):
    return subprocess.run([sys.executable,str(SCRIPT),*args],cwd=cwd or ROOT,capture_output=True,text=True)

def test_study_script_is_present():
    assert SCRIPT.is_file(), 'The read-only study navigator is not implemented yet.'

@pytest.mark.parametrize('stage',[0,6,12,20])
def test_stage_navigation_has_local_targets(stage,tmp_path):
    assert SCRIPT.is_file(), 'Navigator missing'
    r=cli('stage',str(stage),cwd=tmp_path)
    assert r.returncode==0,r.stderr
    out=json.loads(r.stdout)
    assert out['stage']==stage and len(out['outcomes'])==4
    assert (ROOT/out['session']).is_file()
    assert (ROOT/out['consolidation']).is_file()

def test_invalid_stage_fails_cleanly():
    assert SCRIPT.is_file(), 'Navigator missing'
    r=cli('stage','21')
    assert r.returncode==2 and 'invalid choice' in r.stderr

def test_next_starts_at_zero_without_modifying_log(tmp_path):
    assert SCRIPT.is_file(), 'Navigator missing'
    from shape_lab.learning import new_log,write_log
    p=tmp_path/'log.json';write_log(new_log(stage_count=21),p)
    before=hashlib.sha256(p.read_bytes()).hexdigest()
    r=cli('--log',str(p),'next');assert r.returncode==0,r.stderr
    obj=json.loads(r.stdout);assert obj['stage']==0 and obj['reason']=='first_unfinished'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==before

def test_empty_evidence_is_not_certified(tmp_path):
    assert SCRIPT.is_file(), 'Navigator missing'
    from shape_lab.learning import new_log,write_log
    p=tmp_path/'log.json';write_log(new_log(stage_count=21),p)
    r=cli('--log',str(p),'verify-evidence');assert r.returncode==0,r.stderr
    obj=json.loads(r.stdout)
    assert obj['checked_files']==0 and obj['assessment']=='no_recorded_evidence'

def test_doctor_checks_bundled_data_not_network(tmp_path):
    assert SCRIPT.is_file(), 'Navigator missing'
    r=cli('doctor',cwd=tmp_path);assert r.returncode==0,r.stderr
    obj=json.loads(r.stdout);assert obj['network_calls']==0
    assert all(d['status']=='matches' for d in obj['data'])
    assert len(obj['data'])==4
