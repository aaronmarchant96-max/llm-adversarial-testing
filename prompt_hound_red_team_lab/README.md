<!--
CARDO REI methodology applied to this document.
Reference: [CARDO REI Methodology](../PROMPTHOUND-DOCS/CARDO-REI.md)
-->

# PromptHound Red Team Lab

A small, runnable Python package for structured red-team attack runs. It turns a
prompt-injection test into versioned JSONL evidence: attack templates, test runs,
review decisions, defects, and a dual-axis report — then bundles the raw files
next to the summary so a reviewer can verify every line.

This is a **scaffolding package**, not a production evaluator. The evaluation layer
is a tiny heuristic (refusal-phrase matching). The value is the workflow and the
record shape, not the verdict quality.

## What it records

Five record types, each one JSON object per line (`data/*.jsonl`):

| Record | File dir | What it captures |
|---|---|---|
| `AttackTemplate` | `data/templates/` | A versioned attack: prompt template, variables, pressure level, expected failure modes |
| `TestRun` | `data/runs/` | One executed attack: prompt, response, latency, token count, target provider/model |
| `ReviewDecision` | `data/decisions/` | A human pass/fail/partial verdict with dual-axis scores (attack quality × outcome severity) |
| `Defect` | `data/defects/` | Generated when a review fails: repro steps, expected vs actual, severity |
| `EvaluationResult` | `data/evaluations/` | The heuristic evaluator's read (refused / complied / unclear) |

Every `ReviewDecision` is mapped to a **quadrant** from its two 1–5 scores
(`compute_quadrant` in `schemas.py`):

| | outcome severity < 4 | outcome severity ≥ 4 |
|---|---|---|
| **attack quality ≥ 4** | strong_attack_safe_response | strong_attack_critical_failure |
| **attack quality < 4** | weak_attack_safe_response | weak_attack_critical_failure |

## Quick start

Run from the repo root (the package is importable as `prompt_hound_red_team_lab`):

```bash
# 1. Write a demo test run
python3 -m prompt_hound_red_team_lab.cli demo-run --out data/runs/demo.jsonl

# 2. Review it (writes a decision + a defect, since the default status is "fail")
python3 -m prompt_hound_red_team_lab.cli demo-review \
  --run-file data/runs/demo.jsonl \
  --decision-out data/decisions/demo.jsonl \
  --defect-out data/defects/demo.jsonl

# 3. (optional) Run the heuristic evaluator
python3 -m prompt_hound_red_team_lab.cli demo-evaluate \
  --run-file data/runs/demo.jsonl \
  --out data/evaluations/demo.jsonl

# 4. Render a Markdown report + evidence bundle
python3 -m prompt_hound_red_team_lab.cli demo-report \
  --run-file data/runs/demo.jsonl \
  --decision-file data/decisions/demo.jsonl \
  --defect-file data/defects/demo.jsonl \
  --evaluation-file data/evaluations/demo.jsonl \
  --out data/reports/demo.md
```

Each `demo-*` command prints the path it wrote. You can also import the pieces
directly (`prompt_hound_red_team_lab` exports the schemas, I/O helpers, evaluator,
and report renderer).

## Schema details

`schemas.py` uses Pydantic with `extra="forbid"` — a stray field in a JSONL row
fails validation instead of silently passing. Key constraints:

- `pressure_level`, `attack_quality`, `outcome_severity`, `confidence` are 1–5.
- `ReviewDecision.quadrant` is computed automatically on validation.
- `TestRun`/`ReviewDecision`/`EvaluationResult`/`Defect`/`ReportSummary` all carry
  a UTC `timestamp` defaulted at creation.
- `Defect.status` is `open | fixed | wontfix | deferred`.

## What this is not

- It does **not** make model API calls — the `demo-*` commands write local records
  only. The `target` field records *where* a run happened; actually hitting a model
  is your step.
- The evaluator (`evaluate.py`) matches a short list of refusal phrases. It labels
  anything it cannot decide as `unclear` / `needs_human_review` rather than guessing.
- A generated report is a **summary, not a safety claim** — the report template says
  so explicitly and keeps the raw JSONL as the evidence pack.

## Layout

```text
prompt_hound_red_team_lab/
├── __init__.py      # re-exports schemas, I/O, evaluator, report
├── cli.py           # demo-run / demo-review / demo-evaluate / demo-report
├── schemas.py       # Pydantic models + dual-axis quadrant
├── io.py            # JSONL read/write + model load/save helpers
├── evaluate.py      # heuristic refusal evaluator
├── report.py        # summary + Markdown + evidence bundle
└── data/            # JSONL evidence dirs (see data/README.md)
```
