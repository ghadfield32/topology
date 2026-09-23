"""Create the original v7 teaching notebooks. Execution is a separate operation."""
from pathlib import Path
import json, inspect, textwrap
import nbformat as nb
from shape_lab import practice_v7 as P
R=Path(__file__).resolve().parents[1]
SETUP='''from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic('matplotlib','inline')
from pathlib import Path
import sys, json
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'src/shape_lab').is_dir())
if str(ROOT / 'src') not in sys.path: sys.path.insert(0, str(ROOT / 'src'))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shape_lab.evidence_v7 import load_snapshot, conformal_rank, conformal_radius, coverage, overlap_report
from shape_lab.display import show_and_save, save_json
'''
def notebook(path,cells):
    path.parent.mkdir(parents=True,exist_ok=True)
    doc=nb.v4.new_notebook(cells=[nb.v4.new_markdown_cell(t) if k=='m' else nb.v4.new_code_cell(t) for k,t in cells])
    doc.metadata.kernelspec={'display_name':'Python 3','language':'python','name':'python3'}
    doc.metadata.language_info={'name':'python','version':'3.13'}
    nb.write(doc,path)

def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text.strip()+'\n')

lessons={
'seeds':r'''# Agriculture case — What does “shape” mean in a table?

## Start without subject knowledge

A wheat kernel is an individual object. A measurement turns one property of that object into a number. A row collects measurements for one kernel; a column repeats a particular measurement across kernels. A class label names a category, not an amount. Subtracting class 1 from class 3 does not define a meaningful physical difference.

The included UCI Seeds snapshot has 210 rows, seven geometric measurements and three integer class labels, with 70 rows per label. UCI describes X-ray-derived measurements of Kama, Rosa and Canadian kernels. We retain the source integers rather than guess the integer-to-name mapping. The original radiographs are not included. These are observed extracted features, not simulated points and not a segmentation benchmark. [Provider and DOI](https://archive.ics.uci.edu/dataset/236/seeds).

**Learning objective:** distinguish a measurement, a constructed geometric feature, a metric-dependent descriptor, and a topological invariant. Then perform a small classification experiment without confusing its score with agricultural validation.

## A formula you can derive

For area A and perimeter P, define compactness C = 4πA/P². A circle of radius r has A = πr² and P = 2πr. Substitution gives C = 1. Under uniform scaling by s, area becomes s²A and perimeter becomes sP, so C does not change. Under a general stretch, it usually changes. Thus scale invariance is not invariance under every homeomorphism.

For example a rectangle with side lengths 2 and 1 has C = 4π(2)/6² = 2π/9, about 0.698. Stretch one side to 4; the new C is 4π(4)/10² = 4π/25, about 0.503. Both filled rectangles are homeomorphic to a disk. Their different compactness values did not discover different topology. This is an original worked calculation, not a new empirical finding.

The source already includes a compactness column. Recomputing it from the rounded area and perimeter is a consistency check, not permission to replace the provider's values. Small differences can result from rounding. The notebook reports the discrepancy. The inspected repository metadata does not specify physical length/area units, so we do not rename these columns millimetres or square millimetres. The dimensionless relation assumes internally consistent units.

## Why preprocessing changes the question

Euclidean distance adds squared coordinate differences. A column with a much larger numerical scale can dominate it. Our baseline standardizes each feature using the training mean and population standard deviation. That defines a particular geometry; it does not discover the uniquely correct geometry of wheat. A constant training column gets scale one, which avoids division by zero without creating variation.

Fit preprocessing on training observations only. Applying those fixed parameters to a held-out row is different from recalculating them using the held-out collection. The latter lets the test distribution influence the analysis before evaluation.

## The explicit experiment

We declare a stratified 126/42/42 training/validation/test split with fixed seed 17. Stratification preserves the class proportions in this demonstration. It does not supply missing farm or batch identities. Two logistic-regression pipelines use identical rows and fixed C=1: all seven features, and six features without compactness. A training-majority predictor is also shown. No hyperparameter is selected using validation or test results. Validation is reported as a diagnostic; the test partition is exposed after the prescribed experiment and must not become an unlimited tuning set.

The experiment asks whether these recorded features can distinguish the integer classes in this collection. It cannot establish future-farm performance, disease detection, crop yield, or field prevalence. The source table lacks acquisition dates and field/batch identifiers needed for those evaluation designs.

## Return after learning persistence

A small, declared subset of 24 training rows is standardized with the same training scaler and used to build a Vietoris–Rips filtration through triangles. Pairwise distances determine when edges enter; three mutually connected vertices supply a triangle. The notebook calculates H0 and H1 persistence. These are properties of this sampled, standardized seven-dimensional feature cloud, not holes in a physical grain. The subset uses fixed row identities; no class outcome is used to select an attractive diagram. Its row IDs and intervals are saved.

This persistence calculation is descriptive. It is not added secretly to the classifier and is not credited with any classification improvement. The earlier Wine case teaches a fixed-reference predictive descriptor when you are ready to study that separate formulation.

## Read the result correctly

Accuracy is correct predictions divided by test rows. A confusion matrix preserves which classes were confused. Report the denominator, not only a percentage. Balanced classes in this designed collection do not show natural prevalence. Two different models can tie on accuracy but misclassify different rows. Inspect the saved predictions before making a claim about improvement.

## Your independent work

Implement four small functions in `learner.ipynb`. Then explain the rectangle example without looking. Change only the chosen persistence subset after clearly labeling that new experiment exploratory; predict whether its diagram must remain identical. It need not: sample selection changes the complex. Do not mistake a sensitivity result for evidence that the original source table is wrong.

To pass, identify the observation unit; calculate compactness; justify the split and scaler; explain the meaning and limitations of the diagram; and describe a missing data field needed for an actual farm deployment study.

[Data card](../../data/v7/seeds/metadata.json) · [Worked lab](lab.ipynb) · [Your coding exercises](learner.ipynb) · [Reference answers](answers.ipynb) · [Questions and answers](questions.md)
''',
'concrete_slump':r'''# Materials case — A prediction needs an error range and a meaning

## Begin with the observation

A mixture is specified by quantities of ingredients. A laboratory test measures its responses. This source records 103 concrete-mixture tests with seven ingredient quantities and three outputs. Ingredients are given in kilograms in one cubic metre of concrete; slump and flow are centimetres; compressive strength is MPa at 28 days. This is the **Concrete Slump Test** dataset, not the separate 1,030-row concrete-strength dataset. [Provider and DOI](https://archive.ics.uci.edu/dataset/182/concrete+slump+test).

Our task is to predict the 28-day strength from the seven ingredients. The source row ID is an identifier, not an ingredient. Slump and flow are measured responses; they are excluded from the chosen pre-measurement prediction task. Including a column because it improves a score is not a substitute for establishing that it would be available at decision time.

## What a baseline means

A constant training-mean predictor ignores ingredients. It answers: how well can we do using only the typical training response? A ridge regression predicts an intercept plus a weighted sum of standardized ingredient quantities. Its penalty discourages very large fitted coefficients. Our fixed regularization value is 10, chosen for this teaching protocol before results are shown, not reported as optimal.

Suppose measured strengths are 20, 30 and 40, while a model predicts 22, 25 and 43. Absolute errors are 2, 5 and 3 MPa; their mean is 10/3 MPa. Squared-error metrics punish the error of five more strongly, but they answer a different question. We report MAE and RMSE with the target unit. Neither metric is a certification that a structure can safely use the material.

## Why training, calibration and testing are different

The lab uses a fixed random ordering: 52 training rows fit the scaler and model, 25 calibration rows set the error radius, and 26 test rows assess the fixed procedure. The model is not refitted after calibration. We do not reuse calibration rows for tuning the model or choosing the score. Test outcomes are used only for the final reported diagnostics.

The source describes 78 initial and 25 later observations, but the table does not supply authenticated dates or batch IDs. We therefore label the random mixture-level split as an educational protocol, not a proven temporal, new-batch or exchangeable deployment design. Randomly shuffling a dataset does not create independence that the collection process lacked.

## Derive the calibration radius by ranks

For the fitted predictor f, each calibration error is s_i = |y_i - f(x_i)|. At nominal error rate α, use the one-based rank

k = ceil((n_cal + 1)(1 - α)).

Sort calibration errors and take the k-th value. If k exceeds n_cal, use an infinite radius rather than inventing an unsupported finite extreme quantile. For n_cal=25 and α=0.1, k=24. Python's zero-based index is therefore 23. We select an order statistic directly; interpolating between values is not the same rule.

For a hand example with nine sorted errors 1,2,…,9 and α=0.2, k=ceil(10×0.8)=8. A prediction of 30 receives [22,38]. At α=0.1 the radius is nine. Requesting 99% nominal coverage with only nine calibration points needs rank ten and yields an uninformative infinite interval under this conservative construction. This illustrates a sample-size limitation, not a software failure.

Under exchangeability of calibration and future scores for a predictor fixed independently of them, the rank argument gives finite-sample **marginal** coverage. It does not say every recipe, subgroup or realized test set has exactly the nominal coverage. Distribution shift and dependent batches require additional reasoning. [Primary tutorial, including proof and limitations](https://arxiv.org/abs/2107.07511). This package adds the worked arithmetic and a real-data implementation; it does not reproduce that tutorial's experiments.

## Test usefulness as well as coverage

A radius of a million MPa would cover these observed outcomes but be useless. Report interval width alongside empirical coverage. Inspect errors for individual held-out mixtures, but label any subgroup discovered after looking at them as exploratory. Our symmetric intervals may have negative lower bounds; those are retained and discussed rather than silently clipped. Known physical constraints can justify a different set construction, but that choice must be stated before interpreting its coverage.

The notebook draws intervals centered on the fixed test predictions. The x-axis orders points by predicted strength, not time. Sorting for a plot is not a chronological analysis. It saves row IDs, predictions, bounds, coverage flags, calibration scores, rank and radius so you can verify the whole calculation.

## What you may conclude

You may report this model's errors and this interval procedure's empirical coverage on these declared rows. You may not infer engineering fitness, plant-wide safety, causal ingredient effects, or future-batch coverage from this example. A learned coefficient is not a controlled experimental intervention.

To pass, calculate an order statistic by hand, distinguish calibration from model fitting, trace one interval to its source row, explain marginal versus conditional coverage, and identify the batch information that an independent industrial study would need.

[Data card](../../data/v7/concrete_slump/metadata.json) · [Worked lab](lab.ipynb) · [Your coding exercises](learner.ipynb) · [Reference answers](answers.ipynb) · [Questions and answers](questions.md)
''',
'leakage':r'''# Methods lab — Two different rows can contain the same evidence

## What is the object of evaluation?

An array has rows, but the scientific unit might be a person, a physical object, a manufacturing batch, a camera session, or a time interval. A splitter that keeps row numbers apart has not necessarily kept independent units apart. This lab makes that distinction visible without inventing a new observed dataset.

We begin with the 210 observed Seeds feature vectors. Then we deliberately make three exact software copies of each row. There are now 630 array rows but still only 210 source kernels. These copies are a **manufactured leakage stress test**. They are not additional measurements, repeatability trials, new kernels, or a larger agricultural study.

The repeated source ID is the unit key. Generated copy IDs distinguish software rows. Saving both makes it possible to ask two questions independently: are array indices shared, and are source kernels shared?

## Why a nearest-neighbor method exposes the problem

A one-nearest-neighbor classifier assigns the label of the closest training feature vector. If an exact copy of a test row exists in training, its distance is zero. It can look excellent without transferring to a new kernel. We compare a random row split with a split that assigns all copies of each original kernel together.

Both experiments fit standardization only on their own training data. This controls one kind of leakage while intentionally varying the other. All feature columns, labels, copies and fixed random seeds are recorded. The difference is descriptive: this small constructed stress test does not estimate the numerical inflation in every real dataset.

## A hand example

Suppose rows 0 and 1 describe kernel A and rows 2 and 3 describe kernel B. Training on rows [0,2] and testing on [1,3] shares no row indices. It shares both kernels. The row audit passes, but the unit audit fails. A valid new-kernel split might train on [0,1] and test on [2,3], although two kernels would be far too few for a useful real evaluation.

The audit returns both results instead of guessing which one matters. You must provide an appropriate unit key. Unique random IDs assigned to every copied row would conceal the problem; identifiers are part of the scientific design, not merely software formatting.

## Distance depends on units

The lab also multiplies one numerical feature by 1,000. That simulates a change of numerical representation; because the source units are not independently specified, we do not label it a real mm-to-m conversion. Raw Euclidean distances generally change. A training-standardized representation should agree after a positive column-wise rescaling if its scaler is consistently refitted on the same training rows. We test this arithmetic identity separately from any claim that standardization is scientifically appropriate.

Do not transfer the identity to arbitrary nonlinear transforms, feature removal, imputation, or changing reference samples. Nor does equal standardized data imply that a model is fair across missing demographic groups.

## Connect back to images, time and physics

A medical scan produces many image patches; a random patch split may share the patient. A video produces adjacent windows; the windows may share frames and events. A numerical PDE solution produces many spatial samples; testing on different points from the same solution is not necessarily testing a new initial condition. These are proposed analogies. This lab uses Seeds copies only; it does not claim to have evaluated patients, basketball clips, or PDE generalization.

The retained course includes complete-choice-set and time-support checks. Return to those after this exact example. Group splitting and chronological splitting address different threats; neither word is a universal guarantee against leakage.

## Repair the experiment, not the narrative

When an audit fails, first define the intended future query. Is it a new kernel, new plant, new site, or another reading of a familiar device? Then choose the split, transformations and metric to match it. Do not merely delete inconvenient test rows until the score improves. Save the reason and the exclusions, and retain a final evaluation set appropriate to the revised question.

Your assessment is to demonstrate the four-row example, write the two overlap checks, interpret the manufactured-copy result, and propose the missing group key for a domain you care about. A passing test proves this audit implementation detected these overlaps, not that an unseen collection is independent.

[Worked lab](lab.ipynb) · [Learner coding](learner.ipynb) · [Reference answers](answers.ipynb) · [Questions](questions.md)
''',
'claims':r'''# Methods lab — Read a scientific claim, then test exactly what it says

## Four kinds of statement

A source can motivate an idea without proving it. Keep four labels separate: **source claim**, **mathematical statement with assumptions**, **original worked calculation**, and **measured experiment**. This lesson uses the supplied posts about symplectic structure, projection and PINN gradient conflicts as prompts. The source audit records their scope. We do not rewrite the posts as if their authors had supplied our qualifications.

The symplectic post asserts exact energy conservation across arbitrary rollout steps and describes one algebraic correction as restricting updates to a physical constraint manifold. The gradient-conflict post reports Norm-PCGrad advantages on its selected benchmarks. The HNN/LNN post links formulations through the Legendre transform. The manifold post describes local charts and smooth transitions. These are the supplied sources' positions; the calculations below are original educational checks, not reproductions of their empirical studies.

## Continuous dynamics and discrete updates are not the same object

For canonical coordinates z=(q,p), let J=[[0,1],[-1,0]] and dynamics z_dot=J grad H. For differentiable, time-independent H and an exact solution, the chain rule gives dH/dt = grad(H)^T J grad(H)=0 because J is skew-symmetric. Explicit time dependence or external dissipative forces change the claim. A floating-point integrator is a discrete map approximating a trajectory; it needs its own analysis.

Take H=(q²+p²)/2, nondimensional unit-oscillator variables. Kick then drift:

p_new = p - h q; q_new = q + h p_new.

At (q,p)=(1,0), h=0.2 gives p_new=-0.2 and q_new=0.96. Energy changes from 0.5 to (0.96²+0.2²)/2=0.4808. The map A=[[1-h²,h],[-h,1]] nevertheless satisfies A^T J A=J. Thus being symplectic does not imply exact conservation of this H at every step. The lab checks both identities separately and plots a longer trajectory, without calling nondimensional values joules or seconds.

## A single linearized correction can leave a residual

For C(x)=x^T x-1, the desired set is the unit sphere. Its Jacobian is 2x^T. The minimum-norm linearized correction is x_new=x-((x^T x-1)/(2x^T x))x when x is nonzero. At x=(2,0), it gives (1.25,0). The new constraint residual is 1.25²-1=0.5625, not zero. It has solved the first-order approximation, not the original nonlinear equation exactly.

Iteration can reduce the residual; radial normalization x/||x|| is exact for this particular sphere away from zero. Neither fact makes one formula an exact universal projection for every constraint. At zero the Jacobian is rank deficient. The reference function raises a clear error instead of inventing a direction. At arbitrary constraints, rank, convergence region, metric and desired conservation properties must be examined independently.

## Conflicting objectives do not always admit simultaneous improvement

For two losses with gradients g1=(1,0) and g2=(-1,0), their inner product is -1. A small update -ηd decreases both to first order only if g1·d>0 and g2·d>0. These conditions contradict each other. No gradient-surgery algorithm can produce a direction satisfying both strict inequalities in this example. An optimizer may choose a compromise or stall; it does not remove mathematical incompatibility.

The supplied Norm-PCGrad preprint's reported improvements are benchmark-specific. Our small example is not a performance comparison between PCGrad, Norm-PCGrad and ConFIG. The existing Stage 27 covers their operations and interface-condition issues. [Primary preprint](https://arxiv.org/abs/2609.14841).

## Turn the lesson into a claim ledger

For each future paper, save its exact source/version, the proposed guarantee, assumptions, the implemented object, the test, and its scope. Distinguish a model's learned vector field from the numerical solver and the hardware implementation. Timing one matrix multiplication does not establish end-to-end latency; matching a drawing does not establish camera calibration. Those topics are developed in the retained geometry stages.

The lab also loads observed Seeds measurements to compare two homeomorphic rectangle controls and the source's compactness feature. This is a real-data bridge, not evidence that wheat obeys Hamiltonian dynamics. Use observed data when the scientific question fits; use an exact manufactured counterexample when falsifying a universal mathematical claim.

To pass, derive each counterexample on paper, run it, explain the variable and unit conventions, and rewrite your own conclusion so it says no more than the calculation supports. A numerical test supports a calculation; it is not a substitute for a general proof.

[Claim audit](../../docs/v7/SOURCE_AUDIT.md) · [Worked lab](lab.ipynb) · [Learner coding](learner.ipynb) · [Reference answers](answers.ipynb) · [Questions](questions.md)
'''}

