"""Data models for contract audit system."""
from typing import List, Optional, Literal
from pydantic import BaseModel


class RuleResult(BaseModel):
    rule_id: str
    title: str
    severity: Literal["required", "recommended"]
    status: Literal["present", "insufficient", "missing"]
    evidence: Optional[str] = None
    suggestion: str
    redline_action: Optional[Literal["add", "replace"]] = None


class AuditResult(BaseModel):
    total_rules: int
    required_violations: int
    recommended_violations: int
    rule_results: List[RuleResult]