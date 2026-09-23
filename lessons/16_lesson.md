# Stage 16 — Attention and VGGT, from pixels to proposed geometry

Understand the network idea without confusing a toy attention lab with trained inference.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 14, Stage 15.

## 1. Why a geometry model is an extension, not the foundation
The previous stages showed how calibrated projections constrain a scene. A learned model also uses patterns acquired from training data. Those patterns can produce a useful hypothesis when direct geometric evidence is incomplete. They do not turn an ambiguous observation into a guaranteed measurement.

Keep three layers separate: what a camera observed, what a mathematical model permits, and what a trained network predicts. Our small attention experiment teaches a computation. The optional VGGT runner performs a separate model experiment only after you supply an appropriate checkpoint and environment.

## 2. Tokens are pieces of an image represented as vectors
An RGB image is a height-by-width array with three channels. Divide it into patches; flatten each patch or map it through a learned feature extractor to obtain a token vector. A token is not a word here. Its source location and image identity must remain traceable.

Suppose there are N tokens of dimension d. Place them in a matrix X. Learnable linear maps can form queries Q, keys K and values V. The scaled dot-product attention calculation is

```text
scores  = Q Kᵀ / sqrt(d)
weights = softmax(scores, row by row)
output  = weights V.
```

A query asks which other representations should contribute. A key supplies information for the comparison. A value supplies the content being mixed. These descriptions are teaching analogies for matrix operations, not evidence that the model reasons in human sentences.

## 3. Work a tiny softmax example
For scores [0,log 3], exponentiation produces [1,3], and normalization gives weights [1/4,3/4]. If the values are [2,10], the weighted output is 8. Subtracting the same constant from all row scores leaves softmax unchanged; subtracting the maximum helps prevent overflow.

A mask restricts which keys a query may use. A row with no allowed keys is invalid in our implementation. A masked attention calculation can mix representations, but it does not by itself triangulate a point, establish a correspondence, or prove causality.

## 4. Frame attention versus global attention
Frame-wise self-attention allows tokens to mix only within the same input image. Global self-attention allows mixing across the entire image collection. The original VGGT alternates these two forms, with image features, camera tokens, and prediction heads for camera and dense outputs. This is cross-view information exchange implemented with self-attention; it is not an architectural claim that the paper uses separate cross-attention blocks. [V01, V02]

In the notebook, real motorcycle-image patches become tokens. We compare the two masks and inspect row sums and prohibited weights. The features are deliberately simple and untrained. An attention image from this toy is not a VGGT attention visualization, a depth map, or proof of a matched physical object.

## 5. Read the actual model output contract
The original repository documents image tensors as `[S,3,H,W]` or `[B,S,3,H,W]`. Its returned arrays include a camera encoding, depth, confidence, and world-point maps. When query points are provided, the tracking output has shape `[B,S,N,2]`: those are 2D pixel correspondences. [V03]

A **depth map** gives a scalar per pixel under its depth convention. A **point map** gives a 3D coordinate per pixel in a chosen frame. A **track** links an identity across images or times. Turning corresponding pixels and depths into a metric 3D trajectory requires consistent frames, scale, timestamped evidence, and an appropriate dynamic-scene model.

The original paper uses the first camera as its reference and normalized scene scale, assumes a centred principal point, and describes limitations for fisheye/panoramic input and substantial non-rigid deformation. These qualifications are central to a sports application. [V02]

## 6. Use an opt-in runner, not an implicit model download
The package includes `optional/run_vggt_local.py` for the original model API. It requires an existing repository, an exact expected commit, a local checkpoint, a licence-review acknowledgement, and an ordered list of image paths. It records input hashes, checkpoint hash, code revision, processed-image dimensions, timing, and GPU memory. It does not download weights, accept access terms for you, or claim this environment ran inference.

The original repository distinguishes the original non-commercial checkpoint from a separately released commercial-use checkpoint. A code repository's name does not settle the permissions of every weight file. Record the actual checkpoint and applicable terms. [V04]

The runner is not an Omega adapter. Different model generations can have different packages, outputs and preprocessing. Silent substitution would make comparisons uninterpretable.

## 7. What the Omega source update teaches
The supplied source highlights VGGT-Ω. Independent checking found a date discrepancy: the project page labels its training/checkpoint notice September 18, 2026, while the official README labels the corresponding notice September 8. We retain both statements rather than invent a corrected release date. The README identifies a 416-resolution reproduction checkpoint for benchmark comparisons and distinguishes it from other checkpoints. [V05, V06]

Omega's compact register-based exchange is a worthwhile later reading. Training-memory claims and inference-memory measurements are different quantities. Neither is a benchmark on your own GPU unless measured there. [V05, V06]

## 8. What you should be able to say
“Here is the tensor contract. Here is the reference frame. Here is what was learned rather than measured. Here is the preprocessing. Here is the checkpoint. Here are the failure cases. Here is what has actually run.” That description is more useful than “the model understands 3D” when you need accurate measurements.

## Independent conceptual exercises

1. Calculate softmax([0, log 3]) and its weighted average of [2,10].
2. Distinguish frame-wise and global self-attention and describe the mask.
3. Why is the toy patch experiment not a VGGT reconstruction?
4. What does a track tensor ending in dimension two represent?
5. Why do normalized scene coordinates not establish metre accuracy?
6. How should the conflicting Omega update dates be recorded?

## Mastery gate

Explain attention by hand and complete a model-output/source audit before attempting inference.

Readings: V01, V02, V03, V04, V05, V06. See the [source ledger](../docs/SOURCES_V3.md) for checked links, evidence status and source differences.
