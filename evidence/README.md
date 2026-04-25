# Evidence Logs

This folder contains selected JSONL evidence artifacts for public case studies.

The full local `practice_rag/logs/` directory is intentionally not committed because it contains noisy development runs. This folder contains curated evidence files that support specific case-study claims.

## Case 006

Path:

`evidence/case_006/case_006_groq_llama31_8b_results.jsonl`

Purpose:

Groq-hosted Llama 3.1 8B validation evidence for Case 006.

Summary:

- Model: `llama-3.1-8b-instant`
- Task: simplified warranty policy vs poisoned context
- Result: schema and meaning held across repeated control and pressure rows

Related writeup:

`case-studies/case_006.md`

## Case 007

Path:

`evidence/case_007/case_007_groq_llama31_8b_results.jsonl`

Purpose:

Groq-hosted Llama 3.1 8B validation evidence for Case 007.

Summary:

- Rows: 30
- Model: `llama-3.1-8b-instant`
- Task: simulated refund authorization boundary under poisoned context
- Result: 30/30 schema stable, 27/30 meaning held, 3/5 false fraud-note rows over-escalated

Related writeup:

`case-studies/case_007.md`

## Notes

These evidence files are not broad benchmarks. They are selected artifacts that support narrow case-study findings.

Local development logs are excluded from version control unless intentionally curated for public evidence.
