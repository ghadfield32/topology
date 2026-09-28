# Go notebooks (57)

Each `.ipynb` here compiles and runs the **real Go program** for one native learning unit.
Python is only the driver: it builds the binary, launches it, and compares
the result. The mathematics happens in Go.

- **Index of all three languages:** [../index.html](../index.html) or [../README.md](../README.md)
- Python equivalents: [`../python/`](../python/)
- Rust equivalents: [`../rust/`](../rust/)
- Reference source (read-only): [`../../native/go/`](../../native/go/)

## Run one

    uv run --no-sync jupyter nbconvert --to notebook --execute `
      --output-dir my_work/nb_run workbooks/polyglot/go/stage01.ipynb

Or open it in VS Code or JupyterLab and run the cells top to bottom.

To produce the reference result the notebook compares against:

    uv run --no-sync python native_course.py compare --lab stage01 --output my_work/stage01_go01

## Where the Go code lives

Two different places, and the difference matters:

| Path | Role |
|---|---|
| `native/go/` | the **reference** implementation, committed and read-only |
| `my_work/<session>/native/go/` | **your** editable copy, created by `prepare` |

To make changes that actually get compiled and tested:

    uv run --no-sync python native_course.py prepare --lab stage01 --output my_work/stage01_practice01

Then edit inside `my_work/stage01_practice01/go/`. Editing
`native/go/` changes the shared reference for every lab, which is not
the assignment.

These notebooks are **unassessed**, and they are not a second curriculum: the
31-stage route in `curriculum/catalog.json` remains the only required one.
