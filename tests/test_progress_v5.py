from copy import deepcopy
from datetime import date
from pathlib import Path
import subprocess,sys,json
import pytest
from shape_lab import learning as L
ROOT=Path(__file__).resolve().parents[1]

def test_fresh_31_stage_log():
    log=L.new_log(31)
    assert log['schema_version']==5 and log['course_version']=='5.0.0'
    assert len(log['stages'])==31
    assert all(L.stage_status(log,n)=='not_started' for n in range(31))

def test_migration_preserves_attempts_and_does_not_mutate(tmp_path):
    old=L.new_log(21);(tmp_path/'work.md').write_text('A real answer.')
    L.record(old,20,'assessment',90,'work.md',tmp_path,date(2026,9,20),True,True)
    before=deepcopy(old);new=L.migrate_to_v5(old)
    assert old==before and new['stages']['20']==old['stages']['20']
    assert all(new['stages'][f'{i:02d}']['attempts']==[] for i in range(21,31))
    assert L.stage_status(new,20)=='demonstrated'

def test_v5_read_roundtrip(tmp_path):
    log=L.new_log(31);p=tmp_path/'log.json';L.write_log(log,p)
    assert L.read_log(p)==log

def test_reject_repeated_migration():
    with pytest.raises(ValueError):L.migrate_to_v5(L.new_log(31))

def test_legacy_13_can_migrate():
    new=L.migrate_to_v5(L.new_log(13))
    assert len(new['stages'])==31
