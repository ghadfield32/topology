"""Small, inspectable provenance helpers. No downloads or global kernel registration."""
from __future__ import annotations
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import sys

PROBE_TAG = 'shape-runtime-provenance-v10'
PROBE_PREFIX = 'SHAPE_RUNTIME_PROVENANCE='
PROBE_SOURCE = '''# Runtime evidence: this cell checks the environment actually used by the kernel.
import sys as _shape_sys, json as _shape_json, importlib.util as _shape_util
print("SHAPE_RUNTIME_PROVENANCE=" + _shape_json.dumps({
    "python_executable": _shape_sys.executable,
    "python_version": _shape_sys.version.split()[0],
    "shape_lab_origin": _shape_util.find_spec("shape_lab").origin
}))
del _shape_sys, _shape_json, _shape_util
'''


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def write_kernel_spec(parent: Path, executable: str) -> Path:
    directory=Path(parent)/'shape-course-v10'
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'kernel.json').write_text(json.dumps({
        'argv':[executable,'-m','ipykernel_launcher','-f','{connection_file}'],
        'display_name':'Listening to Shape — active environment', 'language':'python'
    },indent=2)+'\n',encoding='utf-8')
    return directory


def validate_kernel_provenance(record: dict, executable: str, workspace: Path) -> dict:
    # Do not resolve the interpreter symlink: two venvs can share one binary but
    # have different site-packages. The invoked interpreter path is evidence.
    if record.get('python_executable') != executable:
        raise ValueError('Kernel interpreter differs from the requested active interpreter.')
    origin=Path(record.get('shape_lab_origin','')).resolve()
    if not origin.is_relative_to((Path(workspace)/'src').resolve()):
        raise ValueError('Kernel did not import the isolated copied source.')
    return record


def parse_probe(cell: dict) -> dict:
    text=''.join(o.get('text','') for o in cell.get('outputs',[]) if o.get('output_type')=='stream')
    lines=[x[len(PROBE_PREFIX):] for x in text.splitlines() if x.startswith(PROBE_PREFIX)]
    if len(lines)!=1:raise ValueError('Kernel provenance probe did not produce exactly one record.')
    return json.loads(lines[0])


def fingerprint_inputs(root: Path) -> dict[str,str]:
    """Hash executable source, reference inputs and learner records, not generated output."""
    root=Path(root).resolve();paths=[]
    trees=['representations','deploy','src','tests','scripts','tools','data','progress','curriculum','notebooks','consolidation','practice',
           'physics/notebooks','physics/answers','physics/data','industry/data','industry/notebooks',
           'industry/answers','applications_v7','methods_v7','sports_v8/data',
           'sports_v8/notebooks','sports_v8/solutions','sports_v9/data',
           'sports_v9/notebooks','sports_v9/solutions']
    for folder in trees:
        p=root/folder
        if p.exists():paths.extend(p.rglob('*'))
    paths.extend(root/x for x in ['pyproject.toml','uv.lock','.python-version','course.py','requirements/constraints-observed.txt'])
    catalog=root/'curriculum/catalog.json'
    if catalog.is_file():
        for name in json.loads(catalog.read_text())['reference_notebooks']:
            if Path(name).is_absolute() or '..' in Path(name).parts:raise ValueError('Unsafe reference path in catalog.')
            paths.append(root/name)
    result={}
    for p in sorted(set(paths)):
        if not p.is_file() or {'__pycache__','.ipynb_checkpoints','.pytest_cache','processed'} & set(p.parts):continue
        if p.suffix in {'.pyc','.pyo'}:continue
        if not p.resolve().is_relative_to(root):raise ValueError('Input symlink escapes the course.')
        result[p.relative_to(root).as_posix()]=sha256(p)
    return result


def environment_record() -> dict:
    packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions() if d.metadata.get('Name')}
    return {'python':platform.python_version(),'executable':sys.executable,
            'platform':platform.platform(),'architecture':platform.machine(),
            'prefix':sys.prefix,'base_prefix':sys.base_prefix,
            'packages':dict(sorted(packages.items(),key=lambda x:x[0].lower()))}

def write_reuse_sites(site_directory: Path, active_sites: list[str]) -> Path:
    """Explicit diagnostic inheritance, including a caller that itself uses a venv.

    This is not used by ordinary uv setup or by Docker. A sidecar makes the
    dependency reuse inspectable; it is not a resolver lock or fresh install.
    """
    directory=Path(site_directory);directory.mkdir(parents=True,exist_ok=True)
    paths=[str(Path(p).resolve()) for p in active_sites]
    target=directory/'00_shape_explicit_dependency_reuse.pth'
    target.write_text('import sys; sys.path[0:0] = '+repr(paths)+'\n',encoding='utf-8')
    (directory/'shape_reuse_installed.json').write_text(json.dumps({
        'independent_install':False,'source_site_paths':paths,
        'purpose':'Explicit --reuse-installed diagnostic only'
    },indent=2)+'\n',encoding='utf-8')
    return target


def assert_clean_setup_target(venv: Path) -> None:
    """Refuse to re-label an inherited environment as independently installed."""
    venv=Path(venv)
    if any(venv.glob('**/shape_reuse_installed.json')):
        raise ValueError('Existing .venv is a diagnostic inherited environment. Use a fresh extraction; no automatic deletion is performed.')
    cfg=venv/'pyvenv.cfg'
    if cfg.exists():
        fields=dict(line.split('=',1) for line in cfg.read_text().splitlines() if '=' in line)
        if any(k.strip()=='include-system-site-packages' and v.strip().lower()=='true' for k,v in fields.items()):
            raise ValueError('Existing .venv inherits system site-packages; use a fresh independent environment.')


def initialize_progress(root: Path) -> list[str]:
    """Copy blank tracked templates only where local learner records are missing."""
    root=Path(root);created=[]
    for source in sorted((root/'progress/templates').glob('*.json')):
        target=root/'progress'/source.name
        if target.exists():continue
        # Exclusive create protects a concurrent learner update as well.
        try:
            with target.open('x',encoding='utf-8') as out:out.write(source.read_text(encoding='utf-8'))
        except FileExistsError:continue
        created.append(target.relative_to(root).as_posix())
    return created
