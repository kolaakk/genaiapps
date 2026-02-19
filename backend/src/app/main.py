from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import TypeAdapter
from typing import Any, Dict

from .settings import settings
from .schemas import AnalyzeRequest, AnalyzeResponse, LLMAnalysis, PolicyMatch
from .security import require_api_key
from .utils import new_request_id, clamp_text
#from .openai_client import get_chat_client
from .policy_store import rank_related_policies
from .evals import basic_quality_checks
from .openai_client import get_llm_clients


app = FastAPI(title="GenAI Policy Impact Analyzer", version="0.1.0")

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "env": settings.app_env}


SYSTEM_PROMPT = """You are a banking technology risk & compliance analyst.
Your job: analyze the provided text and return a STRICT JSON object that matches the schema.

Rules:
- Output MUST be valid JSON only (no markdown).
- Be conservative and bank-grade.
- If sensitive data (PII, account info, auth secrets) is present or implied, set sensitive_data_involved=true.
- Use risk_level: low|medium|high.
- Provide actionable controls and action items.

Schema (keys and types must match):
{
  "title": string,
  "summary": string,
  "risk_level": "low"|"medium"|"high",
  "impacted_domains": [string],
  "sensitive_data_involved": boolean,
  "key_risks": [string],
  "recommended_controls": [{"control_area": string, "why": string}],
  "action_items": [{"title": string, "owner_role": string, "due_in_days": number}],
  "assumptions": [string]
}
"""


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest, _auth: Any = Depends(require_api_key)) -> AnalyzeResponse:
    request_id = new_request_id()

    text = clamp_text(req.text, settings.max_input_chars)
    context = (req.context or "").strip()

    user_prompt = f"""Context (optional):
{context if context else "(none)"}

Text to analyze:
{text}
"""

    try:
        llm = get_llm_clients()
        resp = llm.chat_client.chat.completions.create(
        model=llm.chat_id,  # deployment (azure) OR model (openai)
        temperature=0.2,
        messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ],
    # Works on Azure per your assignment. On standard OpenAI, many models support it too.
    response_format={"type": "json_object"},
)
        content = resp.choices[0].message.content
        if not content:
            raise HTTPException(status_code=502, detail="Empty response from LLM")

        # Validate strict JSON into our Pydantic model
        adapter = TypeAdapter(LLMAnalysis)
        analysis = adapter.validate_json(content)

        # Basic sanity checks (useful for interview: quality gating)
        issues = basic_quality_checks(analysis.model_dump())
        if issues:
            # Not failing the request; but you could. We include as assumptions note.
            analysis.assumptions.extend([f"QualityCheck: {i}" for i in issues])

        # Embedding-based policy recommendations
        related = rank_related_policies(text, top_k=5)
        related_models = [PolicyMatch(**p) for p in related]

        return AnalyzeResponse(
            analysis=analysis,
            related_policies=related_models,
            request_id=request_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analyze failed: {type(e).__name__}: {e}")