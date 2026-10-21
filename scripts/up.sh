#!/usr/bin/env bash
# Create or update the lab: resource group, AKS, CPU pools, optional GPU pool.
# Usage: [DEPLOY_GPU_POOL=true] scripts/up.sh [--validate-only]
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/env.sh
require az

mode="deploy"
[ "${1:-}" = "--validate-only" ] && mode="validate"

echo "Resource group: $RESOURCE_GROUP  Location: $LOCATION  Cluster: $CLUSTER_NAME  GPU pool: $DEPLOY_GPU_POOL ($GPU_VM_SIZE, spot=$GPU_SPOT)"

az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --tags project=k8s-agent-gateway -o none

params=(clusterName="$CLUSTER_NAME" deployGpuPool="$DEPLOY_GPU_POOL" gpuVmSize="$GPU_VM_SIZE" gpuSpot="$GPU_SPOT")

if [ "$mode" = "validate" ]; then
  az deployment group validate -g "$RESOURCE_GROUP" -f infra/main.bicep -p "${params[@]}" -o none
  echo "Validation passed (nothing deployed)."
  exit 0
fi

az deployment group create -g "$RESOURCE_GROUP" -f infra/main.bicep -p "${params[@]}" -o none
echo "Deployed. Fetch credentials with: az aks get-credentials -g $RESOURCE_GROUP -n $CLUSTER_NAME"
