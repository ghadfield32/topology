# Stage 19 conceptual solutions

Attempt the lesson questions first. These are answer criteria, not scores assigned to your work.

## 1. Why is a near-to-far transition not sufficient proof of release?

It does not establish prior contact/control, correct identities, or the mechanism of separation. Measurement error and noncontact motion can produce it.

## 2. For the supplied five samples, state onset and decision time.

The first far sample is .03 seconds and confirmation arrives at .04 seconds, so onset and decision differ by .01 seconds.

## 3. What should missing observations do in this conservative baseline?

They reset the armed/confirmation state; the code does not invent directly observed near/far evidence during the gap.

## 4. Describe a prefix test for causality and one upstream leakage failure.

Run each input prefix and compare decisions available by its endpoint. An offline smoothed feature can leak future observations even when the final detector iterates chronologically.

## 5. Calculate precision and recall for two predictions matched to one reference.

TP=1, FP=1, FN=0, giving precision .5 and recall 1 under the declared one-to-one matching.

## 6. What real event evidence is missing from the bundled stereo data?

There are no labelled athletes, hand/ball identities, event boundaries, motion trajectories, or capture timing for basketball interactions. Real sports precision/recall cannot be calculated from it.
