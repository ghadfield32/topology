"""Exact controls and fail-closed sports data contracts; no athlete skill benchmark."""
import hashlib,json
from pathlib import Path
import numpy as np
import pytest
import shape_lab.sports_v8 as s
R=Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('unit,value,expected',[('ft',10,3.048),('in',12,.3048),('m',2,2)])
def test_units(unit,value,expected): assert s.to_metres(value,unit)==pytest.approx(expected)
@pytest.mark.parametrize('unit',['feet?','pixel','yard',''])
def test_unknown_units(unit):
    with pytest.raises(ValueError):s.to_metres([1],unit)

def test_invalid_length():
    with pytest.raises(ValueError):s.to_metres([np.nan],'ft')

def test_frames_real_clock():assert np.allclose(s.frame_times([110,115,120],60),[110/60,115/60,2])
@pytest.mark.parametrize('frames,fps',[([0,0],60),([2,1],60),([.5,1],60),([0,1],0),([0,1],np.nan),([],60)])
def test_bad_frame_clock(frames,fps):
    with pytest.raises(ValueError):s.frame_times(frames,fps)

def test_angle_right_straight():
    assert s.joint_angles([[1,0,0],[-1,0,0]],[[0,0,0],[0,0,0]],[[0,1,0],[1,0,0]]).tolist()==pytest.approx([90,180])
def test_angle_scale_translation():
    a,b,c=np.array([[1.,0,0]]),np.zeros((1,3)),np.array([[0.,1,0]])
    assert np.allclose(s.joint_angles(a,b,c),s.joint_angles(a*5+9,b+9,c*5+9))
def test_degenerate_angle():
    with pytest.raises(ValueError):s.joint_angles([[0,0,0]],[[0,0,0]],[[1,0,0]])
def test_mismatched_angle():
    with pytest.raises(ValueError):s.joint_angles([[0,0]],[[0,0,0]],[[1,0,0]])

def test_interval_velocity_gap():
    v,ok=s.interval_velocities([0,1,10],[[0,0,0],[.1,0,0],[1,0,0]],10,max_gap_frames=1)
    assert ok.tolist()==[True,False] and v[0,0]==pytest.approx(1) and np.isnan(v[1]).all()
def test_missing_interval_velocity():
    v,ok=s.interval_velocities([0,1,2],[[0,0,0],[np.nan,0,0],[2,0,0]],10,max_gap_frames=1)
    assert not ok.any() and np.isnan(v).all()
@pytest.mark.parametrize('gap',[0,-1,1.5,np.inf])
def test_invalid_gap(gap):
    with pytest.raises(ValueError):s.interval_velocities([0,1],[[0,0,0],[1,0,0]],10,gap)

def test_fit_vertical_exact():
    t=np.arange(7)/10+20;z=2+4*(t-20)-.5*9.81*(t-20)**2
    fit=s.fit_vertical(t,z)
    assert fit.g==pytest.approx(9.81) and fit.z0==pytest.approx(2) and fit.v0==pytest.approx(4)
    assert np.max(abs(fit.predict(t)-z))<1e-10

def test_fixed_gravity_fit():
    t=np.arange(6)/10;z=1+2*t-4.9*t*t
    f=s.fit_vertical(t,z,gravity=9.8)
    assert f.g==9.8 and f.v0==pytest.approx(2)
@pytest.mark.parametrize('t,z',[([0,0,1],[0,1,2]),([0,1],[0,1]),([0,1,2],[0,np.nan,2]),([2,1,0],[1,2,3])])
def test_vertical_invalid(t,z):
    with pytest.raises(ValueError):s.fit_vertical(t,z)

def test_causal_no_future_and_stale():
    v,source=s.causal_hold([0,1,2],[10,20,30],[-.1,.5,1.5,5],max_age=.75)
    assert np.isnan(v[[0,3]]).all() and v[1:3].tolist()==[10,20]
    assert source.tolist()==[-1,0,1,-1]

def test_standardize_only_fit_rows():
    x=np.array([[1,2],[3,2],[99,100]],float)
    z,mean,scale=s.fit_standardize(x,[0,1])
    assert np.allclose(mean,[2,2]) and np.allclose(scale,[1,1]) and z[2,0]==97

def test_groups_cover_not_overlap():
    g=[1,1,2,3,4];p=s.group_partition(g,[1,2],[3],[4])
    assert p['train'].tolist()==[0,1,2]
@pytest.mark.parametrize('a,b,c',[([1],[1],[2,3]),([1],[2],[4]),([1,2],[],[3])])
def test_bad_group_partition(a,b,c):
    with pytest.raises(ValueError):s.group_partition([1,2,3],a,b,c)

