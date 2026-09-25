# Six connected hub lesson plans

**Source organization:** Florent Poux’s supplied six-hub index. **Everything labeled “our lab,” “gate,” or “transfer” below is an original course-integration proposal.** These are not summaries of 37 unseen full articles. Read each source through the [complete register](TUTORIALS.md) only when its prerequisite and question are relevant. Advanced labs below are not yet implemented or executed by this addition.

## Shared evidence contract — learn once, reuse in every hub

A point is not “just three numbers.” For each input record preserve the source asset/version, observation ID, coordinate frame, axis convention, horizontal/vertical units, timestamp/time base where relevant, acquisition type, validity/visibility mask, and measured/estimated/synthetic status. For geospatial work, also retain the coordinate reference system and vertical datum. Unknown metadata stays unknown rather than inferred from a plausible-looking plot.

For each run keep the selection, source hash, independent evaluation IDs, fitted preprocessing, all parameters, random seeds, output schema, metrics, coverage, warnings and code/environment versions. Use a new run folder. Split by independent scene, acquisition, athlete or event **before** creating overlapping blocks/windows. Proposed default gates below are logical checks; numeric accuracy tolerances must come from the actual application and data uncertainty, not from the tutorial’s promotional examples.

<a id="p01"></a>
## P01 — LiDAR & Point Cloud Processing

