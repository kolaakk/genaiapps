#!/usr/bin/env bash
set -euo pipefail

# Required env vars:
#   RG, LOCATION, NAME_PREFIX, ACR_NAME
#   OPENAI_API_KEY, APP_API_KEY
# Optional:
#   OPENAI_ENDPOINT

OPENAI_ENDPOINT="${OPENAI_ENDPOINT:-https://open-ai-resource-rob.openai.azure.com}"

ACR_LOGIN_SERVER=$(az acr show -n "$ACR_NAME" --query loginServer -o tsv)
BACKEND_IMAGE="$ACR_LOGIN_SERVER/policy-backend:1.0.0"
FRONTEND_IMAGE="$ACR_LOGIN_SERVER/policy-frontend:1.0.0"

echo "Deploying Bicep..."
az deployment group create \
  -g "$RG" \
  -f ../bicep/main.bicep \
  -p location="$LOCATION" \
  -p namePrefix="$NAME_PREFIX" \
  -p openaiApiKey="$OPENAI_API_KEY" \
  -p openaiEndpoint="$OPENAI_ENDPOINT" \
  -p appApiKey="$APP_API_KEY" \
  -p backendImage="$BACKEND_IMAGE" \
  -p frontendImage="$FRONTEND_IMAGE" \
  -o table