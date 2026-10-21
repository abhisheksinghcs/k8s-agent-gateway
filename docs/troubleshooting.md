# Troubleshooting

Entries are observation, hypothesis, test, result.

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
