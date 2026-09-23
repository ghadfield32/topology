# Stage 18 — Make the pipeline efficient without changing the evidence

Measure conversion, queues, age and output—not just the model call.

**Track:** applied geometry continuation, not a claimed chapter of the book. **Prerequisites:** Stage 14, Stage 15.

## 1. Throughput and latency answer different questions
Throughput counts completed items per time interval. Latency measures elapsed time from a declared start to a declared finish for one item. A pipeline can process many frames per second while displaying results from long ago if a queue grows. A high frame rate does not guarantee a useful live experience.

Name the boundaries: capture, arrival, queue entry, processing start, preprocessing, device transfer, inference, geometry, serialization, and display. A CPU timer around one function covers only that function. It does not cover phone exposure or browser display unless those timestamps are actually included.

## 2. The attached source gives a hypothesis, not our benchmark
The supplied ROS2/PointPillars account attributes speed improvement to point-cloud conversion and reports its author's timing. We retain that as a reported example. Our lab neither reproduced that hardware pipeline nor measured its claimed frame rate. The transferable hypothesis is that representation conversion can dominate useful work.

The ROS2 source provides structured-array conversion and an equally typed-field NumPy path. Field names, data types, byte order, padding and organization matter. Treating every buffer as contiguous xyz float32 data without inspecting its layout is not a general PointCloud2 parser. [S01]

## 3. Vectorization with a semantic equality check
Our real-data lab transforms a benchmark-derived point cloud using an explicit per-point loop and an array operation. Both compute the same formula. First compare their outputs to numerical tolerance, then time repeated runs. An optimization is not an improvement if it quietly changes invalid-value policy, units, ordering or precision.

Use a monotonic performance timer, a warm-up, multiple repetitions, and a distribution summary. A single lucky run is not a reliable comparison. The saved results describe this build environment only. Your Mac or GPU may behave differently, and pure CPU microbenchmarks say little about a full capture-to-display pipeline.

## 4. Simulate the queue before blaming inference
For a single FIFO server, let aᵢ be an arrival and sᵢ its service time. The completion recurrence is

```text
finish_i = max(arrival_i, finish_(i-1)) + service_i
latency_i = finish_i - arrival_i.
```

If a frame arrives every 10 milliseconds but service always takes 20 milliseconds, delay grows. Batching, dropping stale work, reducing processing, or changing the capture rate have different trade-offs. A latest-frame policy may reduce age while discarding temporal evidence needed for an event. There is no universally correct queue policy independent of the task.

The notebook's queue trace is a simulation with chosen times. It is not a hardware trace. We print that status alongside its p50, p95 and maximum values.

## 5. Timestamps are data
For several devices, timestamps may have offset and drift. A simple model relates a device clock to a reference by `t_ref = a t_device + b`. Estimating both a and b requires appropriate shared timing evidence over a sufficient interval. Matching numeric timestamp values alone does not synchronize clocks.

Keep source frame IDs, presentation timestamps, time base, dropped-frame information and any mapping uncertainty. Never reorder observations silently to make a trace look smoother. Offline preprocessing can use the whole sequence; a live method must respect the observation availability cutoff.

## 6. Device timing needs synchronization
Accelerator work may be asynchronous. Timing only the CPU call can measure scheduling rather than completion. The optional runner places device synchronization around its timed forward pass and separately labels load, preprocess, forward and serialization durations. Those remain model-run boundaries, not capture-to-display latency. [S02]

Peak allocated and reserved GPU memory are different statistics. Baseline model storage, activations, head choices, precision, resolution and frame count all matter. Start with a small run and measure instead of extrapolating a paper's different hardware configuration.

## 7. Preserve evidence while optimizing
A useful event record keeps the source identity, observation timestamp, availability time, model/checkpoint version, calibration version, inferred/observed state and uncertainty. Lightweight tracking and heavier geometry may run at different rates; their outputs still need compatible identities and times.

No ROS2 installation or production rewrite is required to learn these principles. The core exercise is a controlled CPU comparison plus a queue model, with clear boundaries on what was and was not measured.

## Independent conceptual exercises

1. Distinguish throughput, service time, latency, and stale-result age.
2. Calculate the FIFO recurrence for the supplied three-frame example.
3. What must be checked before trusting a vectorized replacement?
4. Why can a CPU timer undermeasure GPU work?
5. What does t_ref=a t_device+b represent?
6. Why is a latest-frame queue not automatically best for event detection?

## Mastery gate

Report a reproducible local benchmark and explain why it is not end-to-end live-system evidence.

Readings: S01, S02. See the [source ledger](../docs/SOURCES_V3.md) for checked links, evidence status and source differences.
