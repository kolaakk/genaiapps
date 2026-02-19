from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=20, description="User-provided text to analyze")
    context: Optional[str] = Field(default=None, description="Optional context (system name, country, etc.)")


RiskLevel = Literal["low", "medium", "high"]


class ControlAction(BaseModel):
    control_area: str
    why: str


class ActionItem(BaseModel):
    title: str
    owner_role: str
    due_in_days: int = Field(ge=1, le=90)


class LLMAnalysis(BaseModel):
    title: str
    summary: str
    risk_level: RiskLevel
    impacted_domains: List[str]
    sensitive_data_involved: bool
    key_risks: List[str]
    recommended_controls: List[ControlAction]
    action_items: List[ActionItem]
    assumptions: List[str]


class PolicyMatch(BaseModel):
    policy_id: str
    title: str
    score: float
    excerpt: str


class AnalyzeResponse(BaseModel):
    analysis: LLMAnalysis
    related_policies: List[PolicyMatch]
    request_id: str