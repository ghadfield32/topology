# Stage 19 — From geometry to cautious interaction hypotheses

Proximity is evidence to inspect—not proof of contact, possession or release.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 15, Stage 18.

## 1. A frame is not an event
An event describes change over time. “The ball is near the hand” is a relation at one moment. “The player released the ball” is an interpretation of a sequence, including control, separation and subsequent motion. A detector should not silently convert a relation into a stronger claim.

Begin with shared frames, units, identities and timestamps. A hand estimate from one player cannot be combined with a ball track from another time and treated as a valid interaction. Invisible or inferred observations need explicit status.

## 2. Build the smallest causal hypothesis
Our exercise uses a distance stream and visibility flags. After several observed near samples, the detector becomes armed. If several observed far samples then occur, it emits a `separation_candidate`. The name matters: it does not say “contact confirmed” or “release measured.” Missing evidence or an excessive time gap resets the state conservatively.

Two thresholds create hysteresis: the “near” threshold is smaller than the “far” threshold. An intermediate band avoids some threshold chatter. Minimum consecutive observations reduce isolated fluctuations but introduce confirmation delay. The threshold and count choices are demonstration settings, not validated basketball operating limits.

## 3. Onset is not decision time
If the first far observation is at .03 seconds and two far observations are required, the detector may make its decision at .04 seconds. Its reported candidate onset can be .03 while availability is .04. That is not time travel: the label is emitted later and refers to an earlier observed boundary.

A live metric must include the decision delay. Comparing this output to an offline sequence model that can inspect every future frame without disclosing the difference is not a fair live-performance comparison.

## 4. Test causality by changing the future
For each prefix of an input sequence, run the detector using only that prefix. Its emitted decisions should equal the subset of full-sequence decisions available by that prefix's last timestamp. This is a powerful test for accidental future access.

It is not enough for the code to be placed in a loop. Precomputed smoothed positions, globally normalized time-series features or future-filled gaps can already contain later evidence. The availability cutoff applies to upstream features as well.

## 5. What the real and simulated examples mean
The real stereo sample provides a static cloud. The lab uses distances between selected reconstructed scene points to show why proximity requires declared units and a compatible frame, while a common rigid frame change preserves distance. It contains no labelled hand–ball interactions. No real basketball-event precision or recall can be estimated from that dataset.

The event sequences are explicitly generated controls: near then far, near miss without a sustained near history, missing evidence near the transition, and a clock-gap case. They test software semantics under known conditions. They are not disguised captured trajectories, and they establish no production sports accuracy.

For genuine event evaluation, collect independent annotated sequences, including hard negatives: a hand passing near a ball without controlling it, brief occlusion, two players crossing, and track swaps. Record annotation uncertainty and disagreements instead of calling every boundary exact.

## 6. Match events one to one
Predicted and reference onsets should be matched under a stated tolerance, using each event at most once. Otherwise several predictions near one true event can all be counted as correct. Count true positives, false positives and false negatives, and state the matching rule. Precision is TP/(TP+FP); recall is TP/(TP+FN). With a zero denominator the corresponding rate is undefined, not automatically perfect.

Our small matcher chooses earliest feasible chronological pairs and maximizes the number of matches for sorted one-dimensional onsets with a fixed tolerance. It does not minimize timing error among all maximum-size matchings. Report its convention rather than hiding this distinction.

## 7. Extend evidence without overclaiming
A stronger basketball model might combine hand–ball distance, relative velocity, motion consistency, pose, visibility and identity continuity. Such features still need reliable measurements and annotation. No threshold alone certifies physical contact. A causal state estimator can preserve a hypothesis during short occlusion, but the output must remain inferred rather than directly observed.

The supplied human–object interaction account motivates this separation. It did not establish metric accuracy, event precision/recall, or a minimum reliable processing rate. Those remain experiments to conduct, not facts to fill in.

## Independent conceptual exercises

1. Why is a near-to-far transition not sufficient proof of release?
2. For the supplied five samples, state onset and decision time.
3. What should missing observations do in this conservative baseline?
4. Describe a prefix test for causality and one upstream leakage failure.
5. Calculate precision and recall for two predictions matched to one reference.
6. What real event evidence is missing from the bundled stereo data?

## Mastery gate

Demonstrate prefix invariance and explain why every emitted label remains a hypothesis.

Readings: U01, S01. See the [source ledger](../docs/SOURCES_V3.md) for checked links, evidence status and source differences.
