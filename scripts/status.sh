#!/usr/bin/env bash
# Read-only status of the lab (Azure side and Kubernetes side).
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/env.sh
require az

echo "--- Azure"
az aks show -g "$RESOURCE_GROUP" -n "$CLUSTER_NAME" \
  --query "{state:provisioningState,power:powerState.code,k8s:kubernetesVersion}" -o table 2>&1 || echo "cluster not found"
az aks nodepool list -g "$RESOURCE_GROUP" --cluster-name "$CLUSTER_NAME" \
  --query "[].{pool:name,vm:vmSize,count:count,state:provisioningState,taints:nodeTaints}" -o table 2>&1 || true

if command -v kubectl >/dev/null && kubectl get nodes >/dev/null 2>&1; then
  echo; echo "--- Kubernetes"
  kubectl get nodes -L agentpool,workload
  kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded 2>/dev/null || true
fi
