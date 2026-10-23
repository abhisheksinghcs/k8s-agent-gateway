# STATUS

Last updated: 2026-10-23 (D-014 trusted, supervised single-operator MCP milestone architecturally accepted; VALIDATED within that boundary)

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
- DECISION (human, clarified 2026-10-22): generated code must have copious workload/contract-oriented comments, assuming Python/language familiarity rather than teaching syntax. Constitution section 9 and main.py explain design rationale, setting ownership, inbound/outbound wiring, tool/data contracts, failure semantics and SDK boundaries. No runtime or architecture change is intended.
- HISTORICAL FACT: the earlier comments-only pass preserved the three-tool source's executable AST and passed 54 tests. The subsequent two-tool teaching revision supersedes that source; current independent validation is 63 PASS as recorded below.
- DECISION: the Python MCP server is a teaching reference for a non-developer with some Python familiarity, not a production application. Exactly two tools support a 10-15 minute code walkthrough, with a separate later 10-15 minute Kubernetes/gateway discussion. LOCAL source acceptance is retained; D-014 separately accepts bounded container/cluster hosting below. Broader exposure is not accepted.
- DECISION: the intended publication should complement abhisingh.org's agent-harness series by explaining component responsibilities and real service integration, not showcasing code complexity. No portfolio article or harness integration has been implemented in this repository.
- FACT (2026-10-23): the human confirms understanding of the revised code and is ready for the next learning stage. README preserves the whole-file flow, lifecycle/yield explanation, tool annotations and their security limitations. That learning-stage confirmation alone did not authorize deployment; the subsequent bounded authorization below supersedes it, not the LOCAL acceptance limits.

## Active request: deploy the MCP Kubernetes component

- OPERATOR EVIDENCE (2026-10-23): human ran curl `tools/call` for
    `get_model_health` through localhost:18000 and supplied the JSON-RPC response:
    `isError: false`, structured `healthy/health_ok/200`. This confirms the manual
    MCP-to-upstream health path, not inference or gateway integration. README now
    documents the full readiness/initialize/notification/list/both-tool sequence.
- INDEPENDENT EVIDENCE (Tester): 63 PASS in 13.87s; live pod imageID and source
    hash match the published artifact and local source. Ready AMD64 app-pool pod,
    zero restarts, runtime hardening/token absence and internal Service confirmed.
    Official SDK over localhost:18000 initialized 2025-11-25, listed exactly two
    argument-free tools, and called both with structured results and no session
    ID. Live health healthy/health_ok/200; both probes 200, invalid Host/Origin
    rejected. Exact cached deployed image with networking disabled independently
    proved overview/probe availability during upstream connection failure.
    Temporary container and forwarding cleaned up; port 18000 free.
- INDEPENDENT SECURITY REVIEW: GO for continued trusted, supervised,
    single-operator D-014 use only; no new CRITICAL/HIGH in inspected artifacts
    and live configuration. Known MEDIUM SDK reflection and unauthenticated
    plaintext access, plus LOW inbound availability, remain. No network isolation,
    shared/customer readiness, whole-image certification or gateway validation
    claimed. Base/bootstrap/dependency pinning and scoped registry pull verified.
    Architectural acceptance is recorded below; execution records are in
    docs/agent-execution-log.md.
- FACT (current execution): complete source suite 63 PASS in 13.98s; initial
    packaging/security/drift checks 3 PASS. Base Python index digest pinned to
    `sha256:6a0e06f5ba0b373d051aabd3fffb9b873f27f9a2a3a14bcbe37dee6f0e3bbc70`.
    uv 0.11.24 bootstrap hashes were obtained from the approved feed and enforced
    by pip. First synchronous AMD64 build FAILED (139): uv itself segfaults under
    Rancher Desktop QEMU, reproduced with `uv --version`; AMD64 Python runs.
    Packaging now exports frozen hashed requirements natively and installs with
    target-platform pip. Repeat synchronous AMD64 build succeeded; image ID
    `sha256:56325c9514265c95e9bcf87a415d40501ac36d31a1be3e735fd810c449037f15`.
    Full post-repair suite 63 PASS in 13.90s. Actual container execution reports
    x86_64, UID/GID 10001, zero effective capabilities, NoNewPrivs=1, seccomp=2
    and read-only rootfs. Real SDK initialize (2025-11-25), exact two-tool list,
    both structured calls and independent 200 healthz/readyz passed, both inside
    the AMD64 container and from host localhost:18000. Intentional unavailable
    upstream returned unknown/connection_failed/null HTTP status. First host
    attempt hit an unrelated pre-existing port 8000 service (405/404); it was
    untouched. First corrected-port request disconnected before forwarding
    settled; container-local pass and subsequent host SDK pass resolved it.
    Session smoke container and its listener removed. No source behavior changed.