**Author’s role:** load, clean and script raw scans, including files too large for RAM. His named topics include representations, initial processing, system tools, geospatial integration, automation, city models and dataset selection. All seven links are in [P01’s register](TUTORIALS.md#p01).

**Reuse:** Stage 01 for weighted sums and linear maps; Stage 02 for distance; Stage 18 for memory/latency reasoning. Do not reread those as new subjects.

**New vocabulary.** A point record stores coordinates and attributes; a voxel is a cell in a declared spatial grid; a mesh specifies vertices and faces. LAS and compressed LAZ are point-cloud storage formats; E57 is another scan format and needs a compatible reader. Do not assume `laspy` reads every format. A terrain model describes selected ground elevations; a surface model may retain roofs or vegetation. Neither arises merely by renaming the same raster.

**Our lab, in order:**

1. Complete the Stage 01 bridge. Estimate coordinate storage by `N × dimensions × bytes per scalar`; treat additional copies, indexes and neighbors separately.
2. Select one small region from an AHN product using official metadata. Record the product/version, exact tile, bounding box, acquisition date, source terms and coordinate/vertical reference. No tile is bundled by this extension.
3. Inspect the header without reading all points. Read a bounded selection, inspect attributes and classification meanings, and preserve invalid/withheld flags.
4. Implement chunked counts, bounds and centroid. Compare with a whole-file result on a small file. Unequal batches require count weights. Record invalid records explicitly rather than silently discarding them.
5. Add a fixed-origin voxel sampler and a reproducible sample. Keep original point membership or a traceable summary for each voxel. Chunkwise downsampling must merge voxels that cross chunks.
6. Produce a small ground-elevation grid using declared ground labels or a separately evaluated classifier. Save empty-cell and point-count masks. Do not interpolate absent ground and label it measured.
7. Repeat over two adjacent tiles. Check duplicates and seams. Neighborhood algorithms need appropriate boundary handling; independent file chunks are not necessarily independent spatial neighborhoods.

**Baseline and gate:** whole-file versus chunked counts agree, coordinate summaries agree within stated floating-point tolerance, no hidden coordinate conversion occurs, and peak memory is actually measured. Count unmatched or uncovered grid cells. A later streaming pipeline must demonstrate bounded peak memory as input size grows; the small bridge does not establish that.

**Failure experiment:** use unweighted batch means, or mix two vertical references. Predict and display the resulting error before repairing it.

**Transfer:** terrain/flood mapping, crop canopy structure, industrial survey inventory, and sports court scans. A player’s time trajectory is not a terrain scan. **Independent question:** why can chunkwise DBSCAN give a different answer even when chunkwise counts and centroids agree?

<a id="p02"></a>
## P02 — 3D Reconstruction

**Author’s role:** turn photos into geometry when a scanner is unavailable. Preserve his classical photogrammetry, Meshroom, image-to-model, DepthAnything v2, zero-shot, semantic Gaussian-splatting and Blender-renderer branches.

**Reuse:** Stages 14–17 already own camera projection, units, measured stereo, learned-geometry candidates, registration and holdouts. This hub adds a full image-set workflow, not a second camera-matrix lesson.

**New vocabulary.** Structure from motion estimates scene/camera structure from correspondences. Multi-view stereo adds denser geometry using views and cameras. Monocular predicted depth incorporates learned assumptions; it is not an independent measured baseline. Gaussian splats are a rendering representation, not automatically a watertight surface. A synthetic renderer generates image observations under chosen geometry and camera assumptions.

**Our lab:**

1. Reproduce the existing measured-stereo control before installing another model. State exactly which reference supplied scale and where invalid disparity is excluded.
2. Capture a small static object or use an appropriately licensed image set. Reserve independent check distances/landmarks before fitting. Track blur, exposure, lens model, crop, overlap and image rejection.
3. Run one pinned COLMAP or Meshroom pipeline. Record keypoint/match statistics, registered and failed images, sparse and dense outputs, camera conventions and run costs. Do not compare two software runs with different input selection and call the difference an architecture effect.
4. Align to a measured frame only using the declared fit references. Evaluate on different references. Report distance error, reprojection error, coverage, scale stability and runtime separately. A lower reprojection error is not by itself a metre-accuracy certificate.
5. Compare one fixed monocular model or existing VGGT candidate under the same allowable evidence. Identify model, weights, code revision, image processing and license. Preserve original prediction and registered/refined variants.
6. Add a splat or Blender view as a separate deliverable. Use held-out cameras for appearance evaluation and independent geometric checks for measurement. Never optimize on evaluation views and present them as untouched.

**Gate:** fit/evaluation references are disjoint; coordinate conventions and units are explicit; failed views and uncovered regions are retained; no single-image result is called survey-grade merely because it looks convincing.

**Failure experiment:** double the arbitrary reconstruction scale, show that image reprojection can remain unchanged under the corresponding camera/scene similarity, and show which independent metric reference detects the error.

**Sports transfer:** reconstruct a static court/rim first. Then separate synchronized multi-view athlete/ball motion from the static background. Do not feed unsynchronized moving poses into a static-scene method and interpret its inconsistency as real anatomy. **Independent question:** what distinguishes scale recovery, world-frame orientation, and camera calibration?

<a id="p03"></a>
## P03 — Segmentation & Clustering

**Author’s role:** use geometric grouping and fitted primitives before deep learning. Retain all eight clustering, RANSAC, shape-detection, voxel and supervised-bridge tutorials.

**Reuse:** Stage 02 for metrics; Stages 05–10 for complexes and topology; Stage 11 for evaluation. A connected-component label, homology class and semantic object class are different things.

**Core derivation:** for a plane `n·x + d = 0` with unit normal `||n||=1`, point-to-plane distance is `|n·x+d|`. Without normalization the expression scales with the arbitrary coefficient magnitude. Three noncollinear points determine a plane; collinear samples are degenerate.

**Our lab:**

1. Begin with an explicitly generated room: floor, walls, objects, noise and missing regions. This supplies known controls, not measured performance.
2. Implement a radius-neighbor graph on a tiny example and its connected components. Demonstrate chaining: A near B and B near C does not require A near C.
3. Compare that graph grouping with K-means and DBSCAN on the same chosen features. State `k`, radius, minimum count, scaling, seed and unassigned-point policy. Cluster identifiers are arbitrary, not class names.
4. Fit a plane with RANSAC, recording threshold units, sample degeneracy, iteration count and consensus coverage. Compare with least squares under controlled outliers. The largest plane is not automatically the ground.
5. Remove only the selected plane support and cluster the remainder. Retain masks linking outputs to original point IDs. Vary threshold and sample density; a stable-looking render is not a sensitivity analysis.
6. Repeat on a bounded observed cloud after verifying its provenance. If no independent labels exist, report geometric diagnostics and review examples, not invented semantic accuracy.
7. For labeled scenes, use scene-level splits and map predictions to original evaluation points before calculating a confusion matrix, classwise IoU and coverage.

**Gate:** the pipeline recovers the declared synthetic controls within specified tolerances, rejects degenerate fits, reports unassigned points and evaluates any semantic claim against independent labels. Do not promise CPU runtime from a ten-line code listing.

**Failure experiment:** change point density without changing the object; show how fixed DBSCAN parameters alter labels. Then explain whether parameter adaptation is justified or is hiding a failure.

**Transfer:** buildings and vegetation, warehouse components, industrial pipes, court/floor segmentation. A planar cluster can be a floor, table or wall; semantics needs additional evidence. **Independent question:** why does grouping points by proximity not prove they are one physical object?

<a id="p04"></a>
## P04 — 3D Deep Learning

**Author’s role:** a network consumes unordered point sets and learns labels, with data preparation taking priority. The supplied index lists only two written tutorials in this hub; the broader paid/course materials are not assumed to be supplied.

**Reuse:** Stage 11 evaluation, Stage 16 attention basics, and R01–R04 representations and fitting. Add point-set structure rather than re-teaching every neural-network term.

**Core model:** apply a shared function to each point and aggregate with a symmetric operation such as max pooling: `g(X) = max_i h(x_i)`. Reordering input points does not change that global aggregate. For per-point outputs, the corresponding output rows should reorder with the input. Neither property automatically supplies rotation invariance or correct semantic labels. The original PointNet project is the primary reading.

**Our lab:**

1. Use a few generated objects to unit-test the input format and permutation behavior. Distinguish class labels for whole shapes from per-point labels.
2. Select a labeled physical-scene dataset only after reviewing its license, units, class definitions and acquisition groups. Keep entire scenes or acquisitions in one partition before constructing overlapping blocks.
3. Implement deterministic sampling and a padded-point validity mask. Fit normalization only on permitted fitting data. Record whether colors/normals/elevation are allowed inputs and how they are computed.
4. Train a small shared-MLP/max-pool baseline. Compare with geometric and ordinary-feature baselines on the same split; keep parameter-selection decisions out of the final test data.
5. Test point-order permutations, missing points, rotation, changed sampling density, scene boundaries and out-of-distribution objects. A test the model was not designed to pass remains a measured limitation, not automatically a software bug.
6. Evaluate at original-point or explicitly defined voxel resolution. Report class counts, classwise IoU, mean IoU, confusion, ignored labels, coverage, seeds and resource usage. Whole-shape accuracy is not segmentation mIoU.

**Gate:** padding does not affect loss or metrics, evaluation scenes never contribute fitted statistics, and permutation tests match the declared output type. A generated-object check is not held-out real-scene performance. The article’s “past 80 percent” example lacks enough detail to become our acceptance target.

**Transfer:** indoor space, industrial surfaces, agriculture, and sports scene objects. Do not expect a pretrained road-LiDAR network to work unchanged on inferred basketball RGB geometry. **Independent question:** can a global invariant embedding still discard information required for per-point prediction?

<a id="p05"></a>
## P05 — Semantic & Spatial AI

**Author’s role:** connect labels, relationships and language queries. Retain the SAM-3D, SAM/CLIP/DINO, labeling-GUI and scene-graph tutorial links. The exact identity of a method called “SAM 3D” must be checked from the linked article before installing a similarly named package.

**Reuse:** existing spatial calibration, Stage 19 temporal hypotheses, Stage 29 graph concepts, and representation units. CLIP-style text/image representations and an LLM response are not substitutes for measured coordinates.

**Our lab:**

1. Start with a small manually reviewed labeled scene. Give each object a stable ID; keep its supporting points, source views, frame/units, time, label confidence, visibility and human-review state.
2. Define relations before querying: distance between which primitives? What numeric criterion means “near”? Does “above” use a verified gravity direction? Is “inside” based on a closed volume or only a bounding box? Unknown evidence must produce unknown, not false certainty.
3. Calculate geometry deterministically and save the inputs behind every relation. A bounding-box overlap is only an overlap test, not a contact detector. Support/contact and safety questions require richer evidence.
4. Add one 2D-to-3D labeling route using saved intrinsics, extrinsics, depth and visibility. Test coordinate round trips, occluded points, conflicting views and unavailable classes. Human edits should be versioned separately from predictions.
5. Build the reviewed object/relation graph. Add a query interface that returns the relevant facts, their provenance and uncertainty before allowing an LLM to explain them. Keep language output separate from the authoritative evidence records.
6. Export to OpenUSD where helpful for scene description and composition. Distinguish this representation from a database of validated physical facts or a reasoning algorithm.

**Gate:** every answer can be traced to objects, observations and relation definitions; contradictory or missing evidence is exposed; prompt injection in captions/annotations is treated as data, not executable authority. Never use a tutorial prototype to certify an emergency exit or other safety-critical condition.

**Failure experiment:** translate one input cloud by 0.3 m without updating its frame record. Show how an apparent spatial relation changes, and identify the earlier provenance check that should prevent it. Then hide the crucial region and require the system to abstain.

**Sports transfer:** athlete–hand–ball–rim relations with identity and time. “Near hand” is not “held,” and “held” is not a verified release event. Reuse the existing observation/world-state ownership rather than creating a competing authoritative scene. **Independent question:** which relation evidence remains valid after a camera moves or the scene changes?

<a id="p06"></a>
## P06 — Capture, Meshing & Visualization

**Author’s role:** both capture choice and delivering a usable surface/view. Preserve his nine sensor, synthetic-room, mesh, change-detection and visualization links. Read capture planning before acquisition, but defer advanced rendering until the geometry is understood.

**Reuse:** Stages 05–06 for complexes and holes; 10 for uncertainty; 14–17 for geometry/registration; 18 for performance. Do not replace an uncertainty lesson with a prettier renderer.

**Our lab:**

1. Write a capture plan covering scale, surface reflectance/texture, occlusion, range, motion, calibration, synchronization, consent and independent check measurements. Compare scanner, stereo and photogrammetric routes as measurement processes, not merely file exporters.
2. Use the generated room from P03 to test normal estimation/orientation and missing surfaces. Then apply the same explicitly bounded process to observed data.
3. Compare at least two appropriate representations: raw points and a reconstructed surface, or two reconstruction parameter choices. For Poisson, inspect density/observed support and extrapolated regions rather than automatically trusting filled holes.
4. For marching cubes, first define the scalar volume, voxel spacing and isovalue. A list of XYZ points is not itself the complete scalar-field input. Keep real spatial spacing, including anisotropy, in exported vertices.
5. Inspect triangle degeneracy, boundary and nonmanifold edges, disconnected components, normals and observed-to-surface residuals. Only use closed-volume measurements when the closure and physical model are justified. Watertightness can be undesirable if a true opening was filled.
6. For change detection, align on independent stable references, compare common visible support, and retain registration/missingness uncertainty. New coverage is not automatically new structure. Show a no-change control with altered viewpoint.
7. Deliver a Blender view or a suitable point-cloud viewer. Record unit/axis conventions, level-of-detail policy, total storage, peak memory, first-useful-view latency and requested resolution. Do not turn a first coarse view into a claim that the complete dataset loaded instantly.

**Gate:** a displayed point or surface element can be traced to its observation or inference status; mesh topology and measurement errors are evaluated separately; viewer frame rate does not certify geometric accuracy. Runtime claims include hardware, data size and timing boundaries.

**Transfer:** crop/terrain change, factory inspection, indoor inventory, and static court/rim reconstruction. Keep fast moving players/ball outside a static-scene mesh unless time is modeled explicitly. **Independent question:** when does closing a mesh hole improve rendering but make a physical conclusion worse?

## One end-to-end capstone, not six isolated achievements

Choose a bounded observed scene whose access and usage rights are understood. Freeze a small input manifest and independent measurement/label protocol. Produce: (1) an audited input cloud; (2) a classical geometric baseline; (3) optional learned labels compared fairly; (4) reviewed objects/relations; (5) a surface/viewer; (6) a report with coverage, errors, uncertainty, performance and failures. Maintain raw versus estimated versus synthetic distinctions throughout.

A sports capstone may begin with a static court and known landmarks, then introduce synchronized slow motion before fast hand/ball interactions. This is a proposed future project, not a claim that the course’s 12 selected frames are sufficient for complete scene reconstruction.

For Kubernetes, first run one bounded job natively; freeze dependencies; compare its container result; then use a new Job/run ID on the existing disposable setup. Preserve and export PVC results before cleanup. Consider memory-bound tile processing, CPU segmentation, GPU model work and the viewer as separate resource classes. No cloud-scale performance or live-cluster acceptance is established by this document.
