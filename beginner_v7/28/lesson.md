# Stage 28 — Functions to functions: DeepONet, Fourier operators and baselines

## Begin with one question

**How is learning an operator different from fitting one function?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Function: maps coordinates to values. Operator: maps functions to functions. Initial condition: a function specifying the starting field. Fourier mode: a sinusoidal basis component.

## Work the example before running it

For a periodic one-dimensional heat equation with diffusivity ν, an initial mode sin(kx) evolves as exp(-νk²t)sin(kx). Doubling k increases the decay exponent by four, not two. A neural operator attempts to learn a rule taking different input functions to their corresponding output functions.

Splitting spatial coordinates from one solution is not the same as testing unseen initial conditions. The retained DeepONet and Fourier-neural-operator labs use manufactured heat data with known solutions and function-level splits. Their small training results teach the machinery; they are not a universal ranking of architectures or evidence of multi-decadal climate accuracy.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/28/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
nu,t=.1,1.
a1=np.exp(-nu*t);a2=np.exp(-nu*4*t)
assert np.isclose(a2,a1**4)
print('Mode-1 amplitude:',a1,'mode-2 amplitude:',a2)
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

The Well is an optional simulation-data extension with its own acquisition and license rules. The historical ocean-temperature series is observed but is not itself a full heat-equation field.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

Interpolation at unseen grid points and generalization to unseen forcing functions are different tasks. Label the split unit.

## Your independent answer

What should be held out to test transfer to a new heat-equation initial profile?

<details><summary>Reveal answer criteria after your attempt</summary>

Entire initial-condition functions and their solution trajectories, not merely coordinates sampled from profiles already used during fitting.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 28 learning section](../../stages/28/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/28.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
