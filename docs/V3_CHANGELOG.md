# Version 3 changes

Preserved the original 13-stage teaching sequence, workbooks, exercises, solutions, datasets and exposed capstone predictions from version 2. Updated the Stage 00 progress-file pointer to the new default without changing its mathematics. Added eight geometry lessons/workbooks, two primers, 48 conceptual exercises, 24 coding exercises, 24 recall questions, 16 reference notebooks and eight learner notebooks. Added real calibrated stereo data, original CPU geometry/attention/event implementations and an optional original-VGGT local runner. The model interface has synthetic contract tests; no trained-model inference is claimed.

Updated the learning log to support 21 stages with a no-overwrite v2 migration. Updated notebook runners to stage 20 and introduced an integrated v3 reader. Legacy v1/v2 verification documents describe their historical builds; use `VERIFICATION_V3.md` for the current release.

The source audit preserves rather than conceals disagreements: Omega project/repository announcement dates differ, and documented stereo disparity shape differs from loaded data. The math and data contracts state the applicable assumptions. WMS production code and scheduled watches were not changed.
