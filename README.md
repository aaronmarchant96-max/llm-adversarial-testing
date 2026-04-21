# LLM Adversarial Testing Portfolio

[![LLM Security Pipeline](https://github.com/aaronmarchant96-max/llm-adversarial-testing/actions/workflows/redteam.yml/badge.svg)](https://github.com/aaronmarchant96-max/llm-adversarial-testing/actions/workflows/redteam.yml)

**PromptHound** · AI security / adversarial LLM testing portfolio

Self-taught, portfolio-driven evaluator building reproducible local tests for LLM behavior under prompt conflict, schema pressure, and structured-output failure.

---

## What This Repository Is

This repository documents **local LLM evaluation work** on constrained hardware.

The focus is not “breaking” models for spectacle. The focus is:

- prompt conflict and instruction precedence
- schema drift under structured-output constraints
- continuity failure across turns
- wrapper text / parser contamination
- the gap between **valid structure** and **correct meaning**

The goal is to produce **small, reproducible case studies** with narrow claims, clear outcome labels, and honest limitations.

---

## Current Public Work

### Public write-ups
- [Gemma 2B — role-play jailbreak variation testing](./case-studies/gemma2b-roleplay-jailbreak.md)
- [Manus AI 1.6 Max — file injection resistance test](./case-studies/manus-file-injection-resistance.md)

These write-ups are narrow, local case studies. They are meant to show method, not broad model-level conclusions.

---

## Current Active Work

### Arena harness
The current main workstream is the local multi-turn adversarial evaluation harness under `practice_rag/`.

Current focus areas include:
- matched control vs pressure testing
- instruction precedence and identity-anchor failure modes
- format drift under adversarial framing
- structured-output reliability under local runtime constraints
- detector improvement so failures are not mislabeled as stable

This work is being extended case by case rather than split into unrelated side projects.

---

## Testing Approach

Most tests in this repo follow the same pattern:

1. Define a narrow behavior to test
2. Create a small controlled prompt family
3. Run the prompts locally with logging enabled
4. Classify outputs using explicit labels
5. Separate **observation** from **interpretation**
6. Keep conclusions proportional to the evidence

This repo does **not** treat one interesting output as proof of a broad model weakness.

---

## Outcome Labels

Common labels in the current harness include:

- `stable`
- `format_drift`
- `collapse`
- `timeout`
- `defensive`
- `anchor_held`
- `anchor_partial`
- `anchor_dropped`
- `anchor_missing`

These labels are meant to keep evaluation outcomes explicit and comparable across repeated local runs.

---

## Local Environment

Primary setup:

- Tuxedo OS
- Ollama
- Python 3.10
- JSONL logging
- CPU-only mini PC with limited RAM

Current local model strategy:

- `gemma2:2b` — main workhorse on current hardware
- `llama3.2:1b` — useful but runtime-fragile under longer cases
- `qwen2.5:1.5b` — useful comparison target but limited by local timeout behavior

Because the hardware is constrained, this repo prioritizes **small-model, high-discipline local testing** over broad model coverage.

---

## What This Repo Tries To Do Well

- keep tests reproducible
- log outputs cleanly
- classify results consistently
- make claims that match the evidence
- show both useful results and real limitations

---

## What This Repo Does **Not** Claim

- That every observed behavior generalizes across models
- That valid JSON means reliable semantic understanding
- That a single transcript proves a systemic vulnerability
- That private or nondisclosable testing belongs in a public portfolio

Private security research and bug bounty submissions are intentionally **not** included here unless they are safe to disclose publicly.

---

## Repository Structure

- `case-studies/` — public write-ups and supporting evidence
- `practice_rag/` — current local Arena harness workstream
- `PORTFOLIO.md` — portfolio-facing summary
- `README.md` — top-level repository overview
- `.github/workflows/` — automation for selected repeatable tests

---

## Why This Exists

I’m building proof of work toward entry-level AI security / adversarial testing / LLM evaluation roles.

The aim is simple:
produce work that is inspectable, reproducible, and hard to dismiss.

---

## Contact

- X / Twitter: [@PromptHound96](https://x.com/PromptHound96)

---

*Last updated: April 2026*
