# Agent execution log

Every delegation to a custom agent (`.github/copilot-instructions.md`, "Agent execution transparency"). Entries 1-3 were written after the fact on 2026-10-20 because the log was not created when those agents ran; they are reconstructed from each agent's final report. Nothing is listed here that was not actually invoked.

## D-011 Final Gate Acceptance (2026-10-27)

### Agent execution
Agent: architect
Date: 2026-10-27
Why selected: required final acceptance after authorized hardening, independent Tester validation and independent Security Reviewer GO.
Task: evaluate resolved explicit-offload/runtime/security gates, preserve provenance limits and reconcile the publication handoff without authorizing model routing.
Files inspected: governing/architect instructions, STATUS.md, README.md, docs/architecture.md, docs/decisions.md, docs/troubleshooting.md, coordinator execution records, llama.cpp manifest and relevant tests; Git status/history.
Files modified: STATUS.md, docs/architecture.md, docs/decisions.md and README.md only.
Commands/tests: scoped documentation diff checks, consistency/safety scans and final editor diagnostics PASS. No runtime tests rerun; acceptance uses recorded independent evidence.
Result: bounded ACCEPT; D-011 model prerequisite cleared. Historical alias/port-correlated CUDA initialization and 29/29,29/29,33/33,41/41 offload plus ReplicaSet/events provenance satisfy the explicit diagnostic gate with stated limits, not fresh final-pod startup or tamper-proof evidence. Final four HTTP 200/exact 42/positive usage, health/discovery/LRU, non-root/RuntimeDefault runtime, nine gates PASS and 66 tests PASS/2 opt-in skips support acceptance. Root/no-seccomp remediation accepted; Security Reviewer GO and explicit human residual disposition clear the bounded security gate.
Limits/handoff: HIGH router access/admin abuse and controller Secret reads remain accepted, not fixed; logging confidentiality/retention unverified. Trusted supervised single operator, trusted workloads/local users, synthetic/public data only; expires before sharing, untrusted users/workloads, wider exposure or target change. No new write/download/full-hash/recovery/throughput/wider-access claim. Phases 9/10 PLANNED; no model route authorized or implemented, D-015 live outage remains deferred. Future separately authorized exact-release route design must prove fixed upstream, narrow inference paths/no admin catch-all and independent gateway validation.
Execution boundary: documentation/recorded evidence only, dirty work preserved; no runtime/cloud/workload/PVC/network mutation, nested delegation, installs, builds, stage/commit/push or execution-log edit by delegate.
Artifacts: final current acceptance in STATUS.md, architecture, decisions and README; coordinator owns execution record and reviewed publication.

## D-011 Gate Resolution Implementation And Validation (2026-10-27)

### Agent execution
Agent: developer
Date: 2026-10-27
Why selected: implement bounded diagnostic and hardening after explicit human approval of interruption, narrow volume permissions and lab access risks.
Task: deploy compatible non-root/RuntimeDefault hardening, collect explicit per-model CUDA/offload proof with temporary verbosity 4, restore normal logging and preserve weights.
Files inspected: governing/developer instructions, STATUS.md, README.md, architecture/decisions/troubleshooting, llama.cpp manifest, existing tests, relevant skills and pinned sources.
Files modified: k8s/llm/llama-cpp.yaml, STATUS.md, README.md, docs/architecture.md, docs/decisions.md, docs/troubleshooting.md.
Commands/tests: manifest/server dry-runs, three Recreate rollouts, sequential synthetic direct inference, runtime/worker/cache inventory/GPU checks; focused drift test 1 PASS, git diff --check PASS.
Result: DEPLOYED with Developer evidence only. Final llama-cpp-5f676cf74f-vzjtv Ready/zero restarts, same pinned build 11749/1d88cb05f; UID/GID 10001, RuntimeDefault/Seccomp 2, all capabilities zero, NoNewPrivs 1, token absent. Supported fsGroup 10001 handled cache permissions without root initializer/manual repair/world-write. Inventories matched paths/sizes/symlinks, not full-content hashes. Diagnostic actual initialization plus offloaded layers: Qwen 29/29, coder 29/29, Llama 33/33, Phi 41/41; each diagnostic and final request HTTP 200/exact 42/positive usage. Normal verbosity 3 restored. Readiness watches 20-31 seconds per rollout, not measured endpoint downtime.
Cleanup/boundary: owned clients/forward stopped; private restricted diagnostic captures retained for independent review. No model route, capacity change, nested delegation, commit or push. Existing dirty tree preserved; coordinator execution log untouched by delegate.
Artifacts: reproducible manifest hardening, explicit human decisions/risk expiry and diagnostic evidence in documentation. Independent validation/security/architecture pending at handoff.

### Agent execution
Agent: tester
Date: 2026-10-27
Why selected: independently validate deployed hardening and diagnostic evidence rather than rely on Developer reports.
Task: verify final runtime/cache/configuration, all-four direct inference and retained historical CUDA/offload evidence without workload changes.
Files inspected: governing/tester instructions, STATUS.md, architecture/decisions, README.md, llama.cpp manifest, tests and private diagnostic evidence; inspection inventory recorded in STATUS.md.
Files modified: STATUS.md and docs/troubleshooting.md only.
Commands/tests: explicit-context metadata/runtime/cache checks, owned localhost-forwarded health/discovery/all-four arithmetic requests, historical alias/repository/port/CUDA/count correlation and ReplicaSet/events provenance; 66 tests PASS, 2 live-gateway opt-ins SKIPPED; scoped diff/diagnostics PASS.
Result: nine scoped validation gates PASS. Final router/workers UID/GID 10001/Seccomp 2/all caps zero/NoNewPrivs 1/token absent, Ready/zero restarts. Four HTTP 200/exact 42 results with usage 3/3/2/2; ordinary max-three/LRU preserved. Retained diagnostic ports 40649/33453/36313/41137 correlate Qwen/coder/Llama/Phi initialization and 29/29,29/29,33/33,41/41 offload. Diagnostic pod deleted; historical logs are not fresh final-pod startup logs. Cache inventory unchanged and permission checks pass; actual new write/download/full hashes/recovery untested.
Cleanup/boundary: owned forward closed, clients completed, restricted private captures retained. No workload changes, installs, nested delegation, commit/push or execution-log edits.
Artifacts: independent post-hardening results and diagnostic provenance caveats in STATUS.md/troubleshooting. Architectural acceptance remains pending; no model route authorized.

### Agent execution
Agent: security-reviewer
Date: 2026-10-27
Why selected: independently assess admitted hardening, explicit human risk disposition, logging and public-repository safety before acceptance/publication.
Task: review final runtime and all pending publication inputs without modifying workloads or accepting risks on behalf of the operator.
Files inspected: governing/security instructions, STATUS.md, README.md, all four docs, registry/llama/gateway inputs, tests, pyproject.toml and ignore files; targeted restricted diagnostic/Tester artifacts.
Files modified: STATUS.md only.
Commands/tests: explicit-context read-only get/exec/logs, runtime/cache checks, historical evidence checks, Git/Node safety scans of 12 pending tracked/untracked files, diff/STATUS diagnostics PASS. No Python suite/inference rerun; observed Tester 66 PASS/2 skips retained.
Result: GO for continued bounded trusted-router use; security prerequisite for separately authorized future private-route design cleared. Root/no-seccomp MEDIUM remediated in observed router/resident workers. Router unauthenticated/unisolated administration HIGH and controller Secret-read HIGH remain explicitly accepted, not fixed. Normal logging confidentiality MEDIUM/collector retention unverified remain; no selected credential/body markers observed. No new scoped blocker, no wider access/route support or implementation authorization.
Public safety: all 12 pending files scanned with no credential/private-content finding or raw diagnostic artifact; registry change newline-only. Index empty during review, so coordinator must stage explicit reviewed paths and rerun staged safety checks before publication.
Cleanup/boundary: no workload changes, installs, forwards, nested delegation, stage/commit/push or execution-log edit. Historical diagnostic provenance, actual write/download/full hashes/recovery remain bounded/unverified; private captures preserved for Architect.
Artifacts: independent runtime security disposition in STATUS.md. Architect acceptance next.

