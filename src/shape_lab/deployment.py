"""Conservative Kubernetes teaching deployment. Static validation != cluster execution."""
from __future__ import annotations
from copy import deepcopy
import json
import re
import shutil
import subprocess


def resources(image: str,namespace: str,profile: str='core') -> dict:
    if not re.fullmatch(r'[a-z][a-z0-9-]{0,61}[a-z0-9]|[a-z]',namespace) or namespace in {'default','kube-system','kube-public','kube-node-lease'}:
        raise ValueError('Use a dedicated non-system lowercase namespace (1–63 characters).')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/:@-]{0,255}',image):raise ValueError('Invalid image reference.')
    if profile not in {'core','physics','full'}:raise ValueError('Unknown profile.')
    label={'app.kubernetes.io/name':'shape-course','app.kubernetes.io/part-of':'shape-learning'}
    env=[{'name':k,'value':v} for k,v in {'HOME':'/tmp/student','MPLCONFIGDIR':'/tmp/matplotlib','JUPYTER_RUNTIME_DIR':'/tmp/jupyter',
       'PYTHONDONTWRITEBYTECODE':'1','PYTHONUNBUFFERED':'1','MPLBACKEND':'Agg','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1',
       'MKL_NUM_THREADS':'1','COURSE_PROFILE':profile,'PYTEST_ADDOPTS':'-p no:cacheprovider'}.items()]
    security={'allowPrivilegeEscalation':False,'readOnlyRootFilesystem':True,'capabilities':{'drop':['ALL']}}
    container={'name':'course','image':image,'imagePullPolicy':'IfNotPresent','workingDir':'/course','env':env,
       'securityContext':security,'resources':{'requests':{'cpu':'500m','memory':'1Gi'},'limits':{'cpu':'2','memory':'4Gi'}},
       'volumeMounts':[{'name':'scratch','mountPath':'/tmp'},{'name':'work','mountPath':'/work'}]}
    pod={'automountServiceAccountToken':False,'securityContext':{'runAsNonRoot':True,'runAsUser':1000,'runAsGroup':1000,
          'fsGroup':1000,'seccompProfile':{'type':'RuntimeDefault'}},'containers':[container],
       'volumes':[{'name':'scratch','emptyDir':{'sizeLimit':'4Gi'}},{'name':'work','persistentVolumeClaim':{'claimName':'learner-work'}}]}
    jobpod=deepcopy(pod);jobpod['restartPolicy']='Never';jc=jobpod['containers'][0]
    jc['env'].append({'name':'POD_UID','valueFrom':{'fieldRef':{'fieldPath':'metadata.uid'}}})
    code="""import os,subprocess,sys,json
from pathlib import Path
out=Path('/work')/('acceptance-'+os.environ['POD_UID']);out.mkdir(exist_ok=False)
commands=[[sys.executable,'course.py','test','--profile',os.environ['COURSE_PROFILE'],'--output',str(out/'tests')],
 [sys.executable,'course.py','run','--stage','0','--jobs','1','--output',str(out/'stage00')]]
results=[]
for cmd in commands:
 rc=subprocess.run(cmd,check=False).returncode;results.append({'command':cmd,'returncode':rc})
 if rc:break
from shape_lab.acceptance import validate_native_evidence
profile=os.environ['COURSE_PROFILE']
tests=json.loads((out/'tests/tests.json').read_text()) if (out/'tests/tests.json').is_file() else {}
refs=json.loads((out/'stage00/execution.json').read_text()) if (out/'stage00/execution.json').is_file() else {}
errors=validate_native_evidence(tests,refs,profile,['notebooks/00_lab.ipynb'])
status={'status':'passed' if len(results)==2 and all(x['returncode']==0 for x in results) and not errors else 'failed',
 'commands':results,'output':str(out),'profile':profile,'errors':errors,'tests':tests,
 'reference_evidence':{k:refs.get(k) for k in ['order','records','passed','failed','source_inputs_unchanged','required_prior_reports_copied']}}

(out/'acceptance.json').write_text(json.dumps(status,indent=2)+'\\n');print('SHAPE_ACCEPTANCE='+json.dumps(status),flush=True)
sys.exit(0 if status['status']=='passed' else 1)
"""
    jc['command']=['python','-c',code]
    readpod=deepcopy(pod);rc=readpod['containers'][0]
    rc['command']=['python','-m','shape_lab.safe_server','--root','/course','--bind','0.0.0.0','--port','8000']
    rc['ports']=[{'name':'http','containerPort':8000}]
    rc['readinessProbe']={'httpGet':{'path':'/START_HERE.html','port':'http'},'initialDelaySeconds':2,'periodSeconds':5}
    rc['livenessProbe']={'httpGet':{'path':'/START_HERE.html','port':'http'},'initialDelaySeconds':10,'periodSeconds':20}
    # The reader serves /course, not private outputs. Avoid binding it to the
    # single-writer results PVC (which can also cause cross-node multi-attach).
    rc['volumeMounts']=[v for v in rc['volumeMounts'] if v['name']!='work']
    readpod['volumes']=[v for v in readpod['volumes'] if v['name']!='work']
    items=[
      {'apiVersion':'v1','kind':'Namespace','metadata':{'name':namespace,'labels':{'pod-security.kubernetes.io/enforce':'restricted','pod-security.kubernetes.io/audit':'restricted','pod-security.kubernetes.io/warn':'restricted'}}},
      {'apiVersion':'v1','kind':'PersistentVolumeClaim','metadata':{'name':'learner-work','namespace':namespace},'spec':{'accessModes':['ReadWriteOnce'],'resources':{'requests':{'storage':'4Gi'}}}},
      {'apiVersion':'apps/v1','kind':'Deployment','metadata':{'name':'course-reader','namespace':namespace,'labels':label},
       'spec':{'replicas':1,'selector':{'matchLabels':{'app':'course-reader'}},'template':{'metadata':{'labels':{'app':'course-reader',**label}},'spec':readpod}}},
      {'apiVersion':'v1','kind':'Service','metadata':{'name':'course-reader','namespace':namespace},'spec':{'type':'ClusterIP','selector':{'app':'course-reader'},'ports':[{'port':8000,'targetPort':'http'}]}},
      {'apiVersion':'batch/v1','kind':'Job','metadata':{'name':'course-acceptance','namespace':namespace,'labels':label},
       'spec':{'backoffLimit':0,'activeDeadlineSeconds':3600,'template':{'metadata':{'labels':{'app':'course-acceptance',**label}},'spec':jobpod}}}]
    return {'apiVersion':'v1','kind':'List','items':items}


