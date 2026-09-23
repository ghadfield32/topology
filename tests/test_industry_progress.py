from datetime import date
import json
import pytest
from shape_lab import industry_progress as ip

def test_empty():
    log=ip.new_log(); assert len(log['cases'])==8
    assert all(ip.status(log,k)=='not_started' for k in log['cases'])

def test_record_roundtrip(tmp_path):
    (tmp_path/'answer.md').write_text('my explanation')
    log=ip.new_log()
    ip.record(log,'wine','practice',100,'answer.md',tmp_path,date(2026,9,20))
    assert ip.status(log,'wine')=='practicing'
    ip.record(log,'wine','assessment',90,'answer.md',tmp_path,date(2026,9,21),True,True)
    assert ip.status(log,'wine')=='demonstrated'
    ip.record(log,'wine','recall',90,'answer.md',tmp_path,date(2026,9,28),True,True)
    assert ip.status(log,'wine')=='retained'
    ip.write_log(log,tmp_path/'log.json')
    assert ip.read_log(tmp_path/'log.json')==log
    assert ip.verify_evidence(log,tmp_path)[0]['status']=='unchanged'
    (tmp_path/'answer.md').write_text('edited')
    assert ip.verify_evidence(log,tmp_path)[0]['status']=='changed'

def test_missing_and_escape(tmp_path):
    log=ip.new_log()
    with pytest.raises(ValueError):ip.record(log,'wine','practice',90,'../x',tmp_path,date.today())
    (tmp_path/'a.md').write_text('hi')
    with pytest.raises(ValueError):ip.record(log,'unknown','practice',90,'a.md',tmp_path,date.today())
    ip.record(log,'wine','practice',90,'a.md',tmp_path,date.today())
    (tmp_path/'a.md').unlink()
    assert ip.verify_evidence(log,tmp_path)[0]['status']=='missing'

def test_refuse_bad_log(tmp_path):
    log=ip.new_log();del log['cases']['wine'];p=tmp_path/'log.json';p.write_text(json.dumps(log))
    with pytest.raises(ValueError):ip.read_log(p)

def test_date_and_score(tmp_path):
    (tmp_path/'a.md').write_text('hi');log=ip.new_log()
    with pytest.raises(ValueError):ip.record(log,'wine','practice',float('nan'),'a.md',tmp_path,date.today())
    ip.record(log,'wine','practice',10,'a.md',tmp_path,date(2026,9,20))
    with pytest.raises(ValueError):ip.record(log,'wine','practice',10,'a.md',tmp_path,date(2026,9,19))

def test_copied_solution_not_mastery(tmp_path):
    (tmp_path/'a.md').write_text('copied');log=ip.new_log()
    ip.record(log,'wine','assessment',100,'a.md',tmp_path,date.today(),False,True)
    assert ip.status(log,'wine')=='practicing'

def test_init_never_overwrites(tmp_path):
    p=tmp_path/'log.json';ip.initialize(p)
    with pytest.raises(FileExistsError):ip.initialize(p)

def test_malformed_attempt_and_path(tmp_path):
    log=ip.new_log();log['cases']['wine']['attempts']=[{'date':'wrong'}]
    p=tmp_path/'log.json';p.write_text(json.dumps(log))
    with pytest.raises(ValueError):ip.read_log(p)