def test_cloud_square_and_rigid():
    x=np.array([[0,0],[1,0],[1,1],[0,1]],float)
    d=s.cloud_diagrams(x)
    assert np.allclose(d[1],[[1,np.sqrt(2)]])
    assert np.allclose(d[1],s.cloud_diagrams(x@np.array([[0,-1],[1,0]])+10)[1])
    assert np.allclose(s.cloud_diagrams(x*3)[1],d[1]*3)

def test_bundled_integrity():
    report=s.verify_local_data(R)
    assert all(x['ok'] for x in report) and len(report)==2

def test_data_units_repeated_players():
    spl,sc=s.load_sports(R)
    assert len(spl['records'])==12 and len(sc)==12 and sc.player_id.nunique()==8
    assert spl['sampling_rate']==60 and spl['xyz_unit']=='ft'
    assert sc.loc[sc.player_id==2858,'position_group'].nunique()==3

def test_lfs_rejected():
    with pytest.raises(ValueError,match='LFS'):s.check_payload(b'version https://git-lfs.github.com/spec/v1\noid sha256:123')

def test_source_git_hash():
    b=b'hello\n'; expected=hashlib.sha1(b'blob 6\0'+b).hexdigest()
    assert s.git_blob_sha1(b)==expected
    with pytest.raises(ValueError,match='revision'):s.check_payload(b,'0'*40)

def test_compare_spl_source_control():
    local={'sampling_rate':60,'session':'2025-12-18','participant_id':'P','trial_id':'T','records':[{'frame':1,'source_time':16,'ball':[1,2,3],'right_shoulder':[2,3,4],'right_elbow':[3,4,5],'right_wrist':[4,5,6]}]}
    src={'sampling_rate':60,'trial_date':'2025-12-18','participant_id':'P','trial_id':'T','tracking':[{'frame':1,'time':16,'data':{'ball':[1,2,3],'player':{'RIGHT_SHOULDER':[2,3,4],'RIGHT_ELBOW':[3,4,5],'RIGHT_WRIST':[4,5,6]}}}]}
    assert s.compare_spl(local,src)['numeric_values']==12
    src['tracking'][0]['data']['ball'][0]=9
    with pytest.raises(ValueError):s.compare_spl(local,src)

def test_tracking_observed_filter():
    records=[{'player_id':1,'x':0.,'y':0.,'is_detected':True},{'player_id':2,'x':2.,'y':3.,'is_detected':False}]
    p,ids=s.tracking_cloud(records,detected_only=True)
    assert p.shape==(1,2) and ids.tolist()==[1]
    p,_=s.tracking_cloud(records,detected_only=False);assert p.shape==(2,2)

def test_tracking_duplicate_identity():
    rows=[{'player_id':1,'x':1.,'y':2.,'is_detected':True}]*2
    with pytest.raises(ValueError):s.tracking_cloud(rows)

def test_skillcorner_comparison_exact_and_mismatch():
    import pandas as pd
    source=pd.DataFrame({'player_id':[1,2],'position_group':['A','B'],'value':[3.,4.]})
    local=source.iloc[[1]].copy();local.insert(0,'source_row',[2])
    assert s.compare_skillcorner(local,source)['equal']
    local.loc[1,'value']=7
    with pytest.raises(ValueError):s.compare_skillcorner(local,source)

def test_empty_and_oversized_payload():
    with pytest.raises(ValueError):s.check_payload(b'')
    with pytest.raises(ValueError):s.check_payload(b'abcd',max_bytes=3)

@pytest.mark.parametrize('x,rows',[([[1,2]],[1]),([[1,np.nan]],[0]),([[1,2],[3,4]],[0,0]),([[1,2]],[.5])])
def test_invalid_scaling_selection(x,rows):
    with pytest.raises(ValueError):s.fit_standardize(x,rows)

@pytest.mark.parametrize('times,values,q,age',[([0,0],[1,2],[0],1),([0,1],[1],[0],1),([0,1],[1,2],[0],-1)])
def test_causal_hold_bad_contract(times,values,q,age):
    with pytest.raises(ValueError):s.causal_hold(times,values,q,age)

def test_source_script_verify_runs_offline():
    import subprocess,sys
    p=subprocess.run([sys.executable,str(R/'scripts/sports_v8.py'),'verify'],capture_output=True,text=True)
    assert p.returncode==0 and 'true' in p.stdout

def test_fetch_demands_license_before_network(tmp_path):
    import subprocess,sys
    p=subprocess.run([sys.executable,str(R/'scripts/sports_v8.py'),'fetch','spl','--destination',str(tmp_path/'never.json')],capture_output=True,text=True)
    assert p.returncode!=0 and '--accept-data-license' in p.stderr
    assert not (tmp_path/'never.json').exists()
