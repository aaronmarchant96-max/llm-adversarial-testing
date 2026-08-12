"""JSONL helpers for PromptHound Red Team Lab."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, TypeVar

from .schemas import AttackTemplate, Defect, EvaluationResult, ReviewDecision, TestRun

T = TypeVar("T")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_jsonl(path: str | Path, rows: Iterable[dict]) -> None:
    path = Path(path)
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def append_jsonl(path: str | Path, row: dict) -> None:
    path = Path(path)
    ensure_parent(path)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
        handle.write("\n")


def read_jsonl(path: str | Path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []

    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def dump_model(path: str | Path, model) -> None:
    append_jsonl(path, model.model_dump(mode="json"))


def load_attack_templates(path: str | Path) -> list[AttackTemplate]:
    return [AttackTemplate.model_validate(row) for row in read_jsonl(path)]


def load_test_runs(path: str | Path) -> list[TestRun]:
    return [TestRun.model_validate(row) for row in read_jsonl(path)]


def load_review_decisions(path: str | Path) -> list[ReviewDecision]:
    return [ReviewDecision.model_validate(row) for row in read_jsonl(path)]


def load_defects(path: str | Path) -> list[Defect]:
    return [Defect.model_validate(row) for row in read_jsonl(path)]


def load_evaluation_results(path: str | Path) -> list[EvaluationResult]:
    return [EvaluationResult.model_validate(row) for row in read_jsonl(path)]


def save_attack_template(path: str | Path, template: AttackTemplate) -> None:
    dump_model(path, template)


def save_test_run(path: str | Path, test_run: TestRun) -> None:
    dump_model(path, test_run)


def save_review_decision(path: str | Path, decision: ReviewDecision) -> None:
    dump_model(path, decision)


def save_defect(path: str | Path, defect: Defect) -> None:
    dump_model(path, defect)


def save_evaluation_result(path: str | Path, result: EvaluationResult) -> None:
    dump_model(path, result)