case_defs={
'seeds':('Agriculture: shape features and topology','applications_v7',[
 ('table_dimensions',"Return the two dimensions of a 2D array; explain what each dimension counts.","assert table_dimensions(np.ones((210, 7))) == (210, 7)","Use the array's shape after checking that it has two axes."),
 ('compactness',"Calculate 4πA/P² for matching positive area and perimeter arrays.","assert np.allclose(compactness([np.pi], [2*np.pi]), [1.])","Square the perimeter, not the area. The circle is an exact control."),
 ('fit_scaler',"Return training column means and population standard deviations; replace a zero scale with one.","c,s=fit_scaler([[0.,9.],[2.,9.]])\nassert np.allclose(c,[1.,9.]) and np.allclose(s,[1.,1.])","axis=0 aggregates observations, preserving a parameter per feature."),
 ('class_counts',"Return the observed integer-label frequencies as a dictionary.","assert class_counts([3,1,3,2]) == {1:1,2:1,3:2}","np.unique can return both values and counts. Do not infer class names.")]),
'concrete_slump':('Materials: prediction intervals','applications_v7',[
 ('absolute_errors',"Compute each absolute prediction error while preserving target units.","assert np.allclose(absolute_errors([20,30,40],[22,25,43]),[2,5,3])","Subtract matching vectors, then take absolute values."),
 ('interval_bounds',"Return lower and upper prediction bounds for a fixed nonnegative radius.","lo,hi=interval_bounds([30.],8.)\nassert np.allclose(lo,[22.]) and np.allclose(hi,[38.])","One radius is used on both sides. Do not refit it on these outcomes."),
 ('empirical_coverage',"Compute the fraction inside closed lower/upper bounds.","assert empirical_coverage([0,1,2],[-1,0,0],[0,1,1]) == 2/3","Both inequalities must hold; the boundary counts as covered."),
 ('mean_baseline',"Predict the training mean for n future cases.","assert np.allclose(mean_baseline([2.,6.],3),[4,4,4])","The test outcomes are not an argument to this function.")]),
'leakage':('Methods: leakage and units','methods_v7',[
 ('shared_rows',"Return sorted row-index overlap.","assert shared_rows([0,2],[1,3]) == []","Set intersection answers row overlap only."),
 ('shared_units',"Return sorted shared unit IDs for two groups of rows.","assert shared_units([0,2],[1,3],['A','A','B','B']) == ['A','B']","Resolve rows to source units before intersecting."),
 ('partition_by_units',"Return row indices in selected units and in all remaining units.","a,b=partition_by_units(['a','b','a','c'],['a'])\nassert a.tolist()==[0,2] and b.tolist()==[1,3]","Build a membership mask; keep all copies together."),
 ('apply_scaler',"Apply previously fitted feature centers and positive scales.","assert np.allclose(apply_scaler([[6,2]],[2,2],[2,1]),[[2,0]])","Broadcast feature-wise arrays; do not fit anything inside this function.")]),
'claims':('Methods: source claims and counterexamples','methods_v7',[
 ('oscillator_energy',"Return (q²+p²)/2 for a finite two-component vector.","assert np.isclose(oscillator_energy([.96,-.2]),.4808)","A dot product computes the sum of squares."),
 ('symplectic_defect',"Compute the Frobenius norm of A.T J A-J for a 2x2 map.","assert symplectic_defect([[.96,.2],[-.2,1.]]) < 1e-14","J is the canonical skew-symmetric matrix, not the identity."),
 ('sphere_newton_step',"Apply one linearized correction for x.x=1, rejecting x=0.","x=sphere_newton_step([2.,0.])\nassert np.allclose(x,[1.25,0.])","This is not radial normalization; preserve the intended formula."),
 ('gradient_inner_product',"Compute the dot product of matching objective gradients.","assert gradient_inner_product([1,0],[-1,0]) == -1","A negative value signals a local conflict, not its universal cure.")])}

