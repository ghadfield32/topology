# Build it yourself: WM01 → WM09, Rust beside Python

**Status: worked reference. `not_assessed`.** This page is the ladder. It is not a second
curriculum, it owns no stage number, and it does not grade you.

The [main page](README.md) shows the finished idea. This page is the order a person actually
builds it in, one small program at a time, with a Python sibling for each rung so the
comparison is about the **languages** rather than about two different experiments.

```
WM01 state        →  WM02 action   →  WM03 simulator  →  WM04 dataset
                                                              ↓
WM09 experiment   ←  WM08 topology ←  WM07 planner    ←  WM06 rollout  ←  WM05 model
```

Start here. Do **not** read all nine rungs before typing the first one.

---

## 0. Before you start: where your code goes

Your `src/main.rs` at the repository root is a `Hello, world!` sitting inside the Python
package tree. It has no `Cargo.toml` beside it, so `cargo` cannot build it there, and it does
not belong next to `src/shape_lab/`.

**Keep your hello-world, move it into a real crate.** A crate is just a directory with a
`Cargo.toml` and a `src/`.

```powershell
# from the repository root
$Practice = "my_work/world_model_practice01"
New-Item -ItemType Directory -Force "$Practice/src" | Out-Null
```

Then in `my_work/world_model_practice01/` create three files. Type them; do not paste.

`Cargo.toml`:
```toml
[package]
name = "world-model-practice"
version = "0.1.0"
edition = "2021"
rust-version = "1.83"

[dependencies]
```

`rust-toolchain.toml`:
```toml
[toolchain]
channel = "1.90.0"
profile = "minimal"
components = ["rustfmt", "clippy"]
```

`src/main.rs` — your program, unchanged in meaning:
```rust
fn main() {
    println!("Hello, world!");
}
```

Check it:
```powershell
Push-Location my_work/world_model_practice01
cargo locate-project          # which manifest did cargo find?
rustup show active-toolchain  # did the pin apply?
cargo run --offline --locked
Pop-Location
```

### The six things that go wrong at this exact step

| Symptom | Cause | Fix |
|---|---|---|
| `could not find Cargo.toml` | you are in `src/`, not the crate root | `cd` up one level, or `cargo locate-project` |
| `no such command: +1.90.0` | the toolchain is not installed | `rustup toolchain install 1.90.0 --profile minimal` |
| `the lock file ... needs to be updated` with `--locked` | no `Cargo.lock` yet | run once **without** `--locked`, then commit the lock |
| `error: linker not found` | MSVC build tools missing | install "Desktop development with C++" in the Visual Studio installer |
| `Println!` / `printIn` | capital `I` for lowercase `l` | it is `println!`, all lowercase |
| `expected ;` after `println!(...)` | statements are not expressions | a bare `println!` line does not end in `;` inside a block is fine, but keep one style |

That last one is worth understanding rather than memorising: `println!(...)` returns `()`, so
`println!("x")` and `println!("x");` both work as a statement. What does **not** work is
`let x = println!("x");` followed by using `x` as a number.

### Python beside it

```python
# my_work/world_model_practice01/hello.py
print("Hello, world!")
```

```powershell
& .\.venv\Scripts\python.exe my_work/world_model_practice01/hello.py
```

| | Rust | Python |
|---|---|---|
| What runs | a compiled binary | the source, by an interpreter |
| Where the type checking happens | before the program exists | at the moment a line runs |
| What "no build step" costs you | — | an error in line 40 after line 39 printed |
| What the build step costs you | seconds per change | — |

---

## 1. The five checks you run on every rung

Do these in this order, every time. They are the whole workflow.

```powershell
Push-Location optional/world_model/rust_ladder

cargo test --offline --locked                      # does the logic hold?
cargo fmt --all -- --check                         # is it formatted the one agreed way?
cargo clippy --offline --all-targets -- -D warnings # is it wrong in a way that compiles?
cargo run --quiet --offline --locked --example 03_step   # what does it actually print?
Pop-Location
```

Why `clippy -D warnings` and not just `cargo check`:

```
cargo check            → exit 0, warning: unused `Result` that must be used
cargo clippy ... -D warnings → exit 101, error: unused `Result` that must be used
```

