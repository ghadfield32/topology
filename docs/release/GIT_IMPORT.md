# Import into Git without damaging another project

## Recommended layout

Use either a new dedicated repository with the course contents at its root, or a new subdirectory in your existing repository:

```text
your-repository/
  learning/
    listening-to-shape/
      pyproject.toml
      .python-version
      course.py
      tools/
      curriculum/
      ...
```

Do not merge this `pyproject.toml` into your production application's file. Run course commands from the course subdirectory so uv selects its environment. If the parent is a uv workspace, explicitly exclude this standalone course or deliberately integrate it after reviewing workspace dependency rules; do not let it become an accidental workspace member.

## Fresh dedicated repository

Extract the ZIP into a new folder, then copy the contents of `listening_to_shape_lab/` into the new repository folder. Include dotfiles such as `.gitignore`, `.github`, `.python-version` and `.dockerignore`. Do not include `.venv` or local caches.

```bash
git init
python -m pip install uv==0.10.0
uv python install 3.13.5
python tools/bootstrap.py --profile core
uv run --no-sync python course.py test --profile core --output my_work/import_tests01
uv run --no-sync python course.py run --stage 0 --output my_work/import_stage00_01
git status --short
```

After reviewing the file list and license requirements:

```bash
git add .
git status --short
git commit -m "Add executable shape-learning course"
```

Configure your chosen remote through your normal workflow. This package does not push, create a remote, create a pull request, or publish data. Do not add an arbitrary remote or force-push on the strength of a generated instruction.

## Existing repository or monorepo

Create a new, empty `learning/listening-to-shape/` directory and copy the complete course into it. Refuse to overwrite an existing course automatically. Inspect the diff before committing.

A `.github/workflows/` directory inside a subdirectory is not a repository-level workflow. For monorepos, adapt the included workflow into the repository's root `.github/workflows/`: set the run steps' working directory to the course subdirectory, adjust artifact paths, and ensure Docker's context points to that subdirectory. Do not replace existing CI blindly. This adaptation is configuration to review, not a workflow that has already run.

The [agent handoff](AGENT_HANDOFF.md) gives a pasteable implementation brief for doing this inside your existing repository while respecting its own instructions.

## Lock and environment rules

`uv.lock` belongs in Git after a real connected-machine resolution. `.venv/` never does. The archive includes observed transitive version constraints but does not mislabel them as a solver-created lock. A first successful bootstrap creates the lock; later bootstraps check it with uv before synchronizing.

An intentional dependency upgrade should happen on its own branch: update the intended constraints, resolve the lock, run the tests and affected reference experiments, review changes, then commit. Do not change package versions during an experiment and continue presenting it as the same run.

## Data and source publication review

Read [LICENSE.md](../../LICENSE.md), the individual data cards, and the sports terms. The SPL excerpt has noncommercial/share-alike restrictions. Code terms do not override data terms. Some optional sports/biomechanics payloads are not included specifically because access, size or license conditions require a separate review.

This archive contains original teaching material, linked references, historical audit records, and user-supplied context. Before making a repository public, review `sources/`, recorded personal context, any local answers, any athlete identifiers, and data terms. A private learning repository is the safer starting point when permission is unclear. This is not a legal opinion or a permission grant from a data provider.

The supplied `.gitignore` excludes secrets, local run folders and progress logs. Git ignore rules do not remove a file already tracked by an existing repository. Inspect `git status` and `git diff --cached` before committing. Never add tokens, `.env`, private video, weights with incompatible licenses, or cloud credentials just because a tutorial uses a local directory.

## Preserve your learning

Keep `my_work/`, edited learner notebooks and existing progress JSON files before upgrading. Keep the evidence files those logs reference; a progress entry without its evidence does not establish reproducibility. Progress files remain self-recorded assessments and are not reset by the new course command.

Retained directories with names such as `sports_v8` and `industry` are source paths, not additional courses to repeat. Their primary routes are selected by the one catalog. Older generated reader aliases preserve links without adding another mandatory reading assignment.

The blank progress and answer templates are tracked separately from personal work. After checkout, run `uv run --no-sync python course.py init` to create only missing local progress records. The repository test suite was run successfully on a local `git archive` export; the remote CI matrix remains unexecuted.
