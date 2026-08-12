"""Tiny validation script using a public Iris sample.

The script:
1. Loads a small CSV sample derived from the public Iris dataset.
2. Applies a simple scoring rule.
3. Uses a cost-weighted decision gate similar to CARDO GUARD.
4. Writes a human-readable markdown report with limitations.
"""

from __future__ import annotations

import csv
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DATA_PATH = Path(__file__).with_name("iris_sample.csv")
DEFAULT_OUT_DIR = Path(__file__).with_name("output")


@dataclass(frozen=True)
class IrisRow:
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    species: str


@dataclass(frozen=True)
class ScoredRow:
    row: IrisRow
    score: float
    actual_positive: bool
    predicted_positive: bool


def load_rows(path: Path) -> list[IrisRow]:
    rows: list[IrisRow] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for item in reader:
            rows.append(
                IrisRow(
                    sepal_length=float(item["sepal_length"]),
                    sepal_width=float(item["sepal_width"]),
                    petal_length=float(item["petal_length"]),
                    petal_width=float(item["petal_width"]),
                    species=item["species"].strip(),
                )
            )
    return rows


def simple_score(row: IrisRow) -> float:
    # A deliberately simple rule: petal dimensions matter most.
    return round((row.petal_length * 1.1) + (row.petal_width * 2.0) - (row.sepal_width * 0.2), 2)


def is_positive(row: IrisRow) -> bool:
    # Treat virginica as the positive class for this validation slice.
    return row.species == "virginica"


def classify(score: float, threshold: float) -> bool:
    return score >= threshold


def score_rows(rows: Iterable[IrisRow], threshold: float) -> list[ScoredRow]:
    scored: list[ScoredRow] = []
    for row in rows:
        score = simple_score(row)
        scored.append(
            ScoredRow(
                row=row,
                score=score,
                actual_positive=is_positive(row),
                predicted_positive=classify(score, threshold),
            )
        )
    return scored


def confusion_counts(scored: Iterable[ScoredRow]) -> dict[str, int]:
    counts = {"tp": 0, "tn": 0, "fp": 0, "fn": 0}
    for item in scored:
        if item.actual_positive and item.predicted_positive:
            counts["tp"] += 1
        elif not item.actual_positive and not item.predicted_positive:
            counts["tn"] += 1
        elif not item.actual_positive and item.predicted_positive:
            counts["fp"] += 1
        else:
            counts["fn"] += 1
    return counts


def precision(counts: dict[str, int]) -> float:
    denom = counts["tp"] + counts["fp"]
    return counts["tp"] / denom if denom else 0.0


def recall(counts: dict[str, int]) -> float:
    denom = counts["tp"] + counts["fn"]
    return counts["tp"] / denom if denom else 0.0


def accuracy(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    return (counts["tp"] + counts["tn"]) / total if total else 0.0


def cost_gate(counts: dict[str, int], cost_to_act: float, cost_of_missing: float) -> dict[str, float | str]:
    total = sum(counts.values())
    false_alarm_rate = counts["fp"] / total if total else 0.0
    miss_rate = counts["fn"] / total if total else 0.0

    action_waste = false_alarm_rate * cost_to_act
    miss_loss = miss_rate * cost_of_missing
    decision = "ACT" if miss_loss > action_waste else "HOLD"

    return {
        "false_alarm_rate": false_alarm_rate,
        "miss_rate": miss_rate,
        "action_waste": action_waste,
        "miss_loss": miss_loss,
        "decision": decision,
    }


def format_row_line(item: ScoredRow) -> str:
    verdict = "P" if item.predicted_positive else "N"
    actual = "P" if item.actual_positive else "N"
    return (
        f"- score={item.score:0.2f} pred={verdict} actual={actual} "
        f"species={item.row.species} "
        f"({item.row.sepal_length:.1f}, {item.row.sepal_width:.1f}, {item.row.petal_length:.1f}, {item.row.petal_width:.1f})"
    )


def render_report(
    rows: list[ScoredRow],
    threshold: float,
    cost_to_act: float,
    cost_of_missing: float,
) -> str:
    counts = confusion_counts(rows)
    gate = cost_gate(counts, cost_to_act, cost_of_missing)
    top = sorted(rows, key=lambda item: item.score, reverse=True)[:3]
    bottom = sorted(rows, key=lambda item: item.score)[:3]

    lines = [
        "# Iris Sample Validation Report",
        "",
        "## What this tool does",
        "It loads a small public Iris sample, scores each row with a simple rule, and uses a cost-weighted gate to decide whether the rule is worth trusting in this slice.",
        "",
        "## Setup",
        f"- Dataset: {DATA_PATH.name}",
        f"- Rows: {len(rows)}",
        f"- Positive class: virginica",
        f"- Score rule: 1.1 * petal_length + 2.0 * petal_width - 0.2 * sepal_width",
        f"- Threshold: {threshold:.2f}",
        f"- Cost to act: {cost_to_act:.2f}",
        f"- Cost of missing: {cost_of_missing:.2f}",
        "",
        "## Results",
        f"- Accuracy: {accuracy(counts):.2%}",
        f"- Precision: {precision(counts):.2%}",
        f"- Recall: {recall(counts):.2%}",
        f"- True positives: {counts['tp']}",
        f"- True negatives: {counts['tn']}",
        f"- False positives: {counts['fp']}",
        f"- False negatives: {counts['fn']}",
        "",
        "## Cost gate",
        f"- False alarm rate: {gate['false_alarm_rate']:.2%}",
        f"- Miss rate: {gate['miss_rate']:.2%}",
        f"- Expected action waste: ${gate['action_waste']:.2f}",
        f"- Expected miss loss: ${gate['miss_loss']:.2f}",
        f"- Decision: {gate['decision']}",
        "",
        "## Highest scores",
    ]

    lines.extend(format_row_line(item) for item in top)

    lines += [
        "",
        "## Lowest scores",
    ]
    lines.extend(format_row_line(item) for item in bottom)

    lines += [
        "",
        "## Limitations",
        "- This is a small sample, not the full Iris dataset.",
        "- The scoring rule is intentionally simple and not tuned for best accuracy.",
        "- The cost numbers are synthetic and are here to show the decision gate, not to represent a real business case.",
        "- A different threshold would change the confusion matrix and the decision.",
        "- This report is useful for checking the shape of the workflow, not for proving the rule is optimal.",
        "",
    ]

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a small public Iris sample with a cost-weighted gate.")
    parser.add_argument("--threshold", type=float, default=9.0, help="Classification threshold for the score rule.")
    parser.add_argument("--cost-to-act", type=float, default=4.0, help="Cost of acting when the score is wrong.")
    parser.add_argument("--cost-of-missing", type=float, default=20.0, help="Cost of missing a positive case.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="Directory for the markdown report.")
    parser.add_argument("--data-file", type=Path, default=DATA_PATH, help="CSV file to load.")
    args = parser.parse_args()

    threshold = args.threshold
    cost_to_act = args.cost_to_act
    cost_of_missing = args.cost_of_missing
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = load_rows(args.data_file)
    scored = score_rows(rows, threshold=threshold)
    report = render_report(scored, threshold, cost_to_act, cost_of_missing)

    report_path = out_dir / "iris_validation_report.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"wrote {report_path}")
    print(f"rows={len(scored)} accuracy={accuracy(confusion_counts(scored)):.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
