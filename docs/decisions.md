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

## D-012 Python lab-information MCP server (LOCAL source accepted, 2026-10-22)

Current authority: the two-tool teaching amendment and its final LOCAL acceptance
below supersede the original three-tool contract/54-test acceptance for current
source. Earlier evidence remains historical; its response-protection guarantees
do not apply to the SDK-only revision.

### Context and scope

- Audience: hands-on learning, customer demonstrations, and explaining the lab to hiring managers. Include a code walkthrough; this is not a published production service.
- Human authorization covers local implementation, tests, and reproducible container/Kubernetes artifacts only. No Azure resource creation, registry creation, image push, cluster deployment, gateway installation/integration, or public exposure. The component remains PLANNED until artifacts exist; this review proves no runtime behavior.
- This work can proceed independently while gateway deployment remains paused. It does not satisfy Phase 8 or remove the independent router-mode llama.cpp validation prerequisite before Phase 9.
- Observed repository baseline: clean working tree at `9eeaa69`; Python 3.12 scaffold, empty project dependencies, greeting-only `main.py`, and no tracked lockfile. No installed SDK, Docker daemon, or live cluster state was checked in this review.

### Options and decision

- Considered: official SDK v1 FastMCP; current official SDK v2 MCPServer; separate `fastmcp` distribution; stdio plus an HTTP adapter; a new package/subproject versus reusing the scaffold.
- Choose official `mcp` v1 FastMCP for this bounded, initialize-based demonstration, not the separate `fastmcp` distribution. The official release page currently lists v2.3.0 as latest and v1.30.0 as the maintenance release. v1 receives critical/security fixes only; it is not the latest major. This deliberate compatibility tradeoff preserves the required explicit initialize/list/call exercise without introducing a second API generation.
- Initial dependency target: `mcp==1.30.0`. Before implementation acceptance, verify that exact installed release exposes the selected public APIs and record its supported protocol revisions. Resolve direct `httpx`, `pydantic`, `starlette`, and `uvicorn` dependencies explicitly when imported; use `pytest` and YAML parsing support as development dependencies. Use the existing root `pyproject.toml`, generate `uv.lock`, and use frozen installs for repeatable local/container runs. Do not add a parallel requirements file or require the SDK CLI extra.
- Verified official v1 documentation/source exposes `from mcp.server.fastmcp import FastMCP`, `stateless_http=True`, `json_response=True`, `streamable_http_path="/mcp"`, `streamable_http_app()`, `custom_route()`, and `TransportSecuritySettings`. Use native Streamable HTTP, not a stdio adapter or legacy `/sse` transport. Preserve the SDK ASGI lifespan/session-manager lifecycle when wrapping the app for safe telemetry and HTTP serving.
- Official v1 source declares supported revisions `2024-11-05`, `2025-03-26`, `2025-06-18`, and `2025-11-25`. Target `2025-11-25` in the smoke test and record the actual initialize response. Stateless HTTP does not remove the v1 client's initialization exchange. Do not claim support for `2026-07-28`, or compatibility with any gateway/client not actually tested. Recheck these branch-level findings against the installed release before claiming compatibility.

### Tool contracts and data boundaries

Expose exactly three read-only tools with no caller-supplied arguments, typed structured results, descriptions, and read-only annotations. Annotations are hints, not enforcement. Reject unexpected arguments before any upstream activity; test this rather than assuming the SDK rejects extra keys.

| Tool | Input/data source | Result and boundary |
|---|---|---|
| `get_lab_overview` | Startup-loaded, curated public-safe configuration | Lab purpose, component roles, intended request path, and explicit limitations. Mark the data as configured/documentary, with a revision; never present it as live deployment discovery. |
| `list_model_presets` | Same curated configuration | Preset IDs, public model repositories, quantization, and brief descriptions. Label these configured presets, not downloaded, loaded, healthy, or inference-validated models. Initially match the four presets in `k8s/llm/llama-cpp.yaml`. |
| `get_model_health` | One operator-configured llama.cpp health URL | Timestamped server/router-level observation with HTTP status, bounded latency, and a safe outcome code. Even a successful router response leaves per-model loaded state and inference readiness unknown. No `/models`, `/v1/models`, model-specific query, inference, model loading, download, or deletion. |

- Configuration is an explicit small JSON file, not arbitrary repository/file access or runtime Markdown scraping. Load/validate it at startup and fail clearly on invalid configuration. Curate public-safe content only; no subscription IDs, kubeconfig, credentials, or private operator details. Include source/revision metadata to make drift visible.
- The health URL is set only by the operator at startup, defaulting in the prepared Kubernetes artifact to `http://llama-cpp.llm.svc.cluster.local:8080/health`. Local tests use a loopback stub. Allow only HTTP(S), a hostname and port, exact `/health`, no userinfo, query, or fragment. It is a trusted configuration boundary, not a general URL-fetch tool.
- Health execution makes at most one asynchronous `GET`, never follows redirects, ignores environment proxies (`trust_env=False`), verifies TLS when used, has a three-second overall deadline and a 16 KiB response cap, and performs no retries. Parse only the expected health response; do not forward raw bodies, headers, URLs, or exceptions to clients or logs.
- A valid `200` health response reports `healthy` at server scope only; a recognized loading response reports `loading`; other non-200 statuses report `unhealthy`. Timeout, connection/DNS failure, malformed/unexpected response, oversized response, and redirect report `unknown` with distinct safe reason codes. These are successful observations (`isError=false`), not proof the tool failed. Internal tool failures use a sanitized MCP error (`isError=true`); inspect both JSON-RPC errors and tool-result errors in tests.
- No runtime shell/subprocess execution, Kubernetes client/API access, Azure SDK, token, mounted kubeconfig, model-provider secret, persistence, or dynamic tool loading. Only the health tool performs downstream network I/O.

