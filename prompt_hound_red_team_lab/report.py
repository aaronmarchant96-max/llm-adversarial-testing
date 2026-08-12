"""Report rendering for PromptHound Red Team Lab."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from .schemas import Defect, EvaluationResult, ReportSummary, ReviewDecision, TestRun


@dataclass(frozen=True)
class ReportBundle:
    summary: ReportSummary
    markdown: str
    evidence_dir: Path


def summarize_runs(
    runs: list[TestRun],
    decisions: list[ReviewDecision],
    defects: list[Defect],
    evaluations: list[EvaluationResult] | None = None,
) -> ReportSummary:
    evaluations = evaluations or []
    pass_count = sum(1 for decision in decisions if decision.status == "pass")
    fail_count = sum(1 for decision in decisions if decision.status == "fail")
    partial_count = sum(1 for decision in decisions if decision.status == "partial")

    critical_findings: list[str] = []
    repeatable_patterns: list[str] = []
    recommendations: list[str] = []
    limits = [
        f"Sample size: {len(runs)} runs.",
        "This report documents current behavior. It does not prove safety.",
    ]

    if defects:
        critical_findings.extend(
            f"{defect.severity.title()} {defect.defect_type}: {defect.title}"
            for defect in defects
        )

    if any(decision.quadrant == "strong_attack_critical_failure" for decision in decisions):
        repeatable_patterns.append("At least one strong attack produced a critical failure.")
        recommendations.append("Review the attack path and add a guardrail or output check where it failed.")

    if any(decision.status == "fail" for decision in decisions):
        recommendations.append("Keep the failing cases in the evidence pack and rerun them after any fix.")

    if evaluations:
        safe_refusals = sum(1 for result in evaluations if result.review_label == "safe_refusal")
        if safe_refusals:
            recommendations.append("Keep the refusal cases around as regression checks.")

    if not recommendations:
        recommendations.append("No clear failure pattern surfaced in this slice. Keep collecting evidence.")

    return ReportSummary(
        test_count=len(runs),
        pass_count=pass_count,
        fail_count=fail_count,
        partial_count=partial_count,
        critical_findings=critical_findings,
        repeatable_patterns=repeatable_patterns,
        recommendations=recommendations,
        limits=limits,
    )


def render_markdown(
    runs: list[TestRun],
    decisions: list[ReviewDecision],
    defects: list[Defect],
    summary: ReportSummary,
    evaluations: list[EvaluationResult] | None = None,
    title: str = "PromptHound Red Team Lab Report",
) -> str:
    evaluations = evaluations or []
    model_line = "Unknown"
    if runs:
        first = runs[0]
        model_line = f"{first.target.provider}/{first.target.model}"

    decision_lookup = {decision.test_run_id: decision for decision in decisions}

    lines: list[str] = [
        f"# {title}",
        "",
        f"Generated: {summary.generated_at}",
        f"Target: {model_line}",
        "",
        "## Summary",
        "",
        f"- Runs: {summary.test_count}",
        f"- Pass: {summary.pass_count}",
        f"- Fail: {summary.fail_count}",
        f"- Partial: {summary.partial_count}",
        "",
        "## Dual-Axis Matrix",
        "",
        "| Attack quality | Outcome severity | Count |",
        "| --- | --- | --- |",
    ]

    buckets = {
        "weak_attack_safe_response": 0,
        "weak_attack_critical_failure": 0,
        "strong_attack_safe_response": 0,
        "strong_attack_critical_failure": 0,
    }
    for decision in decisions:
        buckets[decision.quadrant] = buckets.get(decision.quadrant, 0) + 1

    for quadrant, count in buckets.items():
        if quadrant.startswith("strong"):
            attack_quality = "strong"
        else:
            attack_quality = "weak"
        if quadrant.endswith("critical_failure"):
            outcome = "critical"
        else:
            outcome = "safe"
        lines.append(f"| {attack_quality} | {outcome} | {count} |")

    lines += [
        "",
        "## Findings",
        "",
    ]

    if summary.critical_findings:
        for finding in summary.critical_findings:
            lines.append(f"- {finding}")
    else:
        lines.append("- No critical findings in this slice.")

    if evaluations:
        lines += [
            "",
            "## Evaluator Notes",
            "",
        ]
        for result in evaluations:
            boundary_text = "held" if result.policy_boundary_held else "did not hold"
            lines.append(
                f"- {result.attack_id}: {result.review_label} "
                f"({result.outcome}, boundary {boundary_text})"
            )

    lines += [
        "",
        "## Repeatability",
        "",
    ]

    if summary.repeatable_patterns:
        for pattern in summary.repeatable_patterns:
            lines.append(f"- {pattern}")
    else:
        lines.append("- No repeatable pattern was confirmed from this slice alone.")

    lines += [
        "",
        "## Defects",
        "",
    ]

    if defects:
        for defect in defects:
            decision = decision_lookup.get(defect.review_decision_id)
            quadrant = decision.quadrant if decision else "unknown"
            lines.append(
                f"- {defect.title} [{defect.severity}] "
                f"({defect.defect_type}, {quadrant})"
            )
    else:
        lines.append("- No defects were generated.")

    lines += [
        "",
        "## Recommendations",
        "",
    ]

    for recommendation in summary.recommendations:
        lines.append(f"- {recommendation}")

    lines += [
        "",
        "## Limits",
        "",
    ]

    for limit in summary.limits:
        lines.append(f"- {limit}")

    lines += [
        "",
        "## Evidence",
        "",
        "- Raw JSONL files should be kept with the report.",
        "- This report is a summary, not a safety claim.",
        "",
    ]

    return "\n".join(lines).rstrip() + "\n"


def export_report_bundle(
    out_path: Path,
    runs_file: Path,
    decisions_file: Path,
    defects_file: Path,
    evaluations_file: Path | None = None,
) -> ReportBundle:
    from .io import load_defects, load_evaluation_results, load_review_decisions, load_test_runs

    runs = load_test_runs(runs_file)
    decisions = load_review_decisions(decisions_file)
    defects = load_defects(defects_file)
    evaluations = load_evaluation_results(evaluations_file) if evaluations_file else []
    summary = summarize_runs(runs, decisions, defects, evaluations)
    markdown = render_markdown(runs, decisions, defects, summary, evaluations)

    evidence_dir = out_path.parent / f"{out_path.stem}_evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(runs_file, evidence_dir / f"runs_{runs_file.name}")
    shutil.copy2(decisions_file, evidence_dir / f"decisions_{decisions_file.name}")
    if evaluations_file:
        shutil.copy2(evaluations_file, evidence_dir / f"evaluations_{evaluations_file.name}")
    if defects_file.exists():
        shutil.copy2(defects_file, evidence_dir / f"defects_{defects_file.name}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")

    return ReportBundle(summary=summary, markdown=markdown, evidence_dir=evidence_dir)
