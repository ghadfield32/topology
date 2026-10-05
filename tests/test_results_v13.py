"""Small manufactured fixtures test provenance handling, not a real deployment."""
from pathlib import Path
import json
import hashlib
import nbformat
import pytest
from shape_lab import result_packet as packet
from shape_lab import study_session as study
from shape_lab.course import stage_plan

ROOT=Path(__file__).resolve().parents[1]

@pytest.fixture
def run(tmp_path):
    run=tmp_path/'run'; (run/'executed/notebooks').mkdir(parents=True)
    b=nbformat.v4.new_notebook(cells=[
        nbformat.v4.new_markdown_cell('An observed number is not a population guarantee.'),
        nbformat.v4.new_code_cell('print(2+2)',execution_count=1,
          outputs=[nbformat.v4.new_output('stream',name='stdout',text='4\n')])])
    nbformat.write(b,run/'executed/notebooks/a.ipynb')
    (run/'artifacts').mkdir();(run/'artifacts/results.json').write_text('{"observed":4}')
    report={'mode':'fresh_input_workspace_and_fresh_kernels','required_prior_reports_copied':False,
            'source_inputs_unchanged':True,'order':['notebooks/a.ipynb'],'passed':1,'failed':0,
            'records':[{'path':'notebooks/a.ipynb','status':'passed','source_code_cells':1}],
            'runtime_environment':{'python':'test-fixture'},'learner_assessment':'not_assessed'}
    packet.seal_run(run,report)
    (run/'execution.json').write_text(json.dumps(report))
    return run

@pytest.fixture
def reflection():
    return {'question':'Does this worked calculation reproduce?', 'observation_unit':'One manufactured example.',
            'method':'Evaluate the supplied arithmetic, no statistical model.',
            'result_interpretation':'Four is the displayed output of this example.',
            'limitation':'No empirical population or benchmark was evaluated.',
            'next_experiment':'Change a controlled input and predict the result before running.'}

def test_new_modules_present():
    assert callable(getattr(packet,'seal_run',None))
    assert callable(getattr(study,'prepare_study',None))

def test_seal_validates(run):
    assert packet.validate_run(run)==[]
    r=json.loads((run/'execution.json').read_text())
    assert len(r['output_sha256'])==2

def test_changed_notebook_refused(run):
    p=run/'executed/notebooks/a.ipynb';p.write_text(p.read_text()+' ')
    assert any('Changed' in e for e in packet.validate_run(run))

def test_changed_artifact_refused(run):
    (run/'artifacts/results.json').write_text('{"observed":99}')
    assert packet.validate_run(run)

def test_unlisted_artifact_refused(run):
    (run/'artifacts/late.json').write_text('{}')
    assert packet.validate_run(run)

@pytest.mark.parametrize('change',[{'passed':0},{'failed':1},{'source_inputs_unchanged':False},
 {'required_prior_reports_copied':True},{'records':[]},{'order':[]},{'output_sha256':{}},
 {'output_sha256':{'../outside':'0'*64}},{'output_sha256':{'/outside':'0'*64}}])
def test_bad_ledger_refused(run,change):
    p=run/'execution.json';r=json.loads(p.read_text());r.update(change);p.write_text(json.dumps(r))
    assert packet.validate_run(run)

def test_missing_file_refused(run):
    (run/'executed/notebooks/a.ipynb').unlink()
    assert packet.validate_run(run)

def test_error_output_refused_even_resealed(run):
    p=run/'executed/notebooks/a.ipynb';b=nbformat.read(p,as_version=4)
    b.cells[1].outputs=[nbformat.v4.new_output('error',ename='ValueError',evalue='failed',traceback=[])]
    nbformat.write(b,p);r=json.loads((run/'execution.json').read_text());packet.seal_run(run,r)
    (run/'execution.json').write_text(json.dumps(r));assert packet.validate_run(run)

def test_symlink_escape_refused(run,tmp_path):
    p=run/'artifacts/results.json';p.unlink();other=tmp_path/'private';other.write_text('not-public')
    try:p.symlink_to(other)
    except OSError:pytest.skip('Host disallows symlinks')
    assert packet.validate_run(run)

