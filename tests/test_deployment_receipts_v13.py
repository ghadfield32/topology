"""Manufactured acceptance evidence exercises the validator, not Docker itself."""
import json
from pathlib import Path
import nbformat
import pytest
from shape_lab import acceptance
from shape_lab.result_packet import seal_run

@pytest.fixture
def receipt(tmp_path):
    d=tmp_path/'receipt'; (d/'tests').mkdir(parents=True); (d/'references/executed/notebooks').mkdir(parents=True)
    b=nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell('print(4)',execution_count=1,
        outputs=[nbformat.v4.new_output('stream',name='stdout',text='4\n')])])
    nbformat.write(b,d/'references/executed/notebooks/00_lab.ipynb')
    tests={'profile':'core','status':'passed','returncode':0,'counts':{'total':2,'passed':1,'skipped':1,'failures':0,'errors':0}}
    refs={'mode':'fresh_input_workspace_and_fresh_kernels','required_prior_reports_copied':False,
          'source_inputs_unchanged':True,'passed':1,'failed':0,'order':['notebooks/00_lab.ipynb'],
          'records':[{'path':'notebooks/00_lab.ipynb','status':'passed','source_code_cells':1}]}
    seal_run(d/'references',refs)
    (d/'references/execution.json').write_text(json.dumps(refs))
    (d/'tests/tests.json').write_text(json.dumps(tests))
    (d/'tests/junit.xml').write_text('<testsuites><testsuite><testcase name="a"/><testcase name="b"><skipped/></testcase></testsuite></testsuites>')
    (d/'acceptance.json').write_text(json.dumps({'profile':'core','status':'passed','expected_reference_paths':['notebooks/00_lab.ipynb']}))
    return d

def check(d,profile='core'):
    assert callable(getattr(acceptance,'validate_acceptance_directory',None)), 'Missing on-disk child-evidence validator'
    return acceptance.validate_acceptance_directory(d,profile,['notebooks/00_lab.ipynb'])

def test_valid_child_files(receipt):
    assert check(receipt)==[]

@pytest.mark.parametrize('name',['acceptance.json','tests/tests.json','tests/junit.xml','references/execution.json'])
def test_exit_zero_cannot_replace_missing_files(receipt,name):
    (receipt/name).unlink();assert check(receipt)

def test_xml_counts_must_match_json(receipt):
    (receipt/'tests/junit.xml').write_text('<testsuites><testsuite><testcase name="a"/></testsuite></testsuites>')
    assert check(receipt)

def test_actual_notebook_tamper_rejected(receipt):
    p=receipt/'references/executed/notebooks/00_lab.ipynb';p.write_text(p.read_text()+' ')
    assert check(receipt)

def test_requested_profile_checked(receipt):
    assert check(receipt,'full')

def test_child_status_must_pass(receipt):
    p=receipt/'acceptance.json';r=json.loads(p.read_text());r['status']='failed';p.write_text(json.dumps(r));assert check(receipt)

def test_unsafe_child_symlink_rejected(receipt,tmp_path):
    p=receipt/'tests/tests.json';s=p.read_text();p.unlink();external=tmp_path/'private';external.write_text(s)
    try:p.symlink_to(external)
    except OSError:pytest.skip('Host disallows symlinks')
    assert check(receipt)

def test_malformed_child_json_rejected(receipt):
    (receipt/'tests/tests.json').write_text('null');assert check(receipt)
