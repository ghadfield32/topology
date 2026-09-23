# Geometry delayed recall

24 questions for Stages 13–20. Attempt after a delay without the corresponding lesson open. The original 39 questions remain in `retrieval.md`.

## 13.R1

Explain why one normalized direction cannot recover the original 3D point.

<details><summary>Answer criteria — open after attempting</summary>

All positive multiples of a point yield the same direction. Range was discarded.

</details>

## 13.R2

Derive p·v=0 for a curve on a unit sphere.

<details><summary>Answer criteria — open after attempting</summary>

Differentiate p(t)·p(t)=1, obtaining 2p·p′=0.

</details>

## 13.R3

What fails at the excluded stereographic pole?

<details><summary>Answer criteria — open after attempting</summary>

The chosen chart denominator vanishes; the space itself remains well-defined and another chart works.

</details>

## 14.R1

Why is -t generally not the camera center for Xc=RXw+t?

<details><summary>Answer criteria — open after attempting</summary>

Set Xc=0 and solve C=-Rᵀt.

</details>

## 14.R2

What makes a reflection different from a proper rotation?

<details><summary>Answer criteria — open after attempting</summary>

Both may be orthogonal, but a reflection has determinant -1, not +1.

</details>

## 14.R3

Name three things pixel coordinates alone do not encode.

<details><summary>Answer criteria — open after attempting</summary>

Camera-axis depth, physical scale, and the raw-to-processed pixel mapping or camera calibration; acceptable alternatives must be explained.

</details>

## 15.R1

Derive the sign of doffs in rectified disparity.

<details><summary>Answer criteria — open after attempting</summary>

d=uL-uR=fB/Z+cxL-cxR=fB/Z-doffs, so Z=fB/(d+doffs).

</details>

## 15.R2

Why report both median and mean disparity error?

<details><summary>Answer criteria — open after attempting</summary>

The median reflects a typical magnitude; a heavy error tail may make the mean much larger. Neither replaces coverage.

</details>

## 15.R3

How can asynchronous horizontal motion pass an epipolar check?

<details><summary>Answer criteria — open after attempting</summary>

The same image row may be preserved while the differing-time horizontal position alters disparity and inferred depth.

</details>

## 16.R1

What did the toy attention experiment verify?

<details><summary>Answer criteria — open after attempting</summary>

Within-frame masking and subsequent cross-frame information flow on real patches, not learned reconstruction.

</details>

## 16.R2

What additional evidence turns an image track into a metric 3D trajectory?

<details><summary>Answer criteria — open after attempting</summary>

Valid depth or triangulation, coordinate/frame/scale registration, timing, identity, visibility and independent validation.

</details>

## 16.R3

Why must original VGGT and Omega not share an assumed interface?

<details><summary>Answer criteria — open after attempting</summary>

They have different architectures, code paths, checkpoints and APIs; read and pin each exact implementation.

</details>

## 17.R1

What does a tiny anchor residual fail to establish?

<details><summary>Answer criteria — open after attempting</summary>

Correctness away from fitted anchors, metric accuracy on independent landmarks, or generalization to new scenes.

</details>

## 17.R2

Why does a factor-of-two cloud scale move persistence coordinates?

<details><summary>Answer criteria — open after attempting</summary>

Rips birth/death thresholds are distances; uniform scale multiplies pairwise distances and filtration coordinates.

</details>

## 17.R3

Why is a TDA shape summary not a calibration certificate?

<details><summary>Answer criteria — open after attempting</summary>

It loses information and may be invariant to changes such as rigid pose or insensitive to particular geometric errors.

</details>

## 18.R1

What does synchronized GPU timing measure that an unsynchronized host timer may miss?

<details><summary>Answer criteria — open after attempting</summary>

Completion of queued device work at the declared boundaries rather than launch submission time alone.

</details>

## 18.R2

What happens when average single-worker service time exceeds frame interarrival time?

<details><summary>Answer criteria — open after attempting</summary>

In an indefinitely continuing lossless FIFO setting, backlog and age grow rather than reaching a stable finite queue.

</details>

## 18.R3

Why is a point-cloud message not always a packed Nx3 float array?

<details><summary>Answer criteria — open after attempting</summary>

Field types, offsets, padding, row stride and endianness can vary and must be respected.

</details>

## 19.R1

Distinguish event onset and decision availability.

<details><summary>Answer criteria — open after attempting</summary>

Onset is the estimated event time; a causal decision becomes available only after enough supporting observations arrive.

</details>

## 19.R2

Why reset evidence across an occlusion?

<details><summary>Answer criteria — open after attempting</summary>

Missing observations cannot be silently used as direct support; any continued hypothesis needs an explicit prediction/uncertainty policy.

</details>

## 19.R3

Why is a passing proximity-and-motion test not proof of contact?

<details><summary>Answer criteria — open after attempting</summary>

Objects can approach and separate without touching; contact needs independent evidence and appropriate labels.

</details>

## 20.R1

What survives a course upgrade?

<details><summary>Answer criteria — open after attempting</summary>

Learner answers, notebooks, source data, attempt history, evidence paths/hashes and explicit unresolved gaps—not automatic new-stage passes.

</details>

## 20.R2

What information must accompany a model-derived cloud?

<details><summary>Answer criteria — open after attempting</summary>

Input/source IDs and hashes, preprocessing, exact checkpoint/code revision, units and frame, confidence semantics, timestamp policy and validation status.

</details>

## 20.R3

What distinguishes a reproduced demonstration from an independent project?

<details><summary>Answer criteria — open after attempting</summary>

The independent question, parameter choices and suitable held-out evidence were not taken from the already exposed worked answers.

</details>