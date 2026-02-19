#!/usr/bin/env bash
set -euo pipefail

# Required env vars:
#   ACR_NAME
#   RG
#   LOCATION

ACR_LOGIN_SERVER=$(az acr show -n "$ACR_NAME" --query loginServer -o tsv)

echo "Logging into ACR..."
az acr login -n "$ACR_NAME" >/dev/null

BACKEND_TAG="$ACR_LOGIN_SERVER/policy-backend:1.0.0"
FRONTEND_TAG="$ACR_LOGIN_SERVER/policy-frontend:1.0.0"

echo "Build backend..."
docker build -t "$BACKEND_TAG" ../../backend
docker push "$BACKEND_TAG"

echo "Build frontend..."
docker build -t "$FRONTEND_TAG" ../../frontend
docker push "$FRONTEND_TAG"

echo "BACKEND_IMAGE=$BACKEND_TAG"
echo "FRONTEND_IMAGE=$FRONTEND_TAG"