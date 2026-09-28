#!/usr/bin/env python3
"""Generate the polyglot learning notebooks: one Python/Go/Rust triad per lab.

The Python course stays canonical. These notebooks add an *interactive* route
through the same 57 native teaching units, in three languages, for a learner who
may not be comfortable driving the command line.

Design rules enforced here (see docs/release/LANGUAGE_NOTEBOOKS.md):

* The Go and Rust notebooks never compute the scientific result in Python. They
  invoke the real native binary that the native16 acceptance already built and
  compare the two languages on the learner's own machine.
* The Python notebook does not reimplement the lab either. It reads the same
  registered inputs through the existing course decoder and reads an existing
  native run's output, so the learner inspects real evidence rather than a
  lookalike calculation.
* Nothing here claims biological, physical or semantic meaning, and nothing
  claims operation-for-operation equivalence with the 133 original notebooks.

Regenerate with:  python tools/build_language_notebooks.py
"""

from __future__ import annotations

import importlib.util
import json
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "workbooks" / "polyglot"

LANGS = ("python", "go", "rust")
LANG_TITLES = {"python": "Python", "go": "Go", "rust": "Rust"}
NB_METADATA = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.13.5",
    },
}


def load_runner():
    """Load native_course.py (hyphen-free name, same directory) as a module."""
    spec = importlib.util.spec_from_file_location("shape_native_runner", ROOT / "native_course.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _cell_id(kind: str, body: str) -> str:
    """Deterministic nbformat 4.5 cell id, so regeneration stays byte-stable."""
    return hashlib.sha256(f"{kind}\x00{body}".encode("utf-8")).hexdigest()[:12]


def reference_kind(lab: dict) -> str:
    """A lab's canonical reference is usually a notebook, but not always.

    The Poux extension ships a script (`bridge.py`), so callers must not assume
    `.ipynb` and must not silently present a script as a notebook.
    """
    ref = lab.get("reference") or ""
    if ref.endswith(".ipynb"):
        return "notebook"
    if ref.endswith(".py"):
        return "script"
    return "other"


def reference_label(lab: dict) -> str:
    return {
        "notebook": "the canonical worked notebook",
        "script": "the canonical reference script",
        "other": "the canonical reference",
    }[reference_kind(lab)]


def md(text: str) -> dict:
    body = text.strip("\n")
    return {
        "cell_type": "markdown",
        "id": _cell_id("md", body),
        "metadata": {},
        "source": body.splitlines(True),
    }


def comment_block(text: str) -> str:
    """Turn arbitrary lab text into a valid Python comment block."""
    return "\n".join("# " + line.rstrip() for line in text.splitlines())


def code(text: str) -> dict:
    body = text.strip("\n")
    return {
        "cell_type": "code",
        "id": _cell_id("code", body),
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": body.splitlines(True),
    }


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": json.loads(json.dumps(NB_METADATA)),
        "nbformat": 4,
        "nbformat_minor": 5,
    }


# --------------------------------------------------------------------------
# Cell builders
# --------------------------------------------------------------------------


def bootstrap_cell(lab: dict, lang: str) -> str:
    return f'''
"""Notebook setup. Run this first.

This reads the course catalogue and prepares a fresh output directory for this
lab. Nothing is written into the course tree and nothing is graded.
"""
import importlib.util, json, subprocess, sys
from pathlib import Path

# Locate the course root by walking up until native_course.py is found.
_here = Path.cwd().resolve()
ROOT = next(p for p in [_here, *_here.parents] if (p / "native_course.py").is_file())
sys.path.insert(0, str(ROOT / "src"))


def load_runner():
    spec = importlib.util.spec_from_file_location("shape_native_runner", ROOT / "native_course.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


runner = load_runner()
LAB_KEY = {lab["key"]!r}
LAB_ID = {lab["id"]!r}
REFERENCE = {lab["reference"]!r}
LAB = next(r for r in runner.available_labs(ROOT) if r["key"] == LAB_KEY)
print("course root :", ROOT)
print("lab         :", LAB["key"], "-", LAB["title"])
print("kind        :", LAB["kind"])
print("reference   :", REFERENCE)
print("native goal :", LAB["native_goal"])
print("challenges  :", len(LAB["challenges"]))
'''


