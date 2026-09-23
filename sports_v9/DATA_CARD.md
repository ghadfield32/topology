# SkillCorner ACB sample match catalog

**Provider:** SkillCorner. **Snapshot reviewed:** September 21, 2026. **Season:** 2025–2026. **Observation unit:** one published sample game. **Rows:** 10. **Use in this course:** metadata validation and chronological grouping, not predictive modeling.

## Authoritative links
- [Repository and scope](https://github.com/SkillCorner/opendata-basketball)
- [Exact source path](https://github.com/SkillCorner/opendata-basketball/blob/main/data/matches.json)
- [Current primer: grain, coordinates, clocks](https://github.com/SkillCorner/opendata-basketball/blob/main/docs/PRIMER.md)
- [Known issues](https://github.com/SkillCorner/opendata-basketball/blob/main/docs/KNOWN_ISSUES.md)
- [Repository MIT license](https://github.com/SkillCorner/opendata-basketball/blob/main/LICENSE)

The source path is mutable. The acquired file is identified by the Git blob SHA-1 and SHA-256 in `data/provenance.json`, not by assuming `main` never changes. Exact text reconstruction matched the connector-returned Git hash. Full tracking, events, aggregate CSVs and alias tables were not acquired. Raw data downloads remain optional and require their own complete manifest.

## Fields
| Field | Meaning | Availability or limit |
|---|---|---|
| `id` | Provider game identifier | Not a temporal ordering key. |
| `date_time` | Scheduled tip-off, UTC | Not actual first frame arrival. |
| `home_team`, `away_team` | Provider IDs and names | Team identity may recur across splits. |
| `home_score`, `away_score` | Recorded final integer points | Outcomes, unavailable before the game finishes. |
| `competition_id`, `competition_edition_id`, `season_id` | Provider catalog IDs | Not measurements or ordered covariates. |
| `season` | Season label | Does not imply full coverage. |
| `status` | Provider record status | All selected records are closed. |

## Rights and scope
Copyright (c) 2026 SkillCorner. The repository includes an MIT license, reproduced in `data/LICENSE_SKILLCORNER.txt`. This metadata lesson credits SkillCorner. Check the current terms of each future payload rather than inferring rights from another dataset's license. The older SPL excerpt has separate noncommercial/share-alike terms.

## Split protocol
Sort aware UTC timestamps; use six fit, two validation, two test games. Repeated games, ties at a split boundary, invalid timestamps and modified source bytes are rejected by the relevant checks. The ten-game sample is deliberately small and nonrandom. No model is trained here; this is not season-wide or unseen-team validation. Final scores must not become pregame features.

## How this expands the existing catalogue
For activity recognition and wearables, retain the BasketHAR plan. For multiview footage, retain MUVS. For tracking evaluation, retain UVY/TrackID3x3/SoccerNet. For baseball biomechanics, retain OpenBiomechanics and its special rights restrictions. No one product substitutes for the others: select data by the observation needed to test your claim, not by the newest release date.