def validate_resources(manifest: dict) -> list[str]:
    """Project policy checks; not the Kubernetes OpenAPI schema or admission server."""
    errors=[]
    if not isinstance(manifest,dict) or not isinstance(manifest.get('items'),list):
        return ['Expected a resource List with items.']
    items=manifest['items'];kinds={i.get('kind') for i in items if isinstance(i,dict)}
    if not {'Namespace','PersistentVolumeClaim','Deployment','Service','Job'}<=kinds:errors.append('Missing required resource kind.')
    namespaces=[i.get('metadata',{}).get('name') for i in items if i.get('kind')=='Namespace']
    if len(namespaces)!=1:errors.append('Exactly one dedicated Namespace is required.')
    namespace=namespaces[0] if len(namespaces)==1 else None
    seen=set()
    for item in items:
        kind=item.get('kind');meta=item.get('metadata',{});name=meta.get('name','unknown')
        identity=(kind,meta.get('namespace'),name)
        if identity in seen:errors.append(f'{name}: duplicate resource identity')
        seen.add(identity)
        if kind!='Namespace' and meta.get('namespace')!=namespace:errors.append(f'{name}: namespace mismatch')
        if kind=='Namespace':
            if name in {'default','kube-system','kube-public','kube-node-lease'}:errors.append('System namespace forbidden.')
            if meta.get('labels',{}).get('pod-security.kubernetes.io/enforce')!='restricted':errors.append('Restricted namespace policy required.')
        if kind=='Service' and item.get('spec',{}).get('type')!='ClusterIP':errors.append(f'{name}: public service forbidden')
        if kind not in {'Deployment','Job'}:continue
        pod=item.get('spec',{}).get('template',{}).get('spec',{})
        if pod.get('automountServiceAccountToken') is not False:errors.append(f'{name}: service-account token mounted')
        ps=pod.get('securityContext',{})
        if ps.get('runAsNonRoot') is not True or ps.get('runAsUser',0)==0:errors.append(f'{name}: non-root not enforced')
        if ps.get('seccompProfile',{}).get('type')!='RuntimeDefault':errors.append(f'{name}: runtime seccomp required')
        if any(pod.get(k,False) for k in ['hostNetwork','hostPID','hostIPC']):errors.append(f'{name}: host namespace access forbidden')
        if any('hostPath' in v for v in pod.get('volumes',[])):errors.append(f'{name}: hostPath forbidden')
        if not pod.get('containers'):errors.append(f'{name}: no containers')
        for c in pod.get('containers',[])+pod.get('initContainers',[]):
            sec=c.get('securityContext',{})
            for key,value in [('readOnlyRootFilesystem',True),('allowPrivilegeEscalation',False)]:
                if sec.get(key) is not value:errors.append(f'{name}: {key} policy')
            if sec.get('privileged',False):errors.append(f'{name}: privileged container forbidden')
            if sec.get('capabilities',{}).get('drop')!=['ALL']:errors.append(f'{name}: capabilities not dropped')
            if sec.get('runAsUser')==0:errors.append(f'{name}: root container override')
            if not c.get('resources',{}).get('limits'):errors.append(f'{name}: limits missing')
        if kind=='Job' and (item['spec'].get('backoffLimit')!=0 or pod.get('restartPolicy')!='Never'):errors.append('Job retry policy changed')
    return errors

def preflight(context: str) -> dict:
    if not context.startswith('kind-'):raise ValueError('This teaching verifier only accepts an explicit kind- context; it must not target production.')
    missing=[t for t in ['kubectl','docker','kind'] if shutil.which(t) is None]
    result={'status':'blocked' if missing else 'ready_for_commands','missing_tools':missing,'context':context,'cluster_verified':False}
    if missing:return result
    records=[]
    for cmd in [['docker','info','--format','{{.ServerVersion}}'],['kubectl','--context',context,'cluster-info','--request-timeout=10s']]:
        try:
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=20)
            records.append({'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
        except (OSError,subprocess.TimeoutExpired) as exc:
            records.append({'command':cmd,'returncode':2,'error':str(exc)})
    result['commands']=records
    if any(x['returncode'] for x in records):result['status']='blocked'
    return result
