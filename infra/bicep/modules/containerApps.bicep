param location string
param namePrefix string
param acrLoginServer string

@secure()
param openaiApiKey string
param openaiEndpoint string
param chatDeployment string
param embedDeployment string
param apiVersionChat string
param apiVersionEmbed string
param appApiKey string

param backendImage string
param frontendImage string

resource env 'Microsoft.App/managedEnvironments@2023-11-02-preview' = {
  name: '${namePrefix}-env'
  location: location
  properties: {}
}

resource backend 'Microsoft.App/containerApps@2023-11-02-preview' = {
  name: '${namePrefix}-backend'
  location: location
  properties: {
    managedEnvironmentId: env.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
        transport: 'auto'
      }
      secrets: [
        { name: 'openai-api-key', value: openaiApiKey }
        { name: 'app-api-key', value: appApiKey }
      ]
    }
    template: {
      containers: [
        {
          name: 'backend'
          image: backendImage
          env: [
            { name: 'AZURE_OPENAI_ENDPOINT', value: openaiEndpoint }
            { name: 'AZURE_OPENAI_API_KEY', secretRef: 'openai-api-key' }
            { name: 'AZURE_OPENAI_CHAT_DEPLOYMENT', value: chatDeployment }
            { name: 'AZURE_OPENAI_EMBED_DEPLOYMENT', value: embedDeployment }
            { name: 'AZURE_OPENAI_API_VERSION_CHAT', value: apiVersionChat }
            { name: 'AZURE_OPENAI_API_VERSION_EMBED', value: apiVersionEmbed }
            { name: 'APP_API_KEY', secretRef: 'app-api-key' }
            { name: 'CORS_ORIGINS', value: '*' }
            { name: 'APP_ENV', value: 'azure' }
          ]
          resources: {
            cpu: 0.5
            memory: '1Gi'
          }
        }
      ]
      scale: { minReplicas: 1, maxReplicas: 3 }
    }
  }
}

resource frontend 'Microsoft.App/containerApps@2023-11-02-preview' = {
  name: '${namePrefix}-frontend'
  location: location
  properties: {
    managedEnvironmentId: env.id
    configuration: {
      ingress: {
        external: true
        targetPort: 80
        transport: 'auto'
      }
    }
    template: {
      containers: [
        {
          name: 'frontend'
          image: frontendImage
          resources: {
            cpu: 0.25
            memory: '0.5Gi'
          }
        }
      ]
      scale: { minReplicas: 1, maxReplicas: 2 }
    }
  }
}

output backendUrl string = 'https://${backend.properties.configuration.ingress.fqdn}'
output frontendUrl string = 'https://${frontend.properties.configuration.ingress.fqdn}'