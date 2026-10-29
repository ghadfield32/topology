# Canonical navigation, not a replacement curriculum

Open ../LEARN_TOPOLOGY.html. The 31-stage catalogue remains unchanged. Its existing 57nativeunits have171generated language interfaces. Ten additional project interfaces follow the supplied engineering-source headings. Generated files are deterministic; source belongs to systems/tools/generate_workbooks.py. Never edit your answers into generated files.

Python interfaces run the actual original reference; Go/Rust interfaces run native16. Their scientific protocol differences remain explicit. A fresh run never looks for an old result. The independent learner workspace is created by learn.py session or learn.py project and is never automatically assessed.

The earlier local workbooks/polyglot generator from your log is not in the supplied archive. These files do not overwrite or impersonate that unpublished work. See docs/v17/SOURCE_MAP.md for the evidence boundary.

## Written guides (hand-maintained)

Unlike `learning/workbooks/`, these pages are **not generated**. They explain tooling rather than
own a lesson.

| Page | What it is | Assessed? |
|---|---|---|
| [rust_from_python.md](rust_from_python.md) | Worked reference: creating a Rust project, the daily command routine, a Python comparison, and six verified corrections to earlier advice | **no** |
| [../optional/world_model/README.md](../optional/world_model/README.md) | Worked reference: a CartPole **world model** — learn the environment, then edit a goal function after training — implemented in Python (PyTorch, optional) and in dependency-free Rust, with an independent persistence reduction and an honest trust horizon | **no** |
| [../optional/world_model/LADDER.md](../optional/world_model/LADDER.md) | The build order: `Hello, world!` → WM01 … WM09, each rung runnable on its own, with a Python mirror for every Rust module and the cross-language checks that found two real bugs | **no** |

Adding a page here is additive: it claims no stage number and no lab key. If a page must render in
the offline reader, re-run `python scripts/build_reader_v9.py` rather than hand-editing
`reader/learning/`.

The world-model page is the second hand-maintained guide, and it deliberately lives outside
`learning/` so that `learning/` keeps owning no catalogue. Its `not_assessed` boundary, its
source attribution and its blocked-without-PyTorch behaviour are asserted by
`tests/test_world_model_optional.py`.