def freshness_cell(lab: dict, lang: str) -> str:
    return f'''
# --------------------------------------------------------------------------
# Is an existing native run still valid? Source hashes must be unchanged.
# --------------------------------------------------------------------------
RUN_DIR = ROOT / "my_work" / "notebook_{lab["key"]}_{lang}"
RUN_DIR.mkdir(parents=True, exist_ok=True)

REGISTERED = {json.dumps(lab["source_files"], indent=4)}
declared = {{p: (ROOT / p).stat().st_size for p in REGISTERED if (ROOT / p).is_file()}}
missing = [p for p in REGISTERED if p not in declared]
print("declared source files:", len(REGISTERED))
print("present             :", len(declared))
print("missing             :", missing)
declared
'''


def python_reference_cell(lab: dict) -> str:
    """Execute the canonical reference in this repo, in a private fresh-kernel copy."""
    kind = reference_kind(lab)
    if kind == "notebook":
        body = f'''
REF_OUT = ROOT / "my_work" / f"notebook_{{LAB_KEY}}_reference"
already = REF_OUT / "executed" / REFERENCE
if already.is_file():
    print("already executed :", already.relative_to(ROOT))
    print("delete that output directory to rerun from scratch.")
elif REF_OUT.exists():
    # A previous attempt left the directory without a finished run. Say so plainly
    # instead of letting run_references raise a bare FileExistsError.
    print("This lab's output directory already exists but holds no executed copy:")
    print(" ", REF_OUT.relative_to(ROOT))
    print()
    print("That is a leftover from an earlier attempt (possibly interrupted).")
    print("Evidence is never erased for you. Choose ONE of these:")
    print("  - keep the old attempt and run the reference somewhere new:")
    print(f"      uv run --no-sync python course.py run --stage {{LAB_ID}} --output my_work/stage{{LAB_ID}}_ref02")
    print("  - or, after inspecting it, move the old folder aside yourself.")
else:
    print("Running the canonical reference with a fresh kernel in an isolated")
    print("copied workspace. This is the REAL original experiment, not a")
    print("native16 re-implementation. It may take a minute.")
    sys.path.insert(0, str(ROOT / "src"))
    from shape_lab.course import run_references

    manifest = run_references(ROOT, [REFERENCE], REF_OUT, jobs=1, timeout=300)
    for record in manifest["records"]:
        print(f"{{record.get('path')}} -> {{record.get('status')}} {{record.get('error', '')}}")
    print()
    print("executed copy :", (REF_OUT / "executed" / REFERENCE).relative_to(ROOT))
    print("If it failed, read the error above and fix the cause. Do NOT replace")
    print("the canonical reference with a Python re-implementation of the lab.")
'''
    else:
        body = f'''
# This lab's canonical reference is a SCRIPT, not a notebook, so it is handled
# separately instead of being executed as one.
REF_OUT = ROOT / "my_work" / f"notebook_{{LAB_KEY}}_reference"
test_file = (ROOT / REFERENCE).parent / "test_bridge.py"
if test_file.is_file():
    print("Running the extension's own test:", test_file.relative_to(ROOT))
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_file), "-q"],
        cwd=ROOT, capture_output=True, text=True,
    )
    print("exit code:", completed.returncode)
    print((completed.stdout or "").strip()[-1200:])
    if completed.returncode != 0:
        print((completed.stderr or "").strip()[-800:])
else:
    print("No companion test found for this script reference.")
print()
print("A script reference is not a notebook. Do not present it as one.")
'''
    return f'''
# --------------------------------------------------------------------------
# Run the CANONICAL Python experiment for this lab.
# --------------------------------------------------------------------------
# Reference: {lab["reference"]}
# Kind     : {kind} — {reference_label(lab)}
#
# This is the original course material. It is deliberately separate from the
# native16 Go/Rust labs: those are matching teaching protocols, NOT
# operation-for-operation ports of this reference.
{body}'''