LABS={}
LABS['seeds']=[('m',lessons['seeds'].split('## A formula')[0]),('c',SETUP+"\nOUT=ROOT/'reports/v7/seeds';OUT.mkdir(parents=True,exist_ok=True)\ntable,meta=load_snapshot('seeds')\nprint(meta['observation']);print(table.shape)\ndisplay(table.head())\n"),
('m','## First check: labels and a geometric identity\nPrint all class counts. The compactness discrepancy is reported rather than repaired. Its formula describes geometry, not a topological invariant.'),
('c',"from shape_lab.practice_v7 import compactness, class_counts\nprint(class_counts(table.variety))\nrecomputed=compactness(table.area,table.perimeter)\ncompactness_gap=np.abs(recomputed-table.compactness.to_numpy())\nprint('Largest absolute recomputation gap:',compactness_gap.max())\nassert class_counts(table.variety)=={1:70,2:70,3:70}\n"),
('m','## Declare rows before fitting\n126 training, 42 validation, 42 test. Stratify class labels for this within-collection demonstration; no field or batch validation is asserted.'),
('c',"from sklearn.model_selection import train_test_split\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.dummy import DummyClassifier\nfrom sklearn.metrics import accuracy_score,confusion_matrix\nX=table[meta['features']].to_numpy();y=table.variety.to_numpy();rows=np.arange(len(table))\ntrain,rest=train_test_split(rows,test_size=.4,stratify=y,random_state=17)\nvalid,test=train_test_split(rest,test_size=.5,stratify=y[rest],random_state=17)\nparts={'train':train,'validation':valid,'test':test}\naudit=overlap_report(parts,table.source_id.to_numpy())\nprint({k:len(v) for k,v in parts.items()});assert audit['row_disjoint']\nsplit=pd.DataFrame({'source_id':table.source_id,'split':''})\nfor name,ix in parts.items():split.loc[ix,'split']=name\nsplit.to_csv(OUT/'split.csv',index=False)\n"),
('m','## Fixed baselines; no tuning on test outcomes\nThe two learned models differ only by whether compactness is supplied. The class labels and source IDs are not predictors. The validation scores do not select the model in this protocol.'),
('c',"models={'majority':(DummyClassifier(strategy='most_frequent'),list(range(7))),\n        'seven_features':(make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=3000)),list(range(7))),\n        'without_compactness':(make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=3000)),[0,1,3,4,5,6])}\nmetrics={};predictions=[]\nfor name,(model,cols) in models.items():\n    model.fit(X[train][:,cols],y[train]);metrics[name]={}\n    for part,ix in [('validation',valid),('test',test)]:\n        pred=model.predict(X[ix][:,cols]);metrics[name][part]={'n':len(ix),'correct':int((pred==y[ix]).sum()),'accuracy':float(accuracy_score(y[ix],pred)),'confusion_matrix':confusion_matrix(y[ix],pred,labels=[1,2,3]).tolist()}\n        predictions.extend({'model':name,'split':part,'source_id':int(table.source_id.iloc[r]),'observed':int(y[r]),'predicted':int(v)} for r,v in zip(ix,pred))\nprint(json.dumps(metrics,indent=2));pd.DataFrame(predictions).to_csv(OUT/'predictions.csv',index=False)\n"),
('m','## Geometry plot\nPlotting only two recorded features is an exploratory view, not proof of class separation in all seven dimensions. Source physical units are unresolved and are not invented in the axes.'),
('c',"plt.figure(figsize=(7,4))\nfor label in [1,2,3]:\n    ix=train[y[train]==label]\n    plt.scatter(X[ix,0],X[ix,1],label=f'class {label}',s=18)\nplt.xlabel('Area (provider numerical units)');plt.ylabel('Perimeter (provider numerical units)')\nplt.title('Seeds: training observations only');plt.legend();plt.tight_layout()\nshow_and_save(OUT/'training_geometry.png')\n"),
('m','## Advanced return: topology of a feature cloud\nUse the first 24 sorted training row identities, selected without consulting outcomes or diagrams. All seven standardized features define the metric. This is descriptive, not a new predictive feature or a claim of physical grain holes.'),
('c',"from shape_lab.persistence import rips_filtration,persistent_homology,diagram\nsubset=np.sort(train)[:24];scaler=StandardScaler().fit(X[train]);cloud=scaler.transform(X[subset])\nintervals=persistent_homology(rips_filtration(cloud,max_homology=1),max_dim=1)\nrecords=[{'dim':a.dim,'birth':float(a.birth),'death':None if np.isinf(a.death) else float(a.death)} for a in intervals]\nprint('Subset source IDs:',table.source_id.iloc[subset].tolist())\nprint('Positive finite H1 intervals:',diagram(intervals,1,finite_only=True))\nsave_json(OUT/'persistence.json',{'source_ids':table.source_id.iloc[subset].tolist(),'intervals':records,'infinite_death_encoding':None})\n"),
('m','## Record the scope, not just the score\nRead the model errors before opening the separate solutions. These test labels are now exposed; later tuning needs a newly justified evaluation protocol.'),
('c',"fitted={}\nfor name,(model,cols) in models.items():\n    if hasattr(model,'named_steps'):\n        z=model.named_steps['standardscaler'];m=model.named_steps['logisticregression']\n        fitted[name]={'feature_indices':cols,'center':z.mean_.tolist(),'scale':z.scale_.tolist(),'coef':m.coef_.tolist(),'intercept':m.intercept_.tolist(),'classes':m.classes_.tolist()}\nsave_json(OUT/'fitted_parameters.json',fitted)\nsave_json(OUT/'results.json',{'source_numeric_sha256':meta['numeric_sha256'],'n':len(table),'metrics':metrics,'compactness_max_abs_gap':float(compactness_gap.max()),'scope':'Fixed within-collection demonstration. No farm/batch independence; no predictive TDA comparison in this lab.'})\nsave_json(OUT/'protocol.json',{'seed':17,'features':meta['features'],'split_sizes':{k:len(v) for k,v in parts.items()},'models':'fixed C=1; same rows; no tuning','persistence_subset':'first 24 sorted training row indices','data_acquisition':meta['acquisition'],'split_audit':audit})\nprint('Saved protocol, splits, predictions, metrics and diagram records.')\n")]
LABS['concrete_slump']=[('m',lessons['concrete_slump'].split('## What a baseline')[0]),('c',SETUP+"\nOUT=ROOT/'reports/v7/concrete_slump';OUT.mkdir(parents=True,exist_ok=True)\ntable,meta=load_snapshot('concrete_slump')\ndisplay(table.head());print(meta['units'])\n"),
('m','## Keep decision-time inputs separate from outcomes\nPredict 28-day strength from seven ingredient quantities. The ID and the other two measured responses are excluded. This is not a deployable structural-engineering tool.'),
('c',"X=table[meta['features']].to_numpy();y=table.strength_mpa.to_numpy()\norder=np.random.default_rng(41).permutation(len(table))\ntrain,cal,test=order[:52],order[52:77],order[77:]\nparts={'train':train,'calibration':cal,'test':test}\nprint({k:len(v) for k,v in parts.items()})\naudit=overlap_report(parts,table.source_id.to_numpy());assert audit['row_disjoint']\nsplit=pd.DataFrame({'source_id':table.source_id,'split':''})\nfor name,ix in parts.items():split.loc[ix,'split']=name\nsplit.to_csv(OUT/'split.csv',index=False)\n"),
('m','## Fit once\nStandardization and ridge fitting use only the 52 training rows. The fixed model is not retuned or refitted after looking at calibration outcomes.'),
('c',"from sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import Ridge\nfrom sklearn.metrics import mean_absolute_error,mean_squared_error\nfrom shape_lab.practice_v7 import absolute_errors,interval_bounds,empirical_coverage,mean_baseline\nmodel=make_pipeline(StandardScaler(),Ridge(alpha=10.0))\nmodel.fit(X[train],y[train]);cal_pred=model.predict(X[cal]);test_pred=model.predict(X[test])\nscores=absolute_errors(y[cal],cal_pred)\nalpha=.1;k=conformal_rank(len(cal),alpha);radius=conformal_radius(scores,alpha)\nprint('Calibration count, one-based rank, radius in MPa:',len(cal),k,radius)\nassert k==24\nlo,hi=interval_bounds(test_pred,radius)\npd.DataFrame({'source_id':table.source_id.iloc[cal].to_numpy(),'observed':y[cal],'predicted':cal_pred,'score':scores}).to_csv(OUT/'calibration.csv',index=False)\n"),
('m','## A finite test fraction is not a per-recipe guarantee\nEvaluate both errors and interval width. Exchangeability of future calibration/test scores is an assumption, not established by the random permutation.'),
('c',"baseline=mean_baseline(y[train],len(test))\nmetrics={'test_n':len(test),'ridge_mae_mpa':float(mean_absolute_error(y[test],test_pred)),\n 'ridge_rmse_mpa':float(np.sqrt(mean_squared_error(y[test],test_pred))),\n 'mean_baseline_mae_mpa':float(mean_absolute_error(y[test],baseline)),\n 'nominal_coverage':1-alpha,'empirical_test_coverage':empirical_coverage(y[test],lo,hi),\n 'covered_count':int(((lo<=y[test])&(y[test]<=hi)).sum()),'calibration_n':len(cal),'rank':k,'radius_mpa':radius,'width_mpa':2*radius}\nprint(json.dumps(metrics,indent=2))\npd.DataFrame({'source_id':table.source_id.iloc[test].to_numpy(),'observed_mpa':y[test],'predicted_mpa':test_pred,'lower_mpa':lo,'upper_mpa':hi,'covered':(lo<=y[test])&(y[test]<=hi)}).to_csv(OUT/'predictions.csv',index=False)\n"),
('m','## Inspect all 26 held-out intervals\nThe plot is ordered by prediction, not collection time. A negative lower bound is not silently clipped. Large widths can be statistically conservative but practically unhelpful.'),
('c',"p=np.argsort(test_pred);horizontal=np.arange(len(test))\nplt.figure(figsize=(8,4));plt.errorbar(horizontal,test_pred[p],yerr=radius,fmt='o',capsize=2,label='prediction ± calibrated radius')\nplt.scatter(horizontal,y[test][p],marker='x',label='observed strength');plt.xlabel('Test observations ordered by prediction');plt.ylabel('28-day strength (MPa)')\nplt.title('Concrete mixtures: fixed split-conformal intervals');plt.legend();plt.tight_layout();show_and_save(OUT/'intervals.png')\n"),
('m','## Check the edge case by hand\nNine scores cannot give an informative finite 99% radius under this rule. Infinity is a mathematically explicit result rather than a hidden fallback.'),
('c',"assert conformal_rank(9,.2)==8\nassert conformal_radius(np.arange(1,10),.2)==8\nassert np.isinf(conformal_radius(np.arange(1,10),.01))\nprint('Nine-score example: 80% radius=8; 99% radius=infinity.')\nz=model.named_steps['standardscaler'];m=model.named_steps['ridge']\nsave_json(OUT/'fitted_parameters.json',{'features':meta['features'],'center':z.mean_.tolist(),'scale':z.scale_.tolist(),'coef':m.coef_.tolist(),'intercept':float(m.intercept_)})\nsave_json(OUT/'results.json',metrics)\nsave_json(OUT/'protocol.json',{'source_numeric_sha256':meta['numeric_sha256'],'seed':41,'split_sizes':{k:len(v) for k,v in parts.items()},'inputs':meta['features'],'target':'strength_mpa','fixed_model':'StandardScaler + Ridge(alpha=10)','alpha':alpha,'score':'absolute residual','rank_rule':'ceil((n+1)*(1-alpha)); infinite if n+1','independence_limit':'Missing true batch/time identities; marginal guarantee requires exchangeability not established here','split_audit':audit,'data_acquisition':meta['acquisition']})\n")]
LABS['leakage']=[('m',lessons['leakage'].split('## Why a nearest')[0]),('c',SETUP+"\nOUT=ROOT/'reports/v7/leakage';OUT.mkdir(parents=True,exist_ok=True)\ntable,meta=load_snapshot('seeds')\nX=table[meta['features']].to_numpy();y=table.variety.to_numpy()\n# These copies are a manufactured stress test, not new observed kernels.\nXcopy=np.repeat(X,3,axis=0);ycopy=np.repeat(y,3);unit=np.repeat(table.source_id.to_numpy(),3)\nprint('Observed kernels:',len(X),'constructed rows:',len(Xcopy))\n"),
('m','## Disjoint array rows can share the same source\nCompare randomized row assignment to a group split on kernel IDs. The group split evaluates new source kernels in this collection, not new farms.'),
('c',"from sklearn.model_selection import train_test_split,GroupShuffleSplit\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.neighbors import KNeighborsClassifier\nrows=np.arange(len(Xcopy))\na,b=train_test_split(rows,test_size=.3,random_state=73,stratify=ycopy)\ngroup_train,group_test=next(GroupShuffleSplit(n_splits=1,test_size=.3,random_state=73).split(Xcopy,ycopy,groups=unit))\nsplits={'row_split':(a,b),'unit_split':(group_train,group_test)}\naudits={};results={};records=[]\nfor name,(tr,te) in splits.items():\n    audits[name]=overlap_report({'train':tr,'test':te},unit)\n    model=make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors=1)).fit(Xcopy[tr],ycopy[tr])\n    pred=model.predict(Xcopy[te]);results[name]={'test_rows':len(te),'test_units':int(len(np.unique(unit[te]))),'accuracy':float((pred==ycopy[te]).mean()),'correct':int((pred==ycopy[te]).sum()),'shared_units':len(audits[name]['pairs']['train|test']['shared_units'])}\n    for part,ix in [('train',tr),('test',te)]:\n        records.extend({'experiment':name,'split':part,'copy_row':int(i),'source_id':int(unit[i])} for i in ix)\nprint(json.dumps(results,indent=2))\nassert audits['row_split']['row_disjoint'] and not audits['row_split']['unit_disjoint']\nassert audits['unit_split']['row_disjoint'] and audits['unit_split']['unit_disjoint']\npd.DataFrame(records).to_csv(OUT/'split.csv',index=False)\n"),
('m','## See the mechanism, not just the score\nCount test kernels with a training copy. A high score under that condition need not indicate generalization.'),
('c',"names=list(results);plt.figure(figsize=(7,4))\nplt.bar(names,[results[k]['accuracy'] for k in names]);plt.ylim(0,1.05);plt.ylabel('Constructed-copy test accuracy');plt.title('A manufactured leakage demonstration on real feature vectors')\nplt.tight_layout();show_and_save(OUT/'split_comparison.png')\n"),
('m','## Numerical representation can dominate a raw metric\nMultiply the first feature by 1000 as a declared representation change. Training standardization should cancel that positive linear scale change on the same rows; this is an arithmetic test, not an assumed unit definition.'),
('c',"from shape_lab.practice_v7 import fit_scaler,apply_scaler\ntr=np.arange(126);te=np.arange(126,210)\nc,s=fit_scaler(X[tr]);z=apply_scaler(X[te],c,s)\nscaled=X.copy();scaled[:,0]*=1000\nc2,s2=fit_scaler(scaled[tr]);z2=apply_scaler(scaled[te],c2,s2)\nassert np.allclose(z,z2)\nprint('Maximum standardized difference:',np.max(np.abs(z-z2)))\nprint('Raw distance first two rows:',np.linalg.norm(X[0]-X[1]),np.linalg.norm(scaled[0]-scaled[1]))\n# This identity demo does not train a classifier on the class-ordered first 126 rows.\n"),
('m','## Save the construction and its limits\nA group ID protects only the grouping it actually represents. There are no available farm identifiers. Synthetic duplicates must remain labeled as such in any presentation.'),
('c',"save_json(OUT/'results.json',{'models':results,'standardized_max_abs_difference':float(np.max(np.abs(z-z2))),'data_role':'observed Seeds vectors, each copied three times in software; NOT 630 observed kernels'})\nsave_json(OUT/'protocol.json',{'source_numeric_sha256':meta['numeric_sha256'],'copy_rule':'np.repeat(...,3,axis=0)','seed':73,'model':'training StandardScaler + 1-nearest-neighbor','audits':audits,'scope':'illustrative leakage stress test, not estimate of bias in another domain'})\n")]
LABS['claims']=[('m',lessons['claims'].split('## Continuous dynamics')[0]),('c',SETUP+"\nOUT=ROOT/'reports/v7/claims';OUT.mkdir(parents=True,exist_ok=True)\nfrom shape_lab.practice_v7 import oscillator_energy,symplectic_defect,sphere_newton_step,gradient_inner_product,compactness\n"),
('m','## Symplectic is not synonymous with exact energy\nThis nondimensional oscillator provides an exact arithmetic counterexample to the universal discrete-step claim. It is not measured climate or basketball data.'),
('c',"h=.2;A=np.array([[1-h*h,h],[-h,1.]])\nz=np.array([1.,0.]);znew=A@z\nenergy_before=oscillator_energy(z);energy_after=oscillator_energy(znew);defect=symplectic_defect(A)\nprint('State:',znew,'energy:',energy_before,energy_after,'symplectic defect:',defect)\nassert np.allclose(znew,[.96,-.2]);assert np.isclose(energy_after,.4808);assert defect<1e-14\nassert not np.isclose(energy_before,energy_after)\n"),
('m','## Inspect a rollout without promoting bounded error to exact conservation\nA particular stable step size and linear system are not a theorem for arbitrary nonlinear learned systems.'),
('c',"trajectory=[z.copy()]\nfor _ in range(300):trajectory.append(A@trajectory[-1])\ntrajectory=np.asarray(trajectory);energies=np.sum(trajectory**2,axis=1)/2\nplt.figure(figsize=(7,4));plt.plot(np.arange(len(energies))*h,energies,label='discrete energy');plt.axhline(.5,linestyle='--',label='initial energy')\nplt.xlabel('Nondimensional integration time');plt.ylabel('Nondimensional H');plt.title('Symplectic Euler: oscillating, not exactly constant H');plt.legend();plt.tight_layout();show_and_save(OUT/'energy.png')\n"),
('m','## One nonlinear correction is only a first-order step\nThe same formula is iterated below, but the first step alone does not land on the circle.'),
('c',"x=np.array([2.,0.]);first=sphere_newton_step(x);first_residual=float(first@first-1)\nassert np.allclose(first,[1.25,0.]);assert np.isclose(first_residual,.5625)\nresiduals=[]\nfor _ in range(6):\n    x=sphere_newton_step(x);residuals.append(float(x@x-1))\nprint('Successive constraint residuals:',residuals)\ntry:sphere_newton_step([0.,0.])\nexcept ValueError:print('Rank-deficient origin rejected explicitly.')\n"),
('m','## Incompatible descent conditions\nFor this opposite pair, at least one first-order loss change is nonnegative for every update direction. The test examines directions; the algebra in the lesson proves the general statement for the pair.'),
('c',"g1=np.array([1.,0.]);g2=-g1\ndirections=np.random.default_rng(7).normal(size=(100,2))\nstrict_both=(directions@g1>0)&(directions@g2>0)\nassert not strict_both.any();print('Gradient dot product:',gradient_inner_product(g1,g2))\n"),
('m','## Observed-data bridge: different notions of shape\nThe seven-dimensional Seeds feature cloud and a physical grain are different objects. Compactness changes under a rectangle stretch although the filled rectangles remain homeomorphic.'),
('c',"table,meta=load_snapshot('seeds')\nrectangle_compactness=compactness([2.,4.],[6.,10.])\nprint('Manufactured rectangles:',rectangle_compactness)\nprint('Observed compactness range:',float(table.compactness.min()),float(table.compactness.max()))\nsave_json(OUT/'results.json',{'energy_before':energy_before,'energy_after':energy_after,'symplectic_defect':defect,'first_projection_residual':first_residual,'iteration_residuals':residuals,'opposed_gradient_dot':float(g1@g2),'rectangle_compactness':rectangle_compactness.tolist(),'observed_source':'Seeds feature table; no dynamics measured','scope':'original analytic and numerical counterexamples, not empirical reproduction of supplied posts'})\n")]

