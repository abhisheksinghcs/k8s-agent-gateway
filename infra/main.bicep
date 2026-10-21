// AKS lab cluster: system pool, CPU app pool, optional tainted GPU pool.
// Scope: resource group (created by scripts/up.sh). Teardown = delete the resource group.
targetScope = 'resourceGroup'

param clusterName string = 'aks-agw-lab'
param location string = resourceGroup().location

@description('Major.minor; AKS selects the latest patch.')
param kubernetesVersion string = '1.36'

param systemVmSize string = 'Standard_D2s_v5'
param appVmSize string = 'Standard_D4s_v5'
param appNodeCount int = 1

@description('Create the GPU pool. Leave false until GPU quota exists (Phase 3).')
param deployGpuPool bool = false
param gpuVmSize string = 'Standard_NC72ds_xl_RTXPRO6000BSE_v6'
param gpuNodeCount int = 1
@description('Run the GPU pool on Spot VMs. Spot uses a separate regional quota pool and can be evicted (D-008).')
param gpuSpot bool = false
@description('This SKU is offered in zone 1 only in southeastasia.')
param gpuZones array = ['1']

@description('CIDRs allowed to reach the API server. Empty = unrestricted (lab default, see docs/decisions.md D-007).')
param apiServerAuthorizedIpRanges array = []

var gpuTaint = 'sku=gpu:NoSchedule'

resource aks 'Microsoft.ContainerService/managedClusters@2025-05-01' = {
  name: clusterName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    dnsPrefix: clusterName
    kubernetesVersion: kubernetesVersion
    agentPoolProfiles: [
      {
        name: 'system'
        mode: 'System'
        vmSize: systemVmSize
        count: 1
        osType: 'Linux'
        nodeTaints: ['CriticalAddonsOnly=true:NoSchedule']
      }
      {
        name: 'app'
        mode: 'User'
        vmSize: appVmSize
        count: appNodeCount
        osType: 'Linux'
        nodeLabels: {
          workload: 'app'
        }
      }
    ]
    networkProfile: {
      networkPlugin: 'azure'
      networkPluginMode: 'overlay'
    }
    apiServerAccessProfile: empty(apiServerAuthorizedIpRanges) ? null : {
      authorizedIPRanges: apiServerAuthorizedIpRanges
    }
  }
}

resource gpuPool 'Microsoft.ContainerService/managedClusters/agentPools@2025-05-01' = if (deployGpuPool) {
  parent: aks
  name: 'gpunp'
  properties: {
    mode: 'User'
    vmSize: gpuVmSize
    count: gpuNodeCount
    osType: 'Linux'
    availabilityZones: gpuZones
    // Default is a ~2 TB ephemeral OS disk whose resize outlasts the node bootstrap timeout (docs/troubleshooting.md T-006).
    osDiskType: 'Managed'
    osDiskSizeGB: 128
    scaleSetPriority: gpuSpot ? 'Spot' : 'Regular'
    scaleSetEvictionPolicy: gpuSpot ? 'Delete' : null
    spotMaxPrice: gpuSpot ? -1 : null
    enableAutoScaling: gpuSpot
    minCount: gpuSpot ? gpuNodeCount : null
    maxCount: gpuSpot ? gpuNodeCount : null
    nodeTaints: [gpuTaint]
    nodeLabels: {
      workload: 'gpu-inference'
    }
  }
}

output clusterName string = aks.name
output gpuPoolDeployed bool = deployGpuPool
