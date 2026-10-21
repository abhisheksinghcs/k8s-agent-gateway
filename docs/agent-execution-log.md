# Agent execution log

Every delegation to a custom agent (`.github/copilot-instructions.md`, "Agent execution transparency"). Entries 1-3 were written after the fact on 2026-10-20 because the log was not created when those agents ran; they are reconstructed from each agent's final report. Nothing is listed here that was not actually invoked.

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

## Not yet delegated

- Router-mode llama.cpp with four models (D-011) has only Developer evidence. It needs an independent Tester pass before Phase 9 (agentgateway to llama.cpp), per "validate the llama.cpp upstream independently first".
- Security Reviewer has not been invoked yet; scheduled for Phase 11 and before any external exposure.