QUESTIONS={
'seeds':[
 ('What does one row represent, and what do its seven columns not contain?','One recorded kernel represented by extracted geometric features. The table does not include original X-ray images, acquisition dates, farm identity or an observed growth trajectory.'),
 ('Why are two equal class-number differences not physical distances?','Class integers encode category identity; their numeric spacing is arbitrary. A relabeling changes the differences without changing the categories.'),
 ('Calculate compactness for rectangles 2×1 and 4×1. Did their topology change?','The values are 2π/9 and 4π/25. Both filled rectangles remain disk-like; compactness is geometric, not a homeomorphism invariant.'),
 ('Why must the scaler be fitted only on the declared training rows?','Otherwise parameters of the representation use held-out data. Training-only fitting defines an inductive protocol even though it does not solve missing batch information.'),
 ('What space does H1 describe in the small Rips experiment?','A selected and standardized seven-feature point cloud. It is not direct evidence of a hole in a wheat kernel.'),
 ('What additional data is required for a new-farm claim?','Farm/site and relevant batch/date identifiers, independently acquired new-site observations and a split matching the intended deployment, among other domain-specific requirements.')],
'concrete_slump':[
 ('Why exclude source_id, slump and flow from these predictors?','The ID is not a causal ingredient, and slump/flow are measured responses unavailable under the chosen pre-measurement task. Another task may use them only after documenting availability.'),
 ('For 25 calibration errors and α=0.1, which sorted value is used?','ceil(26×0.9)=24, one-based: Python index 23. No interpolated quantile is used.'),
 ('Why might a small calibration set return an infinite radius?','The finite-sample corrected rank can be n+1 at an extreme target coverage. A finite maximum would not implement the chosen conservative rank rule.'),
 ('Does 90% nominal marginal coverage guarantee this particular recipe?','No. The guarantee averages over calibration and test sampling under its assumptions. It does not give pointwise conditional coverage for every recipe.'),
 ('Why is a wide interval potentially unhelpful even with high coverage?','Coverage alone can be achieved by nearly uninformative sets. Width in MPa and consequences of uncertainty must be reported too.'),
 ('Does a random row permutation prove exchangeability?','No. It does not erase dependence, collection shifts, or missing physical batch identities. The protocol is an educational within-collection study.')],
'leakage':[
 ('How many observed kernels are there after making three copies of each row?','Still 210. The 630 software rows include constructed copies, not independent new observations.'),
 ('Can row indices be disjoint while source kernels overlap?','Yes. Separate copies have different row indices but the same source ID; compare those identities explicitly.'),
 ('Why can one-nearest-neighbor benefit strongly from duplicates?','An exact training copy is at distance zero from a test copy; this rewards memorization of the same evidence rather than transfer to a new kernel.'),
 ('Why not repair the audit by generating unique IDs for every copy?','That changes the meaning of the unit key and conceals the problem. Unit identity must reflect the independent object under evaluation.'),
 ('What remains invariant under a consistent positive column rescaling followed by training standardization?','For the same training rows, the standardized numerical arrays agree up to floating-point error. The statement does not extend to arbitrary nonlinear changes.'),
 ('What group would matter for a deployment on previously unseen camera sessions?','Session identity and, as appropriate, participant/site identity and timing support. A row-only split cannot establish that independence.')],
'claims':[
 ('Compute the first symplectic Euler state and energy for the worked oscillator.','From (1,0), h=.2: p_new=-.2, q_new=.96, H_new=.4808, not .5.'),
 ('What does A.T J A=J establish here, and what does it not establish?','It establishes the canonical symplectic matrix condition for this linear update. It does not establish exact conservation of the chosen H for every step.'),
 ('Why does the sphere correction yield residual .5625?','At (2,0), the linearized correction subtracts (.75,0), leaving (1.25,0); 1.25²-1=.5625.'),
 ('Why is the sphere correction undefined at the origin?','The constraint Jacobian is zero and its required rank condition fails; there is no unique direction supplied by this formula.'),
 ('Can a direction decrease objectives with opposite gradients strictly to first order?','No. Requiring g·d>0 and -g·d>0 simultaneously is contradictory.'),
 ('Does the new lab reproduce Norm-PCGrad benchmark superiority?','No. It tests small operations and counterexamples. The paper’s selected-domain benchmark results remain attributed external findings, not reproduced here.')]
}

