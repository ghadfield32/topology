"""Generate sports worked labs and separate learner/reference coding notebooks."""
from pathlib import Path
import textwrap,json
import nbformat as nbf
R=Path(__file__).resolve().parents[1]
M=nbf.v4.new_markdown_cell;C=nbf.v4.new_code_cell
SETUP='''from pathlib import Path
import sys, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic('matplotlib', 'inline')
from dataclasses import asdict
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'src/shape_lab').exists())
sys.path.insert(0, str(ROOT / 'src'))
from shape_lab import sports_v8 as sport
from shape_lab.persistence import finite_bottleneck
spl, profiles = sport.load_sports(ROOT)
frames = np.array([r['frame'] for r in spl['records']])
times = sport.frame_times(frames, spl['sampling_rate'])
ball = sport.to_metres([r['ball'] for r in spl['records']], spl['xyz_unit'])
report_dir = ROOT / 'reports/v8/sports'
report_dir.mkdir(parents=True, exist_ok=True)
def save_report(stage, result):
    # Reports contain ordinary finite values; absent values are recorded explicitly.
    (report_dir / f'{stage}.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\\n')
print('Data:', len(frames), 'selected frames from one shot;', len(profiles), 'profiles from', profiles.player_id.nunique(), 'players')
'''
LABS={
'S00':[
('Inspect before interpreting','''print(json.dumps({k:v for k,v in spl.items() if k != 'records'}, indent=2))
display(profiles.head(6))
assert profiles.player_id.nunique() == 8
assert len({spl['participant_id']}) == 1
'''),
('One quantity, two unit representations','''first_ft = np.array(spl['records'][0]['ball'])
first_m = sport.to_metres(first_ft, 'ft')
assert np.allclose(first_m / .3048, first_ft)
print('First ball xyz in feet:', first_ft)
print('Same point in metres:', first_m)
print('Hoop offset is a different frame:', sport.to_metres([spl['landing_x'], spl['landing_y']], 'in'))
'''),
('Source grain and repeated identity','''counts = profiles.groupby('player_id').size()
fig, ax = plt.subplots(figsize=(7,4))
ax.bar(counts.index.astype(str), counts.values)
ax.set(xlabel='Provider player ID', ylabel='Selected profile rows', title='12 profile rows are 8 player IDs')
fig.tight_layout(); plt.show()
save_report('S00', {'selected_frames':len(frames),'selected_shots':1,'profile_rows':len(profiles),'distinct_player_ids':int(profiles.player_id.nunique()),'local_integrity':sport.verify_local_data(ROOT),'remote_source_equality_verified':False})
''')],
'S01':[
('A known angle before estimated coordinates','''a=np.array([[1.,0,0]]); b=np.zeros((1,3)); c=np.array([[0.,1,0]])
assert sport.joint_angles(a,b,c)[0] == 90
assert np.allclose(sport.joint_angles(a+20,b+20,c+20), [90])
print('Right-angle and translation checks passed.')
'''),
('Unsigned estimated landmark angles','''shoulder, elbow, wrist = [sport.to_metres([r[k] for r in spl['records']], 'ft') for k in ['right_shoulder','right_elbow','right_wrist']]
angles=sport.joint_angles(shoulder,elbow,wrist)
display(pd.DataFrame({'frame':frames, 'ideal_time_s':times, 'unsigned_angle_deg':angles}))
fig, ax = plt.subplots(figsize=(7,4)); ax.scatter(times, angles)
ax.set(xlabel='Ideal sample-clock time (s)', ylabel='Unsigned angle (degrees)', title='Selected shoulder–elbow–wrist estimates; not clinical flexion')
fig.tight_layout(); plt.show()
'''),
('Do not assign adjacent table rows adjacent frame times','''v1, ok1=sport.interval_velocities(frames,ball,60,max_gap_frames=1)
v5, ok5=sport.interval_velocities(frames,ball,60,max_gap_frames=5)
table=pd.DataFrame({'start_frame':frames[:-1], 'end_frame':frames[1:], 'duration_s':np.diff(times), 'accepted_max_gap_5':ok5, 'secant_magnitude_m_s':np.linalg.norm(v5,axis=1)})
display(table)
assert ok1.sum() == 1
assert ok5.sum() == 7
save_report('S01',{'angles_deg':angles.tolist(),'strict_intervals':int(ok1.sum()),'five_frame_intervals':int(ok5.sum()),'total_intervals':len(ok5),'measurement_accuracy_validated':False})
''')],
'S02':[
('Recover a manufactured known answer','''t=np.arange(8)/10
z=2+4*t-.5*9.81*t*t
control=sport.fit_vertical(t,z)
assert abs(control.g-9.81)<1e-10
assert abs(control.v0-4)<1e-10
print(asdict(control))
'''),
('Explicit fitting and later-point groups from one selected shot','''fit_mask=(frames>=110)&(frames<=130)
later_mask=np.isin(frames,[135,140])
fixed=sport.fit_vertical(times[fit_mask],ball[fit_mask,2],gravity=9.81)
free=sport.fit_vertical(times[fit_mask],ball[fit_mask,2])
last_height=float(ball[fit_mask,2][-1])
truth=ball[later_mask,2]
predictions={'constant_height':np.full(len(truth),last_height),'fixed_gravity':fixed.predict(times[later_mask]),'free_quadratic':free.predict(times[later_mask])}
mae={k:float(np.mean(abs(v-truth))) for k,v in predictions.items()}
print('Later-point absolute errors (m):',mae)
print('Free fitted curvature parameter g:',free.g,'m/s²; NOT a certified physical measurement')
display(pd.DataFrame({'frame':frames[later_mask], 'source_height_m':truth, **predictions}))
'''),
('A plot that reveals both fitting and later observations','''grid=np.linspace(times[fit_mask].min(),times[later_mask].max(),80)
fig,ax=plt.subplots(figsize=(8,4));ax.scatter(times[fit_mask],ball[fit_mask,2],label='Source estimates: fitting')
ax.scatter(times[later_mask],truth,marker='x',label='Source estimates: later same shot')
ax.plot(grid,fixed.predict(grid),label='Fixed g assumption');ax.plot(grid,free.predict(grid),label='Free quadratic')
ax.set(xlabel='Ideal sample-clock time (s)',ylabel='Source-estimated height (m)',title='One selected trial: model-adequacy demonstration')
ax.legend();fig.tight_layout();plt.show()
'''),
('Clock ambiguity despite a good curve fit','''wrong=sport.fit_vertical(times[fit_mask]*2,ball[fit_mask,2])
assert np.isclose(wrong.g,free.g/4)
save_report('S02',{'fit_frames':frames[fit_mask].tolist(),'later_frames':frames[later_mask].tolist(),'fixed':asdict(fixed),'free':asdict(free),'later_mae_m':mae,'g_with_doubled_clock':wrong.g,'later_points_are_independent_athletes':False,'release_label_known':False})
''')],
'S03':[
('Known topology and explicit convention','''square=np.array([[0.,0],[1,0],[1,1],[0,1]])
d=sport.cloud_diagrams(square)
assert np.allclose(d[1],[[1,np.sqrt(2)]])
assert np.allclose(sport.cloud_diagrams(square*3)[1],d[1]*3)
print('Square H1:', d[1])
'''),
('Real profile features, not field positions','''columns=['running_distance_full_all','hsr_distance_full_all','sprint_distance_full_all']
x=profiles[columns].to_numpy()
z,mu,scale=sport.fit_standardize(x,np.arange(len(x)))
# This all-row fit is explicitly exploratory, not a training/evaluation model.
raw=sport.cloud_diagrams(x); standardized=sport.cloud_diagrams(z)
print('Features:',columns)
print('Exploratory mean:',mu,'standard deviation:',scale)
print('Raw H1:',raw[1]);print('Standardized H1:',standardized[1])
'''),
('Display profiles and finite diagram information','''fig,ax=plt.subplots(figsize=(7,4))
ax.scatter(x[:,0],x[:,1])
for i, r in profiles.iterrows():ax.annotate(str(r.player_id),(x[i,0],x[i,1]),fontsize=8)
ax.set(xlabel='Published running-distance summary (m)',ylabel='Published HSR-distance summary (m)',title='Feature coordinates — not a pitch map')
fig.tight_layout();plt.show()
fig,ax=plt.subplots(figsize=(6,4))
for k in (0,1):
    a=standardized[k];a=a[np.isfinite(a[:,1])]
    if len(a):ax.scatter(a[:,0],a[:,1],label=f'H{k} finite bars')
ax.set(xlabel='Birth (standardized feature distance)',ylabel='Death',title='Finite persistence pairs of selected profiles')
ax.legend();fig.tight_layout();plt.show()
save_report('S03',{'features':columns,'profile_rows':len(x),'player_count':int(profiles.player_id.nunique()),'raw_h1':raw[1].tolist(),'standardized_h1':standardized[1].tolist(),'metric':'Euclidean; Rips max-edge; F2; through triangles','predictive_benchmark':False})
''')],
'S04':[
('Past-only estimate versus future-assisted interpolation','''q=np.array([-.1,.5,1.5,5.])
held,index=sport.causal_hold([0,1,2],[10,20,30],q,.75)
assert index.tolist()==[-1,0,1,-1]
display(pd.DataFrame({'query':q,'past_only_value':held,'source_row':index}))
print('At 1.5, interpolation using time 2 would return 25, but it uses the future.')
'''),
('Estimate provenance on sparse actual source times','''q=np.arange(0,3.6,.1)
held,index=sport.causal_hold(times,ball[:,2],q,max_age=.1)
fig,ax=plt.subplots(figsize=(8,4));ax.scatter(times,ball[:,2],label='Selected source estimates')
ax.scatter(q,held,marker='x',label='Past-only derived holds, age <=0.1s')
ax.set(xlabel='Ideal source/query time (s)',ylabel='Height (m)',title='Missing estimates are not silently filled from the future')
ax.legend();fig.tight_layout();plt.show()
'''),
('Known perturbation bound, not a measured noise distribution','''rng=np.random.default_rng(808)
x=profiles[['running_distance_full_all','hsr_distance_full_all','sprint_distance_full_all']].to_numpy()
x,_,_=sport.fit_standardize(x,np.arange(len(x)))
base=sport.cloud_diagrams(x)[1]
trials=[]
for repeat in range(20):
    y=x+rng.normal(0,.01,x.shape) # Artificial error in dimensionless profile coordinates
    delta=float(np.linalg.norm(y-x,axis=1).max())
    distance=finite_bottleneck(base,sport.cloud_diagrams(y)[1])
    assert distance<=2*delta+1e-9
    trials.append({'delta':delta,'bottleneck_h1':float(distance),'bound':2*delta})
save_report('S04',{'perturbation_checks':trials,'accepted_query_count':int((index>=0).sum()),'total_queries':len(q),'perturbations_are_measured_sensor_noise':False})
print('20 matched-cloud checks passed. This is not a camera-error calibration.')
''')],
'S05':[
('Partition the observed athlete IDs, not individual profile rows','''groups=profiles.player_id.to_numpy()
parts=sport.group_partition(groups,[211,218,2759,2858],[4322,4792],[5468,5521])
for name,indices in parts.items():print(name,indices.tolist(),sorted(set(groups[indices])))
assert not set(groups[parts['train']]) & set(groups[parts['test']])
assert sum(map(len,parts.values()))==len(profiles)
'''),
('Preprocessing is fitted on training data','''features=['running_distance_full_all','hsr_distance_full_all','sprint_distance_full_all']
x=profiles[features].to_numpy()
z,train_mean,scale=sport.fit_standardize(x,parts['train'])
all_mean=x.mean(axis=0)
display(pd.DataFrame({'feature':features,'train_mean':train_mean,'all_row_mean_leakage_control':all_mean,'difference':all_mean-train_mean}))
assert np.allclose(z[parts['train']].mean(axis=0),0)
'''),
('Record what this exercise did NOT establish','''result={'partition_rows':{k:v.tolist() for k,v in parts.items()},'partition_players':{k:sorted(map(int,set(groups[v]))) for k,v in parts.items()},'training_mean':train_mean.tolist(),'all_mean':all_mean.tolist(),'model_fitted':False,'sports_predictive_accuracy':None,'reason':'Small ordered excerpt; no independent supervised performance claim.'}
save_report('S05',result)
print(json.dumps(result,indent=2))
''')],
'S06':[
('Audit the required local source excerpts','''checks=sport.verify_local_data(ROOT)
assert all(row['ok'] for row in checks)
print(json.dumps(checks,indent=2))
registry=json.loads((ROOT/'sports_v8/dataset_registry.json').read_text())
display(pd.DataFrame([{k:d[k] for k in ['name','date','status','license']} for d in registry['datasets']]))
'''),
('Demonstrate why an LFS pointer is not a tracking dataset','''pointer=b'version https://git-lfs.github.com/spec/v1\\noid sha256:abc\\nsize 97091519\\n'
try:
    sport.check_payload(pointer)
except ValueError as error:
    print('Expected rejection:',error)
else:raise AssertionError('Pointer should never pass as numeric data.')
'''),
('An explicit schema adapter, with a constructed—not observed—fixture','''fixture=[{'player_id':1,'x':0.,'y':0.,'is_detected':True},{'player_id':2,'x':3.,'y':4.,'is_detected':False}]
observed,obs_ids=sport.tracking_cloud(fixture,detected_only=True)
all_provider,all_ids=sport.tracking_cloud(fixture,detected_only=False)
assert observed.shape==(1,2) and all_provider.shape==(2,2)
print('Constructed fixture:',obs_ids,all_ids)
print('No full-match tracking or body-pose payload was executed.')
'''),
('Build your own protocol before obtaining a score','''protocol={'question':'Does a topological movement descriptor add held-out information beyond conventional features for a specified available label?', 'decision_time':'Must be declared before feature extraction', 'independent_unit':'Athlete/session/trial, chosen to match use', 'baseline':'Conventional features with training-only preprocessing', 'test_policy':'Untouched source groups', 'rights_review_required':True, 'current_excerpt_sufficient_for_prediction':False}
save_report('S06',{'local_sources':checks,'registry_entries':len(registry['datasets']),'full_source_download_executed':False,'tracking_fixture_is_manufactured':True,'protocol':protocol})
print(json.dumps(protocol,indent=2))
''')]
}
# Each answer cell below is original executable exercise code; learners receive the signature only.
EXERCISES={
'S00':[
('Convert feet to metres. Accept a numeric list and return a NumPy array.','def feet_to_metres(values):\n    return np.asarray(values, dtype=float) * 0.3048','assert np.allclose(feet_to_metres([1,10]),[.3048,3.048])','A single factor changes units; it does not change coordinate origin.'),
('Count distinct athlete IDs, not rows.','def athlete_count(ids):\n    return len(set(ids))','assert athlete_count([1,1,2,3,3])==3','Repeated measurements retain the same independent athlete ID.'),
('Return elapsed seconds between two frame IDs; reject reversed frames and nonpositive fps.','def elapsed_seconds(start,end,fps):\n    if end<=start or fps<=0:\n        raise ValueError("Positive elapsed time and fps required")\n    return (end-start)/fps','assert elapsed_seconds(110,140,60)==.5','The difference is in frame numbers, not row positions.')],
'S01':[
('Return straight-line separation of two points.','def separation(a,b):\n    return float(np.linalg.norm(np.asarray(b,float)-np.asarray(a,float)))','assert separation([0,0,0],[3,4,0])==5','Euclidean separation need not equal the unobserved travelled path.'),
('Return secant velocity for two positions and increasing times.','def secant(a,b,t0,t1):\n    if t1<=t0:raise ValueError("Increasing times required")\n    return (np.asarray(b,float)-np.asarray(a,float))/(t1-t0)','assert np.allclose(secant([0,0,0],[.2,0,0],0,.1),[2,0,0])','A secant is an interval average, not an exact instantaneous derivative.'),
('Compute cosine of the angle formed by two nonzero vectors.','def angle_cosine(u,v):\n    u,v=np.asarray(u,float),np.asarray(v,float)\n    denom=np.linalg.norm(u)*np.linalg.norm(v)\n    if denom==0:raise ValueError("Undefined angle")\n    return float(np.clip(np.dot(u,v)/denom,-1,1))','assert angle_cosine([1,0,0],[0,1,0])==0','Dot product over norm product; guard undefined zero rays.')],
'S02':[
('Calculate height under constant downward acceleration.','def vertical_height(z0,v0,g,t):\n    t=np.asarray(t,float)\n    return z0+v0*t-.5*g*t*t','assert np.isclose(vertical_height(2,4,9.81,.2),2.6038)','Keep time relative to the stated origin.'),
('Calculate root-mean-square error of equal nonempty finite arrays.','def rmse(actual,predicted):\n    a,p=np.asarray(actual,float),np.asarray(predicted,float)\n    if a.shape!=p.shape or not a.size or not np.isfinite(a).all() or not np.isfinite(p).all():raise ValueError("Invalid pair")\n    return float(np.sqrt(np.mean((a-p)**2)))','assert np.isclose(rmse([1,2],[1,4]),np.sqrt(2))','Squaring, averaging and taking a square root retains output units.'),
('Map the coefficient of t² to a downward-acceleration parameter.','def gravity_coefficient(quadratic):\n    return -2*float(quadratic)','assert gravity_coefficient(-4.905)==9.81','The coefficient is -g/2. Its physical interpretation still needs validation.')],
'S03':[
('Construct a full Euclidean pairwise-distance matrix.','def pairwise_distance(x):\n    x=np.asarray(x,float)\n    return np.linalg.norm(x[:,None,:]-x[None,:,:],axis=2)','assert np.allclose(pairwise_distance([[0,0],[3,4]]),[[0,5],[5,0]])','Broadcasting compares every row to every row.'),
('Fit feature means on declared training rows only.','def training_mean(x,rows):\n    return np.asarray(x,float)[np.asarray(rows,int)].mean(axis=0)','assert np.allclose(training_mean([[1,2],[3,4],[99,99]],[0,1]),[2,3])','Never fit on the third row when it belongs to test.'),
('Return lifetimes of finite positive intervals from a birth/death array.','def finite_lifetimes(pairs):\n    p=np.asarray(pairs,float).reshape(-1,2)\n    valid=np.isfinite(p).all(axis=1)&(p[:,1]>p[:,0])\n    return p[valid,1]-p[valid,0]','assert np.allclose(finite_lifetimes([[1,2],[0,np.inf],[1,1]]),[1])','This is an explicit reporting policy, not evidence that essential bars do not exist.')],
'S04':[
('Find the latest available row index, or -1 before the first observation. Assume sorted times.','def past_index(times,query):\n    return int(np.searchsorted(np.asarray(times,float),query,side="right")-1)','assert past_index([0,1,2],1.5)==1 and past_index([0,1],-.1)==-1','Right-sided search includes a sample at exactly the query time.'),
('Compute maximum displacement between corresponding points.','def max_displacement(x,y):\n    return float(np.linalg.norm(np.asarray(x,float)-np.asarray(y,float),axis=1).max())','assert max_displacement([[0,0],[1,1]],[[0,0],[1,1.2]])==__import__("pytest").approx(.2)','The correspondence of rows is an assumption; nearest-point matching is different.'),
('Return the matched-cloud edge-error bound for a nonnegative displacement bound.','def edge_bound(delta):\n    if delta<0:raise ValueError("Nonnegative displacement bound required")\n    return 2*delta','assert edge_bound(.01)==.02','Two endpoints can each move by delta.')],
'S05':[
('Return athlete IDs appearing in both collections.','def shared_athletes(train,test):\n    return set(train)&set(test)','assert shared_athletes([1,2,2],[2,3])=={2}','Distinct row numbers can still refer to a shared athlete.'),
('Is a value available by the declared decision time? Use <=.','def available_by(observation_time,decision_time):\n    return observation_time<=decision_time','assert available_by(1,1) and not available_by(2,1)','Actual availability must include arrival/processing delay when relevant.'),
('Return row indices belonging to explicitly assigned athlete IDs.','def rows_for_athletes(all_ids,selected_ids):\n    return np.flatnonzero(np.isin(all_ids,list(selected_ids)))','assert rows_for_athletes([1,2,2,3],{2}).tolist()==[1,2]','Both position records of a selected athlete follow their group.')],
'S06':[
('Compute Git blob SHA1 including its type/length header.','def blob_hash(payload):\n    import hashlib\n    return hashlib.sha1(b"blob "+str(len(payload)).encode()+b"\\0"+payload).hexdigest()','assert blob_hash(b"hello\\n")==sport.git_blob_sha1(b"hello\\n")','Git object IDs are not plain SHA1(file bytes).'),
('Identify Git LFS pointer text.','def is_lfs_pointer(payload):\n    return payload.startswith(b"version https://git-lfs.github.com/spec/")','assert is_lfs_pointer(b"version https://git-lfs.github.com/spec/v1\\n") and not is_lfs_pointer(b"1,2,3\\n")','A pointer carries a hash and size, not the underlying tracking records.'),
('Return required evidence labels not present in the supplied set.','def missing_evidence(required,supplied):\n    return sorted(set(required)-set(supplied))','assert missing_evidence(["units","split","license"],["units"])==["license","split"]','This checks labels present, not the correctness or legal sufficiency of the evidence.')]
}

