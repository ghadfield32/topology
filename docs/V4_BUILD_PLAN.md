# Version 4: deepen, connect, and verify

## Design
Preserve the existing 21-stage topology-to-geometry curriculum, raw data, code, and learner records. Add a beginner-paced *guided session* to every stage, with an explicit local calculation, real-data connection, transfer questions, and a new executed consolidation notebook. Do not add unrelated numbered stages. Keep source-derived coverage, original explanatory additions, synthetic controls, and measured data visibly separate.

## Implementation order
1. Re-extract v3 to an isolated local folder and run the existing suite. Record dependency availability. **Done: 231 passed / 2 optional skips.**
2. Add failing tests for independent pixel topology, prime-field arithmetic, H0 spanning-tree checks, paired-prediction analysis, and progress evidence integrity. Implement and rerun.
3. Author 21 guided sessions and 42 new transfer questions with solutions. Link existing lessons, exercises and prerequisites instead of replacing them.
4. Add 21 inspectable consolidation notebooks using bundled real data and explicitly labeled controls. Execute those and all 42 pre-existing reference notebooks.
5. Add a small read-only study navigator and evidence-file verifier. Reuse the v3 progress schema without resetting it; leave every shipped stage unassessed.
6. Build a v4 offline entrypoint, verify internal links and rendering, record the current execution environment, inventory and checksum the archive, then retest an extracted copy.

## Acceptance boundaries
* No claim of full-book audit, automatic proof grading, trained VGGT execution, new physical ground truth, unseen-writer evaluation, or external-library agreement without the corresponding evidence.
* Existing worked results are exposed demonstrations. Any new statistical examination of those predictions is exploratory and does not create a fresh holdout.
* An unavailable optional package remains a named skip. Mac and Windows instructions are instructions, not execution evidence.
* The additions are original course supplements, not quotations or corrections silently substituted into the supplied source material.