- FACT (current execution): target subscription, Ready AMD64 app node and
    Azure/overlay dataplane with no network policy refreshed. Lab RG ACR list was
    empty before deployment. Fresh AKS kubelet object ID was obtained from `identityProfile`.
    Existing operator inherited Contributor (no condition) and root-scope User
    Access Administrator (no condition) establish the create/push and scoped
    role-assignment permission path for traditional registry RBAC. No operator
    role was added. Earlier design-only observations below are retained as history.
- DEPLOYED: isolated `infra/registry.bicep` adds only Basic ACR (admin/anonymous
    disabled, authenticated public registry endpoint, traditional RBAC) and
    registry-scoped AcrPull for the parameterized existing kubelet identity.
    Bicep 0.48.1 compilation and server validation passed. Reviewed what-if: two
    creates (registry and scoped assignment), AKS Ignore, no modifications/deletes.
    Incremental deployment `d014-mcp-registry` Succeeded. Actual registry
    `acragwlabd18f2ff3` in southeastasia confirms Basic/LegacyRegistryPermissions,
    admin=false/anonymous=false. Sole direct assignment: AcrPull for actual
    kubelet object ID `96b9e4e7-04cc-45e9-aec1-6665234bf394`, registry scope only.
    Existing Entra login and push succeeded; no new operator role or secret.
- CREATED/published: `acragwlabd18f2ff3.azurecr.io/lab-info@sha256:29f6d6d123c54cec36ca64c104ff55450de823a27b52d3a1db75cdfd8e320b76`.
    MCP manifest now pins this digest with IfNotPresent; localhost:18000 is
    explicitly allowed for operator forwarding. Remote inspection confirms
    linux/amd64 and user 10001:10001.
- DEPLOYED: namespace server dry-run passed, namespace created, full manifest
    server dry-run passed, then only Namespace/ConfigMap/Deployment/ClusterIP
    Service applied. Rollout completed within 180s. Pod `lab-info-6856dddf7-zdrrn`
    Ready with zero restarts on `aks-app-42647623-vmss000000`; actual imageID
    exactly matches the published manifest digest. Service has no external IP.
    Actual runtime: x86_64, UID/GID 10001, CapEff=0, NoNewPrivs=1, Seccomp=2,
    root mount ro, no service-account token. Fixed health URL unchanged.
- FACT (Developer implementation check, not independent certification): real
    SDK through localhost:18000 API forwarding initialized protocol 2025-11-25,
    discovered exactly two no-argument tools, called both with structured results
    and no session ID. Live health returned healthy/health_ok/200; healthz and
    readyz returned 200. Prior hardened local image check proved unavailable-
    upstream independence; production upstream was not interrupted. Bounded
    logs show tool outcomes only. Test port-forward closed; no gateway, inference,
    llama.cpp restart, network-policy change or external application exposure.
- FACT (final checks): full suite 63 PASS in 13.88s; `git diff --check` passed.
    No commit or push was performed; pre-existing dirty files were preserved.
    Changes in this execution: Dockerfile, tests/test_lab_mcp.py,
    infra/registry.bicep, k8s/mcp/lab-info.yaml, STATUS.md, README.md,
    docs/architecture.md and docs/troubleshooting.md. Coordinator-owned agent
    execution log was not edited by this execution; no agents were delegated.
- Reproducibility: SHA-256 main.py `a3baf76ceea48b861b19cec4415cc3f9d2180d321f75f296d475e9237952d2b9`,
    uv.lock `215b2e27a012e690d85b70516ae43ca6b4435b42a3d3dc33b84eb1f87232d914`,
    Dockerfile `c62aded33eda022b7baef71a1253761bda106701754d590eb397cfb4ba3a59b6`.
    Curated overview revision remains 2026-10-22.1 intentionally, including its
    historical deployment disclaimer; it is static teaching data, not live state.

- DECISION (human, 2026-10-23): deploy the MCP component to the existing lab.
    Target is existing `aks-agw-lab`; gateway installation, public exposure and
    unrelated infrastructure are outside scope. The dedicated lab registry is
    the sole approved infrastructure expansion; its Basic tier adds ongoing cost.
- LATEST DECISION (human, D-014): proceed toward a trusted, supervised,
    single-operator MCP lab MVP with Cilium/NetworkPolicy enforcement deferred.
    This supersedes D-013's immediate isolation gate and earlier isolation-based
    NO-GO in this scope. Preserve both D-013 phases as future hardening, not
    implemented isolation. No cluster networking change/reimage, ineffective
    policy artifacts, gateway installation or public exposure is authorized.
- MVP boundary: ClusterIP plus operator localhost-bound API port-forward.
    Other pods CAN reach MCP; outbound traffic is NOT network-restricted.
    Fixed application `/health` and Host checks are not network isolation or
    caller authentication. Trust reachable workloads and the supervising operator.
