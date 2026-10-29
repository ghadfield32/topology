# Verification: what ran here, and what did not

Recorded on this Windows host, 29 October 2026. Every number below came from a command run
in this checkout. Nothing is copied from the article, and nothing is claimed beyond the
command that produced it.

## Environment

| Component | Version |
|---|---|
| Python (`.venv`) | 3.13.5 |
| PyTorch | 2.10.0+cpu |
| NumPy | 2.3.5 |
| Platform | Windows-11-10.0.26300-SP0 |
| `rustc` / `cargo` | 1.97.1 on `PATH`; the crate pins 1.90.0 via `rust-toolchain.toml` |
| Go | not used by this area |

PyTorch is an **optional** dependency of the course (`physics` extra). It was already
present in this interpreter. A blocked path exists for the case where it is not, and it
was not exercised by a real missing-PyTorch run — the code path is asserted by inspection
in `tests/test_world_model_optional.py`, not by uninstalling PyTorch.

## Commands and observed results

### Rust companion

```powershell
Push-Location optional/world_model/rust
cargo generate-lockfile --offline
cargo test --offline --locked
Pop-Location
```

Observed: **34 unit tests passed, 0 failed**, plus 0 binary tests and 0 doc-tests. The
crate has no dependencies, so no vendor directory is needed and no network access occurs.
Two of those tests exist only to demonstrate the article's averaging bug: they assert that
`score_park_average` prefers hovering while `score_park` prefers the journey that arrives,
so the lesson cannot decay into a comment that nothing checks.

```powershell
cargo fmt --all -- --check
cargo clippy --offline --all-targets -- -D warnings
```

Observed: `fmt` made no further changes after `cargo fmt --all`, and `clippy` exited 0 with
`-D warnings`. Clippy initially rejected six real style problems in this crate — four
negated comparisons on `f64` and two index-based loops — which were fixed rather than
suppressed with `#[allow]`.

```powershell
cargo run --quiet --offline --bin world-model-rust -- --check-topology ..\fixtures\points.json --output <new dir>
```

Observed on the committed fixture: `h0_finite = 23`, `h1_finite = 2`,
`h1_essential = 0`, `h1_total_persistence = 0.5555447016192441`,
`max_persistence = 0.4576295099615885`, `simplex_count = 785`, `max_edge = 1.0`.

### Fixture reproducibility

```powershell
uv run --no-sync python optional/world_model/python/make_fixture.py --check
```

Observed: `.../fixtures/points.json matches`. The generator uses integer arithmetic in a
fixed recurrence, so the bytes do not depend on the NumPy version or platform. The fixture
is a **manufactured** cloud and is labelled as such in the file itself.

### Python: cross-check against the course's own persistence pipeline

`tests/test_world_model_optional.py::test_summary_reuses_the_course_persistence_pipeline`
computes the H1 diagram of the fixture with `shape_lab.persistence` directly and compares
count and total persistence with `optional/world_model/python/topology.py`. Observed:
identical. `test_rust_topology_matches_the_python_pipeline_on_the_same_fixture` compares
the Rust reduction against the Python one on the same fixture. Observed: identical to
within `1e-9`.

### Python: the small end-to-end run

```powershell
uv run --no-sync python optional/world_model/python/world_model.py --output my_work/world_model_tiny01 `
  --episodes 6 --epochs 1 --train-steps 6 --eval-episodes 2 --planning-episodes 2 `
  --points 12 --horizon 8 --planning-horizon 3 --sequences 8 --warmup 2
```

Observed: `status = completed`, `assessment = not_assessed`. This run is what the test
suite executes; it is a smoke check that the whole pipeline connects, not a measurement.

### Python: the recorded reference run

```powershell
uv run --no-sync python optional/world_model/python/world_model.py --output my_work/world_model_ref06 `
  --episodes 200 --epochs 20 --train-steps 200 --eval-episodes 20 --planning-episodes 20 `
  --horizon 30 --planning-horizon 15 --sequences 200 --points 60 --warmup 8
```

