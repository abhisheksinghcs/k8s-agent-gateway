# STATUS

Last updated: 2026-10-27 (D-011 final bounded architectural ACCEPT; explicit historical offload and final-runtime/security prerequisites cleared; no model route authorized)

Current authority: the final architectural verdict in "Current D-011 Architectural
Acceptance" below supersedes earlier pending/hold statements for resolved gates.
Developer, Tester and Security Reviewer records retain their handoff-time wording;
they are historical evidence, not outstanding requests for another review.

## D-011 Final Independent Security Disposition (2026-10-27)

- Verdict: GO for continued private, trusted, supervised single-operator router
    use with synthetic/public data. The hardening and explicit human residual-risk
    dispositions clear the SECURITY prerequisite for separately authorized future
    private-route design. No new scoped blocker. This supersedes the earlier
    D-011 security hold for those resolved/disposed gates, NOT architectural
    acceptance, supported-release route proof, route implementation/deployment
    authorization or wider-access acceptance. Phases 9/10 remain PLANNED.
- Authority: reviewed D-011's exact human diagnostic/hardening approval and
    bounded risk acceptance; D-015's controller-authority acceptance is separate.
    Acceptance expires BEFORE sharing, a new untrusted workload/local user, wider
    exposure or target change. All workloads/local users must remain trusted.

### Findings And Disposition

- HIGH, accepted NOT fixed: unauthenticated plaintext router inference/model
    administration remains reachable by cluster workloads. Evidence: all-interface
    listener, ClusterIP:8080, no llm Ingress/NetworkPolicy; only existing exact
    MCP route, no model/admin gateway route. Impact: direct backend bypass,
    model-state/GPU/disk abuse and absent confidentiality. Recommendation: retain
    the accepted trust/data boundary for this lab; before customer/shared/untrusted
    access require separately reviewed authentication/authorization, transport and
    enforceable backend isolation; before production also restrict administration
    and resource abuse. No unauthorized network migration is required by this GO.
- HIGH, separately accepted NOT fixed: controller cluster-wide Secret-content
    get/list/watch and TokenReview create. Exact live role
    agentgateway-agentgateway-system confirms these rules; namespaced deployer
    binding does not narrow reads. Impact: controller compromise has broad
    credential blast radius. D-015 accepts this only for the existing lab.
    Recommendation: reconsider supported least-privilege/control-plane isolation
    before shared/customer/production use; no new authority is granted here.
- MEDIUM, confidentiality limitation remains: default verbosity 3 is not a
    general payload-safety guarantee; warning paths can expose generated output
    and temporary 4 can expose metadata/key suffixes. No selected credential/body
    marker was observed in reviewed logs. Synthetic/public traffic only and no
    diagnostic override are required for this bounded lab; review redaction and
    collector access/retention before private/customer data or broader use.
- Prior MEDIUM root/absent-seccomp finding is remediated in the observed router
    AND resident workers. Writable rootfs/model cache, inherited MCP reflection
    and availability residuals are not certified away. Read-only rootfs/writable-
    path validation and supply-chain/logging assurance remain future hardening,
    not new blockers for this unchanged trusted lab.

### Independent Checks And Limits

- Fresh read-only checks: final pod llama-cpp-5f676cf74f-vzjtv Ready/zero
    restarts, exact pinned imageID; UID/GID 10001, Seccomp 2, all five capability
    sets zero and NoNewPrivs 1 for PID 1 and workers 712/798/884. No token file,
    init container, host network/PID/IPC or credential envFrom. Selected key/log
    override presence checks and preset key/debug directives were absent.
    Pod lifecycle start is 20:36:47Z; container start is 20:37:01Z.
- Cache: rw ext4, Bound 64Gi RWO managed-csi-premium; CSI fsGroupPolicy=File.
    Root/model directories root:10001 2775, lost+found 2770; four root:10001
    blobs 0664, four 10001:10001 refs 0644, four symlinks. No world-writable
    non-symlink or inaccessible directory/dereferenced regular target. These are
    read/write/traverse permission checks, NOT a new write/download/remount test.
    Both retained before/after inventories compare equal; no full weight hashes.
- Current bounded log read: 361 lines, nine threshold-3 records, zero selected
    threshold-4/5, CUDA-init/offload or credential/body markers. Router args and
    worker/preset checks retain normal logging. This is not whole-log/image or
    remote-retention certification; no raw log/body/environment dump was output.
- Historical private diagnostic log independently correlates four aliases/ports
    40649/33453/36313/41137 with CUDA initialization and 29/29, 29/29, 33/33,
    41/41 actual offload records. Retained ReplicaSet specs compare identical
    after removing ONLY trailing --log-verbosity 4; surviving pod events
    corroborate the capture window. Diagnostic pod is deleted: no fresh final-pod
    offload logs or signed/tamper-proof provenance is claimed.
- Independently parsed retained Tester responses/status artifacts: four exact
    model matches, HTTP 200/curl exit 0/exact 42, completion counts 3/3/2/2;
    before/after health status ok. Tester reports nine scoped gates and existing
    suite 66 PASS/2 opt-in live-gateway SKIP. Reviewer did NOT rerun Python tests,
    inference, forwarding, downloads/admin APIs or live gateway requests.
- Commands executed: git status --short --untracked-files=all; git log -4
    --oneline; git diff/stat/numstat/check/cached-name and ls-files inventories;
    local Node full-content scans, safe evidence predicates/inventory comparisons;
    explicit-context kubectl get pod/ReplicaSets/events/PVC/CSIDriver/Services/
    Ingress/NetworkPolicy/gateway objects/selected RBAC and existing-pod exec for
    id, selected /proc status/cmdline/override presence and stat/find/mount access;
    bounded logs --timestamps --tail=500 with allowlisted/count-only output.
    EVERY Kubernetes call used --context=aks-agw-lab; local fallback because no
    deferred-tool loader is available. Missing rg (127) was handled locally;
    an empty RBAC label selection was corrected using exact observed role names.

### Public Repository And Architect Handoff

- Scanned complete contents of ALL 12 pending tracked/untracked files, not only
    added lines. No credential/private-content finding or raw diagnostic artifact
    path; JSON request example is the documented public arithmetic prompt. UUID
    candidates are operational pod/PVC IDs, a pre-existing subscription reference
    and a built-in role ID, not credentials. Registry diff is newline-only.
    Index is empty. Heuristic/manual review is not full-history secret assurance.
- Files inspected/read or fully scanned: PROJECT_CONSTITUTION.md,
    .github/copilot-instructions.md, .github/agents/security-reviewer.agent.md,
    STATUS.md, README.md, docs/architecture.md, docs/decisions.md,
    docs/troubleshooting.md, docs/agent-execution-log.md, infra/registry.bicep,
    k8s/llm/llama-cpp.yaml, k8s/gateway/controller-values.yaml,
    k8s/gateway/parameters.yaml, k8s/gateway/gateway.yaml, tests/test_gateway.py,
    relevant tests/test_lab_mcp.py contracts, pyproject.toml, .gitignore and
    .dockerignore; private diagnostic log, both cache inventory pairs, Tester
    response/status/health artifacts and private directory/file mode metadata.
- Modified ONLY STATUS.md for this final disposition; coordinator execution log
    untouched. No delegation, installs, workload/PVC/network mutation, cleanup,
    stage/commit/push or reviewer-created diagnostic artifacts. Existing private
    evidence remains outside Git in directories 0700/files 0600; preserve until
    Architect is done. No Secret objects or credential values were read.
- Publication prerequisite: coordinator stages explicit reviewed paths, excludes
    /tmp diagnostics/raw responses/credentials and reruns staged-content safety
    checks after any later edits. Empty index now cannot guarantee future staging.
- Next: Architect evaluates independent Tester evidence and this security GO,
    explicitly accepting or rejecting historical-offload provenance limits and
    reconciling historical pending claims in current docs. Future route work still
    requires supported v1.6.0 fixed-upstream/path/model proof, separate human
    authorization and independent post-implementation security/behavior checks.
    No gateway inference, route support, outage/recovery, concurrency, cache
    persistence/full-hash, hostile-client defense or shared/production acceptance.

## D-011 Independent Post-Hardening Validation (Tester, 2026-10-27)

- Verdict: bounded direct behavior and observed hardening VALIDATED. No failed
    behavioral gate. Historical explicit-offload evidence passes with the
    provenance limits below; this is NOT fresh offload logging from the final
    pod. Security review and architectural acceptance remain pending. No route
    clearance, phase acceptance or expansion of D-011 risk acceptance follows.
- Scope: read-only local kubectl fallback, EVERY invocation explicitly
    `--context=aks-agw-lab`; no deferred-tool loader available. No workload,
    verbosity, permission, infrastructure, route or MCP changes; no restart,
    download/admin API, installs, delegation, commit/push or execution-log edit.
    No Secret objects, token contents or credential values were read. Selected
    key/log override checks reported presence/absence only; all selected absent.

