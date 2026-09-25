# Poux’s 3D Spatial AI map — an optional course extension

**Current learner position: Stage 01. No restart.** This addition is based on the supplied Florent Poux article and LinkedIn post. It adds application pathways to the existing Listening to Shape course rather than creating a replacement curriculum. The 31 primary stages, five representation units, existing tests, source data, `uv.lock`, deployment files and progress records are unchanged.

Poux organizes the field as **Capture → Understand → Deliver**, with six named hubs. Keep that organization as the source map. His central lesson is to connect the pipeline: errors introduced at capture can become apparent structure in later products. This is a useful integration principle, not proof that every linked technique works for every scene.

## Read one map, then take one appropriate next step

| Source hub | Reuse from your course | New application work |
|---|---|---|
| P01 LiDAR & Point Cloud Processing | Stages 01, 02, 18 | Coordinate/data contracts, formats, chunking, sampling, spatial indexing, tile boundaries, geospatial fusion and terrain products |
| P02 3D Reconstruction | Stages 14–17 | Capture design, SfM/MVS, bounded COLMAP/Meshroom comparison, depth proposals, Gaussian splats and virtual-camera rendering |
| P03 Segmentation & Clustering | Stages 02, 05–11, 17 | Radius graphs, voxel aggregation, RANSAC, density clustering, geometric versus semantic segmentation |
| P04 3D Deep Learning | Stages 11, 16 and R01–R04 | Point-set networks, permutation properties, pointwise supervision, block preparation and scene-level splits |
| P05 Semantic & Spatial AI | Stages 16, 19, 29 and R01–R05 | 2D-to-3D feature grounding, reviewed labels, scene relations, OpenUSD and evidence-grounded queries |
| P06 Capture, Meshing & Visualization | Stages 05, 06, 10, 14, 15, 17, 18, 20 | Sensor selection, normals, scalar fields, meshing, topology/coverage checks, change detection and level-of-detail delivery |

These stage mappings are our integration decisions. They do not certify that the current core lessons completely teach each new hub. Foundational definitions remain owned by their existing stage; the extension supplies application questions and acceptance requirements.

## What was added, and what has not been implemented

- [Tutorial register](TUTORIALS.md): **37** distinct source-index links, in the author’s six groups, each with an original proposed learning outcome.
- [Six hub lesson plans](LESSONS.md): prerequisites, vocabulary, ordered practical work, evaluation, failure experiments, cross-sector transfer and completion gates.
- [Sources and limitations](SOURCES_AND_LIMITS.md): source-derived assertions versus independently checked documentation and our proposed guardrails.
- [Stage 01 bridge](#stage-01-bridge): executable weighted-chunk exercise using the **existing selected SPL motion records**, plus 20 isolated tests.
- [Verification](VERIFICATION.md): actual scope, results and instructions to reproduce them.

The hub plans are learning and implementation specifications, **not six completed software pipelines**. All 37 full-article reviews and the advanced experiments remain explicitly pending. No paid content is needed to run the bridge. No dependency installation, new data download, training, renderer, Docker build or cluster deployment was performed by this extension.

## Stage 01 bridge

The immediate connection is not “install every 3D library.” It is: **a set of records, a mathematical operation on those records, and the information that operation throws away.** Read the existing [Stage 01 primary lesson](../../../lessons/01_lesson.md) first.

Suppose batch A has `n` points and centroid `a`, while batch B has `m` points and centroid `b`. The combined centroid is

```text
c = (n*a + m*b) / (n+m).
```

It is generally **not** `(a+b)/2`. Work the exact example before coding: one point at x=0 and three points at x=3, 6, 9 have overall mean 4.5. The equally averaged batch means give 3. That is a weighting mistake, not floating-point noise.

From the repository root, after copying or merging this extension:

```powershell
uv run --no-sync python curriculum/extensions/poux_spatial_ai/test_bridge.py
uv run --no-sync python curriculum/extensions/poux_spatial_ai/bridge.py --repo . --output my_work/poux_bridge01
```

The bridge uses only Python’s standard library; it does not change the locked environment. `my_work/poux_bridge01` must not exist. The script checks the existing sports source against its existing manifest, refuses missing/unknown units and nonfinite coordinates, and saves `results.json`. It does **not** update learner status or register a new `course.py` case.

### Interpret the output correctly

The existing excerpt has 12 ball positions from **one selected trial**, not 12 independent trials and not a simultaneous static scan. The arithmetic centroid is over these selected rows. Their times are nonuniformly selected, so it is not a time average. Reversing the row order preserves the centroid while changing the ordering of motion. Pooling loses information.

The small JSON is loaded as a whole. The centroid accumulator is streamed, but this run is **not** evidence of out-of-core LAS processing or city-scale performance. No additional sports data are copied into this extension. Existing source terms and transcription limitations remain applicable.

### Your independent evidence file

Save a new `answer.md` in your output directory. Derive the two-batch formula, predict what changes when the second batch doubles in size, explain why reversing order does not affect the mean, and give a sports question the centroid cannot answer. Then replace chunk sizes 1+11 with another unequal partition and compare within a justified numerical tolerance.

Do not mark the exercise independently completed just because the supplied reference works. Reconstruct it without the answer after a delay.

## Learning order without duplicate introductions

1. Finish Stage 01; use the bridge once. At Stage 02, compare distances, scaling and neighborhood definitions.
2. Use P01 to acquire one bounded physical point cloud and one coordinate contract. Do not start with the largest downloadable tile.
3. Use P03’s geometric baseline before P04’s learned segmentation. P02 provides the alternative capture route for photos, after camera foundations.
4. Use P06’s sensor-selection subsection before capture; save its advanced meshing/viewing work until the geometric output is understood.
5. Add P04 and then P05 after labeled evaluation exists. Finish with one P06/P05 end-to-end capstone, not six disconnected demos.

The author’s hub numbering is preserved; this order is our prerequisite-aware execution route. Keep the existing course as the main route and return to its relevant primary lesson instead of copying definitions into another compulsory chapter.

## Repository and deployment boundaries

Copy this directory to `curriculum/extensions/poux_spatial_ai/` and add one link under the existing optional continuations in `curriculum/START.md`. A review branch/PR may contain that exact change. Do not overwrite the repository root, existing `MANIFEST.sha256`, data manifests, package constraints, Docker/Kubernetes settings, answers or progress files. Old release manifests remain historical baselines; deliberate new files should be recorded as additions rather than certified by old hashes.

For later large-data experiments, retain the existing native → container → disposable cluster acceptance sequence. CPU chunk processing, GPU reconstruction and model training are distinct jobs with distinct resource needs. Each should write a new run directory and record input hashes, coordinate versions, random seeds, parameters, peak memory, timings and failure evidence. A static YAML validation is not a completed Job; an index of tutorials is not proof of their execution.
