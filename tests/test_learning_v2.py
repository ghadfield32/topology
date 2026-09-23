from datetime import date
from pathlib import Path
import pytest
from shape_lab.learning import new_log, record, stage_status, due_stages, write_log, read_log


def evidence(tmp_path):
    p=tmp_path/'answers.md';p.write_text('My explanation and results.');return 'answers.md'


def test_new_log_has_no_learner_achievements():
    log=new_log()
    assert len(log['stages'])==13
    assert all(stage_status(log,n)=='not_started' for n in range(13))
    assert due_stages(log,date(2026,9,20))==[]


def test_code_execution_is_not_mastery(tmp_path):
    log=new_log()
    record(log,0,'practice',100,evidence(tmp_path),tmp_path,date(2026,9,20),True,True)
    assert stage_status(log,0)=='practicing'


def test_assessment_requires_independence_and_critical_clear(tmp_path):
    for independent,clear in [(False,True),(True,False)]:
        log=new_log()
        record(log,0,'assessment',100,evidence(tmp_path),tmp_path,date(2026,9,20),independent,clear)
        assert stage_status(log,0)=='practicing'


def test_assessment_then_delayed_recall(tmp_path):
    log=new_log();e=evidence(tmp_path)
    record(log,0,'assessment',90,e,tmp_path,date(2026,9,20),True,True)
    assert stage_status(log,0)=='demonstrated'
    assert due_stages(log,date(2026,9,20))==[]
    assert due_stages(log,date(2026,9,21))==[0]
    record(log,0,'recall',90,e,tmp_path,date(2026,9,21),True,True)
    assert stage_status(log,0)=='demonstrated'
    record(log,0,'recall',90,e,tmp_path,date(2026,9,27),True,True)
    assert stage_status(log,0)=='retained'


def test_failed_recall_requires_review(tmp_path):
    log=new_log();e=evidence(tmp_path)
    record(log,0,'assessment',90,e,tmp_path,date(2026,9,20),True,True)
    record(log,0,'recall',40,e,tmp_path,date(2026,9,27),True,True)
    assert stage_status(log,0)=='needs_review'


def test_recall_without_assessment_does_not_certify_mastery(tmp_path):
    log=new_log();e=evidence(tmp_path)
    record(log,0,'recall',100,e,tmp_path,date(2026,9,20),True,True)
    assert stage_status(log,0)=='practicing'


@pytest.mark.parametrize('n,kind,score',[(13,'practice',50),(-1,'assessment',90),(0,'other',90),(0,'practice',101),(0,'practice',-1),(0,'practice',float('nan'))])
def test_invalid_attempt_rejected(n,kind,score,tmp_path):
    with pytest.raises(ValueError):record(new_log(),n,kind,score,evidence(tmp_path),tmp_path,date(2026,9,20),True,True)


def test_evidence_must_exist_inside_workspace(tmp_path):
    with pytest.raises(ValueError):record(new_log(),0,'practice',10,'missing.md',tmp_path,date(2026,9,20),False,False)
    with pytest.raises(ValueError):record(new_log(),0,'practice',10,'../elsewhere',tmp_path,date(2026,9,20),False,False)


def test_dates_cannot_reorder_history(tmp_path):
    log=new_log();e=evidence(tmp_path)
    record(log,0,'practice',20,e,tmp_path,date(2026,9,20),False,False)
    with pytest.raises(ValueError):record(log,0,'practice',20,e,tmp_path,date(2026,9,19),False,False)


def test_log_roundtrip_and_version_validation(tmp_path):
    log=new_log();p=tmp_path/'state.json';write_log(log,p)
    assert read_log(p)==log
    p.write_text('{"schema_version": 9}')
    with pytest.raises(ValueError):read_log(p)