## D-011 Gate Resolution Reviews (2026-10-27)

### Agent execution
Agent: tester
Date: 2026-10-27
Why selected: independently investigate missing explicit CUDA initialization and layer-offload evidence before implementation changes.
Task: inspect retained logs and pinned-release logging behavior without restarting or reconfiguring workloads.
Files inspected: tester profile, constitution, STATUS.md, architecture, decisions, README.md, llama.cpp manifest, troubleshooting; live args/presets/environment and pinned upstream logging/router/CUDA source.
Files modified: STATUS.md and docs/troubleshooting.md.
Commands/tests: explicit-context existing-pod metadata/log reads, full retained log inspection, pinned executable version and upstream source inspection; focused git diff --check PASS and documentation diagnostics clean.
Result: explicit offload gate remains unsatisfied. Earlier tested pod no longer exists; replacement llama-cpp-74c6bc49b5-6pvtb retained 17 log lines without CUDA/offload matches. Build 11749/commit 1d88cb05f emits required backend INFO at verbosity 4 while deployed default is 3; router child stderr forwarding is active. Minimal proposed diagnostic: separately authorized Recreate with temporary verbosity 4, then bounded sequential synthetic inference for each preset and actual initialization/layer-count capture.
Cleanup/boundary: no inference clients or forwards created; no workload changes, installs, nested delegation, commit or push. Existing dirty tree preserved; coordinator execution log untouched by delegate.
Artifacts: logging cause, authoritative source references and smallest diagnostic handoff in STATUS.md and troubleshooting.

### Agent execution
Agent: security-reviewer
Date: 2026-10-27
Why selected: independently assess router runtime/exposure risks and diagnostic confidentiality before resolving model-routing gates.
Task: identify minimum hardening, human risk disposition and safe offload-diagnostic contract; review pending changes for public-repository safety.
Files inspected: governing/profile documents, STATUS.md, README.md, architecture/decisions, llama manifest, three gateway inputs/tests, scoped pending diffs, pinned source and cached-image metadata.
Files modified: STATUS.md only.
Commands/tests: explicit-context read-only Kubernetes observations, pinned-source/cached-image inspection, Git diff/history and credential-pattern scan; scoped documentation checks PASS. No credential candidates in 1305 added lines plus four untracked inputs; not full-history certification.
Result: NO-GO for new model routing; conditional GO for separately authorized synthetic diagnostic. HIGH unauthenticated/unisolated model administration requires controls or explicit bounded human risk acceptance. MEDIUM root/no seccomp requires compatibility-tested hardening; UID-only change breaks root-owned 0700 cache access. MEDIUM verbosity-4 confidentiality risk includes metadata, configured API-key suffix and warning-path generated output; level 5 body/token logging must remain disabled.
Handoff: authorize Recreate and any necessary PVC permission changes; validate non-root/device/cache/worker access and RuntimeDefault without silent fallback. Diagnostic uses public arithmetic only, reviewed private startup excerpts, restores verbosity 3. Routing separately requires supported fixed upstream/narrow inference paths, no admin/catch-all and independent validation. Human must explicitly dispose new-route plaintext/unrestricted-reachability/admin-abuse risks or approve a separate controls design. No risk accepted by reviewer.
Execution boundary: no workload changes, inference/forwards, installs, nested delegation, commit or push. Existing dirty tree preserved; coordinator execution log untouched by delegate.

## D-011 Bounded Architectural Acceptance (2026-10-27)

### Agent execution
Agent: architect
Date: 2026-10-27
Why selected: required architectural acceptance after independent direct-router validation; human requested the next step.
Task: assess recorded D-011 evidence, preserve unverified gates and reconcile current documentation without model-route implementation.
Files inspected: repository instructions, .github/agents/architect.agent.md, PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md, docs/decisions.md, README.md, docs/agent-execution-log.md, k8s/llm/llama-cpp.yaml.
Files modified: STATUS.md, docs/architecture.md, docs/decisions.md and README.md only. Coordinator added this execution record separately.
Commands/tests: Git status/history; git diff --check -- STATUS.md docs/architecture.md docs/decisions.md README.md PASS after both edits; documentation diagnostics clean. No runtime tests rerun.
Result: bounded ACCEPT of demonstrated four-preset direct inference, normal max-three/LRU behavior and correlated GPU-backed execution for unchanged trusted supervised lab use. Explicit CUDA initialization/offloaded-layer evidence remains unsatisfied; exact counts/full offload unverified. Full D-011 model-routing prerequisite clearance NOT ACCEPTED.
Security/limits: root runtime, absent seccomp and unauthenticated/unisolated HTTP remain unresolved. No new security acceptance granted; separate review/disposition blocks model-route work, not recording unchanged trusted-lab behavior. Phases 9/10 remain PLANNED; D-015 remains CPU/MCP-only with live gateway outage validation deferred.
Artifacts: bounded verdict and remaining gates in current status, architecture, decisions and README. Next: resolve offload evidence and applicable supported-release design/security gates before separately authorized Developer route work.
Execution boundary: documentation/recorded evidence only; no nested delegation, runtime/cloud requests, infrastructure/workload/PVC mutation, installs, builds, deployment, commit or push. Existing dirty changes preserved; coordinator execution log untouched by delegate.

## Independent D-011 Router Validation (2026-10-27)

### Agent execution
Agent: tester
Date: 2026-10-27
Why selected: human requested independent testing after current GPU/workload readiness was observed; D-011 requires independent direct inference evidence before model routing.
Task: validate the existing router's four approved presets, GPU execution and normal max-three loading behavior without deployment or capacity changes.
Files inspected: .github/agents/tester.agent.md, PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md, docs/decisions.md, README.md, k8s/llm/llama-cpp.yaml, docs/troubleshooting.md.
Files modified: STATUS.md and docs/troubleshooting.md only. Coordinator added this execution record separately.
Commands/tests: explicit-context node/pod/configuration/Service/EndpointSlice reads; owned localhost-only port-forward on 18080; curl health/discovery and bounded /v1/chat/completions requests for each preset; existing-pod nvidia-smi, bounded logs and read-only worker /proc inspection. Scoped git diff --check PASS.
Result: independent direct-router behavior PASS. All four presets returned HTTP 200 and exact answer 42 with positive completion tokens (Qwen/coder 3 each, Llama/Phi 2 each). Captured warm request times were 0.870104/0.766674/0.836498/0.825445 seconds respectively, not cold-load benchmarks. Health before/after returned 200/status ok. Discovery contained four approved preset IDs plus four cache IDs; preset equality passed, not total-list equality. Normal fourth-model loading logged idle-LRU Qwen eviction and retained three loaded presets. GPU tables showed llama-server compute workers; final coder/Llama/Phi allocations were 5398/6190/10738 MiB, correlated to aliases and mapped CUDA libraries.
Limits: exact CUDA offloaded-layer counts absent from inspected logs and unverified. Structured NVIDIA PID query lacked permission; ordinary tables and read-only /proc worked without escalation. Terminal capture failures required state checks and warm repeats; no 600-second timeout observed. Root execution, absent runtime seccomp and unauthenticated/unisolated HTTP remain residuals, not accepted or remediated. No architectural acceptance, gateway inference, model tool calling or agent-loop claim; Phases 9/10 remain PLANNED.
Cleanup: owned forward PID 63839 stopped and port 18080 verified free; no remaining matching client/forward. No workload/capacity/PVC changes, installs, build/push, commit/push or nested delegation. Existing dirty tree preserved.
Artifacts: fresh independent evidence in STATUS.md; reusable discovery/GPU diagnostic caveats in docs/troubleshooting.md. Next: Architect acceptance before any gateway model route.

## CPU-only gateway implementation (2026-10-23)

