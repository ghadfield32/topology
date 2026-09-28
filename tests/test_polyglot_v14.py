import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_polyglot_manifest_covers_all_course_labs():
    spec=json.loads((ROOT/'polyglot/specs/labs.json').read_text())
    catalog=json.loads((ROOT/'curriculum/catalog.json').read_text())
    experiments=json.loads((ROOT/'curriculum/experiments.json').read_text())
    assert len(spec['labs'])==len(catalog['stages'])+len(experiments['experiments'])+1==57
    keys=[x['key'] for x in spec['labs']]
    assert len(keys)==len(set(keys))
    assert 'poux_bridge' in keys

def test_each_polyglot_lab_has_spec_go_and_rust_sources():
    spec=json.loads((ROOT/'polyglot/specs/labs.json').read_text())
    import re
    for lab in spec['labs']:
        key=lab['key']; safe=re.sub(r'[^A-Za-z0-9_]','_',key)
        assert (ROOT/'polyglot/specs'/key/'README.md').is_file(), key
        assert (ROOT/'polyglot/go/labs'/f'{safe}.go').is_file(), key
        assert (ROOT/'polyglot/rust/src/labs'/f'{safe}.rs').is_file(), key

def test_go_build_evidence_contains_all_labs():
    report=json.loads((ROOT/'reports/v14/go_all_labs.json').read_text())
    assert report['count']==57
    assert set(report['labs'])=={x['key'] for x in json.loads((ROOT/'polyglot/specs/labs.json').read_text())['labs']}

def test_rust_sources_are_dependency_light_and_complete():
    cargo=(ROOT/'polyglot/rust/Cargo.toml').read_text()
    assert '[dependencies]' in cargo
    tail=cargo.split('[dependencies]',1)[1].strip()
    assert tail==''
    mod=(ROOT/'polyglot/rust/src/labs/mod.rs').read_text()
    assert 'all_registered' in mod
    assert 'poux_bridge' in mod

def test_polyglot_verifier_smokes_all_rust_labs_when_toolchain_exists():
    text = (ROOT / "tools/polyglot_verify.py").read_text(encoding="utf-8")
    assert "cargo,'run','--quiet','--bin','shape-rust','--','--list'" in text.replace('"', "'")
    assert "results['rust']['smoke']" in text