### Gate Results

| Gate | Result | Independent Evidence |
|---|---|---|
| Admitted and runtime hardening | PASS | UID/GID 10001, RuntimeDefault/Seccomp 2, all five capability sets zero, NoNewPrivs 1 for router and workers; eight captured process records, zero violations; token absent, no init container/host networking |
| Image, args, preset and storage drift | PASS | Exact pinned digest below; build 11749/1d88cb05f; four mounted Q4_K_M presets match manifest; models-max 3, context 8192, ngl 99, default verbosity 3; same Bound 64Gi RWO managed-csi-premium PVC |
| Cache permissions and inventory | PASS (permission-level write check) | UID 10001 can read all dereferenced files and write/traverse all cache directories and regular targets; no arbitrary write probe; no world-writable regular file/directory; before/after type/size/path/symlink inventories identical |
| GPU prerequisites and workers | PASS | All three nodes Ready; GPU node allocatable nvidia.com/gpu=1; alias-correlated GPU compute processes and CUDA library mappings observed |
| Historical explicit CUDA/offload | PASS, historical only | Private full log independently extracted alias/port/repository/build/device/X/Y records for all four models; retained ReplicaSet and pod events corroborate capture window, not cryptographic provenance |
| Health and discovery | PASS | HTTP 200/status ok before and after; four exact source=preset IDs plus four source=cache entries; final three loaded presets |
| Four bounded direct inference requests | PASS | Four HTTP 200, curl exit 0, exact content 42, requested model echoed, positive usage; table below |
| Exposure, route and MCP boundary | PASS (observed scope) | Relevant Services ClusterIP/no externalIPs; no llm Ingress; only generation-1 exact /mcp HTTPRoute/backend/Gateway; MCP deployment remains generation 1 and existing image; no model/admin route |
| Existing manifest/protocol regressions | PASS | Full existing two-file suite: 66 passed, 2 skipped in 14.13s; skipped tests require live gateway opt-in, intentionally not set |

- Final pod `llama-cpp-5f676cf74f-vzjtv`, UID
    `d155416b-83e2-4990-8217-673e69593594`, started 20:37:01Z on
    `aks-gpunp-61997117-vmss000017`, remained Ready/zero restarts after requests.
    ImageID is `ghcr.io/ggml-org/llama.cpp@sha256:78d0541639f5ed3f463e4bef8284027792e2d74cc2311b7628e17c2a0e7587db`;
    executable reports `0.7.0-dev (build 11749, commit 1d88cb05f)`.
- Exact structured comparisons: diagnostic ReplicaSet pod spec equals final
    ReplicaSet pod spec after removing only trailing `--log-verbosity 4`;
    final Deployment pod spec equals private baseline after excluding only
    pod securityContext. This bounds image/args/env/resources/volumes/scheduling
    drift; admission-added GPU requests/tolerations were also inspected.
- Cache root/model directories root:10001 2775, lost+found 2770. Four regular
    blobs are root:10001 0664; four refs are 10001:10001 0644. Eight regular
    files/four symlinks, rw ext4 mount, CSI fsGroupPolicy=File. Symlink 0777 mode
    is not world-write permission on its target. No repair or initializer used
    by Tester; no actual new-file write/download, full hash, persistence or
    fsGroup remount test is claimed. Historical before/after inventories also
    compare equal; current independent inventory compares equal across requests.

### Direct Responses And Runtime GPU Evidence

Public prompt: `What is 17 + 25? Reply with only the number.` Each request used
temperature 0, max_tokens 32, stream false, curl deadline 600s, sequentially
through owned `127.0.0.1:18080`. All HTTP 200/exact `42`/positive usage:

| Preset | Completion Tokens | Seconds | Observed Worker PID / Port / GPU MiB |
|---|---|---|---|
| qwen2.5-7b-instruct | 3 | 3.809582 | 610 / 51277 / 5398 (captured before later eviction) |
| qwen2.5-coder-7b-instruct | 3 | 3.873356 | 712 / 44917 / 5398 |
| llama-3.1-8b-instruct | 2 | 3.424428 | 798 / 47325 / 6190 |
| phi-4 | 2 | 4.201650 | 884 / 57669 / 10738 |

- Ordinary LRU evicted Coder for Qwen, Llama for Coder, Phi for Llama, then
    Qwen for Phi; discovery never exceeded three loaded presets. Final workers
    are Coder/Llama/Phi. GPU is RTX Pro 6000 Blackwell DC-4-48Q, MIG enabled,
    driver 595.91.07/CUDA 13.4. Structured nvidia-smi queries returned
    Insufficient Permissions; ordinary nvidia-smi supplied numeric PIDs/memory
    without escalation. No download-matching live log lines, and unchanged
    inventory supports cached operation; not network-egress certification.
    Timings include these cache-backed loads, not a cold-download/throughput test.

### Historical Log Provenance And Limits

- Reviewed targeted extraction from private `/tmp/d011-gates.oMokHP/diagnostic-full.log`
    (133498 bytes, 0600; directory 0700), not copied documentation or broad raw
    payload output. Each child logs build 11749/1d88cb05f, exact bartowski
    repository/Q4_K_M and threshold 4; port-tagged CUDA initialization identifies
    one RTX Pro 6000 Blackwell MIG 4g.48gb, compute 12.0, VMM no, 48838 MiB.

| Preset | Historical Port | CUDA Initialization UTC | Actual Offload UTC / Count |
|---|---|---|---|
| qwen2.5-7b-instruct | 40649 | 20:19:52.670382904 | 20:20:39.602304678 / 29/29 |
| qwen2.5-coder-7b-instruct | 33453 | 20:20:44.416275063 | 20:21:31.231540213 / 29/29 |
| llama-3.1-8b-instruct | 36313 | 20:21:35.985750297 | 20:22:25.229433918 / 33/33 |
| phi-4 | 41137 | 20:22:30.544225461 | 20:24:00.113744727 / 41/41 |

- Lines explicitly say `ggml_cuda_init: found 1 CUDA devices` and
    `load_tensors: offloaded X/Y layers to GPU`, correlated to router alias/port
    spawn and repository lines. Retained ReplicaSet `llama-cpp-578cb5c7b9`,
    created 20:16:52Z, holds the same pin/hardening plus verbosity 4. Surviving
    events identify historical pod `llama-cpp-578cb5c7b9-c9dx5`, UID
    `ab07469c-8050-4a67-875e-fa2c33f0a6e1`, Started 20:17:02Z/Killing 20:36:45Z;
    log starts 20:17:02Z. That pod is deleted: no fresh retrieval/imageID or
    signed/tamper-proof chain can be established. Corroboration supports this
    historical capture, not independent observation of the original rollout.
- Final default-3 log has zero explicit CUDA/offload lines, as expected. Fresh
    inference/process/GPU evidence is separate; historical ports/counts are NOT
    asserted as freshly logged final-pod counts. No restart/verbosity change was
    made to recreate them. Remote log retention/access remains uncertified.

### Reproduction, Cleanup And Handoff

- Commands actually used: `kubectl --context=aks-agw-lab -n llm get pod
    llama-cpp-5f676cf74f-vzjtv -o json`; `get deployment llama-cpp -o json`;
    `get replicasets -l app=llama-cpp -o json`; `get pvc llama-models -o json`;
    existing-pod `exec ... -c llama-server -- sh -c` for id, selected /proc
    status/cmdlines/maps, mounted preset, stat/find permissions/inventories and
    `nvidia-smi`; `exec ... -- sh -c '/app/llama-server --version 2>&1'`.
    All get/exec/log/event/node/Service/route/CSI calls used explicit context.
- Forward: `kubectl --context=aks-agw-lab -n llm port-forward --address 127.0.0.1
    service/llama-cpp 18080:8080`. HTTP requests follow README's exact curl
    arithmetic body/flags with each table alias and private `-o` response plus
    `-w 'http=%{http_code} exit=%{exitcode} seconds=%{time_total}\n'` capture.
    GET `/health` and `/v1/models` only otherwise; no model-admin operation.
    Private log extraction used grep/awk restricted to build, spawn, hf-repo,
    verbosity, CUDA/device, actual offload and LRU records.
- Tests: `env -u GATEWAY_TEST_URL PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.
    .venv/bin/pytest -q tests/test_lab_mcp.py tests/test_gateway.py -p no:cacheprovider`.
    Existing interpreter/dependencies only; no install or environment change.
- Owned forward stopped with Ctrl-C; lsof confirms no listener on 18080.
    All synchronous clients completed. Historical artifacts preserved unchanged
    for Security Reviewer/Architect; new response/runtime/cache evidence retained
    privately in `/tmp/d011-tester.D4YsvT` (0700/files 0600). No raw diagnostics
    added to Git. Dirty work preserved; no coordinator execution-log edits.
