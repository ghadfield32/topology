# Listening to Shape v7 build plan

## Goal
Deliver the complete v6 course plus a beginner entry guide for each of 31 stages, two new directly sourced industry datasets, and explicit uncertainty/leakage/source-claim laboratories. Preserve the earlier source framing and progress logs. New experiments are original educational additions, not reproductions of papers or verified deployments.

## Architecture
Reuse `shape_lab` and all v6 notebooks. Add small `shape_lab.evidence_v7` utilities for canonical numeric fingerprints, stage mapping, split audits and finite-sample calibration. New cases live outside the eight-case v6 catalog to retain backward compatibility. The v7 reader links earlier rendered assets and uses system fonts only. Every bundled data source has an acquisition record; text retrieved via the web tool is not misrepresented as a byte-identical binary download.

## Task sequence and checks
1. Run the inherited test suite and retain its failures/skips. Confirm archive paths are safe.
2. Preserve complete UCI Seeds and Concrete Slump numeric tables, record units and unknowns, license, DOI, rows and column roles. Compare dimensions and class counts with source; allow opt-in remote numeric verification, never silent overwrite.
3. Write failing tests for `canonical_numeric`, `conformal_radius`, `overlap_report`, and source identity checks. Implement and rerun the full suite.
4. Add original beginner lessons and four lab/answer pairs: Seeds, Concrete Slump, leakage stress tests, and claims-versus-evidence. Execute all eight new reference notebooks in fresh kernels.
5. Give all 31 retained stages one plain-language prerequisite check, fully explained small example, runnable check, exact primary assignment link and misconception repair route.
6. Re-execute inherited notebooks in this environment, distinguish preserved historical reports from new verification, build the offline entrypoint, and check links.
7. Test a separately extracted final ZIP, verify file manifest and report exact results and unresolved limitations.

## Review focus
Dataset row order is not an assumed participant ID or timestamp. Synthetic copies are stress tests, not new observed people. A calibration radius uses the ceiling rank with an explicit infinity case. A stable diagram is not evidence of physical validity. Source-provider documentation can omit units; missing units remain unresolved. Old learning records are not rewritten or auto-assessed. No model weights, fonts, restricted sports data or third-party textbooks are bundled.
