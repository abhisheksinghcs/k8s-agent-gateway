#!/usr/bin/env bash
# Read-only Azure prerequisite check for the GPU SKU. Changes nothing.
# Usage: [LOCATION=southeastasia] ./scripts/preflight.sh
set -euo pipefail

LOCATION="${LOCATION:-southeastasia}"
GPU_SKU="${GPU_SKU:-Standard_NC72ds_xl_RTXPRO6000BSE_v6}"
# vCPUs the GPU pool needs at its maximum node count (1 node of NC72 = 72).
NEEDED_VCPUS="${NEEDED_VCPUS:-72}"
# Extra vCPUs for the system/app pools.
CPU_POOL_VCPUS="${CPU_POOL_VCPUS:-8}"

for t in az jq kubectl helm; do
  command -v "$t" >/dev/null || { echo "MISSING tool: $t" >&2; exit 1; }
done

az account show >/dev/null 2>&1 || { echo "Not logged in: run 'az login'" >&2; exit 1; }
echo "Subscription: $(az account show --query name -o tsv) (state: $(az account show --query state -o tsv))"
echo "Location:     $LOCATION"
echo "GPU SKU:      $GPU_SKU"
echo

echo "--- SKU availability / restrictions in $LOCATION"
sku_json="$(az vm list-skus --location "$LOCATION" --size "$GPU_SKU" --resource-type virtualMachines -o json)"
if [ "$(jq length <<<"$sku_json")" -eq 0 ]; then
  echo "FAIL: SKU not offered in $LOCATION"; sku_ok=0
else
  jq -r '.[] | "zones=\((.locationInfo[0].zones // []) | join(","))  restrictions=\(.restrictions | map(.reasonCode) | join(",") | if .=="" then "none" else . end)"' <<<"$sku_json"
  sku_ok=1
fi
family="$(jq -r '.[0].family // empty' <<<"$sku_json")"

echo
echo "--- vCPU quota in $LOCATION"
usage="$(az vm list-usage -l "$LOCATION" -o json)"
total_line="$(jq -r '.[] | select(.name.value=="cores") | "\(.currentValue) \(.limit)"' <<<"$usage")"
read -r total_used total_limit <<<"$total_line"
echo "regional total vCPUs: ${total_used}/${total_limit}"
quota_ok=1
if [ -n "$family" ]; then
  read -r fam_used fam_limit <<<"$(jq -r --arg f "$family" '.[] | select(.name.value==$f) | "\(.currentValue) \(.limit)"' <<<"$usage")"
  echo "family $family: ${fam_used}/${fam_limit}"
  [ $((fam_limit - fam_used)) -ge "$NEEDED_VCPUS" ] || { echo "FAIL: family quota < $NEEDED_VCPUS vCPUs"; quota_ok=0; }
fi
[ $((total_limit - total_used)) -ge $((NEEDED_VCPUS + CPU_POOL_VCPUS)) ] || { echo "FAIL: regional total quota headroom < $((NEEDED_VCPUS + CPU_POOL_VCPUS)) vCPUs"; quota_ok=0; }

echo
echo "--- AKS CLI prerequisites (managed GPU preview)"
az extension show --name aks-preview --query version -o tsv 2>/dev/null | sed 's/^/aks-preview: /' || echo "aks-preview: NOT INSTALLED"
echo "ManagedGPUExperiencePreview: $(az feature show --namespace Microsoft.ContainerService --name ManagedGPUExperiencePreview --query properties.state -o tsv 2>/dev/null || echo unknown)"
echo "Microsoft.ContainerService provider: $(az provider show -n Microsoft.ContainerService --query registrationState -o tsv)"

echo
if [ "$sku_ok" = 1 ] && [ "$quota_ok" = 1 ]; then echo "RESULT: prerequisites satisfied"; else echo "RESULT: BLOCKED (see FAIL lines)"; exit 2; fi
