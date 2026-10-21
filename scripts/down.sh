#!/usr/bin/env bash
# Delete the whole lab resource group (destructive; asks for confirmation).
# Usage: scripts/down.sh [--yes]
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/env.sh
require az

if ! az group exists -n "$RESOURCE_GROUP" | grep -q true; then
  echo "Resource group $RESOURCE_GROUP does not exist; nothing to do."
  exit 0
fi

echo "This will DELETE resource group '$RESOURCE_GROUP' and everything in it:"
az resource list -g "$RESOURCE_GROUP" --query "[].{name:name,type:type}" -o table

if [ "${1:-}" != "--yes" ]; then
  read -r -p "Type the resource group name to confirm: " answer
  [ "$answer" = "$RESOURCE_GROUP" ] || { echo "Aborted."; exit 1; }
fi

az group delete -n "$RESOURCE_GROUP" --yes --no-wait
echo "Deletion started (async). Check: az group exists -n $RESOURCE_GROUP"
