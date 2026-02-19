param location string = resourceGroup().location
param namePrefix string = 'genai'
param acrName string = '${namePrefix}acr${uniqueString(resourceGroup().id)}'

@secure()
param openaiApiKey string
param openaiEndpoint string = 'https://open-ai-resource-rob.openai.azure.com'
param chatDeployment string = 'gpt-4o-mini'
param embedDeployment string = 'text-embedding-3-large'
param apiVersionChat string = '2024-08-01-preview'
param apiVersionEmbed string = '2023-05-15'

param appApiKey string = 'change-me'

param backendImage string
param frontendImage string

module acr './modules/acr.bicep' = {
  name: 'acr'
  params: {
    acrName: acrName
    location: location
  }
}

module ca './modules/containerApps.bicep' = {
  name: 'containerApps'
  params: {
    location: location
    namePrefix: namePrefix
    acrLoginServer: acr.outputs.loginServer
    backendImage: backendImage
    frontendImage: frontendImage
    openaiApiKey: openaiApiKey
    openaiEndpoint: openaiEndpoint
    chatDeployment: chatDeployment
    embedDeployment: embedDeployment
    apiVersionChat: apiVersionChat
    apiVersionEmbed: apiVersionEmbed
    appApiKey: appApiKey
  }
}

output frontendUrl string = ca.outputs.frontendUrl
output backendUrl string = ca.outputs.backendUrl