def test_packet_local_only(run,tmp_path,reflection):
    r=packet.export_packet(run,tmp_path/'packet',reflection)
    assert r['status']=='passed' and r['published'] is False and r['learner_assessment']=='not_assessed'
    assert (tmp_path/'packet/index.html').is_file()
    assert (tmp_path/'packet/notebooks/notebooks/a.html').is_file()
    assert '4' in (tmp_path/'packet/notebooks/notebooks/a.html').read_text()

def test_packet_refuses_existing(run,tmp_path,reflection):
    out=tmp_path/'packet';out.mkdir()
    with pytest.raises(FileExistsError):packet.export_packet(run,out,reflection)

@pytest.mark.parametrize('field',['question','observation_unit','method','result_interpretation','limitation','next_experiment'])
def test_packet_requires_reflection(run,tmp_path,reflection,field):
    reflection[field]=''
    with pytest.raises(ValueError):packet.export_packet(run,tmp_path/'packet',reflection)

def test_packet_escapes_html(run,tmp_path,reflection):
    reflection['question']='<script>alert(1)</script>'
    packet.export_packet(run,tmp_path/'packet',reflection)
    s=(tmp_path/'packet/index.html').read_text()
    assert '<script>alert(1)</script>' not in s and '&lt;script&gt;' in s

def test_packet_refuses_stale_output(run,tmp_path,reflection):
    (run/'artifacts/results.json').write_text('tampered')
    with pytest.raises(ValueError):packet.export_packet(run,tmp_path/'packet',reflection)

@pytest.mark.parametrize('key',['0','06','30','wine','s00','r01','r05','acb'])
def test_study_resolves_existing_routes(tmp_path,key):
    out=tmp_path/f'study-{key}'
    r=study.prepare_study(ROOT,key,out)
    assert r['assessment']=='not_assessed'
    assert (out/'practice/learner.ipynb').is_file()
    assert (out/'START.md').is_file() and (out/'reflection.json').is_file()
    assert (ROOT/r['lesson']).is_file()
    assert r['source_notebook'] in json.loads((ROOT/'curriculum/catalog.json').read_text())['reference_notebooks']

def test_study_invalid_key_no_destination(tmp_path):
    with pytest.raises(ValueError):study.prepare_study(ROOT,'no-such-course',tmp_path/'out')
    assert not (tmp_path/'out').exists()

def test_study_never_overwrites(tmp_path):
    study.prepare_study(ROOT,'0',tmp_path/'session')
    with pytest.raises(FileExistsError):study.prepare_study(ROOT,'0',tmp_path/'session')

def test_study_uses_same_primary_lesson(tmp_path):
    r=study.prepare_study(ROOT,'6',tmp_path/'session')
    assert r['lesson']==stage_plan(ROOT,6)['lesson']
    assert 'not a mastery' in (tmp_path/'session/START.md').read_text()

@pytest.mark.parametrize('change',[{'passed':True},{'failed':False},{'output_seal_schema':True}])
def test_boolean_not_numeric_evidence(run,change):
    p=run/'execution.json';r=json.loads(p.read_text());r.update(change);p.write_text(json.dumps(r))
    assert packet.validate_run(run)

def test_unexecuted_cell_refused_after_reseal(run):
    p=run/'executed/notebooks/a.ipynb';b=nbformat.read(p,as_version=4);b.cells[1].execution_count=None;nbformat.write(b,p)
    r=json.loads((run/'execution.json').read_text());packet.seal_run(run,r);(run/'execution.json').write_text(json.dumps(r))
    assert packet.validate_run(run)

def test_kubernetes_job_checks_actual_outputs():
    from shape_lab.deployment import resources
    r=resources('course:13','shape-test','core')
    job=next(x for x in r['items'] if x['kind']=='Job')
    code=job['spec']['template']['spec']['containers'][0]['command'][-1]
    assert 'validate_run' in code