`cargo check` is not a correctness gate. A silently discarded error passes it.

And the Python side, which has no equivalent of any of those four commands:

```powershell
$env:PYTHONUTF8='1'
& .\.venv\Scripts\python.exe -m pytest -q tests/test_world_model_ladder.py
& .\.venv\Scripts\python.exe -m ladder.wm03_simulator    # from optional/world_model/python
```

| Rust gate | What Python has instead |
|---|---|
| `cargo test` | `pytest`, plus the same idea |
| `cargo fmt --check` | `ruff format --check` / `black --check` — **not installed here**, so not run |
| `cargo clippy -D warnings` | `ruff check` / `pylint` — also not installed here |
| compile | nothing: a syntax error at import, a type error only if a checker runs |

**Say that plainly in your notes.** Python's tooling can do all of this; this environment does
not have it installed, and a missing tool is `blocked`, not passed.

---

## 2. WM01 — represent a state

Read [rust_ladder/src/state.rs](rust_ladder/src/state.rs), then
[python/ladder/wm01_state.py](python/ladder/wm01_state.py).

```powershell
Push-Location optional/world_model/rust_ladder
cargo run --quiet --offline --locked --example 01_state
```

```python
# from optional/world_model/python
python -m ladder.wm01_state
```

### Predict before you run

1. `State::upright()` then change `theta` to `-0.02`. Does `v` change?
2. `visible()` returns a *tuple* of two numbers. Which two fields are missing?
3. Two states with the same `visible()` pair: can they differ?

Answers: no; `v` and `omega`; yes, and that is the entire reason the article needs memory.

### What each language makes you write down

```rust
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct State {
    pub x: f64,
    pub v: f64,
    pub theta: f64,
    pub omega: f64,
}
```

```python
@dataclass(frozen=True)
class State:
    x: float
    v: float
    theta: float
    omega: float
```

Both give you named fields. The differences are real:

- **`f64` is a decision.** Rust has `f32` and `f64`; picking one is part of the code. Python's
  `float` is a `f64` and you never say so.
- **`Copy` is a claim.** Four `f64` are trivially copyable, so passing a `State` does not move
  it. Python always passes references to objects, which is why the dataclass is `frozen`:
  it recovers the "a state is a value" guarantee by refusing mutation.
- **`new` returns `Result`.** Rust cannot add a runtime type check to a struct literal, so
  validation is a function. Python can put it in `__post_init__`, which is closer, but it
  only runs if you use the constructor.
- **`frozen=True` is checked by the runtime**, not the compiler. `state.x = 1.0` raises
  `FrozenInstanceError` in Python; Rust simply has no `&mut` because the value is not `mut`.

**The trap:** Python annotations are not enforced. `State(x="zero", ...)` fails only at
`__post_init__` (or later, if you removed it). In Rust `State { x: "zero", .. }` does not
compile.

---

## 3. WM02 — represent an action

```powershell
cargo run --quiet --offline --locked --example 02_action
```

Expected:
```text
left     -10 N  (index 0)
right     10 N  (index 1)
```

### Predict

Add `Idle` to the Rust `enum Action`, then run `cargo build`. What error do you get, and at
which line?

You get `error[E0004]: non-exhaustive patterns: 'Action::Idle' not covered` pointing at
`force()`. **The compiler found every place that must change.** Now do the same in Python: add
`IDLE = 2` to the `IntEnum` and run the example. It prints a `KeyError` from `_FORCES` at
**run time**, after the program started.

Then undo both. The point is the comparison, not the variant.

### Why an enum instead of `0` and `1`

| | Rust `enum Action` | Python `IntEnum` | Python bare `int` |
|---|---|---|---|
| A third value is possible | only if you edit the type | only if you edit the enum | always |
| Forgetting a case | compile error | `KeyError` at run time | wrong branch silently |
| Printing | `Left` | `Action.LEFT` | `0` |

---

## 4. WM03 — calculate one step

```powershell
cargo run --quiet --offline --locked --example 03_step
```

### Do this on paper first

From rest and upright, push right. Before running:

- does the cart move this step?
- does the pole tilt this step?

Neither does, and the reason is the integration scheme, not the physics: explicit Euler
advances position and angle using the **old** velocities, which are zero. The force changes the
velocities that the *next* step uses.

Observed:
```text
from rest, push right -> x +0.000000  v +0.195122  theta +0.000000  omega -0.292683
```

### The Rust decision that Python cannot express

```rust
pub fn step(state: State, action: Action) -> Result<State, String>
```

Three things in one signature:

1. `State` by value — four `f64`, so nothing is moved away from the caller.
2. `Result<State, String>` — a bad step is a value, not a panic.
3. The `String` is intentionally boring. A real project would use an error type.

Python raises instead:
```python
def step(state: State, action: Action) -> State:
    if not math.isfinite(...):
        raise ValueError(...)
```

| Failure mode | Rust | Python |
|---|---|---|
| Non-finite result | `Err(String)`, must be handled | `ValueError`, must be handled |
| Ignoring it | `#[must_use]` warning; `clippy -D warnings` fails | nothing; the exception propagates or crashes |
| Partial write before failure | impossible: the value is only built at the end | possible if you mutate before validating |

### One parity bug this rung really had

The Python mirror originally wrote `state.omega ** 2`. The Rust wrote `state.omega *
state.omega`. For about **0.06%** of doubles those differ by one unit in the last place,
because `**` rounds differently from a multiply. In a chaotic system that difference grows
into a visibly different trajectory within a few hundred steps, and the cross-language test
failed on the 455-step episode.

Both now use the multiply, and the reason is written in `wm03_simulator.py`. This is the kind
of thing a second implementation catches and a single-language project never sees.

---

## 5. WM04 — collect, and keep the successor

```powershell
cargo run --quiet --offline --locked --example 04_collect
```

### Predict

With `exploration = 0.0` and `bias_scale = 0.0`, would any episode end by *falling*? No: the
controller balances. If you collected only that, your crash data would be empty and any crash
detector trained on it would be confidently wrong. That is why `exploration` and `bias_scale`
exist, and it is not a detail — the sibling reference lost 143 steps of planner performance to
a related bug.

### The record that matters

```
episode  tick  state  action  successor  terminated  truncated
```

The `successor` field on the **final** transition is the one people drop, and dropping it is
how a crash label loses its prediction target. In the sibling reference this exact omission
removed *every* positive example from training while the loss still went down.

Python has the same seven fields (`wm04_dataset.py`), and the same `episode_bounds` arithmetic
so a window can never span two games.

### Splitting

```
by row:      |--- train ---|-- test --|     ← the same episode is in both. Wrong.
by episode:  |--- ep 1..6 ---|- ep 7..8 -|  ← honest.
```

The test `test_split_by_episode_never_shares_an_episode` is the guard.

---

## 6. WM05 — fit a model instead of calling the simulator

```powershell
cargo run --quiet --offline --locked --example 05_fit
```

The five features, in this order: normalized position, normalized angle, action one-hot
(right, left), bias.

```
ŝₜ₊₁ = sₜ + Δ̂(sₜ, aₜ)
```

Predict the **change**, not the next value. Consecutive states are nearly identical, so a
model asked for the next value scores beautifully by copying its input.

### The ownership lesson in one line

```rust
let model = DeltaModel::fit(&training, 1e-6)?;
```

- `&training` **borrows**. The fit reads the transitions and gives them back.
- The model **owns** only its ten coefficients.
- `?` propagates a rejected fit instead of suppressing it.

Python has no `&`, so the equivalent is simply `DeltaModel.fit(training, 1e-6)`. The
*difference* is that in Rust the compiler proves nothing was moved; in Python you rely on
`fit` not reassigning your list.

Test it: `test_fitting_borrows_the_training_data` asserts the slice still has the same length
afterwards.

### Two more cross-language traps, both caught by the parity test

| Trap | What went wrong | Why it matters |
|---|---|---|
| `x ** 2` vs `x * x` | 1-ULP difference in ~0.06% of doubles | chaos amplifies it into a different trajectory |
| signed vs `abs()` angle | a pole leaning *left* scored as **good** | the planner learns to topple the pole |

