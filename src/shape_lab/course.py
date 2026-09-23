"""Single course catalog and isolated, dependency-aware notebook execution.

No command here changes a learner assessment. Saved reference outputs are not
inputs to a clean run; required predecessor notebooks are executed explicitly.
"""
from __future__ import annotations
from pathlib import Path
from collections.abc import Iterable, Mapping
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import time

# Only relationships that consume generated predecessor artifacts belong here.
DEPENDENCIES={
    'representations/notebooks/r05.ipynb':['representations/notebooks/r04.ipynb'],
    'notebooks/12_lab.ipynb':['notebooks/11_lab.ipynb'],
    'consolidation/12_lab.ipynb':['notebooks/12_lab.ipynb'],
    'practice/answers/12_practice.ipynb':['notebooks/12_lab.ipynb'],
    'notebooks/20_lab.ipynb':[f'notebooks/{n:02}_lab.ipynb' for n in range(13,20)],
    'consolidation/20_lab.ipynb':[f'consolidation/{n:02}_lab.ipynb' for n in range(20)],
    'physics/notebooks/30_lab.ipynb':[f'physics/notebooks/{n}_lab.ipynb' for n in range(21,30)],
}

def inside(root: Path, relative: str) -> Path:
    """Resolve an existing or planned local file without allowing root escape."""
    root=Path(root).resolve();p=Path(relative)
    if p.is_absolute() or '..' in p.parts:raise ValueError('Path must stay inside the course.')
    result=(root/p).resolve()
    if not result.is_relative_to(root):raise ValueError('Path escapes the course through a link.')
    return result

def load_catalog(root: Path) -> dict:
    obj=json.loads(inside(root,'curriculum/catalog.json').read_text())
    stages=obj['stages'];ids=[s['id'] for s in stages]
    if ids!=[f'{n:02}' for n in range(31)]:raise ValueError('Expected unique ordered stages 00–30.')
    if len({s['lesson'] for s in stages})!=31:raise ValueError('Repeated required lesson.')
    for s in stages:
        if any(d not in ids for d in s['prerequisites']):raise ValueError('Unknown prerequisite.')
        for k in ('lesson','reference_lab','learner','answers'):
            if not inside(root,s[k]).is_file():raise ValueError(f'Missing {k}: {s[k]}')
    topological_order(ids,{s['id']:s['prerequisites'] for s in stages})
    refs=obj['reference_notebooks']
    if len(refs)!=len(set(refs)):raise ValueError('Repeated reference notebook.')
    return obj

def stage_plan(root: Path, stage: str|int) -> dict:
    try:key=f'{int(stage):02}'
    except (TypeError,ValueError):raise ValueError('Use a stage number from 00 to 30.') from None
    for s in load_catalog(root)['stages']:
        if s['id']==key:return s
    raise ValueError('Use a stage number from 00 to 30.')

def topological_order(targets: Iterable[str], dependencies: Mapping[str,list[str]]) -> list[str]:
    state={};result=[]
    def visit(p):
        if state.get(p)==1:raise ValueError(f'Dependency cycle at {p}')
        if state.get(p)==2:return
        state[p]=1
        for d in dependencies.get(p,[]):visit(d)
        state[p]=2;result.append(p)
    for p in targets:visit(p)
    return result

def execution_order(root: Path, targets: Iterable[str]) -> list[str]:
    allowed=set(load_catalog(root)['reference_notebooks']);targets=list(targets)
    if not targets or any(p not in allowed for p in targets):
        raise ValueError('Only cataloged reference notebooks can run through this command.')
    result=topological_order(targets,DEPENDENCIES)
    for p in result:
        if p not in allowed or not inside(root,p).is_file():raise ValueError(f'Missing reference notebook: {p}')
    return result

def prepare_destination(root: Path, destination: Path) -> Path:
    root=Path(root).resolve();destination=Path(destination).resolve()
    if destination.is_relative_to(root) and not destination.is_relative_to(root/'my_work'):
        raise ValueError('Put outputs under my_work or outside the course; source files are protected.')
    if destination.exists():raise FileExistsError('Output already exists; choose a new run directory.')
    destination.mkdir(parents=True,exist_ok=False)
    return destination

