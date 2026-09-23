from pathlib import Path
import json
import pytest
ROOT=Path(__file__).resolve().parents[1]
def test_canonical_catalog_is_present():
    assert (ROOT/'curriculum/catalog.json').is_file(), 'One canonical course manifest is required.'
def test_course_api_is_present():
    assert (ROOT/'src/shape_lab/course.py').is_file(), 'Safe isolated lesson execution is required.'

def test_catalog_primary_lessons_unique():
    from shape_lab.course import load_catalog
    c=load_catalog(ROOT)
    assert [s['id'] for s in c['stages']]==[f'{i:02}' for i in range(31)]
    assert len({s['lesson'] for s in c['stages']})==31
    assert len(c['reference_notebooks'])==len(set(c['reference_notebooks']))==133

@pytest.mark.parametrize('p',['../elsewhere','/tmp/outside','src/../../outside'])
def test_escape_rejected(p):
    from shape_lab.course import inside
    with pytest.raises(ValueError):inside(ROOT,p)

def test_stage_lookup_rejects_unknown():
    from shape_lab.course import stage_plan
    with pytest.raises(ValueError):stage_plan(ROOT,'31')

def test_prerequisites_are_explicit():
    from shape_lab.course import execution_order
    order=execution_order(ROOT,['notebooks/20_lab.ipynb'])
    assert all(f'notebooks/{i:02}_lab.ipynb' in order for i in range(13,20))
    assert order[-1]=='notebooks/20_lab.ipynb'

def test_cycle_rejected():
    from shape_lab.course import topological_order
    with pytest.raises(ValueError,match='cycle'):topological_order(['a'],{'a':['b'],'b':['a']})

def test_existing_destination_rejected(tmp_path):
    from shape_lab.course import prepare_destination
    d=tmp_path/'run';d.mkdir()
    with pytest.raises(FileExistsError):prepare_destination(ROOT,d)

def test_source_destination_rejected():
    from shape_lab.course import prepare_destination
    with pytest.raises(ValueError):prepare_destination(ROOT,ROOT/'lessons'/'newrun')

def test_doctor_reports_optional_missing_without_pass():
    from shape_lab.course import doctor
    d=doctor(ROOT)
    assert d['network_calls']==0
    assert {'ripser','gudhi'} <= set(d['optional'])
    assert d['learner_assessment']=='not_assessed'

def test_reference_not_learner():
    from shape_lab.course import execution_order
    with pytest.raises(ValueError):execution_order(ROOT,['practice/learner/00_practice.ipynb'])

def test_acb_exact_blob():
    from shape_lab.acb import load_matches
    m=load_matches(ROOT/'sports_v9/data')
    assert len(m)==10 and m[0]['id']==114243 and m[-1]['id']==191313

def test_acb_tamper_rejected(tmp_path):
    from shape_lab.acb import load_matches
    import shutil
    for p in (ROOT/'sports_v9/data').glob('*.json'):shutil.copyfile(p,tmp_path/p.name)
    p=tmp_path/'matches.json';p.write_text(p.read_text().replace('83','82',1))
    with pytest.raises(ValueError,match='hash'):load_matches(tmp_path)

def test_acb_chronological_split():
    from shape_lab.acb import load_matches,chronological_split
    a=load_matches(ROOT/'sports_v9/data');s=chronological_split(a)
    assert [sum(v==name for v in s.values()) for name in ['fit','validation','test']]==[6,2,2]
    assert s[191313]=='test'

@pytest.mark.parametrize('n',[0,1,4])
def test_split_rejects_too_few_games(n):
    from shape_lab.acb import chronological_split,load_matches
    with pytest.raises(ValueError):chronological_split(load_matches(ROOT/'sports_v9/data')[:n])

def test_alias_resolution_and_cycle():
    from shape_lab.acb import canonical_id
    assert canonical_id(1,{1:2,2:3})==3
    assert canonical_id(8,{1:2})==8
    with pytest.raises(ValueError):canonical_id(1,{1:2,2:1})

def test_total_rows_not_double_counted():
    from shape_lab.acb import team_only_total
    rows=[{'team_name':'A','attempts':10},{'team_name':'B','attempts':5},{'team_name':'total','attempts':15}]
    assert team_only_total(rows,'attempts')==15

def test_nonfinite_counts_rejected():
    from shape_lab.acb import team_only_total
    with pytest.raises(ValueError):team_only_total([{'team_name':'A','attempts':float('nan')}],'attempts')

def test_canonical_reader_builder_exists():
    assert (ROOT/'scripts/build_reader_v9.py').is_file()

def test_acb_duplicate_and_tied_boundary_rejected():
    from shape_lab.acb import load_matches, chronological_split
    import copy
    m=load_matches(ROOT/'sports_v9/data')
    with pytest.raises(ValueError,match='Duplicate'):chronological_split(m+[m[0]])
    m=copy.deepcopy(m);m[6]['date_time']=m[5]['date_time']
    with pytest.raises(ValueError,match='Tied'):chronological_split(m)

def test_input_copy_excludes_saved_reports_and_work(tmp_path):
    from shape_lab.course import copy_inputs
    source=tmp_path/'source';source.mkdir()
    (source/'dataset.csv').write_text('x\n1\n')
    for d in ['reports','physics/reports','data/processed','my_work']:
        p=source/d;p.mkdir(parents=True,exist_ok=True);(p/'saved.txt').write_text('do not copy')
    copy_inputs(source,tmp_path/'copy')
    target=tmp_path/'copy'
    assert (target/'dataset.csv').read_text()=='x\n1\n'
    assert not list(target.rglob('saved.txt'))

def test_input_copy_does_not_copy_installed_virtual_environment(tmp_path):
    from shape_lab.course import copy_inputs
    source=tmp_path/'source';source.mkdir()
    for name in ['.venv','venv']:
        p=source/name/'lib';p.mkdir(parents=True);(p/'installed_dependency.txt').write_text('large installed environment')
    copy_inputs(source,tmp_path/'copy')
    assert not list((tmp_path/'copy').rglob('installed_dependency.txt'))

def test_reader_extra_contains_its_html_parser():
    import tomllib
    data=tomllib.loads((ROOT/'pyproject.toml').read_text())
    assert any(x.startswith('beautifulsoup4') for x in data['project']['optional-dependencies']['reader'])