### Agent execution
Agent: architect
Date: 2026-10-23
Why selected: mandatory design and phase sequencing for resumed gateway implementation with GPU inference unavailable.
Task: establish an official-supported, CPU-only internal gateway/MCP scope without weakening D-014 or bypassing independent D-011 inference acceptance.
Files inspected: governing repository documents, architect profile, STATUS.md, docs/architecture.md and relevant decisions; official agentgateway installation/API/customization documentation and exact v1.6.0 chart values/rendered resources.
Files modified: docs/decisions.md, docs/architecture.md, STATUS.md. Coordinator's README inference guide preserved.
Commands/tests: helm show values and corrected offline helm template of v1.6.0; scoped git diff --check and documentation diagnostics PASS. No cluster mutations or deployment.
Result: supported CPU-only path documented in D-015, with model routing deferred. Deployment BLOCKED pending independent security review and explicit human disposition of the controller's cluster-wide Secret-read RBAC. Namespace-scoped writes/discovery selectors do not remove that authority. All runtime acceptance gates remain pending.
Artifacts: D-015 bounded implementation/credential/acceptance contract and refreshed handoff.

### Agent execution
Agent: security-reviewer
Date: 2026-10-23
Why selected: independent review of the new controller credential/RBAC boundary before installation.
Task: inspect exact v1.6.0 chart authority and supported narrowing without changing the cluster or reading Secret values.
Files inspected: PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md, docs/decisions.md, security-reviewer profile, k8s/mcp/lab-info.yaml, main.py, README.md; official chart/source and xDS templates.
Files modified: none.
Commands/tests: Git status/history/HEAD; exact helm show values and offline controller/CRD helm template with explicit kube-context; public-source curl reads. Chart/source checks succeeded. No cluster operations, Secret reads, tests, builds or deployment.
Result: conditional GO for offline implementation; installation initially NO-GO pending explicit human disposition. HIGH: cluster-wide Secret-content reads and other control-plane authority; no supported chart switch removes these reads. MEDIUM: unauthenticated plaintext application traffic remains limited to trusted supervised use. Verified projected proxy token design (audience agentgateway, requested 43200-second lifetime), not live behavior. Runtime and concrete implementation review remain required.
Human disposition: the operator subsequently selected "Accept reviewed permissions and deploy" in the explicit permission question. This accepts the reviewed controller RBAC for this lab only, not wider exposure or a finding resolution. D-015 records the authorization.
Artifacts: preinstallation permission assessment and recorded human acceptance; no runtime security certification.

### Agent execution
Agent: developer
Date: 2026-10-23
Why selected: mandatory implementation/deployment after D-015 design and explicit human RBAC acceptance.
Task: create annotated, exact-release configuration and tests; deploy only the internal CPU-only gateway/MCP path and preserve direct MCP operation.
Files inspected: repository/developer governance, constitution, D-015, STATUS.md, architecture, existing MCP manifest/tests and exact v1.6.0 chart/CRD/helper sources.
Files modified: k8s/gateway/controller-values.yaml, k8s/gateway/parameters.yaml, k8s/gateway/gateway.yaml, tests/test_gateway.py, README.md, STATUS.md, docs/architecture.md, docs/troubleshooting.md. Coordinator-owned execution log untouched by agent.
Commands/tests: offline Helm renders, server dry-runs, apply/install, rollouts/current-generation conditions, explicit-context read-only runtime inspection and official SDK localhost-forwarded calls. GATEWAY_TEST_URL=http://127.0.0.1:18000/mcp .venv/bin/python -m pytest -q: 68 PASS in 27.22s. Editor diagnostics and git diff --check PASS. Corrected read-only command mistakes and Origin-status expectation documented in troubleshooting.
Result: DEPLOYED, not independently VALIDATED. Controller/CRDs/Gateway API v1.6.0; controller/proxy Ready with zero restarts on the app node; ClusterIP-only exact /mcp route. SDK 2025-11-25 discovered the exact two argument-free tools, repeated structured calls without session IDs, foreign Origin 403 and seven unrelated paths 404. Direct MCP probes and Host/Origin rejection unchanged. Health healthy/health_ok/200 observed; unavailable-upstream live gateway behavior not observed and no inference/GPU availability inferred.
Security/cleanup: retained accepted HIGH controller Secret-read authority, authenticated TLS xDS and proxy audience-scoped 43200-second projected token with read-only CA/token mounts; no generic proxy token or MCP credentials. Temporary forward removed, port 18000 free. No Azure/GPU/PVC/network changes, commit or push.
Artifacts: annotated gateway configuration/tests and README reading/deployment/rollback guide; STATUS handoff. Independent Tester, runtime security review and Architect acceptance pending.

### Agent execution
Agent: tester
Date: 2026-10-23
Why selected: independent behavioral and runtime validation of the newly deployed gateway/MCP path.
Task: verify source contracts, real SDK discovery/repeated calls, routing boundaries, direct MCP preservation and actual deployment metadata without workload changes.
Files inspected: governing/tester instructions, PROJECT_CONSTITUTION.md, STATUS.md, architecture/decisions, README.md, all three gateway YAML inputs, tests/test_gateway.py, tests/test_lab_mcp.py, MCP manifest, main.py, pyproject.toml and curated configuration.
Files modified: none.
Commands/tests: explicit-context Kubernetes/Helm metadata; owned localhost forwards on 18151/18152; existing .venv with bytecode/cache writes disabled. Gateway offline 3 PASS; existing failure/deadline/probe cases 4 PASS; live gateway 5 PASS in 13.24s; full live suite 68 PASS in 26.76s; supplemental direct MCP cases 9 PASS. Corrected one malformed metadata query; interrupted foreground attempts did not replace the completed checks.
Result: independent PASS for observed CPU-only gateway/MCP behavior. Current generation 1 GatewayClass/Gateway/listener/route/backend conditions accepted/programmed/resolved; v1.6.0 CRDs/releases; exact pinned imageIDs, Ready app-pool pods and ClusterIP-only exposure confirmed. SDK 2025-11-25 lists exact two argument-free tools, repeated structured calls with no session IDs and matching curated overview. Health healthy/health_ok/200 throughout, not inference/GPU proof. Gateway foreign Origin 403 and seven unrelated paths 404; direct probes/Host/Origin 200/421/403. Gateway accepts foreign inbound Host: MCP's upstream authority check is not a gateway caller-Host boundary.
Limits/cleanup: live upstream outage neither observed nor manufactured; offline failure tests do not prove live gateway outage behavior. No GPU/inference/isolation/authentication certification. Owned forwards exited, no listeners on 18151/18152; 18000 also free. No installs, Secret-value reads, workload mutation, commit or push.
Artifacts: independent behavior/runtime evidence for Architect acceptance; no files created.

### Agent execution
Agent: security-reviewer
Date: 2026-10-23
Why selected: independent review of admitted gateway permissions, credentials, hardening and application exposure.
Task: compare actual live deployment with D-015's accepted authority and trusted-lab boundary, without runtime requests or mutations.
Files inspected: constitution, STATUS.md, README.md, architecture/decisions, repository/security-reviewer instructions, three gateway YAML inputs, MCP manifest, main.py and tests/test_gateway.py.
Files modified: none.
Commands/tests: explicit-context scoped Kubernetes objects/RBAC/bindings/pod specs/imageIDs/conditions/Services/bootstrap ConfigMap reads; proxy auth-can-i Secret-read denial (expected exit 1); bounded existing proxy logs (35 lines); Git/source/official TLS documentation reads. No tests, exec, forwards, runtime curl, Secret-object reads or Helm storage reads. Interrupted/interleaved reads discarded; CRD-version inventory incomplete in this review (separately completed by Tester).
Result: conditional GO for continued trusted, supervised single-operator D-015 use; no new significant finding. Accepted HIGH cluster-wide controller Secret reads/other authority remain, with namespace-scoped provisioner writes. MEDIUM unauthenticated plaintext application access remains; inherited MCP reflection MEDIUM and availability LOW not remediated. Actual proxy generic automount false, audience-agentgateway 43200-second read-only projection/CA and TLS xDS configuration confirmed; proxy Secret-read authorization denied. MCP stays token-free. Admitted non-root/read-only/drop-ALL/no-escalation/seccomp, app placement, immutable images and internal-only Services verified. Bounded logs show request/tool metadata, no observed bodies/prompts/credentials.
Limits: configuration inspection does not prove token/certificate rotation, invalid-token xDS rejection or process-level hardening; no whole-image, GPU/inference, live outage, customer/shared or production readiness claim. No further approval needed for unchanged accepted scope; expanded trust, targets, permissions or exposure needs renewed review/human decision.
Artifacts: runtime security disposition for bounded architectural acceptance; no files created.