- Inspected: constitution, STATUS, repository/tester instructions, architecture,
    relevant decisions/troubleshooting, README, llama manifest, both test files,
    pyproject; private historical log/worker excerpts/baseline/inventory metadata;
    runtime resources/process/cache/GPU/route observations above. Modified only
    STATUS.md and docs/troubleshooting.md. Immediate documentation
    `git diff --check` passed; no source/tests/manifests modified by this assignment.
- Remaining: Security Reviewer assesses artifacts/hardening/risk disposition;
    Architect evaluates independent evidence with historical provenance limits.
    No gateway inference, live MCP regression, outage/recovery, concurrency,
    malicious-client defense, precise Recreate downtime or full-cache hash test.
    Existing unauthenticated/plaintext/direct-admin reachability remains within
    the recorded bounded human acceptance, not remediated or certified here.
    Phases 9/10 remain PLANNED and no new model route is authorized.

## D-011 Bounded Developer Gate Resolution (2026-10-27; DEPLOYED)

- Human selections: **"Approve bounded diagnostic and hardening"** and
    **"Accept bounded lab risks"**. Full scope/expiry is recorded in D-011 in
    docs/decisions.md: brief Recreate, temporary verbosity 4 synthetic arithmetic,
    non-root/RuntimeDefault and only necessary existing-volume permission repair.
    Plaintext/unauthenticated HTTP, unrestricted reachability/direct model admin
    and resource/state abuse are accepted ONLY for future private supervised
    single-operator use, trusted workloads/local users, synthetic/public data.
    Expires BEFORE sharing, new untrusted workload, wider exposure or target change.
    NO route authorization; phases 9/10 remain PLANNED.
- CREATED/DEPLOYED: manifest adds UID/GID 10001, runAsNonRoot, RuntimeDefault and
    fsGroup 10001/OnRootMismatch. Immediate server dry-run passed, other objects
    unchanged. Existing image/presets/storage/scheduling/security controls retained.
- Baseline: Ready llama-cpp-74c6bc49b5-6pvtb, zero restarts on GPU node
    aks-gpunp-61997117-vmss000017; UID/GID 0, Seccomp 0, CapEff 0, NoNewPrivs 1.
    Four root-owned model trees 0755/files 0644; sole 0700 directory is lost+found.
    Azure Disk CSIDriver fsGroupPolicy=File. No manual repair/root init planned.
- Rollout: hardened pod llama-cpp-5f676cf74f-kw6vw reached Ready/zero restarts;
    actual UID/GID 10001, Seccomp 2, CapEff 0, NoNewPrivs 1, token absent.
    Supported fsGroup changed cache dirs to root:10001 2775 and lost+found 2770;
    write probe passed and was removed. No manual chmod/chown/root init used.
- Temporary threshold-4 pod llama-cpp-578cb5c7b9-c9dx5, same image pin/build
    11749/1d88cb05f, returned HTTP 200/exact 42 for all four sequential public
    arithmetic requests (temperature 0, max_tokens 32, stream false, deadline
    600s each). Completion tokens 3/3/2/2; seconds 48.586/48.328/50.844/91.782,
    including loads, not warm/throughput benchmarks. Normal idle-LRU Qwen eviction
    for Phi observed, no administration endpoint invoked.
- Explicit Developer offload evidence, port-correlated to exact aliases:

| Preset | Child Port | CUDA Found | Actual Layer Line |
|---|---|---|---|
| qwen2.5-7b-instruct | 40649 | 1 device, 20:19:52Z | `load_tensors: offloaded 29/29 layers to GPU`, 20:20:39Z |
| qwen2.5-coder-7b-instruct | 33453 | 1 device, 20:20:44Z | `load_tensors: offloaded 29/29 layers to GPU`, 20:21:31Z |
| llama-3.1-8b-instruct | 36313 | 1 device, 20:21:35Z | `load_tensors: offloaded 33/33 layers to GPU`, 20:22:25Z |
| phi-4 | 41137 | 1 device, 20:22:30Z | `load_tensors: offloaded 41/41 layers to GPU`, 20:24:00Z |

- Device each time: NVIDIA RTX Pro 6000 Blackwell DC-4-48Q MIG 4g.48gb,
    compute 12.0, VMM no, reported VRAM 48838 MiB. Captured router/child-worker
    security remained UID/GID 10001/Seccomp 2/CapEff 0/NoNewPrivs 1; workers
    inherited threshold 4. Selected API/HF key and log overrides were absent;
    no credential values printed, level 5/private traffic/browser UI excluded.
- Default threshold 3 restored by server-dry-run/apply of checked-in manifest;
    new pod llama-cpp-5f676cf74f-vzjtv Ready/zero restarts on node 000017. Final
    four-model cached inference passed HTTP 200/exact 42/positive completion usage
    3/3/2/2; seconds 48.015/47.625/50.161/91.031, same bounded public prompt and
    parameters as diagnostic requests. Final health status ok; at 20:42:31Z GPU
    compute PIDs 217/308/400 (Coder/Llama/Phi) held 5398/6190/10738 MiB. Router
    and these workers all had UID/GID 10001, every CapInh/Prm/Eff/Bnd/Amb set 0,
    NoNewPrivs 1 and Seccomp 2. Token absent; no logging override in live args.
    Final imageID equals ghcr.io/ggml-org/llama.cpp@sha256:78d0541639f5ed3f463e4bef8284027792e2d74cc2311b7628e17c2a0e7587db;
    pod started 20:37:01Z. Existing Service ClusterIP:8080 and bound 64Gi PVC
    pvc-01eac67d-00af-493e-b0b9-7a6597404a70 unchanged. Cache inventory diff empty;
    no world-writable cache files found. Cache write test removed its own file.
    Diagnostic forward 127.0.0.1:55957 closed with owned Ctrl-C. Full startup
    captures private outside Git; only reviewed excerpts above are durable.
    Defender host-log access exists; remote retention/access not certified or
    changed, and local deletion cannot remove Kubernetes/collector copies.
- Three approved Recreate rollouts (hardening, temporary 4, restore 3). Readiness
    watches completed in roughly 20-31s; precise endpoint downtime was not sampled.
    Model workers reload cold after replacement. T-003 early/incomplete terminal
    output recurred; private HTTP artifacts prevent blind duplicate requests.
    Earlier missing rg exit 127 was a read-only tooling failure, not workload failure.
- Next: independent Tester must repeat behavior/security observations;
    Security Reviewer assesses
    hardening/cache/logging/risk disposition; Architect evaluates only their
    evidence. No independent VALIDATED/acceptance or model-route clearance claimed.
- Existing dirty work preserved; no agent-execution-log edit, route, infrastructure,
    dependency, image build/push, commit/push or administrative model operation.
- Focused offline check: existing `test_curated_and_packaged_config_drift`
    passed (1 passed, 62 deselected, 2.06s), using installed pytest with
    PYTHONPATH=. and no bytecode/cache provider. Server dry-run passed before
    each workload change; git diff --check passed. Existing editor warning for
    absent CPU limit is unchanged/out of scope. Cache size/path/symlink inventory
    diff is empty; not a full-content hash or independent persistence test.
- Files inspected: PROJECT_CONSTITUTION.md, this STATUS, .github repository
    instructions/developer profile, docs/architecture.md, docs/decisions.md,
    docs/troubleshooting.md, README.md, k8s/llm/llama-cpp.yaml, relevant existing
    tests/test_lab_mcp.py and tests/test_gateway.py contracts; pinned upstream
    CUDA Dockerfile/common/log.cpp/server-models.cpp and Kubernetes security-
    context documentation. Azure diagnostics/AKS skill guidance was read.
- Files modified by this assignment ONLY: k8s/llm/llama-cpp.yaml, STATUS.md,
    README.md, docs/architecture.md, docs/decisions.md, docs/troubleshooting.md.
    Coordinator owns docs/agent-execution-log.md; it was not edited.
- Private rollback/source/runtime evidence is under /tmp/d011-gates.oMokHP
    (0700; log 0600). Keep for independent review, then remove diagnostic logs/
    responses/worker captures. Final lsof check found no listener on owned 55957;
    process check found no owned inference/forward client remaining. Original pod
    template is in baseline-deployment.json and clean last-good manifest snapshot
    in last-good.yaml outside Git. Source rollback removes only the newly added
    pod securityContext; dry-run/apply then retains all pre-existing container
    controls/image/presets/PVC. Group metadata need not be reverted for root.
    Returning to root/absent seccomp is not an accepted final security posture.
