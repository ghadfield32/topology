# ACB readiness lab — what a modern sports dataset actually contains

## Begin with the question, not the algorithm
Imagine you receive three folders: game metadata, tracking frames and season aggregates. They describe the same competition, but they do not contain the same observations. A row in a match catalog is one game. A tracking line is one frame. A player-team-season row summarizes many events. Treating all of these as interchangeable can create double counting and misleading evaluation before a neural network is involved.

This lab adds the complete **ten-game metadata catalog** from SkillCorner's ACB 2025–2026 sample release. It is real provider metadata. It does not include those games' tracking streams or event files. The older course's SPL and soccer excerpts remain separate, with their existing acquisition limitations.

## Exact source evidence
The official GitHub connector returned the complete JSON plus blob ID `6db83d7fa75a699270630c02efc330ce8a8d2e2b`. The included UTF-8 bytes were reconstructed from that text and match the Git blob hash exactly. This closes the transcription-integrity check for this specific file. It is not an independent second retrieval, nor verification of the historical game scores against another organization.

See [the data card](DATA_CARD.md) for source and license information. The loader checks both the Git blob ID and the local SHA-256 before parsing.

## 1. Learn an observation unit
The match with ID 114243 has a final home score of 83 and away score of 68. Its final margin is 83 − 68 = 15 points. That is an observed outcome recorded by the provider, not an input that would have been available before tip-off.

The catalog has ten rows, not 293 games, not 327 games and not millions of independent frames. The broader provider documentation describes 293 covered games in the season aggregates and ten sample games with raw files. A sample catalog does not become a full-season dataset because the season label is shared.

**Your check:** count distinct game IDs, seasons, and teams separately. Say which count answers your question. A team can appear in more than one game without creating a duplicate game.

## 2. Time has a role
The metadata's scheduled tip-off is an aware UTC timestamp. It is not a tracking-frame timestamp. A future frame time is not interchangeable with a countdown game clock, which can stop at whistles. Keep scheduled time, elapsed video time, frame index and period/game clock in different fields.

We sort the ten games chronologically and assign six to fitting, two to validation, and two to testing. This demonstrates a game-level split. It does not establish unseen-team evaluation because teams may recur. There are too few selected games for a credible general sports benchmark; do not use a fitted accuracy number to conceal that limitation.

**Hand calculation:** 6 + 2 + 2 = 10. Intersection of any two game-ID sets must be empty. Changing row order must not change the assignment.

## 3. Avoid counting a traded player twice
The provider documents both team rows and a `team_name = total` row for some players. Suppose an invented example has 10 attempts on team A, 5 on team B, and 15 in its total row. Adding all three yields 30; choosing only team rows yields 15. The example is deliberately constructed and is not a claim about any real athlete.

The sum operation applies to additive counts. Do not sum shooting percentages, speeds or per-game averages as if they were counts. To combine a rate, first identify its numerator, denominator and coverage.

A provider alias table may map multiple IDs to a canonical athlete. We resolve explicit mappings and reject cycles. We do not merge athletes merely because their names look similar.

## 4. Tracking is not automatically physical ground truth
The current primer states that player z coordinates are fixed at zero, whereas ball z is positive. Therefore this product does not independently measure player jump height. Detector flags and uncertainty-like fields need their documented meanings; a model's error estimate is not independent calibration truth.

Do not infer airborne metric position from a ground homography. To validate camera geometry, use the earlier camera and holdout lessons. To evaluate motion, obtain the actual tracking payload, determine units and timing, preserve missingness and estimated observations, and compare with independent labels or measurements.

## 5. Source claims versus our experiments
The supplied learning posts discuss manifolds, mechanics and architectural structure. This lab does not validate their broad claims by counting games. It teaches the data contract needed before attempting those applications. The [claims map](../docs/v9/CLAIMS_AND_LIMITS.md) points to the specific existing calculations that test narrower mathematical statements.

## Independent work
**A1.** Write a function that counts unique games without treating each opponent as a new observation.

**A2.** Recreate the chronological game assignment. Explain which predictions could be legitimately evaluated and which population remains untested.

**A3.** Implement an alias-chain resolver. Give an example where two mappings form a cycle and explain why the loader should stop.

**A4.** Implement the additive team-row total. Explain why this function must not be reused to sum percentages.

**A5.** Write a pre-acquisition protocol for the full tracking files: required source revision, rights review, bounded download size, compressed-file integrity, IDs, coordinate frame, units, clocks, missingness, split unit, baseline and independent acceptance measurement.

Attempt [the learner notebook](practice/acb_readiness.ipynb) before opening [the reference answers](solutions/acb_readiness.ipynb).

## Completion gate
You can distinguish games, frames, athletes, events and aggregates; keep outcomes out of earlier-time inputs; show a split without shared games; and identify a question that this metadata cannot answer. Passing the code checks is evidence of implementation, not mastery or basketball-model validity.