### Minimal implementation and packaging

- Reuse `main.py` as the entrypoint and small server module; replace the greeting stub because it has no lab behavior to preserve. Keep the root project and Python 3.12 baseline; no new framework scaffold, package tree, or separate dependency project.
- Planned new files: `config/lab-info.json`, `tests/test_lab_mcp.py`, `uv.lock`, `Dockerfile`, `.dockerignore`, and `k8s/mcp/lab-info.yaml`. Keep unit, failure, and HTTP smoke tests in the same test module initially. Update existing `pyproject.toml`, `README.md`, and handoff documentation during implementation. Split code only if actual complexity warrants it.
- `k8s/mcp/lab-info.yaml` will contain a dedicated namespace, read-only configuration ConfigMap, one-replica Deployment, and ClusterIP Service. Select `workload=app`; request no GPU and add no GPU/Spot tolerations. Set `automountServiceAccountToken: false`, non-root execution, read-only root filesystem, dropped capabilities, no privilege escalation, and modest CPU/memory requests and limits. No RBAC grants or credentials.
- The image uses locked dependencies and a pinned Python 3.12 base image, copies only necessary application/configuration files, and excludes Git, environments, caches, credentials, and kubeconfig. Use a local image tag for build testing; leave any future registry/image publication to separate authorization. Docker availability is an execution prerequisite, not a reason to create a registry.
- Serve `/mcp` on port 8000 with separate `/healthz` and `/readyz` application endpoints. Liveness checks only the MCP process; readiness checks its initialized configuration, not llama.cpp. Upstream failure must not restart the MCP server or disable overview/preset tools. These probes are not MCP compatibility tests.

### Exposure, authentication, and logging

- Local execution defaults to `127.0.0.1:8000`. Container/pod execution explicitly binds `0.0.0.0:8000`; local Docker publication must use `127.0.0.1:8000:8000`. Document loopback-only port-forwarding for a future authorized deployment, not as a deployment action in this milestone.
- Explicitly enable SDK DNS-rebinding protection with narrow Host and Origin allowlists in both modes, including only configured localhost/internal Service names and required ports. Do not disable protection for container binding, trust arbitrary forwarded headers, or add wildcard CORS. Requests without Origin remain usable by non-browser MCP clients; foreign supplied Origins and Hosts must be rejected. If probe traffic uses pod-IP Host headers, use an explicit safe probe Host or equivalent tested routing, not a wildcard exception.
- Initial mode has no application authentication or TLS and is suitable only for a trusted, operator-controlled local/internal lab. ClusterIP is neither authentication nor workload isolation; localhost is not per-user authorization. No NetworkPolicy enforcement or end-to-end confidentiality is claimed. Broader/customer access requires a separate authentication/TLS/network-control decision and security review. Do not add an Ingress, NodePort, LoadBalancer, public tunnel, or gateway route.
- Emit structured JSON lifecycle logs: startup/shutdown, safe MCP method/discovery outcome and tool count, allowlisted tool start/completion, elapsed time, safe outcome/error code, and server-generated correlation ID. Observe initialization through the tested SDK/ASGI path without maintaining a parallel protocol implementation or logging raw JSON-RPC.
- Never log raw arguments, request/response bodies, prompts, secrets, authorization/cookie/session headers, environment dumps, or unbounded caller-controlled identifiers/tool names. Sanitize/filter SDK, HTTP client, validation-error, and access logs too; SDK warnings may otherwise include supplied Host/Origin values and exceptions can expose URLs or arguments. Disable debug/body logging. Capture logs in adversarial tests to prove the policy, rather than assuming application logging alone controls dependencies.

### Acceptance gates and handoff

Developer implementation evidence (2026-10-22; not independent acceptance):

