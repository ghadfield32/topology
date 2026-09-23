"""Inspect an explicitly selected small point cloud without overwriting the input."""
from pathlib import Path
import argparse,json,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from shape_lab.explore import explore_csv


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv',type=Path)
    p.add_argument('--columns',nargs='+',required=True)
    p.add_argument('--source-note',required=True)
    p.add_argument('--units',required=True)
    p.add_argument('--points',type=int,default=20)
    p.add_argument('--seed',type=int,default=20260920)
    p.add_argument('--scale',choices=['none','standard'],default='none')
    p.add_argument('--out',type=Path,default=ROOT/'reports/my_experiment')
    a=p.parse_args()
    if a.out.exists():p.error('Output directory exists. Choose a new --out to preserve previous evidence.')
    try:r=explore_csv(a.csv,a.columns,a.points,a.seed,a.scale,a.source_note,a.units)
    except (ValueError,OSError) as e:p.error(str(e))
    a.out.mkdir(parents=True)
    (a.out/'results.json').write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
    finite=np.array([[b,d] for b,d in r['diagrams']['H1'] if d is not None]).reshape(-1,2)
    plt.figure(figsize=(6,5))
    if len(finite):
        plt.scatter(finite[:,0],finite[:,1]);upper=float(finite.max())
    else:
        upper=1.;plt.text(.5,.55,'No positive-length finite H1 bars',ha='center',transform=plt.gca().transAxes)
    plt.plot([0,upper],[0,upper],linestyle='--')
    plt.xlabel('Birth edge length');plt.ylabel('Death edge length')
    plt.title('Selected CSV sample — exploratory H1 diagram')
    plt.tight_layout();plt.savefig(a.out/'H1_diagram.png',dpi=140);plt.close()
    print(json.dumps(r,indent=2))
    print('Saved to',a.out)

if __name__=='__main__':main()
