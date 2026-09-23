# Stage 16 conceptual solutions

Attempt the lesson questions first. These are answer criteria, not scores assigned to your work.

## 1. Calculate softmax([0, log 3]) and its weighted average of [2,10].

The weights are (1/4,3/4), giving 2/4+30/4=8.

## 2. Distinguish frame-wise and global self-attention and describe the mask.

Frame attention permits a key only when query and key have the same image ID; global attention permits cross-image keys. Both are self-attention in the cited original architecture.

## 3. Why is the toy patch experiment not a VGGT reconstruction?

It uses simple untrained patch vectors and has no learned geometry heads or pretrained weights. Real photographs do not change the algorithm into a trained geometry model.

## 4. What does a track tensor ending in dimension two represent?

It is a pair of 2D pixel coordinates per point and view, not a metric 3D position.

## 5. Why do normalized scene coordinates not establish metre accuracy?

Normalizing coordinates fixes a numerical gauge; it does not introduce a physically measured length. Independent scale references are still needed for metric claims.

## 6. How should the conflicting Omega update dates be recorded?

Preserve September 18 on the project page and September 8 on the README as source-specific statements, note the discrepancy, and record the actual checkpoint identity rather than asserting a reconciled date.
