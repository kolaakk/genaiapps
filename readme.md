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