### Agent execution
Agent: architect
Date: 2026-10-23
Why selected: mandatory phase acceptance against independent behavior and runtime security evidence.
Task: evaluate D-015's bounded gateway/MCP milestone, preserve unverified gates and reconcile the durable handoff.
Files inspected: governing documents/profile, STATUS.md, architecture/decisions, README.md, coordinator execution log, main.py, all three gateway YAML inputs and tests/test_gateway.py.
Files modified: STATUS.md, docs/architecture.md, docs/decisions.md, README.md only. Source/tests/manifests and coordinator log unchanged by the agent.
Commands/tests: Git status/history; scoped git diff --check PASS twice; documentation diagnostics PASS. No tests rerun or cluster operations; acceptance uses recorded independent Tester and Security Reviewer evidence.
Result: ACCEPT Phase 8 deployment/control plane plus observed CPU-only gateway/MCP interoperability as bounded VALIDATED for unchanged trusted, supervised single-operator use. Workload/contract annotations satisfy the requirement. Accepted HIGH controller Secret-read risk remains, not remediated. Live gateway outage independence is deferred, not passed; existing offline tests prove only MCP independence. Current GPU availability/inference are unvalidated and Phases 9/10 remain PLANNED pending independent D-011 acceptance and model routing.
Artifacts: D-015 final architectural acceptance, current phase/handoff, corrected operator-reported GPU status and supervised gateway guide. No new agents, commit or push.

## MCP Kubernetes deployment prerequisites (2026-10-23)

### Agent execution
Agent: architect
Date: 2026-10-23
Why selected: mandatory milestone acceptance against independent deployed behavior and security evidence.
Task: assess D-014 contract, accept only the evidenced trusted-lab MCP milestone and reconcile current handoff wording.
Files inspected: .github/agents/architect.agent.md, PROJECT_CONSTITUTION.md, STATUS.md, docs/decisions.md, docs/architecture.md, README.md, docs/agent-execution-log.md, k8s/mcp/lab-info.yaml, infra/registry.bicep, Dockerfile.
Files modified: STATUS.md, docs/decisions.md, docs/architecture.md, README.md.
Commands/tests: immediate scoped git diff --check PASS; editor diagnostics clean; current pending-state references reconciled. No new runtime tests or cloud operations; acceptance uses recorded independent evidence.
Result: ACCEPT D-014 as bounded VALIDATED for trusted, supervised, single-operator MCP lab use only. Independent Tester 63 PASS plus deployed digest/source/runtime/SDK/probe/failure checks and Security Reviewer GO satisfy the contract. SDK reflection, unauthenticated plaintext access, unrestricted networking and availability limits remain. No production/shared readiness, gateway/inference milestone or Cilium authorization follows. D-013 future phases and independent D-011 router gate retained. Forwarding remains stopped until operator starts it.
Artifacts: STATUS.md current milestone/handoff; docs/decisions.md D-014 acceptance; architecture and README access instructions.

### Agent execution
Agent: developer
Date: 2026-10-23
Why selected: mandatory implementation/deployment role after D-014 approval and conditional predeployment security GO.
Task: build/test the exact AMD64 source, create the dedicated ACR with scoped pull access, publish an immutable image and deploy only the MCP workload.
Files inspected: governing docs/profile, source/tests/configuration, dependency inputs, Docker/build-context files, MCP and existing AKS infrastructure/manifests, relevant skills and authoritative packaging/Azure guidance.
Files modified: Dockerfile, tests/test_lab_mcp.py, infra/registry.bicep, k8s/mcp/lab-info.yaml, STATUS.md, README.md, docs/architecture.md, docs/troubleshooting.md. main.py unchanged.
Commands/tests: initial focused packaging/security/drift 3 PASS; full suites 63 PASS (13.98s, 13.90s after packaging repair, final 13.88s). Verified base digest/bootstrap hashes; synchronous AMD64 build initially failed 139 from uv under QEMU, reproduced with uv --version; native frozen export and target pip repair built successfully. Hardened AMD64 container and actual SDK/probes passed; temporary container removed. Permission/identity assessment; Bicep compile/server validate/what-if (two creates only); incremental d014-mcp-registry succeeded. Entra registry login/push, remote digest inspection, namespace/full manifest server dry-runs, apply and rollout, read-only runtime inspection and real SDK through localhost:18000 forwarding. git diff --check PASS. Exact reproducible evidence and failure details are in STATUS.md/README.md/troubleshooting.
Result: DEPLOYED, not self-certified VALIDATED. Basic acragwlabd18f2ff3 has admin/anonymous disabled; only direct assignment is actual kubelet registry-scoped AcrPull, no new operator roles/secrets. Published digest 29f6d6d123c54cec36ca64c104ff55450de823a27b52d3a1db75cdfd8e320b76 matches Ready app-pool pod. Both structured tools and healthy/health_ok/200 observed; probes 200. Forward closed; unrelated port 8000 service untouched. No network migration/policies, gateway, public app exposure, llama.cpp restart, commit or Git push.
Artifacts: deployed ACR/MCP; infra/registry.bicep; immutable k8s/mcp/lab-info.yaml; operational handoff.

### Agent execution
Agent: tester
Date: 2026-10-23
Why selected: mandatory independent behavioral/runtime validation after Developer deployment.
Task: verify actual deployed image/source, placement, runtime hardening, Service/probes, real SDK/both tools and failure independence against D-014.
Files inspected: PROJECT_CONSTITUTION.md, STATUS.md, .github/agents/tester.agent.md, docs/decisions.md, docs/architecture.md, k8s/mcp/lab-info.yaml, tests/test_lab_mcp.py, README.md, main.py, Dockerfile; packaged/dependency inputs through tests.
Files modified: none.
Commands/tests: existing full pytest suite 63 PASS in 13.87s; source/lock hashes; explicit-context pod/deployment/Service/EndpointSlice reads and read-only runtime exec; localhost-only Service forwarding and official SDK initialize/list/both calls; invalid Host/Origin and live fixed upstream checks; scoped Azure registry/identity/role reads; same cached AMD64 image offline hardened container failure check; cleanup verification. Initial harness syntax/default-comparison/Azure flag issues corrected and checks passed.
Result: independent PASS. Pod imageID/source match; Ready AMD64 app-pool replica, zero restarts, UID/GID 10001, no capabilities/escalation/token, seccomp and read-only mounts confirmed. Internal Service endpoint ready; no external IP. SDK 2025-11-25, exactly two argument-free tools with structured results/no session ID; healthy/health_ok/200, probes 200, Host/Origin 421/403. Offline same image gives connection_failed while overview/probes work. Scoped kubelet AcrPull confirmed. Forward/container removed, port 18000 free. No inference, gateway/isolation/shared readiness claim or cluster mutation.
Artifacts: independent deployment evidence in STATUS.md; architectural acceptance pending.