def python_inputs_cell(lab: dict) -> str:
    return f'''
# --------------------------------------------------------------------------
# Inspect the ACTUAL registered input this lab consumes, through the existing
# course decoder. This is the same file the native programs read.
# --------------------------------------------------------------------------
from shape_lab import data as course_data

for rel in REGISTERED:
    path = ROOT / rel
    if not path.is_file():
        print(f"{{rel}}: MISSING")
        continue
    print(f"{{rel}}  ({{path.stat().st_size}} bytes)")
    if path.suffix == ".csv":
        rows = course_data.read_csv(path) if hasattr(course_data, "read_csv") else None
        if rows is None:
            import csv
            with path.open(newline="", encoding="utf-8-sig") as fh:
                rows = list(csv.reader(fh))
        print("  header :", rows[0][:8])
        print("  data rows:", len(rows) - 1)
    elif path.suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        kind = type(payload).__name__
        size = len(payload) if hasattr(payload, "__len__") else "-"
        print(f"  json {{kind}} with {{size}} top-level entries")
    else:
        print("  (binary or image; the native readers decode it in Go and Rust)")
'''


def python_compare_cell(lab: dict) -> str:
    return f'''
# --------------------------------------------------------------------------
# Resolve the native evidence this notebook will inspect.
#
# TWO EXPLICIT MODES (Phase C):
#   MODE = "fresh"  -> create the evidence NOW, in this notebook's own run
#                      directory, and verify its identity. Nothing older is used.
#   MODE = "review" -> open a specific previous result and label it as such.
#                      It is never silently "the newest folder that looks right".
# --------------------------------------------------------------------------
MODE = "fresh"          # "fresh" or "review"
PINNED_RUN = None       # for MODE="review": an explicit path, e.g. ROOT / "my_work/native_stage01_01"

if MODE not in ("fresh", "review"):
    raise ValueError('MODE must be "fresh" or "review"')

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("shape_evidence", ROOT / "tools/evidence_pointer.py")
evidence = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(evidence)

NATIVE_RUN = RUN_DIR / "native"

if MODE == "fresh":
    if NATIVE_RUN.exists() and any(NATIVE_RUN.rglob("execution.json")):
        print("This notebook's own run already exists and is reused:")
        print(" ", NATIVE_RUN.relative_to(ROOT))
        print("Delete that directory to force a fresh execution.")
    else:
        print("FRESH EXECUTION: compiling and running the native Go and Rust labs now.")
        print("This creates evidence bound to the CURRENT source and inputs.")
        import shutil
        built = {{}}
        for _lang in ("go", "rust"):
            _tool = shutil.which("go" if _lang == "go" else "cargo")
            print(f"  {{_lang:4s}} toolchain:", _tool or "MISSING (see native/guides/SETUP.md)")
        if all(shutil.which(t) for t in ("go", "cargo")):
            # run_labs writes its command logs into this directory, so it must
            # exist first (native_course.py's own CLI does this via new_directory).
            NATIVE_RUN.mkdir(parents=True, exist_ok=True)
            _result = runner.run_labs(("go", "rust"), [LAB_KEY], NATIVE_RUN, root=ROOT)
            print("  run status:", _result["status"])
            print("  identity  :", "recorded" if _result.get("identity") else "MISSING")
        else:
            print("  Cannot execute fresh: install both toolchains, then re-run this cell.")

# In review mode an explicit path is required. Never scan for "something plausible".
if MODE == "review":
    if PINNED_RUN is None:
        print("REVIEW MODE selected but PINNED_RUN is None.")
        print('Set PINNED_RUN = ROOT / "my_work/<the exact run you mean>".')
        found = None
    else:
        found = evidence.resolve(ROOT, LAB_KEY, run_dir=PINNED_RUN, allow_review=False)
        if found is None:
            print("REVIEW MODE: no readable run at", PINNED_RUN)
        else:
            print("REVIEW MODE: opening a PREVIOUS result, not a fresh execution.")
            print("  path:", PINNED_RUN)
            if not found["has_identity"]:
                print("  WARNING: this evidence has no bound identity; it cannot be")
                print("  matched to the current source, binary or inputs.")
else:
    found = evidence.resolve(ROOT, LAB_KEY, run_dir=NATIVE_RUN, allow_review=False)

results = {{}}
if found is None:
    print()
    print("No usable native evidence for", LAB_KEY)
else:
    results = found["results"]
    run_dir = found["run_dir"]
    print()
    print("run dir      :", run_dir.relative_to(ROOT) if ROOT in run_dir.parents else run_dir)
    print("resolved via :", found["source"])
    print("run status   :", found["status"])
    print("created_at   :", found["created_at"])
    print("languages    :", sorted(results))
    print("has identity :", found["has_identity"])
'''



