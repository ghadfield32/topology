# Orchestration is the final layer, not a prerequisite for topology

This supplemental worker image and Deployment are **configuration only until built and run on your machine**. Existing native/deploy Jobs and historical Python cluster evidence do not prove this new image ran. The standalone HTTP/native integration and queue tests are separate evidence.

## Docker first

From the course root:
```
docker compose -f systems/deploy/compose.yaml config
docker compose -f systems/deploy/compose.yaml build
docker compose -f systems/deploy/compose.yaml up worker
```
The service is on127.0.0.1:8090 only. Submit `{"lab":"stage01"}` to POST /jobs, poll GET /jobs/{id}, and explicitly save its JSON. No authentication, persistent result store or automatic eviction is provided. The retention bound refuses further work instead of growing indefinitely. Restart loses all retained jobs. One worker process launches a separate native executable per job; no arbitrary shell command is accepted over HTTP.

Export results before stopping/replacing a Pod. The Deployment's emptyDir is temporary, not a learner PVC or backup. It does not mount your existing learner volumes. Never rely on an in-memory response as the sole record of an experiment.

## Then a disposable kind namespace

Use your already installed client and explicitly inspect the context. Do not change the global current-context as a shortcut.
```
kubectl --context kind-shape-learning get namespaces
kind load docker-image shape-systems-worker:17 --name shape-learning
```
Choose a NEW namespace. The supplied manifest uses shape-systems-study; if it already exists, use a separately reviewed copy with a new namespace. Do not overwrite another exercise.
```
kubectl --context kind-shape-learning create namespace shape-systems-study
kubectl --context kind-shape-learning apply --dry-run=server -f systems/deploy/worker.yaml
kubectl --context kind-shape-learning apply -f systems/deploy/worker.yaml
kubectl --context kind-shape-learning -n shape-systems-study rollout status deployment/shape-worker
kubectl --context kind-shape-learning -n shape-systems-study port-forward service/shape-worker 18090:8090
```
The API is now temporarily available on localport18090. Port-forward does not make it a public service. ClusterIP is not authentication; do not put this exercise in a shared/production cluster. Stop forwarding with Ctrl+C. Namespace/cluster/volume deletion is a separate deliberate action and is not automated here.

Use native/deploy's batch Jobs for finite Go/Rust lab execution; use this Deployment for the request/queue/service lesson. Static YAML parsing, server validation, scheduling, service readiness, completed work and independently checked results are different acceptance levels.

## CPU/GPU environment

No GPU runtime is requested. GPU container work needs actual NVIDIA/WSL capability, a compatible runtime, resource declarations and its own profiler evidence. A CPU fallback must never be labeled a CUDA benchmark. No Windows/Linux driver or cluster-runtime installation is performed by the course.
