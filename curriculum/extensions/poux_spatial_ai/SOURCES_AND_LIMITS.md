# Sources, audit, and scope

Prepared 25 September 2026. This addition is grounded in two supplied sources: Florent Poux’s **The Ultimate Guide for 3D Spatial AI (Sensors to Systems)**, a Medium export showing 7 July 2026, and the LinkedIn post introducing that map. It uses their **Capture → Understand → Deliver** framing and six hub names. The copied social-page navigation, unrelated account information and images are excluded.

## Source-derived versus added material

**Source-derived:** the six-hub order, 37 labels and links in the article’s explicit tutorial lists, tool names, example applications and the recommendation to learn geometric baselines before networks. The author says his wider collection contains 40+ tutorials and his book has 18 chapters. We do not invent titles for items absent from the supplied index.

**Original additions:** the stage mapping, per-tutorial learning outcomes, six implementation/evaluation plans, the evidence contract, sports/cross-sector transfer, and the weighted-centroid bridge and tests. These are not representations of full articles we have not read.

**Outside verification:** the primary documentation below was read to qualify implementation claims. These checks are explicitly additional to the supplied article. Linked tutorials, paid material and all suggested advanced pipelines remain unexecuted. The full supplied index was sufficient to register the source’s lessons, not to certify mastery or implementation of their detailed contents.

## Qualifications that should remain visible

| Statement/example in the supplied index | How the course handles it |
|---|---|
| Python tools stream huge clouds so they do not fill RAM. | `laspy.read` reads the whole file; `laspy.open` plus its chunk iterator supports bounded reading. Downstream algorithms and temporary copies can still exhaust memory. Test the actual pipeline. [D1, D2] |
| A photographic orbit yields a metric, survey-grade cloud. | Reconstructed shape, metric scale and independent measurement accuracy are separate requirements. COLMAP documents registration to a target frame using 3D correspondences; point/image count alone is not scale or accuracy evidence. [D3] |
| RANSAC plus DBSCAN yields meaningful parts in seconds and roughly ten lines. | Useful baseline proposal, not a universal runtime or semantic-accuracy guarantee. Plane support and proximity clusters need scene/label interpretation. DBSCAN’s parameters and neighborhood memory matter. [D2] |
| A plain network exceeds 80 percent on held-out tiles. | The supplied index does not specify the metric, exact split, class mapping or complete protocol needed to reproduce that number. Record it as the author’s example, not our target or result. PointNet’s documented contribution concerns point-set inputs and tasks, not universal accuracy. [D4] |
| Open-vocabulary scene queries remove a fixed class list and can answer safety-related questions. | Retain this as an application direction. Labels and spatial relations still require grounding, uncertainty, reviewed evidence and appropriate validation. A language response is not a safety certification. OpenUSD describes/organizes scene data; it does not independently certify physical facts. [D5] |
| Poisson or marching cubes produces a watertight usable surface. | Poisson can extrapolate beyond support; inspect density and missing data. Marching cubes requires a defined scalar field. Surface closure, topology, and measurement accuracy require separate checks; true openings should not be filled merely to satisfy a rendering preference. [D6] |
| Very large clouds are served in under a second; Rust may be 100x faster. | These are the author’s reported examples without a complete benchmark protocol in the supplied index. Do not adopt them as expected performance. Define data size, hardware, cold/warm cache, LOD and timing boundaries. |
| All tools/content can be approached through an open Python workflow. | Open-source code, downloadable data, model-weight rights, free articles and paid instruction are distinct. Check the exact artifact’s terms; no blanket free-access/commercial-use assertion is made. |

This table does not silently rewrite the source. It separates its motivating narrative from the conditions needed to support our own quantitative or operational claims.

## Primary documentation read for this addition

- **D1 — laspy, Basic Manipulation:** https://laspy.readthedocs.io/en/latest/basic.html . Whole-file reading versus metadata-only opening and chunk iteration. Use this for the correct I/O route, not as proof that downstream operations are streaming.
- **D2 — Open3D, Point cloud tutorial:** https://www.open3d.org/docs/release/tutorial/geometry/pointcloud.html . Voxel downsampling, normals, DBSCAN and plane segmentation. Read parameter definitions and memory notes before choosing input size.
- **D3 — COLMAP, FAQ:** https://colmap.github.io/faq.html . Camera models, known calibration and geo-registration to a target frame. Version-specific commands belong in the eventual pinned experiment.
- **D4 — PointNet original project:** https://web.stanford.edu/~rqi/pointnet/ . Unordered point-set classification/segmentation. Shared per-point processing and symmetric pooling motivate the permutation checks; do not infer arbitrary rotation invariance.
- **D5 — OpenUSD introduction:** https://openusd.org/release/intro.html . Scene description and composition. Keep semantic evidence and language reasoning as explicitly separate layers.
- **D6 — Open3D, Surface reconstruction:** https://www.open3d.org/docs/release/tutorial/geometry/surface_reconstruction.html . Normals, Poisson reconstruction and density/support diagnostics.

These are free-to-read documentation/project references, not copies of paid course content. Access to the 37 linked Medium full articles was not independently checked. Their exact source-index labels and links remain in [TUTORIALS.md](TUTORIALS.md).

## Data selection and acquisition status

| Path | Current availability | Appropriate work | Do not claim |
|---|---|---|---|
| Existing SPL selected frames | Already present in `sports_v8/data/`; reused by the new bridge | Unit conversion, weighted statistics, record identity and information lost by pooling | Full sports dataset, static scene scan, uniform-time average, reliable release point, new athlete validation |
| Existing measured-stereo example | Already in the course; not rerun by this addition | Reuse stages 15–18 for projection, scale, registration, mask and uncertainty before new reconstruction | A new COLMAP or monocular-model benchmark |
| AHN product/tile | Suggested by the article; no payload acquired here | Inspect official metadata, choose a bounded region, then point processing/terrain work | That AHN4 is the newest available campaign or a tile/vertical datum/license was verified here |
| A small labeled indoor/industrial scene | Selection and terms still required | Geometric baseline, supervised labels, per-scene split, graph and mesh validation | That an unlabeled cloud supports measured semantic accuracy |
| User-captured static court/object | Optional future capture with consent and independent references | Static reconstruction, surface quality and relation grounding, then synchronized dynamics later | That a single phone sweep is automatically calibrated or metric |
| Generated room/point controls | Future original controls under a declared generator/seed | Hand-checkable primitives, invariances and known failure cases | Observed physical performance or domain generalization |

The AHN viewer is an acquisition starting point, not an included dataset: https://www.ahn.nl/ahn-viewer . Choose actual product, region, datum, units, terms and size before downloading. No large automatic acquisition is added to daily course commands.

The SPL source manifest explicitly labels the existing file a selected numeric transcription and states that independent remote byte equality was not executed. The bridge validates that local file against the course manifest and preserves this limitation in its output. It does not certify source authenticity beyond that local continuity check.

## Implementation and environment boundary

Only `bridge.py` is a new executable teaching example here; it uses the standard library and existing data. No `uv.lock`, package constraints, Docker image, Kubernetes resource or `course.py` registry is altered. The core remains on the user’s working v12 installation. New dependencies for LAS/LAZ, E57, PDAL, Open3D, COLMAP, model weights or viewers require separate platform-compatible resolution and acceptance when their specific lab is implemented.

Native unit tests do not establish container or cluster behavior. Existing successful deployment evidence belongs to the existing repository, not to unbuilt future PointNet/reconstruction jobs. Preserve independent artifacts and the existing authoritative WMS state if a later learning experiment is promoted into an application.
