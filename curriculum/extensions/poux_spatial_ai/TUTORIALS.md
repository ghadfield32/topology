# All 37 tutorials explicitly listed in the supplied map

Attribution: Florent Poux, **The Ultimate Guide for 3D Spatial AI (Sensors to Systems)**, supplied Medium export dated 7 July 2026, and its accompanying LinkedIn post. Extracted 25 September 2026.

The author says he has written **40+** tutorials. The supplied article has **37 distinct links inside its six “In this part” lists**: 7 + 7 + 8 + 2 + 4 + 9. We preserve every one; we do not invent the unlisted remainder. Link labels below are exactly the labels in the index, not independently checked article titles.

**Review status:** the complete supplied index and post were read. Linked full articles, videos, paid courses and the book have not been read or executed as part of this addition. Some linked resources may require a subscription. “Catalogued” does not mean “completed,” “free,” “implemented,” or “validated.”

Each proposed outcome below is our curriculum addition, not a claim about all contents of the linked article. All tutorials start as **catalogued / full-text review pending / learner unassessed**.

<a id="p01"></a>
## P01 — LiDAR & Point Cloud Processing
Reuse existing stages: 01, 02, 18. See [the hub lesson plan](LESSONS.md#p01).

| ID | Source-index lesson label and link | Proposed independent outcome |
|---|---|---|
| P01.01 | [Representing 3D data](https://medium.com/data-science/how-to-represent-3d-data-66a0f6376afb) | Compare point, voxel and mesh records; preserve attributes and observation identity. |
| P01.02 | [Point cloud processing in Python](https://medium.com/data-science/discover-3d-point-cloud-processing-with-python-6112d9ee38e7) | Inspect one small physical cloud; state units and axes before displaying it. |
| P01.03 | [3D data science systems and tools](https://medium.com/data-science/ultimate-guide-3d-data-science-systems-and-tools-e92aaa8185eb) | Write the input/output contract for a complete, bounded run. |
| P01.04 | [3D geospatial data integration](https://medium.com/data-science/3d-spatial-data-integration-with-python-7ef8ef14589a) | Align vector, raster and point data using declared CRS, horizontal and vertical units. |
| P01.05 | [Automating LiDAR processing](https://medium.com/data-science/how-to-automate-lidar-point-cloud-processing-with-python-a027454a536c) | Implement bounded processing and compare chunked versus whole-file results. |
| P01.06 | [LiDAR city models in Python](https://medium.com/data-science/3d-python-workflows-for-lidar-point-clouds-100ff40e4ff0) | Compare ground classification, terrain grid and missing-cell coverage across tiles. |
| P01.07 | [Free LiDAR datasets](https://medium.com/data-science/free-lidar-datasets-for-self-driving-cars-ai-applications-50771284daf8) | Select one named acquisition with source date, terms, point count and coordinate metadata. |

<a id="p02"></a>
## P02 — 3D Reconstruction
Reuse existing stages: 14–17. See [the hub lesson plan](LESSONS.md#p02).

| ID | Source-index lesson label and link | Proposed independent outcome |
|---|---|---|
| P02.01 | [Reconstruction with photogrammetry](https://medium.com/data-science/the-ultimate-guide-to-3d-reconstruction-with-photogrammetry-56155516ddc4) | Separate feature matching, camera estimation, triangulation, densification and validation. |
| P02.02 | [Python and Meshroom](https://medium.com/data-science/3d-reconstruction-tutorial-with-python-and-meshroom-2aa37805ab4a) | Reproduce one bounded photogrammetry job; record all inputs and failed images. |
| P02.03 | [3D models from images](https://medium.com/data-science-collective/how-to-generate-3d-models-from-images-with-python-b92b7d549801) | Compare representation types and outputs before choosing a reconstruction pipeline. |
| P02.04 | [DepthAnything v2: 2D to 3D](https://medium.com/data-science-collective/depthanything-v2-tutorial-how-to-convert-2d-images-to-3d-models-with-python-2708d295b7e5) | Distinguish relative depth, model-predicted metric depth and measured scale. |
| P02.05 | [Zero-shot 3D from any image](https://medium.com/data-science-collective/how-to-create-3d-models-from-any-image-with-ai-zero-shot-3d-reconstruction-21d3023ad81b) | Preserve single-view ambiguity and separate visible observations from completion hypotheses. |
| P02.06 | [Semantic 3D Gaussian splatting](https://medium.com/data-science-collective/from-images-to-semantic-3d-gaussian-splatting-with-python-complete-guide-ff9d3d240847) | Evaluate appearance, geometry and labels independently in a splat representation. |
| P02.07 | [Multi-view renderer with Blender](https://medium.com/data-science-collective/how-to-build-a-multi-view-3d-renderer-with-python-blender-3d-gaussian-splatting-100-automated-ce634bae22d8) | Record virtual camera transforms and distinguish rendered supervision from observed images. |

<a id="p03"></a>
## P03 — Segmentation & Clustering
Reuse existing stages: 02, 05–11, 17. See [the hub lesson plan](LESSONS.md#p03).

| ID | Source-index lesson label and link | Proposed independent outcome |
|---|---|---|
| P03.01 | [Clustering high-dimensional clouds](https://medium.com/data-science/fundamentals-to-clustering-high-dimensional-data-3d-point-clouds-3196ee56f5da) | Choose features and a metric before clustering; test scaling and sampling sensitivity. |
| P03.02 | [Clustering with K-means](https://medium.com/data-science/3d-point-cloud-clustering-tutorial-with-k-means-and-python-c870089f3af8) | Compare a fixed-k baseline with the geometry and imbalance of the actual scene. |
| P03.03 | [Clustering with graph theory](https://medium.com/data-science/3d-clustering-with-graph-theory-the-complete-guide-38b21b1c8748) | Build a radius graph and connected components; explain chain connectivity. |
| P03.04 | [Model fitting with RANSAC](https://medium.com/data-science/3d-model-fitting-for-point-clouds-with-ransac-and-python-2ab87d5fd363) | Fit a plane with an explicit residual, threshold, sample degeneracy check and holdout. |
| P03.05 | [Indoor shape detection](https://medium.com/data-science/3d-point-cloud-shape-detection-for-indoor-modelling-70e36e5f2511) | Test geometric primitives on a room without equating a plane to a semantic class. |
| P03.06 | [Automating voxel modelling](https://medium.com/data-science/how-to-automate-voxel-modelling-of-3d-point-cloud-with-python-459f4d43a227) | Voxelize with a fixed origin, cell size, aggregation and provenance mapping. |
| P03.07 | [Automating segmentation and clustering](https://medium.com/data-science/how-to-automate-3d-point-cloud-segmentation-and-clustering-with-python-343c9039e4f5) | Compose plane extraction and density clustering; retain rejected and unassigned points. |
| P03.08 | [Semantic segmentation 201](https://medium.com/data-science/3d-machine-learning-course-point-cloud-semantic-segmentation-9b32618ca5df) | Define supervised targets, reference labels and scene-level evaluation before fitting. |

<a id="p04"></a>
## P04 — 3D Deep Learning
Reuse existing stages: 11, 16; R01–R04. See [the hub lesson plan](LESSONS.md#p04).

| ID | Source-index lesson label and link | Proposed independent outcome |
|---|---|---|
| P04.01 | [Towards 3D deep learning: ANN with Python](https://medium.com/towards-artificial-intelligence/towards-3d-deep-learning-artificial-neural-networks-with-python-efcd4a0b1165) | Derive a small shared pointwise network and inspect its input/target dimensions. |
| P04.02 | [3D deep learning tutorial: PointNet data preparation](https://medium.com/data-science/3d-deep-learning-python-tutorial-pointnet-data-preparation-90398f880c9f) | Split by scene before blocking; document sampling, masks, statistics and class mapping. |

<a id="p05"></a>
## P05 — Semantic & Spatial AI
Reuse existing stages: 16, 19, 29; R01–R05. See [the hub lesson plan](LESSONS.md#p05).

| ID | Source-index lesson label and link | Proposed independent outcome |
|---|---|---|
| P05.01 | [Segment Anything 3D for point clouds](https://medium.com/data-science/segment-anything-3d-for-point-clouds-complete-guide-sam-3d-80c06be99a18) | Identify the exact method named SAM 3D; do not assume similarly named packages coincide. |
| P05.02 | [Turn video into smart 3D models with SAM, CLIP and DINO](https://medium.com/data-science-collective/turn-video-into-smart-3d-models-the-python-guide-with-sam-clip-and-dino-f4878d4c37dc) | Trace image masks and embeddings through calibrated projection and visibility into 3D. |
| P05.03 | [How to build a Python GUI for 3D scene labeling](https://medium.com/data-science-collective/how-to-build-a-python-gui-for-3d-scene-labeling-49dd43624a7f) | Record human edits, object IDs, ambiguity and review state without overwriting raw evidence. |
| P05.04 | [Build 3D scene graphs for spatial AI LLMs](https://medium.com/data-science-collective/build-3d-scene-graphs-for-spatial-ai-llms-from-point-cloud-python-tutorial-c5676caef801?sk=1f1971d675dfde527336a8af0a269793) | Build auditable object and relation records; distinguish scene description from reasoning. |

<a id="p06"></a>
## P06 — Capture, Meshing & Visualization
Reuse existing stages: 05, 06, 10, 14, 15, 17, 18, 20. See [the hub lesson plan](LESSONS.md#p06).

| ID | Source-index lesson label and link | Proposed independent outcome |
|---|---|---|
| P06.01 | [Complete sensor guide](https://medium.com/towards-artificial-intelligence/3d-scanning-your-complete-sensor-guide-de393e1f23f4) | Compare sensor measurement principles and error budgets for the intended task. |
| P06.02 | [11 methods for 3D scanning](https://medium.com/data-science/11-methods-and-hardware-tools-for-3d-scanning-and-data-capture-28083b8377f8) | Choose capture based on scale, surface properties, occlusion, motion and access. |
| P06.03 | [Synthetic point cloud rooms](https://medium.com/data-science-collective/how-to-generate-synthetic-3d-point-cloud-rooms-with-python-05b49a6339d3) | Generate controlled rooms with known truth; mark every generated sample as synthetic. |
| P06.04 | [5-step mesh generation](https://medium.com/data-science/5-step-guide-to-generate-3d-meshes-from-point-clouds-with-python-36bad397d8ba) | Estimate/orient normals and compare surface reconstruction against observed support. |
| P06.05 | [Point clouds into meshes](https://medium.com/data-science/transform-point-clouds-into-3d-meshes-a-python-guide-8b0407a780e6) | Construct an explicit scalar field before marching cubes; vary spacing and threshold. |
| P06.06 | [Smart change detection](https://medium.com/data-science-collective/smart-3d-change-detection-python-tutorial-for-point-clouds-0dfd9945eb6a) | Check registration, coverage and uncertainty before attributing differences to change. |
| P06.07 | [Real-time visualisation](https://medium.com/data-science/guide-to-real-time-visualisation-of-massive-3d-point-clouds-in-python-ea6f00241ee0) | Profile level-of-detail rendering, memory and first-useful-view latency separately. |
| P06.08 | [No-code visualisation](https://medium.com/data-science/learn-to-visualize-massive-point-clouds-3d-mesh-with-no-code-tools-1835dd4be37f) | Inspect a cloud with an independent viewer while retaining reproducible processing. |
| P06.09 | [The Blender rendering handbook](https://medium.com/data-science/the-blender-handbook-for-3d-point-cloud-visualization-and-rendering-1700ebe69c7b) | Create useful renders without letting visual quality substitute for measurement validation. |

## Related resources, not additional counted tutorials

- [Author’s master map](https://learngeodata.eu/3d-spatial-ai-python-complete-guide/) and [free mission](https://learngeodata.eu/free-mission/). “Free mission” is the label used by the author; registration and current access conditions have not been checked.
- [3D Data Science with Python book](https://learngeodata.eu/book). The author’s comment mentions 18 chapters; no chapter titles or full book text were supplied. This is optional, not a requirement to continue the free course.
- Provider programs linked by the author: [Point Cloud Intelligence](https://learngeodata.eu/point-cloud-intelligence-course-description/), [Applied Semantic Segmentation](https://learngeodata.eu/applied-semantic-segmentation-course-description/), [3D Deep Learning OS](https://learngeodata.eu/3d-deep-learning-os-course-description/), [Orchestrating Spatial Agents](https://learngeodata.eu/spatial-agents-course-description/). Access/cost unverified; not bundled.

Primary open documentation alternatives and methodological qualifications are in [Sources and limits](SOURCES_AND_LIMITS.md). No article images, full articles, book chapters, account information or participant payloads are redistributed here.
