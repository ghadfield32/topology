# Stage 21 — Rates, equations, units and what data can identify

## Begin with one question

**What does the derivative’s unit tell you?**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

Rate: change per change in an independent variable. ODE: derivatives in one independent variable. PDE: derivatives in several. Identifiability: whether distinct parameters can be distinguished by evidence.

## Work the example before running it

For x(t)=t², a central difference at t=2 with step h computes ((2+h)²-(2-h)²)/(2h)=4 exactly in algebra. The two h² terms cancel. This example demonstrates the formula; most functions have truncation error and floating-point effects.

If x is measured in metres and t in seconds, dx/dt has metres per second. The manufactured function here is nondimensional unless units are assigned consistently. Real mixture ingredients and response strength have different units; differentiating a fitted response with respect to an ingredient does not automatically identify its causal effect. Distinguish a descriptive function, an ODE state trajectory, and a table of independent observations.

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/21/check.py
```

The script is short enough to inspect in full:

```python
import numpy as np
t=2.;h=1e-3
estimate=((t+h)**2-(t-h)**2)/(2*h)
assert np.isclose(estimate,4.)
print('Central difference for t² at t=2:',estimate)
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

Concrete Slump supports mixture-response modeling. Nile supports a historical scalar sequence. Neither is automatically a full spatial field for solving an arbitrary PDE.

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

More precise arithmetic cannot resolve parameters that the observations do not identify. Check which variables were actually measured.

## Your independent answer

If time is converted from seconds to milliseconds, does the numerical velocity stay the same?

<details><summary>Reveal answer criteria after your attempt</summary>

No. A numerical change per millisecond is one thousandth of the numerical change per second for the same physical motion, with the corresponding unit conversion.

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage 21 learning section](../../stages/21/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/21.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
