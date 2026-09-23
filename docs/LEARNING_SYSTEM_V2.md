# A learning system, not a folder of finished answers

## Three passes, one stable sequence

For each stage use the stage hub as the checklist. First read its lesson and beginner workbook, and predict the worked lab's next output. Second, run the lab and explain one controlled modification; then complete the five coding exercises in the learner notebook. Third, attempt the original conceptual exercises and new retrieval questions without the answers open. Use the proof atlas for claims that need an argument rather than numerical examples.

The primary route is stages 00→12. The four foundation primers are just-in-time explanations, not an extra semester before beginning. A 24-week calendar at roughly 8–10 hours/week is a planning example, not a completion guarantee. A shorter week can still complete one coherent session; do not replace independent reasoning with speed-reading.

## A repeatable 45–75 minute session

Spend roughly 5 minutes recalling the previous idea, 15–25 minutes on one worked explanation, 15–25 minutes on one calculation or code exercise, and 10–20 minutes on prediction, interpretation and an error note. These are suggested timeboxes. Stop at a meaningful evidence checkpoint rather than midway through an unrecorded proof.

Use four lines after each session: **What I can explain; what I calculated or ran; what I still confuse; the exact next exercise.** An error notebook is useful: write the wrong belief, a counterexample, the corrected statement and the condition you omitted.

## The assessment rubric

For a stage, evaluate definitions and examples (20 points), mathematical reasoning (25), independently written code/calculation (25), real-data interpretation (20), and limitations/reproducibility (10). Use the stage's gate and three retrieval questions as a starting sample, not the entire rubric. The proposed pass threshold is 85/100, with no unresolved critical misconception. Passing code alone cannot provide a proof or interpretation score.

A critical error includes confusing boundaries with all cycles, claiming a continuous bijection automatically has a continuous inverse, interpreting a finite point sample as the continuous shape itself, ignoring coefficient fields, calling every long bar meaningful, or fitting evaluation preprocessing on test data. Identify the relevant errors for the stage rather than assigning an unexplained blanket checkbox.

## Evidence-backed local log

`progress/learning_log_v2.json` is the canonical new course log. It starts with zero attempts. It stores dates, scores, independent/critical-clear declarations, a relative evidence-file path and its SHA-256 hash. It has no cloud calls and does not modify your source datasets. The score and flags are supplied by you or a human/tutor reviewer; the program does not understand or grade your mathematical argument.

Create an answer file under `my_work/` before recording an attempt. Example from the course directory:

```bash
python scripts/learn.py status
python scripts/learn.py record --stage 0 --kind practice --score 60 \
  --evidence my_work/00_answers.md --note "First attempt; needed the array primer"
python scripts/learn.py record --stage 0 --kind assessment --score 90 \
  --evidence my_work/00_assessment.md --independent --critical-clear
python scripts/learn.py due
python scripts/learn.py handoff
```

The example filenames are files YOU create; the package does not pre-fill successful learner work. The CLI rejects nonexistent evidence. Do not copy the illustrative scores into your record unless they honestly match your work.

States are **not_started**, **practicing**, **demonstrated**, **retained**, or **needs_review**. Practice never certifies mastery. A qualifying assessment gives demonstrated. A qualifying recall at least seven days after a qualifying independent assessment gives retained. A later unsuccessful assessment or recall marks needs_review. The day gaps are transparent policy choices, not validated cognitive measurements.

The CLI computes proposed due dates only when you run it. It does not schedule reminders, watch your activity, or keep learning in the background. Stage prerequisites guide the curriculum but are not enforced access locks; you can revisit any lesson.

## Preserve your work during upgrades

Keep an independent backup of `my_work/` and `progress/learning_log_v2.json`. Extract a new release to a new folder, inspect its change log, then copy your work and log deliberately. Do not overwrite the whole old course folder before backing up. Evidence hashes record what was submitted; changing an evidence file later will not retroactively change that recorded hash. Store revised submissions under a new name.

The v1 browser progress page is retained as a separate legacy scratchpad. Browser storage and the v2 JSON log do not synchronize. Export anything important from the browser before changing folders/browsers, and use the v2 CLI for the explicit durable record. No automatic migration is claimed.

## Continue in this chat

Paste `python scripts/learn.py handoff` output together with the actual exercise response or a complete error traceback. Ask the tutor to check reasoning, not simply to mark completion. Explain which portion you completed without hints. For a missed concept, request one changed example and one counterexample before returning to the original problem.

This record organizes your ongoing study. It does not certify the actual book's coverage, act as professional accreditation, or guarantee retention indefinitely. The final assessment, independent capstone and book audit remain separate evidence requirements.
