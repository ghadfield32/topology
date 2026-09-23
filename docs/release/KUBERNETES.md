# Kubernetes from zero: inspect, validate, schedule, finish, preserve

## The objects and what they mean

A **cluster** is a Kubernetes control plane plus worker capacity. A **context** selects the cluster and identity your client will use. A **namespace** scopes this exercise's objects. A **Pod** runs containers together. A **Deployment** maintains a long-running application. A **Job** runs work expected to finish. A **Service** supplies a stable route to Pods. A **PersistentVolumeClaim (PVC)** asks for storage that outlives one Pod.

The reader is a Deployment because it stays available. Acceptance is a Job because it must finish with a visible status. These are separate questions: configuration validity, API admission, scheduling, storage binding, process startup, completed tests, completed notebook, and reachable reader. Passing one does not imply the rest.

## Safe local scope

The supplied tool accepts only an explicitly selected `kind-` context and a new non-system namespace. A context name is a guard against accidents, not proof that an arbitrary context is safe. Inspect `kubectl config view --minify --context ...` yourself. Do not use this teaching script with a work/production cluster. No cluster or namespace is deleted automatically.

The deployment uses a restricted namespace policy, non-root containers, no mounted service-account token, no added capabilities, no privilege escalation, RuntimeDefault seccomp, a read-only root, explicit resources, and temporary scratch storage. No hostPath or host-network access is accepted by the project validator. ClusterIP exposes no public endpoint.

Only the acceptance Job mounts `learner-work`. The public reader does not attach the private results PVC; this also avoids an unnecessary second consumer of single-writer storage. A valid PVC declaration still requires a real storage class/provisioner at runtime.

## Step 1: inspect and check without a cluster

```bash
uv run --no-sync python tools/k8s_verify.py --static --profile physics --namespace shape-study01 --output my_work/k8s_static01
```

Read the generated `resources.json` and `verification.json`. This checks project invariants, not the Kubernetes API schema. The static validator rejects privileged/root containers, host namespace/path access, missing restrictions, mixed namespaces, duplicate identities and changed retry policies. A static pass is reported as `static_only`, never `cluster_verified`.

## Step 2: prepare an explicitly disposable local cluster

Install Docker, kind, and a compatible kubectl. Record their actual versions. Follow [Docker setup](DOCKER.md) to build `listening-to-shape:12` from a real lock first.

```bash
kind create cluster --name shape-learning
kind load docker-image listening-to-shape:12 --name shape-learning
kubectl config view --minify --context kind-shape-learning
```

Creating a kind cluster consumes local resources. Use a new approved name if this one exists. This course does not claim a Kubernetes version range was tested; CI's actual client/server/image versions must be saved with each deployment.

## Step 3: request live acceptance explicitly

```bash
uv run --no-sync python tools/k8s_verify.py --context kind-shape-learning --namespace shape-study01 --image listening-to-shape:12 --profile physics --apply --output my_work/k8s_live01
```

The tool checks runtime readiness and namespace absence. It creates only the requested Namespace before doing server-side dry-run for the full manifest, then applies and waits for the reader and Job. Failure preserves resources and diagnostics for inspection. There is no silent retry against another cluster or namespace.

The Job uses `backoffLimit: 0` and an output directory based on its Pod UID. It runs the requested-profile tests and Stage 00 in fresh kernels, reads the child `tests.json` and `execution.json`, validates counts/scope/source continuity, and prints `SHAPE_ACCEPTANCE=` with structured evidence. The host verifier checks the child evidence again. A pair of zero exit codes alone is insufficient. Full profile rejects skipped comparisons. This Job is a bounded acceptance exercise, not an all-notebook distributed benchmark.

## Step 4: inspect access and export results

```bash
kubectl --context kind-shape-learning -n shape-study01 get pods,jobs,pvc
kubectl --context kind-shape-learning -n shape-study01 logs job/course-acceptance
kubectl --context kind-shape-learning -n shape-study01 port-forward service/course-reader 8000:8000
```

Visit `http://localhost:8000/START_HERE.html` and follow an actual lesson and figure link. Readiness probes do not independently establish your browser path. Record this manual check separately. Use the Job's logged output path when exporting results from persistent storage. A completed Job's container is not generally available for `kubectl cp`; use a separately reviewed temporary reader Pod mounting the existing PVC, or your local storage provider's supported export procedure. Avoid concurrent conflicting single-writer mounts. Inspect copied hashes before cleanup.

**Do not delete the namespace, PVC, or kind cluster until your work is exported and checked.** Namespace deletion can delete claims and their underlying storage depending on policy. Cleanup is a separate explicit action, never part of acceptance.

## Diagnose the layer that failed

| Symptom | Inspect next | Do not infer |
|---|---|---|
| Client missing/unreachable server | Tool versions and selected context | That the manifest was rejected |
| Server dry-run rejected | The exact admission/schema error | That Python tests failed |
| Pending Pod | Scheduler events, requests, architecture | That startup code ran |
| Pending PVC | StorageClass/provisioner and access mode | That persistence is configured successfully |
| ImagePullBackOff | Image identity and kind image load | That the image's Python environment was tested |
| Job Failed | Child logs and detailed evidence | That retries should overwrite output |
| Reader not reachable | Pod readiness, Service selector, port-forward | That opening a public port is required |

## Delivery status

This host has no Docker, kind, or kubectl. Project-policy and failure-reporting tests ran; live server validation, image scheduling, PVC binding, cluster Job execution, and cluster browser access did not. The exact statuses remain in the current verification report. Configuration presence is not deployment evidence.

Primary references: https://kubernetes.io/docs/concepts/workloads/controllers/job/ ; https://kubernetes.io/docs/concepts/security/pod-security-standards/ ; https://kind.sigs.k8s.io/docs/user/quick-start/ .