- Reproduction/check commands: `kubectl --context=aks-agw-lab apply
    --dry-run=server -f k8s/llm/llama-cpp.yaml`, then `apply -f` and
    `kubectl --context=aks-agw-lab -n llm rollout status deployment/llama-cpp
    --timeout=240s`; temporary JSON-patch appended only `--log-verbosity`, `4`,
    and checked-in-manifest apply removed them. Named diagnostic pod full logs
    used `logs pod/llama-cpp-578cb5c7b9-c9dx5 -c llama-server --timestamps
    --tail=-1` with explicit context/namespace. Final requests used existing-pod
    `exec llama-cpp-5f676cf74f-vzjtv -c llama-server -- curl --noproxy '*'
    -sS --max-time 600` to loopback:8080/v1/chat/completions, never model-admin.
    Process status/cmdlines, id, nvidia-smi, stat/find and cache inventory diff
    supplied runtime evidence. Offline: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.
    .venv/bin/pytest -q tests/test_lab_mcp.py -k curated_and_packaged_config_drift
    -p no:cacheprovider`; final `git diff --check` passed.
- Tooling limitation: no deferred-tool loader available; used authorized local
    kubectl fallback, every operation explicitly --context=aks-agw-lab. No context
    switch, Azure/pool/network operation, installs, dependency changes or delegation.

Labels used: FACT, DECISION, ASSUMPTION, HYPOTHESIS, OPEN QUESTION.
Lifecycle: PLANNED -> CREATED -> DEPLOYED -> VALIDATED (or FAILED).

## D-011 Independent Security Review (2026-10-27)

- Verdict: NO-GO for new model-route implementation/deployment until the gates
    below are met. Conditional GO for a separately authorized temporary offload
    diagnostic using only synthetic public data within the existing trusted,
    supervised single-operator boundary. No new blocker to unchanged historical
    lab use is asserted. D-015 CPU/MCP GO is not router clearance; no phase
    acceptance, human risk acceptance or model-route authorization is granted.
    This review supplements the earlier Architect verdict below, including its
    then-current statement that a separate security review had not occurred.
- Scope/evidence: governing docs/security profile, current STATUS/architecture,
    D-011/D-014/D-015 decisions, README direct/gateway guides, llama manifest,
    all three gateway inputs and gateway tests; pending tracked diffs and four
    untracked gateway/test inputs. Read-only local kubectl fallback was used
    because no deferred-tool loader is available; EVERY command explicitly used
    `--context=aks-agw-lab`. No context switch or Secret values were read.
- Fresh runtime FACT: existing pod `llama-cpp-74c6bc49b5-6pvtb` imageID matches
    the pinned digest and args still omit logging overrides. `/proc/1/status`
    and `id` show UID/GID 0, CapEff=0, NoNewPrivs=1, Seccomp=0. Service is
    ClusterIP:8080 without externalIPs; no llm Ingress/NetworkPolicy, no
    hostNetwork, token automount false and token file absent. Recorded cluster
    network-policy engine is none; no engine migration/policy objects proposed.

### Findings And Minimum Developer Contract

1. HIGH for new/untrusted access: unauthenticated model administration and
    inference share plaintext, unisolated HTTP. Manifest binds all pod interfaces;
    pinned server registers POST/DELETE `/models` and POST `/models/load` and
    `/models/unload`. Other cluster workloads can bypass any gateway route and
    change/download/delete model state or consume GPU/disk. ClusterIP, localhost
    forwarding, CORS and gateway path filtering are not caller authentication or
    direct-backend isolation. Required before new lab routing: explicit human
    disposition below OR a separately reviewed authentication/transport design.
    Before customer/shared access, implement authentication/authorization and
    confidentiality at both hops plus an enforceable direct-backend boundary;
    before production also separate/restrict administration and bound resource
    abuse. Do not silently add identities/resources or migrate Cilium here.
2. MEDIUM: root process and absent seccomp increase impact of server/model-parser
    compromise despite dropped capabilities/no escalation/token absence.
    Proposed minimum before new lab routing: pod `runAsNonRoot: true`,
    `runAsUser: 10001`, `runAsGroup: 10001`, `seccompProfile.type: RuntimeDefault`;
    retain existing drop-ALL/no-escalation/GPU scheduling/token policy. Numeric
    UID/GID 10001 is a proposed choice, NOT tested image support. The pinned
    CUDA Dockerfile runs the binary directly with no application USER requirement;
    live executable/app are 0755, observed GPU nodes 0666/capability files 0444.
    These permissions are prerequisites, not proof of non-root CUDA operation.
    `/models` is root:root 0755; depth-three inventory found 21 directories 0755,
    one 0700, eight files 0644. Changing UID alone is NOT safe. Evaluate pod
    `fsGroup: 10001` with `fsGroupChangePolicy: OnRootMismatch` and actual CSI
    ownership handling first; this may mutate existing PVC metadata and needs
    explicit permission. No recursive chown, root init container or chmod 777
    workaround is authorized. Verify cache traversal/read/write/download needs,
    child spawning, CUDA libraries/devices and tmp paths before rollout.
    Docker inspect found no locally cached pinned image; no pull/run attempted.
    Local compatibility and actual AKS RuntimeDefault syscall compatibility are
    UNVERIFIED. Under separate authorization validate admission, UID/GID/seccomp=2
    for router AND workers, readiness, all four inference/offload paths and cache
    usability. Never silently fall back to root/Unconfined. Failure requires a
    narrow repair or explicit human exception. Read-only rootfs with bounded tmp
    is recommended for demos/production after writable-path validation, not an
    assumed prerequisite for this minimal lab change.
3. MEDIUM diagnostic confidentiality: verbosity 4 is TRACE, not payload-safe.
    Pinned `server-http.cpp` logs method/path/peer/status at 4 and a single API
    key's final four characters at 4. Request/response dumps and token text are
    DEBUG=5; `server-models.cpp` prints child argv already at INFO=3. Never put
    keys/tokens in CLI/presets or assume a future key-file removes every logging
    risk. `common/chat.cpp` can log unparsed generated output at WARNING even
    below 4; slot-debug can emit prompt fragments. This is not a new observed
    leak from this pod, but rules out a general no-prompt/no-secret logging claim.

### Safe Diagnostic Limits And Remaining Gates

- Pinned-source basis: commit `1d88cb05f1a257f90741538ca3aca6c1b015c6d3`,
    `common/log.h`, `common/log.cpp`, `common/chat.cpp`, `common/arg.cpp`,
    `common/preset.cpp`, `.devops/cuda.Dockerfile`, and server HTTP/context/chat/
    task/models/common/main sources. In particular
    [HTTP metadata/key suffix/body levels](https://github.com/ggml-org/llama.cpp/blob/1d88cb05f1a257f90741538ca3aca6c1b015c6d3/tools/server/server-http.cpp#L229),
    [warning-level generated output](https://github.com/ggml-org/llama.cpp/blob/1d88cb05f1a257f90741538ca3aca6c1b015c6d3/common/chat.cpp#L1667),
    [child argv logging](https://github.com/ggml-org/llama.cpp/blob/1d88cb05f1a257f90741538ca3aca6c1b015c6d3/tools/server/server-models.cpp#L1445).
    Source inspection is bounded, not whole-image/dependency certification.
- Safe diagnostic contract: temporary `--log-verbosity 4` ONLY, same pinned image,
    presets/GPU/context/cache/endpoints; no level 5/verbose, prompt-directory,
    JSONL, slot-debug or trace overrides. Check actual args and selected override
    presence without environment/credential dumps. Selected live overrides checked
    were unset. Use only README's public arithmetic prompt, sequentially for four
    approved presets, `max_tokens=32`, `stream=false`, client deadline 600 seconds
    each; no concurrent normal/customer traffic, secrets, private data or browser
    UI. This limits input sensitivity, not proof that arbitrary output is safe.
- Authorize Recreate interruption/model reload first. Capture named new-pod
    startup logs from deployment through the four loads with explicit context,
    timestamps and finite collection duration, not a trailing 300-line window
    that can miss loads. Keep raw logs private/outside Git with restrictive local
    permissions; inspect locally and retain only reviewed alias/port, CUDA device,
    observed `offloaded X/Y` counts, status/usage/times. Do not dump raw logs into
    chat or Git; filtering does not prevent sensitive originals in Kubernetes
    logs/collectors. Check existing collection/retention/access and delete local
    diagnostics when no longer needed. Revert to threshold 3 after capture under
    the same approval, accounting for another Recreate. No historical log recovery
    is implied. Explicit CUDA initialization AND actual X/Y for EACH model plus
    fresh successful responses remain UNSATISFIED until independently observed.
- Minimum future route contract, not implemented: separately verify v1.6.0
    supported backend/path/model handling; fixed llama Service upstream, exact
    POST `/v1/chat/completions` only (GET discovery only if explicitly needed),
    no generic `/` or `/v1` prefix/admin/UI forwarding, no dynamic destination or
    caller-selected credentials. Preserve exact MCP route and all existing
    control-plane security. Test denied admin/unrelated paths, all four approved
    model mappings and safe logs. Unknown models must not broaden the approved
    catalog. Path restrictions do NOT fix direct Service access. Independent
    gateway inference validation/security review still follows implementation.
- Exact human decision needed if controls are deferred: explicitly accept, for
    the new private model route ONLY, unauthenticated plaintext client/proxy/model
    traffic and unrestricted cluster reachability including direct model admin
    access, resource/state abuse and absent confidentiality; affirm all cluster
    workloads/local users are trusted, one supervised operator, synthetic/public
    data only, no sharing/customer/public access; record an expiry/revisit trigger
    on changed users/workloads/data/exposure. Alternatively keep routing blocked
    and request a separately scoped control design. Existing D-015 RBAC acceptance
    does not answer this question. A general request to resolve gates/commit is
    not informed risk acceptance. Root/seccomp exceptions need separate explicit
    disposition if validated hardening cannot be delivered.
- Public-repo check: heuristic credential scan of 1,305 tracked added lines plus
    four untracked gateway/test files found zero candidates; bounded manual review
    found no new credential/private-content finding. Operational identifiers are
    not credentials. This is not full history/secret certification; coordinator
    must rerun scoped checks after later edits and before publishing.
- Checks/scope: Git status/recent history/diff/diff-check, immutable upstream
    HTTPS source reads, read-only kubectl get/exec process/filesystem observations,
    cached-image inspect only. No inference/forward, log-level/workload/PVC mutation,
    install/build/push, delegation, commit/push or execution-log edit. Only this
    STATUS review was added; prior dirty work preserved. Immediate scoped document
    validation follows. Unresolved: hardening runtime/cache compatibility, actual
    offload logs, human network/auth disposition and supported-release route proof.

## Current D-011 Architectural Acceptance (2026-10-27)

- DECISION: ACCEPT D-011 as bounded VALIDATED for the unchanged trusted,
    supervised single-operator lab. The explicit initialization/offload gate and
    router hardening/security prerequisite are satisfied on the recorded evidence.
    D-011 model-prerequisite clearance is granted, NOT route authorization or
    acceptance of a gateway model path. Phases 9/10 remain PLANNED.

| Gate | Architectural Disposition |
|---|---|
| Explicit CUDA initialization and actual offload | SATISFIED, historical diagnostic only: independent Tester correlated aliases/repositories/child ports 40649/33453/36313/41137 with initialization and Qwen 29/29, Coder 29/29, Llama 33/33, Phi 41/41; Security Reviewer corroborated the retained evidence |
| Diagnostic provenance and final configuration | ACCEPT bounded provenance: retained ReplicaSet specs differ only by trailing verbosity 4; events corroborate the capture window; same pinned build 11749/1d88cb05f. Deleted diagnostic pod prevents fresh retrieval or tamper-proof provenance. These are NOT fresh final-pod startup logs |
| Final direct inference, health, discovery and LRU | SATISFIED: independent four HTTP 200/exact `42`/matching-model results, completion tokens 3/3/2/2; health ok before/after; four presets plus four cache entries; max-three/ordinary LRU preserved; GPU workers/CUDA mappings correlated separately |
| Final hardening and cache compatibility | SATISFIED within observed scope: Ready/zero restarts, same image; router/resident workers UID/GID 10001, RuntimeDefault/Seccomp 2, all capability sets zero, NoNewPrivs 1, no token; default verbosity 3 restored. fsGroup 10001 supplied existing-PVC access without root init/manual repair/world-write |
| Independent regression and security review | SATISFIED: Tester nine gates PASS, existing suite 66 PASS/2 opt-in live-gateway SKIP; final Security Reviewer GO, root/absent-seccomp remediated, no new scoped blocker. No tests rerun by Architect |

- Rationale: accept actual independently reviewed initialization/count records
    plus separately observed final-runtime behavior; do not infer counts from
    `-ngl 99` or demand a repeat diagnostic solely for reassurance. Historical
    full reported X/Y offload applies to those diagnostic model loads, not a
    fresh exact-layer measurement of final default-3 workers.
- Accepted HIGH risks remain NOT fixed: plaintext/unauthenticated HTTP,
    unrestricted cluster reachability, direct model administration and GPU/disk/
    state abuse; controller cluster-wide Secret reads/TokenReview remain under
    separate D-015 acceptance. ONLY trusted workloads/local users, supervised
    single operator and synthetic/public data. Acceptance expires BEFORE sharing,
    new untrusted workloads/local users, wider exposure or target change.
- MEDIUM logging confidentiality remains: default 3 can expose generated output
    on warning paths; temporary 4 is not payload-safe. Remote retention/access,
    whole-log/image safety and full-history secret assurance are not certified.
    Publish only reviewed public-safe summaries, never raw captures/credentials.
    Coordinator owns restricted private evidence cleanup after review; local
    deletion does not remove Kubernetes/collector copies.
- Limits: cache type/path/size/symlink inventories match, not full-content hashes.
    Permission checks are not independent new-write/download/remount tests. No
    new persistence/recovery, precise downtime, concurrency, throughput, hostile-
    client defense, wider-access, model tool-calling or agent-loop claim. D-015
    remains CPU/MCP-only; live gateway outage behavior remains deferred.
- NEXT: coordinator records this review in its execution log and owns eventual
    explicit-path staging/commit/push after staged-content safety checks. Future
    separately authorized design must prove exact v1.6.0 fixed-backend support,
    narrow inference paths and no admin/catch-all route; separately authorized
    implementation then needs independent gateway behavior/security validation
    and architectural acceptance. No model route is authorized by this verdict.
- Rollback/reassess: restore the checked-in default-3 hardened manifest if a
    diagnostic override recurs, subject to rollout approval. Do not silently
    return to root/Unconfined, loosen permissions or delete weights/PVCs. A
    hardening regression, changed image/model/args/CSI/cache layout, permissions
    or trust/exposure boundary requires stopping affected use and reassessment;
    the historical insecure baseline is not an accepted steady state.
- This review inspected governance/profile, current/historical reports, README,
    architecture/decisions/troubleshooting, coordinator execution records, llama
    manifest and relevant tests; checked local Git status/history and focused
    documentation diffs/diagnostics. Modified only STATUS.md, README.md,
    docs/architecture.md and docs/decisions.md. No delegation, runtime/cloud
    requests, test reruns, installs, builds, deployment, workload/PVC/network
    mutation, cleanup, staging, commit or push. Existing dirty work and the
    coordinator-owned execution log are preserved.

## D-011 Explicit Offload Log Investigation (Tester, 2026-10-27)

- Verdict: explicit CUDA initialization/offloaded-layer gate remains UNSATISFIED.
    This read-only investigation does not change the Architect verdict above or
    substitute GPU allocations/configured `-ngl 99` for startup-log proof.
- Hypothesis/check: missing lines might be outside the earlier time window or
    suppressed by release logging. Read all retained logs without `--since`:
    `kubectl --context=aks-agw-lab -n llm logs
    pod/llama-cpp-74c6bc49b5-6pvtb -c llama-server --timestamps --tail=-1`.
    Result: 17 lines, first `2026-10-27T19:27:56.065306587Z`, last
    `2026-10-27T19:27:57.411215010Z`; no CUDA/offload/layer/spawn matches.
    Earlier tested pod `llama-cpp-74c6bc49b5-75d9c` returns NotFound. Its
    historical inference evidence remains historical, not a new-pod validation.
- Current pod started `19:24:42Z`, Ready with zero restarts; imageID is the same
    manifest digest. Read-only `/proc/1/cmdline`, selected logging environment
    and `/config/models.ini` confirm unchanged args/four approved presets,
    `LLAMA_CACHE=/models`, no explicit logging override, and no existing model
    worker. Full two-stream `/app/llama-server --version` reports
    `0.7.0-dev (build 11749, commit 1d88cb05f)`, GNU 14.2.0/Linux x86_64.
- Controlling configuration verified against immutable upstream commit
    `1d88cb05f1a257f90741538ca3aca6c1b015c6d3`: default verbosity is 3;
    `common/log.cpp` maps backend INFO/CONT to TRACE=4 and drops messages above
    the threshold. `common_init` installs that callback; `llama_log_set` also
    installs it for GGML. CUDA initialization uses GGML_LOG_INFO; explicit
    `offloaded %d/%d layers to GPU` uses LLAMA_LOG_INFO. Router child stderr is
    forwarded with LOG (level 0), not suppressed at a router debug threshold.
    Thus backend INFO suppression, not just a short log window, explains why
    the deployed setting cannot supply the required lines during normal loads.
- Supported-release README/parser expose `--log-verbosity 4` (equivalent env
    `LLAMA_ARG_LOG_VERBOSITY=4`); model workers inherit router options/environment.
    No retrospective startup-log API was identified in the inspected release
    docs/source; `--log-file` is an output sink, not recovery of discarded lines.
    Exact source links and reproduction are in troubleshooting below.
- Minimal next action for Developer, NOT implemented or authorized here: add
    only temporary router args `--log-verbosity`, `4`, preserving image, presets,
    cache, GPU/layer/context settings and endpoints. Deployment uses Recreate,
    so obtain authorization for interruption/replacement and increased diagnostic
    logging before applying. Avoid `--verbose`/level 5 and prompt logging.
- Focused validation after that separate change: verify live threshold 4 and
    inherited worker args; use README's localhost-only forward and one sequential
    bounded chat request per approved preset. Capture full startup logs with
    explicit context/timestamps; correlate each spawn alias/port with CUDA device
    initialization and actual `offloaded X/Y layers to GPU`, recording observed
    counts rather than assuming them. Require HTTP 200/nonempty response/positive
    completion usage. Stop owned forward; Developer may revert temporary logging
    under the same authorization. No broad suite or forced outage is needed.
- Cleanup/scope: no forwards or inference clients created; no workload/cloud/PVC
    changes, installs, capacity/admin operations, commit/push, delegation or
    execution-log edits. Only STATUS and reusable troubleshooting notes changed;
    pre-existing dirty work preserved. Separate security/model-route gates remain.

## Independent D-011 Direct Router Validation (2026-10-27)

- FACT (fresh independent Tester, beginning 18:19 UTC): direct router health,
    configured discovery, all four preset inference requests and observed normal
    three-model loading behavior passed. This is behavioral VALIDATED evidence,
    NOT architectural acceptance. Historical Developer results below were not
    used as proof. Phases 9/10 remain PLANNED; gateway inference, tool calling,
    agent loops and broader security acceptance were excluded.
- Target: every Kubernetes command used `--context=aks-agw-lab`; no context
    switch. Node `aks-gpunp-61997117-vmss000015` Ready, GPU allocatable 1;
    `llama-cpp-74c6bc49b5-75d9c` remained Running/Ready 1/1, zero restarts.
    Actual imageID matches the manifest's `sha256:78d05416...7587db` pin.
    Live pod args and mounted preset match D-011: `--models-preset
    /config/models.ini --models-max 3 -ngl 99 -c 8192`, `LLAMA_CACHE=/models`,
    four approved Q4_K_M repositories, existing PVC mounted at `/models`.
- Health before/after: HTTP 200, `{"status":"ok"}`, 0.831/0.806 seconds.
    `/v1/models`: HTTP 200, 0.798 seconds; exactly the four approved
    `source=preset` IDs below, PLUS four `source=cache` repository IDs (eight
    entries total). An assertion that discovery contains ONLY four IDs would
    fail; preset-set equality passed. Initially all eight were unloaded.
- Each captured chat response was valid nonempty JSON, exact assistant content
    `42`, matching response model, `finish_reason=stop`, HTTP 200 and positive
    completion usage. Exact prompt: `What is 17 + 25? Reply with only the number.`
    Parameters: `temperature=0`, `max_tokens=32`, `stream=false`.

| Requested Model | HTTP | Completion Tokens | Captured Client Seconds |
|---|---|---|---|
| `qwen2.5-7b-instruct` | 200 | 3 | 0.870104 |
| `qwen2.5-coder-7b-instruct` | 200 | 3 | 0.766674 |
| `llama-3.1-8b-instruct` | 200 | 2 | 0.836498 |
| `phi-4` | 200 | 2 | 0.825445 |

- These are captured WARM requests, not cold-load benchmarks. Initial requests
    completed model loading/generation in logs, but terminal capture was empty
    or incomplete (known T-003); request state and absence of a remaining client
    were checked before warm capture repeats. No 600-second client timeout was
    observed. Llama's saved transport also reports curl exitcode 0; Phi's initial
    transport artifact was empty, so its body alone was not counted as HTTP proof.
    The subsequent Phi response included literal HTTP/1.1 200 headers.
- Normal fourth-model observation, not an administrative eviction test:
    discovery showed Qwen/coder/Llama loaded (three), then coder/Llama/Phi loaded
    (three), Qwen unloaded. Log at `18:24:53.435Z`: `evicting idle LRU
    name=qwen2.5-7b-instruct for a queued request`. No model administration,
    stress, concurrency, persistence deletion or forced outage was performed.
- GPU evidence from the existing pod: before inference, `nvidia-smi` showed
    63/46791 MiB and no compute processes. After Qwen/coder inference: PIDs
    134/220, `/app/llama-server`, 5398 MiB each, total 10862 MiB. At 18:27:17 UTC:
    coder PID 220 (5398 MiB), Llama PID 314 (6190 MiB), Phi PID 401 (10738 MiB),
    total 22394 MiB. Read-only `/proc/{220,314,401}/cmdline` maps exact aliases
    and `--n-gpu-layers 99`; their maps contain `libggml-cuda.so`, `libcuda.so`
    and `libcudart.so`. This supports GPU-backed inference, not just allocation.
    Explicit CUDA initialization/offloaded-layer counts were NOT present in the
    inspected current logs; exact layer counts remain unverified. Structured
    `nvidia-smi --query-compute-apps=pid` returned `Insufficient Permissions`;
    ordinary `nvidia-smi` worked. No privilege change or diagnostic pod was used.
- Scoped exposure/security observation: private ClusterIP:8080, no external IP,
    no `llm` Ingress/NetworkPolicy; expected GPU selector/both taint tolerations,
    GPU request/limit 1, no host network/host port, token automount false and
    token absent. Runtime UID/GID 0, CapEff=0, NoNewPrivs=1, Seccomp=0; root,
    absent seccomp and unauthenticated/unisolated HTTP remain residuals, not
    remediated or accepted by this test. No Secrets were read.
- Reproduce: README direct-inference guide using owned localhost-only
    `kubectl --context=aks-agw-lab -n llm port-forward --address 127.0.0.1
    service/llama-cpp 18080:8080`; health/discovery `curl --noproxy '*' --max-time
    10`; repeat its exact chat JSON for each table ID with `--max-time 600`.
    Runtime diagnostics: `kubectl --context=aks-agw-lab -n llm logs
    pod/llama-cpp-74c6bc49b5-75d9c -c llama-server --since=20m --timestamps`
    and `kubectl --context=aks-agw-lab -n llm exec
    llama-cpp-74c6bc49b5-75d9c -c llama-server -- nvidia-smi`. Read-only live
    ConfigMap, Service, EndpointSlice, node/pod and `/config/models.ini` checks
    established configuration/placement separately from inference.
- Cleanup PASS: owned forward PID 63839 stopped; `lsof -nP -iTCP:18080
    -sTCP:LISTEN` found no listener, and process inspection found no remaining
    matching inference client/forward. Temporary response artifacts were outside
    the repo. No cloud/workload/PVC mutation, installs, build/push, commit/push,
    further delegation or execution-log edit. Existing dirty tree preserved;
    only STATUS and the reusable troubleshooting entry were edited.
- Handoff at test completion: Architect acceptance was pending. The current
    bounded verdict above supersedes that pending state, not the test's limits
    or missing gates. Coordinator owns the agent execution log.

## Fresh GPU Prerequisite Observation (2026-10-27)

- FACT: explicit-context, read-only `kubectl --context=aks-agw-lab` checks show
    GPU node `aks-gpunp-61997117-vmss000015` Ready with `nvidia.com/gpu: 1`
    allocatable. Pod `llama-cpp-74c6bc49b5-75d9c` is Running, Ready 1/1, with
    zero restarts on that node (age 11h at observation).
- This supersedes the older operator-reported GPU absence below. Node/pod
    readiness does not establish current GPU execution or successful inference;
    no health request, model loading, inference or runtime GPU check was performed.
- NEXT at that observation (superseded by independent results above): validate direct router-mode inference for all four
    presets and actual GPU execution under D-011, then seek architectural
    acceptance before implementing any gateway model route. Follow README's
    direct-inference guide; no capacity or deployment changes are needed for
    the prerequisite check. D-015's live gateway outage test remains deferred.

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

## Current D-015 Architectural Acceptance

- DECISION (Architect, 2026-10-23): ACCEPT the deployed CPU-only control plane
    and observed gateway/MCP submilestone as bounded VALIDATED for continued
    trusted, supervised, single-operator use. Phase 8 deployment/reconciliation
    and MCP interoperability are accepted; Phase 9 model integration and Phase 10
    end-to-end inference remain PLANNED. This is not full D-015 outage acceptance.
- Independent basis: coordinator-maintained CPU-only section of
    [docs/agent-execution-log.md](docs/agent-execution-log.md) records actual
    Architect, Developer, Tester and Security Reviewer invocations. Tester:
    full live suite **68 PASS in 26.76s**, gateway offline 3 PASS, focused MCP
    failure/deadline/probe 4 PASS, live gateway 5 PASS in 13.24s, supplemental
    direct MCP 9 PASS. Existing environment only; bytecode/cache writes disabled.
- Accepted observations: official v1.6.0 releases/Established CRDs; current
    generation 1 class, Gateway/listener, route and backend conditions; Ready,
    zero-restart app-pool controller/proxy/MCP; pinned imageIDs listed below;
    ClusterIP-only proxy port 8080, exact /mcp and one static StreamableHTTP
    Stateless/unprefixed upstream. SDK 1.30.0/protocol 2025-11-25: two sessions,
    exactly two argument-free tools, repeated structured calls, no session ID,
    direct MCP matches. Gateway foreign Origin 403/seven unrelated paths 404;
    direct probes/Host/Origin 200/421/403. Foreign inbound Gateway Host is accepted;
    upstream MCP Host validation is NOT a gateway caller-Host boundary.
- Scope adjustment: health was healthy/health_ok/200 throughout. Existing offline
    source failure tests prove MCP independence ONLY, not deployed gateway outage
    behavior. D-015 Gate C's live unavailable-upstream portion is DEFERRED, not
    passed. Later record independent gateway SDK discovery/overview/bounded health
    plus direct MCP probe evidence during an authorized or naturally occurring
    outage; do not disrupt/reconfigure the upstream just to complete this gate.
- Security condition: runtime Security Reviewer conditional GO applies only to
    unchanged trusted supervised use. Human's explicit "Accept reviewed permissions
    and deploy" supersedes historical holds. HIGH controller cluster-wide Secret
    reads/other authority remain ACCEPTED, NOT REMEDIATED; scoped writes do not
    narrow reads. MEDIUM plaintext/unauthenticated access and MCP reflection,
    LOW availability remain. TLS xDS, audience-scoped read-only proxy token/CA,
    proxy Secret-read denial, MCP token absence and admitted hardening verified;
    no rotation/invalid-token rejection/process-level/whole-image certification.
- NEXT: human may use README's localhost gateway forward and SDK checks; stop
    their forward afterward. Reassess before changing trust, permissions, targets
    or exposure. Fresh 2026-10-27 D-011 evidence/verdict above supersedes the older
    GPU-absence report. D-011 historical offload/final-runtime/security gates are
    cleared within bounded ACCEPT; separate exact-release model-route design/
    security proof and authorization remain. Healthy /health alone proves neither GPU availability nor inference.
    D-015 itself did not investigate GPUs.
- This acceptance inspects repository/recorded reports only: no runtime tests,
    agents, cluster/cloud changes, installs, commit or push. Base is already
    committed 8c80d03. Tester-owned 18151/18152 forwards removed; 18000 also free
    at recorded cleanup. Current edits are limited to four acceptance documents;
    coordinator owns the execution log. Historical execution scopes below remain
    history, not current installation prohibitions.

## D-014 MCP Deployment And Acceptance (Historical Execution)

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
    not approved for execution. Gateway remains PLANNED; the later D-015 request
    resumes CPU-only work. D-011 independent router validation still precedes
    model integration, not MCP routing.
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

## D-015 Gateway/MCP (DEPLOYED; Developer Evidence)

- Latest authority: human selected **Accept reviewed permissions and deploy**
    after the independent preinstallation Security Reviewer finding. D-015 records
    acceptance of HIGH cluster-wide Secret reads and reviewed controller authority,
    not remediation or new Azure IAM. Historical installation holds below are
    superseded by that disposition. No additional agents/delegation authorized.
- CREATED: annotated controller values, parameters applied before Gateway, one
    exact `/mcp` route and static StreamableHTTP backend, focused offline/opt-in
    SDK checks. Images resolved from official v1.6.0 indexes and digest pinned.
    First focused tests: 3 PASS; exact controller render confirms app placement,
    ClusterIP, TLS-only xDS, hardening and resources. No MCP/GPU/llama changes.
- Read-only preflight: explicit context aks-agw-lab; Ready untainted app node
    aks-app-42647623-vmss000000 (AMD64), 3860m CPU/12074728Ki allocatable,
    existing requests 1335m/2004Mi. Two 100m/128Mi workloads fit. No gateway CRDs,
    namespace, release or matching RBAC objects present. Existing operator
    `auth can-i '*' '*' --all-namespaces` returned yes; no operator grant added.
    AKS Running/Succeeded, Azure networking, networkPolicy none. No Azure mutation.
- Tool limitation: deferred loader unavailable; explicit-context terminal
    kubectl/Helm used. Helm 4 rejected obsolete `list --all`; corrected to
    `list --all-namespaces`. A guessed chart template path did not exist; actual
    templates inspected instead. Both were local read-only failures.
- DEPLOYED: standard Gateway API v1.6.0 bundle (10 CRDs and official CRD
    safe-upgrade admission policy/binding, all previously absent); agentgateway
    v1.6.0 CRDs (4) and controller Helm releases revision 1. Namespace/controller
    render and all custom resources passed server dry-run. Controller and proxy
    rollouts completed. `lab-internal` parameters were applied BEFORE Gateway.
    Complete local suite before install: 66 PASS, 2 opt-in live tests skipped.
- FACT: controller `agentgateway-657866fcbf-9ctzr` and proxy
    `agentgateway-proxy-79f4976fcb-86d9n` Ready, zero restarts, UID 10101 on
    `aks-app-42647623-vmss000000`. Both requests 100m/128Mi, limits 500m/512Mi;
    nonroot/read-only/drop ALL/no escalation/RuntimeDefault in admitted pod specs.
    No GPU requests/tolerations/host networking/host ports. Controller ClusterIP
    ports 9978/9093/9092; proxy ClusterIP port 8080 only; no external IPs.
- FACT: generation 1 matches observedGeneration throughout: GatewayClass
    Accepted, Gateway Accepted/Programmed, listener Accepted/Programmed/ResolvedRefs,
    HTTPRoute Accepted/ResolvedRefs and backend Accepted. Class controller name is
    agentgateway.dev/agentgateway. One same-namespace exact `/mcp` route and one
    static lab-info.mcp.svc.cluster.local:80/mcp destination; no model/admin route.
- Live image references, both v1.6.0 indexes pinned and observed as imageIDs:
    `cr.agentgateway.dev/controller@sha256:d84259a7e2d87f8f39bae385d4b032d823c0a4450aecb32e0e31e2258449645b`;
    `cr.agentgateway.dev/agentgateway@sha256:9d3e6044ddcdc0878b1787f77bd401252b95e22684203fb5e874c4c42d2ed90c`.
    Exact chart/bundle hashes, reproduction commands and rollback are in README.
- FACT: controller's native API token retained; HTTPS xDS to controller FQDN:9978
    uses self-managed certificate Secret `kgateway-xds-cert` and proxy read-only CA plus projected
    token (audience agentgateway, requested 43200s). Proxy generic automount false;
    `auth can-i get secrets --all-namespaces --as=system:serviceaccount:agentgateway-system:agentgateway-proxy`
    returned no (expected exit 1). Reviewed controller read authority is unchanged;
    scoped deployer RoleBinding only in agentgateway-system. No Azure/operator
    grant added. Only token/Secret reference metadata inspected, never values.
- FACT: `GATEWAY_TEST_URL=http://127.0.0.1:18000/mcp .venv/bin/python -m pytest -q -s tests/test_gateway.py`
    5 PASS in 13.31s. Python 3.12.15/MCP 1.30.0; official SDK negotiated
    2025-11-25, initialized twice, listed exactly get_lab_overview/get_model_health
    with no arguments, called both twice per initialization, structured results,
    no session ID. Foreign Origin 403; /, /health, /healthz, /readyz, /mcp/,
    /v1/models, /metrics all 404. No allowlist or Origin rewriting changed.
