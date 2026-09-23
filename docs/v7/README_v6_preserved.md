# Listening to Shape Learning System v6

Open **START_HERE.html** after extracting the full ZIP. This version includes the entire 31-stage course plus eight parallel real-data industry cases. It is an original learning companion, not the actual book or an endorsed course.

[Start and preserve your work](../v6/START.md) · [Included data](../v6/DATA_CATALOG.md) · [31-stage transfer map](../v6/STAGE_MAP.md) · [Optional larger datasets](../v6/OPTIONAL_DATA.md) · [Coverage](../v6/COVERAGE.md) · [Verification](../v6/VERIFICATION.md).

Read without installing anything. To execute the new CPU industry cases, create an environment and install `python -m pip install -e ".[notebooks,test,reader]"`. Install the `physics` extra for all older neural examples. Then run `python scripts/industry.py verify`, `python -m pytest -q -ra`, and `python -m jupyterlab`. Full Mac/Linux/Windows instructions are in the start guide.

The core evidence file remains `progress/learning_log_v5.json` (same 31-stage schema). The new optional cases use `progress/industry_log_v6.json`. Preserve both and their evidence files during upgrades. Empty supplied logs do not replace your work.

All legacy guides and reports are retained as historical records. The authoritative current status is `docs/v6/VERIFICATION.md`; older version numbers refer to earlier snapshots, not extra unassessed work. Optional datasets are plans, not hidden downloads. See each dataset's own license rather than assuming the course's code license covers all data.
