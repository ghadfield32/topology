from copy import deepcopy
from datetime import date
import pytest
from shape_lab.learning import new_log, migrate_v2_to_v3, record, read_log, write_log, stage_status, due_stages


def test_migration_preserves_all_attempts_without_mutating_original(tmp_path):
    old=new_log();p=tmp_path/'proof.md';p.write_text('Attempt, not certification.')
    record(old,1,'assessment',90,'proof.md',tmp_path,date(2026,9,20),True,True)
    before=deepcopy(old);new=migrate_v2_to_v3(old)
    assert old==before and new['schema_version']==3 and len(new['stages'])==21
    for n in range(13):assert new['stages'][f'{n:02d}']==old['stages'][f'{n:02d}']
    assert all(stage_status(new,n)=='not_started' for n in range(13,21))
    path=tmp_path/'new.json';write_log(new,path);assert read_log(path)==new


def test_bridge_evidence_is_recordable_and_due(tmp_path):
    log=new_log(stage_count=21);(tmp_path/'work.md').write_text('Work')
    record(log,20,'assessment',85,'work.md',tmp_path,date(2026,9,20),True,True)
    assert stage_status(log,20)=='demonstrated' and due_stages(log,date(2026,9,21))==[20]
    with pytest.raises(ValueError):record(log,21,'assessment',90,'work.md',tmp_path,date(2026,9,20),True,True)
