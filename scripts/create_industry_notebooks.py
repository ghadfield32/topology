"""Build original, source-linked teaching notebooks (execution is a separate step)."""
from pathlib import Path
import json, textwrap
import nbformat as nbf
ROOT=Path(__file__).resolve().parents[1]
SETUP='''from pathlib import Path
import sys, json, hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, Ridge, LinearRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss, mean_absolute_error, mean_squared_error, roc_auc_score, confusion_matrix
ROOT = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p / "src/shape_lab").is_dir())
sys.path.insert(0, str(ROOT / "src"))
from shape_lab.industries import *
from shape_lab.persistence import rips_filtration, persistent_homology, diagram
CASE = "CASE_ID"
OUT = ROOT / "reports/v6/industries" / CASE
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20260920

def write_json(name, value):
    def convert(x):
        if isinstance(x, np.ndarray): return x.tolist()
        if isinstance(x, np.generic): return x.item()
        raise TypeError(type(x).__name__)
    (OUT / name).write_text(json.dumps(value, indent=2, default=convert, allow_nan=False))

def plot_done(name):
    plt.tight_layout()
    plt.savefig(OUT / (name + ".png"), dpi=125)
    plt.show()

def regression_metrics(y, pred):
    return {"mae":float(mean_absolute_error(y,pred)),"rmse":float(mean_squared_error(y,pred)**.5)}

def class_metrics(y, pred):
    return {"accuracy":float(accuracy_score(y,pred)),"balanced_accuracy":float(balanced_accuracy_score(y,pred))}

def stratified_split(y):
    index=np.arange(len(y))
    train, other=train_test_split(index,test_size=.4,random_state=SEED,stratify=y)
    val,test=train_test_split(other,test_size=.5,random_state=SEED,stratify=y[other])
    return {"train":np.sort(train),"validation":np.sort(val),"test":np.sort(test)}

def save_split(split, ids):
    frames=[pd.DataFrame({"example_index":v,"source_id":np.asarray(ids)[v],"partition":k}) for k,v in split.items()]
    pd.concat(frames,ignore_index=True).to_csv(OUT / "split.csv",index=False)

def topology_report(points, name):
    bars=persistent_homology(rips_filtration(points,max_homology=1),max_dim=1)
    finite=[{"dimension":b.dim,"birth":b.birth,"death":b.death} for b in bars if np.isfinite(b.death)]
    write_json(name+".json",{"points":len(points),"coefficient_field":2,"edge_convention":"distance <= epsilon","finite_bars":finite,"essential_h0":1,"role":"exploratory descriptor, not significance"})
    plt.figure(figsize=(7,4))
    for dim in (0,1):
        a=diagram(bars,dim,finite_only=True)
        if len(a): plt.scatter(a[:,0],a[:,1],label="H"+str(dim),s=22)
    plt.xlabel("Birth (declared metric units)");plt.ylabel("Death (same units)");plt.title(name.replace('_',' '));plt.legend()
    plot_done(name)
    return finite

df, meta = load_dataset(CASE)
print(meta["title"])
print("Shape:",df.shape,"; snapshot SHA-256:",meta["data_sha256"])
print("Observation unit:",meta["observation_unit"])
display(df.head())
write_json("protocol.json",{"dataset":CASE,"seed":SEED,"data_sha256":meta["data_sha256"],"code_sha256":hashlib.sha256((ROOT/"src/shape_lab/industries.py").read_bytes()).hexdigest(),"data_kind":"observed","evaluation":"fixed teaching experiment; displayed test outcomes are now exposed","external_validation":False})
'''
CASES={}
def add(name,title,sections): CASES[name]=(title,sections)
add('wdbc','Healthcare: measurements are not a diagnosis',[
('1. Define the independent example before fitting','''Each row summarizes nuclei in a digitized fine-needle-aspirate image. These are not raw images. The sklearn snapshot lacks the original identifiers, so we cannot verify a patient-disjoint or hospital-disjoint test. We map **malignant to 1** explicitly. No threshold or model in this lesson is a clinical recommendation.\n\nPredict: which columns would leak the answer or identify a row rather than measure the specimen?''','''features=[c for c in df if c not in ("row_id","label")]
x=df[features].to_numpy(float)
y=(df.label.to_numpy()==0).astype(int)  # positive class = malignant
split=stratified_split(y);save_split(split,df.row_id)
scaler=TrainScaler.fit(x[split["train"]]);z=scaler.transform(x)
write_json("preprocessing.json",{"feature_names":features,"mean":scaler.mean,"scale":scaler.scale,"fit_rows":split["train"],"positive_class":"malignant"})
print({k:{"n":len(v),"malignant":int(y[v].sum())} for k,v in split.items()})
assert not(set(split["train"]) & set(split["test"]))'''),
('2. Establish a fixed, explainable baseline','''A logistic model maps a linear score to a number between zero and one. That number is not automatically calibrated for a new hospital. We fix C=1 before viewing validation or test results. Accuracy can hide unequal class performance, so we also report balanced accuracy, a confusion matrix, and ROC AUC. All preprocessing parameters come from training rows.''','''model=LogisticRegression(C=1,max_iter=3000,random_state=SEED).fit(z[split["train"]],y[split["train"]])
majority=int(np.bincount(y[split["train"]]).argmax());scores={}
for key in ("validation","test"):
    ix=split[key];p=model.predict_proba(z[ix])[:,1];pred=(p>=.5).astype(int)
    scores[key]={"logistic":class_metrics(y[ix],pred),"majority":class_metrics(y[ix],np.full(len(ix),majority)),"roc_auc":float(roc_auc_score(y[ix],p)),"confusion_true_rows_pred_columns":confusion_matrix(y[ix],pred).tolist(),"n":len(ix)}
    pd.DataFrame({"row_id":df.row_id.to_numpy()[ix],"malignant":y[ix],"probability_malignant":p,"prediction":pred}).to_csv(OUT/(key+"_predictions.csv"),index=False)
write_json("results.json",scores);display(pd.DataFrame({k:v["logistic"] for k,v in scores.items()}))'''),
('3. Ask a topological question at the correct level','''Now study the geometry of a fixed small training cohort. A persistence diagram belongs to this point cloud and its metric; it is not a separate diagnostic test for each row. A loop can reflect sampling, correlated features or preprocessing. Selecting the most dramatic diagram after inspecting labels would be exploratory selection, not an independent discovery.''','''sample=np.random.default_rng(SEED).choice(split["train"],size=28,replace=False)
write_json("topology_rows.json",sample)
_ = topology_report(z[sample],"training_cohort_persistence")
plt.figure(figsize=(7,4));plt.hist(model.predict_proba(z[split["test"]])[:,1],bins=12)
plt.xlabel("Model score for malignant class");plt.ylabel("Image summaries");plt.title("Held-out scores: not a calibration certificate")
plot_done("score_distribution")'''),
('4. Stop before an unsupported conclusion','''**Answer independently:** (a) Why does a row-disjoint test not establish patient independence here? (b) Why does zero training error not prove a clinically usable system? (c) What additional identifiers and validation cohorts would be required?\n\nDo not improve the reported test score by repeatedly trying features. Any further search needs a newly protected evaluation. The source card records the original source and reuse conditions.''',None)])
add('wine','Food chemistry: do topological descriptors add information?',[
('1. Distinguish measurement, cultivar and quality','''The target identifies three cultivars, not consumer quality or safety. A change from grams to milligrams can alter raw Euclidean distances. Standardization is therefore an explicit modeling choice, fitted on training data only.\n\nOur comparison gives every model the **same supervised fitting rows**. A separate subset of training rows is reserved as a fixed reference cloud.''','''features=[c for c in df if c not in ("row_id","label")];x=df[features].to_numpy(float);y=df.label.to_numpy(int)
split=stratified_split(y);save_split(split,df.row_id)
scaler=TrainScaler.fit(x[split["train"]]);z=scaler.transform(x)
order=np.random.default_rng(SEED).permutation(split["train"])
anchors=order[:30];fit_rows=np.sort(order[30:])
assert not(set(anchors)&set(fit_rows))
assert not(set(anchors)&set(split["test"]))
write_json("preprocessing.json",{"feature_names":features,"mean":scaler.mean,"scale":scaler.scale,"anchor_rows":anchors,"supervised_rows":fit_rows,"neighbors":8})
print("Reference rows:",len(anchors),"supervised rows:",len(fit_rows))'''),
('2. Define a descriptor that can be applied to an unseen row','''For one query, choose its eight nearest training reference points. Form the nine-point Rips complex through dimension two. Summarize finite H0 merge lengths and H1 lifetimes. The reference set is frozen; test observations never become reference points.\n\nThe six numbers are engineered local summaries. They are not a magical recovery of the topology of one vector. Small complete complexes keep the computation inspectable.''','''descriptor_names=["h0_mean","h0_std","h0_max","h1_count","h1_max_lifetime","h1_total_lifetime"]
needed=np.r_[fit_rows,split["validation"],split["test"]]
top=np.full((len(df),6),np.nan)
top[needed]=local_topology(z[needed],z[anchors],k=8)
assert np.isfinite(top[needed]).all()
top_scaler=TrainScaler.fit(top[fit_rows]);ts=np.full_like(top,np.nan);ts[needed]=top_scaler.transform(top[needed])
pd.DataFrame(top[needed],columns=descriptor_names,index=needed).rename_axis("row_id").to_csv(OUT/"topological_features.csv")
write_json("topology_preprocessing.json",{"names":descriptor_names,"mean":top_scaler.mean,"scale":top_scaler.scale,"fit_rows":fit_rows})
print(pd.DataFrame(top[fit_rows],columns=descriptor_names).describe().round(3))'''),
('3. Compare raw, topological, and combined representations','''C=1, eight neighbors and thirty anchors are fixed teaching choices—not the outcome of a hidden test-set search. We show validation and test scores separately. A win here would be a result for this one protocol, not evidence that topology is generally superior.''','''representations={"raw":z,"topology":ts,"combined":np.column_stack((z,ts))}
results={};predictions={}
for name,a in representations.items():
    model=LogisticRegression(C=1,max_iter=3000,random_state=SEED).fit(a[fit_rows],y[fit_rows])
    results[name]={}
    for key in ("validation","test"):
        ix=split[key];pred=model.predict(a[ix]);results[name][key]=class_metrics(y[ix],pred)
        if key=="test": predictions[name]=pred
majority=int(np.bincount(y[fit_rows]).argmax());results["majority"]={k:class_metrics(y[ix],np.full(len(ix),majority)) for k,ix in split.items() if k!="train"}
write_json("results.json",results)
pd.DataFrame({"row_id":split["test"],"cultivar":y[split["test"]],**predictions}).to_csv(OUT/"test_predictions.csv",index=False)
display(pd.DataFrame({name:r["test"] for name,r in results.items()}))
plt.figure(figsize=(7,4));plt.bar(list(results),[r["test"]["accuracy"] for r in results.values()]);plt.ylim(0,1)
plt.ylabel("Test accuracy");plt.title("Same fitting rows; fixed representations")
plot_done("comparison")'''),
('4. Check a property, not just a score','''Multiplying all standardized coordinates by two should multiply Rips birth/death distances by two. Counts need not be reinterpreted as physical units. The assertion below tests the descriptor contract independently of cultivar prediction. Then explain why arbitrary feature-wise scaling is a different operation.''','''q=z[split["validation"][:2]];a=z[anchors]
one=local_topology(q,a,k=8);two=local_topology(2*q,2*a,k=8)
np.testing.assert_allclose(two[:,[0,1,2,4,5]],2*one[:,[0,1,2,4,5]],atol=1e-10)
np.testing.assert_allclose(two[:,3],one[:,3]);print("Uniform-scale contract passed")''')])
add('stackloss','Manufacturing: what twenty-one process records cannot prove',[
('1. Read the encoded variables','''There are only twenty-one plant records. Exact dates and instrument metadata are absent. We preserve source row order, but do not call it a verified future-production timeline. Stack loss uses the documented encoded response scale; other ambiguous units are not invented. We hold out rows to demonstrate the procedure, not certify a plant-control system.''','''features=["AIRFLOW","WATERTEMP","ACIDCONC"];x=df[features].to_numpy(float);y=df.STACKLOSS.to_numpy(float)
split={"train":np.arange(14),"validation":np.arange(14,17),"test":np.arange(17,21)};save_split(split,df.row_id)
scale=TrainScaler.fit(x[split["train"]]);z=scale.transform(x)
model=Ridge(alpha=1).fit(z[split["train"]],y[split["train"]]);mean=y[split["train"]].mean()
results={}
for k in ("validation","test"):
    ix=split[k];pred=model.predict(z[ix]);results[k]={"ridge":regression_metrics(y[ix],pred),"mean":regression_metrics(y[ix],np.full(len(ix),mean)),"n":len(ix)}
    pd.DataFrame({"row_id":ix,"observed":y[ix],"ridge":pred,"training_mean":mean}).to_csv(OUT/(k+"_predictions.csv"),index=False)
write_json("results.json",results);display(pd.DataFrame({k:v["ridge"] for k,v in results.items()}))'''),
('2. Investigate how fragile the fitted coefficients are','''Leave out one **training** row, refit both scaling and model on the remaining training rows, then predict that omitted row. This is a sensitivity exercise, not an additional independent test set. A large change caused by a single row matters when the whole training set has fourteen observations.''','''loo=[]
for i in split["train"]:
    keep=split["train"][split["train"]!=i]
    sc=TrainScaler.fit(x[keep]);m=Ridge(alpha=1).fit(sc.transform(x[keep]),y[keep])
    loo.append({"row_id":int(i),"observed":float(y[i]),"omitted_prediction":float(m.predict(sc.transform(x[[i]]))[0])})
loo=pd.DataFrame(loo);loo.to_csv(OUT/"training_leave_one_out.csv",index=False)
plt.figure(figsize=(7,4));plt.plot(loo.row_id,loo.observed,"o-",label="Observed");plt.plot(loo.row_id,loo.omitted_prediction,"s--",label="Prediction without that row")
plt.xlabel("Preserved source row index (not verified date)");plt.ylabel("Encoded stack loss");plt.legend();plot_done("training_sensitivity")'''),
('3. Compare geometry with process meaning','''Build a small training point-cloud diagram. The distances join observations with similar standardized process values. The diagram does not enforce a mass-balance law. A scalar residual model is not a reconstructed reactor, and correlation cannot determine whether changing a control knob causes the predicted change.''','''_ = topology_report(z[split["train"]],"process_training_geometry")
print("Independent H0 merge lengths:",mst_lengths(z[split["train"]]))
write_json("preprocessing.json",{"features":features,"mean":scale.mean,"scale":scale.scale,"physical_guarantee":False})'''),
('4. Define a responsible next experiment','''Specify the missing timestamps, calibration units, actuator limits, safe excitation protocol, and independently recorded future runs before proposing a physics-informed model. Do not pretend that the eight new datasets supply the boundary conditions for every PDE in the course.\n\nTransfer questions: why might a neural network fit these rows and still be useless? Which quantities would a defensible conservation-law experiment need to measure?''',None)])
add('grunfeld','Business panels: availability time is part of the feature',[
('1. Respect the panel structure','''A panel repeatedly observes the same entity. This table contains eleven firms, with annual records over twenty years. We create prior-year predictors within each firm. In particular, same-year year-end market value is not available at the beginning of that year.\n\nThis is an explicitly simplified availability assumption: the notebook does not contain publication-time or revision-vintage data.''','''panel=df.sort_values(["firm","year"]).copy()
for c in ("invest","value","capital"):
    panel["lag_"+c]=panel.groupby("firm")[c].shift(1)
panel=panel.dropna().reset_index(drop=True)
features=["lag_invest","lag_value","lag_capital"]
x=panel[features].to_numpy(float);y=panel.invest.to_numpy(float)
split={"train":np.flatnonzero(panel.year.to_numpy()<=1947),"validation":np.flatnonzero(panel.year.between(1948,1950)),"test":np.flatnonzero(panel.year>=1951)}
save_split(split,panel.row_id)
assert panel.iloc[split["train"]].year.max()<panel.iloc[split["test"]].year.min()
print(panel.groupby("year").size().head());print({k:len(v) for k,v in split.items()})'''),
('2. Compare with doing almost nothing','''The last observed investment value is a serious baseline. A pooled ridge model shares one relationship across firms; it does not imply that all firms have the same structural mechanism. Both MAE and RMSE retain the source monetary scale. We do not invent a million-dollar multiplier.''','''scale=TrainScaler.fit(x[split["train"]]);z=scale.transform(x)
model=Ridge(alpha=1).fit(z[split["train"]],y[split["train"]]);results={}
for key in ("validation","test"):
    ix=split[key];pred=model.predict(z[ix]);last=x[ix,0]
    results[key]={"ridge":regression_metrics(y[ix],pred),"last_investment":regression_metrics(y[ix],last),"n":len(ix)}
    out=panel.iloc[ix][["row_id","firm","year"]].copy();out["observed"]=y[ix];out["ridge"]=pred;out["last_investment"]=last;out.to_csv(OUT/(key+"_predictions.csv"),index=False)
write_json("results.json",results);display(pd.DataFrame({k:v["ridge"] for k,v in results.items()}))
write_json("preprocessing.json",{"features":features,"mean":scale.mean,"scale":scale.scale,"predictor_availability":"previous annual record assumed available; publication timestamps absent"})'''),
('3. Look at errors by firm instead of hiding them in an average','''A low pooled error can hide a poorly modeled firm. The following view is a descriptive breakdown of this exposed test set, not a basis for tuning firm-specific models against it. A new-firm claim would require a different, entity-disjoint evaluation.''','''out=pd.read_csv(OUT/"test_predictions.csv");out["absolute_error"]=abs(out.observed-out.ridge)
by=out.groupby("firm").absolute_error.mean().sort_values();by.to_csv(OUT/"test_error_by_firm.csv")
plt.figure(figsize=(8,5));plt.barh(by.index,by.values);plt.xlabel("MAE in source 1947-dollar scale");plt.title("Historical test-period error by firm");plot_done("firm_errors")
refs=np.random.default_rng(SEED).choice(split["train"],size=28,replace=False)
_ = topology_report(z[refs],"lagged_business_geometry")'''),
('4. Separate prediction from intervention','''No fitted coefficient here is a causal effect of increasing a firm's equipment. The data contain selection, omitted variables, repeated firms, and historical accounting conventions.\n\nExercise: design two different tests—future years of known firms and years from previously unseen firms. Explain why these answer different questions, and why revised financial data complicate a genuine real-time historical simulation.''',None)])
add('co2','Environment: missingness and past-only windows',[
('1. A blank observation is not zero','''The archive has 2,284 weekly date slots but only 2,225 measurements. Fifty-nine missing values remain missing. Dropping them and treating adjacent remaining rows as adjacent weeks would change the time axis. We create source-traceable windows and reject windows that cross a missing measurement or a time gap.''','''dates=pd.to_datetime(df.date);days=(dates-dates.iloc[0]).dt.days.to_numpy();values=df.co2.to_numpy(float)
assert np.isnan(values).sum()==59
batch=past_windows(values,days,length=12,horizon=1,expected_step=7)
raw=ordered_split(days);split=assign_windows(batch,raw)
save_split(split,batch.target)
write_json("window_audit.json",{"raw_slots":len(df),"observed":int(np.isfinite(values).sum()),"missing":int(np.isnan(values).sum()),"valid_windows":len(batch.y),"partition_windows":{k:len(v) for k,v in split.items()},"strict_boundary_policy":True})
print(json.loads((OUT/"window_audit.json").read_text()))'''),
('2. Define exactly what is being forecast','''Each example uses twelve observed past weeks to predict one week ahead. During test evaluation later test predictions may use earlier **observed** test-period readings. This is rolling one-step prediction, not a free-running forecast of the entire future.\n\nOur strict support split drops boundary windows instead of borrowing history across partitions; it is conservative and explicitly different from a less restrictive operational evaluation.''','''scale=TrainScaler.fit(batch.x[split["train"]]);z=scale.transform(batch.x)
model=Ridge(alpha=1).fit(z[split["train"]],batch.y[split["train"]]);results={}
for k in ("validation","test"):
    ix=split[k];pred=model.predict(z[ix]);last=batch.x[ix,-1]
    results[k]={"ridge":regression_metrics(batch.y[ix],pred),"last_value":regression_metrics(batch.y[ix],last),"n":len(ix)}
    pd.DataFrame({"start_row":batch.start[ix],"last_feature_row":batch.end[ix],"target_row":batch.target[ix],"target_date":df.date.to_numpy()[batch.target[ix]],"observed":batch.y[ix],"ridge":pred,"last_value":last}).to_csv(OUT/(k+"_predictions.csv"),index=False)
write_json("results.json",results);print(results)
write_json("preprocessing.json",{"mean":scale.mean,"scale":scale.scale,"features":"12 observed weekly lags in chronological order","units":"ppmv","forecast_mode":"rolling one-step observed-history"})'''),
('3. Inspect trend, gaps, and a delay-space cloud','''A delay vector turns a time interval into a point. A loop may reflect seasonal repetition. It is not proof that the scalar series uniquely reconstructs the atmosphere's physical state. The point-cloud sample below is training-only; no test labels decide which diagram to show.''','''plt.figure(figsize=(9,4));plt.plot(dates,values,linewidth=.7);plt.xlabel("Date");plt.ylabel("CO2 (ppmv)");plt.title("Historical weekly observations; gaps remain gaps");plot_done("observations")
ix=np.random.default_rng(SEED).choice(split["train"],size=28,replace=False)
# Subtract each window's first value to inspect short-term shape, not long-term level.
centered=batch.x[ix]-batch.x[ix][:,[0]]
_ = topology_report(centered,"training_delay_shape")'''),
('4. Diagnose an invalid shortcut','''Why is interpolation using readings on both sides of a future gap unavailable for an online forecast? Why should overlapping windows not be treated as independent patients? How would changing the forecast horizon alter the information set?\n\nFurther model development needs a new locked protocol; the displayed test results are already exposed. These are historical observations, not a statement of today's atmospheric concentration.''',None)])
add('nile','Water infrastructure: change points without causal overreach',[
('1. Define volume and chronology','''The measurements are annual river volumes, in units of 100 million cubic metres. A volume is not a flow rate in cubic metres per second. There are one hundred years, not one hundred independent river systems. First partition years, then construct windows inside each partition.''','''values=df.volume.to_numpy(float);years=df.year.to_numpy();raw=ordered_split(years)
batch=past_windows(values,years,length=5,expected_step=1);split=assign_windows(batch,raw);save_split(split,batch.target)
print({k:(int(years[v[0]]),int(years[v[-1]])) for k,v in raw.items()})
print("Forecast examples:",{k:len(v) for k,v in split.items()})'''),
('2. Find a descriptive change using training years only','''We fit two constant means and choose the split with smallest within-segment squared error. The selected split is retrospective within the training period. A low error does not explain the cause, prove a change is significant, or justify moving a dam. Many candidate splits were inspected; ordinary one-test reasoning would ignore that search.''','''train=raw["train"];k,sse=best_mean_change(values[train],min_segment=10)
change_year=int(years[train[k]])
write_json("change_point.json",{"first_year_second_segment":change_year,"train_rows":train,"within_segment_sse":sse,"minimum_segment":10,"causal_claim":False})
plt.figure(figsize=(9,4));plt.plot(years,values,".-");plt.axvline(change_year,linestyle="--",label="Training-selected split")
plt.xlabel("Year");plt.ylabel("Annual volume (10^8 cubic metres)");plt.legend();plot_done("change_point")
print("First year of fitted second regime:",change_year)'''),
('3. Keep a forward prediction question separate','''The change-point fit is not automatically a forecasting model. Here we independently compare last value, a fixed training mean, and a ridge model of five past annual readings. No causality or physical conservation law is enforced by any of them.''','''scale=TrainScaler.fit(batch.x[split["train"]]);z=scale.transform(batch.x)
model=Ridge(alpha=1).fit(z[split["train"]],batch.y[split["train"]]);mu=batch.y[split["train"]].mean();results={}
for key in ("validation","test"):
    ix=split[key];pred=model.predict(z[ix]);last=batch.x[ix,-1]
    results[key]={"ridge":regression_metrics(batch.y[ix],pred),"last_value":regression_metrics(batch.y[ix],last),"training_mean":regression_metrics(batch.y[ix],np.full(len(ix),mu)),"n":len(ix)}
    pd.DataFrame({"target_row":batch.target[ix],"year":years[batch.target[ix]],"observed":batch.y[ix],"ridge":pred,"last_value":last}).to_csv(OUT/(key+"_predictions.csv"),index=False)
write_json("results.json",results);print(results)
ix=np.random.default_rng(SEED).choice(split["train"],size=24,replace=False)
_ = topology_report(z[ix],"river_delay_geometry")'''),
('4. Identify what would be required for physics','''A hydrological conservation model needs more than this scalar annual series: specify inflows, outflows, storage, rainfall, spatial boundaries and uncertainty. The manufactured PDE examples in the core course have these assumptions by construction; this observational series does not magically inherit them.\n\nTransfer exercise: write one descriptive claim supported by the plot and one causal claim that it cannot support.''',None)])
add('elnino','Marine climate: seasonal means before neural operators',[
('1. Reshape without changing time','''The original rows contain years and twelve named month columns. We create a long table ordered January through December for each year. This adds no observations: 61 annual rows become 732 monthly values. The signal is regional mean SST in degrees Celsius, not an anomaly until we subtract a declared baseline.''','''month_names=["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
values=df[month_names].to_numpy(float).ravel();years=np.repeat(df.YEAR.to_numpy(),12);months=np.tile(np.arange(1,13),len(df));tick=np.arange(len(values))
long=pd.DataFrame({"month_index":tick,"year":years,"month":months,"sst_c":values});long.to_csv(OUT/"monthly_derived.csv",index=False)
raw={"train":np.flatnonzero(years<=1985),"validation":np.flatnonzero((years>=1986)&(years<=1997)),"test":np.flatnonzero(years>=1998)}
climate=seasonal_means(values[raw["train"]],months[raw["train"]]);anomaly=values-climate[months-1]
write_json("climatology.json",{"fit_period":"1950–1985","monthly_means_c":climate,"anomaly_definition":"observed SST minus that calendar month's training-period average"})
print("Monthly measurements:",len(values));print("Training monthly means:",climate.round(2))'''),
('2. Compare a seasonal forecast, persistence, and learned lags','''The seasonal baseline predicts the training average for the target month. Persistence predicts the last observed temperature. Ridge predicts from twelve observed lags. Each makes a different assumption. All test windows remain inside the test period and predict one month ahead using observed history.''','''batch=past_windows(values,tick,length=12,expected_step=1);split=assign_windows(batch,raw);save_split(split,batch.target)
scale=TrainScaler.fit(batch.x[split["train"]]);z=scale.transform(batch.x)
model=Ridge(alpha=1).fit(z[split["train"]],batch.y[split["train"]]);results={}
for key in ("validation","test"):
    ix=split[key];pred=model.predict(z[ix]);last=batch.x[ix,-1];season=climate[months[batch.target[ix]]-1]
    results[key]={"ridge":regression_metrics(batch.y[ix],pred),"last_value":regression_metrics(batch.y[ix],last),"monthly_mean":regression_metrics(batch.y[ix],season),"n":len(ix)}
    pd.DataFrame({"target_month_index":batch.target[ix],"year":years[batch.target[ix]],"month":months[batch.target[ix]],"observed_c":batch.y[ix],"ridge_c":pred,"last_c":last,"climatology_c":season}).to_csv(OUT/(key+"_predictions.csv"),index=False)
write_json("results.json",results);print(results)'''),
('3. Visualize anomalies and training delay topology','''Subtracting a seasonal mean is not harmless by default: the reference period is part of the definition. A baseline fit on all years would use future distribution information. We keep the training baseline fixed. A short delay cloud is an exploratory summary, not a recovered global climate manifold or a climate neural operator.''','''plt.figure(figsize=(9,4));plt.plot(years+(months-1)/12,anomaly,linewidth=.8);plt.axhline(0,linestyle="--")
plt.xlabel("Year");plt.ylabel("SST anomaly against 1950–1985 mean (degrees C)");plot_done("anomalies")
ab=past_windows(anomaly,tick,3,expected_step=1);ass=assign_windows(ab,raw)
ix=np.random.default_rng(SEED).choice(ass["train"],size=28,replace=False)
_ = topology_report(ab.x[ix],"marine_anomaly_delays")'''),
('4. Distinguish one series from an operator dataset','''An operator-learning study needs multiple input functions or conditions and corresponding solution fields, with function-level splits. This single regional series is not equivalent to many independent PDE trajectories. The core manufactured heat-operator examples and optional simulated field datasets serve a different role.\n\nIndependent task: explain how changing the climatology fit period can change the apparent anomalies without changing any original observations.''',None)])
add('modechoice','Transportation: four rows can be one learning example',[
('1. Reconstruct the choice set','''Each traveler has four alternatives. Randomly splitting the 840 rows could put the same traveler into training and test. Instead, pivot to 210 person-level examples. Include offered waiting times, prices, in-vehicle times and income. Exclude the target and party size whose availability is tied to the chosen mode. We also exclude generalized cost because it is constructed from other cost/time terms.''','''x,y,ids,features=choice_table(df)
split=stratified_split(y);save_split(split,ids)
print("Alternative rows:",len(df),"person examples:",len(ids),"features:",len(features))
assert len(set(ids))==len(ids)
assert not(set(ids[split["train"]])&set(ids[split["test"]]))
scale=TrainScaler.fit(x[split["train"]]);z=scale.transform(x)
write_json("preprocessing.json",{"features":features,"mean":scale.mean,"scale":scale.scale,"split_unit":"traveler","excluded":["choice","gc","psize"],"mode_map":{"1":"air","2":"train","3":"bus","4":"car"}})'''),
('2. Establish person-level baselines','''This simple multinomial classifier treats each traveler's thirteen offered attributes as predictors. It is not the same model as a conditional-logit utility model. We compare it with the training-majority mode and the cheapest offered mode. All return exactly one choice per traveler.''','''model=LogisticRegression(C=1,max_iter=3000,random_state=SEED).fit(z[split["train"]],y[split["train"]])
majority=int(np.bincount(y[split["train"]]).argmax());results={}
for key in ("validation","test"):
    ix=split[key];proba=model.predict_proba(z[ix]);pred=model.predict(z[ix]);cheapest=np.argmin(x[ix][:,[1,4,7,10]],axis=1)+1
    np.testing.assert_allclose(proba.sum(axis=1),1)
    results[key]={"logistic":class_metrics(y[ix],pred),"majority":class_metrics(y[ix],np.full(len(ix),majority)),"cheapest":class_metrics(y[ix],cheapest),"log_loss":float(log_loss(y[ix],proba,labels=model.classes_)),"n_travelers":len(ix)}
    out=pd.DataFrame({"individual":ids[ix],"selected":y[ix],"predicted":pred,"cheapest":cheapest})
    for j,mode in enumerate(model.classes_):out["prob_mode_"+str(mode)]=proba[:,j]
    out.to_csv(OUT/(key+"_predictions.csv"),index=False)
write_json("results.json",results);print(results)'''),
('3. Inspect sample geometry without inventing market shares','''The study deliberately oversamples some modes. Prediction fractions are not population transport shares, and learned probabilities are not automatically population-calibrated. A topology diagram summarizes offered attributes in the chosen standardized metric; it does not recover the real road network.''','''sample=np.random.default_rng(SEED).choice(split["train"],size=28,replace=False)
_ = topology_report(z[sample],"traveler_attribute_geometry")
plt.figure(figsize=(7,4));labels,count=np.unique(y,return_counts=True);plt.bar(labels,count)
plt.xticks([1,2,3,4],["air","train","bus","car"]);plt.ylabel("Travelers in choice-based sample");plt.title("Counts are not population market shares");plot_done("sample_counts")'''),
('4. Transfer the grouping lesson','''In sports, several shots can belong to one athlete; in healthcare, several images can belong to one patient; in manufacturing, many overlapping windows can come from one run. Choose the independent unit before creating a split.\n\nExplain why a predicted change under a modified ticket price is not a validated causal effect. What sampling weights, policy experiment, or external evidence would be needed?''',None)])

