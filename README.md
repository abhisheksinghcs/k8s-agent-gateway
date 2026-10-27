# k8s-agent-gateway

Reproducible AKS lab for GPU-backed open-weight models: client -> agentgateway -> llama.cpp -> NVIDIA GPU.

Current state, plan and blockers: [STATUS.md](STATUS.md). Design: [docs/architecture.md](docs/architecture.md). Rules for agents and contributors: [PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md).

## Prerequisites check (read-only)

```bash
LOCATION=westus2 ./scripts/preflight.sh
```

No secrets belong in this repository.

## Python lab-information MCP server (LOCAL source VALIDATED)

Python 3.12, official `mcp==1.30.0` maintenance SDK, native stateless
Streamable HTTP at `http://127.0.0.1:8000/mcp`. Independent SDK HTTP tests negotiate
`2025-11-25`; no claim is made for `2026-07-28` or gateway interoperability.
Architect accepts this D-012 two-tool teaching revision for supervised loopback
only: independent Tester **63 PASS in 13.95s** plus own SDK HTTP probes;
Security Reviewer **63 PASS in 13.90s** plus **23 supplemental checks**.
This supersedes historical three-tool/54-test acceptance for current source,
not its stronger response-protection guarantees. Evidence is recorded in
[docs/agent-execution-log.md](docs/agent-execution-log.md). D-014 now separately
permits a deployed trusted, supervised lab MVP: independent Tester 63 PASS plus
live AMD64 pod/SDK/probe checks, live health 200, Security Reviewer GO with
explicit residuals. Architect ACCEPTS the D-014 MCP milestone as VALIDATED only
for trusted, supervised, single-operator lab use. D-015's CPU-only gateway/MCP
path is separately ACCEPTED, bounded VALIDATED with independent SDK/runtime
evidence below; live gateway outage behavior remains deferred, not proven.
D-011 has final bounded architectural ACCEPT (2026-10-27), clearing historical
explicit offload and final-runtime/security prerequisites. Model routing remains unimplemented and is not
authorized by that review; Phases 9/10 stay PLANNED. See the current verdict in
[STATUS.md](STATUS.md#current-d-011-architectural-acceptance-2026-10-27).

Known MEDIUM residual: plain SDK errors can reflect malformed input, unsupported
protocol headers and unknown tool names. Log suppression does not sanitize SDK
responses; removing the old guard is not equivalent protection. Supervised
loopback experimentation only: localhost is not authorization against other
local processes/users. LOW limitations remain: no inbound upload deadline or
concurrency bound. Deployment pins the base image and hashes the approved-feed
bootstrap/dependencies; this is not whole-image security certification. No shared/
customer exposure, authentication, TLS or NetworkPolicy acceptance is claimed.

### Approved dependencies

Only `https://packagefeedproxy.microsoft.io/pypi/simple` is permitted.
The default uv index in [pyproject.toml](pyproject.toml) replaces implicit
public PyPI. Do not add extra indexes, public download URLs or fallbacks.
The lockfile records this feed and its returned Microsoft artifact URLs
under `ms-feed-25.pkgs.visualstudio.com`, with SHA-256 hashes. These hashes
provide artifact integrity, not a verified publisher signature/attestation.
If access requires secrets, tell the coordinator; never send them through chat.

```bash
UV_PYTHON_DOWNLOADS=never uv venv --python /path/to/approved/python3.12 .venv
UV_INDEX=https://packagefeedproxy.microsoft.io/pypi/simple UV_DEFAULT_INDEX=https://packagefeedproxy.microsoft.io/pypi/simple UV_PYTHON_DOWNLOADS=never uv sync --frozen --default-index https://packagefeedproxy.microsoft.io/pypi/simple
.venv/bin/python -m pytest -q tests/test_lab_mcp.py
.venv/bin/python main.py
```

For an intentional dependency update, use `uv lock --default-index
https://packagefeedproxy.microsoft.io/pypi/simple` with the same environment
overrides, then inspect **all** registry/artifact sources before syncing.
Rerun `test_approved_dependency_and_container_sources` after regeneration.
Do not silently substitute the SDK version if it becomes unavailable.

### Configuration and tools

[main.py](main.py) is the entrypoint and server implementation. Start with
[config/lab-info.json](config/lab-info.json), then follow these functions:

- `health_url` and `load_overview`: validate operator configuration at startup. The shared JSON/ConfigMap shape is unchanged; runtime overview omits revision/source scaffolding and includes purpose, components, intended path, limitations and configured `models`.
- `observe_health`: one GET to the fixed exact `/health`, with a 3-second overall deadline, 16 KiB streamed cap, no redirects/retries/environment proxies, compression rejection and normal HTTPS verification. It returns only `status`, `reason`, `http_status`. Only 200 plus `status: ok` is healthy; only 503 plus `status: loading model` is loading. Other 4xx/5xx are unhealthy; malformed/mismatched expected responses are unknown. No inference or model administration occurs.
- `create_app`: plain official FastMCP registers exactly `get_lab_overview` and `get_model_health`, both without caller parameters. String-key dictionary annotations give structured output without schema classes. Expected upstream failures are observations (`isError=false`); unexpected application failures use constant `ToolError` (`isError=true`). SDK-ignored extra arguments cannot choose a URL, path or action; strict rejection is not promised.
- SDK HTTP handling owns initialization/discovery/dispatch and the 64 KiB MCP request cap. Narrow Host/Origin DNS-rebinding protection remains enabled. Custom `/healthz` and `/readyz` explicitly use its request validator and never contact the upstream. No custom envelope parsing, request replay, correlation or HTTP telemetry remains.
- `configure_logging` and the SDK lifespan hook: small startup/shutdown and handler-outcome logs only. Dependency/access diagnostics are suppressed, and proxy-header trust is disabled. No raw payloads, URLs, headers, caller IDs or exception text are logged by the application. This is not gateway/agent tracing or SDK response redaction.

| Variable | Default / use |
|---|---|
| `LAB_HOST` | `127.0.0.1`; only explicit `0.0.0.0` enables pod/container binding |
| `LAB_PORT` | `8000` |
| `LAB_CONFIG` | `config/lab-info.json`; validated once, restart to reload |
| `LAB_HEALTH_URL` | `http://127.0.0.1:8080/health`; trusted operator setting, no userinfo/query/fragment |
| `LAB_ALLOWED_HOSTS` | `127.0.0.1:<port>,localhost:<port>`; comma-separated exact values, no wildcards |
| `LAB_ALLOWED_ORIGINS` | matching `http://` loopback origins; absent Origin is permitted for non-browser clients |

No llama.cpp server is needed to run or test MCP. With the default unavailable
upstream, the health tool returns a safe `unknown` observation while overview
(including presets) and application readiness still work. Tests use local stubs, real SDK
HTTP initialization/discovery/calls, and clean up their own listeners. To run
the HTTP smoke alone: `.venv/bin/python -m pytest -q tests/test_lab_mcp.py -k sdk_http`.
Stop the interactive server with Ctrl-C.

### Twelve-minute local walkthrough

Proposed agenda for a non-developer with some Python; delivery and duration
have not been measured.

Use the existing frozen `.venv`; these steps do not install dependencies or
require llama.cpp, Docker, a cluster, a new client or an agent framework.

1. **Minutes 0-2, run it.** In one terminal run `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python main.py`. In another run `curl --noproxy '*' http://127.0.0.1:8000/readyz`. The probe checks this information service, not GPU capacity. Stop with Ctrl-C after the walkthrough. If 8000 is occupied, set `LAB_PORT=8001` and use that port for the probe.
2. **Minutes 2-5, read the contracts.** Open [main.py](main.py), starting at its reading map, then [config/lab-info.json](config/lab-info.json). Trace `load_overview` into `get_lab_overview`: static context and all four configured presets, not a live model inventory. Trace the operator's `LAB_HEALTH_URL` into `get_model_health`: callers cannot change it.
3. **Minutes 5-9, follow the live observation.** Read `observe_health`: one streamed GET, timeout/size/compression limits, then the three-field dictionary. Healthy router does not prove model inference. Read the two decorators and `create_app`: the SDK supplies MCP, not an agent loop. Application errors are constant; the disclosed SDK reflection remains.
4. **Minutes 9-12, see the protocol work.** Run `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/test_lab_mcp.py -k 'sdk_http or upstream_failure' -p no:cacheprovider`. Existing tests start temporary loopback listeners, initialize the official client, discover exactly two tools, call both, then stop all listeners. The failure case proves overview/probes stay usable without llama.cpp. Read `exercise_sdk` in [tests/test_lab_mcp.py](tests/test_lab_mcp.py) beside the results.

Reserve Kubernetes Service/pod binding, app-pool placement and the gateway route
for the **separate 10-15 minute discussion** below. The local lesson itself does
not prove gateway behavior; no delivered live human walkthrough is claimed.

### Presenter reference: how the file fits together

The story is: "An MCP client discovers two tools. One returns configured lab
information; the other makes a bounded request to a real service. The SDK handles
the protocol; our functions supply the capabilities."

Read [main.py](main.py) in execution order rather than top-to-bottom:

| Step | Code | Responsibility and contract |
|---|---|---|
| 1 | `main()` | Resolve operator settings, assemble the application, then start Uvicorn. Invalid startup configuration stops the process. |
| 2 | `configure_logging()` | Suppress generic diagnostics and record only controlled lifecycle/handler outcomes. This does not sanitize SDK responses. |
| 3 | `create_app()` | Connect configuration, the SDK transport, two tools and probes; separate assembly from listening so tests can reuse it. |
| 4 | `health_url()` | Validate the fixed operator-selected HTTP(S) `/health` address. No credentials, query, fragment or whitespace; valid optional port. No DNS or connectivity check occurs here. |
| 5 | `load_overview()` | Read/validate JSON once and combine lab context with configured models into the static tool result. Restart to pick up file changes. |
| 6 | `lifespan()` | Log application startup/shutdown, not individual tool calls. |
| 7 | Tool registration | `@server.tool` exposes `get_lab_overview` and `get_model_health`; the SDK advertises and dispatches them. Neither accepts a caller-selected target. |
| 8 | `observe_health()` | On each health invocation, make one fixed GET with a three-second overall deadline and 16 KiB streamed cap. Return `status`, `reason`, `http_status`. |
| 9 | `probe()` | Serve ordinary HTTP `/healthz` and `/readyz` routes with SDK Host/Origin validation, independent of llama.cpp. |

`LAB_HOST`/`LAB_PORT` are inbound: where this MCP app listens. `LAB_HEALTH_URL`
is outbound: where its health tool sends a request. `LAB_CONFIG` selects local
documentary data. Host/Origin allowlists restrict request authorities/origins,
not client IPs or tool destinations; they are not authentication. The operator
controls these settings at startup, not the MCP client.

The static tool does not query Kubernetes or discover loaded models. The live
tool recognizes HTTP 200 plus JSON `status: ok` as healthy and HTTP 503 plus
`status: loading model` as loading. Other 4xx/5xx responses are unhealthy;
connection/timeout/malformed responses produce an unknown observation with a
fixed reason. Health checking does not run inference. Unexpected application
failures use a constant `ToolError`; known SDK error reflection remains separate.

The probes answer "is this information service available?", not "is the GPU
upstream available?" Its static tool stays useful during an upstream outage,
and restarting the MCP service cannot restore Spot GPU capacity.

### Presenter reference: application lifecycle

The `@asynccontextmanager` decorator lets FastMCP enter and exit this lifecycle:

```python
@asynccontextmanager
async def lifespan(server):
	APP_LOG.info("startup")
	try:
		yield
	finally:
		APP_LOG.info("shutdown")
```

FastMCP receives it through `lifespan=lifespan`. Before `yield`, startup code
runs. At `yield`, control returns to the SDK while the application serves
requests. When the lifecycle exits, `finally` runs the shutdown code. This is
application lifecycle, not once per request/tool. In this lab it only logs;
other applications could acquire/release shared resources here. Cleanup is
not guaranteed after a forced process kill.

Presenter wording: "This brackets the application's lifetime: initialize,
serve requests, then clean up. It does not implement the agent loop."

### Presenter reference: tool annotations and security

The same annotations are attached to both tools through
`@server.tool(annotations=annotations)` and advertised during MCP discovery:

| Annotation | Intended meaning for these tools |
|---|---|
| `readOnlyHint=True` | Read configuration or health; do not intentionally modify the target. |
| `destructiveHint=False` | No destructive operation is intended. |
| `idempotentHint=True` | Repetition creates no additional changes. The health answer can still change between calls. |
| `openWorldHint=False` | A bounded configured lab scope, not arbitrary caller-selected destinations. It does not mean no network access. |

Annotations are descriptive hints, NOT permissions, a sandbox, authorization,
or proof of actual behavior. A client may use trusted hints for warnings or
approval decisions; client behavior varies, and untrusted servers can lie.
Some hints may be redundant or ignored for a read-only tool. A client should
not blindly skip approval simply because a server declares a tool safe.

The tool implementation should honor its advertised contract, but the SDK does
not enforce that match. Changing a hint does not change our GET method, URL,
timeout, filesystem access or process privileges. Destructive code would not
be blocked by `readOnlyHint=True`. Actual restrictions come from code and
permissions: here, a fixed operator target, GET-only health operation, bounded
I/O and no model administration or Kubernetes API calls.

Presenter wording: "Annotations describe intent. Code and permissions enforce
behavior. Our server exposes tools; it does not choose tools for an agent."

### Packaging And Deployment

[Dockerfile](Dockerfile) pins the Python `3.12.15-slim-bookworm` index digest,
hash-verifies `uv==0.11.24` from the approved feed, exports frozen hashed runtime
requirements natively, and installs hash-verified wheels with target-platform pip.
Native export avoids a demonstrated AMD64 uv/QEMU crash on the ARM64 builder.
The default-deny build context excludes Git, environments, tests, kubeconfigs and
credentials. Actual AMD64 container and AKS runtime checks passed; lifecycle is
VALIDATED only for the D-014 trusted supervised single-operator lab: independent
Tester **63 PASS in 13.87s** plus deployed image/source/runtime/SDK and offline
failure checks, Security Reviewer bounded GO, and Architect ACCEPT. This is not
network isolation, whole-image certification or production readiness. See
[D-014 acceptance](docs/decisions.md#final-architectural-acceptance-2026-10-23-bounded-validated).

Rebuild and publish using existing Entra authority, without admin/pull secrets:

```bash
docker buildx build --platform linux/amd64 --load --tag lab-info:d014 .
az acr login --subscription d18f2ff3-4ef1-4102-8c8f-3a344037aeed --name acragwlabd18f2ff3
docker tag lab-info:d014 acragwlabd18f2ff3.azurecr.io/lab-info:d014
docker push acragwlabd18f2ff3.azurecr.io/lab-info:d014
```

Docker's default health target is loopback. If changing the listener port,
update the healthcheck as well. Do not publish application ports to all interfaces.
After a rebuild, inspect the remote digest and runtime before intentionally
updating the manifest; do not assume a reused tag identifies the same image.

[k8s/mcp/lab-info.yaml](k8s/mcp/lab-info.yaml) is deployed under bounded D-014
authorization: namespace `mcp`, curated ConfigMap, one CPU `app`
replica and ClusterIP port 80 -> 8000. It requests no GPU, token, RBAC, secret
or writable application storage. It applies non-root UID/GID 10001, read-only
root/config, dropped capabilities, no privilege escalation, RuntimeDefault
seccomp, CPU/memory bounds and upstream-independent probes with explicit safe
Host headers. The exact full Service DNS name, with/without `:80`, is allowlisted;
short Service aliases are intentionally not. The image is pinned to the published
digest with `IfNotPresent`. [infra/registry.bicep](infra/registry.bicep) owns only
the dedicated Basic ACR and existing kubelet's registry-scoped AcrPull; it does
not redeploy AKS. Registry admin and anonymous access are disabled.

Repeat admission/rollout and operator-only localhost access:

```bash
kubectl --context=aks-agw-lab apply --dry-run=server -f k8s/mcp/lab-info.yaml
kubectl --context=aks-agw-lab apply -f k8s/mcp/lab-info.yaml
kubectl --context=aks-agw-lab -n mcp rollout status deployment/lab-info --timeout=180s
kubectl --context=aks-agw-lab -n mcp port-forward --address 127.0.0.1 service/lab-info 18000:80
```

MCP endpoint (not a web page): `http://127.0.0.1:18000/mcp`, available only while
you run forwarding; the test forward was closed. There is no public application
URL. Stop forwarding when finished. Port 18000
is explicitly allowlisted because an unrelated local process already uses 8000.
The real SDK initialize/list/both-tool check and live fixed health passed on
this path. Curated overview revision 2026-10-22.1 remains historical static data,
not live deployment discovery. Current evidence is in [STATUS.md](STATUS.md).
There is no public Service, application authentication/TLS or NetworkPolicy here.
D-015 separately adds the private gateway route below; the direct MCP path is
unchanged. ClusterIP and DNS-rebinding protection are not authorization or
workload isolation.

### Test The Deployed MCP With Curl

Keep the localhost port-forward above running in one terminal. In a second
terminal, run these commands in order. Testing an existing deployment does not
require repeating `kubectl apply`, rebuilding the image or installing a client.
`--noproxy '*'` keeps these loopback requests out of any configured HTTP proxy.

1. Check MCP readiness:

```bash
curl --noproxy '*' -sS http://127.0.0.1:18000/readyz
```

Expected: `{"status":"ok"}`. This checks MCP itself, independently of llama.cpp.
`/healthz` provides the corresponding application liveness check.

2. Initialize the MCP protocol:

```bash
curl --noproxy '*' -sS http://127.0.0.1:18000/mcp \
	-H 'Content-Type: application/json' \
	-H 'Accept: application/json, text/event-stream' \
	-d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}}}'
```

Expected: a JSON-RPC result with `protocolVersion: "2025-11-25"`, server
information and capabilities. This deployment is stateless; no session ID needs
to be copied into later requests. Keep the two media types in `Accept`.

3. Send the initialized notification:

```bash
curl --noproxy '*' -sS http://127.0.0.1:18000/mcp \
	-H 'Content-Type: application/json' \
	-H 'Accept: application/json, text/event-stream' \
	-H 'MCP-Protocol-Version: 2025-11-25' \
	-d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```

An empty response is normal for this notification (HTTP 202).

4. Discover the tools:

```bash
curl --noproxy '*' -sS http://127.0.0.1:18000/mcp \
	-H 'Content-Type: application/json' \
	-H 'Accept: application/json, text/event-stream' \
	-H 'MCP-Protocol-Version: 2025-11-25' \
	-d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

Expected: exactly `get_lab_overview` and `get_model_health` in `result.tools`.
Neither tool requires arguments.

5. Call live model health:

```bash
curl --noproxy '*' -sS http://127.0.0.1:18000/mcp \
	-H 'Content-Type: application/json' \
	-H 'Accept: application/json, text/event-stream' \
	-H 'MCP-Protocol-Version: 2025-11-25' \
	-d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_model_health","arguments":{}}}'
```

When llama.cpp is healthy, expect `result.isError: false` and this
`result.structuredContent`:

```json
{"status":"healthy","reason":"health_ok","http_status":200}
```

The operator independently observed this result on 2026-10-23. The response
also includes a text representation under `result.content`; that duplication is
normal. This proves curl -> MCP -> llama.cpp `/health`, not model inference or
gateway routing. A non-healthy observation can still have `isError: false`:
the tool succeeded in reporting the upstream state.

6. Call the static overview:

```bash
curl --noproxy '*' -sS http://127.0.0.1:18000/mcp \
	-H 'Content-Type: application/json' \
	-H 'Accept: application/json, text/event-stream' \
	-H 'MCP-Protocol-Version: 2025-11-25' \
	-d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_lab_overview","arguments":{}}}'
```

Expected: `isError: false` and structured lab context with four configured model
presets. This is curated static data, not a live inventory or model-readiness
check, and does not depend on llama.cpp being available.

For troubleshooting, add `-i` to a curl command to inspect the HTTP status and
headers. Connection refused usually means forwarding is not running or the
local port differs. HTTP 421/403 indicates Host/Origin rejection; use the exact
allowlisted loopback URL above. HTTP 406 indicates an unacceptable `Accept`
header; retain both listed media types. A healthy MCP probe with a non-healthy
tool observation points to the upstream health path, not automatically an MCP
failure. Stop port-forwarding with Ctrl-C in its terminal when finished.

### Validate llama.cpp Directly Before Model Routing

This tests client -> llama.cpp without MCP or agentgateway. Independent checks on
2026-10-27 supersede older GPU absence: all four presets passed direct inference
with correlated GPU worker/memory evidence and normal three-model LRU behavior.
Final bounded Architect ACCEPT clears step 5's explicit log gate on independently
corroborated historical diagnostic evidence, plus separate final-runtime checks
and final Security Reviewer GO. Tester nine gates PASS and 66 tests PASS/2
live-gateway SKIP are recorded, not rerun here. Historical ~0.77-0.87 s timings
were warm; latest cached requests were ~3.42-4.20 s, not throughput/cold-download
benchmarks. Separate exact-v1.6.0 fixed-backend/narrow-inference-path design and
security proof remain; no admin/catch-all or routing work is authorized. Future
implementation requires separate authorization and independent gateway validation.
Check prerequisites
each time because Spot capacity can disappear. Do not change the pool, SKU or
node count merely to run this guide. MCP/gateway CPU-only success does not prove
inference. This acceptance review did not rerun these commands.

1. Check the inference workload before opening a connection:

```bash
kubectl --context=aks-agw-lab get nodes -l workload=gpu-inference
kubectl --context=aks-agw-lab -n llm get pods -l app=llama-cpp -o wide
```

Require a Ready GPU node and a Ready/Running llama.cpp pod. An absent node or
Pending pod is a prerequisite failure, not a model API test result.

2. In one terminal, open localhost-only access and leave it running:

```bash
kubectl --context=aks-agw-lab -n llm port-forward \
	--address 127.0.0.1 service/llama-cpp 18080:8080
```

3. In another terminal, check router health and configured model discovery:

```bash
curl --noproxy '*' -sS -i --max-time 10 http://127.0.0.1:18080/health
curl --noproxy '*' -fsS --max-time 10 http://127.0.0.1:18080/v1/models
```

Expect health HTTP 200 with `{"status":"ok"}`, and model IDs including
`qwen2.5-7b-instruct`. Validate the four approved `source=preset` IDs, not an
exactly-four total list: independent discovery also showed four `source=cache`
entries. Healthy router status and listed presets do not prove that any model
is loaded, can generate tokens, or uses the GPU.

4. Request actual inference using an exact preset ID:

```bash
curl --noproxy '*' -sS -i --max-time 600 \
	http://127.0.0.1:18080/v1/chat/completions \
	-H 'Content-Type: application/json' \
	-d '{"model":"qwen2.5-7b-instruct","messages":[{"role":"user","content":"What is 17 + 25? Reply with only the number."}],"temperature":0,"max_tokens":32,"stream":false}'
```

Pass: HTTP 200, `choices[0].message.content` answers `42`, and
`usage.completion_tokens` is greater than zero. First use can download weights
to the existing PVC and load them into memory; the 600-second deadline bounds
the client wait, not guaranteed model load time. A timeout is inconclusive:
inspect workload state/logs before retrying. Repeat with each remaining ID:
`qwen2.5-coder-7b-instruct`, `llama-3.1-8b-instruct`, and `phi-4`.
The router permits at most three loaded models; loading the fourth can evict
an earlier model from memory, not delete its cached weights.

5. Inspect model startup logs for actual CUDA offload:

Normal operation retains the pinned release's default verbosity 3. Backend INFO
CUDA/offload messages require temporary `--log-verbosity 4`; they cannot be
recovered retrospectively. Do not enable this casually: Recreate interrupts
service, level 4 can expose key suffixes/metadata, and warning paths can log
generated output even below 4. Never use level 5, private traffic, credentials
or prompt/slot-debug logging for this diagnostic. Recheck selected key/logging
overrides without printing values, use only the public arithmetic request above,
and obtain approval for the rollout and log handling first.

```bash
# Use the actual named diagnostic pod, not a trailing deployment log window.
# Save full retained startup logs outside Git with restricted local permissions.
umask 077
diagnostic_dir=$(mktemp -d /tmp/d011-diagnostic.XXXXXX)
kubectl --context=aks-agw-lab -n llm logs pod/<diagnostic-pod> \
	-c llama-server --timestamps --tail=-1 > "$diagnostic_dir/startup.log"
```

Require CUDA device initialization and model layers offloaded to GPU. A successful
chat response alone does not prove GPU execution. Capture from startup through
all four sequential loads, correlate alias -> child port -> CUDA -> actual X/Y.
Correlated GPU processes, memory and CUDA library mappings support bounded GPU
use, but do not satisfy this explicit log gate; `-ngl 99` is configuration only.
Restore the checked-in manifest/default 3 after capture, wait for Ready, repeat
all four bounded requests, close owned forwarding and delete private raw logs
once reviewed. Kubernetes/collector copies may remain; filtering local excerpts
does not sanitize those copies or prove retention/access policy.

Accepted historical capture on 2026-10-27: Qwen `29/29`, Qwen Coder `29/29`, Llama `33/33`,
Phi `41/41`, each with one initialized CUDA MIG device and HTTP 200/exact `42`.
Independent Tester correlated aliases/repositories/child ports/CUDA/counts;
ReplicaSet specs and events corroborate the capture window. The diagnostic pod
is deleted: no fresh retrieval/tamper-proof provenance or fresh final-pod startup
counts are claimed. Separate final default-3 four-model requests passed HTTP 200/
exact `42`/positive usage 3/3/2/2, with healthy discovery/LRU and GPU workers.
Router/resident workers use UID/GID 10001, RuntimeDefault/Seccomp 2, all caps zero,
NoNewPrivs 1, no token; fsGroup 10001/OnRootMismatch supplied existing-cache access
without root initialization/manual repair/world-write. Inventories match paths/
sizes/links, not full hashes; independent permission checks do not prove new
writes/downloads/remounts/recovery. No throughput or wider-access claim follows.

D-011 accepts HIGH plaintext/unauthenticated HTTP, unrestricted cluster reachability,
direct administration and resource/state abuse only for a private supervised single
operator, trusted workloads/local users and synthetic/public data. Controller
Secret-read HIGH risk remains separately accepted in D-015, not fixed. Acceptance
expires BEFORE sharing, new untrusted workloads/local users, wider exposure or
target change. MEDIUM logging confidentiality remains even at default 3; collector
access/retention is not certified. Publish only reviewed public-safe summaries,
never raw diagnostics/credentials. Coordinator owns restricted-artifact cleanup
after review and staged-content safety checks before eventual commit/push.
No model route or Phase 9/10 completion is authorized here; D-015 live gateway
outage validation remains deferred.

Rollback only if hardening regresses: remove the newly added pod-level
`securityContext` block and server-dry-run/apply the reviewed manifest; this
returns the prior root/no-explicit-seccomp posture and is NOT an accepted final
security state. Leave container drop-ALL/no-escalation, token policy, image,
presets, GPU placement and PVC untouched. Existing cache group metadata need
not be reversed for root compatibility. Reapplying the current manifest alone
removes the temporary logging patch while keeping hardening.

On hardening regression or changes to image/model/args/permissions/CSI/cache
layout or the accepted trust/exposure boundary, stop affected use and reassess.
Any rollout/rollback needs appropriate approval; do not silently fall back to
root/Unconfined, loosen permissions or delete model weights/PVCs.

Record the time, tested model IDs, response status/content, generation usage and
offload evidence in STATUS. These manual smoke checks do not replace the
independent Tester acceptance of router mode required before wiring the model
route. They do not validate agentgateway, model tool calling or an agent loop.
Stop the port-forward with Ctrl-C when finished. No public endpoint is needed.

## Private Gateway And MCP (D-015, Bounded VALIDATED)

Actual application path: operator -> localhost API forwarding -> ClusterIP
agentgateway proxy port 8080 -> exact `/mcp` ->
`lab-info.mcp.svc.cluster.local:80/mcp` -> existing MCP pod port 8000.
There is no llama.cpp backend/route, public URL, LoadBalancer or NodePort.
Only MCP's existing health tool may perform its fixed `/health` GET.

Human accepted the preinstallation HIGH finding: the native controller can read
Secret contents cluster-wide, plus reviewed discovery, TokenReview, GatewayClass
and status authority. Namespace-scoped writes do not remove those reads.
[D-015](docs/decisions.md#d-015-cpu-only-gateway-and-mcp-first-2026-10-23-planned)
records the disposition; it accepts this trusted-lab blast radius, not a fix,
new Azure IAM grant or shared/public readiness. Independent Tester and runtime
Security Reviewer reports now support Architect ACCEPT for observed CPU-only
deployment/control-plane and MCP interoperability, for unchanged trusted,
supervised single-operator use only. Live gateway outage independence is deferred,
not accepted; Phase 9/10 model integration/end-to-end inference remain PLANNED.

### A 10-15 Minute Reading Map

1. **Minutes 0-3, split control from traffic.** Read [k8s/gateway/controller-values.yaml](k8s/gateway/controller-values.yaml). Helm deploys the Kubernetes controller, not the MCP service. Top-level CPU placement, resources, narrow discovery and namespaced writes are explicit. The controller needs its API token and manages an xDS certificate Secret. Optional mesh/model/inference/monitoring integrations are off.
2. **Minutes 3-6, follow generated infrastructure.** Read [k8s/gateway/parameters.yaml](k8s/gateway/parameters.yaml). Store these parameters BEFORE the Gateway to prevent a transient default LoadBalancer. The controller merges this input into its generated Deployment and ClusterIP Service. Do not patch those outputs. It preserves probes, the read-only CA and audience-scoped xDS token, but disables generic proxy API-token automount. Both gateway processes run as UID 10101 on the app pool; neither requests a GPU.
3. **Minutes 6-9, trace the one route.** Read [k8s/gateway/gateway.yaml](k8s/gateway/gateway.yaml): Gateway/listener -> HTTPRoute -> AgentgatewayBackend -> one static Service DNS target. Same-namespace attachment and exact `/mcp` avoid catch-all/admin/model routes. `Stateless` matches FastMCP; `prefixMode: Never` preserves both tool names. DNS selection is not authorization. No ReferenceGrant is needed for a static hostname.
4. **Minutes 9-12, compare credential boundaries.** The controller has reviewed Kubernetes API authority. The proxy authenticates TLS xDS on 9978 with its dedicated projected token (audience `agentgateway`, requested 43200 seconds) and read-only CA; its ServiceAccount has no Secret-read grant. MCP remains token-free. Application HTTP is still plaintext/unauthenticated inside the trusted lab; xDS TLS does not encrypt that application path. Other pods can reach these Services; no network isolation was added.
5. **Minutes 12-15, distinguish evidence.** Run [tests/test_gateway.py](tests/test_gateway.py) as below. Conditions prove reconciliation, SDK calls prove protocol interoperability, and health reports only one upstream observation. Neither proves model inference, GPU availability, model tool calling or an agent loop. The overview intentionally remains historical static data.

### Reproduce The Bounded Install

Prerequisites: the existing authorized operator, explicit context `aks-agw-lab`,
Helm (execution used 4.2.2), kubectl and the frozen Python environment. Do not
change the current context. No Python installs or new Azure resources are needed.
Use only the approved feed if a separately approved dependency change is needed.

Start with read-only ownership/capacity checks. Inspect GatewayClasses if that API
already exists. Stop on unrelated shared CRDs/classes/releases, unsupported
versions or insufficient existing authority; do not replace/adopt them or grant
new operator rights. The original preflight found all gateway resources absent.

```bash
kubectl --context=aks-agw-lab get nodes -l workload=app -o wide
kubectl --context=aks-agw-lab describe nodes -l workload=app
kubectl --context=aks-agw-lab get crd
kubectl --context=aks-agw-lab api-resources --api-group=gateway.networking.k8s.io
helm list --kube-context=aks-agw-lab --all-namespaces
kubectl --context=aks-agw-lab auth can-i '*' '*' --all-namespaces
.venv/bin/python -m pytest -q
helm template agentgateway oci://cr.agentgateway.dev/charts/agentgateway --version v1.6.0 --namespace agentgateway-system -f k8s/gateway/controller-values.yaml
```

For a fresh, conflict-free approved target, download the exact official standard
bundle to a disposable directory and verify the reviewed hash. On this already
installed lab, retain established CRDs rather than reinstalling/deleting them
as troubleshooting. The standard bundle includes its CRD safe-upgrade admission
policy/binding, not just CRDs; no unrelated existing guard was replaced.

```bash
workdir=$(mktemp -d)
curl -fsSL https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.6.0/standard-install.yaml -o "$workdir/standard-install.yaml"
printf 'a557172e8348f758479e9ee4000bbbb4b4aa48302a6b73461823ea5349bad56d  %s\n' "$workdir/standard-install.yaml" | shasum -a 256 -c -
kubectl --context=aks-agw-lab apply --server-side --dry-run=server -f "$workdir/standard-install.yaml"
kubectl --context=aks-agw-lab apply --server-side -f "$workdir/standard-install.yaml"
kubectl --context=aks-agw-lab create namespace agentgateway-system --dry-run=client -o yaml | kubectl --context=aks-agw-lab apply --dry-run=server -f -
kubectl --context=aks-agw-lab create namespace agentgateway-system --dry-run=client -o yaml | kubectl --context=aks-agw-lab apply -f -
helm template agentgateway-crds oci://cr.agentgateway.dev/charts/agentgateway-crds --version v1.6.0 --namespace agentgateway-system | kubectl --context=aks-agw-lab apply --server-side --dry-run=server -f -
helm upgrade --install agentgateway-crds oci://cr.agentgateway.dev/charts/agentgateway-crds --version v1.6.0 --namespace agentgateway-system --kube-context=aks-agw-lab --wait --timeout 180s
helm template agentgateway oci://cr.agentgateway.dev/charts/agentgateway --version v1.6.0 --namespace agentgateway-system -f k8s/gateway/controller-values.yaml | kubectl --context=aks-agw-lab apply --dry-run=server -f -
helm upgrade --install agentgateway oci://cr.agentgateway.dev/charts/agentgateway --version v1.6.0 --namespace agentgateway-system --kube-context=aks-agw-lab -f k8s/gateway/controller-values.yaml --wait --timeout 240s
kubectl --context=aks-agw-lab apply --dry-run=server -f k8s/gateway/parameters.yaml
kubectl --context=aks-agw-lab apply -f k8s/gateway/parameters.yaml
kubectl --context=aks-agw-lab apply --dry-run=server -f k8s/gateway/gateway.yaml
kubectl --context=aks-agw-lab apply -f k8s/gateway/gateway.yaml
kubectl --context=aks-agw-lab -n agentgateway-system rollout status deployment/agentgateway-proxy --timeout=180s
```

Expected versions: both Helm charts/app versions `v1.6.0`; Gateway API standard
bundle `v1.6.0` (10 established CRDs); four established agentgateway CRDs serve
`v1alpha1`. Controller chart OCI digest:
`sha256:d3edf2b33cbf2e9d59406c207b8d3554597799707b8803b5f62e698fe5376e28`;
CRD chart digest:
`sha256:dd7f965d43e54dffa9c95af089b6f762397a23c963a159ad6d4992f6c582292a`.
Compare pulled digests before installation, not just chart names/tags.

Pinned and observed pod imageIDs (multi-platform indexes, not chart digests):

- Controller: `cr.agentgateway.dev/controller@sha256:d84259a7e2d87f8f39bae385d4b032d823c0a4450aecb32e0e31e2258449645b`.
- Proxy: `cr.agentgateway.dev/agentgateway@sha256:9d3e6044ddcdc0878b1787f77bd401252b95e22684203fb5e874c4c42d2ed90c`.

Controller values use the chart-supported `v1.6.0@sha256:...` tag verbatim;
proxy parameters use the release's explicit `image.digest` field. Both select
AMD64 on this app node. Render and inspect before upgrading either version.

### Observe And Exercise

```bash
kubectl --context=aks-agw-lab get gatewayclass agentgateway -o yaml
kubectl --context=aks-agw-lab -n agentgateway-system get gateway,httproute,agentgatewaybackend -o yaml
kubectl --context=aks-agw-lab -n agentgateway-system get pods,services -o wide
kubectl --context=aks-agw-lab -n agentgateway-system get deployment agentgateway-proxy -o yaml
```

Require `observedGeneration == metadata.generation` for Accepted/Programmed,
listener Accepted/Programmed/ResolvedRefs and route Accepted/ResolvedRefs. Current
evidence: all generation 1, true; controller/proxy Ready with zero restarts on
`aks-app-42647623-vmss000000`. Both Services are ClusterIP, no external IP:
controller ports 9978/9093/9092, proxy port 8080 only. Admin readiness remains
`/healthz/ready:15021` on the proxy pod, not an application route.

Check port availability; leave unrelated listeners alone. Start forwarding in
one terminal and stop it with Ctrl-C when finished:

```bash
lsof -nP -iTCP:18000 -sTCP:LISTEN
kubectl --context=aks-agw-lab -n agentgateway-system port-forward --address 127.0.0.1 service/agentgateway-proxy 18000:8080
```

In another terminal:

```bash
GATEWAY_TEST_URL=http://127.0.0.1:18000/mcp .venv/bin/python -m pytest -q -s tests/test_gateway.py
```

If occupied, choose a free port and change the forward/test URL together; the
non-browser SDK sends no Origin. Do not widen allowlists or remove a foreign
Origin. The gateway supplies the already allowlisted upstream Service authority;
incoming Host is not caller authentication, and the listener has no hostname
restriction. Direct MCP still rejects foreign Host/Origin (421/403).

Independent Tester evidence: full live suite 68 PASS in 26.76s; live gateway
5 PASS in 13.24s, offline gateway 3 PASS, focused MCP failure/deadline/probe
4 PASS and supplemental direct MCP 9 PASS. Official SDK 1.30.0 negotiates
`2025-11-25`, initializes twice, discovers exactly `get_lab_overview` and
`get_model_health` with no parameters, calls both twice per initialization, and
receives structured results with no session ID. Foreign Origin returns 403;
`/`, `/health`, `/healthz`, `/readyz`, `/mcp/`, `/v1/models`, `/metrics` return 404.
Observed health was `healthy/health_ok/200`, contrary to expected unavailable
upstream; no GPU availability or inference conclusion follows. Direct MCP
healthz/readyz remain 200; its image, pod, fixed target and token absence are
unchanged. No live failure was manufactured. Existing offline tests establish
MCP failure independence ONLY, not deployed gateway outage behavior. That original
D-015 Gate C portion is explicitly deferred beyond this narrowed acceptance:
later independently verify gateway discovery/overview/bounded health and direct
MCP probes during a naturally occurring or separately authorized outage. Do not
disrupt/reconfigure the upstream to manufacture evidence for this acceptance.

Proxy defaults emit request/tool metadata, including paths and tool names;
inspected bounded logs contain no bodies, prompts or credentials. This is not
whole-image/logging certification. Application authentication/TLS, network
isolation, HIGH controller Secret-read authority and existing MCP residuals are
not fixed by these checks. No public/shared/customer readiness is claimed.

### Roll Back Only This Layer

Do not execute rollback as part of validation. First stop your own forward.
Remove route/backend/Gateway; the controller garbage-collects its generated proxy.
Then remove parameters. Only uninstall the controller if no other Gateway uses
it. Leave CRDs, standard upgrade guards and the namespace in place for explicit
review; deleting shared CRDs can erase custom resources. Never remove MCP,
registry, llama.cpp, PVCs or node pools as part of gateway rollback.

```bash
kubectl --context=aks-agw-lab delete -f k8s/gateway/gateway.yaml
kubectl --context=aks-agw-lab delete -f k8s/gateway/parameters.yaml
kubectl --context=aks-agw-lab get gateways --all-namespaces
helm uninstall agentgateway --namespace agentgateway-system --kube-context=aks-agw-lab
```

Official release sources: [Helm install](https://agentgateway.dev/docs/kubernetes/latest/documentation/install/helm/),
[static MCP](https://agentgateway.dev/docs/kubernetes/latest/documentation/mcp/static-mcp/),
[parameters overlays](https://agentgateway.dev/docs/kubernetes/latest/documentation/setup/customize/configs/),
[TLS xDS](https://agentgateway.dev/docs/kubernetes/latest/documentation/install/tls/),
and [v1.6.0 generated pod helper](https://github.com/agentgateway/agentgateway/blob/v1.6.0/controller/pkg/helm/agentgateway/templates/_helpers.tpl).
APIs/values were checked against the exact downloaded release charts, not only
mutable latest documentation. Full evidence/handoff: [STATUS.md](STATUS.md).
