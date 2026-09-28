# Rust notebooks (57)

Each `.ipynb` here compiles and runs the **real Rust program** for one native learning unit.
Python is only the driver: it builds the binary, launches it, and compares
the result. The mathematics happens in Rust.

- **Index of all three languages:** [../index.html](../index.html) or [../README.md](../README.md)
- Python equivalents: [`../python/`](../python/)
- Go equivalents: [`../go/`](../go/)
- Reference source (read-only): [`../../native/rust/`](../../native/rust/)

## Run one

    uv run --no-sync jupyter nbconvert --to notebook --execute `
      --output-dir my_work/nb_run workbooks/polyglot/rust/stage01.ipynb

Or open it in VS Code or JupyterLab and run the cells top to bottom.

To produce the reference result the notebook compares against:

    uv run --no-sync python native_course.py compare --lab stage01 --output my_work/stage01_rust01

## Where the Rust code lives

Two different places, and the difference matters:

| Path | Role |
|---|---|
| `native/rust/` | the **reference** implementation, committed and read-only |
| `my_work/<session>/native/rust/` | **your** editable copy, created by `prepare` |

To make changes that actually get compiled and tested:

    uv run --no-sync python native_course.py prepare --lab stage01 --output my_work/stage01_practice01

Then edit inside `my_work/stage01_practice01/rust/`. Editing
`native/rust/` changes the shared reference for every lab, which is not
the assignment.

These notebooks are **unassessed**, and they are not a second curriculum: the
31-stage route in `curriculum/catalog.json` remains the only required one.
