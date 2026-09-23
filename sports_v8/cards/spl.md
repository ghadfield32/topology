# Data card: selected SPL free-throw frames

**Status:** observed-source, markerless motion-capture estimates; manually transcribed
numeric excerpt. Not a full release or independently measured ground truth.

**Provider:** Maple Leaf Sports & Entertainment Sport Performance Lab.
**Source documentation checked:** 2026-09-21; documentation labels its update March 2026.
**Collection:** 2025-12-18 session; selected P0001/T0001. The provider describes
458 trials across 5 participants at 60 fps in this session, plus the older
2024-08-28 session at 30 fps. We bundle only one trial excerpt.

**Included:** 12 selected frames [0,1,90,110,115,120,125,130,135,140,180,210];
ball centre, right shoulder, right elbow and right wrist xyz. A 12x3 array for
each landmark. The source trial has other frames and landmarks not included.
Selected columns preserve displayed numeric values without deliberate rounding.
`source_time` retains the original `time` value. Calculation time is original
frame ID / 60, an ideal clock assumption rather than audited camera PTS.

| Field | Meaning / unit | Learning constraint |
|---|---|---|
| session, participant_id, trial_id | identity keys | one independent shot, one athlete |
| frame | source frame index | retained spacing is nonuniform |
| source_time | raw source clock value | retained, not silently treated as exposure time |
| ball/right shoulder/elbow/wrist | xyz in feet; court-centre frame | markerless estimates; no per-frame accuracy supplied here |
| landing_x/landing_y | hoop-local outcome, inches | different origin; future information for pre-release tasks |
| entry_angle_deg | final angle, degrees | future outcome-related information |
| result | made for this selected shot | not a frame-level sample of 12 independent outcomes |

**Selection:** manual convenience selection to inspect pre-motion, a short candidate
flight window, and later uncertain ball values. It was not random, outcome-balanced
or preregistered. Frames 110–130 fit the example; 135/140 are later points of the
same selected shot, not an independent athlete test. No release label is inferred.

**Missingness:** unselected frames are unavailable in the excerpt, not proof of
sensor dropout in the source. The provider warns about noisy ball coordinates at
capture-volume entry/exit. Identity, tracking accuracy, contact and release are
not independently validated by this course. Never fill unavailable observations
and then label the filled values measured.

**Rights:** CC BY-NC-SA 4.0. The selected/reformatted excerpt and SPL-data-derived
figures are shared with attribution under those terms. Keep them separate from
commercial training or products unless appropriate additional rights are obtained.
The code license does not override data terms. See `../data/LICENSE_SPL.md`.

**Integrity:** the manifest records the full source Git blob
`7ca18fac37806137fd3cd559f5c0ecd8339db5aa`, expected byte length, local SHA256 and
selection rule. Network download into the build container failed. Local hashes
and hand spot-checks are not remote equality. The optional verifier must compare
full original bytes and selected numbers before independent source verification
can be claimed. Unknowns remain recorded rather than guessed.

**Sources:**
- https://github.com/Sport-Performance-Lab/SPL-Open-Data
- https://github.com/Sport-Performance-Lab/SPL-Open-Data/blob/main/basketball/freethrow/README.md
- https://raw.githubusercontent.com/Sport-Performance-Lab/SPL-Open-Data/main/basketball/freethrow/data/2025-12-18/P0001/BB_FT_P0001_T0001.json
