"""Inspect a completed original-VGGT run; emit a small exploratory point table.

No metric registration or benchmark acceptance is performed. Confidence filtering
is a declared selection rule, not calibrated reliability. Run --help for usage.
"""
from pathlib import Path
import argparse,json,hashlib,sys,csv
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--frame',type=int,default=0)
    p.add_argument('--max-points',type=int,default=32)
    p.add_argument('--confidence-quantile',type=float,default=.5)
    a=p.parse_args()
    import numpy as np
    from shape_lab.model_contract import sample_candidate_points
    from shape_lab.persistence import rips_filtration,persistent_homology,diagram
    from shape_lab.display import save_json
    meta=json.loads((a.run/'run.json').read_text())
    if meta.get('status')!='completed_contract_check_only' or meta.get('model_family')!='original_VGGT':p.error('Expected a completed original-VGGT adapter run, not a fixture or Omega output.')
    file=a.run/'predictions.npz'
    with file.open('rb') as f:
        h=hashlib.file_digest(f,'sha256').hexdigest()
    if h!=meta['predictions_sha256']:p.error('Prediction archive changed after the recorded run.')
    if a.output.exists():p.error('Choose a new output directory; no overwrite is allowed.')
    with np.load(file,allow_pickle=False) as z:arrays={k:z[k] for k in z.files}
    X,ids=sample_candidate_points(arrays,a.frame,a.max_points,a.confidence_quantile)
    intervals=persistent_homology(rips_filtration(X,max_homology=1),max_dim=1)
    a.output.mkdir(parents=True,exist_ok=False)
    with (a.output/'candidate_points.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['frame','processed_row','processed_column','x_model_units','y_model_units','z_model_units'])
        for key,point in zip(ids,X):w.writerow([*key.tolist(),*point.tolist()])
    save_json(a.output/'exploration.json',{'source_run':str(a.run),'checkpoint':meta['checkpoint'],
        'source_prediction_hash':h,'point_count':len(X),'frame':a.frame,'confidence_quantile':a.confidence_quantile,
        'H0_intervals':diagram(intervals,0),'H1_intervals':diagram(intervals,1),
        'infinite_interval_encoding':'null death; surviving supplied filtration',
        'distance_units':'unvalidated model units','metric_validated':False,'confidence_is_probability':False,
        'warning':'Exploratory shape summary only; no independent reference comparison. Predicted topology can reflect model errors.'})
    print(a.output)
if __name__=='__main__':main()
