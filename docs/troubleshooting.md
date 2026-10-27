# Troubleshooting

Entries are observation, hypothesis, test, result.

## D-011 Permission Checks Must Distinguish Symlinks (Tester, 2026-10-27)

- Observation: an unrestricted `find /models -perm -0002` also lists the four
	snapshot symlinks (conventional link mode 0777), although their regular blob
	targets are 0664 and no directory/regular file is world-writable.
- Hypothesis/check/result: inspect file types, not link mode alone. Existing-pod
	`kubectl --context=aks-agw-lab -n llm exec llama-cpp-5f676cf74f-vzjtv
	-c llama-server -- sh -c 'find /models \( -type f -o -type d \) -perm -0002 -print;
	find -L /models -type f ! -readable -print;
	find /models -type d \( ! -writable -o ! -executable \) -print'`
	returned no violations as UID 10001. Dereferenced regular targets also passed
	`-writable`; this checks permissions, not successful new-file I/O or remount
	behavior. No arbitrary write probe/permission repair was performed.
- Independently captured before/after file-type/size/path/symlink inventories
	were identical across four successful bounded inference requests. Historical
	CUDA/offload evidence and its provenance limits are recorded in STATUS;
	do not conflate historical verbosity-4 ports with final default-3 workers.

## D-011 Non-root Cache And Explicit Offload (Developer, 2026-10-27)

- Observation: UID 0/Seccomp 0 baseline, four cache trees root-owned 0755/files
	0644. The only 0700 directory was filesystem lost+found, not model weights.
	Azure Disk CSIDriver v1.33.7 advertises fsGroupPolicy=File.
- Hypothesis/test/result: supported fsGroup 10001/OnRootMismatch with numeric
	UID/GID 10001 and RuntimeDefault admitted, rolled out and reached Ready.
	Actual process Seccomp=2, CapEff=0, NoNewPrivs=1. Cache root/model directories
	became root:10001 2775, lost+found 2770; temporary unique cache write probe
	succeeded and was removed. No manual chmod/chown, privileged/root init,
	replacement PVC or weight deletion. Group metadata changes persist on rollback;
	OnRootMismatch can skip later matching mounts, not continuously repair all
	descendants. Recheck if the image, CSI or cache layout changes.
- Approved temporary verbosity 4 pod llama-cpp-578cb5c7b9-c9dx5, same pinned
	build 11749/1d88cb05f, produced these reviewed correlations:

| Preset | Child Port | CUDA Initialization | Actual Offload Line |
|---|---|---|---|
| qwen2.5-7b-instruct | 40649 | 20:19:52Z, found 1 CUDA devices | 20:20:39Z, `load_tensors: offloaded 29/29 layers to GPU` |
| qwen2.5-coder-7b-instruct | 33453 | 20:20:44Z, found 1 CUDA devices | 20:21:31Z, `load_tensors: offloaded 29/29 layers to GPU` |
| llama-3.1-8b-instruct | 36313 | 20:21:35Z, found 1 CUDA devices | 20:22:25Z, `load_tensors: offloaded 33/33 layers to GPU` |
| phi-4 | 41137 | 20:22:30Z, found 1 CUDA devices | 20:24:00Z, `load_tensors: offloaded 41/41 layers to GPU` |

- Each reported device 0 NVIDIA RTX Pro 6000 Blackwell DC-4-48Q MIG 4g.48gb,
	compute capability 12.0, VMM no, 48838 MiB reported VRAM. All four public
	arithmetic responses HTTP 200/exact 42, completion tokens 3/3/2/2; client
	seconds 48.586/48.328/50.844/91.782 include loading, not throughput benchmarks.
	Qwen was normally idle-LRU evicted for Phi. Router/observed workers retained
	UID/GID 10001, Seccomp 2, CapEff 0, NoNewPrivs 1; inherited threshold 4.
- Logging boundaries: selected configured key/logging overrides absent before
	enabling 4; no private/credential requests, no level 5 or model-admin endpoint.
	Full retained startup logs captured privately outside Git, only reviewed
	initialization/layer/model excerpts retained here. Defender DaemonSets have
	host log access; remote retention/access was not certified or changed.
	Kubernetes logs may persist independently of local cleanup. Default 3 restored
	by applying the checked-in manifest. It cannot provide these backend INFO lines.