- FACT: live health returned healthy/health_ok/200, contrary to expected upstream
    absence; this does NOT prove inference or GPU availability. No GPU/Spot/pool
    investigation, llama.cpp restart/PVC mutation or manufactured live failure.
    Existing deterministic local tests cover MCP unavailable-upstream independence;
    gateway-specific unavailable-upstream evidence is not established.
- FACT: direct MCP pod lab-info-6856dddf7-zdrrn, exact image digest, zero restarts,
    hardening/allowlists/fixed health target unchanged. In-pod loopback probes 200,
    foreign Host 421/Origin 403, API token absent. First one-off assertion expected
    Origin 400 and FAILED; corrected expected 403 and same check passed. No runtime
    fix was needed. Bounded proxy logs contain request/path/tool metadata, not
    observed bodies/prompts/credentials; this is not comprehensive certification.
- Final complete suite with live gateway checks:
    `GATEWAY_TEST_URL=http://127.0.0.1:18000/mcp .venv/bin/python -m pytest -q`:
    **68 PASS in 27.22s**. Prior default suite 66 PASS/2 opt-in skips. No dependency
    installation, public Python feed, commit/push or additional delegation.
- Files modified by this execution: k8s/gateway/controller-values.yaml,
    k8s/gateway/parameters.yaml, k8s/gateway/gateway.yaml, tests/test_gateway.py,
    README.md, STATUS.md, docs/architecture.md, docs/troubleshooting.md.
    Inspected constitution, repository/developer instructions, D-015, MCP manifest,
    existing tests/pyproject, exact v1.6.0 chart values/templates/CRD schemas and
    generated proxy helper. Existing five dirty documentation changes preserved;
    coordinator-owned docs/agent-execution-log.md was not edited. An unrelated
    infra/registry.bicep change appeared during execution and was left untouched.
