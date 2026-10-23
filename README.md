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
for trusted, supervised, single-operator lab use; gateway remains unverified.
Phase 8 stays paused.

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

Reserve Kubernetes Service/pod binding, app-pool placement and the future
gateway route for a **separate later 10-15 minute discussion**. No gateway
implementation, integration, deployment or live human walkthrough is claimed here.

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
There is no public Service,
gateway route, application authentication, TLS or NetworkPolicy here. ClusterIP
and DNS-rebinding protection are not authorization or workload isolation.

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