- HISTORICAL FACT (Architect pre-deployment checks): `aks-agw-lab` responds with Kubernetes
    v1.36.4; its Ready, untainted `workload=app` node is AMD64. Local host is ARM64.
    Namespace `mcp` is absent. llama.cpp has a Ready pod and internal Service
    endpoint, but no fresh HTTP health or inference check was performed.
- FACT: earlier read-only snapshot reported active context `litellm-demo-aks`.
    Final direct read of only the stored kubeconfig current-context field reports
    `aks-agw-lab` (KUBECONFIG unset). No context-switch command was issued in this
    execution; the discrepancy's origin is not established and no assumed value
    was restored. All cluster operations explicitly select `--context=aks-agw-lab`.
- FACT: Docker 29.5.3 is running, Linux ARM64; actual AMD64 build/runtime
    proof now supersedes advertised-platform-only evidence and earlier failures.
- FACT (refreshed before execution): AKS reports `networkPlugin:
    azure`, `networkPluginMode: overlay`, `networkDataplane: azure`, `networkPolicy:
    none`. No enforcement is claimed. D-014 defers migration; absent enforcement
    no longer gates this MVP. Any later cluster-wide change needs separate approval.
- FACT: kube-dns Service selects `k8s-app=kube-dns`, UDP/TCP 53; llama.cpp
    Deployment selects `app=llama-cpp`. Existing policy inventory contains only
    `kube-system/konnectivity-agent`, not an MCP allowance. No policies applied.
- FACT: dedicated lab ACR and scoped kubelet-only AcrPull were deployed after
    permission assessment and reviewed what-if. No existing registry was reused,
    no operator assignment added, and no admin password or pull secret introduced.
- FACT: the former offline image placeholder is replaced with the published
    immutable AMD64 digest, successfully pulled by the actual deployed pod.
- SECURITY: human accepts reduced isolation as MVP direction, not risk resolution
    or independent security acceptance. Known SDK response reflection MEDIUM,
    availability LOW and no authentication/TLS remain explicit. Base digest,
    bootstrap hashes, locked dependency hashes and actual runtime are evidenced;
    this is not an independent whole-image security certification.
    Independent review follows actual image/runtime evidence against D-014's
    trusted-lab scope; new findings require disposition. Shared/untrusted use is
    not accepted. Historical LOCAL acceptance remains unchanged.
