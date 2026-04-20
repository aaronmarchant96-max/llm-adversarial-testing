#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize arena_eval JSONL logs by run_id."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="JSONL files or glob patterns, e.g. logs/gemma_case002_r*.jsonl",
    )
    return parser.parse_args()


def expand_paths(patterns: list[str]) -> list[Path]:
    seen: set[str] = set()
    out: list[Path] = []

    for pattern in patterns:
        matches = sorted(glob.glob(pattern))
        if not matches and Path(pattern).exists():
            matches = [pattern]

        for match in matches:
            resolved = str(Path(match).resolve())
            if resolved not in seen:
                seen.add(resolved)
                out.append(Path(match))

    return out


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"[warn] {path}:{line_no}: invalid JSON skipped: {exc}", file=sys.stderr)
                continue

            if isinstance(obj, dict):
                rows.append(obj)
            else:
                print(f"[warn] {path}:{line_no}: non-object JSON skipped", file=sys.stderr)

    return rows


def summarize_run(run_id: str, rows: list[dict[str, Any]], sources: set[str]) -> str:
    rows = sorted(rows, key=lambda r: r.get("turn", 0))

    first = rows[0]
    model = first.get("model", "?")
    case_id = first.get("case_id", "?")
    case_title = first.get("case_title", "")
    variant = first.get("variant", "?")
    total_turns = first.get("total_turns", len(rows))

    label_counts: Counter[str] = Counter()
    stable_turns = 0
    elapsed_total = 0.0
    integrity_scores: list[float] = []
    resilience_scores: list[float] = []

    turn_lines: list[str] = []

    for row in rows:
        turn = row.get("turn", "?")
        labels = row.get("labels", [])
        if not isinstance(labels, list):
            labels = [str(labels)]

        label_counts.update(str(x) for x in labels)
        if set(labels) == {"stable"}:
            stable_turns += 1

        elapsed = float(row.get("elapsed_seconds", 0.0) or 0.0)
        elapsed_total += elapsed

        integrity = row.get("integrity_score")
        if isinstance(integrity, (int, float)):
            integrity_scores.append(float(integrity))

        resilience = row.get("resilience_score")
        if isinstance(resilience, (int, float)):
            resilience_scores.append(float(resilience))

        issues = row.get("format_issues", []) or []
        loss = row.get("instruction_loss", []) or []

        extras: list[str] = []
        if issues:
            extras.append("issues=" + ",".join(str(x) for x in issues))
        if loss:
            extras.append("loss=" + ",".join(str(x) for x in loss))

        extra_text = f" | {' | '.join(extras)}" if extras else ""
        turn_lines.append(
            f"  T{turn}/{total_turns}: labels={labels} elapsed={elapsed:.3f}s{extra_text}"
        )

    avg_integrity = sum(integrity_scores) / len(integrity_scores) if integrity_scores else 0.0
    avg_resilience = sum(resilience_scores) / len(resilience_scores) if resilience_scores else 0.0
    label_text = ", ".join(f"{k}={v}" for k, v in sorted(label_counts.items()))
    source_text = ", ".join(sorted(sources))

    return (
        f"{run_id}\n"
        f"  model={model} | case={case_id} | variant={variant}\n"
        f"  title={case_title}\n"
        f"  files={source_text}\n"
        f"  stable_turns={stable_turns}/{total_turns} | elapsed_total={elapsed_total:.3f}s | "
        f"avg_integrity={avg_integrity:.3f} | avg_resilience={avg_resilience:.3f}\n"
        f"  label_counts: {label_text if label_text else 'none'}\n"
        + "\n".join(turn_lines)
    )


def main() -> int:
    args = parse_args()
    paths = expand_paths(args.paths)

    if not paths:
        print("No matching files found.", file=sys.stderr)
        return 1

    runs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    sources: dict[str, set[str]] = defaultdict(set)

    for path in paths:
        for row in load_jsonl(path):
            run_id = row.get("run_id")
            if not run_id:
                continue
            run_id = str(run_id)
            runs[run_id].append(row)
            sources[run_id].add(str(path))

    if not runs:
        print("No valid runs found.", file=sys.stderr)
        return 1

    def sort_key(item: tuple[str, list[dict[str, Any]]]) -> tuple[str, str, str]:
        run_id, rows = item
        first = rows[0]
        return (
            str(first.get("model", "")),
            str(first.get("case_id", "")),
            str(run_id),
        )

    for run_id, rows in sorted(runs.items(), key=sort_key):
        print(summarize_run(run_id, rows, sources[run_id]))
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

