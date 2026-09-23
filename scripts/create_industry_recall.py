"""Make three explicit delayed-recall prompts for each case; no automatic grading."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
cat=json.loads((R/'data/industries/catalog.json').read_text())['datasets']
traps={
'wdbc':('What does a high score on this partition fail to establish?', 'The original IDs/sites are absent. This image-summary split is not independent clinical or new-site validation.'),
'wine':('How can a training query accidentally get an advantage in a local topology descriptor?', 'Including the training query itself as a reference point creates an advantage absent for an unseen query. Reserve and freeze the reference set; compare models on identical fitting rows.'),
'stackloss':('Why is source order not automatically a forward-time evaluation?', 'Dates and their validated ordering are absent from the distribution. Call it a source-order holdout, not established temporal forecasting.'),
'grunfeld':('Why lag firm value before forecasting investment?', 'The supplied same-year value is measured at year end. It is not established to be available when making an earlier prediction; group by firm before lagging.'),
'co2':('What observations can one forecast window depend on?', 'Only past finite measurements at the expected weekly spacing. In this strict protocol the full input-to-target support belongs to one raw time block; never interpolate across a held-out boundary silently.'),
'nile':('Why is a fitted mean change not a discovered cause?', 'The breakpoint minimizes a retrospective objective; other processes can explain a mean shift. Independent causal evidence and an explicit competing explanation are needed.'),
'elnino':('How do you prevent climatology from seeing future observations?', 'Fit all twelve monthly means using training years only, then apply them unchanged. Keep sequence order and account for whole-window support at the split.'),
'modechoice':('Why must four alternative rows travel together through a split?', 'They belong to one decision maker and one choice set. Splitting rows leaks a person and can leave incomplete choice sets. The sample is choice-based, not a population market-share estimate.')}
rec=[];questions=[]
for m in cat:
    k=m['id'];qa=[('What is one observation here, and when is a row not an independent example?',m['observation_unit']),traps[k],('State one unsupported conclusion and the additional evidence needed.',m['scope_limitations']+' Name an independent evaluation appropriate to the claim; explain what the existing data do not contain.')]
    for i,(q,a) in enumerate(qa,1):rec.append({'id':f'{k}.R{i}','case':k,'question':q,'answer':a})
    p=R/f'industry/answers/{k}.md';s=p.read_text().split('## Delayed recall')[0]
    s+='## Delayed recall: attempt after a gap\n\n'
    for i,(q,a) in enumerate(qa,1):s+=f'### {k}.R{i}\n\n{q}\n\n**Answer criteria:** {a}\n\n'
    p.write_text(s)
    lesson=(R/f'industry/lessons/{k}.md').read_text()
    # Actual conceptual question and answer sections generated for this case.
    for match in re.finditer(r'## ('+k+r'\.Q\d+)\n\n(.*?)\n\n\*\*Reasoning:\*\* (.*?)(?=\n\n## |\Z)',s,re.S):
        ident,q,a=match.groups();questions.append({'id':ident,'case':k,'question':q,'answer':a.strip()})
assert len(questions)==32 and len(rec)==24
(R/'industry/retrieval.json').write_text(json.dumps(rec,indent=2)+'\n')
(R/'industry/concept_questions.json').write_text(json.dumps(questions,indent=2)+'\n')
