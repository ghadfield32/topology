# How to work through the whole system

## One foundation, two tracks
Stages 00–12 remain the original topology/TDA course. Stages 13–20 add geometry, measured reconstruction, a source-critical VGGT introduction, systems and cautious temporal reasoning. The first route is sequential. After the topology foundation is comfortable, prerequisite lists allow targeted review; no script skips prerequisites based on your job title.

You do not need a GPU, model weights or an external dataset to execute the required CPU labs. First-time package installation needs internet or a cache. Offline HTML pages and saved outputs need no Python installation. Optional external model inference is deliberately separate.

## Efficient study without shallow completion
Use three passes per stage. In the first, read the lesson, inspect its smallest example, and explain the vocabulary. In the second, work the beginner workbook and run the reference lab only after predicting the output. In the third, complete your coding practice and conceptual questions without the answer file open. Use the solution to diagnose mistakes, not to count a copied answer as independently solved.

Each stage has a linked learning section: lesson, workbook, lab, learner code, reference answers, conceptual solutions and mastery gate. The new geometry stages have three coding exercises each; the original core stages retain five each. All stages have separate learner notebooks with intentional unfinished functions.

A practical session has one question, one calculation, one code change and one explanation. When a symbol or step is unfamiliar, open a foundation primer immediately. Stop accumulating new terminology until you can explain the previous distinction. A familiar prerequisite can be tested rather than reread, but an unknown one is not assumed away.

## Six primers
Numbers and notation; Python; proof-writing; linear algebra; calculus for geometry; and measurement uncertainty/evidence. The last two introduce derivatives, Jacobians and covariance from examples rather than presupposing a calculus course. The course does not assess fluency merely because the reader opened the primer.

## Record evidence, not a checkmark
The new default is `progress/learning_log_v3.json`, with stages 00–20 initially unassessed. Use the existing commands:

```bash
python scripts/learn.py status
python scripts/learn.py due
python scripts/learn.py handoff
```

After writing a real answer file under `my_work/`, record a declared assessment:

```bash
python scripts/learn.py record --stage 0 --kind assessment --score 90 --evidence my_work/stage_00_answers.md --independent --critical-clear
```

The score and flags are your declarations, not an automated correctness judgment. Use `--kind practice` for guided work. The file must exist; its bytes are hashed. Do not use independent or critical-clear flags merely because a notebook's reference checks passed. Delayed recall uses `--kind recall`. The tool calculates review dates only when you run it; no notification or background task is scheduled.

## Preserve work when moving from v2
Extract v3 into a new folder. Copy your `my_work/` material with its relative paths intact. Preserve your prior notebooks separately; merge your answers into new learner notebooks rather than overwriting updated instructions. Keep your old log as a backup.

The migration command writes a NEW log and refuses to overwrite an existing path:

```bash
python scripts/migrate_progress_v3.py --source /path/to/v2/progress/learning_log_v2.json --output progress/my_migrated_log_v3.json
python scripts/learn.py --log progress/my_migrated_log_v3.json status
```

Continue passing `--log progress/my_migrated_log_v3.json` with record, due and handoff. Existing attempt records, scores, notes, evidence paths and hashes are preserved; stages 13–20 start empty. Evidence paths remain meaningful only when the referenced files are copied unchanged. The legacy browser progress page and JSON command-line log are separate stores; no synchronization is implied.

## Delayed recall and repair
The original 39 recall questions remain in `practice/retrieval.md`; 24 geometry questions are in `practice/retrieval_v3.md`. Try them after a delay with source material closed. Record the error precisely, reread the smallest relevant section, solve a different example, and retest later. Do not restart the whole course after one mistake.

## Completion means a defensible scope
Core completion requires definitions, counterexamples, hand calculations, elementary proofs, a small implemented algorithm, interpretation and an independent capstone. The geometry continuation adds coordinate correctness, reference-aware reconstruction, causal evidence and a model-run audit. Passing synthetic model-shape fixtures does not satisfy real-model execution. An actual-book audit remains separate until the complete text is available.

## Continuing here
At the end of a stage, provide your answer file or notebook, your current log/handoff and one unresolved question. Review should distinguish arithmetic mistakes, misunderstood definitions, missing assumptions, implementation bugs and unjustified interpretations. Work on the earliest unresolved foundation rather than replacing the course with a new roadmap.
