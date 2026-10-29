# Build a world model: one idea, in Python and in Rust

**Status: worked reference. `not_assessed`.** This directory is additive. It is not a second curriculum: it owns no stage number, no lab key, and no place in the lesson order.

The 31-stage route in [curriculum/catalog.json](../../curriculum/catalog.json) remains the
single mandatory curriculum, and Go/Rust in [`native/`](../../native/) remain the
scientific reference implementations.

It exists because one public article — Anubhab Banerjee's
*How to Make Your First World Model from Scratch* (Towards Data Science, 23 September
2026) — teaches a pivot this course did not yet have a worked example for: **stop training
a network to know what to do; train one to know what happens next.** Its author's code is
at <https://github.com/AnubhabBanerjee/CartPole-Daydream>. [SOURCE_AUDIT.md](SOURCE_AUDIT.md)
records exactly what belongs to the author, what is ours, and what is not claimed.

---

## The pivot, in the article's own shape

Ordinary reinforcement learning bakes the goal into the weights. Train a DQN with "one
point per step survived" and the goal is *spent*: there is no argument, no flag and no
field to change afterwards. The article demonstrates the consequence memorably. A
perfectly competent balancing agent, politely asked to park the cart at x = +1.0, hovers
at x ≈ −0.1. It is not refusing. There is no ear.

A **world model** is trained on a different question. Hand it a situation and a shove; it
returns the next situation. It knows how carts behave and has no opinion about what you
should do with them. Physics is indifferent to your goals, which is exactly why the goal
has nowhere to hide: it becomes a plain function that reads an imagined future and says
how much it likes it.

Then deciding is almost embarrassingly simple:

1. Invent a few hundred random sequences of shoves.
2. Daydream every one inside the model. **The real world is not consulted.**
3. Score each daydream with whatever function you feel like today.
4. Take the first shove of whichever scored best.
5. Play that one shove for real. Bin the plan. Think again.

That is it. The rest of this page is the part that makes it honest: measuring when the
daydream stops resembling anything.

---

## Run it

Python is the full reference. Rust reproduces the algorithmic core so the arithmetic is
checkable. Each language writes to a **new** directory and refuses to reuse one.

```powershell
# Python — full reference (PyTorch, optional dependency)
uv run --no-sync python optional/world_model/python/world_model.py --output my_work/world_model01

# Python — a run small enough to finish in a minute
uv run --no-sync python optional/world_model/python/world_model.py --output my_work/world_model_tiny01 `
    --episodes 6 --epochs 1 --train-steps 6 --planning-episodes 2 --points 12 --sequences 8

# Rust — independent topology + the linear delta model
Push-Location optional/world_model/rust
cargo test --offline --locked
cargo run --quiet --offline --bin world-model-rust -- --output ..\..\..\my_work\world_model_rust01
Pop-Location

# Rust — the beginner ladder, one example per rung (see LADDER.md)
Push-Location optional/world_model/rust_ladder
cargo test --offline --locked
cargo run --quiet --offline --locked --example 03_step
Pop-Location

