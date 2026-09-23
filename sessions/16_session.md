# Stage 16 guided session — Attention moves information; training gives it task meaning

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/16_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/16_lab.ipynb). The [original workbook](../workbooks/16_workbook.md) and [worked lab](../notebooks/16_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real stereo-image patches processed by an explicitly untrained attention operator; no VGGT predictions.

## What you will be able to demonstrate

1. Identify query, key, and value shapes in scaled dot-product attention.
2. Explain why each attention row sums to one.
3. Check a controlled attention calculation on patches from a real image.
4. Distinguish an attention example, a model-output contract, and actual trained VGGT inference.

## Read one attention row
Queries ask which inputs should contribute to an output. Keys provide values used in comparison. Values provide the information to combine. For Q with N rows, K with M rows, and matching feature width d, the score matrix `Q K.T / sqrt(d)` has shape N by M. Apply a row-wise softmax to turn each allowed score row into nonnegative weights summing to one. Multiply those weights by V to obtain N output rows.

The scaling and softmax define a computation. They do not establish that the scores represent physical correspondence or calibrated probability. Those interpretations need training, architecture choices, data, and independent evaluation.

## A hand-checkable special case
If one query is the zero vector and all keys are allowed, every score in that row is zero. Softmax assigns weight 1/M to each key. The output is therefore the arithmetic mean of the values. If every value row is the same vector c, any valid attention weights produce c. These cases test the implementation without requiring learned weights.

Subtracting a row's largest score before exponentiation changes neither the normalized weights nor their interpretation. It reduces overflow risk. A row with every key masked out has no defined probability distribution; the implementation rejects it rather than returning silent NaNs.

## Connect to the geometry model without impersonating it
VGGT's within-frame and across-frame attention motivates why information can move between views. Our notebook only flattens patches from a real stereo image and applies an untrained attention calculation. It does not use a trained image encoder, pretrained weights, positional embeddings, or geometry prediction heads. Real image input does not turn a toy attention operator into VGGT.

The optional runner belongs after the camera and validation foundations. Its outputs require shape, finiteness, coordinate, scale, preprocessing, and provenance checks. Passing those contracts does not establish reconstruction accuracy. A 2D track must not be relabeled as a measured 3D trajectory.

The v3 model-source discussion is preserved with its original review date. This revision adds teaching and arithmetic checks, not a new benchmark claim or a fresh verification of every later model release. Model weights and licenses must be checked for the exact artifact actually used. No trained VGGT execution is included in the shipped evidence.

## Predict, execute, and explain

### Step 1

Extract actual image patches; these are raw flattened pixels, not trained embeddings.

```python
from shape_lab.stereo import reference_sample
from shape_lab.attention import patch_tokens, attention
left, _, _, _ = reference_sample()
tokens, rc = patch_tokens(left[:32,:32], patch_size=8)
tokens = tokens/255.
print('patch tokens:', tokens.shape, 'locations:', rc.shape)
```

### Step 2

A zero query must average the values. Check this directly.

```python
query = np.zeros((1,tokens.shape[1]))
output, weights = attention(query, tokens, tokens)
assert np.allclose(weights, 1/len(tokens))
assert np.allclose(output[0], tokens.mean(axis=0))
print('attention weight sum:', weights.sum())
```

### Step 3

For arbitrary allowed weights, constant values must remain constant.

```python
Q = tokens[:3]; K = tokens
V = np.tile([2., -1., .5], (len(K),1))
out, w = attention(Q, K, V)
assert np.allclose(w.sum(axis=1), 1.)
assert np.allclose(out, [2., -1., .5])
result = {'real_image_patch_count': len(tokens), 'zero_query_mean_check': 'passed',
          'constant_value_check': 'passed', 'trained_embeddings_used': False,
          'VGGT_inference_executed': False}
```

## Transfer problems — attempt without the solution

### 16.T1

Why does a softmax row summing to one not make it a calibrated correspondence-confidence distribution?

<details><summary>Reveal reasoning after your attempt</summary>

Normalization is a mathematical property of the operator. Calibration concerns agreement between predicted probabilities and real outcomes under evaluation, which this untrained example does not establish.

</details>

### 16.T2

If every value is c, can attention produce a different vector under valid normalized weights?

<details><summary>Reveal reasoning after your attempt</summary>

No. The weighted sum is c times the sum of weights, hence c. An output differing from c would expose an implementation or numerical problem under the stated conditions.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/16_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