Observed, from `my_work/world_model_ref06/results.json` (not committed; this workspace's
`my_work/` is private):

| Metric | Observed |
|---|---|
| Model parameters | 14,547 |
| Collected transitions | 37,352 |
| Episodes | 200 (187 ended by falling, 13 by the timer) |
| Mean episode length | 186.8 steps |
| Action 0 fraction | 0.5007 |
| Best validation epoch / restored | 16 of 20, and restored |
| Teacher-forced validation error | 0.00639 m cart, 0.00235 rad pole |
| Crash recall / false alarms | 0.945 / 100.9 per episode (155 TP, 9 FN) |
| Free-rollout trust horizon at 0.02 rad | **7 steps** |
| Deepest depth beating the frozen baseline | **29** |
| Coin-flip agent (20 episodes) | 21.85 ± 13.23 steps |
| Hand controller (20 episodes) | 500.0 steps |
| Planner, balance goal, memory carried | **176.0 steps**, 0.01034 s per decision |
| Planner, park goal, memory carried | 52.0 steps, 0.868 m from the target |
| Planner, balance goal, memory reset each step | 51.0 steps |
| Topology, 60 evenly spaced observations, `max_edge = 1.5` | H0 59, H1 10, 0 essential, total persistence 0.1227 |

Free-rollout pole-angle error **at each depth**, after an 8-transition warm-up:

| Depth | 1 | 4 | 7 | 8 | 15 | 20 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|
| Model (rad) | 0.00175 | 0.00918 | 0.01826 | 0.02101 | 0.03360 | 0.03814 | 0.05307 | 0.05694 |
| Frozen (rad) | 0.00372 | 0.01463 | 0.02207 | 0.02514 | 0.03577 | 0.04391 | 0.05354 | 0.05351 |

The model crosses the 0.02 tolerance at depth 8 (so the trust horizon is 7) but keeps
beating the frozen baseline until depth 29. **Those two numbers disagree, and that is the
article's methodological point reproduced as a measurement rather than quoted.**

### Three defects this run exposed, and their fixes

These are the reason the numbers above are trustworthy; the earlier `ref01`–`ref05`
directories were discarded rather than reinterpreted.

1. **Blank memory in the planner.** Every candidate plan forked from a zeroed GRU state.
   Because the observation hides the velocities, a blank memory cannot know the cart is
   moving, so planning degenerated. Fixed with `advance_memory`: fold each *real*
   observation and shove forward, then fork. Measured effect: 176 steps versus 51 for the
   retained broken policy.
2. **Blank memory in the drift measurement.** The same mistake in `free_rollout_errors`
   made the first predicted step a pure guess, so the model lost to the frozen baseline at
   depth 1 for reasons that were not drift. Fixed by warming the memory with the same
   number of real transitions (`memory_warmup_steps`, recorded).
3. **Zero crash positives in training.** `valid_window_starts` used `end - sequence - 1`,
   which drops the final transition of every episode — the only transition that can carry
   a `terminated` label. Measured: 0 positives in 7,906 windows. Fixed to
   `end - sequence`, and the dataset now records `next_observations` explicitly so the
   labelled transition always has a prediction target. A test asserts a positive is present.

### Four more defects, found by auditing the finished code against its own claims

These were not caught by a test failure. They were caught by asking the six questions in
[docs/release/VERIFICATION.md](../../docs/release/VERIFICATION.md) about the code that already
passed its suite. That is the honest order: a green suite is a statement about the tests, not
about the experiment.

4. **Goals were scored in normalized units against a metric target.** `PARK_TARGET` is
   `1.0` **metres**, but `score_park` compared it against a normalized observation, where
   `1.0` means `2.4 m`. The planner was asked for the rail limit while the constant said one
   metre. Fixed by converting to metres first, with a test asserting that a dream ending
   exactly at the target scores `1.0` and one metre off scores `0.0`.
