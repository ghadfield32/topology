# Source audit: the world-model article

## What the source is

| Field | Value |
|---|---|
| Author | Anubhab Banerjee (PhD, TUM; senior AI researcher) |
| Title | *How to Make Your First World Model from Scratch* |
| Venue | Towards Data Science, 23 September 2026, 27-minute read |
| Subtitle | "A beginner-friendly guide to building a world model in Python, letting it daydream its way through CartPole, and accurately measuring when the illusion collapses." |
| Author's code | <https://github.com/AnubhabBanerjee/CartPole-Daydream> |
| Supplied form | A reader-mode paste of the article, supplied by the repository owner on 29 October 2026 |

The paste contains the article's prose, its illustrative Python fragments, and its
measured tables. It does **not** contain the author's notebooks, their checkpoints, or
their figures as data. Nothing in this directory is a copy of that repository.

## What belongs to the author

Every number in the article's figures and tables is the author's measurement under the
author's configuration. **None of it is reproduced here as ours.** In particular:

- "350 ± 184 out of 500" for DQN on standard CartPole;
- "156,967 transitions" from 500 episodes, mean length 313.9;
- "one step in 380" failure rate;
- "3.8 millimetres" cart error and "0.00026 radians" angle error at one step;
- "H = 29" from a 0.02-radian tolerance, and "37 steps" for the frozen baseline;
- "500.0 ± 0.0" for the planner, "2.94 ms" per decision, "0.16 ms" for the DQN;
- the horizon sweep (25.0 → 500.0 → 493.0 → 477.1 → 450.1 → 245.9 → 158.8).

Where this directory quotes one of those, it says "the article reports". Our own
`results.json` files contain only numbers we produced on this machine, and each carries
the interpreter, PyTorch version and full configuration beside them.

## What is ours

- The CartPole integrator, collector, normalisation and trust-horizon function, written
  from the standard published CartPole equations (Barto, Sutton and Anderson 1983) and
  the task description in the article, not copied from any repository.
- The GRU world model, teacher-forced trainer, batched free rollout and planner.
- The two goal functions, including the terminal-position scoring that the article says
  took a bug to discover.
- The independent Rust F2 persistence reduction, the linear delta model, and the
  comparison harness that checks Rust against Python on one committed fixture.
- The deterministic fixture generator and the fixture it produces (a **manufactured**
  cloud, explicitly not observed CartPole episodes).

## Deliberate departures from the article

| Article | Here | Why |
|---|---|---|
| Trains a GRU with PyTorch, ~13,635 parameters | Same, with a smaller hidden size | A smaller model trains in minutes on a CPU and its parameter count is recorded rather than asserted |
| Predicts the next observation | Predicts the **change**, in normalized units | Stated by the article as the reason the model learns physics instead of copying its input; made explicit in code |
| "Count each crash 380 times over" | `pos_weight=380` inside the BCE, plus a declared `TERMINATION_LOSS_SCALE` | A literal `380 * BCE` scales the gradient but leaves the optimum at the base rate, so it still predicts "always alive". The two heads also differ in natural scale, so the coefficient has to be stated |
| Uses 500 collection episodes | Defaults to 200, configurable | Documented as a smaller run, never presented as the article's numbers |
| Reports a planner result with an 8-step warm-up | Same warm-up, and the same warm-up applied to the drift measurement | The article discloses the planner warm-up; the drift sweep had the same blank-memory problem, so it is warmed too and the count is recorded |
| Reports free-rollout error to depth 100 | Depths up to `--horizon`, default 30 | Long rollouts of a small model are dominated by the truncation artefacts we already measure |
| Uses a DQN baseline | Uses a coin-flip agent, the hand controller and the frozen-state model | A DQN is a second training problem; the point being measured is whether the planner beats doing nothing |
| Reports a policy that ties the hand controller | Our planner beats coin flips by ~8× and loses to the hand controller | Different model size, fewer episodes, one seed. The ordering, not the values, is what we can support |

## What this directory does not claim

- It does not reproduce the article's figures, and no figure comparison is asserted.
- It does not run on a GPU, and no timing comparison with the article is made. Decision
  time here is measured on this CPU and is only comparable with our own other agents.
- It does not establish that a world model is a good idea for any real robot. CartPole is
  four numbers with no friction, no contact and no sensor noise.
- The topology summary describes the collector, not the physics. See
  `../README.md#what-the-shape-does-not-say`.
- Nothing here assesses a learner. `assessment` is `not_assessed` in every record.

## Licensing and redistribution

The article and its code are third-party work. This directory links to both and does not
redistribute either. The author's repository has its own licence; check it before copying
anything from it. The CartPole equations are standard published physics and are restated
here from the task description.

## Related course sources

- `sources/v5_sources.json` — the primary-source ledger for the physics and representation
  tracks (`HNN`, `LNN`, `PCGRAD`, `CONFIG`), which is where the physics-loss material
  already lives.
- `docs/sources.json` — the topology reference ledger (`R1`–`R10`, `D1`–`D3`, `L1`–`L3`).
- `docs/release/VERIFICATION.md` — what has actually been executed in this checkout.