# Verify the committed fixture still matches its generator (never overwritten)
uv run --no-sync python optional/world_model/python/make_fixture.py --check
```

If PyTorch is absent, the Python command writes `"status": "blocked"` with the reason and
exits 3. A blocked run is **not** a pass and must never be reported as passed, and no
number is invented to fill the gap. This is the same rule the rest of the repository
follows: an optional dependency that is missing produces `blocked`, never a relabelled
pass.

---

## Part 1 — the game, written out

CartPole is four numbers and two buttons:

| Number | Meaning |
|---|---|
| cart position | where the cart is along the rail; ends the game beyond ±2.4 m |
| cart velocity | how fast it slides |
| pole angle | tilt from upright; ends the game beyond 12° (0.20944 rad) |
| pole angular velocity | how fast it is tipping |

See [python/cartpole.py](python/cartpole.py). Three decisions there are load-bearing:

**Two endings, kept apart.** `terminated` means the pole fell or the cart left the rail.
`truncated` means the 500-step timer expired and nothing failed. Collapsing them into one
`done` flag teaches the model that step 500 of a beautiful game is a catastrophe — it
teaches a hallucination. In Rust the same distinction is an `enum Ending`, so it cannot be
forgotten:

```rust
pub enum Ending { Terminated, Truncated }
```

**The collector must cover the actions, not just the situations.** A perfect balancer
keeps the pole so vertical that the model never sees anything go wrong; pure random
flailing sees nothing but falling over and learns nothing about balancing. The article
spikes the drink: 25% random shoves, and a small per-episode bias so some games travel
along the rail instead of all hovering in place. Without that bias a planner that wants
to *go somewhere* asks about journeys the model has never watched.

**The model is deliberately handicapped.** It sees only position and angle. The
velocities are hidden, because a camera reports where things are, never how fast. To
recover a speed you must compare now against a moment ago, which requires memory — hence
the GRU. `states_are_complete()` in [python/cartpole.py](python/cartpole.py) says so in
code: four numbers determine the next state, two do not.

---

## Part 2 — the network that predicts the world

[python/world_model.py](python/world_model.py) implements a small GRU world model. Two
choices matter more than the architecture:

**Predict the change, not the position.** Consecutive moments are nearly identical. A
network asked for the next position scores magnificently by copying its input: a student
who answers every question with "same as last time" and passes. Ask for the delta and the
trick evaporates.

```python
return obs_norm + delta, termination_logit, hidden
```

**Put both numbers on one scale.** Cart position roams over about 2.4; pole angle over
about 0.21. Unnormalised, the network concludes position errors matter ten times more.
They do not; the angle is what ends the game.

**Crashes need a thumb on the scale — the right kind of thumb.** About one step in 380 is
a failure. A detector answering "we're fine" every time scores 99.7% and is useless — a
smoke alarm with the battery out. Multiplying the *whole* loss by 380 does not fix that: it
changes the optimizer's step size and leaves the optimum at "always alive". The fix is a
positive-class weight inside the BCE, which actually moves the optimum, plus a declared
coefficient (`TERMINATION_LOSS_SCALE = 0.02`) because a normalized-delta MSE of about
1e-4 and a 380-weighted BCE of about 1 cannot share one unscaled sum. Both numbers are in
every results file.

The reported numbers are **recall and false alarms per episode**, never accuracy. At
0.02 the crash head reached 0.93 recall with about 117 false alarms per episode; at 0.01 it
reached 0.38. A detector that flinches too often wastes planning on safe dreams, and one
that never fires strolls into futures where the pole already fell. Which failure you prefer
is a decision, not a measurement.

### The lie the whole method rests on

During training, every step is handed the **real** observation, even when the previous
guess was nonsense. That is teacher forcing: a driving instructor who grabs the wheel
after every mistake. It makes training fast and stable, and it means the model never once
experiences the consequences of its own error.

Hold on to that. Part 3 is where the bill arrives.

---

## Part 3 — take the instructor's hand off

Give the model one real starting situation and a list of shoves. Then make it predict each
moment from its **own** previous prediction:

```python
for index in range(plans.shape[1]):
    observed, logit, hidden = model.step(observed, torch.tensor(plans[:, index]), hidden)
```

One variable changed. That line is the difference between a predictor and a world model,
and it is where errors stop being erased and start compounding.

Measure it against the laziest possible baseline: **assume nothing ever changes**. A
sophisticated network that loses to that potato has not learned physics. The depth at
which our model stops beating it is the deepest honest statement in this directory about
how far the daydream can be trusted.

One measurement detail decides whether that number means anything: error is reported at each depth, never averaged over steps `1..h`. Averaging answers "how wrong is the dream on average" and hides the depth where it falls apart, which is the only depth a planner cares about.

`trust_horizon()` is that measurement, and it returns **a ceiling, not a recommendation.**

---

## Part 4 — changing the goal without touching the model

This is the payload. One trained model, two functions, no retraining:

```python
GOALS = {GOAL_BALANCE: score_balance, GOAL_PARK: score_park}
```

`score_balance` reads "did the dream stay alive, and how upright was it".
`score_park` reads "where did the dream *end up*".

That last phrase is the article's hardest-won correction, and it is worth a paragraph
because it is a bug that looks exactly like a weak model. Scoring each dream by its
*average* distance from the target across the whole dream feels unimpeachable. But to move
a cart-pole right you must first push left — tip it the way you want to go, then chase it.
The opening move of the only manoeuvre that works takes the cart *further away*. Every
dream containing the correct answer scored badly, and the planner correctly discarded it.
It was not failing to find the solution; it was finding it, evaluating it exactly as
instructed, and binning it.

> When a planner underperforms, suspect the objective before the model. A broken model is
> obvious, because predictions are visibly wrong. A broken objective fails quietly, in a
> plausible direction.

---

## Part 5 — planning is a ceiling and a search, and they are different

The article's three lessons, each of which this directory makes measurable:

**Your definition of "good" can silently forbid the solution.** → `terminal_mean()` exists
only because of the paragraph above.

**Cover the actions you will ask about.** → the collector's `bias_scale`; without it the
model has never watched a journey.

**The trustworthy horizon is a ceiling, not a recommendation.** → two separate numbers
limit how far ahead you can usefully plan. How long the model stays accurate (Part 3), and
how well your random search covers the space. There are 8 possible 3-step plans and 200
samples find the best one every time; there are about half a billion 29-step plans and 200
samples are indistinguishable from none. The second limit usually bites first.

### One bug this directory found by measuring, not assuming

The first version of the planner forked every dream from a **zeroed** memory. That looks
harmless and is wrong: the visible observation has no velocities, so a blank memory cannot
know the cart is already moving. Planning then degenerates into guessing, and the goal
function is blamed for a memory bug.

The fix is three lines — fold the real observation and shove into the memory, then fork:

```python
if carry_memory:
    hidden = advance_memory(model, torch, state, action, hidden)