def python_verify_cell(lab: dict) -> str:
    return f'''
# --------------------------------------------------------------------------
# Compare the two languages with the runner's own tolerance rules, verify the
# run identity, and check the inputs the native programs consumed.
# --------------------------------------------------------------------------
if not results:
    print("Nothing to compare yet. Create a run and re-run the cell above.")
else:
    if {{"go", "rust"}} <= set(results):
        comparison = runner.compare_values(results["go"]["metrics"], results["rust"]["metrics"])
        comparison["input_hashes_identical"] = results["go"]["inputs"] == results["rust"]["inputs"]
        print("go == rust (within tolerance):", comparison["passed"])
        print("numeric values compared      :", comparison["numeric_values_compared"])
        print("max absolute difference      :", comparison["max_absolute_difference"])
        print("input hashes identical       :", comparison["input_hashes_identical"])
        if comparison["discrepancies"]:
            print("discrepancies:", comparison["discrepancies"])
        print()
        print("Is this evidence CURRENT source, or stale?")
        for lang in ("go", "rust"):
            recorded = (found["execution"].get("identity") or {{}}).get("languages", {{}}).get(lang, {{}})
            live = runner.source_id(lang, ROOT)
            if not recorded:
                print(f"  {{lang}}: no identity recorded (legacy evidence) -> cannot confirm")
            else:
                same_src = recorded.get("source_sha256") == live
                print(f"  {{lang}}: source {{'MATCH' if same_src else 'DIFFERS'}}; recorded {{str(recorded.get('source_sha256'))[:12]}} live {{live[:12]}}")
    else:
        print("Only one language result present:", sorted(results))

    # The native result records the hash of every file it consumed.
    audit = results.get("go", results.get("rust", {{}})).get("inputs", {{}})
    for rel in sorted(audit):
        info = audit[rel]
        actual = runner.digest(ROOT / rel)
        flag = "OK " if actual == info["sha256"] else "CHANGED"
        print(f"{{flag}} {{rel}}")
'''


def python_explain_cell(lab: dict) -> str:
    challenges = comment_block("\n".join(f"{i + 1}. {c}" for i, c in enumerate(lab["challenges"])))
    return f'''
# --------------------------------------------------------------------------
# Now switch language. The SAME lab, the same inputs, the same comparison.
# --------------------------------------------------------------------------
# Read next:
#   native/guides/labs/{lab["key"]}.md              (the implementation guide)
#   native/guides/LEARNING_PATHS.md                 (the C. Python path)
#   {lab["lesson"]}
#
# Then open, in this order:
#   ../go/{lab["key"]}.ipynb
#   ../rust/{lab["key"]}.ipynb
#
# Three independent challenges for THIS lab:
{challenges}
#
# Boundary to remember:
{comment_block(lab["original_scope_gaps"])}
#
# Unassessed. Record your prediction, hand calculation, change, output and one
# limitation in your own notes before moving on.
print("python notebook complete for", LAB_KEY)
'''


def native_bootstrap_cell(lab: dict, lang: str) -> str:
    return f'''
"""Notebook setup. Run this first.

You are in the {LANG_TITLES[lang]} notebook for {lab["key"]}. It compiles and runs
the real {LANG_TITLES[lang]} program, exactly as native_course.py does, so you can
walk through the code and the evidence interactively.
"""
import importlib.util, json, subprocess, sys, os
from pathlib import Path

_here = Path.cwd().resolve()
ROOT = next(p for p in [_here, *_here.parents] if (p / "native_course.py").is_file())


def load_runner():
    spec = importlib.util.spec_from_file_location("shape_native_runner", ROOT / "native_course.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


runner = load_runner()
LANG = {lang!r}
LAB_KEY = {lab["key"]!r}
LAB = next(r for r in runner.available_labs(ROOT) if r["key"] == LAB_KEY)
RUN_DIR = ROOT / "my_work" / "notebook_{lab["key"]}_{lang}"
RUN_DIR.mkdir(parents=True, exist_ok=True)

print("course root :", ROOT)
print("language    :", LANG)
print("lab         :", LAB["key"], "-", LAB["title"])
print("output dir  :", RUN_DIR.relative_to(ROOT))
'''