5. **Predicted failure was not absorbing.** `survival_mask` applied a per-step threshold, so
   a dream could crash at step 3 and be scored alive at step 4 — making a doomed plan look
   survivable. Fixed with a running logical AND, plus a test on a `[-1, +5, -1, -1]` dream.
6. **Rollout error was averaged over depths.** `free_rollout_errors` averaged steps `1..h`,
   which answers "how wrong on average" and hides the depth where the model falls apart.
   Fixed to report error at depth `h`, which is what changed the headline result from "9
   within tolerance, 8 beating frozen" to the article's actual finding: **7 within tolerance,
   29 beating frozen.**
7. **The best checkpoint was logged but not restored.** `train()` recorded the best
   validation epoch and then left the final-epoch weights in the model, so every later
   measurement described a different model from the one the reported loss belonged to.
   Fixed with `load_state_dict` on a saved copy; the restore is now recorded as
   `restored_best_epoch`.

Question 6 in the audit list — "does evaluation use the selected model checkpoint?" — is
exactly defect 7. The answers are now asserted rather than intended:
`test_goal_is_scored_in_physical_units_not_normalized_ones`,
`test_predicted_failure_is_absorbing`,
`test_rollout_error_is_reported_at_depth_not_averaged_over_depths`, and
`test_training_restores_the_best_validation_checkpoint`.

### A correction to the loss, not just the code

The article's "count each crash 380 times over" was first implemented as
`380 * BCE(...)`. That scales the loss and its gradient but leaves the optimum at the 99.4%
base rate, so the head still answered "always alive" with confidence. The correct form is
`pos_weight=380` inside the BCE, which moves the optimum. The two heads also differ in
natural scale by about four orders of magnitude, so `TERMINATION_LOSS_SCALE` is declared
and recorded. Measured on a smaller 60-episode run: scale 0.01 gave 0.38 recall, 0.02 gave
0.93 with the delta error unchanged, 0.10 gave 0.81. The default is 0.02.

### Python test suite

```powershell
uv run --no-sync python -m pytest -q -ra
```

Observed for the whole repository: **954 passed, 3 skipped, 0 failed** in about 5 minutes.
The 3 skips are the pre-existing host-dependent ones (POSIX directory mode bits, the
opt-in Rust mutation build, POSIX symlink creation) and are unrelated to this area.

```powershell
uv run --no-sync python -m pytest -q -ra tests/test_world_model_optional.py
```

Observed: 38 tests in the main file, all passing. The end-to-end smoke run is the slow one;
everything else finishes in seconds.

### Rust: the beginner ladder (`rust_ladder/`)

A separate crate: nine modules, nine runnable examples, and a Python mirror for each rung.

```powershell
Push-Location optional/world_model/rust_ladder
cargo test --offline --locked
cargo fmt --all -- --check
cargo clippy --offline --all-targets -- -D warnings
Pop-Location
```

Observed: **53 unit tests passed**, `fmt` clean, `clippy -D warnings` clean. All nine examples
were run; `09_experiment` was invoked twice and the second invocation refused to reuse the
directory.

Hand-checked output from `03_step`, which matches the guide's stated numbers exactly:

```text
from step zero, push right -> x +0.000000  v +0.195122  theta +0.000000  omega -0.292683
hand controller survived 500 of 500 steps
```

### The cross-language parity check

```powershell
uv run --no-sync python -m pytest -q tests/test_world_model_ladder.py
```

Observed: **16 passed.** The important one runs both ladders on the same configuration and
compares their saved records: exact equality for counts and coefficients, `1e-9` for
floating-point results.

It found two real bugs, which is the entire argument for writing the second implementation:

| Bug | Symptom | Why only a second implementation found it |
|---|---|---|
| `x ** 2` in Python vs `x * x` in Rust | 1 ULP differs for ~0.06% of doubles | chaos amplifies it into a visibly different trajectory within a long episode |
| signed `theta` in Python's score vs `theta.abs()` in Rust | Python's best "balance" plan scored 1.048; Rust's 0.993 | Python rewarded a pole leaning one way, so its best plan was to **fall over** |