manifest=[];question_cards=[]
for key,(title,parent,activities) in case_defs.items():
    folder=R/parent/key;folder.mkdir(parents=True,exist_ok=True)
    write(folder/'lesson.md',lessons[key])
    notebook(folder/'lab.ipynb',LABS[key])
    intro=[('m',f'# {title} — independent coding\n\nFour small assignments. Try the learner version first. Reading a reference answer is not independent completion. All checks are illustrative tests, not a guarantee for every input.'),('c',SETUP)]
    learner=list(intro);answers=list(intro);solution=['# Coding answer explanations\n']
    for i,(fn,prompt,check,hint) in enumerate(activities,1):
        ident=f'{key}.C{i}';source=inspect.getsource(getattr(P,fn))
        header=source.split('\n')[0]
        stub=header+'\n    # Your independent implementation goes here.\n    raise NotImplementedError("Learning exercise '+ident+'")\n'
        text=f'## {ident} — `{fn}`\n\n{prompt}\n\nPredict one result by hand before running the check.\n\n<details><summary>Hint</summary>{hint}</details>'
        learner += [('m',text),('c',stub),('c',check)]
        answers += [('m',text),('c',source),('c',check+f"\nprint('{ident}: reference check passed')")]
        solution.append(f'## {ident}\n\n{prompt}\n\n{hint}\n\n```python\n{source}```\n\nCheck:\n```python\n{check}\n```')
    notebook(folder/'learner.ipynb',learner);notebook(folder/'answers.ipynb',answers)
    write(folder/'solutions.md','\n\n'.join(solution))
    qtext=['# Concepts, transfer and delayed recall\n\nAnswer before revealing the criteria. These are not automatically graded.']
    for i,(q,a) in enumerate(QUESTIONS[key],1):
        ident=f'{key}.Q{i}';qtext.append(f'## {ident}\n\n{q}\n\n<details><summary>Answer criteria</summary>\n\n{a}\n\n</details>')
        question_cards.append({'id':ident,'kind':'concept','question':q,'answer':a})
    for i,j in enumerate([0,2,5],1):
        q,a=QUESTIONS[key][j];ident=f'{key}.R{i}'
        q='Without reopening the lab, answer and invent one contrasting example: '+q
        a=a+' A correct contrasting example must change a relevant assumption, not merely a numerical constant.'
        qtext.append(f'## {ident} — delayed recall\n\n{q}\n\n<details><summary>Criteria</summary>\n\n{a}\n\n</details>')
        question_cards.append({'id':ident,'kind':'recall','question':q,'answer':a})
    write(folder/'questions.md','\n\n'.join(qtext))
    write(folder/'MY_RESPONSE.md',f'# My response: {title}\n\nStatus: unassessed. Copy this file to my_work before editing.\n\n## Prediction before execution\nWrite your own prediction here.\n\n## Hand calculation\nRecord quantities, units and assumptions.\n\n## Observation and evidence path\nRecord the notebook, code revision and output you actually ran.\n\n## Explanation and counterexample\nExplain a result and what would change it.\n\n## Unsupported conclusion\nName one claim this evidence does not justify.\n\n## Independent assessment\nRecord your own answer and later feedback; reading a solution is not an independent pass.')
    manifest.append({'id':key,'title':title,'type':'industry' if parent=='applications_v7' else 'methods','path':str(folder.relative_to(R)),'reference_notebooks':[str((folder/'lab.ipynb').relative_to(R)),str((folder/'answers.ipynb').relative_to(R))],'learner_notebook':str((folder/'learner.ipynb').relative_to(R)),'coding_exercises':4,'concepts':6,'recall':3})
write(R/'docs/v7/new_sections.json',json.dumps(manifest,indent=2));write(R/'docs/v7/questions.json',json.dumps(question_cards,indent=2))
print('Created four teaching sections, eight reference notebooks, four learner notebooks and sixteen exercises.')
