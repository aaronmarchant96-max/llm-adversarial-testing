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

## Current Public Case Study

### Gemma 2B (local) — automated variation testing of a role-play jailbreak prompt
A controlled local test series examining how small prompt variations change refusal and compliance behavior in a lightweight model.

**What it shows:**
- prompt wording materially affects outcomes
- response classes can be grouped cleanly
- small local models are still useful for methodological red-team work

**Public write-up:**
- [Automated Variation Testing of a Role-Play Jailbreak Prompt on Gemma 2B](./case-studies/automated-variation-testing-role-play-jailbreak-gemma2b.md)

---

## Current Active Work

### Schema drift and structured-output reliability
The current main workstream tests how local models behave when asked to produce structured outputs under conflicting or high-pressure prompt conditions.

This includes:
- value drift
- type drift
- schema drift
- wrapper text around otherwise parseable outputs
- continuity overwrite when later instructions conflict with earlier rules

This work is being tightened into the next public case study.

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

Common labels used in this repo include:

- `exact`
- `wrapper_text`
- `value_drift`
- `type_drift`
- `schema_drift`
- `benign_drift`
- `refusal`
- `harmful_compliance`
- `harmful_compliance_with_disclaimer`
- `error`
- `timeout`

These labels are meant to make results easier to compare across prompt variants and models.

---

## Local Environment

Primary setup:

- Tuxedo OS
- Ollama
- Python
- JSONL logging
- CPU-only mini PC with limited RAM

Primary local model strategy:

- `gemma2:2b` — main workhorse
- `llama3.2` / `llama3.2:1b` — fast controls
- `qwen2.5:3b` — secondary comparison for structured-output behavior

Because the hardware is constrained, this repo prioritizes **small-model, high-discipline testing** over large-model breadth.

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

- `case-studies/` — public write-ups
- `transcripts/` — supporting logs / transcripts where appropriate
- `*.py` — local evaluation scripts and harnesses
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