def toolchain_cell(lab: dict, lang: str) -> str:
    tool = "go" if lang == "go" else "cargo"
    version_args = ["version"] if lang == "go" else ["--version"]
    extra_line = (
        ""
        if lang == "go"
        else "\n    print('note: native/rust pins its own toolchain in rust-toolchain.toml')"
    )
    return f'''
# --------------------------------------------------------------------------
# Step 1: is the toolchain present? A missing compiler is an environment
# problem, NOT a mathematics failure. Read native/guides/SETUP.md if it fails.
# --------------------------------------------------------------------------
import shutil

tool = shutil.which({tool!r})
print({tool!r}, "->", tool)
if tool:
    version = subprocess.run([tool, *{version_args!r}], capture_output=True, text=True)
    print(version.stdout.strip() or version.stderr.strip()){extra_line}
else:
    print("Install the toolchain before continuing: native/guides/SETUP.md")
'''


def dispatch_cell(lab: dict, lang: str) -> str:
    dispatch = lab["go_dispatch"] if lang == "go" else lab["rust_dispatch"]
    return f'''
# --------------------------------------------------------------------------
# Step 2: read the dispatch arm for THIS lab.
# The dispatch file is a map of lab key -> algorithm. It is not the algorithm.
# Follow the helper calls it makes.
# --------------------------------------------------------------------------
dispatch = ROOT / {dispatch!r}
text = dispatch.read_text(encoding="utf-8")
print("dispatch file:", dispatch.relative_to(ROOT))
print("lines:", len(text.splitlines()))

needle = {lab["key"]!r}
for i, line in enumerate(text.splitlines(), start=1):
    if needle in line:
        lo, hi = max(1, i - 3), i + 18
        print(f"--- context around line {{i}} ---")
        for j in range(lo, hi + 1):
            rows = text.splitlines()
            if j <= len(rows):
                marker = ">>" if j == i else "  "
                print(f"{{marker}} {{j:4d}} {{rows[j - 1]}}")
        break
else:
    print("No direct dispatch arm found for", needle, "- inspect the file yourself.")
'''


def build_cell(lab: dict, lang: str) -> str:
    return f'''
# --------------------------------------------------------------------------
# Step 3: compile the native program. This can take a few seconds the first
# time and is cached afterwards under my_work/native_build/.
# --------------------------------------------------------------------------
exe = runner.build(LANG, RUN_DIR, root=ROOT)
print("binary:", exe)
print("sha256:", runner.digest(exe))
'''


def run_cell(lab: dict, lang: str) -> str:
    return f'''
# --------------------------------------------------------------------------
# Step 4: run ONLY this lab and read the JSON it produced.
# The runner validates the result schema and every consumed-file hash.
# --------------------------------------------------------------------------
result = runner.execute_lab(LANG, LAB_KEY, exe, RUN_DIR, root=ROOT)
print("lab      :", result["lab"])
print("language :", result["language"])
print("status   :", result["status"])
print()
print("metrics:")
print(json.dumps(result["metrics"], indent=2, sort_keys=True))
'''


def inputhash_cell(lab: dict, lang: str) -> str:
    return f'''
# --------------------------------------------------------------------------
# Step 5: what did this program actually read? Every entry is hashed.
# --------------------------------------------------------------------------
for rel, info in sorted(result["inputs"].items()):
    on_disk = runner.digest(ROOT / rel)
    verdict = "MATCH" if on_disk == info["sha256"] else "CHANGED"
    print(rel)
    print("  recorded", info["sha256"])
    print("  on disk ", on_disk, " ", verdict)
'''


