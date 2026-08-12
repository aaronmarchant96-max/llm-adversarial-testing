"""PromptHound Red Team Lab core package."""

from .io import (
    append_jsonl,
    load_attack_templates,
    load_defects,
    load_evaluation_results,
    load_review_decisions,
    load_test_runs,
    read_jsonl,
    save_attack_template,
    save_defect,
    save_evaluation_result,
    save_review_decision,
    save_test_run,
    write_jsonl,
)
from .report import export_report_bundle, render_markdown, summarize_runs
from .schemas import (
    AttackTemplate,
    Defect,
    EvaluationResult,
    ModelTarget,
    ReportSummary,
    ReviewDecision,
    TestRun,
    TokenCount,
    compute_quadrant,
)
