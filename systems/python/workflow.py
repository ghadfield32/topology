"""Bounded project builds and measured-data experiments. No automatic deployment or installs."""
from __future__ import annotations
from pathlib import Path
import datetime as dt, csv, hashlib, io, json, os, shutil, sqlite3, subprocess, sys, time
from .contract import export_spl, read_binary, write_binary, predict, validate_payload, sha256
ROOT=Path(__file__).resolve().parents[2]

def dump(path,value):Path(path).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n',encoding='utf8')
def new_directory(path):
 p=Path(path)
 if p.exists() or p.is_symlink():raise FileExistsError('Choose a new output directory: '+str(p))
 p.parent.mkdir(parents=True,exist_ok=True);p.mkdir();return p.resolve()
def _resolve(executable):
 """Locate an executable, including a Windows .cmd/.bat shim, into a shell-free argv.

 A package-manager install on Windows (for example `tsc`) is a `.cmd` wrapper that
 CreateProcess cannot start by bare name. Resolving it here keeps every caller
 shell-free instead of special-casing `shell=True` per command.
 """
 found=shutil.which(executable)
 if not found:return [executable]
 if os.name=='nt' and Path(found).suffix.lower() in {'.cmd','.bat'}:
  return [os.environ.get('COMSPEC','cmd.exe'),'/d','/c',found]
 return [found]

def command(args,cwd,log,env=None,timeout=300):
 begin=time.perf_counter();cmd=[str(x) for x in args]
 if cmd:cmd=[*_resolve(cmd[0]),*cmd[1:]]
 try:
  p=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=timeout)
  r=dict(command=cmd,cwd=str(cwd),exit_code=p.returncode,seconds=time.perf_counter()-begin,stdout=p.stdout,stderr=p.stderr)
 except (OSError,subprocess.TimeoutExpired) as e:r=dict(command=cmd,cwd=str(cwd),exit_code=-1,seconds=time.perf_counter()-begin,error=str(e))
 dump(log,r)
 if r['exit_code']!=0:raise RuntimeError('Command failed; inspect '+str(log))
 return r

def source_fingerprints(root=ROOT):
 paths=[]
 for area in ['systems/c','systems/cpp','systems/rust_validator/src','systems/rust_validator/tests','systems/typescript/src','systems/go_service','systems/python','systems/gpu','systems/pyo3','systems/tools']:
  for p in (root/area).rglob('*'):
   if p.is_file() and not any(x in p.parts for x in ['__pycache__','target','build','.git']):paths.append(p)
 paths.extend([root/'sports_v8/data/spl_selected_frames.json',root/'systems/catalog.json',root/'systems/rust_validator/Cargo.toml',root/'systems/rust_validator/Cargo.lock',root/'systems/rust_validator/.cargo/config.toml',root/'systems/typescript/tsconfig.json',root/'learn.py'])
 return {p.relative_to(root).as_posix():sha256(p) for p in sorted(set(paths))}

def _binary(folder,name):
 suffix='.exe' if os.name=='nt' else ''
 for p in [folder/(name+suffix),folder/'Debug'/(name+suffix),folder/'Release'/(name+suffix)]:
  if p.exists():return p
 raise FileNotFoundError(name)

def build_c_cpp(out,root=ROOT,sanitize=False,bindings=False):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);bins={}
 for key in ['c','cpp']:
  build=out/(key+'_build');args=['cmake','-S',root/'systems'/key,'-B',build,'-DCMAKE_BUILD_TYPE=Debug']
  if sanitize:args+=['-DSHAPE_SANITIZE=ON']
  if key=='cpp' and bindings:
   args+=['-DSHAPE_PYBIND=ON','-DPython_EXECUTABLE='+sys.executable]
   try:
    import pybind11
    args+=['-Dpybind11_DIR='+pybind11.get_cmake_dir()]
   except ImportError:
    # Explicit inspected headers in the installed PyTorch distribution; never downloaded or silently reimplemented.
    import torch
    headers=Path(torch.__file__).parent/'include'
    if not (headers/'pybind11/pybind11.h').exists():raise RuntimeError('pybind11 headers unavailable')
    args+=['-DSHAPE_PYBIND_HEADERS='+str(headers)]
  command(args,root,out/(key+'_configure.json'))
  command(['cmake','--build',build,'--config','Debug','--parallel','2'],root,out/(key+'_build.json'))
  command(['ctest','--test-dir',build,'-C','Debug','--output-on-failure'],root,out/(key+'_tests.json'))
  bins[key]=_binary(build,'trajectory_reader' if key=='c' else 'trajectory_cpp')
 return bins