- T-003 recurred: sync terminal returned early/incomplete output while artifacts
	continued appearing. Do not infer request failure or repeat blindly. Inspect
	private HTTP status/body captures and allow the sequential client to finish;
	do not enqueue additional terminal input into an active loop. Missing `rg`
	caused an earlier read-only inspection exit 127; ordinary search tools suffice.
- Rollback: reapply current manifest to remove temporary logging. For an actual
	hardening regression only, remove its added pod securityContext and dry-run/
	apply, retaining all pre-existing fields and PVC. This restores the insecure
	baseline, not a security exception/acceptance. Independent gates still apply.
- Sources: [Kubernetes security-context and volume ownership](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/),
	pinned CUDA Dockerfile/common logging/server-models sources linked in the
	earlier entry below. CSI ownership delegation can affect fsGroupChangePolicy;
	observed permissions, not policy declaration alone, establish this result.

## D-011 Router Discovery And GPU Diagnostics (2026-10-27)

- Observation: independent direct tests found eight `/v1/models` entries despite
	exactly four ConfigMap preset sections. Four have `source=preset` and the
	approved friendly IDs; four have `source=cache` and repository IDs. Initially
	all were unloaded. Health 200 and discovery alone still do not prove inference.
- Hypothesis/test/result: discovery combines cached repositories and presets.
	Compare the live mounted `/config/models.ini` with `source=preset` entries,
	not total list length; exact four-preset equality passed. Request only the
	approved preset IDs. Observe `status.value` through this existing GET for
	loaded-state evidence; do not call model administration endpoints.
- Observation: ordinary fourth-preset inference logged idle-LRU eviction of
	Qwen; discovery remained at three loaded presets after Phi loaded. This did
	not delete cached weights or test persistence/concurrency/failure recovery.
- GPU diagnostic limit: current bounded logs contained load/generation events
	but no explicit CUDA initialization/offloaded-layer counts. Do not fabricate
	counts from `-ngl 99`. Existing-pod `nvidia-smi` showed actual compute workers
	and GPU memory; worker cmdlines/maps correlated aliases and CUDA libraries.
	Structured `--query-compute-apps=pid --format=csv,noheader,nounits` returned
	`[Insufficient Permissions]` on this MIG setup despite the ordinary table
	listing numeric PIDs. Do not parse that string as a PID or escalate privileges;
	use the already observed table PIDs for bounded read-only `/proc` inspection.
- Terminal evidence limit (T-003 recurrence): empty output or shell exit 130
	did not reliably describe the HTTP result. Inspect workload/client state
	before repeating; retain generated response bodies and curl transport output
	outside the repo when useful. Llama's saved curl exitcode was 0/HTTP 200;
	Phi's first transport artifact was empty even though its body was valid.
	A body alone is insufficient HTTP-success evidence; a subsequent ordinary
	warm request captured literal 200 headers. No 600-second timeout was observed.
- Reproduce runtime checks with `kubectl --context=aks-agw-lab -n llm exec
	<existing-pod> -c llama-server -- nvidia-smi` and bounded `logs` in the same
	explicit context. Follow README's localhost-only direct-inference guide;
	do not change capacity, workloads, logging config or model cache to get proof.

## D-011 Backend INFO Logs Require Verbosity 4 (2026-10-27)

- Observation: full retained replacement-pod logs had only 17 router startup
	lines, no CUDA/offload evidence; the previously tested pod was NotFound.
	Live imageID matched the manifest; executable reported build 11749,
	commit `1d88cb05f`. Args/presets/environment had no logging override.
- Hypothesis/check/result: backend INFO is filtered, rather than child stderr
	requiring debug forwarding. Pinned source confirms default threshold 3,
	backend INFO/CONT mapped to TRACE=4 and discarded by the callback. Both
	CUDA initialization and `offloaded X/Y layers to GPU` use backend INFO.
	Router forwards child stderr at level 0. `-ngl 99` cannot prove offload.
