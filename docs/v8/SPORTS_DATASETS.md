# Modern sports dataset guide

Checked against primary documentation on **2026-09-21**. Release dates, collection
periods and our access date are distinct. Modernity is not a license or an accuracy
guarantee. Choose evidence that can answer your question, not the largest download.
The two bundled numeric excerpts are explicitly transcribed; other entries are
**acquisition and study plans**, not executed benchmarks.

For a beginner, work S00–S02 on the small basketball excerpt and S03–S05 on
profile data. Choose a full dataset only after its independent unit, clock, units,
labels, license and baseline are written down.

## SPL Open Data free throws

**Date:** Documentation March 2026; recent collection 2025-12-18

**Sport:** Basketball

**Evidence:** Markerless 3D estimates and shot outcomes

**What was actually done:** 12 selected frames bundled and executed; full release not downloaded

**Rights/access:** CC BY-NC-SA 4.0

**Release scope and storage:** Selected source trial 2,385,805 bytes; release 583 trials across two sessions

**Units and annotations:** xyz feet; hoop outcome inches; angle degrees; recent session 60 fps

**First experiment:** Unit/clock checks, landmark angles, fixed-gravity versus free quadratic

**Split design:** Athlete/session/trial; stable athlete IDs across sessions

**Evaluation:** Held-out trajectory errors with reference type; missingness; timing uncertainty

**Failure modes:** One selected trial cannot test prediction; no verified release label; noisy volume boundaries.

Primary source: https://github.com/Sport-Performance-Lab/SPL-Open-Data

## SkillCorner Open Data / body pose

**Date:** 2024/2025 A-League season; current documentation inspected 2026-09-21

**Sport:** Soccer

**Evidence:** Broadcast-derived XY, physical profiles and model-estimated 3D pose

**What was actually done:** 12 profile rows bundled; full tracking/pose unexecuted

**Rights/access:** MIT repository license; inspect dataset-specific hosting terms

**Release scope and storage:** 10 sample matches; XY example 97 MB; full pose approximately 3.3 GB per match

**Units and annotations:** XY metres at 10 fps; pose 29 joints at 25 fps; predicted error cm

**First experiment:** Constant-velocity tracks and detected-only coverage before learned models

**Split design:** Match first, then independent teams/venues as required; player groups for profiles

**Evaluation:** Localization/identity errors, observed-versus-extrapolated coverage; temporal alignment

**Failure modes:** Pose relative z may differ from global pitch z; XY interpolated to 25 fps is not 25 Hz independent XY measurement; full payloads need Git LFS/HF.

Primary source: https://github.com/SkillCorner/opendata

## BasketHAR

**Date:** Paper submitted 2026-04-18

**Sport:** Basketball training

**Evidence:** Wearable/IMU signals with synchronized video

**What was actually done:** Primary paper inspected; hosted data not retrieved; not bundled

**Rights/access:** Paper states Apache 2.0; verify actual hosted artifact license before acquisition

**Release scope and storage:** Not verified; inspect hosting file inventory before download

**Units and annotations:** Per-sensor units, clock offsets, rate and calibration must be read from release; not guessed

**First experiment:** Window statistics with subject-grouped evaluation; compare each modality

**Split design:** Subject/session; keep synchronized windows and overlaps together

**Evaluation:** Macro F1, balanced accuracy, latency and sensor failure sensitivity

**Failure modes:** Paper claims are not reproduced; synchronization and labels must be verified before fusion.

Primary source: https://arxiv.org/abs/2604.17065

Linked hosting: https://huggingface.co/datasets/Xian-Gao/BasketHAR

## MUVS

**Date:** Zenodo v1.0 published 2026-06-15

**Sport:** Basketball, soccer, hockey, volleyball

**Evidence:** Real handheld multiview videos and device sensors

**What was actually done:** Repository record/README inspected; video and sensor payloads not downloaded

**Rights/access:** License field not resolved in rendered record; obtain explicit release/media terms before redistribution

**Release scope and storage:** 17 events; 5,039 three-second fragments; 258 period videos; 9.8 MB record files exclude hosted video payload

**Units and annotations:** Video/sensor clocks and device frames require manifest; camera-selection labels are not 3D ground truth

**First experiment:** Timestamp audit and simple camera-selection policy before learned reconstruction

**Split design:** Whole event across all views; independent venues/devices when possible

**Evaluation:** Selection agreement, synchronization residuals; separate independently measured geometry checks

**Failure modes:** Do not equate synchronized views or sensor records with metrically calibrated cameras.

Primary source: https://zenodo.org/records/20708683

## UVY / UVY-Track

**Date:** Zenodo v1 published 2026-07-11

**Sport:** Seven sports including basketball, soccer, tennis and cricket

**Evidence:** User-generated video with multi-object tracking labels

**What was actually done:** Record inspected; payload not downloaded

**Rights/access:** Provider says source videos CC BY; record license field not fully rendered; verify per-video and annotation terms

**Release scope and storage:** 20 videos; 31,961 annotated frames; 128,258 boxes; 378 tracks; 3.3 GB ZIP

**Units and annotations:** Pixel boxes and track IDs, not calibrated 3D metres

**First experiment:** Detector plus tracker, compare with supplied labels

**Split design:** Video/event/uploader context; never adjacent-frame random split

**Evaluation:** HOTA/IDF1 plus detection recall and occlusion breakdown

**Failure modes:** Semi-automatic annotations with manual review remain reference labels, not perfect physical truth; UVY and MUVS are different.

Primary source: https://zenodo.org/records/21303900

## TrackID3x3

**Date:** 2025 paper/repository; current README inspected 2026-09-21

**Sport:** 3x3 basketball