### Agent execution
Agent: security-reviewer
Date: 2026-10-23
Why selected: independent security review of actual image, registry permissions and admitted deployment.
Task: assess deployed D-014 trusted-lab scope and newly introduced infrastructure/build changes without application listeners or mutations.
Files inspected: governing docs/profile, STATUS.md, architecture/decisions, main.py/tests, Dockerfile/.dockerignore, dependencies/lock excerpt, registry and existing AKS Bicep, MCP manifest; Microsoft ACR/network policy and uv Docker references.
Files modified: none.
Commands/tests: explicit-context read-only Kubernetes configuration; explicit-subscription ACR/AKS/direct-role reads; local image metadata. No tests, exec, listeners, downloads or mutations. Concurrent Tester evidence excluded; fresh fingerprint comparison limited by shared-terminal interference.
Result: GO only for continued trusted, supervised, single-operator D-014 use. No new CRITICAL/HIGH; known MEDIUM input reflection and unauthenticated plaintext/unrestricted internal access, LOW inbound availability retained. Verified Basic registry/admin/anonymous disabled/actual kubelet-only scoped pull, digest-linked AMD64 image and hardened pod. Base/approved-feed bootstrap/dependency hashes inspected; not whole-image certification. Flagged stale handoff statements for coordinator reconciliation. Reassess if reachable workloads cease to be trusted.
Artifacts: bounded security disposition and residuals in STATUS.md; no architectural milestone acceptance by this role.

### Agent execution
Agent: architect
Date: 2026-10-23
Why selected: amend the deployment design following explicit human approval of the simpler trusted-lab MVP.
Task: record D-014, defer Cilium/enforced policies, preserve D-013 future phases and define the bounded image/registry/runtime contract.
Files inspected: PROJECT_CONSTITUTION.md, .github/agents/architect.agent.md, STATUS.md, docs/architecture.md, docs/decisions.md, Dockerfile, k8s/mcp/lab-info.yaml.
Files modified: docs/decisions.md, STATUS.md, docs/architecture.md.
Commands/tests: immediate git diff --check (PASS); editor diagnostics clean for the three documents. No runtime or cloud operations.
Result: D-014 approves trusted, supervised single-operator ClusterIP/localhost-forwarded deployment direction. Other pods can reach MCP; outbound networking is unrestricted. Prior isolation gate superseded only for this MVP; no networking migration or gateway authorized. Dedicated ACR and registry-scoped kubelet-only AcrPull require permission assessment before execution. Deployment acceptance remains pending.
Artifacts: docs/decisions.md D-014; current architecture and handoff.

### Agent execution
Agent: security-reviewer
Date: 2026-10-23
Why selected: independently reassess the reduced-isolation MVP before deployment.
Task: review D-014, application/packaging and permission contract against the newly approved trusted-lab boundary.
Files inspected: PROJECT_CONSTITUTION.md, .github/agents/security-reviewer.agent.md, STATUS.md, docs/architecture.md, docs/decisions.md D-012 through D-014, main.py, tests/test_lab_mcp.py, Dockerfile, k8s/mcp/lab-info.yaml, config/lab-info.json, pyproject.toml, .dockerignore, infra/main.bicep; lock-source checks via existing test.
Files modified: none.
Commands/tests: existing pytest with -k 'config_and_application or invalid_config or wildcard_or_missing_authority or main_listener_contract or startup_error or reject_health_url or curated_and_packaged_config_drift or manifest_security_and_service_allowlists or approved_dependency_and_container_sources' (28 PASS, 35 deselected, 1.69s); git status and scoped recent log. No listeners, builds, downloads or live cloud/cluster checks.
Result: conditional GO toward D-014 deployment, not acceptance. MEDIUM SDK reflection and unauthenticated/plaintext unrestricted cluster access remain bounded lab residuals; LOW availability/provenance remain. Require public-safe synthetic inputs and trusted reachable workloads, immutable current-source AMD64 image/runtime proof, explicit permission assessment and independent deployed SDK/security checks. Prior NetworkPolicy-based NO-GO does not apply to D-014.
Artifacts: deployment gates and explicit residuals for Developer and Tester.

### Agent execution
Agent: architect
Date: 2026-10-23
Why selected: recommend a supported enforcement path and assess cluster-wide impact before requesting migration approval.
Task: research existing Azure CNI Overlay migration options for D-013, without implementation or cloud changes.
Files inspected: PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md, docs/decisions.md D-013, infra/main.bicep, .github/agents/architect.agent.md.
Files modified: none.
Commands/tests: no shell commands or tests; fetched official Microsoft Learn guidance on upgrade-aks-ipam-and-dataplane, azure-cni-powered-by-cilium and concepts-network-azure-cni-overlay.
Result: recommends AKS-managed Cilium in-place migration, subject to exact eligibility preflight and separate human approval. All pools are reimaged; possible llama.cpp downtime, disk/model recovery and Spot uncertainty require planning. No simple reverse migration established by reviewed guidance. Existing konnectivity policy must be reviewed before enforcement. Recover and validate existing workloads before MCP deployment. No infrastructure or runtime milestone accepted.
Artifacts: STATUS.md recommendation and pending migration approval; official source https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-ipam-and-dataplane.

### Agent execution
Agent: developer
Date: 2026-10-23
Why selected: mandatory implementation role for bounded Phase 1 preparation after D-013 approval.
Task: verify build and networking prerequisites, prepare minimal isolation and locally test packaging if prerequisites permit; no cloud/cluster mutation, push or RBAC change.
Files inspected: PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md, docs/decisions.md, .github/agents/developer.agent.md, Dockerfile, .dockerignore, pyproject.toml, k8s/mcp/lab-info.yaml, tests/test_lab_mcp.py; required skills.
Files modified: none.
Commands/tests: docker info --format and docker buildx inspect both succeeded. Docker 29.5.3, Linux ARM64, Rancher Desktop builder advertises linux/amd64. No application tests or image build.
Result: build daemon prerequisite now satisfied, AMD64 execution unproven. Delegate could not load deferred inspection tools and stopped before inventing selectors or editing source. Coordinator subsequently obtained read-only networking evidence below. No containers, artifacts or deployments created.
Artifacts: STATUS.md updated prerequisite evidence and enforcement blocker.

### Coordinator prerequisite follow-up (not an agent invocation)
Date: 2026-10-23
Commands/checks: dedicated kubectl tool rejected explicit --context selection on five read-only requests; no command executed through it. Consulted Azure MCP troubleshooting guidance. Local kubectl explicitly selected aks-agw-lab for kube-system pods/services/daemonsets, llama.cpp deployment selectors and all-namespace NetworkPolicy inventory. Azure MCP aks_cluster_get read existing target metadata.
Result: DNS Service selects k8s-app=kube-dns on UDP/TCP 53; llama.cpp selects app=llama-cpp; only existing policy is kube-system/konnectivity-agent. AKS networkPolicy is none, networkDataplane azure, plugin azure/overlay; no obvious policy engine in node-agent inventory. Deployment blocked pending separately approved supported enforcement change; no active-context switch or cluster mutation. Documentation whitespace validation passed after recording the findings.

### Agent execution
Agent: architect
Date: 2026-10-23
Why selected: formalize the human-approved two-phase network boundary and resume authorization.
Task: document Phase 1 operator-only forwarding and restricted egress, then later Phase 2 gateway-only pod ingress; preserve runtime and security gates.
Files inspected: PROJECT_CONSTITUTION.md, .github/agents/architect.agent.md, STATUS.md, docs/architecture.md, docs/decisions.md, k8s/mcp/lab-info.yaml; Git status and recent relevant history.
Files modified: docs/decisions.md, docs/architecture.md, STATUS.md.
Commands/tests: git diff --check -- docs/decisions.md docs/architecture.md STATUS.md (PASS); editor diagnostics found no errors. No application tests, build, network, cloud or cluster operations.
Result: D-013 records both phases as approved design, not enforced policy. Explanation pause lifted for reviewed MCP scope. Gateway installation remains separately authorized work; independent runtime, security and acceptance gates remain. Registry approved but not created; Docker readiness still requires a fresh check.
Artifacts: docs/decisions.md D-013; docs/architecture.md MCP boundary; STATUS.md current authorization and next steps.

