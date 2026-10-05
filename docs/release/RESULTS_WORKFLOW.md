# One session, one explanation, one inspectable result

Version 14 • 4 October 2026 • original workflow, not an additional theory course

## The distinction that makes this useful

A **lesson** explains a concept. An **assignment** asks you to apply it. A **reference run** executes the supplied example. A **reflection** is your explanation. An **evidence packet** keeps that explanation next to the actual executed code and outputs. None of these alone certifies that you have mastered a subject.

Use the existing primary lesson for theory. This guide adds only the steps that connect reading to your own results. It does not introduce another mandatory definition of topology, regularization, or a world model.

## Prepare a session

After the environment acceptance in [FIRST_RUN.md](FIRST_RUN.md), run:

```bash
uv run --no-sync python course.py study 0 --output my_work/study00_attempt01
```

Replace `0` with any core stage 0–30 or a named case such as `wine`, `s00`, `acb`, or `r01`. The command checks the existing catalog before creating anything. An unknown item or an existing destination is refused. It does not install packages, download data, launch a notebook, contact a service, or update your mastery record.

The new folder contains `START.md`, `prediction.md`, `reflection.json`, `study.json`, and a private `practice/` directory. `START.md` links to the same canonical lesson, lists the completion target and known prerequisites, and provides the exact run and report commands. The individual command arguments are also saved in `study.json`. Absolute paths refer to this checkout; after moving the repository, generate a new session and keep the old evidence.

## Predict before executing

Write in `prediction.md` before opening the answers. Name one observation and one feature. State the units. Choose the smallest calculation that you can do without the notebook. Write an expected result and the assumption on which it depends.

For example, a table with four athletes and three measurements is a 4-by-3 array, not twelve independent athletes. A three-dimensional position is not a velocity until a time interval is defined. A numerical distance is not meaningful until its inputs and units are specified.

Wrong predictions are not wasted effort. After running, explain which assumption was wrong or which computation was misunderstood. Do not erase the original prediction to make the work appear effortless.

## Execute the reference and inspect it

From the same prepared environment:

```bash
uv run --no-sync python course.py run --stage 0 --output my_work/study00_attempt01/run01
```

The runner uses a fresh copied workspace and fresh notebook kernels. Needed predecessor notebooks run first. Existing reports are not imported as hidden inputs. `execution.json` records the notebook identities, teaching-cell counts, runtime provenance, input continuity, and SHA-256 hashes of the produced notebook and artifact files.

Open the executed notebook. For each cell, connect the output to its inputs. Change one condition only when you can predict its effect. Run changes in your private learner copy, not in the canonical reference. Keep each attempt in a new directory; `run02` is a different experiment record, not an overwrite of `run01`.

The recorded hash proves byte continuity relative to the locally written ledger. It does not authenticate the author, certify sensor accuracy, make an exposed holdout independent, or prevent someone from manufacturing both a file and its hash.

## Solve independently

Open `practice/learner.ipynb` in Jupyter and write your answers in `practice/answer.md`. A deliberate `NotImplementedError` is an assignment. A failing reference cell is an execution failure. Use the linked answers after a serious attempt, and record what help you used.

Before moving on, explain a counterexample and a limitation. Return later for the existing delayed-recall questions. The `study` and `report` commands never change the core or case assessment logs.

## Fill the six reflection fields

Edit `reflection.json` as valid JSON. Keep the double quotes around strings and put a comma between adjacent fields. The six fields serve different purposes:

| Field | What you write | What to avoid |
|---|---|---|
| `question` | A question the actual experiment can answer. | A universal question supported by one small example. |
| `observation_unit` | Person, image, trial, time window, sample, or another explicit unit; include important units. | Treating repeated frames or copied rows as new people. |
| `method` | Data selection, baseline, transformations, model or calculation, and evaluation design. | Omitting preprocessing or selection choices. |
| `result_interpretation` | The observed result and the conclusion it supports. | Replacing a number with an unsupported claim of superiority. |
| `limitation` | The strongest reason the conclusion should not be generalized. | “More data needed” without identifying what data and why. |
| `next_experiment` | One testable change with an expected comparison and preserved evaluation boundary. | Tuning repeatedly on the exposed test set and calling it held out. |

