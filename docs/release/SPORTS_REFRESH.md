# Sports-source verification scope — 22 September 2026

This release repairs course execution and evidence collection. It does not silently replace a selected excerpt with a full modern dataset, remove its terms, or turn a metadata exercise into a tracking benchmark.

## Sources rechecked for this delivery

**SPL Open Data.** The official repository's March 2026 summary describes 583 free-throw trials, five participants and two sessions, with CC BY-NC-SA 4.0 terms. These provider-wide counts are not the size of our bundled selected excerpt. The existing source-specific card remains authoritative for selected frame identities, feet/inches conventions, acquisition/transcription and its limitations. Source: https://github.com/Sport-Performance-Lab/SPL-Open-Data .

**SkillCorner basketball.** The official repository describes ten ACB 2025–26 sample games with tracking/events and separate offense-only season aggregates over 293 of 327 games. The tracking is 25 fps in feet and distinguishes detected from extrapolated positions. The retained ACB exercise uses the ten-game metadata table and identity conventions, not newly acquired tracking. Its source-file identity evidence does not independently certify sporting outcomes or metric accuracy. Source: https://github.com/SkillCorner/opendata-basketball .

Full tracking payloads, derived events and season aggregates answer different questions. Ten game files cannot reproduce a 293-game aggregate. Athlete aliases, total rows, frame clocks, visibility flags and selection limits remain part of the existing lessons. Follow the provider's current primer, data dictionary, known issues and artifact-specific terms before use.

## Current catalogue versus historical source checks

The larger sports catalogue is retained as a dated acquisition guide, including multiview video, wearables, pose, tracking and baseball biomechanics. Only sources explicitly named above were freshly rechecked for this small release audit. Do not label every catalogue entry newly verified. No optional dataset was downloaded or benchmarked during this build. Old source dates, transcription cautions and restricted-use terms remain visible.

## Choose by the experiment, not merely recency

For learning identifiers, units and leakage, start with the bundled small cases. For full athlete generalization, acquire sufficiently varied trials with participant/session identities. For calibration, choose measured geometry and independent holdouts. For event detection, require event annotations and a temporal split. For image representation, preserve what labels were and were not used. Newness alone does not determine suitability or measurement quality.

Before expanding data, write the question, observation unit, source revision, rights, byte hash, schema, units, identity mapping, inclusion rules, missingness policy, baseline, split, metric, uncertainty procedure and failure examples. Keep raw observations, model outputs, extrapolations and manufactured controls distinguishable. A source checksum cannot prove the physical truth of an observation.

Related canonical routes: [dataset index](DATA_AND_SPORTS.md), [applications](../../curriculum/APPLICATIONS.md), [sports catalogue](../v8/SPORTS_DATASETS.md). No new duplicated dataset lessons are added here.
