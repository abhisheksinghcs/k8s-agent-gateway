# STATUS

Last updated: 2026-10-20 (Phases 5-7 VALIDATED by independent Tester: direct llama.cpp inference on the Spot GPU; next: agentgateway)

Labels used: FACT, DECISION, ASSUMPTION, HYPOTHESIS, OPEN QUESTION.
Lifecycle: PLANNED -> CREATED -> DEPLOYED -> VALIDATED (or FAILED).

## What this project is

Reproducible AKS lab for GPU-backed open-weight models and agent infrastructure.

    client / AI agent -> agentgateway -> llama.cpp -> NVIDIA GPU (Standard_NC72ds_xl_RTXPRO6000BSE_v6)

Details: [docs/architecture.md](docs/architecture.md). Rationale: [docs/decisions.md](docs/decisions.md). Operational findings: [docs/troubleshooting.md](docs/troubleshooting.md). Agent delegations: [docs/agent-execution-log.md](docs/agent-execution-log.md).

## Human decisions so far

- DECISION: region is **southeastasia** (D-005). Cost is not a constraint.
- DECISION: standard GPU quota is not expected, so the GPU pool runs on **Spot** (D-008). The node can be evicted at any time.
- `PROJECT_CONSTITUTION.md` is complete and governs the project.

## Current phase

Phase 8: install agentgateway v1.6.0 on the `app` pool and validate the control plane. Before Phase 9, get an independent Tester pass on the router-mode llama.cpp (D-011), because the gateway must not be wired to an unvalidated upstream.

## Phase tracker

| Phase | Description | State |
|---|---|---|
| 0 | Repository/bootstrap validation | VALIDATED |
| 1 | Azure prerequisites and infra design | Done (standard quota unavailable; Spot used, D-008) |
| 2 | AKS base cluster | VALIDATED (independent Tester, 4/4 checks) |
| 3 | GPU node pool | VALIDATED (independent Tester) |
| 4 | NVIDIA/Kubernetes GPU validation | VALIDATED (independent Tester, 5/5 checks) |
| 5 | Model storage strategy | VALIDATED (D-009: Azure Disk PVC, persistence tested) |
| 6 | llama.cpp deployment | VALIDATED |
| 7 | Direct llama.cpp inference validation | VALIDATED (independent Tester, 6/6 checks) |
| 8 | agentgateway deployment | PLANNED |
| 9 | agentgateway -> llama.cpp integration | PLANNED |
| 10 | End-to-end inference validation | PLANNED |
| 11 | Security review and hardening | PLANNED |
| 12 | Final docs and repeatability validation | PLANNED |

## Component lifecycle

| Component | State | Notes |
|---|---|---|
| Governance docs | CREATED | `PROJECT_CONSTITUTION.md` and `.github/copilot-instructions.md` are complete (human-updated 2026-10-20) |
| `scripts/preflight.sh` | CREATED | Checks standard family quota only; does not know about the Spot route (needs update). `--resource-type` speedup unverified. |
| `infra/main.bicep` | DEPLOYED | CPU pools + Spot GPU pool (managed 128 GB OS disk) |
| `scripts/up.sh`, `status.sh`, `env.sh` | DEPLOYED (used) | `down.sh` CREATED, never exercised |
| AKS `aks-agw-lab` (rg `rg-aks-agw-lab`, southeastasia, v1.36.4) | DEPLOYED | system, app, gpunp pools all Succeeded |
| GPU node `gpunp` (Spot) | DEPLOYED | Ready, taints `sku=gpu:NoSchedule` + `kubernetes.azure.com/scalesetpriority=spot:NoSchedule`, label `workload=gpu-inference` |
| NVIDIA device plugin (`k8s/gpu/nvidia-device-plugin.yaml`) | DEPLOYED | Runs privileged (T-007); node advertises `nvidia.com/gpu: 1` |
| GPU smoke test (`k8s/gpu/gpu-smoke-test.yaml`) | DEPLOYED, passed | See evidence; not yet independently validated |
| llama.cpp (`k8s/llm/llama-cpp.yaml`) | DEPLOYED, router mode with 4 models (D-011); single-model version was VALIDATED | Router change tested by Developer only; needs an independent Tester pass. agentgateway path NOT validated |
| agentgateway | PLANNED | |

## Evidence

Phase 2: see [docs/troubleshooting.md](docs/troubleshooting.md) T-004 and earlier history; Tester confirmed nodes Ready, scheduling on `app`, DNS, 30 kube-system pods Running.

Router mode with four models (2026-10-20, Developer evidence, not yet independently validated):

- FACT: `llama-server --models-preset ... --models-max 3` lists 4 preset models (+1 cached); child processes inherit `-ngl 99 -c 8192`.
- FACT: from an in-cluster pod each of `qwen2.5-7b-instruct`, `qwen2.5-coder-7b-instruct`, `llama-3.1-8b-instruct`, `phi-4` answered "17 + 25" with `42` at temperature 0; first-load times 48 s, 26 s, 27 s, 72 s (include download); generation 81, 80, 76, 49 tokens/s.
- FACT: after loading the fourth model the router had unloaded the least recently used one (the first Qwen), consistent with `--models-max 3`.
- FACT: through the localhost port-forward the coder model returned a code answer; Pi's `~/.pi/agent/models.json` (outside the repo, no secrets) lists all four models under provider `aks-llama`.
- FACT (2026-10-21, observed): the Spot GPU node was evicted (~15 h after creation) and recovered automatically; replacement node Ready with `nvidia.com/gpu: 1`, device plugin running, PVC re-attached, all four models cached (no re-download), chat returned `42`. Downtime ~25-30 min (T-008).
- NOT tested: the agentgateway path, concurrent use of different models, model-switch latency under load.