The exporter checks that all six entries are nonempty strings. That is a completeness check, not grading. It does not judge whether your proof, terminology, or conclusion is correct. The included example reflection is explicitly assistant-authored, not your assessed work.

## Create a local report

```bash
uv run --no-sync python course.py report --run my_work/study00_attempt01/run01 --reflection my_work/study00_attempt01/reflection.json --output my_work/study00_attempt01/report01
```

Open `report01/index.html`. It contains your explanation, links to saved code/output pages, and the exact output files under `evidence/`. `packet.json` records file hashes, the source ledger hash, and `published: false`. It stays local; there is no upload or external sharing operation.

The exporter refuses changed, missing, or added run-output files; inconsistent notebook identity/count claims; missing execution cells; saved error outputs; unsafe paths; or an absent output seal. Legacy runs without the new seal require a fresh replay. If a run was edited, preserve it and make a fresh attempt rather than manually rewriting hashes to obtain a pass.

Only plain text, code and PNG notebook outputs are displayed. Arbitrary HTML, JavaScript and SVG outputs are not executed in the report. Markdown and equations remain visible as escaped source notation in this portable evidence view; the main course reader provides the fuller lesson rendering.

## Review before showing another person

The report is a draft, not an automatic public portfolio. Inspect every included file for personal paths, participant information, measurements you are not permitted to redistribute, and claims beyond the design. Locally generated hashes are not digital signatures. Check each source's data license separately from the course code license. Do not publish restricted sports excerpts under the assumption that public access means unrestricted commercial use.

A useful portfolio entry contains the question, observation unit, baseline, evaluation protocol, result, error analysis, limits, and a reproducing command. A polished page cannot compensate for an invalid split or unsupported interpretation.

## Practice in different situations without relearning the definition

| Situation | Existing route | Independent task |
|---|---|---|
| Measurement table | Stage 00 → 02 → `wine` | Explain the row unit and compare raw with training-scaled distances. |
| Image topology | Stage 05 → 06 → 08 → 11 | State the pixel/complex convention and distinguish a cycle from a boundary. |
| Environmental series | `co2` after basic array/time lessons | Identify missing observations and information available at prediction time. |
| Materials regression | `concrete_slump` after evaluation basics | Separate fitting, calibration and testing; interpret interval coverage narrowly. |
| Sports motion | `s00` → `s01` → `s02` | Convert units, identify elapsed time, and compare the proposed flight model with a simpler baseline. |
| Sports metadata | `acb` | Keep entire games together and avoid identity aliases crossing partitions. |
| Learned representations | `r01` → `r02` → `r03` → `r04` → `r05` | Distinguish covariance shape, Gaussianity, noncollapse and downstream information. |
| Physical dynamics | Stage 21 → 23 → 24 → 25 | Separate continuous conservation from discrete solver error and nonlinear-constraint residual. |

Do not skip prerequisite definitions to reach an impressive-looking model. Conversely, do not reread every optional primer after you can demonstrate the underlying skill.

## Distinct acceptance questions

A source checksum asks whether bytes match. A test checks its assertions. A repeat run checks the specified computation. An independent evaluation addresses generalization under its design. Docker acceptance checks the image/runtime. Kubernetes adds admission, scheduling, storage and Job execution. Learner mastery requires independent explanation, calculation, transfer and delayed recall.

No single green status answers all of these questions. Continue from your existing learning record; the original proof-depth requirements and actual-book audit remain in force.

## Open the completed worked example

[Wine experiment evidence](../../reports/v13/example_report/index.html) demonstrates the full workflow using real observed features. Its reflection is assistant-authored, not a learner attempt. All learner templates remain empty.
