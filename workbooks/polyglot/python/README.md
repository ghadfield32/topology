# Python notebooks (57)

Each `.ipynb` here runs the **canonical Python reference** for one learning unit in a fresh
kernel inside an isolated copy of the source, then audits that lab's
registered inputs and one specific native run. It is not a Python
re-implementation of the native lab.

- **Index of all three languages:** [../index.html](../index.html) or [../README.md](../README.md)
- Go equivalents: [`../go/`](../go/)
- Rust equivalents: [`../rust/`](../rust/)
- Independent data and scientific checks: [`../../native/python/`](../../native/python/)
- Full repository map: [`../../docs/release/REPOSITORY_LAYOUT.md`](../../docs/release/REPOSITORY_LAYOUT.md)

## Run one

    uv run --no-sync jupyter nbconvert --to notebook --execute `
      --output-dir my_work/nb_run workbooks/polyglot/python/stage01.ipynb

Or open it in VS Code or JupyterLab and run the cells top to bottom.

To produce the reference result the notebook compares against:

    uv run --no-sync python course.py run --stage 1 --output my_work/stage01_ref01

## Where the Python code lives

Your own Python work belongs in the learner notebook produced by
`course.py practice`, not in the reference notebook.

These notebooks are **unassessed**, and they are not a second curriculum: the
31-stage route in `curriculum/catalog.json` remains the only required one.
