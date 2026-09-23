"""Rebuild the explicitly transcribed 56-row NIST Hahn1 excerpt; no network.

Source web lines 60–115 (zero-based), numeric observations 1–56. This is NOT the
full 236-row certified benchmark. See manifest for the limits of this subset.
"""
from pathlib import Path
import csv, json, hashlib
ROOT=Path(__file__).resolve().parents[1]
TEXT='''
.591 24.41
1.547 34.82
2.902 44.09
2.894 45.07
4.703 54.98
6.307 65.51
7.03 70.53
7.898 75.70
9.470 89.57
9.484 91.14
10.072 96.40
10.163 97.19
11.615 114.26
12.005 120.25
12.478 127.08
12.982 133.55
12.970 133.61
13.926 158.67
14.452 172.74
14.404 171.31
15.190 202.14
15.550 220.55
15.528 221.05
15.499 221.39
16.131 250.99
16.438 268.99
16.387 271.80
16.549 271.97
16.872 321.31
16.830 321.69
16.926 330.14
16.907 333.03
16.966 333.47
17.060 340.77
17.122 345.65
17.311 373.11
17.355 373.79
17.668 411.82
17.767 419.51
17.803 421.59
17.765 422.02
17.768 422.47
17.736 422.61
17.858 441.75
17.877 447.41
17.912 448.7
18.046 472.89
18.085 476.69
18.291 522.47
18.357 522.62
18.426 524.43
18.584 546.75
18.610 549.53
18.870 575.29
18.795 576.00
19.111 625.55
'''
def main():
    path=ROOT/'data/physics/hahn1_excerpt.csv';path.parent.mkdir(exist_ok=True)
    with path.open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['source_observation','temperature_K','expansion_response'])
        for i,line in enumerate(TEXT.strip().splitlines(),1):
            y,x=line.split();w.writerow([i,x,y])
    meta={'name':'NIST Hahn1 — first 56 observations only','source_url':'https://www.itl.nist.gov/div898/strd/nls/data/LINKS/DATA/Hahn1.dat',
          'review_date':'2026-09-20','origin':'Observed copper thermal-expansion study; NIST/ITL StRD',
          'capture':'Numeric transcription from web-visible official source; not a byte-for-byte original download.',
          'selection':'Observations 1–56 of 236, original order retained. Selection fixed before model fitting.',
          'rows':56,'original_rows':236,'temperature_unit':'kelvin',
          'response_unit':'Original source response scale; dimensional multiplier not specified in the source file.',
          'time_axis':False,'replicate_ids_available':False,
          'unsupported_claims':['PDE solution accuracy','thermal diffusivity identification','energy conservation','NIST full-data certified residual replication','new independent benchmark'],
          'permission':'U.S. NIST reference data; attributed. No third-party photographs or full papers added.',
          'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (path.parent/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
if __name__=='__main__':main()