The second one is the most instructive bug in this whole ladder. The Rust score used
`theta.abs()`; the Python used `theta`. Python scored a leftward topple at 1.048 while Rust
scored it 0.993 — the "better" plan in Python was to fall over. Neither language helped; only
running both on the same data exposed it.

---

## 7. WM06 — one step is not a rollout

```powershell
cargo run --quiet --offline --locked --example 06_rollout
```

Two experiments:

```
one-step:     sₜ (real) → ŝₜ₊₁          start again from reality each time
free rollout: s₀ → ŝ₁ → ŝ₂ → …          feed the model its own output
```

### The measurement detail that changes the conclusion

Report error **at depth h**, not the mean over `1..h`.

```
mean over depths:  "how wrong on average"     → hides the depth where it breaks
error at depth h:  "how wrong at step h"      → what a planner actually needs
```

### Predict

Will the model beat the frozen baseline ("nothing ever changes") at depth 1? At depth 20?

Look at the printed table. In the reference run the answer is depth 1 yes, depth 29 no — and
the *accurate* horizon (inside a 0.02 rad tolerance) is only 7. **Two different numbers, and
the article's point is that they are different.** Neither specifies a good planning horizon.

Python: `wm06_rollout.py`, same eligible episodes, same frozen baseline.

---

## 8. WM07 — plan, and change the goal without refitting

```powershell
cargo run --quiet --offline --locked --example 07_plan
```

Watch the coefficients printed at the top and the bottom. They are identical. That is the
payload: the goal is not in the weights.

```rust
pub fn plan(
    model: &DeltaModel,      // borrowed: read only
    start: State,            // copied: four f64
    goal: Goal,              // a value chosen at run time
    horizon: usize,
    sequences: usize,
    rng: &mut Rng,           // the only thing that mutates
) -> Result<Plan, String>
```

Three ownership facts in one signature:

- `&DeltaModel` — the planner cannot train, because it has no `&mut`.
- `&mut Rng` — the generator must be mutable, and two `&mut` to it cannot exist at once.
- `Result<Plan, String>` — the failure path is part of the API.

### The objective bug, reproduced

Score a dream by its **average** distance to the target and the planner rejects the only
manoeuvre that works. Moving a cart-pole right requires pushing left first, so the correct
opening move looks worse under an average.

Both languages have the corrected rule (`last_reachable` / `terminal_mean`) and both keep a
test proving the wrong rule ranks the dreams the other way round:

```
Rust:  fn average_scoring_rejects_the_journey_that_arrives
Python: test_parking_is_scored_in_metres
```

### Units, once more

The park target is **metres**. The model's observation is **normalized**. A normalized `1.0` is
`2.4 m`. Comparing them directly is the bug the sibling reference had, and the test that
catches it is:

```python
assert score(2.0) == pytest.approx(0.0, abs=1e-5)   # 1 m away costs exactly 1.0
```

---

## 9. WM08 — geometry, not dynamics

```powershell
cargo run --quiet --offline --locked --example 08_topology
```

The example prints component counts at three radii, then **reverses the trajectory** and
prints them again. Same numbers.

That is the lesson:

> Point-cloud topology describes the sampled geometry of a trajectory and discards temporal
> direction. It cannot certify that the model predicts the next state.

This rung is deliberately H0 only — connected components — because you can check it by hand.
The sibling crate does full H1 persistence with an independent reduction; read that **after**
this, and read it knowing a diagram is a description of a cloud, not of behaviour.

### What the radius does

```
radius 0.05 → 8 components
radius 0.15 → 1 component
```

Neither is "the answer". A number without its radius is not reproducible. The same applies to
the H1 bars in the sibling crate: a bar that survives only because the truncation cut off its
death is an artefact of the scale.

---

## 10. WM09 — save a run nothing can overwrite

```powershell
cargo run --quiet --offline --locked --example 09_experiment -- my_work/ladder01
cargo run --quiet --offline --locked --example 09_experiment -- my_work/ladder01   # refused
```

The refusal is the feature. Read `my_work/ladder01/results.json`: every number has the
configuration that produced it beside it, and `"assessment": "not_assessed"` is in the file.