- DECISION (Architect, 2026-10-23): ACCEPT D-014 as VALIDATED only for the
    trusted, supervised, single-operator MCP lab milestone. Independent Tester
    deployment/SDK/failure evidence and Security Reviewer's bounded GO satisfy
    the contract; this is not a gateway or whole-project milestone.
    Detailed contract: [D-014](docs/decisions.md#d-014-trusted-supervised-mcp-lab-mvp-human-approved-amendment-2026-10-23-planned).
    Next: the human may try the MCP endpoint using the command below. Every cluster
    command must retain explicit `--context=aks-agw-lab`; do not switch context.
- Future: retain D-013 enforced operator-only and gateway-only phases; reassess
    enforcement and allow/deny tests when resumed. Cilium migration is deferred,
    not approved for execution. Gateway remains PLANNED/paused; D-011 independent
    router validation still precedes integration.
- FACT: registry, image publication, local/runtime checks and MCP deployment
    are evidenced above. No NetworkPolicy, Cilium migration, gateway installation,
    public application exposure, Git commit or push occurred. Historical
    design-only observations are superseded by current deployment evidence.

### D-014 architectural acceptance (2026-10-23; bounded VALIDATED)

- Basis: recorded Developer deployment, independent Tester 63 PASS in 13.87s
    plus exact deployed digest/source, AMD64 app-pool hardening, real SDK
    initialize/list/both structured calls, live fixed health and independent
    probes, Host/Origin rejection and same-image offline failure independence.
    Security Reviewer independently permits continued trusted-lab use only.
- Accepted artifact: `acragwlabd18f2ff3.azurecr.io/lab-info@sha256:29f6d6d123c54cec36ca64c104ff55450de823a27b52d3a1db75cdfd8e320b76`.
    Isolated Basic ACR/scoped kubelet AcrPull and pinned/hashed approved-feed
    packaging satisfy the bounded delivery contract, not whole-image certification.
- Accepted residuals: MEDIUM SDK input reflection and unauthenticated plaintext
    access with unrestricted pod ingress/egress; LOW inbound upload/concurrency
    availability. Trust reachable workloads and use only public-safe synthetic
    lab data. Host/Origin checks are not caller authentication or isolation.
- D-013's two hardening phases remain deferred; Cilium migration is not approved.
    No gateway, public/shared/customer/production readiness, model inference or
    D-011 independent router acceptance follows. Reassess before widening trust,
    operators, targets or exposure; stop/roll back MCP if trust assumptions fail.
- This acceptance changes documentation only. No new runtime/cloud checks,
    tests, builds or delegation; the recorded evidence above is the basis.
    Test forwarding/container were removed; no always-running local endpoint.

Human next action (start only when needed, stop with Ctrl-C):

```bash
kubectl --context=aks-agw-lab -n mcp port-forward --address 127.0.0.1 service/lab-info 18000:80
```

MCP endpoint while forwarding: `http://127.0.0.1:18000/mcp` (not a web page).
There is no public application URL. Overview revision 2026-10-22.1 remains
historical static teaching data, not live inventory; no rebuild is required.

## Current phase

Phase 8: install agentgateway v1.6.0 on the `app` pool and validate the control plane. Before Phase 9, get an independent Tester pass on the router-mode llama.cpp (D-011), because the gateway must not be wired to an unvalidated upstream.

Gateway implementation remains paused. The human authorized building the
Python lab-information MCP server. Architect reviewed the bounded local-first
design (D-012). Architect accepts the two-tool teaching LOCAL source milestone
against its amendment and recorded independent Tester/Security evidence.
This supersedes the historical three-tool/54-test acceptance for current source,
not its stronger response-protection guarantees. The approved Python feed restriction remains
in force. D-014 container/cluster hosting is separately VALIDATED and architecturally
accepted only for the trusted supervised single-operator lab. Public exposure is not authorized.

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
| GPU smoke test (`k8s/gpu/gpu-smoke-test.yaml`) | VALIDATED (historical independent GPU checks) | Tester confirmed GPU allocation, execution and scheduling isolation; see Phase 4 evidence. No fresh cluster check this session. |
| llama.cpp (`k8s/llm/llama-cpp.yaml`) | DEPLOYED, router mode with 4 models (D-011); single-model version was VALIDATED | Router change tested by Developer only; needs an independent Tester pass. agentgateway path NOT validated |
| agentgateway | PLANNED | |
| Python lab-information MCP server | VALIDATED (D-014 trusted supervised single-operator lab only) | Architect ACCEPT: Tester 63 PASS plus deployed SDK/runtime checks; Security Reviewer bounded GO with accepted residuals. Dedicated ACR and digest-pinned app-pool replica; no gateway or network isolation. |

## Current handoff: MCP learning requirements

### Active revision: two-tool teaching simplification (LOCAL VALIDATED)

- Human now requests a 10-15 minute Python code walkthrough with exactly
    `get_lab_overview` (static, including configured presets) and `get_model_health`
    (one fixed GET `/health`). Plain SDK implementation now replaces the three-tool
    hierarchy/wrappers; acceptance below uses new independent evidence, not historical tests.
- D-012's teaching amendment is the Developer contract: plain SDK 1.30.0 FastMCP,
    roughly 160-220 lines with workload comments; no schema hierarchy, custom dispatch
    or HTTP/telemetry wrapper. Retain bounded health I/O, SDK DNS-rebinding/body-size
    controls, independent probes and safe application errors/logs. Removing the
    wrapper reintroduces known SDK malformed-request reflection; protection is NOT
    equivalent. Supervised localhost only; shared/untrusted access requires review.
- Completed: replaced architecture-specific test expectations with the amendment's
    two-tool behavioral/security/offline checks in the existing test file. No old
    test-count gate, new client/harness, SDK migration or dependency changes.
- Completed Developer pass: local source/tests and README/architecture/STATUS edits;
    existing environment only, loopback network only. No installs/downloads,
    cloud, Docker/cluster/deployment, commits/push, delegation, execution-log edits,
    new source/doc files or dependency/config/manifest changes. Main coordinator
    owns invocation logging. Existing packaging/provenance LOWs remain unresolved;
    Phase 8 gateway work is still paused.

### Final two-tool LOCAL acceptance (Architect, 2026-10-22)

- DECISION: ACCEPT the amended D-012 LOCAL source milestone for supervised
    loopback experimentation only. Source inspection confirms 212-line plain
    official SDK 1.30 FastMCP, exactly `get_lab_overview` (static, including presets)
    and `get_model_health` (one validated fixed GET `/health`), without wrappers
    or an output-model hierarchy.
- Independent Tester: **63 PASS in 13.95s**, plus own real SDK loopback
    initialize/list/both calls, protocol `2025-11-25`, no session ID, fixed target
    despite extra arguments, slow-body deadline observed at **3.006s**, independent
    overview/probes, Host/Origin rejection, sanitized application errors/logs and
    listener/worker cleanup. Security Reviewer: **63 PASS in 13.90s** plus
    **23 supplemental checks**, acceptable only in this scope; no new blocker.
    Recorded invocations: `docs/agent-execution-log.md` (coordinator-owned).
- Known MEDIUM SDK response reflection is accepted only within this supervised
    loopback boundary, NOT resolved or equivalent to former guard protection.
    LOW upload deadline/concurrency and packaging provenance remain unresolved.
    This supersedes historical three-tool/54-test acceptance for current source;
    no broad phase, shared exposure, container, Kubernetes, live upstream or
    gateway milestone is accepted. Approved-feed-only policy is unchanged.
- README's twelve-minute walkthrough remains a proposed live teaching agenda.
    A full written walkthrough has now been delivered in conversation, covering
    startup/settings, health_url, load_overview, logging, observe_health,
    create_app, lifecycle, tool registration and probes. On 2026-10-23 the human
    confirmed code understanding; explanations are saved in README's presenter
    reference. No live rehearsal or measured 10-15 minute presentation has
    occurred. Kubernetes/gateway is the next separate 10-15 minute discussion.
    This acceptance changes documentation only; no tests were rerun for reassurance.

### Two-tool Developer evidence (2026-10-22; pre-acceptance record)

- CREATED: plain official SDK 1.30 FastMCP with a small `create_app`, exactly two
    no-parameter handlers, static overview plus four configured models, and live
    health returning only `status`, `reason`, `http_status`. No schema hierarchy,
    custom protocol guard/replay, dispatch subclass or correlation telemetry.
- Preserved fixed operator exact HTTP(S) `/health` startup validation; one GET,
    3-second overall deadline, 16 KiB streamed cap, no compression/redirects/
    retries/environment proxies and normal HTTPS verification. Host/Origin SDK
    checks and 64 KiB inbound MCP cap remain; custom probes call its validator
    directly. Loopback defaults, explicit pod binding and `proxy_headers=False`
    remain. Probes/static context are independent of upstream availability.
- Known MEDIUM residual intentionally retained per D-012: SDK malformed-envelope,
    protocol-header and unknown-tool errors can reflect caller input. Tests
    characterize that response behavior while checking suppressed logs. This is
    NOT equivalent to the removed guard. Extra SDK-ignored arguments cannot alter
    target/action; strict rejection is not promised. Unexpected app errors remain
    constant `ToolError`. Supervised loopback only, not untrusted/shared access.
- Implementation checks: initial URL/connection discriminator 6 PASS; focused
    SDK/health/security check initially 22 PASS/1 FAIL because bare `dict` lacked
    SDK structured output. Installed SDK source established `dict[str, object]`;
    same check then 23 PASS. First whole-file check 51 PASS in 13.90s; added
    startup/listener/probe independence checks 13 PASS.
- Final full command: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/test_lab_mcp.py -p no:cacheprovider`
    -> **63 PASS in 13.90s**. Focused contract command used the same prefix/options
    with `-k 'sdk_http or upstream_cases or application_error or extra_arguments or transport_security or reflection'`
    -> **23 PASS, 28 deselected** after the annotation repair. Startup follow-up
    used `-k 'invalid_config or authority or listener_contract or startup_error or upstream_failure'`
    -> **13 PASS, 50 deselected**. Editor diagnostics: no errors in source/tests;
    `git diff --check` passed. `main.py`: **212 lines** including workload comments.
    Temporary listeners stopped through existing fixture cleanup.
- This revision modifies exactly `main.py`, `tests/test_lab_mcp.py`, `README.md`,
    `docs/architecture.md`, `STATUS.md`. Existing unrelated uncommitted work was
    preserved, including the coordinator's execution log. No D-012 deviation
    requires a decision amendment. Reading order: startup configuration, bounded
    health observation, two tool handlers/probes, listener startup.
- JSON, embedded ConfigMap, Dockerfile, manifests, pyproject and lock remain
    unchanged; offline drift/hardening/approved-feed checks are retained. README
    provides a runnable 12-minute local walkthrough and defers Kubernetes/gateway
    discussion to a separate later 10-15 minutes. No live walkthrough delivered;
    the later written walkthrough is recorded in the current handoff above.
- Next at Developer handoff (now completed above): main coordinator obtains independent Tester two-tool pass, Security
    review explicitly accepting/rejecting the MEDIUM residual in supervised
    loopback scope, then Architect acceptance. No Developer self-certification.

### Historical acceptance and evidence (superseded three-tool source)

- DECISION (Architect, 2026-10-22): ACCEPT D-012 LOCAL source milestone for supervised loopback experimentation only. Final independent Tester: 54 PASS in 12.90s plus two own ASGI probes; final Security Reviewer: 54 PASS in 13.22s, no response/log leaks or uncaught ASGI exceptions. The malformed-envelope reflection and post-response telemetry recursion defects are resolved. Evidence and invocation history: `docs/agent-execution-log.md`; acceptance mapping: D-012. No full suite rerun was needed for this documentation-only acceptance. Dockerfile/manifest remain CREATED, not run, deployed or cluster-validated.
- Security review found no CRITICAL/HIGH issues. Accepted for supervised loopback experimentation only: inbound slow uploads lack a deadline/concurrency limit. Container provenance remains incomplete (mutable base tag and unhashed uv bootstrap); verify/approve these inputs before packaging/deployment. No claim of shared/customer-ready exposure.

- Audience: learning, customer demonstrations, and explaining the project to hiring managers; not a published production application.
- Accepted LOCAL tools: exactly `get_lab_overview`, `list_model_presets`, `get_model_health`, with no caller arguments; read-only, no shell execution or Kubernetes API access. Independent review is complete within the supervised-loopback scope.
- Accepted source uses official `mcp==1.30.0` FastMCP, stateless Streamable HTTP `/mcp`; real SDK HTTP flows negotiated `2025-11-25`. One app-pool replica, ClusterIP and no automatic ServiceAccount token mount are offline manifest properties only, not runtime validation.
- `docs/architecture.md` now explains GPU plugin responsibilities, MCP transports/adapters, virtual MCP tradeoffs, the phase-by-phase MCP/LLM event sequence, and the proposed server hosting/security model. These are documentation additions, not enabled telemetry or deployed MCP capabilities.
- Observability must distinguish MCP discovery/invocation from agent-side context assembly and model selection. Correlate both gateway legs without logging secrets or raw sensitive payloads.
- Completed LOCAL workflow: Architect design review; Developer implementation and repairs; final independent Tester and Security Reviewer passes; Architect source acceptance. The main coordinator owns invocation logging in `docs/agent-execution-log.md`; broader Phase 11 review remains separate.
- After implementation, walk the human through tool functions, configuration, HTTP/session handling, health checks, logs, container packaging, and Kubernetes routing. Do not assume they know TypeScript or the SDK internals.
- No live cluster checks were run during this documentation session; deployment descriptions below remain last-known evidence.

### Developer prerequisite check (2026-10-22)

Historical attempt only: the public-host commands and metadata lookup below
precede the explicit feed restriction. Do not repeat them; the approved-feed
implementation evidence below supersedes the dependency blocker.

- FACT: PyPI metadata at `https://pypi.org/pypi/mcp/1.30.0/json` confirms version `1.30.0`, Python `>=3.10`, and the official SDK dependencies. Release availability is established; installed API signatures and protocol support are NOT verified.
- FACT: local Python is 3.12.15; `uv venv --python /opt/homebrew/opt/python@3.12/bin/python3.12 .venv` created an isolated environment. No project source or dependency manifest was changed, and no lockfile was generated.
- BLOCKER: `uv pip install --python .venv/bin/python 'mcp==1.30.0' httpx pydantic starlette uvicorn pytest pyyaml` cannot fetch artifacts from `files.pythonhosted.org`: `Socket is not connected (os error 57)`. System-TLS and serial uncached attempts also failed. Direct `curl --head` and `curl -4 --head` to the SDK wheel metadata failed with curl error 35, `Recv failure: Socket is not connected`. Restore artifact-host connectivity before resuming; do not substitute SDK versions or claim runtime compatibility from metadata alone.
- BLOCKER (packaging only): `docker info --format '{{.ServerVersion}}'` reports it cannot connect to `unix:///var/run/docker.sock`. Container build/run is unverified until a local daemon is running; no registry or cloud workaround is authorized.
- No tests ran; no Dockerfile, Kubernetes MCP manifest, Azure resources, cluster operations, gateway changes, public exposure, commit, push, or nested delegation occurred. Existing Architect/coordinator documentation edits were preserved. The coordinator owns delegation logging.

### Developer implementation evidence (2026-10-22)

- DECISION (human): public PyPI, direct public package downloads and fallback/bypass are prohibited. Only `https://packagefeedproxy.microsoft.io/pypi/simple` is approved. The uv project default index replaces public PyPI; dependency commands and Docker bootstrap/frozen sync explicitly use this feed. No feed secret was required or printed. If authentication becomes necessary, notify the coordinator without requesting secrets through the model.
- FACT: approved feed lists exact `mcp==1.30.0`; `uv lock --python /opt/homebrew/opt/python@3.12/bin/python3.12 --default-index https://packagefeedproxy.microsoft.io/pypi/simple --no-cache` resolved 38 packages. Commands set `UV_DEFAULT_INDEX` and `UV_INDEX` to that feed and `UV_PYTHON_DOWNLOADS=never`. No public-host attempt occurred in this resumed implementation.
- FACT: pre-install lock audit passed: 37 registry entries use the approved index; all 177 artifact URLs are feed-provided `ms-feed-25.pkgs.visualstudio.com` URLs, with SHA-256 hashes. Frozen uncached sync from the approved feed installed 35 platform-selected packages. Integrity hashes are not publisher-signature verification. A regression test audits lock/project/Docker sources.
- FACT: Python 3.12.15; installed `mcp` 1.30.0, httpx 0.28.1, pydantic 2.14.1, starlette 0.52.1, uvicorn 0.54.0, pytest 9.1.1, PyYAML 6.0.3. Full resolved record: `uv.lock`. Installed signatures verified the selected FastMCP, Streamable HTTP and transport-security APIs. Runtime supports `2024-11-05`, `2025-03-26`, `2025-06-18`, `2025-11-25`; real SDK HTTP tests negotiated `2025-11-25`, initialized/listed/called all three tools, and observed no persistent session ID.
- FACT: `.venv/bin/python -m pytest -q tests/test_lab_mcp.py` -> **26 passed in 7.75s**. Coverage includes real HTTP SDK flow and structured schemas, strict argument rejection, fixed GET health, healthy/loading/non-200/malformed/timeout/slow-body/oversize/redirect/DNS/connection failures, proxy-env exclusion, compression rejection, Host/Origin rejection and packaged Service/probe allowlists, log/error redaction, config/preset drift and offline manifest hardening/source policy. Temporary local listeners stopped by fixture cleanup; no live llama.cpp or cluster dependency.
- FACT: the first source slice passed 7/7. Expanded HTTP tests found an SDK unsupported-protocol error reflection (20 passed/1 failed); constant boundary rejection fixed it (21/21). Packaging checks then passed 25/25; final slow-body test brings the suite to 26/26. See T-009. No independent acceptance is claimed.
- CREATED: `main.py`, `config/lab-info.json`, `pyproject.toml`, `uv.lock`, `tests/test_lab_mcp.py`, `Dockerfile`, `.dockerignore`, `k8s/mcp/lab-info.yaml`. Run/configuration/security walkthrough: `README.md`. Curated content is revisioned configuration, not live deployment/loaded-model evidence. Health performs no inference/model administration; app readiness does not depend on llama.cpp.
- SECURITY BOUNDARY: loopback by default; explicit container/pod bind; narrow Host/Origin lists; no shell/Kubernetes API/token; fixed operator-configured `/health`, 3-second overall deadline, 16 KiB cap, no redirect/retry/proxy env, TLS verification when HTTPS is used; safe JSON lifecycle metadata, dependency/access logs silenced. No authentication, TLS termination, NetworkPolicy isolation or customer-ready exposure is claimed.
- UNVERIFIED: `docker info --format '{{.ServerVersion}}'` cannot connect to `unix:///var/run/docker.sock`. Docker build/run, Python base-tag availability/immutable digest, Linux dependency execution, Kubernetes admission/scheduling/probes and live upstream behavior remain unverified. The manifest is offline-only with local image placeholder/pull policy, one app-pool replica, ClusterIP and hardened read-only non-root runtime; no deployment was performed.
- No nested delegation, agent execution log edit, registry action, gateway build/integration, cloud operation, commit or push occurred. Existing coordinator/Architect edits were preserved. Main coordinator owns independent agent routing and invocation logging.

### Developer focused transport repair (2026-10-22; historical pre-final-rerun evidence)

- CREATED: focused repair in `main.py`; real HTTP regressions in `tests/test_lab_mcp.py`; minimal README/T-009 explanation. This supplements, and does not replace, the coordinator's FAILED D-012 review status above. No independent validation, security acceptance, or Architect acceptance is claimed.
- Installed SDK 1.30.0 source confirms envelope errors reflect `str(ValidationError)`. `/mcp` POST prevalidation now uses that same `JSONRPCMessage` model behind the SDK's 65,536-byte request limiter. Parse/encoding/recursion failures return constant HTTP 400/code `-32700`; envelope failures return constant HTTP 400/code `-32602`, preserving SDK `server-error` ID. Accepted request bytes and all response streams remain unchanged; no blanket JSON-RPC error rewrite or response buffering. Telemetry ignores non-string method extras accepted on response envelopes.
- Commands/results in existing `.venv`, no installs: initial `.venv/bin/pytest -q tests/test_lab_mcp.py -k 'malformed_envelope_is_safe or parse_error_is_safe'` failed collection because direct pytest lacked the root import path. Repeating with `PYTHONPATH=.` reproduced 10 failures/4 passes. One test assumption was corrected to preserve SDK notification-union semantics, rather than tightening accepted inputs.
- Focused repair check: `PYTHONPATH=. .venv/bin/pytest -q tests/test_lab_mcp.py -k 'malformed_envelope_is_safe or parse_error_is_safe or sdk_http_initialize or malformed_protocol'` -> **16 passed, 24 deselected**. Tests assert correct HTTP 400/error codes and sentinel absence in responses, application logs, stdout/stderr for invalid jsonrpc/method/params, nested envelopes and parse failures.
- Compatibility check: `PYTHONPATH=. .venv/bin/pytest -q tests/test_lab_mcp.py -k 'sdk_accepted_envelopes or mcp_body_limit or malformed_body_preserves or sse_transport'` -> **12 passed, 40 deselected** after correcting the expected SDK Content-Type rejection from 415 to 400 and adding its distinct inner 415 case. Covers accepted 202/empty notifications/responses, exact cap/declared/chunked overflow, header errors and real SDK SSE initialization/discovery/all calls.
- Full suite: `PYTHONPATH=. .venv/bin/pytest -q` -> **52 passed in 13.26s**. Temporary loopback listeners stopped and worker shutdown assertions passed. No new dependencies, downloads, delegation, agent-log changes, deployment, cloud/API operations, commit or push. Existing review/coordinator edits preserved. LOW upload deadline/concurrency and mutable base/unhashed uv bootstrap findings remain deferred, not resolved here.
- Next: coordinator routes independent Tester/Security reruns of these regressions, then Architect acceptance against D-012; container execution remains unverified. Main review status must not change based solely on this Developer evidence.

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
- HISTORICAL NOTE (2026-10-20): the Tester saw a young GPU node (~17:08Z) and suspected eviction. That node (`...61997117...`) was the third pool created after two failed attempts (T-006), not an observed eviction. A later actual Spot eviction/recovery was recorded on 2026-10-21 (T-008); see router evidence above.
- FACT: Azure Policy admission warnings appear on pod creation (non-root, limits, read-only FS, capabilities); pods are still admitted, including the privileged plugin.

## Blockers

MCP Python dependency blocker is resolved through the approved feed only.
Container build/run still needs a running local Docker daemon; independent
LOCAL two-tool behavioral/security reviews and Architect acceptance are complete
for supervised loopback only; no blocker remains for that local source milestone.
Container/Linux runtime and packaging provenance are not accepted. See D-012
and final independent evidence above. Existing infrastructure risks:
1. Spot eviction can delete the GPU node at any time (D-008); the pool autoscaler (min=max=1) tries to replace it but capacity is best effort.
2. The device plugin runs privileged (T-007); needs review.

## Open questions

1. (resolved, D-010) llama.cpp image: `server-cuda13` works on this node; pinned by digest.
2. (resolved, D-010) First model: Qwen2.5-7B-Instruct Q4_K_M. Larger models up to ~30B at 4-bit should fit in the ~46 GiB MIG slice (untested).
3. (resolved, D-009) Model storage: Azure Disk PVC.
4. (resolved) `.github/copilot-instructions.md` is now complete.
5. `image.png` is tracked; previously suggested removal remains awaiting human approval.
6. Whether to submit a support ticket for standard GPU quota to allow non-Spot later.
7. Add a NetworkPolicy and an API key for llama-server before any wider exposure (Phase 11).

## Repository notes

- Earlier lab/governance/explanatory commits were pushed. Current MCP implementation, simplification, commenting-policy and handoff changes have not been committed or pushed during this work; do not treat earlier commit authorization as authorization for them.
- `main.py` and `pyproject.toml` now implement the D-012 MCP server; `.python-version` retains the Python 3.12 baseline.
- Failed GPU pools were deleted (they were our own failed artifacts). No other resources were deleted.

## Historical change inventory before the teaching revision

Earlier documentation-only edits and current implementation are distinct.
Final bounded Architect acceptance modifies only `STATUS.md`,
`docs/architecture.md`, `docs/decisions.md` and `README.md`; the implementation
inventory below describes earlier Developer work, not this acceptance pass.
This bounded Developer work changes `main.py`, `pyproject.toml`, `README.md`,
`STATUS.md`, `docs/architecture.md`, `docs/decisions.md`, `docs/troubleshooting.md`;
adds `config/lab-info.json`, `tests/test_lab_mcp.py`, `uv.lock`, `Dockerfile`,
`.dockerignore`, `k8s/mcp/lab-info.yaml`. Existing changes to
`docs/agent-execution-log.md` belong to the coordinator and were not edited here.

## Plan (remaining)

1. Phases 8-10: agentgateway v1.6.0 on the `app` pool; `Gateway`, `AgentgatewayBackend`, `HTTPRoute`; end-to-end request via port-forward.
2. Phase 11-12: Security Reviewer pass (privileged plugin, public API server, Spot, unauthenticated llama-server, no NetworkPolicy); teardown and rebuild test; update `preflight.sh` for Spot; test Spot eviction recovery.

## Next action

Next: walk through Kubernetes workload/Service wiring and gateway responsibilities
in a separate 10-15 minute teaching segment. The human confirms code understanding;
the written explanations are saved in README. Live execution/presentation and
timing have not been demonstrated to the human. The amended two-tool LOCAL source
is VALIDATED for supervised loopback only; gateway implementation stays paused.
Use the existing frozen approved-feed environment; never restore public PyPI
access as a workaround. This status refresh is documentation-only: no test rerun,
cluster operation, deployment, commit or push. Last recorded Docker prerequisite
check found the local daemon unavailable; it was not rechecked during this refresh.
Base-image
digest/availability, unhashed uv bootstrap provenance, Linux execution, Kubernetes
admission/scheduling/probes and live upstream behavior remain unverified gates
for separately authorized packaging/deployment work. Inbound upload
deadline/concurrency remains a LOW limitation before untrusted access. No
authentication, TLS, NetworkPolicy or customer-ready exposure is accepted.
Phase 8 gateway work stays paused; independent D-011 router-mode validation
remains a separate prerequisite before Phase 9. No deployment is authorized here.
