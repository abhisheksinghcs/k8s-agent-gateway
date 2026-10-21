# Decisions

Format: context, options, decision, rationale, tradeoffs, revisit conditions.

## D-001 Governing files use uppercase names (accepted, 2026-10-19)

- Context: files were `project_constitution.md` and `status.md`; all agent and instruction files reference `PROJECT_CONSTITUTION.md` and `STATUS.md`. macOS is case-insensitive but Git and Linux are not.
- Decision: renamed to `PROJECT_CONSTITUTION.md` and `STATUS.md`.
- Tradeoff: none meaningful. Revisit: never.

## D-002 Bicep plus bash scripts for infrastructure (accepted, from starter prompt)

- Decision: Bicep for Azure resources; small `set -euo pipefail` scripts for operations. Kubernetes content as plain manifests/Helm via scripts.
- Tradeoff: GPU pool profile flags that are CLI-preview-only might not be in Bicep API versions yet; if so, use `az aks nodepool add` in a script and record it here.
- Revisit: if Bicep cannot express the required `gpuProfile` settings.

## D-003 GPU pool isolation by taint and label (accepted, design)

- Context: GPU pool must not receive general workloads.
- Options: taint only; taint plus label/nodeSelector; dedicated cluster.
- Decision: taint `sku=gpu:NoSchedule` (pattern used in AKS GPU docs) plus a label; GPU workloads set toleration, nodeSelector and `nvidia.com/gpu` limit.
- Rationale: simple, documented, reversible. Taints are creation-time only, so it is set when the pool is created.
- Revisit: if a managed GPU/NAP flow applies its own taints.

## D-004 GPU software stack chosen empirically (proposed)

- Context: SKU is a fractional (1/2) GPU and its position on the AKS supported-GPU list is unverified.
- Options: managed GPU preview; default driver-only + NVIDIA device plugin; `--gpu-driver None` + GPU Operator.
- Decision (proposed): start with the AKS default profile and observe; escalate to device plugin, then GPU Operator, only on evidence. Do not enable the preview feature unless needed.
- Outcome (2026-10-20): the AKS default profile installs the driver only (driver 595.91.07, CUDA 13.2, container runtime configured). The SKU's GPU is a MIG slice (~46 GiB). No device plugin is installed by default, so we deploy the NVIDIA device plugin v0.18.0 (`k8s/gpu/nvidia-device-plugin.yaml`) with `MIG_STRATEGY=single`; it only works privileged (T-007). Managed GPU preview and GPU Operator were not needed. D-004 is therefore accepted: AKS-installed driver plus our own device plugin.
- Revisit: if the device plugin can be run without `privileged`, or if the node image/driver changes.

## D-005 Region: southeastasia (accepted, 2026-10-19, human decision)

- Context: only westus2 and southeastasia offer the SKU to this subscription; GPU family quota is 0 in both. westus2 has only 66 vCPUs of regional headroom; southeastasia has 100 free.
- Decision: southeastasia. Cost is explicitly not a constraint (human instruction), but teardown stays easy (`scripts/down.sh`).
- Consequence: the SKU is offered in zone 1 only there, so the GPU pool is pinned to zone 1.
- Quota requests are made by a human on the shared subscription, not by agents.
- Revisit: if quota cannot be obtained in southeastasia (fall back to westus2 plus a regional quota increase).

## D-007 Cluster baseline for the lab (accepted, design)

- Decision: AKS Standard, system-assigned managed identity, Azure CNI overlay, API server public with optional authorized-IP parameter, local accounts left enabled. System pool `Standard_D2s_v5` x1 tainted `CriticalAddonsOnly`; app pool `Standard_D4s_v5` x1; GPU pool added by a flag (`deployGpuPool`) so Phase 2 can run before GPU quota exists.
- Rationale: simplest thing that satisfies CPU/GPU separation (constitution section 7). Entra-integrated auth and a private API server add setup friction with little lab value.
- Tradeoff: public API endpoint and local admin credentials. Differs from customer-demo/production; Security Reviewer to assess at Phase 11 and before any external exposure.
- Revisit: Phase 11, or if sharing the cluster.

## D-009 Model storage: Azure Disk PVC, model pulled by llama-server (accepted, 2026-10-20)

- Context: the GPU node is Spot and local disk is lost on eviction (D-008).
- Options considered: emptyDir + download each start; hostPath; Azure Disk PVC; Azure Files/blob mount; model baked into an ACR image.
- Decision: a 64 GiB `managed-csi-premium` ReadWriteOnce PVC mounted at `/models`; `llama-server -hf <repo>:<quant>` with `LLAMA_CACHE=/models` downloads on first start and reuses the file afterwards. Deployment strategy `Recreate` (one GPU unit, RWO disk).
- Rationale: survives node eviction without a re-download, one small manifest, no registry or token needed for ungated models. The GPU pool is pinned to zone 1, so the zonal disk can follow it.
- Tradeoffs: a small recurring disk cost; a replacement node still needs the disk to detach and re-attach (minutes); first start depends on Hugging Face reachability.
- Revisit: if disk attach delays hurt, or for gated models (add a token Secret, never committed).

