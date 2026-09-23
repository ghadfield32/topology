# Data card: selected SkillCorner physical profiles

**Status:** observed-source, provider-derived season aggregate features; numeric
transcription of selected official CSV columns. Not raw GPS, full tracking,
per-player medical assessment or simultaneous pitch positions.

**Provider:** SkillCorner; open-data collaboration with PySport.
**Collection/aggregation period:** AUS A-League 2024/2025. **Checked:** 2026-09-21.
No exact release date for this CSV is asserted. The source has changed over time;
the recorded Git blob pins the version inspected rather than assuming `master`
will remain unchanged.

**Included:** first 12 data rows, 8 distinct player IDs, 12 selected columns
including added one-based `source_row`. Names and birthdates were not copied.
Numbers preserve the source's displayed precision. This is an ordered convenience
subset, not a representative league sample or held-out recruitment benchmark.

The README calls these player-season aggregates. The rows inspected additionally
separate player positions; preserve player/team/season/position and source row.
Repeated IDs matter for splitting. Never call twelve rows twelve independent
players or treat player_id as a numeric predictor.

| Column | Interpretation |
|---|---|
| source_row | added 1-based original data-row number, excluding header |
| player_id/team_id/season_id | categorical provider identifiers |
| position_group | provider position category |
| minutes_full_all | published minutes summary, NOT accumulated full-season minutes |
| count_match | qualifying match-performance count associated with the record |
| total_distance_full_all | published distance summary in metres, NOT a season total |
| total_metersperminute_full_all | provider metres/minute summary |
| running/hsr/sprint_distance_full_all | published distances in speed regimes |

The README says performances above 60 minutes are included. The current physical
glossary defines male speed bands for running 15–20 km/h, HSR 20–25 km/h, and
sprinting above 25 km/h. Those thresholds define categories; they do not make the
CSV a timestamped running-speed series. Exact aggregation weighting and deployment
version should be confirmed before interpreting sums or ratios as operational
performance metrics. Our lab uses published values descriptively and does not
invent a season-total interpretation. Rounded ratios need not match exactly.

**Study protocol:** choose three distance-category features. Inspect raw and
standardized descriptive Rips diagrams. Separately show player-disjoint partition
indices and training-only scaling. No supervised sports model is fitted or scored.
No diagram is labeled a tactical formation.

**Rights:** source repository carries the MIT license, copied to
`../data/LICENSE_SKILLCORNER.txt`. Credit SkillCorner/PySport. That does not by
itself license unrelated video or other providers' model weights.

**Integrity and acquisition:** manually transcribed official connector output;
Git blob `b80308d7662c8923dc82e0721e0b6f17df827d2e`. Full source equality was not
executed. Local SHA256 and the selection rule are in the manifest. The verifier
checks source revision and selected original columns against a full CSV.

**Not included:** match-level XY tracks, dynamic events, pose, or full season
aggregate tables. The XY adapter is only schema-tested with constructed fixtures.
The full tracking URL exposed a Git LFS pointer in this environment, not the
97,091,519-byte tracking payload.

**Sources:**
- https://github.com/SkillCorner/opendata
- https://raw.githubusercontent.com/SkillCorner/opendata/master/data/aggregates/aus1league_physicalaggregates_20242025.csv
- https://skillcorner.crunch.help/en/glossaries/physical-data-glossary
- https://raw.githubusercontent.com/SkillCorner/opendata/master/LICENSE
