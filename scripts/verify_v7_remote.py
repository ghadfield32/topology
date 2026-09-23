"""Opt-in comparison with official plaintext: python scripts/verify_v7_remote.py seeds.

Fetch only the two documented small public text files. Compare every numeric
value in order using canonical decimal notation. Never replace bundled data.
A network error is an error, not a match. No service or recurring task is created.
"""
from pathlib import Path
from io import StringIO
import argparse,json,sys,urllib.request
import pandas as pd
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from shape_lab.evidence_v7 import numeric_digest,load_snapshot,IDS

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('dataset',choices=IDS);a=p.parse_args()
 _,meta=load_snapshot(a.dataset)
 with urllib.request.urlopen(meta['raw_url'],timeout=30) as r:
  body=r.read(1_000_001)
 if len(body)>1_000_000:raise ValueError('Unexpected source size')
 t=pd.read_csv(StringIO(body.decode('utf-8-sig')),sep=r'\s+' if a.dataset=='seeds' else ',',header=None if a.dataset=='seeds' else 0,dtype=str)
 digest=numeric_digest(t.values.tolist())
 report={'dataset':a.dataset,'rows':len(t),'numeric_sha256':digest,'matches_bundled_values_in_order':digest==meta['numeric_sha256']}
 print(json.dumps(report,indent=2))
 if digest!=meta['numeric_sha256']:raise SystemExit('Official values differ; do not silently overwrite the teaching snapshot.')
if __name__=='__main__':main()
