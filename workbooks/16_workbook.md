# Stage 16 beginner workbook

## Tiny hand calculation
Write a two-query, two-key score matrix. Apply softmax by row. Confirm that each row sums to one and that a forbidden entry has weight zero. Then multiply by two simple values. Keep track of every matrix shape.

## The real-image toy
The two input photographs are real. Patch extraction and attention are deterministic computations. The experiment has no trained weights and no 3D supervision. Label all three facts in your notebook. Change from frame-only to global attention and explain what new information exchange becomes possible, without claiming that this proves correct geometry.

## Before GPU inference
Prepare a manifest with image hashes, order, scene identifier, camera information, timestamps where available, checkpoint hash, exact repository commit, and preprocessing description. Keep the first static-scene run small. Compare predictions to references using disjoint registration and evaluation anchors, not the first attractive visualization.

## Deep route
Derive the computational difference between S independent P×P attention matrices and one SP×SP matrix, holding feature dimension fixed. This is a dense-score complexity calculation, not an actual device-memory forecast; fused kernels, layer counts, heads and retained activations change realized memory. Read the Omega register design only after you can explain this distinction.

## Three passes

**Understand:** work the hand example and identify an assumption. **Build:** run the worked lab, predict a change, and implement the coding exercises. **Demonstrate:** answer unfamiliar questions without the solutions and return for delayed recall. Passing reference code does not assess your understanding.