def notebook(cells,path):
    book=nbf.v4.new_notebook(cells=cells,metadata={'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'},'language_info':{'name':'python'}})
    nbf.write(book,path)

def main():
    for stage,sections in LABS.items():
        title=(R/'sports_v8/lessons'/f'{stage}.md').read_text().splitlines()[0][2:]
        cells=[M(f'# {title}\n\nRead the matching lesson before running. Predictions first; source facts, manufactured controls and interpretations are labeled separately. This is not a sports performance benchmark.'),C(SETUP)]
        for heading,code in sections:cells.extend([M('## '+heading),C(code)])
        cells.append(M('## Independent explanation\nState the observation unit, assumptions, units, one result and one unsupported conclusion. Then work the separate learner notebook without the answer notebook open.'))
        notebook(cells,R/'sports_v8/notebooks'/f'{stage}.ipynb')
        for kind in ['practice','solutions']:
            cells=[M(f'# {stage} — '+('Independent coding practice' if kind=='practice' else 'Worked coding answers')+'\n\nThree exercises. Learner NotImplementedError cells are assignments, not broken reference code. Read the prose lesson and predict the checks first.'),C(SETUP)]
            for j,(spec,code,check,note) in enumerate(EXERCISES[stage],1):
                # Avoid making pytest a runtime requirement for the exercise notebook.
                check=check.replace('assert max_displacement([[0,0],[1,1]],[[0,0],[1,1.2]])==__import__("pytest").approx(.2)','assert np.isclose(max_displacement([[0,0],[1,1]],[[0,0],[1,1.2]]),.2)')
                cells.append(M(f'## {stage}.C{j} — {spec}\n\nHint: {note}'))
                cells.append(C(code if kind=='solutions' else code.splitlines()[0]+'\n    raise NotImplementedError("Learner assignment: implement before running check")'))
                cells.append(C(check+f'\nprint("{stage}.C{j}: check passed")'))
            notebook(cells,R/f'sports_v8/{kind}/{stage}.ipynb')
    print('Generated 7 worked, 7 answer and 7 learner notebooks.')
if __name__=='__main__':main()