## D-010 First model: Qwen2.5-7B-Instruct Q4_K_M (accepted, 2026-10-20)

- Context: the human wants small models; the GPU slice has ~46 GiB.
- Decision: `bartowski/Qwen2.5-7B-Instruct-GGUF:Q4_K_M` (about 4.7 GB, Apache-2.0). Verified via the Hugging Face API: not gated, single-file Q4_K_M present. Served under the alias `qwen2.5-7b-instruct`.
- Image: `ghcr.io/ggml-org/llama.cpp:server-cuda13`, now pinned by digest `sha256:78d05416...7587db` (build `b11749-1d88cb05f`), the build that passed validation. The node driver supports CUDA 13.x.
- Revisit: the model is a one-line change (`-hf` argument); larger models fit in ~46 GiB.

## D-011 llama.cpp runs in router mode with several models (accepted, 2026-10-20)

- Context: the human wants to choose between several models (a Qwen coder, a Phi, a Llama) from the Pi client, not just one. Only one `nvidia.com/gpu` unit exists, so one pod per model does not work (a second GPU pod stays Pending).
- Options: (a) router mode, one pod, models loaded on demand from the shared PVC; (b) one Deployment per model with GPU time-slicing in the device plugin; (c) keep single-model and redeploy to switch.
- Decision: (a). `llama-server --models-preset /config/models.ini --models-max 3 -ngl 99 -c 8192`; preset in ConfigMap `llama-models-preset`. Models (all verified ungated with a single Q4_K_M file): `qwen2.5-7b-instruct`, `qwen2.5-coder-7b-instruct`, `llama-3.1-8b-instruct` (bartowski/Meta-Llama-3.1-8B-Instruct-GGUF, Llama 3.1 community license), `phi-4` (bartowski/phi-4-GGUF, MIT). Model id in requests = preset section name. Memory limit raised to 48Gi.
- Rationale: one GPU unit, no sharing config, new models are one ConfigMap entry, files persist on the PVC (D-009).
- Tradeoffs: first request to a model downloads and loads it (minutes); switching models reloads weights; with `--models-max 3` the least recently used model is unloaded. The router API exposes model download/delete endpoints (`POST/DELETE /models`), so it must stay ClusterIP or localhost only (Phase 11). Pi's built-in llama.cpp provider (`/llama`) should also work against a router, but only the OpenAI-compatible `models.json` route is used so far.
- Revisit: if load latency hurts, or when agentgateway routing (D-006) needs a model-name mapping.

## D-006 agentgateway integrates via AgentgatewayBackend + HTTPRoute (proposed)

- Basis: official docs show OpenAI-compatible in-cluster backends (vLLM guide) using `AgentgatewayBackend` with `ai.provider.openai`, `host`, `port`, and an `HTTPRoute`. An `AgentgatewayModel` route-by-model alternative exists in v1.6; revisit if it fits llama.cpp better.
- Revisit: Phase 9, after confirming llama-server's request path and model naming.

## D-008 GPU pool runs on Spot VMs (accepted as the primary path, 2026-10-20)

- Human input: standard GPU quota is not expected to be granted, so Spot is the working assumption rather than a stopgap.
- Context: standard-family GPU quota is 0/0 for every modern GPU family in every visible subscription, and portal quota requests fail (T-005). A support ticket is the standard route.
- Options: (a) support ticket for standard quota; (b) a subscription that has GPU quota; (c) Spot GPU pool, which draws on the separate regional Spot quota pool (docs: Spot has a separate quota pool; regional Spot limit here is 100 vCPUs); (d) a different, lower-quota SKU.
- Decision (proposed): use (c) via `GPU_SPOT=true` while (a) is pursued in parallel. Spot pool: eviction policy Delete, max price -1, autoscaler min=max=1 so an evicted node is replaced. AKS taints it `kubernetes.azure.com/scalesetpriority=spot:NoSchedule` in addition to `sku=gpu:NoSchedule`; GPU workloads need both tolerations.
- Tradeoffs: no SLA; the node can be evicted at any time (model reload cost); Spot pool cannot be the system pool; no surge during upgrades; capacity is best effort.
- Revisit: when standard quota is granted (switch `GPU_SPOT=false`, recreate the pool: priority is immutable), or if Spot capacity is unreliable.