def build_rust(out,root=ROOT):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);env=os.environ.copy();env['CARGO_TARGET_DIR']=str(out/'rust_target')
 command(['cargo','test','--offline','--locked'],root/'systems/rust_validator',out/'rust_tests.json',env,timeout=300)
 command(['cargo','build','--offline','--locked'],root/'systems/rust_validator',out/'rust_build.json',env,timeout=300)
 return _binary(out/'rust_target/debug','capture-validator')

def compile_typescript(out,root=ROOT):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);js=out/'shape.js'
 command(['tsc','-p',root/'systems/typescript','--outFile',js],root,out/'ts_compile.json')
 command(['node',root/'systems/typescript/tests/test_viewer.cjs',js],root,out/'ts_tests.json')
 return js

def run_demo(path,root=ROOT):
 """C + C++ + Rust + Python + SQL + TypeScript on the same selected observations."""
 out=new_directory(path);before=source_fingerprints(root);dump(out/'inputs_before.json',before)
 try:
  import numpy as np
  rows,source=export_spl(root);write_binary(out/'trajectory.bin',rows);dump(out/'observations.json',dict(source=source,records=rows))
  bins=build_c_cpp(out/'build',root);rust=build_rust(out/'build',root);js=compile_typescript(out/'build',root)
  c=json.loads(command([bins['c'],out/'trajectory.bin'],root,out/'c_run.json')['stdout'])
  r=json.loads(command([rust,'--binary',out/'trajectory.bin'],root,out/'rust_run.json')['stdout'])
  values=np.array([[p[k] for k in ('x','y','z')]for p in rows]);mean=values.mean(axis=0)
  if c['count']!=len(rows)or r['count']!=len(rows)or not np.allclose(c['mean'],mean,atol=1e-12,rtol=0)or not np.allclose(r['mean'],mean,atol=1e-12,rtol=0):raise AssertionError('Reader calculation mismatch')
  frames=[110,115,120,125,130,135,140];selected=[next(p for p in rows if p['frame']==f)for f in frames]
  times=np.array([p['time']for p in selected]);t0=times[0];t=times-t0;xyz=np.array([[p[k]for k in ('x','y','z')]for p in selected]);fit=[0,1,2,3,4];test=[5,6];g=9.81
  design=np.column_stack([np.ones(len(fit)),t[fit]])
  target=xyz[fit].copy();target[:,2]+=.5*g*t[fit]**2
  coef=np.linalg.lstsq(design,target,rcond=None)[0];position,velocity=coef
  python_pred=np.array([predict(position.tolist(),velocity.tolist(),float(x),g)for x in t])
  args=[bins['cpp'],t0,*position,*velocity,g,5/60,len(selected)]
  stdout=command(args,root,out/'cpp_run.json')['stdout'];(out/'cpp_predictions.csv').write_text(stdout,encoding='utf8')
  cpp=np.array([[float(row[k])for k in ('x','y','z')]for row in csv.DictReader(io.StringIO(stdout))])
  if not np.allclose(cpp,python_pred,atol=1e-12,rtol=0):raise AssertionError('Independent prediction mismatch')
  limits=["One selected trial from one participant; no independent athlete generalization.","The underlying excerpt is a selected numeric transcription; source-provider byte equality is not established here.","Times use an ideal frame/sample-rate clock, not measured synchronized camera PTS.","Confidence was not provided and remains null, not a predicted zero probability.","Fixed g=9.81 m/s^2, no spin/drag/contact; selected observations need not be pure free flight.","First five selected positions fit the initial state; two later same-shot positions evaluate this exposed teaching protocol."]
  payload=dict(schema='shape.systems.trajectory.v1',units='m',observed=selected,
    predicted=[dict(time=float(times[i]),x=float(p[0]),y=float(p[1]),z=float(p[2]),confidence=None)for i,p in enumerate(cpp)],
    metadata=dict(source=source,model='fixed-gravity initial-state least squares',train_frames=frames[:5],test_frames=frames[5:],limitations=limits))
  validate_payload(payload);dump(out/'trajectory.json',payload)
  metrics=dict(count=len(rows),confidence_known=c['known_confidence'],mean_m=mean.tolist(),cpp_python_max_abs_m=float(np.max(abs(cpp-python_pred))),
    height_fit_rmse_m=float(np.sqrt(np.mean((cpp[fit,2]-xyz[fit,2])**2))),height_test_mae_m=float(np.mean(abs(cpp[test,2]-xyz[test,2]))),
    height_mean_baseline_mae_m=float(np.mean(abs(xyz[fit,2].mean()-xyz[test,2]))),height_last_baseline_mae_m=float(np.mean(abs(xyz[fit[-1],2]-xyz[test,2]))),train_frames=frames[:5],test_frames=frames[5:])
  with sqlite3.connect(out/'experiment.sqlite')as db:
   db.executescript('CREATE TABLE observations(frame INTEGER PRIMARY KEY,time REAL NOT NULL,x REAL,y REAL,z REAL);CREATE TABLE predictions(frame INTEGER PRIMARY KEY,split TEXT NOT NULL,z REAL NOT NULL);')
   db.executemany('INSERT INTO observations VALUES(?,?,?,?,?)',[(p['frame'],p['time'],p['x'],p['y'],p['z'])for p in rows])
   db.executemany('INSERT INTO predictions VALUES(?,?,?)',[(f,'fit'if i<5 else 'later',float(cpp[i,2]))for i,f in enumerate(frames)])
   sql=db.execute('SELECT split,COUNT(*),AVG(ABS(p.z-o.z)) FROM predictions p JOIN observations o USING(frame) GROUP BY split ORDER BY split').fetchall()
   gaps=db.execute('SELECT frame,time-LAG(time) OVER(ORDER BY time) AS dt FROM observations').fetchall()
  dump(out/'sql_results.json',dict(error_by_split=sql,interval_seconds=gaps))
  viewer=out/'viewer';viewer.mkdir();shutil.copy2(root/'systems/typescript/index.html',viewer/'index.html');(viewer/'build').mkdir();shutil.copy2(js,viewer/'build/shape.js')
  dump(out/'results.json',dict(status='passed',metrics=metrics,source=source,limitations=limits))
  after=source_fingerprints(root)
  if before!=after:raise RuntimeError('Source inputs changed')
  dump(out/'execution.json',dict(schema='shape.systems.run.v17',status='passed',source_unchanged=True,source_hashes=before,python=sys.version,created_at=dt.datetime.now(dt.timezone.utc).isoformat(),scope='new measured-data integration demo; not all historical notebooks'))
  (out/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Systems experiment</title><body style="font:18px/1.6 system-ui;max-width:900px;margin:40px auto;padding:16px"><h1>One observation stream, several language roles</h1><p>Source: selected SPL ball records. C and Rust decode the same portable binary. Python fits a simple state, C++ computes its trajectory, SQLite aggregates its errors, and TypeScript validates and displays the result.</p><p><a href="viewer/index.html">Open viewer, then select ../trajectory.json</a> · <a href="results.json">Results and limitations</a> · <a href="execution.json">Execution evidence</a> · <a href="sql_results.json">SQL checks</a></p><p>This is a worked teaching example, not an assessed learner submission or a new validation of the source measurements.</p></body></html>',encoding='utf8')
  return out
 except Exception as e:
  dump(out/'failure.json',dict(status='failed',error=str(e)));raise