Direct llama.cpp inference, single-model version (2026-10-20, Tester independent):

- FACT: pod Ready on the GPU node; Service `llama-cpp` is ClusterIP only (no LoadBalancer/NodePort/Ingress).
- FACT: from a separate in-cluster pod, `GET /health` ok and `POST /v1/chat/completions` (model `qwen2.5-7b-instruct`) returned a correct answer ("What is 17 + 25?" -> `42`, temperature 0). Generation ~95-97 tokens/s, prompt evaluation ~700-1100 tokens/s.
- FACT: `llama-server` holds ~5.4 GiB of GPU memory (`nvidia-smi` on the node and in the pod; the server log itself prints no CUDA/offload lines at this verbosity).
- FACT: PVC `llama-models` Bound, 64Gi, `managed-csi-premium`; 4.4 GB under `/models`. Deleting the pod: replacement Ready in 12 s, no re-download, answer identical.
- FACT: first start ~4 min (image pull 3m14s + model download).
- NOT tested: Spot eviction recovery (new node, re-attach, re-pull), the agentgateway path, a different model.
- FACT: server warns "no API key set and CORS allows all origins"; no NetworkPolicy in `llm`.

GPU (2026-10-20, reproduce with `kubectl apply -f k8s/gpu/gpu-smoke-test.yaml && kubectl -n gpu-resources logs gpu-smoke-test`):

- FACT: GPU family quota (`StandardNCdsRTXPRO6000BSEv6XLFamily`) is 0/0 in both regions; A100/H100 and all other modern GPU families are also 0/0 in every subscription visible to this login; portal quota requests failed (T-005).
- FACT: Spot GPU quota is a separate pool (regional Spot limit 100 vCPU); the 72-vCPU Spot node was allocated.
- FACT: first two Spot attempts failed bootstrap (CSE exit 84). Cause: default 2040 GB ephemeral OS disk resize ~29 s (T-006). With `osDiskType=Managed, osDiskSizeGB=128` the third attempt succeeded.
- FACT: on the node, `nvidia-smi` shows NVIDIA RTX Pro 6000 Blackwell, driver 595.91.07, CUDA 13.2, MIG mode Enabled, 1 MIG device with ~46 GiB.
- FACT: AKS default GPU profile installs the driver only (`gpuProfile.driver=Install`). No device plugin by default, so `nvidia.com/gpu` was absent until we deployed one.
- FACT: the device plugin with `MIG_STRATEGY=single` fails with "Insufficient Permissions" unless `privileged: true` (SYS_ADMIN and NVIDIA_MIG_MONITOR_DEVICES did not help) (T-007).
- FACT: with the privileged plugin the node allocatable shows `nvidia.com/gpu: 1`. A test pod requesting `nvidia.com/gpu: 1` (both tolerations) scheduled on the GPU node, completed, and its log shows `nvidia-smi` with the GPU and a 46791 MiB MIG device.
- FACT (Tester, independent): GPU node Ready with both taints; `nvidia.com/gpu: 1` allocatable; GPU pod ran `nvidia-smi` on it; a pod without tolerations/GPU request landed on the `app` node; a second GPU pod stayed Pending (`Insufficient nvidia.com/gpu`) while the first held the GPU.
- NOTE: the Tester saw a young GPU node (~17:08Z) and suspected eviction. That is not the cause: this node (`...61997117...`) is the third GPU pool created in this session (earlier two failed, T-006). No eviction has been observed.
- FACT: Azure Policy admission warnings appear on pod creation (non-root, limits, read-only FS, capabilities); pods are still admitted, including the privileged plugin.

## Blockers

None blocking. Risks:
1. Spot eviction can delete the GPU node at any time (D-008); the pool autoscaler (min=max=1) tries to replace it but capacity is best effort.
2. The device plugin runs privileged (T-007); needs review.

## Open questions

1. (resolved, D-010) llama.cpp image: `server-cuda13` works on this node; pinned by digest.
2. (resolved, D-010) First model: Qwen2.5-7B-Instruct Q4_K_M. Larger models up to ~30B at 4-bit should fit in the ~46 GiB MIG slice (untested).
3. (resolved, D-009) Model storage: Azure Disk PVC.
4. (resolved) `.github/copilot-instructions.md` is now complete.
5. `image.png` is redundant and untracked; recommend deleting (awaiting OK).
6. Whether to submit a support ticket for standard GPU quota to allow non-Spot later.
7. Add a NetworkPolicy and an API key for llama-server before any wider exposure (Phase 11).

## Repository notes

- Governing files renamed to uppercase (D-001). Only the initial commit exists; all current files are untracked.
- `main.py`, `pyproject.toml`, `.python-version`: uv scaffold stubs unrelated to the lab. Untouched.
- Failed GPU pools were deleted (they were our own failed artifacts). No other resources were deleted.

## Files changed this session

`.gitignore`, `README.md`, `STATUS.md`, `PROJECT_CONSTITUTION.md` (user-updated), `docs/*.md`, `infra/main.bicep`, `scripts/{env,preflight,up,down,status}.sh`, `k8s/gpu/nvidia-device-plugin.yaml`, `k8s/gpu/gpu-smoke-test.yaml`.

## Plan (remaining)

1. Phases 8-10: agentgateway v1.6.0 on the `app` pool; `Gateway`, `AgentgatewayBackend`, `HTTPRoute`; end-to-end request via port-forward.
2. Phase 11-12: Security Reviewer pass (privileged plugin, public API server, Spot, unauthenticated llama-server, no NetworkPolicy); teardown and rebuild test; update `preflight.sh` for Spot; test Spot eviction recovery.

## Next action

Phase 5 (model storage) and Phase 6 (llama.cpp deployment).