def compare_cell(lab: dict, lang: str) -> str:
    other_lang = "rust" if lang == "go" else "go"
    return f'''
# --------------------------------------------------------------------------
# Step 6: compare with the other language.
# Open ../{other_lang}/{lab["key"]}.ipynb and run its Step 5 first, then come
# back and run this cell.
# --------------------------------------------------------------------------
OTHER = {other_lang!r}
other = (ROOT / "my_work" / f"notebook_{{LAB_KEY}}_{{OTHER}}" / OTHER / f"{{LAB_KEY}}.json")
print("looking for:", other.relative_to(ROOT))
if not other.is_file():
    print("Not found yet - run Step 4 in the other language notebook first.")
else:
    mine = json.loads((RUN_DIR / LANG / f"{{LAB_KEY}}.json").read_text(encoding="utf-8"))
    theirs = json.loads(other.read_text(encoding="utf-8"))
    comparison = runner.compare_values(mine["metrics"], theirs["metrics"])
    comparison["input_hashes_identical"] = mine["inputs"] == theirs["inputs"]
    print("agreement within tolerance:", comparison["passed"])
    print("numeric values compared   :", comparison["numeric_values_compared"])
    print("max absolute difference   :", comparison["max_absolute_difference"])
    print("input hashes identical    :", comparison["input_hashes_identical"])
    if comparison["discrepancies"]:
        print("discrepancies:", comparison["discrepancies"])
'''


def explain_cell(lab: dict, lang: str) -> str:
    challenges = comment_block("\n".join(f"{i + 1}. {c}" for i, c in enumerate(lab["challenges"])))
    other = "Go" if lang == "rust" else "Rust"
    lang_specific = {
        "go": (
            "Go: is the working matrix a copy of the outer slice, the rows, or both? "
            "Change one element of a pivot row and observe whether the caller sees it."
        ),
        "rust": (
            "Rust: which function borrows the input and which one takes ownership? "
            "Try removing a `.clone()` and read the compiler diagnostic before restoring it."
        ),
    }[lang]
    return f'''
# --------------------------------------------------------------------------
# Step 7: explain, then change one thing.
# --------------------------------------------------------------------------
# Implementation guide : native/guides/labs/{lab["key"]}.md
# Language path        : native/guides/LEARNING_PATHS.md  (section {'D. Go' if lang == 'go' else 'E. Rust'})
# Original Python ref  : {lab["reference"]}
#
# Three independent challenges for THIS lab:
{challenges}
#
{comment_block(lang_specific)}
#
# Boundary - what this lab does NOT establish:
{comment_block(lab["original_scope_gaps"])}
#
# Copy native/{lang} to a private folder, change ONE assumption, predict the
# effect BEFORE running, then compare. A copied reference is guided practice.
print("{LANG_TITLES[lang]} notebook complete for", LAB_KEY)
'''


# --------------------------------------------------------------------------
# Notebook assembly
# --------------------------------------------------------------------------


def python_notebook(lab: dict) -> dict:
    return notebook([
        md(f'''
# {lab["key"]} — {lab["title"]}

**Python route** · lab `{lab["key"]}` · {lab["kind"]}

Make your hand prediction first, then open {reference_label(lab)}
(`{lab["reference"]}`) and the [lesson]({lab["lesson"]}).
The canonical course is `lessons/` + references; this notebook adds an
interactive route through the native16 evidence, not a second curriculum.

## The native experiment for this lab

{lab["native_goal"]}

## Boundary

{lab["original_scope_gaps"]}
'''),
        md("## 1. Setup"),
        code(bootstrap_cell(lab, "python")),
        md("## 2. Run the canonical Python experiment"),
        code(python_reference_cell(lab)),
        md("## 3. Which registered inputs does this lab consume? (input audit)"),
        code(freshness_cell(lab, "python")),
        md("## 4. Inspect the real input data (input audit)"),
        code(python_inputs_cell(lab)),
        md("## 5. Find a real native run to inspect (output audit)"),
        code(python_compare_cell(lab)),
        md("## 6. Compare Go against Rust, and re-check the input hashes (output audit)"),
        code(python_verify_cell(lab)),
        md(f'''
## 7. Continue in Go and Rust

Steps 3–6 above audit the **inputs and an existing native run's outputs**; they do
not recompute the lab. The native experiment itself runs in Go and Rust.

| Language | Notebook | What it shows |
|---|---|---|
| Go | `../go/{lab["key"]}.ipynb` | slice copying, row storage, explicit errors |
| Rust | `../rust/{lab["key"]}.ipynb` | ownership, borrowing, `Result`, owned working copies |

This notebook is **unassessed**.
'''),
        code(python_explain_cell(lab)),
    ])