**Evidence:** Indoor/outdoor fixed-camera and drone video with tracks and partial pose labels

**What was actually done:** Official repository inspected; linked video not downloaded

**Rights/access:** Dataset CC BY 4.0; original code Apache 2.0; third-party jersey pipeline CC BY-NC 3.0

**Release scope and storage:** Inspect linked file inventory; no size invented here

**Units and annotations:** Six on-court players; boxes all frames; ten pose keypoints some frames; metric mapping needs court calibration

**First experiment:** Tracking/identification baseline with manual court localization separated from learned steps

**Split design:** Sequence/camera/event; cross-view leakage audit

**Evaluation:** TI-HOTA/identity and court localization, conditioned on visibility

**Failure modes:** Partial pose coverage is not complete 3D mocap; code/weights/data licenses differ.

Primary source: https://github.com/open-starlab/TrackID3x3

## SoccerTrack v2

**Date:** Paper submitted 2025-08-03

**Sport:** Soccer

**Evidence:** Full-pitch panoramic 4K match video with reconstruction and ball-action labels

**What was actually done:** Primary paper inspected; payload not downloaded

**Rights/access:** Dataset license not verified from abstract; inspect linked host before acquisition

**Release scope and storage:** 10 full-length university matches; storage budget not verified

**Units and annotations:** Annotated 2D pitch positions, jersey IDs, roles, teams; 12 ball-action classes

**First experiment:** Annotated positions to team-shape descriptors; simple temporal action baseline

**Split design:** Match/venue, retaining all views and contiguous windows in one group

**Evaluation:** Tracking/reconstruction accuracy and event timing/matching under official protocol

**Failure modes:** 2D pitch labels do not provide airborne metric ball/player height.

Primary source: https://arxiv.org/abs/2508.01802

## SoccerNet Game State Reconstruction

**Date:** Task page checked 2026-09-21; page retains historical 2024 challenge placeholder

**Sport:** Soccer

**Evidence:** Broadcast reconstruction benchmark

**What was actually done:** Official task description inspected; media not downloaded

**Rights/access:** Review current task data/media access agreement; not assumed permissive

**Release scope and storage:** Page lists 57 train, 59 validation, 50 test clips of 30 seconds at 1080p

**Units and annotations:** On-field coordinates, roles, teams and jersey IDs; see official coordinate specification

**First experiment:** Official development kit and a simple calibrated tracking baseline

**Split design:** Official partitions; prohibit tuning on test results

**Evaluation:** Official GS-HOTA, plus error breakdowns

**Failure modes:** Page includes an unresolved challenge count; not presented as verified 2026 challenge statistics.

Primary source: https://www.soccer-net.org/tasks/game-state-reconstruction

## OpenBiomechanics

**Date:** Current repository documents 2026-07-04 history rewrite and release-based distribution

**Sport:** Baseball pitching/hitting and physical assessment

**Evidence:** C3D motion capture, processed signals, POI and force-plate assessments

**What was actually done:** Current official README/license wording inspected; data not bundled

**Rights/access:** Data/documentation CC BY-NC-SA 4.0 with additional professional-sports/financial-firm exclusion; code MIT

**Release scope and storage:** 411 pitching trials/100 athletes; 677 swing trials/98 athletes; 1,934 assessments/1,162 athletes; approximately 1.1 GB large release compressed

**Units and annotations:** Per-column dictionaries; marker signals 360 Hz and force plates 1,080 Hz; POI units vary

**First experiment:** Validated ID joins and conventional biomechanics before topological descriptors

**Split design:** Athlete/session; session_pitch or session_swing joins; no unsupported cross-module person linkage

**Evaluation:** Signal reconstruction or target-specific held-out errors; not injury prediction without injury labels

**Failure modes:** Current download path differs from old clones. Additional license restriction is material; no commercial/pro-team permission is granted here.

Primary source: https://github.com/drivelineresearch/openbiomechanics

## BASKET-Multiview

**Date:** Current official dataset page inspected 2026-09-21; release date not asserted

**Sport:** Basketball

**Evidence:** SYNTHETIC Unreal Engine scenes

**What was actually done:** Official description inspected; render payload not downloaded

**Rights/access:** Inspect dataset license and any SMPL/asset restrictions separately

**Release scope and storage:** 1080p/4K renders at 30 fps; choose bounded scene/camera subset

**Units and annotations:** Simulator camera parameters, depth, segmentation, normals and meshes; verify coordinate conventions

**First experiment:** Known-camera triangulation and reconstruction checks

**Split design:** Scene/play/actor/camera, not adjacent rendered frames

**Evaluation:** Errors against simulator truth plus separate real-data transfer evaluation

**Failure modes:** Excellent known-answer controls do not validate real-world camera calibration or athlete dynamics.

Primary source: https://humansensinglab.github.io/basket-multiview/data.html

## A bounded acquisition checklist

Read the actual release/card/license and choose one dataset version. Record the
SHA/DOI, collection dates, byte sizes, checksums and expected file schema. Estimate
storage before accepting full archives; body-pose JSON and video can be gigabytes.
Use a separate environment for third-party models and review their scripts before
execution. Never paste credentials into a notebook or bundle them in this archive.
Validate one small file, then IDs, clocks and units, then one sequence. Detect Git
LFS pointer text before parsing it as data. Quarantine a mismatch; do not silently
refresh the reference hash to make verification pass.

For full sports data, keep match/athlete/session/video identities through every
transformation. Preserve source/derived status and availability timestamps. Record
selection and exclusion counts. Pin full-source training/validation/test manifests
before tuning. Display uncertainty and rejected frames rather than implying every
model output is measured truth. The current sports examples intentionally do not
report predictive accuracy from one basketball trial or twelve soccer profiles.