# Notebooks are deliberately readable from a fresh kernel, not dependent on previous runs.
for name,(title,sections) in CASES.items():
    meta=json.loads((ROOT/f'data/industries/{name}/metadata.json').read_text())
    cells=[nbf.v4.new_markdown_cell(f'# {title}\n\n**Beginner route:** read the [case lesson](../lessons/{name}.md) and [dataset card](../cards/{name}.md). Predict each result before executing.\n\nSource: [{meta["citation"]}]({meta["source_url"]}). Snapshot obtained by offline export from {meta["provider"]} {meta["provider_version"]}. Numerical results below are our computations, not source claims.\n\nThis fixed test partition is a teaching demonstration, not an untouched future benchmark.'),nbf.v4.new_code_cell(SETUP.replace('CASE_ID',name))]
    for heading,body,code in sections:
        cells.append(nbf.v4.new_markdown_cell('## '+heading+'\n\n'+body))
        if code:cells.append(nbf.v4.new_code_cell(textwrap.dedent(code)))
    cells.append(nbf.v4.new_markdown_cell('## Save your evidence\n\nCreate `my_work/industries/'+name+'.md` with your prediction, actual result, explanation, one failed assumption and one claim the evidence does not justify. Use the separate learner notebook only after you understand the worked code. No notebook execution automatically marks your learning complete.'))
    nb=nbf.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'learning_role':'worked_reference','dataset_id':name})
    nbf.write(nb,ROOT/f'industry/notebooks/{name}.ipynb')
print('Created',len(CASES),'worked notebooks')
