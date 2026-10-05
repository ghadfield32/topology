# Separate checks, and what each one actually claims

One blended "all green" number hides which claim was tested. These checks are
deliberately separate. Run them individually with `tools/check_matrix.py`.

```powershell
uv run --no-sync python tools/check_matrix.py --list
uv run --no-sync python tools/check_matrix.py --fast
uv run --no-sync python tools/check_matrix.py --only contracts,python,readers,native
uv run --no-sync python tools/check_matrix.py --only science --output my_work/checks01
uv run --no-sync python tools/check_matrix.py --only notebooks --output my_work/nb_verify01
```

| Check | Scope | Typical cost |
|---|---|---|
| `contracts` | generator freshness, notebook contracts, verifier contracts | seconds |
| `python` | the current Python test suite, with skip reasons collected | ~1 min |
| `readers` | native data decoders vs the independent Python oracle | ~30 s |
| `native` | native algorithm suites (Go and Rust unit tests) | ~10 s |
| `science` | native acceptance plus selected independent NumPy/PyTorch oracles | ~1 min |
| `notebooks` | the generated workbook runtime sweep, all 171 entries | tens of minutes |

Each run writes `check_matrix.json` listing every check's scope, argv, exit code,
timing, output tail and (for `python`) the skip reasons.

## New in v14: the systems layer has its own separated checks

The engineering layer is checked separately from the mathematical reference
sweep, so a pass in one cannot be read as a pass in the other:

```powershell
uv run --no-sync python -m unittest discover -s systems/tests -p 'test_*.py'   # contracts, projects, navigation, workflow
uv run --no-sync python learn.py workbooks --check                            # 181 generated interfaces, no drift
uv run --no-sync python learn.py project --unit sys01 --output my_work/c_reader01
uv run --no-sync python learn.py check-project --workspace my_work/c_reader01 --output my_work/c_reader01/attempt01
uv run --no-sync python learn.py demo --output my_work/integrated_demo01
uv run --no-sync python learn.py verify-projects --output my_work/projects_acceptance01
```

Exit codes follow the same convention: `0` passed, `3` blocked by an absent
optional dependency, `1` a real build or assertion failure. `verify-projects`
returns `3` when any requested unit is blocked — that is a truthful partial, not
an all-pass. The systems sweep that actually executes the generated interfaces is
`systems/tools/sweep_workbooks.py`; it is a reference sweep, not learner
assessment, and each fresh kernel is shut down explicitly even after failure.

## What no check establishes

Stated in the tool's own output, and repeated here so it cannot be missed:

- **Original 133-notebook native parity is NOT certified.** `native/COVERAGE.md`
  records each unit's difference, and
  `native_course.py verify --require-original-parity` refuses the claim on purpose.
  Do not remove that guard to make a screen green.
- Docker/OCI image build and runtime acceptance.
- Live Kubernetes admission, scheduling or a completed Job.
- macOS, GPU/Triton/CUDA execution, PyO3/maturin packaging, or the remote
  systems CI workflow.
- Learner mastery. Every generated notebook is `not_assessed`.

## Protocol parity: say which kind it is

When two implementations are compared, state the category rather than implying
equality:

| Category | Meaning | Where it applies |
|---|---|---|
| exact | integer/structural identity, zero tolerance | rank, counts, IDs, F2 |
| numerical | agrees within a stated tolerance | `1e-8` absolute, `1e-7` relative for native f64 |
| same-protocol optimization | same architecture, split and seed on both sides | the native16 small models |
| related control | analogous but not identical construction | several geometry and operator labs |
| not implemented | outside the native16 scope | full FNO, VGGT inference, alpha/Delaunay |

A different Wine split or a different neural architecture between the original
notebook and the native unit is **not** a language performance comparison. It is
a protocol difference, and `native/COVERAGE.md` says so explicitly.

## Test-identity tracking, not a frozen count

Do not carry a historical pass count across platforms as if it were a constant.
Compare the collected test identities and justify each skip. The current local
result and its three platform skips are recorded by the `python` check, and the
skip reasons differ from the Linux reference host's (which skips Ripser/GUDHI
instead).

## Deploy gates

`tools/native_deploy_verify.py` handles the new native images and Jobs. Static
YAML parsing is reported as `static_only` and is **not** runtime evidence.
Building images and running Jobs require explicit flags, and the cluster gate
refuses to run unless you pass a disposable context (`kind-` by default). The
cleanup path deletes only the namespace that run created and never deletes PVCs.

Exit codes: `0` every requested gate passed, `2` blocked/not-run, `1` a gate ran
and failed.

### What actually ran here

| Gate | Result |
|---|---|
| static policy parse | passed: `read_only_rootfs`, `network_disabled`, `no_new_privileges`, 2 Jobs with deadlines and pinned namespaces |
| docker runtime | passed: server 29.7.2 |
| `--build` (Go + Rust images) | **passed**: both Dockerfiles built, including their in-build native tests, exit 0 |
| hardened `docker run` | **passed**: exit 0 for both; the Go container reported `real_rank 3`, `f2_rank 2` |
| `--jobs` in `kind-shape-learning` | **passed**: both Jobs reached `condition met`, a verify Pod read the PVC, and both `result.json` files parsed with `lab stage01`, `status completed` |

The verifier caught a real defect while doing this: `kubectl apply` rejects a Job
that uses `generateName`. The fix uses `create`, matching the deployment guide,
and waits for the PVC to bind before waiting on the Job.

The learner namespace and its PVC were never touched. Only namespaces created by
these verification runs were removed, and only after exporting their evidence.

