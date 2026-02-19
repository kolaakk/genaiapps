import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any

from .openai_client import get_llm_clients

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "policies.json"


def load_policies() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def embed_text(text: str) -> np.ndarray:
    llm = get_llm_clients()
    resp = llm.embed_client.embeddings.create(
        model=llm.embed_id,  # deployment (azure) OR model (openai)
        input=text,
    )
    vec = resp.data[0].embedding
    return np.array(vec, dtype=np.float32)


def rank_related_policies(user_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
    policies = load_policies()
    user_vec = embed_text(user_text)

    scored = []
    for p in policies:
        p_vec = embed_text(p["text_for_embedding"])
        score = cosine_similarity(user_vec, p_vec)
        scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    out = []
    for score, p in scored[:top_k]:
        out.append({
            "policy_id": p["policy_id"],
            "title": p["title"],
            "score": round(float(score), 4),
            "excerpt": p["excerpt"],
        })
    return out