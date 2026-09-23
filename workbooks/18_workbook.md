# Stage 18 beginner workbook

## Timing by hand
For arrivals [0,.01,.02] seconds and three .02-second service times, completions are [.02,.04,.06]. Latencies are [.02,.03,.04]. The service duration is unchanged while the delivered result becomes older. Explain why a function-only benchmark misses that growth.

## Real-cloud optimization
Use the same fixed cloud, rotation, translation and dtype in both implementations. Record maximum absolute coordinate difference before timing. Run a warm-up and repeated measurements. Include the number of points and environment in the result. Do not transfer the measured speed ratio to another machine as a fact.

## Debugging challenge
Change only one implementation from metres to millimetres. It may still run faster, but it no longer performs the same calculation. A semantic test should fail before a timing claim is accepted.

## Deep route
Design an end-to-end trace schema for your own capture path. Define precisely which clocks produce each timestamp and which clock transformations are required. State which omissions prevent a genuine capture-to-display latency claim. Then compare FIFO and latest-frame policies on a labelled event sequence, accounting for dropped evidence.

## Three passes

**Understand:** work the hand example and identify an assumption. **Build:** run the worked lab, predict a change, and implement the coding exercises. **Demonstrate:** answer unfamiliar questions without the solutions and return for delayed recall. Passing reference code does not assess your understanding.
