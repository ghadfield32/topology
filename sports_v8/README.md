# Sports learning path — v8

Begin with **S00**, or return to core Stage 00 for Python and notation. No video
model or GPU is needed for these seven required mini-stages. The full 31-stage
course is retained; this is a connected application path, not a replacement.

| Section | Main question | Prerequisite core stages |
|---|---|---|
| S00 | What is one observation, and what do its numbers mean? | 00–01 |
| S01 | How do position, angle and velocity differ? | 01–03, optional 14 |
| S02 | When does a simple flight model explain the data? | 01, 15, 21 |
| S03 | What does shape mean for player profiles? | 02, 06–09 |
| S04 | What changes when time, visibility or coordinates are uncertain? | 10, 18–19 |
| S05 | Can a model use this information at decision time? | 11–12 |
| S06 | How do we select a modern dataset and finish an independent project? | All earlier S sections |

Each section has `lessons/Sxx.md`, `notebooks/Sxx.ipynb`,
`practice/Sxx.ipynb`, and `solutions/Sxx.ipynb`. Answers to prose questions
are at the end of each lesson so you can stop before looking. Reference
execution does not mark any learner work passed.

Two required data excerpts are bundled: twelve selected 2025-12-18 SPL
basketball frames and twelve SkillCorner 2024/25 physical-profile records.
They are explicitly transcribed excerpts, not complete downloaded releases.
Source cards and current-source registry describe acquisition and licensing.

Run from the project root:

```bash
python scripts/sports_v8.py verify
python scripts/sports_v8.py stage S00
python -m jupyterlab sports_v8/notebooks/S00.ipynb
```

Protect existing work: keep `my_work/` and all existing progress JSON files.
Use `progress/sports_log_v8.json` only for this new path. It is an ordinary
manual learning record, not an automatic grading system. Full source bytes
can be independently verified later without changing the excerpt:

```bash
python scripts/sports_v8.py fetch spl --destination external_data/spl_T0001.json --accept-data-license
python scripts/sports_v8.py verify-source spl external_data/spl_T0001.json
```

The optional command was not executed successfully in the build environment.
It checks the recorded Git blob and numeric excerpt and rejects revisions,
LFS pointers, oversized content, unexpected redirects and existing targets.