### Agent execution
Agent: architect
Date: 2026-10-23
Why selected: mandatory bounded deployment planning and prerequisite assessment.
Task: read-only checks for MCP deployment to existing aks-agw-lab; no gateway, public exposure, image build or infrastructure changes.
Files inspected: PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md, docs/decisions.md, .github/agents/architect.agent.md, Dockerfile, k8s/mcp/lab-info.yaml; installed Azure resource-lookup skill.
Files modified: none.
Commands/tests: command availability, uname -m, docker info, docker buildx inspect, git status --short, scoped git log; kubectl current-context, selected config view fields, context names; explicit --context=aks-agw-lab version, selected node scheduling/architecture fields, namespaces, deployments/services/pods and EndpointSlices. One rg-based guard failed because rg is unavailable; no cluster request ran from that guard. No application tests.
Result: target cluster reachable at v1.36.4, Ready untainted AMD64 app node; mcp absent; llama.cpp Ready pod and internal endpoint, not HTTP/inference proof. Active context differs and was left unchanged. Local ARM64; Docker daemon unavailable. Registry/pull access unknown to delegate. Require reviewed security boundary and approved image delivery before apply. No changes or deployment.
Artifacts: STATUS.md active deployment request; docs/decisions.md pending gates.

### Agent execution
Agent: security-reviewer
Date: 2026-10-23
Why selected: independent review before expanding supervised localhost acceptance to cluster access.
Task: read-only predeployment assessment and smallest acceptable isolated-lab controls; no risk acceptance or deployment.
Files inspected: PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md, docs/decisions.md, .github/agents/security-reviewer.agent.md, main.py, Dockerfile, .dockerignore, k8s/mcp/lab-info.yaml, pyproject.toml, tests/test_lab_mcp.py, config/lab-info.json, k8s/llm/llama-cpp.yaml, relevant uv.lock entries.
Files modified: none.
Commands/tests: file reads and lockfile text search only; no shell, tests, network, cloud or cluster operations.
Result: NO-GO as-is. MEDIUM unrestricted unauthenticated cluster reachability and SDK response reflection; LOW inbound availability and packaging provenance. Proposes ingress isolation/operator-only loopback forwarding and DNS/llama.cpp-only egress, subject to human approval and enforcement tests. L4 cannot restrict upstream HTTP paths. No risks accepted. Current local acceptance remains unchanged.
Artifacts: STATUS.md active deployment security gate; docs/decisions.md pending boundary.

### Agent execution
Agent: tester
Date: 2026-10-19
Why selected: independent validation of Phase 2 (AKS base cluster); the Developer role had deployed it and must not self-certify (Constitution section 13).
Task: validate nodes Ready, pod scheduling on the `app` pool and not the tainted `system` pool, in-cluster DNS, kube-system health.
Files inspected: PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md (per task prompt).
Files modified: none (temporary namespace `phase2-test`, deleted afterwards).
Commands/tests: `kubectl get nodes`, test pod with no tolerations, `nslookup` for a cluster name and an external name, `kubectl get pods -n kube-system`.
Result: Completed. 4/4 checks PASS. Observations: Azure Policy admission warnings; extra add-ons (Azure Policy, Defender) not set by our Bicep.
Artifacts: STATUS.md (Phase 2 VALIDATED), docs/troubleshooting.md T-004.

### Agent execution
Agent: tester
Date: 2026-10-20
Why selected: independent validation of Phases 3-4 (Spot GPU pool, NVIDIA device plugin) after Developer deployment.
Task: validate GPU node taints/labels/Spot, `nvidia.com/gpu` allocatable, GPU pod runs `nvidia-smi`, non-GPU pod stays off the GPU node, a second GPU pod stays Pending.
Files inspected: PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md, docs/troubleshooting.md (T-006, T-007).
Files modified: none (temporary namespace `phase4-test`, deleted afterwards).
Commands/tests: `kubectl describe/get node`, test pods t3/t4/t5, pod logs, events.
Result: Completed. 5/5 checks PASS. The Tester's suspicion that the young GPU node meant a Spot eviction was not confirmed: it was the third pool created that day (T-006).
Artifacts: STATUS.md (Phases 3-4 VALIDATED).

### Agent execution
Agent: tester
Date: 2026-10-20
Why selected: independent validation of Phases 5-7 (PVC model storage, llama.cpp deployment, direct inference), single-model version.
Task: pod/Service state, in-cluster health and chat completion, GPU evidence, PVC persistence across pod deletion, PVC contents, no external exposure.
Files inspected: PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md, docs/decisions.md (D-009, D-010).
Files modified: none (temporary pod `tst-curl`, deleted; the llama-cpp pod was deleted once on purpose for the persistence test).
Commands/tests: `kubectl` get/exec/logs, in-cluster curl against `/health` and `/v1/chat/completions`, pod deletion and re-check.
Result: Completed. 6/6 checks PASS (GPU evidence via `nvidia-smi`, not server logs). Gaps noted: no NetworkPolicy, no API key, image tag floating at the time (since pinned by digest).
Artifacts: STATUS.md (Phases 5-7 VALIDATED), docs/architecture.md, docs/decisions.md (image pinned).

## MCP server work (2026-10-22)

### Agent execution
Agent: architect
Date: 2026-10-22
Why selected: mandatory architecture review before implementing the first Python MCP server.
Task: bound local implementation, SDK/protocol selection, security limits, and acceptance criteria; no gateway or cluster deployment.
Files inspected: PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md, docs/decisions.md, pyproject.toml, main.py, .python-version, k8s/llm/llama-cpp.yaml, .github/agents/architect.agent.md, supplied repository instructions.
Files modified: docs/decisions.md (D-012), docs/architecture.md.
Commands/tests: git status --short, scoped git log -5 --oneline, git diff --check on the two modified documents (PASS).
Result: approved bounded local implementation, not milestone completion. Use official SDK FastMCP with verified protocol support, three read-only tools, fixed bounded upstream health GET, local transport/security tests, and offline deployment artifacts. Installed SDK and Docker capabilities remain to be verified. No deployment, commit, or push.
Artifacts: docs/decisions.md D-012, docs/architecture.md.

### Agent execution
Agent: developer
Date: 2026-10-22
Why selected: mandatory implementation role for the first Python MCP server.
Task: implement D-012 locally, preserving gateway and cluster deployment boundaries.
Files inspected: PROJECT_CONSTITUTION.md, STATUS.md, docs/architecture.md, docs/decisions.md, .github/agents/developer.agent.md, main.py, pyproject.toml, k8s/llm/llama-cpp.yaml, README.md, Python fact-grounded and container/Kubernetes skills.
Files modified: STATUS.md; created ignored local .venv.
Commands/tests: created Python 3.12.15 environment; dependency installation/download attempts failed with socket errors; Docker daemon unavailable; git diff --check passed. No behavior tests ran.
Result: blocked before implementation. This attempt preceded the human's explicit approved-feed restriction; public package access must not be repeated.
Artifacts: STATUS.md prerequisite evidence.

### Agent execution
Agent: developer
Date: 2026-10-22
Why selected: resume implementation after the human supplied the approved Python feed.
Task: implement and locally test the bounded MCP server using only the approved feed, with no public PyPI fallback, cluster deployment, or gateway work.
Files inspected: governing docs, developer profile, existing scaffold and llama.cpp manifest, required Python and container/Kubernetes skills.
Files modified: main.py, pyproject.toml, README.md, STATUS.md, docs/architecture.md, docs/decisions.md, docs/troubleshooting.md; added config/lab-info.json, tests/test_lab_mcp.py, uv.lock, Dockerfile, .dockerignore, k8s/mcp/lab-info.yaml.
Commands/tests: approved-feed uv resolution and frozen sync; lock/source audit (37 approved registry entries, 177 feed-provided Microsoft artifact URLs); .venv/bin/python -m pytest -q tests/test_lab_mcp.py (26 PASS); offline uv lock check and frozen sync PASS; git diff --check and editor diagnostics clean.
Result: CREATED, locally checked by Developer. Real MCP HTTP exchange negotiated 2025-11-25 using Python 3.12.15 and mcp 1.30.0. Container build/run unverified because Docker daemon is unavailable. Independent validation and review pending; no deployment, commit or push.
Artifacts: implementation, tests, offline packaging, and run/configuration walkthrough in README.md.

