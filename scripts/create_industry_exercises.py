from pathlib import Path
import json
import nbformat as nb
ROOT=Path(__file__).resolve().parents[1]
E=[]
def item(case,n,title,spec,signature,solution,checks,explanation):
    E.append(dict(id=f'{case}.C{n}',case=case,title=title,spec=spec,signature=signature,solution=solution,checks=checks,explanation=explanation))
item('wdbc',1,'Read the label map','Given loader labels 0 or 1, return integer 1 for malignant (original 0), else 0. Reject other labels.','malignant_indicator(labels)',
'''def malignant_indicator(labels):
    a=np.asarray(labels)
    if not np.isin(a,[0,1]).all(): raise ValueError('Unknown loader label')
    return (a==0).astype(int)''',
"np.testing.assert_array_equal(malignant_indicator([0,1,0]),[1,0,1])\ntry: malignant_indicator([2])\nexcept ValueError: pass\nelse: raise AssertionError('Invalid label accepted')",
'Equality creates a Boolean mask; converting it to integer gives 1/0. The explicit map is necessary because numeric label order is not universal.')
item('wdbc',2,'Count errors','For aligned nonempty binary vectors return (true negatives,false positives,false negatives,true positives).','confusion_counts(actual,predicted)',
'''def confusion_counts(actual,predicted):
    a,p=np.asarray(actual),np.asarray(predicted)
    if a.shape!=p.shape or a.ndim!=1 or not len(a) or not np.isin(a,[0,1]).all() or not np.isin(p,[0,1]).all(): raise ValueError('Binary aligned vectors required')
    return tuple(int(np.sum((a==t)&(p==q))) for t,q in [(0,0),(0,1),(1,0),(1,1)])''',
"assert confusion_counts([0,0,1,1],[0,1,0,1])==(1,1,1,1)\nassert confusion_counts([0,1],[0,0])==(1,0,1,0)",
'Count each actual/predicted pair separately; do not swap the row meaning and column meaning.')
item('wdbc',3,'Calculate balanced accuracy','For aligned binary vectors with both actual classes present, average recall for class 0 and class 1.','balanced_binary(actual,predicted)',
'''def balanced_binary(actual,predicted):
    a,p=np.asarray(actual),np.asarray(predicted)
    if a.shape!=p.shape or a.ndim!=1 or set(a)!={0,1} or not np.isin(p,[0,1]).all(): raise ValueError('Two actual classes required')
    return float(np.mean([np.mean(p[a==c]==c) for c in (0,1)]))''',
"assert balanced_binary([0,0,0,1],[0,0,0,0])==.5\nassert balanced_binary([0,1],[0,1])==1",
'Each actual class contributes one recall regardless of how many rows belong to it. This does not certify clinical usefulness.')
item('wine',1,'Use fitted scaling','Standardize a finite 2-D matrix using supplied training means and positive scales. Do not calculate new means.','apply_scale(x,mean,scale)',
'''def apply_scale(x,mean,scale):
    a,m,s=np.asarray(x,float),np.asarray(mean,float),np.asarray(scale,float)
    if a.ndim!=2 or m.shape!=(a.shape[1],) or s.shape!=m.shape or np.any(s<=0): raise ValueError('Incompatible shape or scale')
    return (a-m)/s''',
"np.testing.assert_allclose(apply_scale([[101,5]],[2,5],[1,1]),[[99,0]])\nnp.testing.assert_allclose(apply_scale([[2,4]],[1,2],[1,2]),[[1,1]])",
'The training transformation is frozen. Recalculating it on the test query would change the model definition.')
item('wine',2,'Choose nearby reference points','Return indices of the k nearest reference points to a query using Euclidean distance; preserve input order on ties.','nearest_reference(query,reference,k)',
'''def nearest_reference(query,reference,k):
    q,a=np.asarray(query,float),np.asarray(reference,float)
    if a.ndim!=2 or q.shape!=(a.shape[1],) or not 1<=k<=len(a): raise ValueError('Bad neighbor request')
    return np.argsort(np.linalg.norm(a-q,axis=1),kind='stable')[:k]''',
"np.testing.assert_array_equal(nearest_reference([0,0],[[4,0],[1,0],[2,0]],2),[1,2])\nnp.testing.assert_array_equal(nearest_reference([0],[[1],[-1]],2),[0,1])",
'Distance selects neighbors; sorting indices preserves the link back to the training rows. The tie convention differs explicitly from the production teaching descriptor’s coordinate-based tie rule.')
item('wine',3,'Filter finite lifetimes','Given an n-by-2 birth/death array, return death-birth for finite positive-lifetime intervals only.','finite_lifetimes(diagram)',
'''def finite_lifetimes(diagram):
    a=np.asarray(diagram,float).reshape(-1,2)
    valid=np.isfinite(a).all(axis=1)&(a[:,1]>a[:,0])
    return a[valid,1]-a[valid,0]''',
"np.testing.assert_allclose(finite_lifetimes([[0,1],[2,2],[0,np.inf],[3,5]]),[1,2])\nassert finite_lifetimes([]).size==0",
'Essential classes need separate handling. Silently averaging infinity is not a meaningful finite persistence statistic.')
item('stackloss',1,'Compute MAE','Return mean absolute error for aligned nonempty finite vectors.','mean_absolute_error_hand(actual,predicted)',
'''def mean_absolute_error_hand(actual,predicted):
    a,p=np.asarray(actual,float),np.asarray(predicted,float)
    if a.shape!=p.shape or a.ndim!=1 or not len(a) or not np.isfinite(a).all() or not np.isfinite(p).all(): raise ValueError('Finite aligned vectors required')
    return float(np.mean(np.abs(a-p)))''',
"assert mean_absolute_error_hand([10,12],[11,8])==2.5\nassert mean_absolute_error_hand([1],[1])==0",
'Absolute value removes the direction of error; averaging retains the response unit but can hide extreme failures.')
item('stackloss',2,'Keep signed residuals','Return observed minus predicted; the sign convention must be explicit.','signed_residual(actual,predicted)',
'''def signed_residual(actual,predicted):
    a,p=np.asarray(actual,float),np.asarray(predicted,float)
    if a.shape!=p.shape: raise ValueError('Shapes differ')
    return a-p''',
"np.testing.assert_array_equal(signed_residual([10,12],[11,8]),[-1,4])\nnp.testing.assert_array_equal(signed_residual([20],[15]),[5])",
'A positive residual under this convention means the prediction was too low. Another convention is possible only when declared.')
item('stackloss',3,'Leave one row out','Return all integer indices from 0 to n-1 except the specified omitted index.','leave_out_indices(n,omitted)',
'''def leave_out_indices(n,omitted):
    if n<2 or not 0<=omitted<n: raise ValueError('Invalid omission')
    return np.array([i for i in range(n) if i!=omitted],dtype=int)''',
"np.testing.assert_array_equal(leave_out_indices(4,1),[0,2,3])\nassert 0 not in leave_out_indices(3,0)",
'The scaler and model must both be refit on these indices, not only the model.')
item('grunfeld',1,'Lag within an entity','Sort a table by firm and year and add lag_invest from the previous row within the same firm. Keep first records missing.','lag_investment(table)',
'''def lag_investment(table):
    result=table.sort_values(['firm','year']).copy()
    result['lag_invest']=result.groupby('firm')['invest'].shift(1)
    return result''',
"t=pd.DataFrame({'firm':['A','B','A','B'],'year':[1,1,2,2],'invest':[10,90,20,80]})\nr=lag_investment(t)\nassert r.loc[2,'lag_invest']==10 and r.loc[3,'lag_invest']==90\nassert r.loc[[0,1],'lag_invest'].isna().all()",
'Group boundaries are information boundaries. A global shift would mix different companies.')
item('grunfeld',2,'Enforce a cutoff','Return indices with timestamp strictly earlier than the supplied decision cutoff.','before_cutoff(times,cutoff)',
'''def before_cutoff(times,cutoff):
    return np.flatnonzero(np.asarray(times)<cutoff)''',
"np.testing.assert_array_equal(before_cutoff([1947,1948,1948,1950],1948),[0])\nassert len(before_cutoff([3],3))==0",
'Strictly earlier differs from earlier-or-equal. Decide how simultaneous measurements become available.')
item('grunfeld',3,'Find shared entities','Return the set of entities appearing in both partitions.','shared_entities(first,second)',
'''def shared_entities(first,second):
    return set(first)&set(second)''',
"assert shared_entities(['A','B','A'],['C','B'])=={'B'}\nassert shared_entities([1,2],[3])==set()",
'Entity overlap can be acceptable for future-known-firm evaluation but invalid for a new-firm claim.')
item('co2',1,'Preserve a missingness mask','For a vector and positive window length, return starting indices of finite contiguous windows. This task checks rows only; time-spacing validation is a separate obligation.','finite_window_starts(values,length)',
'''def finite_window_starts(values,length):
    a=np.asarray(values,float)
    if a.ndim!=1 or length<1: raise ValueError('Invalid window request')
    return np.array([i for i in range(len(a)-length+1) if np.isfinite(a[i:i+length]).all()],dtype=int)''',
"np.testing.assert_array_equal(finite_window_starts([1,2,np.nan,4,5],2),[0,3])\nassert len(finite_window_starts([1],2))==0",
'A finite contiguous row window is necessary but not sufficient: real time gaps must also be checked.')
item('co2',2,'Separate past and target','For a finite vector make length-L feature windows and one-step targets. Return (x,y), including correctly shaped empty arrays.','one_step_examples(values,length)',
'''def one_step_examples(values,length):
    a=np.asarray(values,float)
    if a.ndim!=1 or length<1 or not np.isfinite(a).all(): raise ValueError('Finite vector required')
    n=max(0,len(a)-length)
    return np.array([a[i:i+length] for i in range(n)],float).reshape(n,length),a[length:].copy()''',
"x,y=one_step_examples([0,1,2,3,4],3)\nnp.testing.assert_array_equal(x,[[0,1,2],[1,2,3]])\nnp.testing.assert_array_equal(y,[3,4])",
'The target is not included in its own features. Reading later true observations for later predictions is observed-history evaluation.')
item('co2',3,'Check the entire support','Return whether every integer index from start through target inclusive belongs to the allowed partition.','support_inside(start,target,allowed)',
'''def support_inside(start,target,allowed):
    if start>target: raise ValueError('Start follows target')
    return set(range(start,target+1))<=set(allowed)''',
"assert support_inside(1,3,[0,1,2,3])\nassert not support_inside(1,3,[1,3])",
'Checking only the final target misses leakage through an earlier feature or an intermediate observation.')
item('nile',1,'Convert units explicitly','Convert annual volumes expressed in 10^8 cubic metres to cubic metres. Do not call the output a rate.','volume_in_cubic_metres(source_volume)',
'''def volume_in_cubic_metres(source_volume):
    return np.asarray(source_volume,float)*1e8''',
"np.testing.assert_allclose(volume_in_cubic_metres([1,2.5]),[1e8,2.5e8])",
'The conversion changes representation, not information about peaks or subannual timing.')
item('nile',2,'Score a candidate split','For a finite vector and split k with two nonempty segments, return the within-segment squared error around each segment mean.','two_mean_sse(values,k)',
'''def two_mean_sse(values,k):
    a=np.asarray(values,float)
    if not 0<k<len(a) or not np.isfinite(a).all(): raise ValueError('Two finite segments required')
    return float(np.sum((a[:k]-a[:k].mean())**2)+np.sum((a[k:]-a[k:].mean())**2))''',
"assert two_mean_sse([0,0,1,1],2)==0\nassert two_mean_sse([0,0,1,1],1)>0",
'Minimizing this across many k is a search; the selected minimum is not automatically a significance test.')
item('nile',3,'Divide by the actual elapsed time','Return successive finite-difference rates for aligned finite values and strictly increasing times.','difference_rates(values,times)',
'''def difference_rates(values,times):
    a,t=np.asarray(values,float),np.asarray(times,float)
    if a.shape!=t.shape or a.ndim!=1 or len(a)<2 or np.any(np.diff(t)<=0) or not np.isfinite(a).all() or not np.isfinite(t).all(): raise ValueError('Aligned increasing times required')
    return np.diff(a)/np.diff(t)''',
"np.testing.assert_allclose(difference_rates([0,2,8],[0,1,4]),[2,2])",
'A difference in annual volume per year is not the instantaneous river-discharge signal. Units propagate through the calculation.')
item('elnino',1,'Respect calendar order','Given YEAR and JAN..DEC columns, return a 1-D vector in year-sorted calendar order.','calendar_vector(table)',
'''def calendar_vector(table):
    names=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    return table.sort_values('YEAR')[names].to_numpy(float).ravel()''',
"t=pd.DataFrame({'YEAR':[2001,2000],**{m:[i+13,i+1] for i,m in enumerate(['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'])}})\nnp.testing.assert_array_equal(calendar_vector(t),np.arange(1,25))",
'Column names are not alphabetically ordered times; the explicit month sequence preserves meaning.')
item('elnino',2,'Fit only a supplied reference period','For finite values and corresponding month labels 1..12, return twelve monthly means; require all months.','monthly_reference(values,months)',
'''def monthly_reference(values,months):
    a,m=np.asarray(values,float),np.asarray(months)
    if a.shape!=m.shape or set(m)!=set(range(1,13)) or not np.isfinite(a).all(): raise ValueError('All twelve months required')
    return np.array([a[m==j].mean() for j in range(1,13)])''',
"m=np.tile(np.arange(1,13),2)\nnp.testing.assert_allclose(monthly_reference(m.astype(float),m),np.arange(1,13))",
'Which rows you pass determines the fitted climatology. The function cannot infer the training boundary for you.')
item('elnino',3,'Compute anomalies against a fixed baseline','Subtract each value’s month-specific mean from a supplied length-12 reference.','monthly_anomalies(values,months,reference)',
'''def monthly_anomalies(values,months,reference):
    a,m,r=np.asarray(values,float),np.asarray(months,int),np.asarray(reference,float)
    if a.shape!=m.shape or r.shape!=(12,) or not np.isin(m,np.arange(1,13)).all(): raise ValueError('Bad month or reference shape')
    return a-r[m-1]''',
"np.testing.assert_allclose(monthly_anomalies([25.5,22],[1,2],[24,20]+[0]*10),[1.5,2])",
'A positive anomaly is relative to a declared baseline, not an absolute category of climate behavior.')
item('modechoice',1,'Recover one selected mode per person','Validate four modes and one selected alternative per individual, then return a Series of selected modes indexed by individual.','selected_modes(table)',
'''def selected_modes(table):
    result={}
    for person,g in table.groupby('individual',sort=True):
        if len(g)!=4 or set(g['mode'])!={1,2,3,4} or not g.choice.isin([0,1]).all() or g.choice.sum()!=1: raise ValueError('Invalid choice set')
        result[person]=int(g.loc[g.choice==1,'mode'].iloc[0])
    return pd.Series(result,dtype=int)''',
"t=pd.DataFrame({'individual':[1]*4,'mode':[1,2,3,4],'choice':[0,1,0,0]})\nassert selected_modes(t).loc[1]==2",
'Four alternative rows contain one decision. Invalid choice sets must not silently create extra labels.')
item('modechoice',2,'Build a cheapest-mode baseline','Given an n-by-4 finite cost matrix ordered air/train/bus/car, return mode codes1..4; choose the first mode on ties.','cheapest_mode(costs)',
'''def cheapest_mode(costs):
    a=np.asarray(costs,float)
    if a.ndim!=2 or a.shape[1]!=4 or not np.isfinite(a).all(): raise ValueError('Four finite offered costs required')
    return np.argmin(a,axis=1)+1''',
"np.testing.assert_array_equal(cheapest_mode([[4,2,3,1],[1,1,2,3]]),[4,1])",
'A baseline embodies a simple assumption; it is not a claim that all people minimize ticket price.')
item('modechoice',3,'Check disjoint travelers','Return True precisely when the two identifier collections share no member.','groups_disjoint(train_ids,test_ids)',
'''def groups_disjoint(train_ids,test_ids):
    return not bool(set(train_ids)&set(test_ids))''',
"assert groups_disjoint([1,1,2],[3,4])\nassert not groups_disjoint([1,2],[2,3])",
'Apply the same principle to athletes, patients and experiment runs. Disjoint rows alone do not establish disjoint entities.')
(ROOT/'industry/exercises.json').write_text(json.dumps(E,indent=2))
for case in sorted(set(x['case'] for x in E)):
    activities=[x for x in E if x['case']==case]
    for answer in (False,True):
        kind='answers' if answer else 'learner'
        cells=[nb.v4.new_markdown_cell(f'# {case}: '+('worked coding answers' if answer else 'independent coding practice')+'\n\nRead the [case lesson](../lessons/'+case+'.md). '+('Every reference function below has executed checks. Compare only after attempting.' if answer else 'The functions below intentionally raise NotImplementedError. Replace those bodies yourself; they are not unfinished reference software.')+'\n\nThese checks verify limited function contracts, not your scientific interpretation.'),nb.v4.new_code_cell('import numpy as np\nimport pandas as pd')]
        for e in activities:
            cells.append(nb.v4.new_markdown_cell(f'## {e["id"]} — {e["title"]}\n\n{e["spec"]}\n\nPredict the check output before writing your function.'))
            cells.append(nb.v4.new_code_cell(e['solution'] if answer else 'def '+e['signature']+':\n    raise NotImplementedError("Independent learner exercise '+e['id']+'")'))
            cells.append(nb.v4.new_code_cell(e['checks']+'\nprint("'+e['id']+' checks passed")'))
            if answer:cells.append(nb.v4.new_markdown_cell('**Why it works:** '+e['explanation']))
        obj=nb.v4.new_notebook(cells=cells,metadata={'kernelspec':{'name':'python3','language':'python','display_name':'Python 3'},'learning_role':'coding_reference' if answer else 'learner_assignment'})
        nb.write(obj,ROOT/f'industry/{kind}/{case}.ipynb')
print('Built',len(E),'activities in eight learner and eight reference notebooks')
