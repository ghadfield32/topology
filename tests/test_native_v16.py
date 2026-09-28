"""Acceptance contracts for the new native course, separate from learner mastery."""
from pathlib import Path
import importlib.util,json,pytest
ROOT=Path(__file__).resolve().parents[1]

def load():
    p=ROOT/'native_course.py'
    assert p.is_file(), 'native runner must exist, not just a design'
    spec=importlib.util.spec_from_file_location('native_course_v16',p)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def test_exact_inventory():
    m=load(); items=m.available_labs(ROOT)
    assert len(items)==57 and len({r['key'] for r in items})==57
    assert {'stage01','poux_bridge','r04','wine'}<= {r['key']for r in items}

def test_refuse_existing_output(tmp_path):
    m=load();p=tmp_path/'run';m.new_directory(p)
    sentinel=p/'work';sentinel.write_text('keep')
    with pytest.raises(FileExistsError):m.new_directory(p)
    assert sentinel.read_text()=='keep'

def test_compared_metrics_are_real():
    m=load();a={'x':[1.,2.],'n':2};b={'x':[1.,2.1],'n':2}
    assert not m.compare_values(a,b)['passed']
    assert not m.compare_values({'x':1},{})['passed']
    assert not m.compare_values({'x':True},{'x':1})['passed']
    assert m.compare_values(a,a)['passed']

def test_wrong_native_identity_rejected():
    m=load();base={'schema':'shape.native.v16','lab':'stage01','language':'go','status':'completed','metrics':{'rank':3},'inputs':{},'original_notebook_parity':'not_certified'}
    m.validate_result(base,'stage01','go')
    with pytest.raises(ValueError):m.validate_result(base,'stage02','go')
    with pytest.raises(ValueError):m.validate_result({**base,'metrics':{}},'stage01','go')
    with pytest.raises(ValueError):m.validate_result({**base,'metrics':{'implemented':True}},'stage01','go')

def test_required_registry_sources():
    m=load();r=json.loads((ROOT/'native/data_registry.json').read_text())
    paths={x['path']for x in r['files']}
    assert {'data/raw/digits.npz','data/stereo/left.png','sports_v8/data/spl_selected_frames.json','sports_v9/data/matches.json'}<=paths
    assert m.audit_registry(ROOT)['passed']

def test_no_native_python_delegation():
    for lang,extensions in [('go',['.go']),('rust',['.rs'])]:
        for p in (ROOT/'native'/lang).rglob('*'):
            if 'vendor' in p.parts or p.suffix not in extensions:continue
            text=p.read_text()
            assert 'exec.Command('not in text and 'std::process::Command'not in text

def test_core_catalog_preserved():
    x=json.loads((ROOT/'curriculum/catalog.json').read_text())
    assert len(x['stages'])==31

def test_every_unit_has_one_guide_and_three_challenges():
    m=load()
    for row in m.available_labs(ROOT):
        assert len(row['challenges']) == 3
        assert (ROOT/'native/guides/labs'/f"{row['key']}.md").is_file()
        assert (ROOT/row['lesson']).is_file()
        assert row['native_goal']

def test_prepare_is_editable_and_unassessed(tmp_path):
    m=load(); out=m.new_directory(tmp_path/'practice')
    m.prepare('stage01',out,ROOT)
    assert m.read_json(out/'study.json')['assessment']=='not_assessed'
    assert (out/'go/engine/math.go').is_file()
    assert (out/'rust/src/math.rs').is_file()
    assert (out/'rust/.cargo/config.toml').is_file()
    assert not (out/'rust/vendor').exists()
    marker=out/'rust/src/math.rs'
    old=marker.read_text();marker.write_text(old+'\n// private exercise\n')
    assert not (ROOT/'native/rust/src/math.rs').read_text().endswith('// private exercise\n')

def test_original_parity_gate_refuses(tmp_path):
    m=load();dest=tmp_path/'original'
    assert m.main(['verify','--require-original-parity','--output',str(dest)])==1
    assert m.read_json(dest/'failure.json')['status']=='failed'

def test_cache_reuse_keeps_first_compiler_record(tmp_path,monkeypatch):
    m=load();out=m.new_directory(tmp_path/'evidence');cache=tmp_path/'my_work/native_build/go';cache.mkdir(parents=True)
    exe=cache/('shape-go.exe' if m.os.name=='nt'else'shape-go');exe.write_bytes(b'fixture-binary')
    key={'source_sha256':'fixture-source','compiler':'fixture-go','platform':m.sys.platform}
    m.write_json(cache/'build.json',{'key':key,'binary_sha256':m.digest(exe)})
    first={'status':'compiled','exit_code':0,'scope':'test fixture'};m.write_json(out/'go_build.json',first)
    monkeypatch.setattr(m,'source_id',lambda lang,root:'fixture-source')
    monkeypatch.setattr(m.shutil,'which',lambda name:'fixture-go')
    monkeypatch.setattr(m,'command',lambda *args,**kwargs:{'stdout':'fixture-go'})
    assert m.build('go',out,root=tmp_path)==exe
    assert m.read_json(out/'go_build.json')==first
    assert m.read_json(out/'go_build_reuse.json')['status']=='verified_cache'