```

`play_episode(..., carry_memory=False)` keeps the broken policy available on purpose, and
`results.json` reports both under `goal_balance` and
`goal_balance_without_carried_memory`, so the difference is a recorded number rather than
a claim. This is also what the article's eight-step warm-up is quietly working around, and
why it discloses the warm-up count.

### Two more bugs the same measurement exposed

Both were found by looking at numbers that could not be right, not by reading the code.

**The crash head had zero positives to learn from.** An off-by-one in the training-window
bounds (`end - sequence - 1` instead of `end - sequence`) dropped the final transition of
every episode — and the final transition is the only one that can carry a `terminated`
label. Training therefore contained 0 crash examples in 7,906 windows. The head learned
"always alive" with perfect confidence, the planner threw away every dream that ended in a
fall, and the result looked like a model that simply was not good enough. A test now
asserts that at least one labelled crash appears inside the training windows.

**The rare-class weight was applied to the wrong quantity.** `380 * BCE(...)` scales the
loss and its gradient; it does **not** move the optimum, which stays at the 99.4% base
rate. `pos_weight=380` reweights only the positive examples and does move it. Separately,
the two heads have natural scales about four orders of magnitude apart, so they need an
explicit `TERMINATION_LOSS_SCALE`; without it whichever term is larger owns the gradient
and the other head degrades.

---

## Part 6 — where the topology comes in

This is the part of the page that is ours rather than the article's.

The course's own `shape_lab.persistence` pipeline can describe the collected
observations: project each transition to `(cart position, pole angle)`, normalise both by
their limits, and read a Rips diagram. [python/topology.py](python/topology.py) does that
with the **same metric and scale as the model's input**, so the cloud and the network are
looking at the same space.

Two things follow, and the second matters more:

1. The same filtration is reduced **independently in Rust**
   ([rust/src/persistence.rs](rust/src/persistence.rs)) from the definition rather than
   translated line by line. Agreement is then evidence about the algorithm; translation
   would only be evidence about a copy.
2. **A Rips diagram of a 2-D cloud is a description, not a meaning.**

### What the shape does *not* say

- White covariance, finite projection scores, or a finite self-supervised loss are not
  semantics, and neither is a homology bar. A loop in this cloud is a feature of where the
  collector drove the cart.
- The diagram depends on `max_edge`. A bar that only survives because the truncation cut
  off its death is a scale artefact. Both the scale and the essential-bar count are
  reported beside the numbers so that nobody can read a loop out of a truncation.
- Changing the collector changes the shape. That is a fact about our collection policy,
  not about CartPole.
- Nothing here is evidence about the learner.

One measured surprise worth keeping: a three-point triangle reports **no** H1 bar. The
third edge arrives at the hypotenuse length and the 2-simplex that fills the loop arrives
at the *same* length, so the bar has zero persistence and the default reporting policy
excludes it. Both implementations agree on this, and both have a test saying so.

---

## What we actually observed on this Windows host

One run, one seed, recorded in full in [VERIFICATION.md](VERIFICATION.md). It is **one
configuration**, not a benchmark, and it is deliberately smaller than the article's. Every
number below is copied from `my_work/world_model_ref06/results.json`; the table is not
reconciled by hand.

| Measured | Value |
|---|---|
| Model size | 14,547 parameters (article: 13,635) |
| Collected transitions | 37,352 from 200 episodes; 187 ended by falling, 13 by the timer |
| Best validation epoch | 16 of 20 — and those weights are **restored**, not just logged |
| One-step error (teacher forced) | 0.0064 m cart, 0.0024 rad pole |
| Crash head | 0.945 recall, 101 false alarms per episode |
| Free-rollout trust horizon at 0.02 rad | **7 steps** |
| Deepest depth still beating the frozen baseline | **29** |
| Coin-flip agent | 21.9 ± 13.2 steps |
| Hand controller | 500.0 steps |
| Planner, balance goal, memory carried | **176.0 steps**, 0.0103 s per decision |
| Planner, park goal, memory carried | 52.0 steps, 0.868 m from the target |
| Planner, balance goal, **memory reset each step** | 51.0 steps |

Free-rollout pole-angle error, after an 8-transition warm-up, at each depth:

| Depth | 1 | 4 | 7 | 8 | 20 | 29 | 30 |
|---|---|---|---|---|---|---|---|
| Model (rad) | 0.0018 | 0.0092 | 0.0183 | 0.0210 | 0.0381 | 0.0531 | 0.0569 |
| Frozen (rad) | 0.0037 | 0.0146 | 0.0221 | 0.0251 | 0.0439 | 0.0535 | 0.0535 |

Read that table the way the article tells you to read it.

- **The two horizons really are different.** The model stays inside a 0.02 rad tolerance for
  **7** steps but beats the frozen baseline for **29**. The article's central methodological
  point reproduces: how long the dream is *accurate* and how long it is *better than doing
  nothing* are separate questions, and neither chooses your planning horizon.
- The planner beats coin flips by about **8×**, using a model that was never told what "good"
  means. The goal was written after training finished.
- It still **loses to a three-line hand-written controller**. If balancing a pole is all you
  want, the napkin wins and you should use it.
- The park goal survives shorter and ends further out, because nothing in this small model
  reliably plans the two-phase manoeuvre. A goal you can change is not a goal you can always
  achieve.
- The memory row is the largest single effect on the page: resetting the memory costs
  **125 steps** (176 → 51). A blank GRU state cannot infer velocity, so the planner forfeits
  most of what the world model knows.
- The crash head fires often (101 false alarms per episode). That is a stated tradeoff, not an
  accident: at a lower weight it missed 62% of real crashes instead.

---

## Learning it from the beginning

[LADDER.md](LADDER.md) is the build order: nine small rungs from `Hello, world!` to a working
planner, in **both** languages, with a Python mirror for every Rust module. Its
`rust_ladder/` crate is separate from the reference `rust/` crate on purpose — one is for
learning the steps, the other is the finished companion.

The cross-language test in that crate found two bugs that neither language could have found
alone: `x ** 2` versus `x * x` (a 1-ULP difference that chaos amplifies), and a scoring
function that used a signed angle, so the Python planner's best plan was to **fall over**.

---

## What each language made explicit

| Question | Python | Rust |
|---|---|---|
| Two endings | two booleans that can disagree | one `enum`, exhaustive `match` |
| A bad action | `int` coerced silently | `Result<State, String>` at the boundary |
| The state | a NumPy array of unknown length | a fixed `struct` of four `f64` |
| Bounds inside a window | a slice that may silently be short | `episode_bounds()` + explicit indexing |
| Numerical fragility | a `nan` that propagates quietly | `f64::INFINITY` for essential bars, checked finiteness |
| The goal | a dict of closures chosen at runtime | an `enum Goal` matched at runtime |
| The averaging bug | `terminal_mean` beside an averaging mean | `score_park` beside `score_park_average`, with a test that fails if they agree |
| The fit | `torch.optim.Adam` | partial-pivoted Gaussian elimination you can read |
| The reduction | `dict` of pivots | `BTreeMap` of pivots, deterministic order |
| Speed of writing it | minutes | much longer, and the types found two of my own bugs |

The last row is the honest one. `cargo test` caught a mutable-capture mistake and a moved
value that Python would have accepted silently. Neither was a scientific error — but
`clippy -D warnings` also caught a real one: an index-based loop bound (`end - sequence - 1`)
that silently excluded every crash example in Python, and whose Rust equivalent the type
system did not catch either. That one had to be found by measuring the label count.

---

## Boundaries and honest limits

- **PyTorch is optional.** Without it the Python path is `blocked`, with a reason and no
  numbers. `optional` in this repository never means "assumed installed".
- **This is a worked reference, not an assignment.** The independent change is described in
  [EXERCISES.md](EXERCISES.md) and stays `not_assessed`.
- **One seed is not a result.** Every record states its seed, episode count and model size
  next to its numbers.
- **No reproduction of the article.** Different sizes, different defaults, no GPU. See
  [SOURCE_AUDIT.md](SOURCE_AUDIT.md).
- **Runs belong in `my_work/`.** No reference file here is edited to make an experiment
  work.
- The Rust crate is dependency-free and builds offline; `--locked` refuses a stale or
  missing lockfile rather than regenerating one.

---

## Course links

- [The 31-stage route](../../curriculum/catalog.json) — the single lesson order
- [LADDER.md](LADDER.md) — build it yourself, WM01 → WM09, in both languages
- [Source audit](SOURCE_AUDIT.md) — attribution, departures, and what is not claimed
- [Exercises](EXERCISES.md) — the independent work, `not_assessed`
- [Verification](VERIFICATION.md) — the exact commands run here and their output
- [Repository layout](../../docs/release/REPOSITORY_LAYOUT.md) — who owns what
- [Optional Rust practice](../rust_practice/README.md) — the sibling additive crate
