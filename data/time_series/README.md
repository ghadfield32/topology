# Historical annual observations for temporal reasoning

The file contains the 309 annual observations for 1700–2008 shipped in the installed statsmodels dataset snapshot. `YEAR` is the annual index and `SUNACTIVITY` is the supplied annual activity value. Values are preserved; the year column is written as integers. The source describes this dataset as public domain. Attribution, exact upstream package version and SHA-256 are in `manifest.json`.

Source: https://www.statsmodels.org/stable/datasets/generated/sunspots.html

This is not the latest or a newly corrected solar dataset. The source page uses slightly inconsistent wording about monthly files; the bundled file here is explicitly annual, and its shape and year range are verified. Do not reinterpret the decimal-valued activity measure as an exact integer count from an instantaneous image.

We use these real dated observations for lagged features and past-only confirmation logic. The teaching threshold is not an authoritative solar-event definition. Actual publication times, human-contact annotations, camera timestamps, and basketball events are not supplied. Annual sample-boundary availability is an explicit simplification. No forecasting or sports-event accuracy is claimed.

The CSV is bundled so statsmodels is NOT a runtime dependency for the course.
