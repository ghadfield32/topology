# Stage 19 beginner workbook

## Trace the state machine by hand
Write the sequence [.01,.01,.01,.20,.25] metres at 10-millisecond intervals. With three near observations and two far observations, identify the armed state, candidate onset and decision time. Then set the fourth visibility flag to false and repeat. Explain the conservative reset.

## Avoid a false success
Two predicted onsets at .10 and .11 seconds cannot both match one reference onset at .10 under a .02-second tolerance. The matched count is one, not two. Calculate precision and recall explicitly.

## Real-data boundary
Select two rows from the real cloud and compute their distance. That distance concerns scene points, not contact between a hand and an object. Write the observation identity before using any physical label. This exercise trains semantic discipline with real geometry rather than pretending the static scene contains motion labels.

## Deep route
Design a schema with source frame IDs, entity IDs, onset interval, decision time, visibility, direct/inferred status, calibration ID and evidence cutoff. Specify event-level splits by session and athlete. Separate offline retrospective analysis from live past-only detection and define which hard negatives would falsify a useful model claim.

## Three passes

**Understand:** work the hand example and identify an assumption. **Build:** run the worked lab, predict a change, and implement the coding exercises. **Demonstrate:** answer unfamiliar questions without the solutions and return for delayed recall. Passing reference code does not assess your understanding.
