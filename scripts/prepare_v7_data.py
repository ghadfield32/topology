"""Normalize the complete source tables transcribed from official web text.

This preserves observed numeric values; it does not recreate raw provider bytes.
Run only when intentionally rebuilding data and review all hash changes.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from shape_lab.evidence_v7 import numeric_digest
D=ROOT/'data/v7'
configs={
 'seeds':dict(source='source_numeric.txt',sep=r'\s+',header=None,rows=210,
  columns=['area','perimeter','compactness','kernel_length','kernel_width','asymmetry','groove_length','variety'],
  features=['area','perimeter','compactness','kernel_length','kernel_width','asymmetry','groove_length'],
  targets=['variety'],units={'area':'not specified in inspected UCI metadata','perimeter':'not specified in inspected UCI metadata','compactness':'dimensionless if A and P use consistent units','kernel_length':'not specified','kernel_width':'not specified','asymmetry':'definition/unit not specified','groove_length':'not specified','variety':'categorical label, not a magnitude'},
  doi='10.24432/C5H30K',citation='Charytanowicz, Niewczas, Kulczycki, Kowalski and Lukasik (2010). Seeds. UCI Machine Learning Repository.',
  url='https://archive.ics.uci.edu/dataset/236/seeds',raw_url='https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt',
  observation='One wheat kernel described by seven extracted geometric measurements; original X-ray images are not bundled.',
  unknowns=['Field/plant/batch identifiers and acquisition dates unavailable in table','Physical area and length units not given in inspected repository entry','Cultivar integer mapping retained as 1,2,3; named varieties are Kama, Rosa and Canadian, but numeric-to-name mapping not independently verified'],
  limitations=['Balanced historical collection; does not estimate field prevalence','Classification is not disease diagnosis or yield forecasting','Compactness is derived geometry, not a topological invariant']),
 'concrete_slump':dict(source='source_numeric.csv',sep=',',header=0,rows=103,
  columns=['source_id','cement_kg_m3','slag_kg_m3','fly_ash_kg_m3','water_kg_m3','sp_kg_m3','coarse_aggregate_kg_m3','fine_aggregate_kg_m3','slump_cm','flow_cm','strength_mpa'],
  features=['cement_kg_m3','slag_kg_m3','fly_ash_kg_m3','water_kg_m3','sp_kg_m3','coarse_aggregate_kg_m3','fine_aggregate_kg_m3'],
  targets=['slump_cm','flow_cm','strength_mpa'],units={'source_id':'provider row identifier; not physical quantity','ingredients':'kg in one cubic metre of concrete','slump_cm':'cm','flow_cm':'cm','strength_mpa':'MPa at 28 days'},
  doi='10.24432/C5FG7D',citation='Yeh, I. (2007). Concrete Slump Test. UCI Machine Learning Repository.',
  url='https://archive.ics.uci.edu/dataset/182/concrete+slump+test',raw_url='https://archive.ics.uci.edu/ml/machine-learning-databases/concrete/slump/slump_test.data',
  observation='One recorded concrete mixture/test with seven composition inputs and three measured responses.',
  unknowns=['Exact collection dates and physical batch identifiers are not supplied','UCI says 78 initial and 25 later observations; row order alone is not an authenticated time split'],
  limitations=['Not the 1030-row Concrete Compressive Strength dataset','Three outputs are not interchangeable; the lab predicts strength from ingredients only','No structural engineering certification or per-recipe guaranteed interval'])}
for name,c in configs.items():
 folder=D/name;source=folder/c['source']
 a=pd.read_csv(source,sep=c['sep'],header=c['header'],dtype=str)
 if a.shape!=(c['rows'],len(c['columns'])):raise ValueError((name,a.shape))
 tokens=a.values.tolist();a.columns=c['columns'];table=a.apply(pd.to_numeric)
 if name=='seeds':
  assert table.variety.value_counts().to_dict()=={1:70,2:70,3:70}
  table.insert(0,'source_id',np.arange(1,211))
 else:assert list(table.source_id)==list(range(1,104))
 table.to_csv(folder/'table.csv',index=False,lineterminator='\n')
 meta={k:v for k,v in c.items() if k not in ['source','sep','header']}
 meta.update(name=name,columns=list(table),license='CC BY 4.0',license_url='https://creativecommons.org/licenses/by/4.0/',
  retrieved='2026-09-21',provenance_kind='observed',
  acquisition='All numeric records transcribed from official plaintext returned by web retrieval. Whitespace normalized. Direct container download failed (DNS/network). No claim of provider-byte checksum verification.',
  modifications=['Whitespace/column naming normalized','Generated 1-based source_id for Seeds only','No rows dropped or numerical values intentionally altered'],
  numeric_sha256=numeric_digest(tokens),numeric_columns_in_source=len(c['columns']),
  remote_numeric_verification='not executed in build environment',
  files_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,folder/'table.csv']})
 (folder/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 print(name,table.shape,meta['numeric_sha256'])
