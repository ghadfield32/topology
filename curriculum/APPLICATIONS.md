# Apply one idea in another industry

Do not run every case before learning the foundations. Choose the observation type that matches your question, finish one baseline, then compare the topological or geometric extension. A new dataset is a new scientific context, not permission to reinterpret its units.

| Domain | Case / data card | Important observation distinction |
|---|---|---|
| Healthcare | [Image-summary classification](../industry/lessons/wdbc.md) | Feature records are not raw clinical images or a deployment validation cohort. |
| Food chemistry | [Wine cultivars](../industry/lessons/wine.md) | Cultivar label is not a taste or quality score. |
| Manufacturing | [Plant process measurements](../industry/lessons/stackloss.md) | Twenty-one days are not a large independent manufacturing benchmark. |
| Business | [Firm-year panel](../industry/lessons/grunfeld.md) | Firm identity and time both matter for splitting. |
| Environment | [Historical CO₂](../industry/lessons/co2.md) | Missing weekly slots are not measured values. |
| Water | [Annual Nile measurements](../industry/lessons/nile.md) | A change point alone does not establish a cause. |
| Marine climate | [Sea-surface temperatures](../industry/lessons/elnino.md) | A scalar historical series is not a full atmospheric field. |
| Transportation | [Traveler choice sets](../industry/lessons/modechoice.md) | Alternatives belong to the same traveler and must stay together. |
| Agriculture | [Seed geometry](../applications_v7/seeds/lesson.md) | Feature-space topology is not a physical hole in a kernel. |
| Materials | [Concrete mixtures and uncertainty](../applications_v7/concrete_slump/lesson.md) | Split calibration data from fitting and evaluation data. |
| Handwriting | [Representation comparison](../lessons/11_lesson.md) | A now-exposed demonstration test set is not a new holdout. |
| Stereo vision | [Measured reconstruction](../lessons/15_lesson.md) | Pixels, disparity and metric depth require explicit conventions. |
| Solar activity | [Temporal analysis](../sessions/19_session.md) | Later confirmation is not live detection at onset. |
| Material response | [Copper measurements](../physics/lessons/21.md) | A measured response is not automatically a governing differential equation. |
| Basketball biomechanics | [SPL units and motion](../sports_v8/lessons/S00.md) | Selected frames from one trial are not independent athlete outcomes. |
| Soccer profiles | [Profile topology](../sports_v8/lessons/S03.md) | Aggregate profiles are not pitch trajectories. |
| Modern basketball metadata | [ACB readiness](../sports_v9/lesson.md) | Ten sample games are not all covered season games or tracking frames. |

## Open data does not mean unlimited rights or complete coverage
Read the [retained data catalogue](../docs/v7/DATA_CATALOG.md), [modern sports plans](../docs/v8/SPORTS_DATASETS.md), [ACB data card](../sports_v9/DATA_CARD.md), and [optional cross-industry plans](../docs/v6/OPTIONAL_DATA.md). A plan is not an acquired dataset. The exact filenames are also reachable through the reader's all-materials library.

For video, wearables, motion capture, medical or industrial systems, define the task before selecting the newest source. Preserve participant identity for grouping, but do not use identifiers as predictive features without a justified task. Respect dataset-specific noncommercial and other restrictions before using any examples in a product.

The original small hand-derived controls remain essential: they distinguish a software defect from a surprising real-data result. Synthetic and manufactured examples are labeled and never counted as observed sources.


## Latest basketball source check

Read the [v9 sports update](../docs/v9/SPORTS_UPDATE.md) for the verified ACB metadata boundary and the larger tracking acquisition plan.


[Exact square explorer](../reference/square_explorer.html) · [Historical browser progress widget](../site/progress.html). The historical widget uses separate local browser storage and is not synchronized with the evidence-backed CLI log.


## Representation-learning continuation (v11)

These five units reuse the established mathematical/data foundations instead of repeating a second core course. Read them in order after their stated prerequisites.

| Unit | Primary lesson | Experiment key |
|---|---|---|
| R01 | [Distributions, covariance, and whitening](../representations/lessons/R01.md) | `r01` |
| R02 | [Characteristic functions, projections, and SIGReg](../representations/lessons/R02.md) | `r02` |
| R03 | [Agreement, collapse, and SSL mechanisms](../representations/lessons/R03.md) | `r03` |
| R04 | [Real-image training and independent evaluation](../representations/lessons/R04.md) | `r04` |
| R05 | [Sports and cross-industry transfer](../representations/lessons/R05.md) | `r05` |

Use the [terminology map](../representations/TERMINOLOGY.md) for acronym lookup and the [source audit](../representations/SOURCE_AUDIT.md) for supplied claims versus verified qualifications. The optional [Kubernetes lesson](../docs/release/KUBERNETES.md) is deployment practice, not a prerequisite for topology.
