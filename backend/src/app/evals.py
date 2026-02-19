from typing import Dict, Any


def basic_quality_checks(result: Dict[str, Any]) -> list[str]:
    issues = []
    if len(result.get("summary", "")) < 40:
        issues.append("Summary too short")
    if result.get("risk_level") not in {"low", "medium", "high"}:
        issues.append("Invalid risk_level")
    if not result.get("recommended_controls"):
        issues.append("No recommended_controls")
    return issues