- Authoritative pinned sources:
	[threshold/callback](https://github.com/ggml-org/llama.cpp/blob/1d88cb05f1a257f90741538ca3aca6c1b015c6d3/common/log.cpp#L548),
	[callback installation](https://github.com/ggml-org/llama.cpp/blob/1d88cb05f1a257f90741538ca3aca6c1b015c6d3/common/common.cpp#L388),
	[GGML linkage](https://github.com/ggml-org/llama.cpp/blob/1d88cb05f1a257f90741538ca3aca6c1b015c6d3/src/llama-impl.cpp#L55),
	[child forwarding](https://github.com/ggml-org/llama.cpp/blob/1d88cb05f1a257f90741538ca3aca6c1b015c6d3/tools/server/server-models.cpp#L187),
	[offload message](https://github.com/ggml-org/llama.cpp/blob/1d88cb05f1a257f90741538ca3aca6c1b015c6d3/src/llama-model.cpp#L1991),
	[CUDA message](https://github.com/ggml-org/llama.cpp/blob/1d88cb05f1a257f90741538ca3aca6c1b015c6d3/ggml/src/ggml-cuda/ggml-cuda.cu#L311),
	[supported flags/default](https://github.com/ggml-org/llama.cpp/blob/1d88cb05f1a257f90741538ca3aca6c1b015c6d3/tools/server/README.md#L106).
- Reproduce read-only: `kubectl --context=aks-agw-lab -n llm logs
	pod/<existing-pod> -c llama-server --timestamps --tail=-1`; filter the full
	stream for `CUDA|cuda|offload|layer|spawn`, retaining bounded excerpts and
	total counts. Version: `kubectl --context=aks-agw-lab -n llm exec
	<existing-pod> -c llama-server -- sh -c '/app/llama-server --version 2>&1'`.
- Recommended Developer change only: temporary `--log-verbosity 4` (supported
	equivalent `LLAMA_ARG_LOG_VERBOSITY=4`), not level 5/`--verbose` or prompt
	logging. Requires separately authorized Recreate interruption; no change was
	made here. Afterward one sequential normal request per approved preset plus
	full startup logs must correlate alias/port, CUDA device and observed X/Y
	offloaded layers. No retrospective log recovery API was identified; raising
	verbosity later cannot reconstruct discarded startup messages. Exact layer
	counts and the explicit log gate remain unverified until that test succeeds.

## D-015 Gateway/MCP Deployment (2026-10-23)

- Observation: v1.6.0 controller/proxy rolled out with TLS xDS, CPU placement,
	hardening and private Services; all current-generation conditions were true.
	SDK 1.30.0 negotiated 2025-11-25 and preserved both unprefixed tools/no sessions.
- Contract: controller placement/resources are TOP-LEVEL Helm values, not
	controller.nodeSelector. Put AgentgatewayParameters in place BEFORE Gateway;
	otherwise generated Service defaults could briefly expose it. Use named
	agentgateway container overlays to preserve generated probes and credentials.
- Credential evidence: native controller API token; proxy audience agentgateway,
	requested 43200-second token/CA read-only mounts, HTTPS xDS:9978 and generic
	automount false. MCP stays token-free. Do not weaken xDS/hardening to fix errors.
- Observation/test: every request through exact /mcp succeeded; foreign Origin
	returned upstream 403 unchanged. Seven unrelated paths returned 404. Direct
	MCP probes returned 200, foreign Host 421, foreign Origin 403. A one-off direct
	diagnostic asserted 400 instead of 403 and failed; corrected assertion passed.
	Do not change service behavior to satisfy an incorrect diagnostic expectation.
- Observation: health was healthy/health_ok/200 despite the operator's absent-GPU
	report. Conclusion: health is not inference/GPU-allocation evidence. Leave
	llama.cpp/PVC/pools untouched; gateway unavailable-upstream proof remains open
	rather than manufacturing disruption. Local deterministic failure tests pass.
- Tool mechanics: Helm 4.2.2 rejects old `helm list --all`; use
	`helm list --kube-context=aks-agw-lab --all-namespaces`. RBAC templates are
	role.yaml and serviceaccount.yaml (not clusterrole.yaml/rolebinding.yaml).
	Exact generated pod source is controller/pkg/helm/agentgateway/templates/_helpers.tpl,
	not _pod.tpl (404). Use explicit resource/name syntax for admission lookups,
	not a comma-joined name interpreted as a resource type. These read-only command
	errors caused no deployment changes. A dedicated deferred-tool loader was
	unavailable, so cluster commands used terminal with explicit context throughout.
- Safety: standard Gateway API v1.6.0 includes 10 CRDs PLUS its official CRD
	safe-upgrade policy/binding, all absent before this install. Keep them on
	rollback; never delete unrelated/shared CRDs. Controller Secret reads remain
	reviewed HIGH/human accepted, not fixed by namespace selection/write scoping.
- Reproduce: [README gateway guide](../README.md#private-gateway-and-mcp-d-015-deployed).
	Source/default tests are offline; set GATEWAY_TEST_URL only to a localhost-bound
	proxy forward for real SDK/negative checks. No wildcard allowlists, Origin
	stripping, model routes, public exposure or network-policy changes are needed.

## AMD64 uv crashes under local QEMU (D-014 execution, 2026-10-23)

- Observation: synchronous `docker buildx build --platform linux/amd64 --load
	--tag lab-info:d014 .` failed with exit 139 after hash-verified uv 0.11.24
	bootstrap from the approved feed. No dependency-feed/network failure occurred.
- Hypothesis: uv binary emulation failure, not application or dependency failure.
- Test: disposable AMD64 pinned Python container ran `uname -m` and Python
	3.12.15 successfully, then the same verified uv wheel's `uv --version` crashed
	with QEMU signal 11. Container was automatically removed.
- Result: use native BUILDPLATFORM stage only for offline frozen hash-preserving
	lock export; target AMD64 Python/pip enforces hashes and wheel-only installs.
	Synchronous rebuild succeeded; full source suite 63 PASS. Actual hardened
	AMD64 container and deployed AKS pod ran both tools through the real SDK.
	Do not infer AMD64 application support from Python alone, or retry the same
	crashing uv path without new evidence.

## Local smoke-test port conflict (D-014 execution, 2026-10-23)

- Observation: host port 8000 returned 405 for MCP and 404 for probes while the
  container-local probe passed. An unrelated existing Python process owned 8000.
- Test/result: leave that process untouched, publish only localhost:18000 and
  explicitly allow its Host/Origin. One initial forwarding disconnect was followed
  by successful container-local and host SDK checks. AKS localhost:18000 forwarding
  later passed both tools and probes; all session-owned listeners were removed.

## T-001 GPU family quota is 0 (blocker, 2026-10-19)

- Observation: `az vm list-usage -l westus2|southeastasia` shows `StandardNCdsRTXPRO6000BSEv6XLFamily` limit 0. `az vm list-skus` reports no restrictions, so availability is not the problem; quota is.
- Result: needs a quota increase before any GPU node can be created. Also check the regional total (`cores`): westus2 uses 34/100.
- Reproduce: `LOCATION=westus2 ./scripts/preflight.sh`.

## T-002 `az vm list-skus --all` is very slow

- Observation: `--all` across every region took several minutes; filtering by `--location` is much faster.
- Even with `--location`, `az vm list-skus --size` took many minutes in Phase 2 (the preflight run never finished). `preflight.sh` now adds `--resource-type virtualMachines`; HYPOTHESIS: this speeds it up. Not yet re-verified.
- Workaround: run scripts that call it in the background with output redirected to a file.

## T-004 Azure Policy admission warnings on the cluster (observation, 2026-10-19)

- Observation: pod creation prints warnings from `default-k8s-misconfiguration-policy` (non-root, limits, read-only root FS, drop capabilities, ACR-only images, SA token). Pods are admitted.
- Next: apply sensible securityContext/limits to lab workloads where practical; if the policy turns to deny, record the fix here.

## T-005 Portal quota requests for GPU families fail (2026-10-20)

- Observation: requests for the RTX PRO 6000 BSE v6, A100 v4 and H100 v5 families in southeastasia each returned "We were unable to adjust your quota. Submit a support ticket". All other modern GPU families are also 0/0, in every one of the ~15 subscriptions visible to the login that exposed these families (none had non-zero limits).
- Result: standard-family GPU quota needs a support ticket. Workaround found: Spot uses a separate regional quota pool (D-008).

## T-006 Spot GPU node fails bootstrap: "containerd did not become ready", exit 84 (2026-10-20)

- Observation: Spot pool create on `Standard_NC72ds_xl_RTXPRO6000BSE_v6` (southeastasia, zone 1) passed quota and allocated a VM, then failed in the AKS custom script extension (exit 84, "containerd did not become ready", CSE ran 31 s). Pool state: Failed.
- Evidence (run-command on the node): GPU is visible (`lspci`: NVIDIA device 2bb5, a Blackwell part); no NVIDIA driver loaded yet (no `nvidia-smi`, no modules). containerd later started fine (`booted in 0.87s`) at 16:49:46, about 2 s after the CSE gave up (CSE started 16:49:13). cloud-init `config-resizefs` took 29.5 s and delayed `sysinit.target`, which containerd waits on.
- HYPOTHESIS: a boot-time race on this SKU (slow root filesystem resize) rather than a GPU/driver incompatibility. NOT yet proven: driver install had not run, so a later failure is still possible.
- Test: delete the failed pool and retry once. If it fails the same way: try Ephemeral OS disk, then a different SKU (A100/H100) to isolate SKU vs spot.
- Diagnostic method (no SSH needed): `az vmss run-command invoke -g <MC_ resource group> -n <vmss> --instance-id 0 --command-id RunShellScript --scripts '...'`; output is capped near 4 KB, so keep commands narrow.
- Result: an identical retry failed the same way (deterministic, not random). Root cause: for this SKU AKS defaults to an Ephemeral OS disk of 2040 GB on the local NVMe (the CPU pools get a 128 GB Managed disk); growing that filesystem takes ~29 s. Fix: `osDiskType: Managed`, `osDiskSizeGB: 128` on the GPU pool (in `infra/main.bicep`). The third attempt succeeded; node Ready. RESOLVED.

## T-007 NVIDIA device plugin cannot read MIG info unless privileged (2026-10-20)

- Observation: the GPU is exposed as a MIG slice (`nvidia-smi`: MIG mode Enabled, ~46 GiB). The AKS docs' static device-plugin manifest with `MIG_STRATEGY=single` crashes/blocks with `error getting MIG profile ... error getting parent memory info: Insufficient Permissions`; node advertised no `nvidia.com/gpu`.
- Tests (one change each): (1) add `SYS_ADMIN`: same error. (2) add `NVIDIA_MIG_MONITOR_DEVICES=all`: same error. (3) `privileged: true`: works, node advertises `nvidia.com/gpu: 1`.
- Open: the minimum privilege is not known; the manifest is currently privileged (lab only). Candidates to test: a different device-plugin version, or Helm chart/GPU Operator defaults. Security Reviewer to look at this at Phase 11.
- Also note: the Spot GPU pool carries two taints, `sku=gpu:NoSchedule` and `kubernetes.azure.com/scalesetpriority=spot:NoSchedule`; every GPU pod needs both tolerations.

## T-008 Spot eviction of the GPU node and automatic recovery (2026-10-21)

- Observation: the `kubectl port-forward` to the llama.cpp Service dropped ("lost connection to pod"), then reported `pod is not running. Current status=Pending`. The original GPU node (VMSS instance 000000, created 2026-10-20 ~17:08Z) was gone; instance 000005 replaced it. Pod events: `FailedScheduling` (no GPU node), `TriggeredScaleUp ... 0->1`, then `Scheduled`, image `Pulled` (3m14s earlier on the old node, again on the new one).
- Result: a real Spot eviction after roughly 15 hours. Recovery was automatic: the pool autoscaler (min=max=1) created a new node, the device plugin DaemonSet landed on it, the node advertised `nvidia.com/gpu: 1`, the PVC re-attached, and the router started with all four models already cached (no re-download). A chat request after recovery returned the correct answer. Time from eviction to serving: roughly 25-30 minutes (autoscaler scale-up + node boot + image pull + disk attach); the exact eviction time was not captured.
- Consequence: expect ~half an hour of downtime per eviction; clients (Pi, port-forward) must reconnect. A `port-forward` bound to a pod dies when the pod is replaced; the reconnect loop restores it once the pod is Running.
- Not yet done: measuring eviction frequency/duration precisely; pre-pulling the image to cut recovery time.

## T-003 Terminal output sometimes empty in the agent shell

- Observation: during Phase 0, commands run in a shell that had a background job returned no output or exit code 130.
- Workaround: run long Azure CLI queries in a fresh terminal and redirect output to a file, then read the file.

## T-009 Python MCP dependency source and SDK error reflection (2026-10-22)

- Observation: an earlier implementation attempt failed against the public artifact host before source implementation. The human subsequently prohibited public PyPI and approved only `https://packagefeedproxy.microsoft.io/pypi/simple`. Do not retry the historical public-host commands.
- Test/result: exact `mcp==1.30.0` resolved and installed from the approved feed with frozen uv dependencies. The lock audit found 37 approved-registry entries and 177 feed-provided Microsoft artifact URLs. No authentication secret was needed; if future feed access requires one, tell the coordinator without requesting it through the model. Docker remains blocked by its unavailable local daemon, not by Python dependencies.
- Observation: adversarial HTTP tests initially produced 20 passes/1 failure because the SDK reflected an unsupported `MCP-Protocol-Version` value in an error. Hypothesis: reject that header before SDK handling, leaving ordinary MCP processing to the SDK.
- Result: `SafeHTTP` now returns a constant unsupported-revision error. The rerun passed 21/21 at that stage; later tests extend packaging and deadline coverage. Run `.venv/bin/python -m pytest -q tests/test_lab_mcp.py` for current evidence. SDK/dependency/access log streams are silenced, while safe application lifecycle records are retained. This is Developer evidence, not independent security acceptance.
- Independent review follow-up: malformed JSON-RPC envelopes still reflected Pydantic `input_value` in SDK HTTP 400 responses; application logs were clean. Installed `mcp==1.30.0` transport source uses `json.loads` then `JSONRPCMessage.model_validate`, returning codes `-32700` (parse) and `-32602` (envelope validation), with ID `server-error`.
- Repair: prevalidate only `/mcp` POST envelopes behind the SDK's `RequestBodyLimitMiddleware(65536)`, using the same SDK model. Return constant errors for parse/encoding/recursion and envelope validation failures; replay accepted bytes unchanged. Do not rewrite ordinary JSON-RPC errors or buffer responses. Preserve SDK-accepted notifications/responses, including its permissive union behavior. Allowlisted telemetry also checks that a method is a string, since accepted response extras can contain non-string methods.
- Regression evidence: the initial new HTTP cases produced 10 failures/4 passes (including one incorrectly assumed invalid ID that the SDK accepts as a notification); the repaired focused run passed 16 checks. Additional compatibility checks passed 12/12, including real SSE SDK calls, 202/empty notification and response acknowledgements, exact 64 KiB acceptance, declared/chunked overflow 413, and SDK 400/406/415 header errors. Every malformed-envelope/parse case asserts no sentinel in HTTP output, application logs, or captured stdout/stderr. Non-JSON Content-Type is rejected by SDK transport security with 400 before its inner 415 check.
- Reproduce without installing: `PYTHONPATH=. .venv/bin/pytest -q` -> **52 passed in 13.26s**. Direct pytest needs `PYTHONPATH=.` for this repository (the documented `python -m pytest` invocation supplies the import path itself). Local listener shutdown assertions passed. Inbound upload deadlines/concurrency and mutable base/unhashed uv bootstrap remain separate exposure/container gates. Independent retest/security review and Architect acceptance remain required.
- Final telemetry follow-up: two exception-propagating ASGI regressions reproduced a post-response `RecursionError` at `json.loads(captured)` for 12,000 nested arrays, both top-level and inside `params`, below 64 KiB. Catching `RecursionError` in that telemetry-only handler preserves the constant 400/code `-32700` and emits correlated `http_complete` metadata (`method=other`, `status=400`), without changing the SDK envelope boundary. `PYTHONPATH=. .venv/bin/pytest -q tests/test_lab_mcp.py -k deep_nested_json_completes_asgi` -> **2 failed before / 2 passed after**; `PYTHONPATH=. .venv/bin/pytest -q` -> **54 passed in 13.12s**, including listener cleanup assertions. Developer local repair evidence only, not independent acceptance; no dependencies installed or external network/cloud operations performed.
