# Stage 18 guided session — Separate throughput from how old the answer is

**Role:** Original v4 teaching supplement. It deepens the preserved lesson; it does not replace the book or its unavailable full text.

**Read first:** [Stage lesson](../lessons/18_lesson.md), then use this explanation before the [consolidation notebook](../consolidation/18_lab.ipynb). The [original workbook](../workbooks/18_workbook.md) and [worked lab](../notebooks/18_lab.ipynb) remain available. Repair earlier concepts only where needed; do not restart the whole course.

**Data and evidence:** Real reference point table for measured CPU operations; separate deterministic FIFO simulation.

## What you will be able to demonstrate

1. Preserve numerical outputs while changing an implementation.
2. Distinguish measured code duration from simulated queue latency.
3. Derive queue growth when service is slower than arrival.
4. Report warm-up, work units, and timing boundaries.

## Time the path you actually claim
Throughput is completed work per unit time. Latency is elapsed time for a particular item between named boundaries. Result age is how old the source observation is when its result is used or displayed. A pipeline can have high throughput and still show stale results because work waits in a queue or because batches delay individual observations.

Before timing anything, specify the work item: an image, a frame pair, a point table, or a batch. Specify whether timing includes capture, decode, preprocessing, transfer, model execution, synchronization, serialization, and display. A CPU array operation is not a benchmark of the entire video pipeline.

## Preserve the answer before optimizing it
The real stereo reference generates a point table. Apply one rigid transform using a Python loop and using matrix operations. Compare the resulting coordinates first. Timing a faster but incorrect transformation is not an optimization of the same calculation.

Warm each implementation, then time several repetitions and record the median. The exact numbers depend on hardware, runtime, process contention, and array size. This small benchmark is illustrative. It does not establish performance on your Mac, Windows desktop, GPU, or ROS2 pipeline.

## Derive a queue example
Suppose observations arrive every 0.02 seconds but each takes 0.03 seconds to process on one FIFO server. The first item finishes at 0.03 seconds with latency 0.03. The second arrives at 0.02, waits until 0.03, and finishes at 0.06 with latency 0.04. Each item adds another 0.01 seconds of backlog. By the hundredth item, latency is 1.02 seconds.

This is a constructed deterministic simulation, not a measured camera benchmark. It explains why a model's isolated service time is insufficient to assess a live system. Dropping work, replacing stale queued items, parallel processing, or lowering the incoming rate are different policies with different completeness and ordering consequences. They should not be silently exchanged in a benchmark.

## Carry the evidence forward
A timing report should name the input size, repetitions, warm-up, clock, device, and boundary. A latency report should retain observation timestamps and report queue age and drops as well as summary percentiles. Optimizations should be compared on the same numerical and temporal contract.

The original performance sources motivate profiling; their reported measurements are not results of this course. This notebook records only the small CPU transformation it executes and the FIFO example it simulates. Keeping those labels separate is part of learning accurate systems engineering.

## Predict, execute, and explain

### Step 1

Compare two implementations on a point table derived from real reference data.

```python
from shape_lab.stereo import reference_sample, point_cloud
from shape_lab.geometry import exp_so3
from time import perf_counter
_, _, disparity, calibration = reference_sample()
X, _ = point_cloud(disparity, calibration, stride=20)
rotation = exp_so3([.1,.2,.3]); translation = np.array([.2,0.,-.1])
def loop_transform():
    return np.array([rotation @ p + translation for p in X])
def array_transform():
    return X @ rotation.T + translation
assert np.allclose(loop_transform(), array_transform())
```

### Step 2

Measure only the CPU coordinate transformation, with warm-up and repeated runs.

```python
loop_transform(); array_transform()
timings = {}
for name, operation in [('loop', loop_transform), ('array', array_transform)]:
    durations = []
    for _ in range(7):
        start = perf_counter(); operation(); durations.append(perf_counter()-start)
    timings[name] = float(np.median(durations))
print('median CPU seconds:', timings)
```

### Step 3

A separate FIFO simulation demonstrates backlog. It is not relabeled as measured latency.

```python
from shape_lab.temporal import fifo_latencies
arrival = np.arange(100)*.02
latency = fifo_latencies(arrival, np.full(100,.03))
assert np.isclose(latency[0], .03)
assert np.isclose(latency[-1], 1.02)
result = {'points': len(X), 'median_cpu_transform_seconds': timings,
          'timing_boundary': 'in-memory CPU transform only',
          'simulated_first_latency_s': float(latency[0]), 'simulated_last_latency_s': float(latency[-1]),
          'end_to_end_camera_latency_measured': False}
```

## Transfer problems — attempt without the solution

### 18.T1

How can a system with acceptable per-item inference time still display old results?

<details><summary>Reveal reasoning after your attempt</summary>

Queue wait, batching, transfer, decode, serialization, or display delay can dominate source-to-result age. Service time is only one portion of the path.

</details>

### 18.T2

What must be checked before calling a vectorized implementation a valid optimization?

<details><summary>Reveal reasoning after your attempt</summary>

It must preserve the intended numerical result, shapes, units, ordering and relevant metadata. Timings must then use comparable inputs and declared boundaries.

</details>

## Record what you actually demonstrated

Copy [the response template](../curriculum/response_templates/18_response.md) to a new dated file in `my_work/`. Explain each output, attempt the two transfer questions, and complete the original independent coding tasks. A passed reference notebook is not a mastery score. The four outcomes above are assessed by explanation, calculation, implementation and critique; delayed recall remains a separate check.

**References:** The original stage's reading assignments remain authoritative for that stage. See [the core source ledger](../docs/SOURCES.md), [the geometry source ledger](../docs/SOURCES_V3.md), and [the v4 source and scope ledger](../docs/SOURCES_V4.md). The worked calculations and these questions are original course additions; theorem proof obligations remain explicit in the proof atlases.
