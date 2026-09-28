#!/usr/bin/env python3
"""Verify the NEW native images and Jobs from `native/deploy` — for real.

Static YAML parsing is not runtime evidence, so this refuses to claim anything
until an actual image is built and an actual Job completes.

Safety rules enforced here:

* The Kubernetes context must be passed explicitly and must look disposable
  (default allowed prefix: `kind-`). Without it, the check records `not_run`.
* A brand-new namespace is created; existing namespaces are never targeted.
* No PVC or learner volume is ever deleted. `--cleanup` only deletes resources
  in the namespace this run created, and only with an explicit flag.
* The Go and Rust images are separate, as in `native/deploy/compose.yaml`.

Exit codes: 0 = every requested gate actually passed, 2 = blocked/not-run,
1 = a gate ran and failed. Blocked is reported, never disguised as a pass.

Usage:
    python tools/native_deploy_verify.py --output my_work/native_deploy01
    python tools/native_deploy_verify.py --output my_work/native_deploy02 `
        --context kind-shape-learning --build --jobs
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEPLOY = ROOT / "native" / "deploy"
LAB = "stage01"


def run(cmd: list[str], timeout: int = 900, cwd: Path | None = None) -> dict:
    started = time.perf_counter()
    try:
        proc = subprocess.run(
            [str(x) for x in cmd], cwd=cwd or ROOT, capture_output=True, text=True, timeout=timeout
        )
        return {
            "cmd": [str(x) for x in cmd],
            "exit_code": proc.returncode,
            "seconds": round(time.perf_counter() - started, 2),
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:],
        }
    except (OSError, subprocess.SubprocessError) as exc:
        return {
            "cmd": [str(x) for x in cmd],
            "exit_code": -1,
            "seconds": round(time.perf_counter() - started, 2),
            "error": f"{type(exc).__name__}: {exc}",
        }


def tool(name: str) -> str | None:
    return shutil.which(name)


def context_is_disposable(context: str, prefixes: tuple[str, ...]) -> bool:
    return any(context.startswith(p) for p in prefixes)


def static_config_checks() -> dict:
    """Parse the shipped YAML and confirm the safety posture. Not runtime evidence."""
    results = {}
    compose = yaml.safe_load((DEPLOY / "compose.yaml").read_text(encoding="utf-8"))
    services = compose.get("services", {})
    results["compose_services"] = sorted(services)
    limits = services.get("go", {})
    results["read_only_rootfs"] = limits.get("read_only") is True
    results["network_disabled"] = limits.get("network_mode") == "none"
    results["no_new_privileges"] = "no-new-privileges:true" in (limits.get("security_opt") or [])

    docs = [d for d in yaml.safe_load_all((DEPLOY / "jobs.yaml").read_text(encoding="utf-8")) if d]
    results["job_kinds"] = [d.get("kind") for d in docs]
    jobs = [d for d in docs if d.get("kind") == "Job"]
    results["job_count"] = len(jobs)
    results["jobs_have_deadline"] = all(
        "activeDeadlineSeconds" in (j.get("spec") or {}) for j in jobs
    )
    results["jobs_pin_namespace"] = all(
        (j.get("metadata") or {}).get("namespace") for j in jobs
    )
    results["pvc_kind_present"] = any(d.get("kind") == "PersistentVolumeClaim" for d in docs)
    results["static_only"] = True
    results["note"] = "YAML parsed and policy-checked. This is NOT image build or cluster execution."
    return results


def build_namespaced_manifests(raw: str, namespace: str, out_dir: Path) -> list[Path]:
    """Rewrite the shipped manifests into THIS run's disposable namespace.

    The shipped jobs.yaml pins `namespace: shape-native-study`. Applying it
    unchanged would touch a namespace this run did not create, so every
    namespaced document is rewritten and written to the run's evidence folder.
    """
    written = []
    for index, doc in enumerate(yaml.safe_load_all(raw)):
        if not doc:
            continue
        metadata = doc.get("metadata")
        if metadata and "namespace" in metadata:
            metadata["namespace"] = namespace
        path = out_dir / f"manifest-{index:02d}-{doc.get('kind', 'doc').lower()}.yaml"
        path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        written.append(path)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--context", default="", help="explicit disposable kube context (e.g. kind-shape-learning)")
    parser.add_argument("--allow-context-prefix", default="kind-", help="comma-separated allowed prefixes")
    parser.add_argument("--namespace-prefix", default="shape-native-verify")
    parser.add_argument("--build", action="store_true", help="build the Go and Rust images")
    parser.add_argument(
        "--images-ready",
        action="store_true",
        help="accept pre-built images referenced by jobs.yaml; verifies they exist locally",
    )
    parser.add_argument("--jobs", action="store_true", help="run the Jobs in the cluster")
    parser.add_argument("--cleanup", action="store_true", help="delete ONLY this run's namespace afterwards")
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args(argv)

    out = Path(args.output).resolve()
    if out.exists():
        print(f"ERROR: choose a NEW output directory: {out}", file=sys.stderr)
        return 2
    out.mkdir(parents=True)

    prefixes = tuple(p.strip() for p in args.allow_context_prefix.split(",") if p.strip())
    record: dict = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scope": "native16 Go/Rust images and finite Jobs; runtime evidence only",
        "static_config": static_config_checks(),
        "gates": {},
        "not_claimed": [
            "original 133-notebook native parity",
            "any production cluster",
            "learner mastery",
        ],
    }

    # --- Gate 1: tools -----------------------------------------------------
    tools = {name: tool(name) for name in ("docker", "kubectl", "kind")}
    record["tools"] = tools
    record["gates"]["tools"] = {
        "status": "passed" if tools["docker"] and tools["kubectl"] else "blocked",
        "detail": tools,
    }

    # --- Gate 2: container runtime ----------------------------------------
    if not tools["docker"]:
        record["gates"]["docker_runtime"] = {"status": "blocked", "reason": "no docker CLI"}
        docker_ok = False
    else:
        probe = run(["docker", "version", "--format", "{{.Server.Version}}"], timeout=60)
        docker_ok = probe["exit_code"] == 0
        record["gates"]["docker_runtime"] = {
            "status": "passed" if docker_ok else "blocked",
            "server_version": (probe.get("stdout") or "").strip(),
            "reason": "" if docker_ok else "docker daemon unreachable",
        }

    # --- Gate 3: image build ----------------------------------------------
    if args.build and docker_ok:
        built = {}
        for lang, dockerfile in (("go", "Dockerfile.go"), ("rust", "Dockerfile.rust")):
            tag = f"shape-native-{lang}:16-verify"
            result = run(
                ["docker", "build", "-f", str(DEPLOY / dockerfile), "-t", tag, "."],
                timeout=args.timeout,
            )
            built[lang] = {"tag": tag, **result, "status": "passed" if result["exit_code"] == 0 else "failed"}
        images_ok = all(v["status"] == "passed" for v in built.values())
        record["gates"]["image_build"] = {
            "status": "passed" if images_ok else "failed",
            "images": {k: {kk: vv for kk, vv in v.items() if kk in ("tag", "status", "exit_code")} for k, v in built.items()},
        }
    elif args.images_ready and docker_ok:
        # The Jobs reference tags without the -verify suffix; confirm they exist.
        expected = {}
        for lang in ("go", "rust"):
            tag = f"shape-native-{lang}:16"
            probe = run(["docker", "image", "inspect", tag, "--format", "{{.Id}}"], timeout=60)
            expected[lang] = {
                "tag": tag,
                "status": "passed" if probe["exit_code"] == 0 else "failed",
                "image_id": (probe.get("stdout") or "").strip()[:80],
            }
        images_ok = all(v["status"] == "passed" for v in expected.values())
        record["gates"]["image_build"] = {
            "status": "passed" if images_ok else "failed",
            "mode": "prebuilt images referenced by native/deploy/jobs.yaml",
            "images": expected,
        }
    else:
        record["gates"]["image_build"] = {
            "status": "not_run",
            "reason": "pass --build or --images-ready (with a working docker daemon) to execute this gate",
        }
        images_ok = False

    # --- Gate 4: live cluster ---------------------------------------------
    if not args.jobs:
        record["gates"]["kubernetes_live"] = {
            "status": "not_run",
            "reason": "pass --jobs with an explicit disposable --context to execute this gate",
        }
    elif not tools["kubectl"]:
        record["gates"]["kubernetes_live"] = {"status": "blocked", "reason": "no kubectl"}
    elif not args.context:
        record["gates"]["kubernetes_live"] = {
            "status": "blocked",
            "reason": "refusing to guess a context; pass --context explicitly",
        }
    elif not context_is_disposable(args.context, prefixes):
        record["gates"]["kubernetes_live"] = {
            "status": "blocked",
            "reason": f"context {args.context!r} does not match disposable prefixes {prefixes}",
        }
    elif not images_ok:
        record["gates"]["kubernetes_live"] = {
            "status": "blocked",
            "reason": "images were not built; a cluster Job would pull nothing new",
        }
    else:
        namespace = f"{args.namespace_prefix}-{time.strftime('%H%M%S')}"
        record["namespace"] = namespace
        created = run(["kubectl", "--context", args.context, "create", "namespace", namespace], timeout=120)
        if created["exit_code"] != 0:
            record["gates"]["kubernetes_live"] = {
                "status": "failed",
                "reason": "namespace creation failed",
                "detail": created.get("stderr", ""),
            }
        else:
            live = {"status": "passed", "namespace": namespace, "steps": {}}
            live["steps"]["namespace_create"] = {"exit_code": created["exit_code"]}

            # Rewrite the shipped manifests into this run's disposable namespace.
            raw = (DEPLOY / "jobs.yaml").read_text(encoding="utf-8")
            manifests = build_namespaced_manifests(raw, namespace, out)
            live["manifests_applied"] = [p.name for p in manifests]

            # `create`, not `apply`: the Jobs use generateName, which apply rejects,
            # and a fresh Pod UID must never overwrite a previous run's output.
            for manifest in manifests:
                applied = run(
                    ["kubectl", "--context", args.context, "-n", namespace, "create", "-f", str(manifest)],
                    timeout=300,
                )
                live["steps"][f"create_{manifest.name}"] = {
                    "exit_code": applied["exit_code"],
                    "stderr": applied.get("stderr", "")[-600:],
                }
                if applied["exit_code"] != 0:
                    live["status"] = "failed"

            # The Job cannot start until its claim is bound; wait rather than guess.
            pvc_wait = run(
                ["kubectl", "--context", args.context, "-n", namespace, "wait",
                 "--for=jsonpath={.status.phase}=Bound", "pvc/native-results",
                 f"--timeout={args.timeout}s"],
                timeout=args.timeout + 60,
            )
            live["steps"]["pvc_bound"] = {
                "exit_code": pvc_wait["exit_code"],
                "stdout": pvc_wait.get("stdout", ""),
                "stderr": pvc_wait.get("stderr", "")[-600:],
            }
            if pvc_wait["exit_code"] != 0:
                live["status"] = "failed"

            wait = run(
                ["kubectl", "--context", args.context, "-n", namespace, "wait",
                 "--for=condition=complete", "job", "-l", "course=shape-native",
                 f"--timeout={args.timeout}s"],
                timeout=args.timeout + 60,
            )
            live["steps"]["wait_complete"] = {
                "exit_code": wait["exit_code"],
                "stdout": wait.get("stdout", ""),
                "stderr": wait.get("stderr", "")[-600:],
            }
            if wait["exit_code"] != 0:
                live["status"] = "failed"

            pods = run(
                ["kubectl", "--context", args.context, "-n", namespace, "get", "pods,jobs,pvc", "-o", "wide"],
                timeout=120,
            )
            live["steps"]["get_all"] = {"exit_code": pods["exit_code"], "stdout": pods.get("stdout", "")}

            for lang in ("go", "rust"):
                logs = run(
                    ["kubectl", "--context", args.context, "-n", namespace, "logs",
                     "-l", f"language={lang}", "--tail=400"],
                    timeout=120,
                )
                log_text = logs.get("stdout", "") + logs.get("stderr", "")
                (out / f"{lang}_job.log").write_text(log_text, encoding="utf-8")
                live["steps"][f"{lang}_logs"] = {
                    "exit_code": logs["exit_code"],
                    # The program prints the path of the result it wrote.
                    "reported_result_path": log_text.strip().splitlines()[-1] if log_text.strip() else "",
                }

            # Verify the PVC actually holds native result JSON. A completed Job plus
            # a printed path is not the same as readable, valid output.
            verify_pod = {
                "apiVersion": "v1",
                "kind": "Pod",
                "metadata": {"name": "native-result-verify", "namespace": namespace},
                "spec": {
                    "restartPolicy": "Never",
                    "automountServiceAccountToken": False,
                    "securityContext": {"runAsNonRoot": True, "runAsUser": 10001, "runAsGroup": 10001, "fsGroup": 10001},
                    "containers": [
                        {
                            "name": "verify",
                            "image": "shape-native-go:16",
                            "imagePullPolicy": "Never",
                            "command": ["/bin/sh", "-c"],
                            "args": [
                                "for f in /work/*/result.json; do "
                                "[ -f \"$f\" ] || continue; echo \"== $f\"; cat \"$f\"; echo; done"
                            ],
                            "securityContext": {
                                "readOnlyRootFilesystem": True,
                                "allowPrivilegeEscalation": False,
                                "capabilities": {"drop": ["ALL"]},
                            },
                            "volumeMounts": [{"name": "results", "mountPath": "/work", "readOnly": True}],
                        }
                    ],
                    "volumes": [{"name": "results", "persistentVolumeClaim": {"claimName": "native-results", "readOnly": True}}],
                },
            }
            pod_path = out / "verify-pod.yaml"
            pod_path.write_text(yaml.safe_dump(verify_pod, sort_keys=False), encoding="utf-8")
            created_pod = run(
                ["kubectl", "--context", args.context, "-n", namespace, "create", "-f", str(pod_path)],
                timeout=120,
            )
            live["steps"]["verify_pod_create"] = {"exit_code": created_pod["exit_code"], "stderr": created_pod.get("stderr", "")[-400:]}
            pod_wait = run(
                ["kubectl", "--context", args.context, "-n", namespace, "wait",
                 "--for=jsonpath={.status.phase}=Succeeded", "pod/native-result-verify",
                 f"--timeout={args.timeout}s"],
                timeout=args.timeout + 60,
            )
            live["steps"]["verify_pod_wait"] = {"exit_code": pod_wait["exit_code"], "stderr": pod_wait.get("stderr", "")[-400:]}
            if pod_wait["exit_code"] != 0:
                live["status"] = "failed"
            pod_logs = run(
                ["kubectl", "--context", args.context, "-n", namespace, "logs", "pod/native-result-verify"],
                timeout=120,
            )
            (out / "pvc_results.json").write_text(pod_logs.get("stdout", ""), encoding="utf-8")
            # Validate that both languages produced parseable result JSON on the PVC.
            verified = {"go": False, "rust": False}
            try:
                blocks = pod_logs.get("stdout", "").split("== ")
                for block in blocks[1:]:
                    header, _, body = block.partition("\n")
                    payload = json.loads(body.strip())
                    for lang in ("go", "rust"):
                        if f"/{lang}-" in header and payload.get("lab") == LAB and payload.get("status") == "completed":
                            verified[lang] = True
            except (ValueError, KeyError) as exc:
                live["steps"]["pvc_result_parse_error"] = str(exc)
            live["steps"]["pvc_results_valid"] = verified
            if not all(verified.values()):
                live["status"] = "failed"

            # Export before ANY cleanup; never delete PVCs.
            exported = run(
                ["kubectl", "--context", args.context, "-n", namespace, "get", "all,pvc", "-o", "yaml"],
                timeout=120,
            )
            (out / "cluster_export.yaml").write_text(exported.get("stdout", ""), encoding="utf-8")
            live["exported"] = exported["exit_code"] == 0
            if args.cleanup:
                # Only this run's namespace. Learner PVCs elsewhere are untouched.
                removed = run(["kubectl", "--context", args.context, "delete", "namespace", namespace], timeout=300)
                live["cleanup"] = {"exit_code": removed["exit_code"], "scope": "this run's namespace only"}
            else:
                live["cleanup"] = {"status": "not_run", "reason": "pass --cleanup after exporting"}
            record["gates"]["kubernetes_live"] = live

    (out / "native_deploy.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({k: (v if k != "static_config" else "…") for k, v in record["gates"].items()}, indent=2)[:2000])
    print("evidence:", out / "native_deploy.json")

    statuses = [g.get("status") for g in record["gates"].values()]
    if "failed" in statuses:
        return 1
    if any(s in ("blocked", "not_run") for s in statuses):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