def native_notebook(lab: dict, lang: str) -> dict:
    title = LANG_TITLES[lang]
    return notebook([
        md(f'''
# {lab["key"]} — {lab["title"]}

**{title} route** · lab `{lab["key"]}` · {lab["kind"]}

This notebook compiles and runs the **real {title} program**. Python is only the
driver: it builds the binary, launches it and compares results. The mathematics
happens in {title}.

## The native experiment for this lab

{lab["native_goal"]}

## Boundary

{lab["original_scope_gaps"]}
'''),
        md("## 1. Setup"),
        code(native_bootstrap_cell(lab, lang)),
        md("## 2. Toolchain check"),
        code(toolchain_cell(lab, lang)),
        md("## 3. Read the dispatch arm for this lab"),
        code(dispatch_cell(lab, lang)),
        md("## 4. Compile"),
        code(build_cell(lab, lang)),
        md("## 5. Run this lab"),
        code(run_cell(lab, lang)),
        md("## 6. Which inputs did it consume?"),
        code(inputhash_cell(lab, lang)),
        md(f'''
## 7. Compare against the other language

Run step 5 in `../{"rust" if lang == "go" else "go"}/{lab["key"]}.ipynb`, then run
the cell below. You should see agreement within tolerance and identical input
hashes. Agreement is software evidence, not a proof of meaning.
'''),
        code(compare_cell(lab, lang)),
        md(f'''
## 8. Change one thing

`native/guides/LEARNING_PATHS.md`, section {'D. Go' if lang == 'go' else 'E. Rust'}.

Copy the {title} source to a private folder, change a single assumption, predict the
effect before running it, then explain what the language made explicit. This
notebook is **unassessed**.
'''),
        code(explain_cell(lab, lang)),
    ])


