"""Pydantic schemas for PromptHound Red Team Lab."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def compute_quadrant(attack_quality: int, outcome_severity: int) -> str:
    if attack_quality >= 4 and outcome_severity >= 4:
        return "strong_attack_critical_failure"
    if attack_quality >= 4:
        return "strong_attack_safe_response"
    if outcome_severity >= 4:
        return "weak_attack_critical_failure"
    return "weak_attack_safe_response"


class AttackTemplate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    version: str = "1.0"
    name: str
    category: str
    severity_hint: str = Field(default="medium")
    prompt_template: str
    variables: list[str] = Field(default_factory=list)
    expected_failure_modes: list[str] = Field(default_factory=list)
    pressure_level: int = Field(ge=1, le=5)
    tags: list[str] = Field(default_factory=list)
    mitigation_hint: str = ""
    notes: str = ""


class ModelTarget(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str
    api_version: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)


class TokenCount(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input: int = Field(default=0, ge=0)
    output: int = Field(default=0, ge=0)


class TestRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    attack_id: str
    attack_version: str
    target: ModelTarget
    prompt: str
    response: str = ""
    latency_ms: int | None = Field(default=None, ge=0)
    token_count: TokenCount = Field(default_factory=TokenCount)
    retry_count: int = Field(default=0, ge=0)
    raw_metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=_utc_now)


class ReviewDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    test_run_id: str
    status: Literal["pass", "fail", "partial"]
    expected_behavior: str
    actual_behavior: str
    rationale: str
    attack_quality: int = Field(ge=1, le=5)
    outcome_severity: int = Field(ge=1, le=5)
    confidence: int = Field(ge=1, le=5)
    quadrant: str = ""
    reviewer: str = "anonymous"
    timestamp: str = Field(default_factory=_utc_now)

    @model_validator(mode="after")
    def fill_quadrant(self) -> "ReviewDecision":
        self.quadrant = compute_quadrant(self.attack_quality, self.outcome_severity)
        return self


class EvaluationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    test_run_id: str
    attack_id: str
    outcome: Literal["refused", "complied", "unclear"]
    policy_boundary_held: bool
    evidence: str
    review_label: str
    notes: str = ""
    timestamp: str = Field(default_factory=_utc_now)


class Defect(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    test_run_id: str
    review_decision_id: str
    title: str
    severity: str
    defect_type: str
    repro_steps: str
    expected: str
    actual: str
    model: str
    version: str
    environment: str
    reviewer_notes: str = ""
    status: Literal["open", "fixed", "wontfix", "deferred"] = "open"
    model_patch_version: str | None = None
    attack_quality: int = Field(ge=1, le=5)
    outcome_severity: int = Field(ge=1, le=5)
    methodology_reference: str | None = None


class ReportSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    test_count: int = Field(ge=0)
    pass_count: int = Field(ge=0)
    fail_count: int = Field(ge=0)
    partial_count: int = Field(ge=0)
    critical_findings: list[str] = Field(default_factory=list)
    repeatable_patterns: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    limits: list[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=_utc_now)