- Human constraint supersedes the earlier dependency-download prerequisite: only `https://packagefeedproxy.microsoft.io/pypi/simple` is approved. `pyproject.toml` sets it as uv's default index (replacing public PyPI); explicit approved-index commands and frozen installs are used locally and in Docker. No public fallback/direct download is permitted. Feed access succeeded without requesting secrets.
- The approved feed offers exact `mcp==1.30.0`. Installed signatures confirm the selected FastMCP settings, `streamable_http_app`, tool registration and HTTP client APIs. Runtime constants list `2024-11-05`, `2025-03-26`, `2025-06-18`, `2025-11-25`; a real HTTP SDK client negotiated `2025-11-25` with no persistent session ID. No v2 substitution or modern-protocol claim.
- The generated lock audit found 37 approved-registry entries and 177 artifact links, all under the feed-returned `ms-feed-25.pkgs.visualstudio.com` host, with SHA-256 hashes. Integrity hashes are not publisher-signature verification. Tests retain the source-policy check.
- Direct installed versions: Python 3.12.15, mcp 1.30.0, httpx 0.28.1, pydantic 2.14.1, starlette 0.52.1, uvicorn 0.54.0; development pytest 9.1.1 and PyYAML 6.0.3. The lock is the complete dependency record.
- FastMCP handler registration disables low-level input validation; explicit dispatch rejection of unexpected arguments/unknown names is therefore implemented and tested. The SDK's unsupported-version error reflects caller input; an outer constant-response protocol-header check prevents this leak. Health rejects compressed responses before decoding so the byte cap cannot be bypassed by unsolicited compression.
- Docker's daemon is unavailable. The Dockerfile pins a specific Python patch tag, but the tag's availability/digest and Linux build/runtime remain unverified; do not claim immutable-image or container acceptance. No registry/cloud workaround was used. Offline manifest and source/drift invariants are checked; no cluster operation occurred.

The gates below define independent acceptance, not Developer self-acceptance.
The final LOCAL verdict and remaining runtime gates are recorded after the checklist.

1. Developer records the exact resolved dependency versions, Python version, selected release's API support, and negotiated MCP revision. Frozen installation succeeds; all three input/output schemas and the configured-vs-observed distinction are tested. A drift test compares curated preset IDs/repositories/quantization against the existing llama.cpp ConfigMap and checks the packaged ConfigMap matches the curated JSON.
2. A real official SDK client uses `streamable_http_client` and `ClientSession` over a running loopback HTTP listener, calls `initialize()` (including the initialized notification), `list_tools()`, and `call_tool()` for all three tools. Assert exactly the named catalog, structured results, error semantics, negotiated `2025-11-25`, and no dependency on a persistent session ID. In-memory ASGI/direct function tests or HTTP 200 alone do not pass this gate. MCP Inspector is an optional walkthrough, not a substitute.
3. Deterministic local upstream tests cover valid health, loading/503, unexpected non-200, connection refusal/DNS failure, timeout, invalid JSON/schema, oversized response, and redirect. Assert the fixed method/path, no redirect following/retry/inference, bounded completion, safe codes, and that overview/presets and MCP readiness still work during failure. No live GPU/cluster dependency is allowed for these tests.
4. Negative HTTP tests reject foreign Host/Origin, unexpected tool arguments (including URL/path injection), unknown tools, malformed protocol input, and unsupported protocol use without unsafe output. Sentinel secrets supplied in bodies, headers, bad arguments, upstream responses, and exception paths must not appear in logs or errors. Verify local defaults/published ports remain loopback-only.
5. Validate manifest structure and invariants offline: one replica, app selector, no GPU, ClusterIP only, no token/RBAC, hardening, configuration mounts, explicit binding/allowlists, independent probes, and configurable image reference. Build/run the container and repeat HTTP smoke/probe tests if Docker/daemon is available. Otherwise record container build/run as BLOCKED/unverified, with the exact prerequisite; do not claim packaging runtime acceptance or provision a replacement registry/cluster.
6. Tester independently reruns behavioral gates; Security Reviewer checks information exposure, fixed egress target, logging, binding, token absence, and unauthenticated internal-only limitations. Architect accepts only the evidenced local milestone; any unexecuted gate stays explicit. Provide the requested code/configuration/transport/logging/container/Kubernetes walkthrough. Keep gateway, container, deployment, and MCP validation lifecycle claims separate.

### Historical three-tool LOCAL acceptance (2026-10-22; superseded)

**Verdict: ACCEPT the LOCAL source milestone for supervised loopback experimentation only.**

- Gates 1-4 PASS on recorded independent evidence: exact SDK/API/protocol and approved-feed/frozen dependency checks; exactly three no-argument read-only tools with structured curated-vs-observed results; real SDK HTTP initialize/list/all calls; fixed bounded GET health failure cases; transport/input rejection and response/log redaction. Source inspection confirms the SDK envelope guard behind the 64 KiB limiter and the telemetry `RecursionError` catch.
- Gate 5 offline artifact checks PASS; Dockerfile/manifest remain CREATED. The unavailable Docker daemon blocks build/run. Python base-tag availability/immutable digest, unhashed uv bootstrap provenance, Linux dependency execution, Kubernetes admission/scheduling/probes and live upstream behavior remain unverified, not accepted or waived as deployment gates.
- Gate 6 LOCAL independent reviews PASS: final Tester suite **54 PASS in 12.90s** plus two own direct-ASGI deep-input probes; final Security Reviewer suite **54 PASS in 13.22s**, with no response/log leaks or uncaught ASGI exceptions. Recorded invocations are in `docs/agent-execution-log.md`. Earlier malformed-envelope MEDIUM and telemetry recursion LOW findings were repaired and independently retested; earlier failed reviews remain historical evidence, not current blockers. README provides the requested walkthrough; delivery of a live human walkthrough is not claimed.
- Residual LOW findings accepted only in this supervised-loopback scope: no inbound slow-upload deadline/concurrency bound; mutable Python base and unhashed uv bootstrap. The application lock is not whole-container provenance. No authentication, TLS, NetworkPolicy isolation, shared/customer-ready exposure, container, cluster, live upstream or gateway validation is claimed.
- Rationale: the independent final results and inspected contracts satisfy the bounded local behavior/security criteria; unavailable container execution is explicitly permitted as a recorded unverified gate by criterion 5. Accepting this evidence does not expand scope or require further assurance-only suite runs. Phase 8 stays PLANNED/paused; independent D-011 router validation remains separate before Phase 9. No broad phase completion or deployment authorization follows.