- HISTORICAL NEXT (completed except deferred live outage test): independent Tester (including gateway failure semantics when naturally
    available, not production disruption), runtime Security Reviewer and Architect
    acceptance. Continue trusted supervised use only. Independent D-011 router
    acceptance still gates any model route; README direct-inference guide preserved.
- Cleanup COMPLETE: execution-owned localhost forward terminated, port 18000
    confirmed free; no disposable container was created. Deployed private gateway
    remains running. Final condition/placement/Service snapshot unchanged, zero
    restarts; `git diff --check` and editor diagnostics for all four source files
    passed. Only Secret names/types were listed to confirm the self-managed cert;
    no release Secret payload, token, kubeconfig or certificate key was output.
- This is DEPLOYED, not independently VALIDATED. Tester/runtime Security
    Reviewer/Architect acceptance remain coordinator-owned follow-up gates.

## Current phase

Phase 8: agentgateway v1.6.0 deployment/control plane and observed MCP path are
bounded VALIDATED on the existing CPU `app` pool; live gateway outage validation
is explicitly deferred above. D-011 has final bounded ACCEPT, including historical
explicit offload and final-runtime/security prerequisites. Separate model-route
design/security proof and authorization remain. Phases
9/10 stay PLANNED; no llama.cpp route is authorized by this review.

