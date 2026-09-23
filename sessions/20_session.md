# Stage 20 guided session — Turn a completed course into a reproducible next investigation

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/20_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/20_lab.ipynb). The [original workbook](../workbooks/20_workbook.md) and [worked lab](../notebooks/20_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Actual bundled dataset bytes and executed reference reports; learner and deployment claims remain separate.

## What you will be able to demonstrate

1. Assemble the chain from question through measurement, representation, computation and claim.
2. Audit the presence and integrity of execution evidence without equating it with mastery.
3. Identify what a new independent dataset must provide for the intended claim.
4. Use a finite completion contract while leaving advanced topics and the actual-book audit explicit.

## Start with the claim you want to make
A useful capstone begins with a question narrow enough to test. For example: does a chosen topological representation improve a declared prediction task over a specified baseline on independent sessions? Or: after fitting scale and pose on anchor measurements, how accurate are reconstructed distances at different held-out locations? Those questions require different data and evaluation procedures.

Write the observation unit first. An image is not a person, a frame is not an independent session, and a reference-generated coordinate is not a new physical measurement. Define units, identifiers, timestamps, and missing-data treatment before building features. List which quantities are measured, fitted, assumed, or generated for a control.

## Build a reproducible claim chain
A report should connect the question to the source records, transformations, mathematical object, parameters, code revision, test evidence, numerical results, and interpretation. If one link changes, downstream results may need rerunning. Hashes can detect byte changes; they cannot tell you whether the content is true. A semantic change may require an experiment even when a software test still passes.

The v4 evidence verifier reads the existing progress log and checks whether each referenced answer file still matches its recorded hash. Missing, changed, or outside-folder paths are reported separately. It does not rewrite the history, score your proof, or treat a modified answer as dishonest. Revision is normal; save a new dated answer and record a new attempt when appropriate.

## Complete the foundation without endless restarting
The course's core scope is the agreed introductory topology and TDA path, plus the applied geometry continuation. The included lessons, original exercises, coding practice, consolidation sessions, proofs, and capstone cover that declared scope at explicitly stated levels. Reading a page is not the same as independently proving its statements or applying them to new data.

Use the objective matrix to find a specific missing capability. Repair that prerequisite, solve a fresh transfer problem, and continue. Do not restart Stage 00 merely because you encountered a difficult theorem later. Likewise, do not add a new modeling architecture to avoid an unresolved measurement or algebra gap.

## What remains an honest next step
The actual book has not been compared page by page with this course. Its audit remains unassessed. Trained VGGT inference, independent physical camera validation, real basketball event accuracy, and later advanced mathematics are separate obligations. Their absence does not invalidate the tested introductory exercises; it limits which claims those exercises support.

The notebook assembles the preceding consolidation evidence and names the boundaries. Your independent capstone must add your own question, data, analysis, and defense rather than republishing the reference outputs as personal mastery. Finish with a failure analysis and a concrete next experiment that could change your conclusion. That is a foundation capable of continued learning rather than an archive that only grows.

## Predict, execute, and explain

### Step 1

Inspect the real dataset manifests and prior experiment evidence available in this package.

```python
from hashlib import sha256
paths = [ROOT/'data/raw/iris.csv', ROOT/'data/raw/digits.npz',
         ROOT/'data/stereo/motorcycle.npz', ROOT/'data/time_series/sunspots_yearly.csv']
inventory = [{'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
              'sha256': sha256(p.read_bytes()).hexdigest()} for p in paths]
print(json.dumps(inventory, indent=2))
assert len(inventory)==4
```

### Step 2

Check the preceding consolidation reports exist. These certify reference execution only.

```python
folder = ROOT/'reports/consolidation_v4'
completed = []
for stage in range(20):
    path = folder/f'{stage:02d}.json'
    if not path.is_file():
        raise FileNotFoundError(f'Run or restore the preceding reference notebook for Stage {stage:02d}.')
    report = json.loads(path.read_text())
    assert report['execution_role']=='reference_consolidation'
    completed.append(stage)
print('preceding reference sessions:', completed)
```

### Step 3

Audit the unchanged learner-log format and leave unestablished claims false.

```python
from shape_lab.learning import read_log
from shape_lab.audits import verify_evidence
log = read_log(ROOT/'progress/learning_log_v3.json')
audit = verify_evidence(log, ROOT)
result = {'bundled_real_datasets': 4, 'preceding_reference_sessions': len(completed),
          'learner_evidence_records_checked': len(audit), 'evidence_audit': audit,
          'learner_mastery_inferred_from_reference_runs': False,
          'full_book_text_audited': False, 'VGGT_inference_executed': False,
          'independent_physical_validation': False, 'real_basketball_event_validation': False}
```

## Transfer problems — attempt without the solution

### 20.T1

A file checksum matches the saved learning record. What does that establish, and what does it not establish?

<details><summary>Reveal reasoning after your attempt</summary>

It establishes byte identity with the recorded artifact, assuming the log itself is trusted. It does not establish mathematical correctness, independence of the attempt, understanding, or retention.

</details>

### 20.T2

What is a productive response to discovering that a capstone result depends heavily on one arbitrary scale?

<details><summary>Reveal reasoning after your attempt</summary>

Report the sensitivity, revisit the measurement and metric rationale, and design a controlled comparison or new validation protocol. Do not silently choose the scale giving the most attractive result.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/20_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
