<!--
CARDO REI methodology applied to this document.
Reference: [CARDO REI Methodology](PROMPTHOUND-DOCS/CARDO-REI.md)
-->

# JSONL Folder Layout

This folder holds the local JSONL evidence for PromptHound Red Team Lab.

## Layout

```text
data/
├── templates/
├── runs/
├── evaluations/
├── decisions/
├── defects/
└── reports/
```

## File Types

- `templates/` - versioned attack templates
- `runs/` - raw test runs with prompts, responses, and metadata
- `evaluations/` - simple review labels from the tiny evaluator layer
- `decisions/` - reviewer decisions and dual-axis scores
- `defects/` - defect records generated from failed reviews
- `reports/` - generated Markdown summaries and evidence-pack metadata

## Notes

- Keep each record as one JSON object per line.
- Keep the files human-readable.
- Keep the schema flat enough to query later with SQLite if needed.
