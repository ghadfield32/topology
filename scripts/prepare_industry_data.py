"""Rebuild the eight v6 snapshots from explicitly versioned local distributions.

This is an export step, NOT a network download. Run only to intentionally rebuild
snapshots; normal lessons read bundled CSVs. Existing snapshots require --replace.
"""
from pathlib import Path
import argparse, hashlib, json, shutil
import numpy as np
import pandas as pd
import sklearn
from sklearn.datasets import load_breast_cancer, load_wine
import statsmodels
import statsmodels.datasets as smd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/industries'
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def export(replace=False):
    if (OUT/'catalog.json').exists() and not replace:
        raise FileExistsError('Snapshots exist. Use --replace only for an intentional rebuild, then rerun verification.')
    OUT.mkdir(parents=True,exist_ok=True)
    catalog=[]
    specs=[
      ('wdbc','healthcare','Cell-image measurements and honest classification','sklearn','breast_cancer',
       'https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic','10.24432/C5DW2B','CC BY 4.0',
       'Wolberg, Mangasarian, Street and Street (1993), Breast Cancer Wisconsin (Diagnostic), UCI.',
       'One digitized fine-needle-aspirate image summary. The scikit-learn snapshot does not retain original IDs.',
       '569 rows; 30 features. Educational observational data, not clinical validation.'),
      ('wine','food_chemistry','Chemistry, scale and out-of-sample topological descriptors','sklearn','wine',
       'https://archive.ics.uci.edu/dataset/109/wine','10.24432/C5PC7J','CC BY 4.0',
       'Aeberhard and Forina (1992), Wine, UCI Machine Learning Repository.',
       'One wine sample; cultivar is a category, not a quality score.',
       '178 rows, 13 chemistry features, three cultivars. Different from Wine Quality (UCI 186).'),
      ('stackloss','manufacturing','Small-sample process monitoring','statsmodels','stackloss',
       'https://www.statsmodels.org/stable/datasets/generated/stackloss.html',None,'Public domain (dataset distributor statement)',
       'Brownlee (1965), Statistical Theory and Methodology in Science and Engineering; statsmodels distribution.',
       'One operating-day measurement in the historical plant table; original timestamps are unavailable.',
       '21 records. Cannot support a broad plant-deployment claim or certify a mechanistic model.'),
      ('grunfeld','business','Firm panels, timestamps and prediction availability','statsmodels','grunfeld',
       'https://www.statsmodels.org/stable/datasets/generated/grunfeld.html',None,'Public domain (dataset distributor statement)',
       'Grunfeld; 11-firm reconstruction documented by Kleiber and Zeileis (2008); statsmodels distribution.',
       'One firm-year record. A repeated firm is not a new independent company.',
       '220 rows; 11 firms, 1935–1954. Historical data, not investment advice or current-market evidence.'),
      ('co2','environment','Missingness, past-only windows and seasonal shape','statsmodels','co2',
       'https://www.statsmodels.org/stable/datasets/generated/co2.html',None,'Public domain (dataset distributor statement)',
       'Keeling and Whorf (2004), atmospheric CO2 series, CDIAC; historical statsmodels snapshot.',
       'One weekly date slot, possibly missing a CO2 observation.',
       '2284 slots, 2225 observed values and 59 missing. Snapshot covers 1958–2001, not current CO2.'),
      ('nile','water_infrastructure','Retrospective change and forward evaluation','statsmodels','nile',
       'https://www.statsmodels.org/stable/datasets/generated/nile.html',None,'Public domain (dataset distributor statement)',
       'Cobb (1978), The Problem of the Nile; statsmodels distribution.',
       'One annual river-volume observation, not an instantaneous discharge-rate sample.',
       '100 annual observations, 1871–1970. A detected change is not proof of its physical cause.'),
      ('elnino','marine','Monthly climate records and delay representations','statsmodels','elnino',
       'https://www.statsmodels.org/stable/datasets/generated/elnino.html',None,'Public domain (dataset distributor statement)',
       'NOAA NWS ERSST.V3B, Niño 1+2; historical statsmodels distribution.',
       'One year with twelve monthly regional mean temperatures; the derived long view has one month per row.',
       '61 years, 1950–2010, 732 monthly observations. Not an operational forecast or a simulated PDE field.'),
      ('modechoice','transportation','Choice sets, group splits and fair baselines','statsmodels','modechoice',
       'https://www.statsmodels.org/stable/datasets/generated/modechoice.html',None,'Public domain (dataset distributor statement)',
       'Greene and Hensher, 1987 intercity mode-choice sample documented in Greene (1997/2011); statsmodels distribution.',
       'One alternative offered to one traveler. Four rows form one choice set.',
       '840 alternatives, 210 travelers. Choice-based sampling oversamples some modes; not population market shares.')]
    for id,sector,title,provider,name,url,doi,license,citation,unit,limits in specs:
        d=OUT/id; d.mkdir(exist_ok=True)
        if provider=='sklearn':
            bunch=(load_breast_cancer if name=='breast_cancer' else load_wine)()
            table=pd.DataFrame(bunch.data,columns=[str(x).replace(' ','_').replace('/','_') for x in bunch.feature_names])
            table['label']=bunch.target.astype(int)
            table.insert(0,'row_id',np.arange(len(table),dtype=int))
            raw=Path(sklearn.__file__).parent/'datasets/data'/('breast_cancer.csv' if name=='breast_cancer' else 'wine_data.csv')
            version=sklearn.__version__; label_map={str(i):str(x) for i,x in enumerate(bunch.target_names)}
            if id=='wdbc': label_map={'0':'malignant','1':'benign'}
        else:
            mod=getattr(smd,name);table=mod.load_pandas().data.copy()
            raw=Path(mod.__file__).parent/f'{name}.csv';version=statsmodels.__version__;label_map={}
            if id=='co2':table=table.rename_axis('date').reset_index();table['date']=table['date'].dt.strftime('%Y-%m-%d')
            table.insert(0,'row_id',np.arange(len(table),dtype=int))
            for c in ['year','YEAR','individual','mode','choice']:
                if c in table:table[c]=table[c].astype(int)
        dest=d/'source_distribution.csv';shutil.copyfile(raw,dest)
        table.to_csv(d/'data.csv',index=False,float_format='%.12g',lineterminator='\n')
        item={'id':id,'sector':sector,'title':title,'provider':provider,'provider_version':version,
              'source_url':url,'source_doi':doi,'citation':citation,'license':license,
              'license_evidence_url':url,'license_url':'https://creativecommons.org/licenses/by/4.0/' if provider=='sklearn' else url,
              'observation_unit':unit,'scope_limitations':limits,'rows':len(table),'columns':list(table.columns),
              'label_map':label_map,'data_kind':'observed','acquisition':'offline export from installed package distribution; no invented records',
              'source_review_date':'2026-09-20','data_file':f'data/industries/{id}/data.csv',
              'data_sha256':digest(d/'data.csv'),'source_file':f'data/industries/{id}/source_distribution.csv',
              'source_sha256':digest(dest),'missing_by_column':{c:int(table[c].isna().sum()) for c in table},
              'transforms':['Preserved package data values and row order; added zero-based row_id.',
                  'Normalized CSV serialization; replaced spaces/slashes in sklearn feature names.',
                  'Provider label codes preserved and mapped explicitly; not original UCI IDs.'] if provider=='sklearn' else
                  ['Preserved loaded values and row order; added zero-based row_id.',
                   'Calendar fields cast to integers; CO2 datetime index exported as ISO date.',
                   'Missing CO2 observations remain blank, never zero.'],
              'schema':[]}
        for c in table:
            role='metadata' if c in ['row_id','date','year','YEAR','individual','firm','mode'] else 'feature'
            if c in ['label','STACKLOSS','invest','choice','co2','volume'] or (id=='elnino' and c not in ['row_id','YEAR']):role='response_or_signal'
            item['schema'].append({'name':c,'role':role,'dtype':str(table[c].dtype),'units':'source scale; see data card (not guessed)','description':c.replace('_',' ')})
        if id=='wdbc':
            for f in item['schema']:
                if f['name'] not in ['row_id','label']:
                    f['description']='Image-derived nuclear '+f['name'].replace('_',' ')+'; not a raw medical image.'
                    f['units']='source image/derived scale; physical calibration not specified in the cited summary'
        if id=='wine':
            for f in item['schema']:
                if f['role']=='feature':f['description']='Chemistry measurement: '+f['name'].replace('_',' ')+'. Original source does not specify every unit.'
        defs={
          'stackloss':{'STACKLOSS':('10 × percent','Ammonia escaping the absorption column on the source encoded scale.'),'AIRFLOW':('source process-rate scale','Rate of plant operation; do not invent a flow unit.'),'WATERTEMP':('source temperature scale','Cooling-water temperature; no calibrated unit is asserted here.'),'ACIDCONC':('encoded concentration','Source wording of offset/scaling is ambiguous; preserve encoded values, do not invert the transform.')},
          'grunfeld':{'invest':('1947-dollar source scale','Gross investment; no additional millions multiplier is assumed.'),'value':('1947-dollar source scale','Year-end market value; not available at the beginning of that same year.'),'capital':('1947-dollar source scale','Stock of plant and equipment.'),'year':('calendar year','1935–1954.'),'firm':('category','Company identity; eleven labels.')},
          'co2':{'date':('ISO date','Weekly calendar slot from the loaded index; no intraday timestamp asserted.'),'co2':('ppmv','Atmospheric CO2 concentration; blanks are missing.')},
          'nile':{'year':('calendar year','1871–1970.'),'volume':('10^8 m^3 per annual observation','Annual recorded volume; do not label as cubic metres per second.')},
          'modechoice':{'individual':('ID','One traveler/choice-set identifier.'),'mode':('category','1 air; 2 train; 3 bus; 4 car.'),'choice':('binary','One selected alternative per choice set.'),'ttme':('minutes','Terminal waiting time, zero for car.'),'invc':('source dollars','In-vehicle monetary cost; not inflation-adjusted here.'),'invt':('minutes','In-vehicle travel time.'),'gc':('source dollars','Generalized cost combining cost and time; excluded to avoid double-counting.'),'hinc':('source thousands of dollars','Household income.'),'psize':('persons','Group size in the chosen mode; excluded because availability for prospective choice is uncertain.')}}
        for f in item['schema']:
            if f['name'] in defs.get(id,{}):f['units'],f['description']=defs[id][f['name']]
            if id=='elnino' and f['name'] not in ['row_id','YEAR']:
                f['units']='degrees Celsius';f['description']='Regional monthly mean sea-surface temperature for '+f['name']+'.'
        (d/'metadata.json').write_text(json.dumps(item,indent=2,ensure_ascii=False)+'\n')
        catalog.append(item)
    (OUT/'catalog.json').write_text(json.dumps({'schema_version':1,'snapshot':'v6','datasets':catalog},indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'datasets':len(catalog),'canonical_rows':sum(x['rows'] for x in catalog),'providers':{'sklearn':sklearn.__version__,'statsmodels':statsmodels.__version__}},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--replace',action='store_true');args=p.parse_args();export(args.replace)