The main coordinator owns invocation logging; this final bounded Architect pass
updates only `STATUS.md`, `docs/architecture.md`, this decision and `README.md`.
No code/configuration changes, new files, downloads, delegation, deployment,
commit or push are part of this acceptance.

### Rationale, tradeoffs, and revisit conditions

Three argument-free tools and one fixed GET teach MCP discovery/invocation without administrative access, inference cost, or an agent framework. Reusing the scaffold and native SDK transport minimizes moving parts. Curated content can drift, so provenance and drift checks are required. Stateless operation sacrifices subscriptions/session features this demo does not need. Router health cannot establish per-model readiness. Unauthenticated ClusterIP HTTP is a documented lab limitation, not a customer-ready security boundary.

Revisit the SDK major when 2026-protocol support is required, v1 support ends, a security fix requires migration, or the intended client cannot interoperate. Revisit permissions/exposure before adding arguments, new network targets, write operations, Kubernetes access, shared customer access, authentication, or gateway integration. Do not silently relax the fixed-target or security constraints to make a test pass.

Official evidence reviewed on 2026-10-22:

- [SDK releases, including v1.30.0 and v2.3.0](https://github.com/modelcontextprotocol/python-sdk/releases) and [support policy](https://github.com/modelcontextprotocol/python-sdk/blob/main/VERSIONING.md).
- [v1 server/transport/structured-result documentation](https://github.com/modelcontextprotocol/python-sdk/blob/v1.x/docs/server.md) and [v1 HTTP client example](https://github.com/modelcontextprotocol/python-sdk/blob/v1.x/docs/client.md).
- [FastMCP settings and ASGI lifecycle](https://github.com/modelcontextprotocol/python-sdk/blob/v1.x/src/mcp/server/fastmcp/server.py), [Host/Origin validation](https://github.com/modelcontextprotocol/python-sdk/blob/v1.x/src/mcp/server/transport_security.py), [supported versions](https://github.com/modelcontextprotocol/python-sdk/blob/v1.x/src/mcp/shared/version.py), and [v1 latest protocol constant](https://github.com/modelcontextprotocol/python-sdk/blob/v1.x/src/mcp/types.py).
- [Current v2 API](https://github.com/modelcontextprotocol/python-sdk) and [protocol roadmap](https://github.com/modelcontextprotocol/python-sdk/blob/main/ROADMAP.md). These establish the distinction from v1, not tested interoperability in this lab.

### Teaching simplification amendment (LOCAL VALIDATED, 2026-10-22)

This contract supersedes the three-tool/schema/telemetry requirements above for
the bounded local teaching revision. It was initially planned without execution;
subsequent implementation and independent evidence support the acceptance below.
Historical three-tool acceptance is not evidence for the simplified source.

- Context: a reader with some Python wants a 10-15 minute code walkthrough,
	followed later by a separate 10-15 minute Kubernetes/gateway discussion.
	Workload comments remain useful; Python tutorials and elaborate metadata do not.
- Decision: exactly two argument-free tools. `get_lab_overview` returns static
	public-safe purpose/components/intended path and the existing configured model
	presets from the JSON file. One plain description identifies these as configured
	information; remove runtime kind/revision/source/readiness metadata scaffolding.
	`get_model_health` makes only the fixed operator-configured GET `/health`.
- Implementation shape: plain official `FastMCP`, SDK 1.30.0, stateless JSON
	Streamable HTTP `/mcp`; retain a small app factory for existing tests. Remove
	`LabMCP`, `SafeHTTP`, custom protocol parsing/body replay/correlation telemetry,
	and the output-model hierarchy. Prefer ordinary dictionaries and existing files,
	no new framework, client, harness, guard module, or dependency migration. Target
	about 160-220 lines in main.py including concise workload comments, not a hard cap.
- Host/security: retain loopback defaults and current operator environment names,
	explicit container bind, exact non-wildcard Host/Origin allowlists, enabled SDK
	DNS-rebinding protection and its 64 KiB MCP request limit. Disable proxy-header
	trust. Check custom probes with the SDK request validator directly because
	SDK MCP protection must not be assumed to cover custom routes. No authentication,
	TLS, NetworkPolicy, shared/customer or cluster exposure is accepted.
- Upstream: validate HTTP(S), hostname/port, exact `/health`, no userinfo/query/
	fragment at startup. Keep one GET, three-second overall deadline including body
	consumption, 16 KiB streamed cap, compression rejection, no redirects/retries/
	environment proxies, and normal HTTPS certificate validation. No inference,
	model administration, shell, Kubernetes credentials or discovery.
- Health result: only `status`, `reason`, `http_status` (null without a response).
	Use `healthy/health_ok` only for HTTP 200 plus an object with `status: ok`;
	`loading/model_loading` only for 503 plus `status: loading model`; other 4xx/5xx
	are `unhealthy/http_error`. Unexpected/malformed 200 or mismatched health status
	is `unknown/invalid_response`; redirects, timeout, connection failure, oversize
	and compression use fixed safe reasons. Ignore unrelated JSON fields without
	returning them. This observes router health, never per-model inference readiness.
	Expected upstream failures return normal tool results, not MCP execution errors.
	Unexpected application handler errors use constant `ToolError` messages.
- Probes/logs: preserve `/healthz` and `/readyz`, configuration-loaded MCP process
	only, no upstream I/O. Keep small safe startup/shutdown and handler outcome logs;
	suppress SDK/dependency/access diagnostics, no raw payloads, headers, URLs,
	exception text, caller IDs, body parsing for logs or discovery instrumentation.
- Scoped tradeoff: choose SDK-only HTTP handling over retaining the isolated
	envelope guard for this supervised localhost lesson. The prior MEDIUM SDK
	malformed-envelope/protocol-header reflection risk returns; log suppression
	does NOT sanitize SDK responses. Loopback is not authorization against other
	local processes/users. SDK-ignored extra arguments may remain ignored: discovery
	has no parameters, and extras must never select a URL/file/action. Do not promise
	strict rejection or equivalent redaction. Untrusted callers/inputs or broader
	access require reconsidering the guard and a separate security/exposure review.
	LOW inbound upload deadline/concurrency and container provenance remain unresolved.
- Acceptance: adapt the existing test module/helpers, not the old 54-test count.
	Require real loopback SDK initialize/list/both calls with exactly two tools,
	protocol 2025-11-25 and stateless behavior; static overview works with upstream
	down; fixed-target health success/loading/false-positive 200/failure matrix;
	bounded slow-body/size behavior, no redirects/retries/proxy use; SDK Host/Origin
	rejection on MCP and probes; application error/log sentinel checks. Explicitly
	characterize residual SDK reflection rather than requiring old guard assertions.
	Test extra-key target invariance, not nonexistent strict SDK rejection. Keep
	offline preset/ConfigMap drift, manifest hardening and approved-feed/lock checks.
- Files for Developer: main.py, existing tests, JSON, README and architecture
	description; synchronize only embedded JSON in the offline MCP manifest when
	needed. Keep Docker paths/port/probes, Service type, app placement and hardening
	unchanged; Dockerfile need not change if its interface stays compatible.
	No installs/network/build/deployment in this planning pass. Keep the existing
	lock/dependencies and approved feed only; public PyPI/fallback is prohibited.
- Revisit/acceptance: local implementation and its new tests must precede renewed
	acceptance. Packaging/Linux/probes in Kubernetes and live upstream remain
	unverified. Phase 8 stays paused; this is not gateway authorization. An external
	publication may explain this server, while agent/harness orchestration remains
	outside it; no article or harness work is part of this revision. Main coordinator
	owns the execution log; no agent invocation is claimed here.

### Final two-tool LOCAL acceptance (Architect, 2026-10-22)

**Verdict: ACCEPT the amended LOCAL source milestone for supervised loopback experimentation only.**

- Inspected source matches the amendment: 212 lines, plain official SDK 1.30
	FastMCP, exactly two no-parameter tools, static overview including configured
	presets, three-field health result, no wrappers or output-model hierarchy.
- Independent Tester: **63 PASS in 13.95s** plus own actual SDK HTTP
	initialize/list/both calls, negotiated `2025-11-25`, no session ID, fixed GET
	`/health` despite extra target arguments, slow-body timeout **3.006s**,
	upstream-independent overview/probes, Host/Origin enforcement, safe application
	errors/logs and cleanup. Security Reviewer: **63 PASS in 13.90s** plus
	**23 supplemental checks**, acceptable only for supervised loopback, no new
	scoped blocker. The coordinator's `docs/agent-execution-log.md` records both.
- These results cover the amended protocol, bounded health/failure, transport,
	error/log, target-invariance and offline drift/hardening/approved-feed gates.
	SDK response reflection is explicitly characterized, not sanitized: the known
	MEDIUM is retained in this narrow scope. Strict extra-key rejection and former
	54-test source protection are not promised. LOW upload deadline/concurrency and
	container provenance remain unresolved; shared/untrusted access requires review.
- README's twelve-minute agenda fits the requested code-first teaching structure;
	no live delivery or measured duration is claimed. Kubernetes/gateway is reserved
	for a separate later 10-15 minute discussion, not part of this acceptance.
- Container/Linux runtime, Kubernetes deployment/probes, live upstream and
	gateway behavior remain unverified. Dockerfile/manifest stay CREATED. No broad
	phase is accepted; Phase 8 stays paused and D-011 independent router validation
	remains a prerequisite before Phase 9. Approved-feed-only policy is unchanged.
- This documentation-only verdict uses existing independent evidence without
	rerunning tests. No code, new files, installs, network/cloud, Docker, client,
	article, delegation, execution-log edits, commit or push. Next: deliver the
	local code walkthrough; seek separate authorization for runtime/deployment work.

### MCP Kubernetes deployment request (2026-10-23; historical pause, superseded by D-013)

The human now authorizes deploying this MCP component to the existing AKS lab,
not gateway installation, public exposure or new Azure infrastructure. This
supersedes earlier deployment pauses, but does not extend LOCAL security
acceptance automatically. No deployment has occurred.

Independent predeployment Security Reviewer verdict: NO-GO as-is. ClusterIP and
Host/Origin checks do not authenticate cluster callers. Proposed isolated-lab
boundary: deny MCP pod ingress, use operator-only loopback port-forwarding and
restrict egress to required DNS and actual llama.cpp pods on TCP 8080. Human
approval and dataplane enforcement evidence are pending; no policies were
created. An L4 rule cannot constrain traffic to `/health` or exclude other
llama.cpp endpoints. SDK reflection, plaintext HTTP, inbound availability and
base/bootstrap provenance remain residual decisions, not accepted risks here.

Build/delivery gates are also unresolved: Docker daemon unavailable, local ARM64
versus target AMD64, no approved registry destination or verified pull access.
Do not replace these gates with a new registry, cloud build service, RBAC change
or risk exception without human approval. Preserve simple teaching code unless
a separately approved security decision requires changing it.

Subsequent human response: Docker is reportedly running (not rechecked), and a
dedicated lab registry is approved but not created. The human chose to pause
deployment for an explanation of network-isolation tradeoffs. NetworkPolicies
were not approved at that point. D-013 records subsequent approval and lifts
this pause for the reviewed MCP scope; the LOCAL acceptance above is unchanged.

## D-013 Two-phase MCP network boundary (human-approved design, 2026-10-23; PLANNED)

Current authority: D-014 supersedes this decision's immediate isolation gate and
predeployment NO-GO for the trusted supervised single-operator MVP only. Both
phases below remain future hardening designs; the original rationale and evidence
are retained, not claims of implemented isolation.

### Context and alternatives

The human approves both phases below and authorizes resuming the reviewed MCP
deployment work on existing `aks-agw-lab`. ClusterIP and Host/Origin checks alone
do not isolate callers. Options considered: retain unrestricted internal access;
isolate MCP now with operator API port-forwarding; install a gateway immediately.
Choose isolation now and a narrowly selected gateway path later: this separates
the MCP learning milestone from gateway installation without adding Python guards.

### Decision: Phase 1, operator-only access

- Use dedicated namespace `mcp`. NetworkPolicy selects MCP pods (the prepared
	manifest uses `app: lab-info`) and denies ordinary pod-network ingress.
- Operator access uses authenticated, authorized Kubernetes API port-forwarding
	bound explicitly to localhost only. This is an administrative API access path,
	not an ingress allow rule or application authentication. Do not broaden RBAC.
- Isolate MCP egress: allow only required cluster DNS and the actual llama.cpp
	pods in namespace `llm` on TCP 8080; deny other direct pod/external connections.
	Verify DNS endpoints/protocols and actual namespace/pod labels before authoring
	selectors. Select llama.cpp with combined namespace AND pod selectors in the
	same peer, not separate OR alternatives; do not allow the whole `llm` namespace.

### Decision: Phase 2, future gateway-only ingress

- Later allow only intended gateway pods to reach the MCP listener on TCP 8000,
	using combined namespace AND pod selectors in the same ingress peer. Keep all
	other ordinary ingress denied and retain Phase 1 egress restrictions.
- Verify the actual gateway deployment identity, namespace and pod selectors
	before creating that rule. No gateway is presently installed or selected by
	this decision; do not fabricate labels or pre-authorize a whole namespace.
	Gateway installation/integration is separate future work, not authorized now.

### Limits, tradeoffs and acceptance gates

- NetworkPolicy is L3/L4 reachability control, not client authentication, TLS or
	HTTP path filtering. TCP 8080 permission cannot restrict access to `/health`
	versus llama.cpp's other endpoints. A Host allowlist checks the requested
	destination authority, not caller identity. Permitting DNS is not strict
	information-exfiltration prevention; DNS queries remain a possible channel.
- Do not claim literally nobody else can connect: node/kubelet traffic has
	NetworkPolicy exceptions, and privileged administrators/API forwarding are
	outside ordinary pod isolation. Localhost is not per-user authentication.
	Namespace/pod source labels are administrator-controlled, not cryptographic
	workload identity; control who can assign labels or create matching workloads.
- Policies are additive: inspect all policies selecting MCP and relevant peers
	for allowances that widen the boundary. Verify the cluster's actual CNI policy
	support and enforcement; an accepted manifest alone proves neither. Independent
	tests must demonstrate allowed operator/DNS/llama.cpp paths and denied unrelated
	ingress/egress, including same-namespace callers. Repeat for the real gateway
	and non-gateway callers before accepting Phase 2.
- The prior predeployment NO-GO is not cleared by design approval. After isolation
	and image evidence, require independent Tester validation, Security Reviewer
	review and Architect acceptance. Known SDK response reflection MEDIUM and
	availability/provenance LOW findings remain unresolved, not automatically
	risk-accepted here. Plaintext HTTP remains an explicit review limitation.
- Scope: existing lab only, with the previously approved dedicated lab registry
	as the sole infrastructure expansion. No public exposure, unrelated resources,
	gateway installation or silent RBAC expansion. Recheck reported Docker readiness;
	verify image provenance, Linux AMD64 execution, delivery and cluster pull access.
	Approved-feed-only dependency policy remains unchanged.
- State: approved design only, not deployed or enforced. No MCP image has been
	built/pushed, registry created, container run, NetworkPolicy created/applied or
	MCP cluster deployment performed. Subsequent Developer checks confirm Docker
	29.5.3 running, Linux ARM64, with builder-advertised AMD64 support; no AMD64
	execution has been proven yet.
- Subsequent live prerequisite evidence: AKS reports `networkPolicy: none` and
	`networkDataplane: azure` with Azure CNI overlay. Do not assume NetworkPolicy
	objects enforce this decision on the current cluster. A supported enforcement
	change needs Architect planning, existing-workload impact assessment and separate
	human approval before cluster mutation; D-013 does not authorize that migration.
	DNS Service selector is `k8s-app=kube-dns` (UDP/TCP 53); llama.cpp selector is
	`app=llama-cpp`. Only existing policy is `kube-system/konnectivity-agent`.
- Revisit before shared/untrusted access, new egress targets, gateway integration,
	identity/TLS changes or any wider infrastructure/RBAC scope. Keep changes
	reversible: Phase 2 can remove its gateway allowance to return to Phase 1;
	rollback must not silently restore unrestricted access.

## D-014 Trusted supervised MCP lab MVP (human-approved amendment, 2026-10-23; PLANNED)

Current authority: the heading retains its original design-state text for stable
links. The final architectural acceptance below supersedes that PLANNED state
and pre-execution observations for this bounded MCP milestone only: VALIDATED.

### Authority, context and decision

The human explicitly approves documenting the reduced-isolation recommendation
and moving toward MCP deployment. This amends D-013 for the trusted, supervised,
single-operator lab MVP, not shared/customer/production use. Options: migrate to
Cilium before MCP; defer enforcement with explicit trust assumptions; install a
gateway now. Choose deferral to preserve the simple roughly ten-minute two-tool
code lesson and avoid cluster-wide disruption. No Python redesign is required.

- Last recorded AKS settings: `networkPlugin: azure`, `networkPluginMode: overlay`,
  `networkDataplane: azure`, `networkPolicy: none`. No fresh checks in this pass.
  Defer Cilium and NetworkPolicy enforcement; no networking migration, node-pool
  reimage or policies presented as enforced without an enforcement engine.
- MVP: dedicated `mcp` namespace, one app-pool replica, ClusterIP HTTP and operator
  localhost-bound Kubernetes API port-forwarding. Other pods CAN reach MCP;
  outbound traffic is NOT restricted by this design. Fixed application GET
  `/health` limits the tool's behavior, not pod networking. Host/Origin checks
  are not caller authentication; localhost forwarding does not isolate the pod.
- Known SDK response reflection MEDIUM, inbound availability LOW, no application
  authentication/TLS and incomplete packaging provenance remain explicit residuals.
  Human accepts reduced isolation as MVP direction; these findings are not fixed.
  The earlier isolation-based NO-GO is not a mandatory deployment gate in this
  bounded scope. Independent security review follows and must assess actual
  image/runtime evidence and residuals; this is not independent security acceptance.
- Preserve D-013 Phase 1 (operator path plus enforced ingress/egress restriction)
  and Phase 2 (verified namespace AND pod-selected gateway ingress) as future
  hardening. Neither is implemented or required before this MVP. Reassess supported
  enforcement, additive policies and actual allow/deny behavior when resumed.

### Bounded Developer contract, before execution

1. Target existing `aks-agw-lab` in `rg-aks-agw-lab`; every Kubernetes operation
	explicitly selects `--context=aks-agw-lab`. Active context is last recorded as
	unrelated `litellm-demo-aks`; do not use or silently switch it. No gateway
	install/integration, public exposure, unrelated infrastructure or networking changes.
2. Plan the previously approved dedicated lab ACR, including recurring cost,
	name/SKU/location and reproducible creation. Assess the exact permission path
	before executing: operator identity and existing registry-create authority,
	authenticated image-push authority, actual AKS kubelet principal, registry role
	mode, and authority to assign the pull role. Planned deployment minimum is
	`AcrPull` for that kubelet principal at that registry's resource scope only,
	not the control-plane identity, resource group or subscription. Confirm the
	registry mode supports this role; if not, return for a decision. Do not grant
	broader roles to make creation/push/assignment succeed. Missing authority is a
	blocker to surface, not implicit approval. No admin passwords or image-pull secrets.
3. Build the exact current two-tool source for `linux/amd64`; record source
	provenance, base/bootstrap inputs, approved-feed frozen dependencies and image
	digest. Resolve/review mutable base and unhashed bootstrap provenance before
	claiming packaging acceptance. Docker 29.5.3 ARM64 and builder-advertised AMD64
	support are historical facts, NOT execution proof. Prove AMD64 container
	execution, push the image, and replace `lab-info:dev` / `imagePullPolicy: Never`
	with a pullable immutable registry digest and suitable pull policy.
4. Preserve app-only placement, no GPU, non-root/read-only filesystem, dropped
	capabilities, seccomp, no privilege escalation, no ServiceAccount token/RBAC,
	resource bounds, narrow Host/Origin lists and upstream-independent probes.
	Keep exactly `get_lab_overview` and `get_model_health`; no wrappers/new framework.
5. Independently validate image pull/digest/AMD64 runtime, scheduling/security
	settings, `/healthz` and `/readyz`, then real SDK HTTP initialize/list/call for
	both tools through localhost forwarding. Check tool results/errors and live
	fixed-target health without inference; upstream failure must not disable static
	overview/probes. Historical 63 PASS is LOCAL source evidence, not this smoke test.

### Acceptance, tradeoffs and revisit

Developer implements; Tester independently validates runtime; Security Reviewer
independently reviews the trusted-lab exposure, reflection, availability, plaintext,
identity and provenance; Architect accepts only that evidenced scope. New findings
need explicit disposition, not an automatic waiver. No cluster isolation or
shared/customer readiness can be accepted under this decision. D-011 independent
router validation remains separate before gateway integration.

Revisit before additional operators, shared/untrusted callers or workloads,
gateway integration, public access, new tools/targets, or identity/TLS changes.
Deferral avoids reimage/downtime but trusts reachable workloads and the operator;
stop/roll back MCP if that assumption fails. At design approval, this was a
deployment design only: registry/image/runtime/MCP deployment were unbuilt or
unverified. The final acceptance below supersedes that historical state.

### Final architectural acceptance (2026-10-23; bounded VALIDATED)

DECISION: ACCEPT the deployed MCP milestone for trusted, supervised,
single-operator lab use only. The recorded independent evidence satisfies the
bounded contract; no new runtime/cloud checks or tests were needed for this
documentation-only review. Reports: [agent-execution-log.md](agent-execution-log.md).

- Delivery: isolated Basic ACR `acragwlabd18f2ff3`, southeastasia, admin/anonymous
	disabled, traditional registry RBAC. Existing operator authority was assessed;
	only registry-scoped kubelet AcrPull was added. Server validation and reviewed
	what-if showed two creates, AKS Ignore and no other mutations.
- Artifact: `acragwlabd18f2ff3.azurecr.io/lab-info@sha256:29f6d6d123c54cec36ca64c104ff55450de823a27b52d3a1db75cdfd8e320b76`.
	Independent Tester matched deployed imageID/source and confirmed a Ready AMD64
	CPU app-pool replica, zero restarts, UID/GID 10001, read-only rootfs, no effective
	capabilities/escalation/ServiceAccount token, seccomp, resource bounds/probes
	and ClusterIP only. Base/bootstrap/dependency hashes and frozen approved-feed
	packaging were reviewed; native export avoids the reproduced QEMU uv crash
	without application behavior changes. This is not whole-image certification.
- Behavior: independent Tester 63 PASS in 13.87s; official SDK HTTP protocol
	2025-11-25, exactly two argument-free tools, structured results/no session ID,
	live fixed health healthy/health_ok/200, probes 200, Host/Origin 421/403.
	The same cached image with networking disabled independently preserved
	overview/probes while health returned unknown/connection_failed. Temporary
	container/forward removed and port 18000 free at cleanup.
- Security: independent read-only review GO only for continued D-014 trusted-lab
	use; no new CRITICAL/HIGH in inspected artifacts/configuration. Accept existing
	MEDIUM SDK input reflection and unauthenticated plaintext/unrestricted internal
	reachability/egress, plus LOW inbound availability, within this boundary only.
	These risks are not fixed. Require trusted reachable workloads and public-safe
	synthetic lab data; this network is not a secure production boundary.
- Exclusions: D-013 both phases remain future hardening; Cilium migration is
	deferred, not approved. No NetworkPolicy, gateway, public application exposure,
	shared/customer/production readiness or inference acceptance. D-011 independent
	router validation still gates gateway integration; Phase 8 remains paused.
- Handoff: human may use explicit-context localhost port-forwarding documented
	in [README.md](../README.md); no public application URL or running local forward
	is claimed. Overview revision 2026-10-22.1 remains historical static teaching
	data, not deployment inventory. D-012 LOCAL acceptance/history is unchanged.

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