def doctor(root: Path) -> dict:
    import platform
    required=['numpy','scipy','pandas','matplotlib','scikit-learn','nbclient','nbformat','ipykernel']
    def version(name):
        try:return importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:return None
    return {'python':platform.python_version(),'platform':platform.platform(),
            'required':{p:version(p) for p in required},
            'optional':{p:{'version':version(p),'status':'available_not_tested' if version(p) else 'not_installed_not_tested'} for p in ['ripser','gudhi','torch']},
            'stages':len(load_catalog(root)['stages']),'network_calls':0,
            'learner_assessment':'not_assessed'}

def copy_inputs(root: Path, target: Path) -> None:
    """Exclude reference result folders, caches, rendered pages and learner work."""
    excluded={'.venv','venv','node_modules','site','reader','.git','__pycache__','.pytest_cache','.ipynb_checkpoints','my_work','reports','processed','dist','build','.uv-cache','.ruff_cache','.mypy_cache'}
    def ignore(directory,names):
        blocked=[]
        for n in names:
            if (n in excluded or n.endswith(('.egg-info','.pem','.key')) or n.startswith('COMPLETE_COURSE')
                or (n.startswith('.env') and n != '.env.example')):
                blocked.append(n);continue
            item=Path(directory)/n
            if item.is_symlink() and not item.resolve().is_relative_to(Path(root).resolve()):
                raise ValueError(f'External symlink is not a declared course input: {item}')
        return blocked
    shutil.copytree(root,target,ignore=ignore)
    # Writable execution belongs to this disposable copy, never the source.
    # copytree preserves source modes, including legitimately read-only inputs.
    import stat
    for item in [target,*target.rglob('*')]:
        permissions=stat.S_IMODE(item.stat().st_mode)
        item.chmod(permissions | (0o700 if item.is_dir() else 0o600))
    (target/'reports').mkdir(exist_ok=True)
    (target/'my_work').mkdir(exist_ok=True)
    (target/'physics/reports').mkdir(parents=True,exist_ok=True)

def _execute_one(workspace: str, notebook: str, destination: str, timeout: int) -> dict:
    """Worker creates a new kernel and always records actual executed cells."""
    import nbformat
    from nbclient import NotebookClient
    from jupyter_client import AsyncKernelManager
    from jupyter_client.kernelspec import KernelSpecManager
    from .runtime import write_kernel_spec, validate_kernel_provenance, parse_probe, PROBE_TAG, PROBE_SOURCE
    start=time.perf_counter();work=Path(workspace);dest=Path(destination)
    path=inside(work,notebook);b=nbformat.read(path,as_version=4)
    b.cells=[c for c in b.cells if PROBE_TAG not in c.get('metadata',{}).get('tags',[])]
    for c in b.cells:
        if c.cell_type=='code':c.outputs=[];c.execution_count=None
    source_code_cells=sum(c.cell_type=='code' for c in b.cells)
    b.cells.insert(0,nbformat.v4.new_code_cell(PROBE_SOURCE,metadata={'tags':[PROBE_TAG]}))
    source_hash=hashlib.sha256(path.read_bytes()).hexdigest()
    record={'path':notebook,'source_sha256':source_hash,'source_code_cells':source_code_cells,'runtime_probe_cells':1}
    try:
        with tempfile.TemporaryDirectory(prefix='shape-kernels-') as kernel_dir:
            write_kernel_spec(Path(kernel_dir),sys.executable)
            manager=AsyncKernelManager(kernel_name='shape-course-v10',
                kernel_spec_manager=KernelSpecManager(kernel_dirs=[kernel_dir]))
            NotebookClient(b,timeout=timeout,km=manager,kernel_name='shape-course-v10',allow_errors=False,
                           resources={'metadata':{'path':str(work)}}).execute(cleanup_kc=True)
        record['kernel']=validate_kernel_provenance(parse_probe(b.cells[0]),sys.executable,work)
        errors=[o for c in b.cells if c.cell_type=='code' for o in c.outputs if o.output_type=='error']
        if errors:raise RuntimeError('An error output survived execution.')
        record.update(status='passed',code_cells=sum(c.cell_type=='code' for c in b.cells),
                      png_outputs=sum('image/png' in o.get('data',{}) for c in b.cells if c.cell_type=='code' for o in c.outputs))
    except Exception as exc:
        record.update(status='failed',error=f'{type(exc).__name__}: {exc}')
    out=dest/'executed'/notebook;out.parent.mkdir(parents=True,exist_ok=True);nbformat.write(b,out)
    record['seconds']=round(time.perf_counter()-start,3)
    return record

