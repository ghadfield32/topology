"""Render/check locally, or explicitly apply to an EXISTING disposable kind cluster.

Never creates/deletes a cluster or deletes a namespace/PVC. --apply is a requested
side effect; namespace must not already exist. Export data before manual cleanup.
"""
import argparse,json,re,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from shape_lab.deployment import resources,validate_resources,preflight


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--image',default='listening-to-shape:12');p.add_argument('--namespace',default='shape-learning-v12')
    p.add_argument('--profile',choices=['core','physics','full'],default='core')
    p.add_argument('--context',default='kind-shape-learning');p.add_argument('--apply',action='store_true')
    p.add_argument('--static',action='store_true');p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.apply and a.static:p.error('Choose static checks OR explicit live apply.')
    a.output.mkdir(parents=True,exist_ok=False)
    manifest=resources(a.image,a.namespace,a.profile)
    path=a.output/'resources.json';path.write_text(json.dumps(manifest,indent=2)+'\n')
    errors=validate_resources(manifest)
    report={'static_policy':'passed' if not errors else 'failed','policy_errors':errors,'cluster_verified':False,
            'scope':'Static project checks are not schema validation or a live deployment.','commands':[]}
    status=1 if errors else 0
    def save():
        (a.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
    if errors:save();return 1
    if a.static:report['status']='static_only';save();return 0
    ready=preflight(a.context);report['preflight']=ready
    if ready['status']!='ready_for_commands':report['status']='blocked';save();return 2
    if not a.apply:report['status']='ready_not_applied';save();return 2
    def command(args,timeout=60):
        cmd=['kubectl','--context',a.context,*args]
        try:
            proc=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
            record={'command':cmd,'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}
        except (OSError,subprocess.TimeoutExpired) as exc:record={'command':cmd,'returncode':2,'error':str(exc)}
        report['commands'].append(record)
        (a.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
        return record
    existing=command(['get','namespace',a.namespace,'-o','name','--ignore-not-found=true'])
    if existing['returncode'] or existing.get('stdout','').strip():
        report.update(status='blocked',reason='Cannot verify that the dedicated namespace is absent.');save();return 2
    # Server-side validation requires the namespace for namespaced resources. Create
    # the Namespace alone, then dry-run every object against the real server.
    nsfile=a.output/'namespace.json';nsfile.write_text(json.dumps(manifest['items'][0]))
    if command(['create','-f',str(nsfile)])['returncode']:
        report['status']='failed';save();return 1
    if command(['apply','--dry-run=server','-f',str(path)])['returncode']:
        report.update(status='failed',reason='Server schema/admission rejected resources; namespace retained for inspection.');save();return 1
    if command(['apply','-f',str(path)])['returncode']:
        report['status']='failed';save();return 1
    rollout=command(['-n',a.namespace,'rollout','status','deployment/course-reader','--timeout=300s'],330)
    completed=command(['-n',a.namespace,'wait','--for=condition=complete','job/course-acceptance','--timeout=3600s'],3630)
    log=command(['-n',a.namespace,'logs','job/course-acceptance','--all-containers=true'],60)
    command(['-n',a.namespace,'get','pods,pvc,jobs','-o','json'])
    command(['-n',a.namespace,'get','events','--sort-by=.lastTimestamp'])
    lines=[x.split('SHAPE_ACCEPTANCE=',1)[1] for x in log.get('stdout','').splitlines() if x.startswith('SHAPE_ACCEPTANCE=')]
    try:evidence=json.loads(lines[-1]) if lines else {}
    except json.JSONDecodeError:evidence={}
    from shape_lab.acceptance import validate_native_evidence
    child_errors=validate_native_evidence(evidence.get('tests',{}),evidence.get('reference_evidence',{}),a.profile,['notebooks/00_lab.ipynb'])
    report['child_evidence_errors']=child_errors
    valid=not child_errors and evidence.get('profile')==a.profile and evidence.get('status')=='passed' and len(evidence.get('commands',[]))==2 and all(x['returncode']==0 for x in evidence.get('commands',[]))
    report.update(status='passed' if valid and rollout['returncode']==0 and completed['returncode']==0 else 'failed',
                  cluster_verified=bool(valid and rollout['returncode']==0 and completed['returncode']==0),job_evidence=evidence,
                  persistent_results='Retained on learner-work PVC; copy them out before manual namespace deletion.')
    save();return 0 if report['cluster_verified'] else 1

if __name__=='__main__':raise SystemExit(main())
