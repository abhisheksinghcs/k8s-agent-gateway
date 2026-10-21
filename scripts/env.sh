#!/usr/bin/env bash
# Shared defaults. Override by exporting variables before running a script.
export LOCATION="${LOCATION:-southeastasia}"
export RESOURCE_GROUP="${RESOURCE_GROUP:-rg-aks-agw-lab}"
export CLUSTER_NAME="${CLUSTER_NAME:-aks-agw-lab}"
# Set DEPLOY_GPU_POOL=true only after GPU quota exists (see STATUS.md).
export DEPLOY_GPU_POOL="${DEPLOY_GPU_POOL:-false}"
export GPU_VM_SIZE="${GPU_VM_SIZE:-Standard_NC72ds_xl_RTXPRO6000BSE_v6}"
# true = Spot GPU pool (separate quota pool, evictable); see docs/decisions.md D-008.
export GPU_SPOT="${GPU_SPOT:-false}"

require() {
  for t in "$@"; do command -v "$t" >/dev/null || { echo "MISSING tool: $t" >&2; exit 1; }; done
  az account show >/dev/null 2>&1 || { echo "Not logged in: run 'az login'" >&2; exit 1; }
}