def run_references(root: Path, targets: Iterable[str], destination: Path, jobs: int=2, timeout: int=300) -> dict:
    """Run the dependency closure once in a clean workspace; no prior reports copied.

    Individual notebooks use fresh kernels. Jobs with unmet/failed predecessors
    do not run. The returned manifest distinguishes failures from blocked work.
    """
    root=Path(root).resolve()
    from .runtime import fingerprint_inputs,environment_record
    before=fingerprint_inputs(root)
    if not 1<=jobs<=4 or timeout<1:raise ValueError('Use 1–4 jobs and a positive cell timeout.')
    order=execution_order(root,targets);dest=prepare_destination(root,destination)
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        os.environ[name]='1'
    status={'mode':'fresh_input_workspace_and_fresh_kernels','required_prior_reports_copied':False,
            'learner_assessment':'not_assessed','order':order,'records':[],'environment':doctor(root),
            'runtime_environment':environment_record(),'input_sha256':before,
            'kernel_policy':'active sys.executable plus runtime probe; isolated copied source'}
    def save():
        (dest/'execution.json').write_text(json.dumps(status,indent=2)+'\n')
    save()
    with tempfile.TemporaryDirectory(prefix='shape-course-') as temp:
        work=Path(temp)/'course';copy_inputs(root,work)
        # Jupyter kernels inherit a path to the copied code, never the build tree.
        old_pythonpath=os.environ.get('PYTHONPATH')
        os.environ['PYTHONPATH']=str(work/'src')
        pending=set(order);finished={};running={}
        try:
            with ProcessPoolExecutor(max_workers=jobs) as pool:
                while pending or running:
                    for p in order:
                        if p not in pending:continue
                        deps=DEPENDENCIES.get(p,[])
                        if any(d in finished and finished[d]!='passed' for d in deps):
                            pending.remove(p);finished[p]='blocked'
                            status['records'].append({'path':p,'status':'blocked','reason':'A required predecessor did not pass.'});save()
                        elif len(running)<jobs and all(finished.get(d)=='passed' for d in deps):
                            pending.remove(p)
                            running[pool.submit(_execute_one,str(work),p,str(dest),timeout)]=p
                    if not running:
                        if pending:raise RuntimeError('No runnable notebook remains; inspect dependency graph.')
                        break
                    done,_=wait(running,return_when=FIRST_COMPLETED)
                    for future in done:
                        p=running.pop(future)
                        try:r=future.result()
                        except Exception as e:r={'path':p,'status':'failed','error':repr(e)}
                        finished[p]=r['status'];status['records'].append(r);save()
                        print(f"{len(finished)}/{len(order)} {r['status']} {p}",flush=True)
            for folder in ['reports','physics/reports','industry/reports']:
                src=work/folder
                if src.exists():shutil.copytree(src,dest/'artifacts'/folder,dirs_exist_ok=True)
        finally:
            if old_pythonpath is None:os.environ.pop('PYTHONPATH',None)
            else:os.environ['PYTHONPATH']=old_pythonpath
    status['passed']=sum(r['status']=='passed' for r in status['records'])
    status['failed']=sum(r['status']!='passed' for r in status['records'])
    after=fingerprint_inputs(root)
    status['source_inputs_unchanged']=(after==before)
    status['changed_source_inputs']=[p for p in sorted(set(before)|set(after)) if before.get(p)!=after.get(p)]
    if after!=before:status['failed']+=1
    save();return status
