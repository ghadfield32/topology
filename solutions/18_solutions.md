# Stage 18 conceptual solutions

Attempt the lesson questions first. These are answer criteria, not scores assigned to your work.

## 1. Distinguish throughput, service time, latency, and stale-result age.

Throughput is completions per interval, service time is work duration, latency spans specified start/end boundaries, and stale age compares the present to the source observation time.

## 2. Calculate the FIFO recurrence for the supplied three-frame example.

Completion times are .02,.04,.06 and latencies .02,.03,.04 seconds.

## 3. What must be checked before trusting a vectorized replacement?

Equivalent inputs, ordering, units, mask policy, dtype, output values and relevant invariants must be tested before comparing timing.

## 4. Why can a CPU timer undermeasure GPU work?

Asynchronous calls may return before the accelerator finishes. Synchronization or suitable device events are needed for the chosen measurement boundary.

## 5. What does t_ref=a t_device+b represent?

a models relative clock rate or drift and b models offset. They need evidence and uncertainty estimates; equal numeric timestamps alone are not synchronization.

## 6. Why is a latest-frame queue not automatically best for event detection?

Discarding stale frames can reduce latency while deleting evidence of short events. The appropriate policy depends on temporal coverage and accuracy requirements.
