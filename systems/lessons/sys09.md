# sys09 — Go: bounded workers and native analysis jobs
**Source:** Stage 9. The source says Go's role here is services, workers, networking and infrastructure. Keep the existing numerical Go labs; this project adds the intended systems role rather than replacing them.

## Explain the job lifecycle
An HTTP request asks for work; a job has a longer lifecycle. Completing POST must not automatically cancel queued work. Our manager therefore owns a root context and a per-job timeout from submission. GET returns a snapshot; DELETE requests cancellation. A goroutine runs work, channels organize delivery, and a mutex protects shared state. None of these guarantees speed. `defer` schedules cleanup on function return, not at an arbitrary time chosen by a garbage collector.

The manager has explicit worker, queue and retained-job limits. Queue saturation returns an error rather than growing memory indefinitely. The reference retains at most 128 jobs in memory and then refuses new submissions; persistence/eviction is an independent production extension. Service restart loses the in-memory store. This is openly documented rather than presented as a durable distributed scheduler.

## Actual work, not shell commands from the network
The server reads the existing native protocol registry. A request supplies only an allowed lab key. The production engine starts the specified native Go executable with fixed argument structure using exec.CommandContext—never a user-provided shell command. Each job is a separate native process because the original engine's provenance has a one-run-per-process lifecycle. Multiple workers must not call that shared engine concurrently inside one process without a proper refactor.

The result is JSON from the real native program. Stdout/stderr are bounded. Context expiry terminates the direct child; status records distinguish success, failure, cancellation and timeout. Submitted/started/finished timestamps expose queue age separately from compute duration. The default bind is loopback with no authentication; do not expose this educational service publicly or treat it as a multi-tenant boundary.

## Predict and implement
Predict what happens when one worker is busy, one queued slot is full and another job arrives. Run the tests, including the race detector on a supported compiler/OS. The tests use controlled engines to isolate scheduling; a separate live HTTP probe runs Stage 01 through the actual native Go executable. Those are distinct forms of evidence.

Prepare sys09 and compile the private module. Start the server with `--repo` set to the unchanged course root and `--binary` set to a known compiled `shape-go` program. Submit `{"lab":"stage01"}` to POST /jobs; poll the returned ID through GET /jobs/{id}. Inspect the actual result's input hashes. Try an unknown lab or an extra `cmd` field: it must be rejected.

## Break and recover
Use cancellation while queued and while running, a bounded timeout and graceful shutdown. Record what becomes of pending jobs and whether the server accepts work after Close. A worker crash, disk-full persistent store or a multi-process restart policy remains a separate production concern. Do not use 1000 unbounded local processes as the 'load test'; send requests into the existing bound and measure rejected/queued/running/completed counts.

## Kubernetes application
First make the standalone service and one batch job work. Only then package images and submit an explicitly selected kind namespace. A Deployment serves an ongoing endpoint; a Job performs finite work. PVCs retain files beyond a Pod but are not backups. The current service stores results in memory; export them explicitly or implement a durable store before claiming persistence. The new deployment files require live verification and do not borrow the old Python cluster's pass.

## Exit gate
Explain errors/defer, interfaces, goroutines/channels, synchronization, context lifetime, HTTP/JSON, backpressure, deadlines, cancellation and shutdown. Show one successful real native job and one deliberately rejected request. Measure queue and compute behavior separately. Your report should explain why this is a learning service, not an exposed production queue.