## Outstanding validation

### Agent execution
Agent: tester
Date: 2026-10-22
Why selected: independent behavior validation after Developer implementation.
Task: read-only local CLI and real HTTP MCP checks, upstream failures, approved-feed audit, and offline packaging checks.
Files inspected: governing docs and tester profile, STATUS.md, docs/{architecture,decisions,troubleshooting}.md, README.md, main.py, config/lab-info.json, tests/test_lab_mcp.py, pyproject.toml, uv.lock, Dockerfile, .dockerignore, k8s/{mcp/lab-info,llm/llama-cpp}.yaml, installed SDK sources.
Files modified: none.
Commands/tests: existing pytest suite 26 PASS; independent HTTP/subprocess harness 49 passing assertions and 3 malformed-envelope redaction failures; corrected manifest/startup/audit follow-up 17 PASS. Docker daemon unavailable. Temporary listeners/processes cleaned up.
Result: local happy path demonstrated; D-012 acceptance FAILED pending malformed JSON-RPC error-redaction repair. Malformed jsonrpc/method/params values reflected in HTTP 400 responses, not application logs. Container, gateway and cluster runtime not validated.
Artifacts: finding in main.py transport boundary, regression requirement for tests/test_lab_mcp.py.

### Agent execution
Agent: security-reviewer
Date: 2026-10-22
Why selected: independent MCP endpoint, credential and information-exposure review.
Task: read-only review and local adversarial probes of D-012 implementation and packaging.
Files inspected: security profile, constitution, STATUS.md, docs/{architecture,decisions}.md, main.py, config/lab-info.json, tests/test_lab_mcp.py, pyproject.toml, uv.lock, Dockerfile, .dockerignore, .gitignore, k8s/mcp/lab-info.yaml, README.md, installed MCP/HTTPX/Uvicorn sources.
Files modified: none.
Commands/tests: pytest 26 PASS; local malformed-envelope, chunked/oversized body, slow upload, startup redaction and lock-audit probes. No installs or remote/cloud operations; temporary listeners cleaned up.
Result: no CRITICAL/HIGH findings. MEDIUM: caller input reflected in malformed-envelope errors (must fix for D-012). LOW: inbound upload deadline/concurrency not bounded (before untrusted access). LOW: mutable base image and unhashed uv bootstrap mean application lock is not whole-container provenance. Supervised loopback experimentation acceptable; full acceptance pending redaction fix. No authentication or network-isolation claim.
Artifacts: focused transport repair request; future exposure and packaging gates.

### Agent execution
Agent: developer
Date: 2026-10-22
Why selected: implementation repair after independent error-redaction failure.
Task: prevent malformed JSON-RPC envelope validation details from echoing caller input; preserve bounded bodies and valid SDK behavior.
Files inspected: main.py, tests/test_lab_mcp.py, STATUS.md, D-012, developer profile and installed SDK sources.
Files modified: main.py, tests/test_lab_mcp.py, README.md, docs/troubleshooting.md, STATUS.md.
Commands/tests: focused repair 16 PASS; compatibility 12 PASS; full pytest 52 PASS; diagnostics and git diff --check clean.
Result: bounded SDK-model envelope guard and constant 400 errors implemented; pending independent retest. No new dependencies or deployment.
Artifacts: transport guard and malformed-envelope regressions, T-009.

### Agent execution
Agent: tester
Date: 2026-10-22
Why selected: independent retest of transport repair.
Task: confirm redaction, body-limit ordering, valid JSON/SSE SDK flow, and clean ASGI completion.
Files inspected: governing docs, tester profile, STATUS.md, docs/architecture.md, D-012, main.py, tests/test_lab_mcp.py, README.md, pyproject.toml, installed SDK; suite also checked configuration, lock and packaging artifacts.
Files modified: none.
Commands/tests: full pytest 52 PASS; independent in-memory probes 50 PASS; body/chunk transparency 4 PASS; two deep-input clean-completion failures.
Result: original reflection fixed, but acceptance still FAILED because telemetry json.loads raised RecursionError after safe 400 for deep nested bodies below 64 KiB. Temporary listeners cleaned up; no external operations.
Artifacts: focused telemetry repair request.

### Agent execution
Agent: security-reviewer
Date: 2026-10-22
Why selected: independent security re-review of malformed-envelope repair.
Task: verify redaction and boundary ordering without broadening the review.
Files inspected: main.py, tests/test_lab_mcp.py, pyproject.toml, Dockerfile, .dockerignore, README.md, governing docs, STATUS.md, docs/{architecture,decisions,troubleshooting,agent-execution-log}.md, security profile, installed SDK sources; suite checked config, lock and manifests.
Files modified: none.
Commands/tests: pytest 52 PASS; corrected independent matrix 111 expected HTTP responses, with two post-response recursion exceptions; body-cap instrumentation.
Result: MEDIUM reflection resolved. New LOW telemetry recursion defect; supervised local security acceptance otherwise appropriate. Prior upload/provenance LOW risks unchanged. No sentinel leaks, external operations or lingering listeners.
Artifacts: independent repair assessment and deferred exposure gates.

### Agent execution
Agent: developer
Date: 2026-10-22
Why selected: focused telemetry defect repair requested by both reviewers.
Task: handle recursion failure while recording completion metadata without changing accepted MCP traffic.
Files inspected: main.py telemetry path and tests/test_lab_mcp.py.
Files modified: main.py, tests/test_lab_mcp.py, docs/troubleshooting.md.
Commands/tests: new deep-nesting ASGI regression initially 2 FAIL, then 2 PASS; full pytest 54 PASS; whitespace and diagnostics clean.
Result: caught RecursionError in safe metadata parsing; two 12,000-level nesting cases verify redacted 400, no ASGI exception, and correlated completion. No new dependencies or external operations.
Artifacts: two exception-propagating regressions and T-009 evidence.

### Agent execution
Agent: tester
Date: 2026-10-22
Why selected: final independent local behavioral gate after telemetry repair.
Task: inspect narrow repair and verify clean ASGI completion plus full local behavior.
Files inspected: constitution, STATUS.md, docs/architecture.md, D-012, tester profile, main.py, tests/test_lab_mcp.py, pyproject.toml; suite also read config, lock, Dockerfile, ignore and manifests.
Files modified: none.
Commands/tests: bytecode/cache-disabled full pytest 54 PASS in 12.90s; two independent direct-ASGI deep-input cases PASS, including completion metadata and reset correlation state.
Result: D-012 LOCAL behavioral gates PASS. Container/Linux runtime, Kubernetes, live upstream and gateway remain unverified; no packaging provenance acceptance. Temporary listeners cleaned up.
Artifacts: independent local validation evidence; no deployment or commits.

### Agent execution
Agent: security-reviewer
Date: 2026-10-22
Why selected: final security confirmation of the telemetry repair.
Task: verify no response/log leak or uncaught ASGI exception and reassess scoped local acceptance.
Files inspected: main.py, tests/test_lab_mcp.py, pyproject.toml, Dockerfile, constitution, STATUS.md, docs/architecture.md, D-012, security profile; suite also checked config, lock, ignore and manifests.
Files modified: none.
Commands/tests: bytecode/cache-disabled offline pytest 54 PASS in 13.22s, including deep-nesting and real HTTP SDK flows; cleanup assertions PASS.
Result: reflection and telemetry findings resolved. Security-scoped supervised loopback use accepted. Deferred LOW: inbound upload deadline/concurrency, mutable base image and unhashed uv bootstrap. No shared/customer exposure, authentication, TLS, isolation, container or cluster acceptance.
Artifacts: final local security verdict; no external operations or commits.

- Router-mode llama.cpp with four models (D-011) still needs independent validation before Phase 9.
- Broader Phase 11 security review remains separate from the MCP review and local acceptance below.