### A bug this rung had

The first version created the output directory in **both** `prepare` and `save`, so every real
run failed against its own work, and no `results.json` was ever written. The fix is the two
functions that now exist:

```rust
let prepared = ensure_new_output(&output)?;   // once, before the work
// ... compute ...
let file = write_into(&prepared, &config, &sections)?;   // refuses an existing record
```

Two tests lock it: `preparing_once_and_writing_once_is_the_supported_sequence` and
`saving_writes_the_file_it_names`.

---

## 11. The cross-language check that makes the pair worth having

```powershell
& .\.venv\Scripts\python.exe -m pytest -q tests/test_world_model_ladder.py
```

16 tests. The important one runs **both** ladders on the same configuration and compares the
saved records:

```python
for section in ("data", "model"):
    for key, value in python["sections"][section].items():
        assert rust["sections"][section][key] == value        # exact
...
assert rust["sections"]["one_step"]["angle_error_rad"] == \
    pytest.approx(python["sections"]["one_step"]["angle_error_rad"], abs=1e-9)
```

Exact for anything derived from integers and seeding; `1e-9` for anything that solves the
same 5×5 system in a different order.

If you only build one language, you cannot run this, and the two bugs above stay hidden.

---

## 12. What to do with this, in order

| # | Do this | Time |
|---|---|---|
| 1 | Move your hello-world into `my_work/world_model_practice01` and get `cargo run` working | 10 min |
| 2 | WM01 + WM02: type both examples, predict, run, then break the enum on purpose | 30 min |
| 3 | WM03: do the hand calculation before running | 20 min |
| 4 | WM04: collect with `exploration = 0.0` and again with `0.25`; compare the crash counts | 20 min |
| 5 | WM05: delete the `simulator::step` call from a copy and confirm `predict` still works | 15 min |
| 6 | WM06: predict the depth at which the model loses to the frozen baseline, then check | 20 min |
| 7 | WM07: add `Goal::Park(0.5)` and explain the score change in one sentence | 20 min |
| 8 | WM08: explain why reversing time cannot change the component count | 15 min |
| 9 | WM09: run twice; read the refusal; read `results.json` | 15 min |
| 10 | Write `comparison.md`: the seven questions from [polyglot/LEARNING_WORKFLOW.md](../../polyglot/LEARNING_WORKFLOW.md) | 30 min |

**Guided versions of the first three rungs**, with measured output from this machine, are in
the private workspace:

| File | Covers |
|---|---|
| `my_work/world_model_practice01/WALKTHROUGH_WM01_WM02.md` | the broken hello-world, `struct`, `enum`, the `E0004` experiment |
| `my_work/world_model_practice01/WALKTHROUGH_WM03.md` | the exact `8/41` algebra, `Result` versus exceptions, the `must_use` gate, and a measured speed comparison |

Then, and only then, read the sibling reference
([`rust/`](rust/src/lib.rs)) for the GRU version: hidden velocities, a recurrent memory, and a
planner that replans after every real step.

---

## 13. Honest boundaries

- **The linear model is not the article's GRU.** It is fully observed and linear. Its numbers
  must not be compared with the GRU's as though only the language changed.
- **The planner here is open loop** — it commits to a sequence. The sibling reference replans
  after every real step. Different problem, stated rather than blurred.
- **Simulated observations, not measured data.** Nothing here is a sports measurement.
- **One seed, one configuration.** Every record states both.
- **A shape summary is not evidence about dynamics.** See WM08.
- **No learner assessment.** `assessment` is `not_assessed` in every file, and your
  `comparison.md` is yours.

---

## Course links

- [Main world-model page](README.md) — the finished idea, in six parts
- [Source audit](SOURCE_AUDIT.md) — attribution and what is not claimed
- [Exercises](EXERCISES.md) — the independent work
- [Verification](VERIFICATION.md) — exactly what ran, and what did not
- [polyglot/LEARNING_WORKFLOW.md](../../polyglot/LEARNING_WORKFLOW.md) — the seven comparison questions
- [Polyglot parity matrix](../../polyglot/PARITY_MATRIX.md) — how companions are scoped