Both are fixed, and both now carry a comment saying why the code is written that way.

### Learner workspace: WM01–WM03 (private, `my_work/`)

The private practice crate was built and executed here, so the walkthroughs quote real
output rather than illustrations. These numbers are **not** part of the repository's
evidence; they exist so the teaching pages can be checked.

| Check | Observed |
|---|---|
| `cargo test --offline --locked` | 4 passed (`my_work/world_model_practice01`) |
| `cargo run --offline --locked` | matches the guide, byte for byte |
| Python mirror `wm03_step.py` | identical output to the Rust binary |
| `cargo fmt --all -- --check` | exit 0 after formatting |
| `cargo clippy --all-targets -- -D warnings` | exit 0 |
| `cargo build --release` | 1.71 s |
| Hand calculation, exact via `fractions.Fraction` | `v = 8/41`, `omega = -12/41` |
| Deliberately flipped force sign | 2 of 4 tests failed, with the actual value printed |

Speed comparison, same arithmetic and `DT`, same 2,000,000 steps, identical checksum
(`-3123714.471541`) across all three:

| Implementation | Time | Per step |
|---|---|---|
| Rust `--release`, scalar | 144.1 ms | 72.0 ns |
| Python, scalar | 1988.9 ms | 994 ns |
| NumPy, vectorised 200,000 × 10 | 267.7 ms | 133.8 ns |

One run each, on a machine under simultaneous load, with no warmup or repeats. That is a
**demonstration that the difference is real and measured**, not a benchmark claim — and the
NumPy row is the one that keeps it honest: vectorised Python is within 2× of Rust, so "Rust
is faster" is true of *sequential per-step loops*, not of array work.

### The `must_use` gate, tested rather than described

A bare `step(...);` statement that drops its `Result`:

```text
cargo check            → warning: unused `Result` that must be used   → exit 0
cargo clippy -- -D warnings → error: unused `std::result::Result`     → exit 101
```

`let _ = step(...);` produces no warning under either, which is the difference between an
explicit acknowledgement and a silent omission.

## What was **not** executed here

- **No GPU run.** No CUDA path, no mixed precision, no timing comparison with the article.
- **No DQN baseline.** The comparison agents are coin flips, the hand-written controller,
  and the frozen-state model.
- **No reproduction of the article's figures or numbers.** See
  [SOURCE_AUDIT.md](SOURCE_AUDIT.md) for the exact list of the author's measurements that
  are quoted rather than re-measured. In particular the article's "H = 29", "37 steps" in
  front of the frozen baseline, "500.0 ± 0.0", "2.94 ms" and "one step in 380" are **the
  author's** numbers under the author's configuration. Ours are 7, 29, 176.0, 10.3 ms and
  about 1 in 187 (from collected episodes).
- **No `ruff`/`black`/`pylint` run.** Those are the Python equivalents of `fmt` and `clippy`
  and they are not installed in this environment. Their absence is `blocked`, not passed; the
  repository's Python suite is the gate that actually ran.
- **No `--release` build for either Rust crate.** Only `cargo test --offline --locked`,
  `cargo run --offline`, `cargo fmt --check` and
  `cargo clippy --all-targets -- -D warnings`.
- **No Go implementation.** Not every companion needs three languages; this one is Python
  and Rust because the point is a scientific reference plus a checkable core.
- **No learner assessment.** `assessment` is `not_assessed` in every record, and
  [EXERCISES.md](EXERCISES.md) and [LADDER.md](LADDER.md) leave the independent work to the
  learner.

## Scope of these results

These are numbers from **one configuration and one seed** on one machine under
simultaneous external load. They show this pipeline runs, that the two persistence
implementations agree, and that the disclosed bug is real and measurable. They do not show
that a world model is a good idea for any real robot, that the planner is competitive with
a tuned policy, or anything about a learner.
