"""Private project preparation; check-project compiles the copied source, not the reference."""
from pathlib import Path
import json,os,shutil,sys
from .workflow import ROOT,new_directory,command,dump,_binary
from .contract import export_spl,write_binary

class DependencyUnavailable(RuntimeError):
 pass

def units(root=ROOT):return json.loads((root/'systems/catalog.json').read_text())['units']
def prepare(unit,path,root=ROOT):
 item=next((x for x in units(root)if x['id']==unit),None)
 if item is None:raise ValueError('Unknown systems unit')
 out=new_directory(path);project=out/'project';project.mkdir()
 for name in item['projects']:
  shutil.copytree(root/'systems'/name,project/name,ignore=shutil.ignore_patterns('target','build','__pycache__'))
  cfg=project/name/'.cargo/config.toml'
  if cfg.exists():cfg.write_text('[source.crates-io]\nreplace-with = "course-vendor"\n[source.course-vendor]\ndirectory = '+json.dumps(str(root/'native/rust/vendor'))+'\n')
 rows,source=export_spl(root);(out/'data').mkdir();write_binary(out/'data/trajectory.bin',rows);dump(out/'data/source.json',source)
 dump(out/'project.json',dict(unit=unit,source_root=str(root),assessment='not_assessed',projects=item['projects']))
 (out/'prediction.md').write_text('# Prediction before execution\n\nWhat should happen? Derive one numerical result or expected error.\n')
 (out/'answer.md').write_text('# Independent project evidence\n\n## Explain\n\n## Predict\n\n## Implement (files I changed)\n\n## Break (expected failure and observed diagnostic)\n\n## Apply (same real inputs)\n\n## What surprised me\n\n## Why it failed\n\n## Python equivalent\n\n## Where this could help my work\n\n## Limitations\n\n## Delayed recall\n')
 (out/'START.md').write_text(f'# {item["title"]}\n\nRead `{root / item["lesson"]}`. Edit code under `project/`, not reference files.\n\nRun from the course root:\n```\npython learn.py check-project --workspace "{out}" --output "{out / "attempt01"}"\n```\nThe command compiles the source in THIS workspace. Original datasets stay at `{root}`. Data here is a derived binary of the existing selected SPL excerpt, not a new dataset. Missing optional tools return BLOCKED, not passed. Your answer remains unassessed.\n')
 return out

def check(workspace,path):
 ws=Path(workspace).resolve();m=json.loads((ws/'project.json').read_text());unit=m['unit'];repo=Path(m['source_root']);out=new_directory(path);proj=ws/'project';status='passed';reason=None
 try:
  if unit in ['sys00','sys01','sys02','sys03','sys04']:
   kind='c' if unit in ['sys00','sys01'] else 'cpp';build=out/'build';args=['cmake','-S',proj/kind,'-B',build,'-DCMAKE_BUILD_TYPE=Debug']
   if unit=='sys03':
    args+=['-DSHAPE_PYBIND=ON','-DPython_EXECUTABLE='+sys.executable]
    try:
     import pybind11
     args+=['-Dpybind11_DIR='+pybind11.get_cmake_dir()]
    except ImportError:
     import torch
     headers=Path(torch.__file__).parent/'include'
     if not (headers/'pybind11/pybind11.h').exists():raise DependencyUnavailable('No pybind11 headers; see sys03 setup.')
     args+=['-DSHAPE_PYBIND_HEADERS='+str(headers)]
   if unit=='sys04':
    import subprocess
    probe=subprocess.run(['pkg-config','--exists','opencv4'],capture_output=True) if shutil.which('pkg-config') else None
    if (probe is None or probe.returncode!=0) and not os.environ.get('OpenCV_DIR'):raise DependencyUnavailable('C++ OpenCV development package not detected through pkg-config; see sys04 for explicit CMake OpenCV_DIR setup.')
    args+=['-DSHAPE_OPENCV=ON']
    if os.environ.get('OpenCV_DIR'):args+=['-DOpenCV_DIR='+os.environ['OpenCV_DIR']]
   command(args,ws,out/'configure.json');command(['cmake','--build',build,'--config','Debug'],ws,out/'build.json');command(['ctest','--test-dir',build,'-C','Debug','--output-on-failure'],ws,out/'tests.json')
   if kind=='c':
    s=json.loads(command([_binary(build,'trajectory_reader'),ws/'data/trajectory.bin'],ws,out/'run.json')['stdout'])
    from .contract import read_binary
    rows=read_binary(ws/'data/trajectory.bin')
    expected=[sum(p[k]for p in rows)/len(rows)for k in ['x','y','z']]
    if s['count']!=len(rows)or any(abs(a-b)>1e-12 for a,b in zip(s['mean'],expected)):raise AssertionError('Private C source failed independent data check')
   if unit=='sys03':
    probe="import sys,math;sys.path.insert(0,sys.argv[1]);import shape_cpp; p=shape_cpp.predict([1.,2.,3.],[2.,0.,1.],0.5,9.81);assert max(abs(a-b) for a,b in zip(p,[2.,2.,2.27375]))<1e-12;d=shape_cpp.mst_deaths([[0.,0.,0.],[1.,0.,0.],[1.,1.,0.],[0.,1.,0.]]);assert d==[1.,1.,1.];print('pybind11 actual import, trajectory and topology checks passed')"
    candidates=list(build.rglob('shape_cpp*.so'))+list(build.rglob('shape_cpp*.pyd'))
    if len(candidates)!=1:raise RuntimeError('Ambiguous/missing built Python module')
    command([sys.executable,'-c',probe,candidates[0].parent],ws,out/'bindings_check.json')
   if unit=='sys04':command([_binary(build,'opencv_probe')],ws,out/'opencv_run.json')
  elif unit=='sys05':
   command([sys.executable,proj/'gpu/profile.py','--repo',repo,'--device','cpu','--output',out/'cpu_profile'],ws,out/'profile.json')
  elif unit=='sys06':
   command(['tsc','-p',proj/'typescript','--outFile',out/'shape.js'],ws,out/'ts_compile.json');command(['node',proj/'typescript/tests/test_viewer.cjs',out/'shape.js'],ws,out/'ts_tests.json')
  elif unit=='sys07':
   env=os.environ.copy();env['CARGO_TARGET_DIR']=str(out/'target');src=proj/'rust_validator'
   command(['cargo','test','--offline','--locked'],src,out/'rust_tests.json',env);command(['cargo','run','--offline','--locked','--bin','capture-validator','--','--binary',ws/'data/trajectory.bin'],src,out/'rust_run.json',env)
  elif unit=='sys08':
   status='blocked';reason='Resolve PyO3/maturin in a separate reviewed environment; no PyO3 lock or dependency download is fabricated. Follow systems/lessons/sys08.md.'
  elif unit=='sys09':
   command(['go','test','-race','-count=1','./...'],proj/'go_service',out/'go_tests.json')
  else:raise ValueError('Unknown unit')
 except Exception as e:
  status='blocked'if isinstance(e,(DependencyUnavailable,ImportError,FileNotFoundError))else'failed';reason=str(e)
 dump(out/'project_check.json',dict(status=status,unit=unit,workspace=str(ws),reason=reason,assessment='not_assessed',scope='copied-project build and declared checks; not every source exercise'))
 return out,status