The latest human request authorizes gateway implementation, superseding the
historical gateway pause, not the exposure/security or infrastructure limits.
The earlier Architect assignment was documentation-only; subsequent Developer
deployment/evidence above supersedes its planning-only state.
Fresh independent evidence (2026-10-27) supersedes the 2026-10-23 GPU-absence
report: Ready GPU node, allocatable GPU and successful direct inference observed.
This review made no new runtime request; the snapshot is not a Spot availability
guarantee. Do not change GPU SKU, capacity or node counts.
CPU-only gateway/MCP work does not require a GPU; unavailable upstream
health must remain a normal bounded tool result, not a gateway-readiness gate.

The human previously authorized building the Python lab-information MCP
server. Architect reviewed the bounded local-first
design (D-012). Architect accepts the two-tool teaching LOCAL source milestone
against its amendment and recorded independent Tester/Security evidence.
This supersedes the historical three-tool/54-test acceptance for current source,
not its stronger response-protection guarantees. The approved Python feed restriction remains
in force. D-014 container/cluster hosting is separately VALIDATED and architecturally
accepted only for the trusted supervised single-operator lab. Public exposure is not authorized.

### Historical Architect Gateway Handoff (D-015; PLANNED at review time)

- Preserved coordinator-owned README addition: direct llama.cpp health, discovery,
    all-four-preset inference and CUDA-offload checks when GPU capacity returns.
    Manual checks do not replace independent D-011 acceptance.