def write_notebook(path: Path, nb: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def index_html(labs: list[dict]) -> str:
    rows = "\n".join(
        "<tr>"
        f'<td><code>{lab["key"]}</code></td>'
        f'<td>{lab["title"]}</td>'
        f'<td><a href="python/{lab["key"]}.ipynb">Python</a></td>'
        f'<td><a href="go/{lab["key"]}.ipynb">Go</a></td>'
        f'<td><a href="rust/{lab["key"]}.ipynb">Rust</a></td>'
        "</tr>"
        for lab in labs
    )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Learn any lab in Python, Go or Rust · Listening to Shape</title>
<style>
body{{font:17px/1.55 system-ui;max-width:1100px;margin:36px auto;padding:0 20px}}
table{{border-collapse:collapse;width:100%}}
th,td{{border-bottom:1px solid #ddd;padding:6px 10px;text-align:left}}
notice,.notice{{display:block;background:#f0f4f8;padding:14px 16px;border-left:4px solid #4a6fa5;margin:18px 0}}
code{{background:#f4f4f4;padding:1px 4px;border-radius:3px}}
</style></head><body>
<h1>Learn any lab in Python, Go or Rust</h1>
<p>One notebook triad per learning unit: the same lab, the same registered inputs,
the same comparison, in three languages. Start with Python, then Go, then Rust.</p>
<div class="notice">
<strong>Unassessed.</strong> These notebooks add an interactive route through the
same {len(labs)} native teaching units. They are not a second curriculum, they do
not grade you, and they do not establish scientific meaning.
Read <a href="../../docs/release/LANGUAGE_NOTEBOOKS.md">the guide</a> and
<a href="../../native/guides/LEARNING_PATHS.md.html">the language paths</a>.
</div>
<p>{len(labs)} labs &times; 3 languages = {len(labs) * 3} notebooks.
<a href="README.md">Plain-text index</a> ·
<a href="../">Course workbooks</a> ·
<a href="../../START_NATIVE.html">Native learning home</a></p>
<table>
<thead><tr><th>Lab</th><th>Title</th><th>Python</th><th>Go</th><th>Rust</th></tr></thead>
<tbody>
{rows}
</tbody></table>
<p>Run a lab without a notebook:
<code>uv run --no-sync python native_course.py compare --lab stage01 --output my_work/native_stage01_01</code></p>
</body></html>
'''


def index_markdown(labs: list[dict]) -> str:
    lines = [
        "# Learn any lab in Python, Go or Rust",
        "",
        "One notebook triad per learning unit: the same lab, the same registered",
        "inputs, the same comparison — three languages. Start with Python, then Go,",
        "then Rust. See [the guide](../../native/guides/LEARNING_PATHS.md) and the",
        "[import record](../../docs/release/LANGUAGE_NOTEBOOKS.md).",
        "",
        "Each notebook is **unassessed**. Nothing here is a second mandatory curriculum.",
        "",
        "| Lab | Title | Python | Go | Rust |",
        "|---|---|---|---|---|",
    ]
    for lab in labs:
        key = lab["key"]
        lines.append(
            f"| `{key}` | {lab['title']} | "
            f"[py](python/{key}.ipynb) | [go](go/{key}.ipynb) | [rust](rust/{key}.ipynb) |"
        )
    lines += [
        "",
        f"Total: {len(labs)} labs × 3 languages = {len(labs) * 3} notebooks.",
        "",
        "## Run a lab without a notebook",
        "",
        "```",
        "uv run --no-sync python native_course.py compare --lab stage01 --output my_work/native_stage01_01",
        "```",
        "",
    ]
    return "\n".join(lines)


def render(labs: list[dict]) -> dict[str, str]:
    """Return every generated path -> exact content. The single source of output."""
    files: dict[str, str] = {}
    for lab in labs:
        files[f"python/{lab['key']}.ipynb"] = nb_text(python_notebook(lab))
        files[f"go/{lab['key']}.ipynb"] = nb_text(native_notebook(lab, "go"))
        files[f"rust/{lab['key']}.ipynb"] = nb_text(native_notebook(lab, "rust"))
    files["README.md"] = index_markdown(labs)
    files["index.html"] = index_html(labs)
    return files


def nb_text(nb: dict) -> str:
    return json.dumps(nb, indent=1, ensure_ascii=False) + "\n"


def check(out_root: Path = OUT_ROOT) -> int:
    """Compare the committed tree against a fresh render. Non-zero means stale.

    Without this, running the generator with any flag (including an unknown one)
    silently rewrote all 171 workbooks and still exited 0.
    """
    labs = load_runner().available_labs(ROOT)
    expected = render(labs)
    stale: list[str] = []
    missing: list[str] = []
    for rel, content in sorted(expected.items()):
        path = out_root / rel
        if not path.is_file():
            missing.append(rel)
        elif path.read_text(encoding="utf-8") != content:
            stale.append(rel)

    extra = [
        p.relative_to(out_root).as_posix()
        for p in out_root.rglob("*")
        if p.is_file() and p.relative_to(out_root).as_posix() not in expected
    ]

    print(f"generator check: {len(expected)} expected files under {out_root}")
    for name, group in (("missing", missing), ("stale", stale), ("unexpected", extra)):
        if group:
            print(f"  {name}: {len(group)}")
            for rel in group[:20]:
                print("   ", rel)
    if missing or stale or extra:
        print("FAILED: the committed workbooks differ from the generator.")
        print("Run: python tools/build_language_notebooks.py")
        return 1
    print("OK: committed workbooks match the generator exactly.")
    return 0


def main(out_root: Path = OUT_ROOT, check_only: bool = False) -> int:
    if check_only:
        return check(out_root)

    labs = load_runner().available_labs(ROOT)
    assert len(labs) == 57, f"expected 57 labs, found {len(labs)}"

    files = render(labs)
    for rel, content in sorted(files.items()):
        path = out_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    label = out_root.relative_to(ROOT) if ROOT in out_root.parents or out_root == ROOT else out_root
    print(f"wrote {len(files)} files ({len(labs) * 3} notebooks) under {label}")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed workbooks match the generator; exit 1 if stale",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUT_ROOT,
        help="target directory (defaults to workbooks/polyglot)",
    )
    args = parser.parse_args()
    # Unknown flags are now a hard error instead of a silent full rewrite.
    sys.exit(main(args.output.resolve(), check_only=args.check))
