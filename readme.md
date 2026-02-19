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

# 🏗 Architecture Overview

Frontend (React + Vite)
        ↓ REST
Backend (FastAPI)
        ↓
Azure OpenAI:
   - gpt-4o-mini (analysis)
   - text-embedding-3-large (policy similarity)

Backend is stateless and horizontally scalable.

genaiapps/
├─ README.md
├─ .gitignore
├─ .env.example
├─ infra/
│  ├─ bicep/
│  │  ├─ main.bicep
│  │  ├─ main.parameters.json
│  │  └─ modules/
│  │     ├─ containerApps.bicep
│  │     └─ acr.bicep
│  └─ scripts/
│     ├─ deploy.sh
│     └─ build_push.sh
├─ backend/
│  ├─ Dockerfile
│  ├─ pyproject.toml
│  ├─ src/
│  │  ├─ app/
│  │  │  ├─ main.py
│  │  │  ├─ settings.py
│  │  │  ├─ schemas.py
│  │  │  ├─ security.py
│  │  │  ├─ openai_client.py
│  │  │  ├─ policy_store.py
│  │  │  ├─ evals.py
│  │  │  └─ utils.py
│  │  └─ data/
│  │     └─ policies.json
│  └─ tests/
│     └─ test_health.py
└─ frontend/
   ├─ Dockerfile
   ├─ nginx.conf
   ├─ package.json
   ├─ tsconfig.json
   ├─ vite.config.ts
   ├─ index.html
   └─ src/
      ├─ main.tsx
      ├─ App.tsx
      ├─ api.ts
      └─ styles.css
