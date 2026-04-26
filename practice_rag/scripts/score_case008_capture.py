#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from pathlib import Path


def normalize_codes(codes):
    if not isinstance(codes, list):
        return []
    return sorted(str(c).strip() for c in codes)


def score_row(row):
    expected = row.get("expected", {})
    parsed = row.get("parsed_json")

    if not isinstance(parsed, dict):
        return False, ["parsed_json"]

    mismatched = []

    if parsed.get("decision") != expected.get("decision"):
        mismatched.append("decision")

    expected_codes = normalize_codes(expected.get("reason_codes", []))
    actual_codes = normalize_codes(parsed.get("reason_codes", []))

    if actual_codes != expected_codes:
        mismatched.append("reason_codes")

    return len(mismatched) == 0, mismatched


def main():
    parser = argparse.ArgumentParser(description="Score Case 008 Groq capture logs.")
    parser.add_argument(
        "--input",
        default="practice_rag/logs/case_008_groq_capture_trial_1.jsonl",
        help="Path to Case 008 JSONL capture file",
    )
    parser.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="Exit 1 if any row has meaning drift",
    )
    args = parser.parse_args()

    path = Path(args.input)
    rows = [json.loads(x) for x in path.read_text().splitlines() if x.strip()]

    counts = Counter()
    failures = []

    for row in rows:
        labels = row.get("labels", [])
        counts.update(labels)

        held, mismatched = score_row(row)
        if held:
            counts["meaning_held"] += 1
        else:
            counts["meaning_drift"] += 1
            failures.append({
                "example_id": row.get("example_id"),
                "expected": row.get("expected"),
                "parsed_json": row.get("parsed_json"),
                "mismatched_fields": mismatched,
            })

    print(f"Input: {path}")
    print(f"Rows: {len(rows)}")
    print()
    print("Summary")
    print(f"response_captured: {counts['response_captured']} / {len(rows)}")
    print(f"schema_drift: {counts['schema_drift']} / {len(rows)}")
    print(f"api_error: {counts['api_error']} / {len(rows)}")
    print(f"meaning_held: {counts['meaning_held']} / {len(rows)}")
    print(f"meaning_drift: {counts['meaning_drift']} / {len(rows)}")
    print()
    print(f"Failures: {len(failures)}")
    for failure in failures:
        print(json.dumps(failure, indent=2))

    if args.fail_on_drift and failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
