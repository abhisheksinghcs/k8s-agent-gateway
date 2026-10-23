targetScope = 'resourceGroup'

@description('Dedicated lab registry; globally unique alphanumeric name.')
@minLength(5)
@maxLength(50)
param registryName string

param location string = resourceGroup().location

@description('Existing AKS kubelet identity object ID, refreshed from identityProfile before deployment.')
param kubeletPrincipalId string

var acrPullRoleId = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')

resource registry 'Microsoft.ContainerRegistry/registries@2025-11-01' = {
  name: registryName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
    anonymousPullEnabled: false
    publicNetworkAccess: 'Enabled'
    roleAssignmentMode: 'LegacyRegistryPermissions'
  }
}

resource kubeletPull 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(registry.id, kubeletPrincipalId, acrPullRoleId)
  scope: registry
  properties: {
    roleDefinitionId: acrPullRoleId
    principalId: kubeletPrincipalId
    principalType: 'ServicePrincipal'
  }
}

output registryId string = registry.id
output loginServer string = registry.properties.loginServer