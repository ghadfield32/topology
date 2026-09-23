"""Honest environment and artifact checks for a source-based learning repository."""
from __future__ import annotations
import hashlib
import importlib.metadata as md
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any
from .course import load_catalog, inside

CORE=['packaging','jupyterlab','numpy','scipy','pandas','matplotlib','scikit-learn','nbclient','nbformat','ipykernel','pytest','mistune','beautifulsoup4']
PROFILES={'core':CORE,'physics':CORE+['torch'],'full':CORE+['torch','ripser','gudhi']}
EXTRAS={'core':['notebooks','test','reader'], 'physics':['notebooks','test','reader','physics'],
        'full':['notebooks','test','reader','physics','crosscheck']}

def required_distributions(profile: str) -> list[str]:
    if profile not in PROFILES:raise ValueError('Choose core, physics, or full.')
    return list(PROFILES[profile])

def environment_status(root: Path, profile: str='core') -> dict[str,Any]:
    """Check declared direct versions, not just distribution presence.

    This is not a transitive dependency solver, clean-install record, vulnerability
    audit, or proof that an optional backend behaves correctly.
    """
    import tomllib
    import platform
    from packaging.requirements import Requirement
    from packaging.specifiers import SpecifierSet
    from packaging.utils import canonicalize_name
    project=tomllib.loads((root/'pyproject.toml').read_text(encoding='utf-8'))['project']
    declared=list(project.get('dependencies',[]))
    for extra in EXTRAS[profile]:declared.extend(project.get('optional-dependencies',{}).get(extra,[]))
    requirements={}
    for text in declared:
        req=Requirement(text)
        if req.marker is None or req.marker.evaluate():requirements[canonicalize_name(req.name)]=req
    versions={};incompatible=[]
    for name in required_distributions(profile):
        try:versions[name]=md.version(name)
        except md.PackageNotFoundError:versions[name]=None
        req=requirements.get(canonicalize_name(name))
        if versions[name] is not None and req is not None and versions[name] not in req.specifier:
            incompatible.append({'distribution':name,'installed':versions[name],'required':str(req.specifier)})
    python_ok=platform.python_version() in SpecifierSet(project['requires-python'])
    missing=[n for n,v in versions.items() if v is None]
    return {'profile':profile,'python':sys.version.split()[0],'interpreter':sys.executable,
            'distributions':versions,'missing':missing,'incompatible':incompatible,
            'python_compatible':python_ok,'compatible':not missing and not incompatible and python_ok,
            'uv':shutil.which('uv'),'docker_cli':shutil.which('docker'),
            'kubectl_cli':shutil.which('kubectl'),'kind_cli':shutil.which('kind'),'kubernetes_runtime_validated':False,
            'lockfile_present':(root/'uv.lock').is_file(),'fresh_install_validated':False,
            'notice':'Declared direct-package and Python compatibility only; not clean sync, a full dependency audit, or deployment evidence.'}

def verify_manifest(root: Path, manifest: str='MANIFEST.sha256') -> dict:
    file=root/manifest
    if not file.is_file():return {'status':'missing','verified':0,'errors':[manifest]}
    count=0;errors=[]
    for line in file.read_text(encoding='utf-8').splitlines():
        if not line.strip():continue
        expected,rel=line.split('  ',1)
        p=inside(root,rel)
        if not p.is_file():errors.append(f'Missing: {rel}');continue
        digest=hashlib.sha256(p.read_bytes()).hexdigest()
        if digest!=expected:errors.append(f'Changed: {rel}')
        count+=1
    return {'status':'passed' if not errors else 'failed','verified':count,'errors':errors,
            'scope':'Listed delivered files only; intended edits change this archive-level check.'}

def validate_course(root: Path, profile: str='core') -> dict:
    c=load_catalog(root);env=environment_status(root,profile)
    missing=[p for p in c['reference_notebooks'] if not inside(root,p).is_file()]
    registry=json.loads((root/'curriculum/experiments.json').read_text(encoding='utf-8'))
    for e in registry['experiments']:
        for key in ['notebook','lesson','learner','answers']:
            if not inside(root,e[key]).is_file():missing.append(e[key])
    return {'status':'passed' if not missing and env['compatible'] else 'failed',
            'course_stages':len(c['stages']),'reference_notebooks':len(c['reference_notebooks']),
            'experiments':len(registry['experiments']),'missing_paths':missing,'environment':env,
            'learner_assessment':'not_assessed','scope':'Course structure and selected installed distributions, not Docker or a fresh install.'}

def run_tests(root: Path, output: Path, profile: str='core') -> dict:
    from .course import prepare_destination
    out=prepare_destination(root,output)
    env=environment_status(root,profile)
    result={'profile':profile,'environment':env}
    if not env['compatible']:
        result.update(status='blocked',reason='Required profile distributions or Python are missing/incompatible.',returncode=2)
    else:
        cmd=[sys.executable,'-m','pytest','-q','-ra','--junitxml='+str(out/'junit.xml')]
        with (out/'pytest.log').open('w',encoding='utf-8') as stream:
            p=subprocess.run(cmd,cwd=root,stdout=stream,stderr=subprocess.STDOUT)
        result.update(status='passed' if p.returncode==0 else 'failed',returncode=p.returncode,command=cmd)
        if (out/'junit.xml').exists():
            import xml.etree.ElementTree as ET
            tree=ET.parse(out/'junit.xml')
            cases=tree.findall('.//testcase')
            result['counts']={'total':len(cases),'skipped':sum(c.find('skipped') is not None for c in cases),
                             'failures':sum(c.find('failure') is not None for c in cases),'errors':sum(c.find('error') is not None for c in cases)}
            result['counts']['passed']=result['counts']['total']-sum(result['counts'][k] for k in ['skipped','failures','errors'])
            if not cases or result['counts']['failures'] or result['counts']['errors']:
                result.update(status='failed',returncode=2,reason='Missing passing testcases or failing JUnit evidence.')
            if profile=='full' and result['counts']['skipped']:
                result.update(status='failed',returncode=2,reason='Full verification does not accept skipped checks.')
        else:
            result.update(status='failed',returncode=2,reason='pytest did not write its required JUnit evidence.')
    (out/'tests.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result