### Agent execution
Agent: architect
Date: 2026-10-22
Why selected: required final milestone acceptance against D-012 and independent evidence.
Task: evaluate local source behavior only and reconcile durable claims with validation and remaining deployment gates.
Files inspected: constitution, architect profile, STATUS.md, docs/{architecture,decisions,agent-execution-log}.md, README.md, main.py, tests/test_lab_mcp.py, pyproject.toml, Dockerfile, k8s/mcp/lab-info.yaml.
Files modified: STATUS.md, docs/architecture.md, docs/decisions.md, README.md.
Commands/tests: git status --short; relevant git log -5; immediate git diff --check for modified documents PASS. Relied on independent Tester 54 PASS plus two probes and Security Reviewer 54 PASS; no redundant test run.
Result: ACCEPT D-012 LOCAL source for supervised loopback experimentation. Container/Linux runtime, provenance, Kubernetes, live upstream and gateway remain unverified; no broad phase completion. Upload/provenance LOW risks and access-control gates remain explicit. Phase 8 paused; D-011 validation separate.
Artifacts: scoped architectural acceptance and consistent documentation; no installs, external operations, commits or pushes.

## Two-tool teaching simplification (2026-10-22)

### Agent execution
Agent: architect
Why selected: bound the human-authorized simplification for a non-developer's 10-15-minute code walkthrough.
Task: replace the three-tool implementation with a static overview and a live health observation, keeping gateway deployment paused.
Files inspected: constitution, Architect profile, STATUS.md, architecture, D-012, main.py, tests/test_lab_mcp.py, README.md, configuration, manifests, pyproject.toml, Dockerfile, Git status/history.
Files modified: docs/decisions.md, STATUS.md.
Commands/tests: git status --short, relevant git log, git diff --check PASS; documentation diagnostics clear. No runtime tests for this planning step.
Result: D-012 teaching amendment PLANNED. Prefer plain FastMCP, no schema hierarchy/custom HTTP wrapper, fixed bounded health GET and two tools. Explicit MEDIUM residual: removing response guard restores SDK caller-input reflection; supervised loopback only. No deployment or broader protection claim.
Artifacts: D-012 amendment and bounded Developer contract.

### Agent execution
Agent: developer
Why selected: substantial implementation under the approved two-tool teaching contract.
Task: simplify source, adapt existing tests and document a 12-minute walkthrough without changing deployment scope.
Files inspected: Developer profile, constitution, STATUS.md, D-012, architecture, main.py, tests, README.md, JSON, MCP/llama.cpp manifests, pyproject.toml, Dockerfile; offline assertions also inspect lock/ignore sources and installed SDK behavior.
Files modified: main.py, tests/test_lab_mcp.py, README.md, docs/architecture.md, STATUS.md.
Commands/tests: existing-environment python -m pytest, bytecode/cache disabled: initial focused 6 PASS; SDK/health/security focused 23 PASS after dictionary annotation repair; startup/probe follow-up 13 PASS; final full file 63 PASS in 13.90s. Diagnostics and git diff --check clean.
Result: 212-line plain FastMCP source CREATED pending independent acceptance; exactly two tools, overview includes presets, bounded health dict, SDK/probe protection. No new dependencies or deployment. Custom response sanitization deliberately removed and residual documented, not silently treated as resolved.
Artifacts: simplified source/tests and README walkthrough. No installs, downloads, cloud operations, delegation, commits or pushes.

### Agent execution
Agent: tester
Why selected: independent behavioral validation of the simplified implementation.
Task: verify the two-tool SDK path and fixed-target health/probe behavior against the teaching amendment.
Files inspected: Tester profile, constitution, STATUS.md, architecture, D-012, main.py, tests, README.md, config, MCP/llama.cpp manifests, pyproject.toml, Dockerfile, ignore; suite parsed uv.lock. Python fact-grounded skill and relevant Git state/history also reviewed.
Files modified: none.
Commands/tests: PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_lab_mcp.py -> 63 PASS in 13.95s; independent inline loopback SDK/HTTP probes PASS. Git status unchanged.
Result: PASS bounded local behavior. SDK 1.30.0 negotiated 2025-11-25, exactly two no-parameter tools and no session ID. Fixed GET /health despite extra target arguments; actual slow-body timeout 3.006s. Overview/probes independent of health, Host 421/Origin 403, application errors/logs sanitized, temporary ports/workers cleaned up. SDK reflection remains known MEDIUM residual, not a new blocker.
Artifacts: independent evidence only; no container, cluster, live llama.cpp or gateway validation; no external operations or commits.

### Agent execution
Agent: security-reviewer
Why selected: independent security review of the SDK-only boundary and changed safeguards.
Task: assess fixed egress, local binding, Host/Origin protection, errors/logging and explicit residual risk without requiring a production framework.
Files inspected: Security Reviewer profile, constitution, STATUS.md, architecture, D-012, main.py, tests, README.md, MCP manifest, JSON, Dockerfile, pyproject.toml, ignore and installed SDK sources; suite checked lock and llama.cpp presets.
Files modified: none.
Commands/tests: full suite 63 PASS in 13.90s; supplemental 23 scenarios/checks PASS, including forwarded headers, probe GET/HEAD, source override and error/log probes. Exploratory parse error/status expectation corrected before conclusions; review listeners/threads cleaned up.
Result: acceptable ONLY for supervised loopback; no new scoped blocker. MEDIUM known SDK reflection includes malformed input, protocol header and unknown tool names. LOW upload deadline/concurrency and packaging provenance remain. Invalid UTF-8 constant 500 observed without sentinel leak. Shared/customer access requires separate controls/review; not architectural acceptance.
Artifacts: independent scoped security verdict; no edits, installs, non-loopback operations, deployment, delegation, commits or pushes.

### Agent execution
Agent: architect
Date: 2026-10-22
Why selected: final acceptance of the amended two-tool teaching milestone against independent evidence.
Task: reconcile the current source and handoff with the narrower demonstration scope, without accepting deployment or equivalent former guard protection.
Files inspected: constitution, Architect profile, STATUS.md, docs/decisions.md, docs/architecture.md, README.md, main.py, test contract anchors, docs/agent-execution-log.md.
Files modified: STATUS.md, docs/decisions.md, docs/architecture.md, README.md.
Commands/tests: git status --short, relevant git log -3, immediate scoped git diff --check PASS; document diagnostics clear. Relied on independent Tester 63 PASS plus SDK/timeout/target probes and Security Reviewer 63 PASS plus 23 checks; no redundant runtime tests.
Result: ACCEPT amended D-012 two-tool LOCAL source for supervised loopback only. Known MEDIUM SDK response reflection and LOW uploads/provenance remain. Former three-tool guard acceptance does not carry over. No container, Kubernetes, live llama.cpp or gateway acceptance; Phase 8 paused.
Artifacts: current scoped acceptance and proposed 12-minute README walkthrough (delivery timing unmeasured). No code edits, installs, external operations, delegation, commits or pushes.

### Agent execution
Agent: architect
Date: 2026-10-23
Why selected: required architectural coordination for the next Kubernetes/gateway learning stage after the human confirmed code understanding.
Task: prepare a bounded 10-15 minute walkthrough of current manifests and planned gateway responsibilities, not deployment.
Files inspected: PROJECT_CONSTITUTION.md, Architect profile, STATUS.md, docs/architecture.md, docs/decisions.md (D-006/D-011/D-012), k8s/mcp/lab-info.yaml, k8s/llm/llama-cpp.yaml, Dockerfile; file/text searches checked existing gateway artifacts.
Files modified: none.
Commands/tests: read_file, file_search, grep_search only; no shell commands or tests.
Result: ready for teaching sequence: CPU Deployment/Pod, ConfigMap/probes, Service 80->8000, GPU contrast, separate model/MCP/health paths, controller versus data-plane roles. No gateway manifests exist; documented versions/fields remain proposals requiring verification before implementation. No live state checked.
Artifacts: read-only walkthrough outline and prerequisites. MCP container/cluster and gateway remain unverified; independent router validation remains required before Phase 9. No network, installation, cloud/cluster/Docker operations, delegation, commits or pushes.
