# Sports update and acquisition boundary — 21 September 2026

## The added basketball source
SkillCorner's basketball open-data repository now provides three distinct products for Liga ACB 2025–2026: a ten-game tracking sample, model-derived events for those games, and offensive aggregates covering 293 of 327 games. The repository's README and primer identify the coverage and conventions. This course adds the complete ten-game **metadata catalog**, not those larger performance payloads.

Primary sources:
- Repository: https://github.com/SkillCorner/opendata-basketball
- Overview: https://github.com/SkillCorner/opendata-basketball/blob/main/README.md
- Primer: https://github.com/SkillCorner/opendata-basketball/blob/main/docs/PRIMER.md
- Known issues: https://github.com/SkillCorner/opendata-basketball/blob/main/docs/KNOWN_ISSUES.md
- License: https://github.com/SkillCorner/opendata-basketball/blob/main/LICENSE

The checked source revision for the metadata is a Git **blob**, not a guessed commit: `6db83d7fa75a699270630c02efc330ce8a8d2e2b`. The connector returned the full text and blob identifier. The serialized included file produces that same Git object hash; SHA-256 is recorded too. That is an exact file-identity check against the returned source identifier, not a second independent download or independent verification of the final scores.

Read [the data card](../../sports_v9/DATA_CARD.md), then [the lesson](../../sports_v9/lesson.md). Execute it with:

```bash
python scripts/course.py run --acb --output my_work/acb_readiness_01
```

The notebook keeps real game metadata distinct from constructed alias and duplicate-total examples. The chronological 6/2/2 split is an exercise, not a trained sporting outcome model. Teams can recur in different partitions, and this small selection is not a representative sample of all basketball.

## Why this is useful before downloading motion data
The actual tracking schema uses feet and video-time clocks; players currently have ground-level z values. Do not use that field as measured jump height. Model-derived events need their own validation rather than being promoted automatically to human ground truth. Consult the provider's detected/extrapolated flags and quality fields before selecting measurements.

The provider identifies duplicate athlete IDs and player-team-season rows that include additional season-total rows. Normalize only documented ID aliases. Choose the row grain before aggregating; do not add team rows to a total row representing the same events. The provider also reports event-field exceptions, so similar column names are not a substitute for reading the dictionary.

## Continue through an explicit acquisition gate
Before bringing in the full tracking files: review the current license; choose one game; verify Git LFS pointers are replaced by the actual compressed payload; preserve the source revision and a file hash; read the field dictionary; validate timestamps, units and detection flags; and declare the observation/split unit. Only then create downstream arrays. The repository describes roughly 30–46 MB per compressed tracking game; this is provider-reported size, not a local performance benchmark.

Acquire an independent labeled or measured reference before claiming event accuracy or metric reconstruction accuracy. A dataset can be useful for descriptive learning without meeting that stronger validation standard.

## Earlier sports sources remain available, with their boundaries
The v8 sports guide still contains SPL free throws, SkillCorner soccer, BasketHAR, MUVS, UVY, TrackID3x3, OpenBiomechanics, SoccerTrack v2, SoccerNet and BASKET-Multiview plans. They cover different modalities; none is a universal “best dataset.” Use pose for kinematics, tracking for spacing, synchronized cameras for reconstruction, and separate annotations for event evaluation.

The included SPL and soccer data remain small selected excerpts with their previously documented transcription limitations. Other linked payloads were not downloaded in this release. BASKET-Multiview is a synthetic-data route. A public repository or permissive code license does not establish unrestricted rights to its videos, weights or athlete data. Review the exact artifact terms before any use beyond this learning course.

See [the retained sports source guide](../v8/SPORTS_DATASETS.md) for the dated per-source plans and [the application index](../../curriculum/APPLICATIONS.md) for non-sports datasets. All sources continue to carry their own provenance, units, use conditions and evaluation limits.