- Official Helm/static-MCP/API/overlay/TLS sources reviewed; actual v1.6.0
    controller values and both chart renders inspected offline. MCP target
    StreamableHTTP/stateless/unprefixed fields and proxy overlays exist in the
    exact CRD chart. Corrected controller `nodeSelector.workload=app` renders;
    `controller.nodeSelector` is silently ignored and must not be used.
- Implementation contract and recommended artifacts/values are in
    [D-015](docs/decisions.md#d-015-cpu-only-gateway-and-mcp-first-2026-10-23-planned).
    Annotate all future YAML/shell/tests with workload contracts, ownership,
    trust limits and failure behavior, not language-syntax lessons.
- HISTORICAL DEPLOYMENT HOLD (cleared by later human disposition above): scoped write RoleBinding does not remove controller-wide
    Secret reads, TokenReview and cluster-scoped management/status authority.
    Independent security assessment plus explicit human RBAC disposition is
    required before install. Preserve authenticated TLS xDS and required proxy
    token projection; MCP stays token-free. No silent privilege expansion.
- Next: Developer prepares bounded annotated CPU-only artifacts and renders;
    permission/security gate before mutation; Tester independently exercises real
    SDK through gateway including unavailable upstream; Security Reviewer reviews
    actual runtime; Architect accepts only that evidenced MCP path. This assignment
    invokes no additional agents; the coordinator owns execution logging.
- Checks in this Architect assignment: `git status --short` initially only README
    dirty; HEAD/origin main `8c80d03`; recent history inspected. `helm show values`
    and offline controller/CRD `helm template` succeeded. First status edit passed
    scoped `git diff --check`. `rg` was unavailable; existing file/read tools used.
    Source 63 PASS is prior evidence, not rerun here. No Kubernetes/cloud operation,
    install/deploy, context switch, image build, commit or push. Changed only STATUS,
    architecture and decisions; README and execution log left untouched.

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
| 7 | Direct llama.cpp inference validation | VALIDATED (2026-10-27 final bounded D-011 ACCEPT); historical explicit offload and final hardened runtime accepted; single-model 6/6 historical |
| 8 | agentgateway deployment | VALIDATED (bounded CPU-only control plane + observed MCP path; live outage test deferred) |
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
| AKS `aks-agw-lab` (rg `rg-aks-agw-lab`, southeastasia, v1.36.4) | DEPLOYED | CPU gateway/MCP accepted; independent 2026-10-27 Ready GPU/inference snapshot, not future availability |
| GPU node `gpunp` (Spot) | VALIDATED at independent 2026-10-27 observation | Ready, allocatable GPU 1 and inference worker allocations; Spot availability remains best effort |
| NVIDIA device plugin (`k8s/gpu/nvidia-device-plugin.yaml`) | DEPLOYED | Privileged (T-007); GPU advertisement/allocation observed 2026-10-27, no new plugin security certification |
| GPU smoke test (`k8s/gpu/gpu-smoke-test.yaml`) | VALIDATED (historical independent GPU checks) | Tester confirmed GPU allocation, execution and scheduling isolation; see Phase 4 evidence. No fresh cluster check this session. |
| llama.cpp (`k8s/llm/llama-cpp.yaml`) | VALIDATED (2026-10-27 final bounded D-011 ACCEPT) | Four presets, historical explicit offload, final hardened runtime and max-three behavior accepted; gateway path NOT implemented/validated |
| agentgateway | VALIDATED (bounded D-015) | CPU control plane + observed MCP path accepted; live upstream-outage gateway test deferred; no model route or network isolation |
| Python lab-information MCP server | VALIDATED (D-014 trusted supervised single-operator lab only) | D-014 acceptance retained; D-015 independently confirms unchanged direct MCP and observed gateway interoperability, not live outage behavior or isolation |

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

MCP dependency/packaging/deployment prerequisites were resolved within bounded
D-014 acceptance; D-015 accepts only observed CPU/gateway/MCP behavior. Neither
is whole-image or production certification. D-011's explicit historical CUDA/
offload and final-runtime/security prerequisites are cleared within bounded
ACCEPT. Remaining model-route blockers are exact v1.6.0 fixed-backend/narrow-path
design/security proof and separate implementation authorization; independent
gateway validation/acceptance follows implementation. Live gateway outage
evidence remains deferred. Infrastructure risks:
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

- Current base `8c80d03` (HEAD/main and origin/main at inspection) already commits
    the deployed two-tool MCP MVP. Earlier no-commit/no-push execution statements
    are historical, not a claim that this base is uncommitted. D-015 working-tree
    changes remain uncommitted; no commit/push is authorized or performed now.
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

1. Phase 8's CPU deployment/control plane and observed MCP path are accepted;
    defer independent live gateway outage evidence as specified at the top.
    Phases 9-10 remain PLANNED: D-011 prerequisites have final bounded clearance;
    exact v1.6.0 fixed-backend/narrow-inference-path design/security proof and
    separate authorization must precede bounded Developer route work.
    Independent gateway inference validation/acceptance follows implementation.
2. Phase 11-12: Security Reviewer pass (privileged plugin, public API server, Spot, unauthenticated llama-server, no NetworkPolicy); teardown and rebuild test; update `preflight.sh` for Spot; test Spot eviction recovery.

## Next action

Use README's localhost gateway forward/SDK guide for continued supervised use;
stop the forward afterward. No local endpoint is always running. Preserve the
accepted trust boundary and defer live outage testing without disruptive changes.
Coordinator next records final D-011 bounded acceptance and owns publication:
stage explicit reviewed paths, exclude private/raw diagnostics and check staged
content before eventual commit/push. No staging/commit/push occurred here.
Next technical work requires separately authorized exact v1.6.0 fixed-backend/
narrow-inference-path design/security proof, then separately authorized Developer
route work and independent gateway validation. No route or capacity change is
authorized here; bounded prerequisite clearance is not Phase 9/10 completion.

### Historical Teaching-Revision Handoff (Superseded By D-014/D-015)

The following captures that earlier documentation-only execution, not current
packaging/deployment gates or an active gateway installation hold:

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
