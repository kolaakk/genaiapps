# genai-policy-impact-analyzer
# GenAI Policy Impact Analyzer (Backend + Frontend)

A GenAI application that analyzes a text (change request / incident / procedure),
produces structured risk & control output via Azure OpenAI GPT-4o-mini, and recommends related
policies using embeddings + cosine similarity.

## Features
- REST API (FastAPI)
- Calls Azure OpenAI Chat Completions (GPT-4o-mini) for structured JSON output
- Calls Azure OpenAI Embeddings (text-embedding-3-large) to recommend policies
- Basic API key auth (X-API-Key)
- CORS configured for frontend
- Containerized frontend + backend
- Azure Container Apps deployment (Bicep)

## Local Run (Docker Compose style with 2 containers)
1) Create env files:
- copy `.env.example` to `.env` (root) for your reference
- set env vars in your shell or in Azure Container Apps

2) Backend:
```bash
cd backend
docker build -t policy-backend:local .
docker run --rm -p 8000:8000 \
  -e AZURE_OPENAI_ENDPOINT="https://open-ai-resource-rob.openai.azure.com" \
  -e AZURE_OPENAI_API_KEY="(from KeyVault: open-ai-keys-rob / open-ai-key-rob)" \
  -e AZURE_OPENAI_CHAT_DEPLOYMENT="gpt-4o-mini" \
  -e AZURE_OPENAI_EMBED_DEPLOYMENT="text-embedding-3-large" \
  -e AZURE_OPENAI_API_VERSION_CHAT="2024-08-01-preview" \
  -e AZURE_OPENAI_API_VERSION_EMBED="2023-05-15" \
  -e APP_API_KEY="local-dev-key" \
  policy-backend:local

cd frontend
docker build -t policy-frontend:local .
docker run --rm -p 3000:80 \
  -e VITE_API_BASE_URL="http://localhost:8000" \
  -e VITE_APP_API_KEY="local-dev-key" \
  policy-frontend:local

  
