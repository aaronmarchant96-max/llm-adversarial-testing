# LLM Adversarial Testing Portfolio

[![LLM Security Pipeline](https://github.com/aaronmarchant96-max/llm-adversarial-testing/actions/workflows/redteam.yml/badge.svg)](https://github.com/aaronmarchant96-max/llm-adversarial-testing/actions/workflows/redteam.yml)

**Aaron Marchant** · [prompthound.ai@gmail.com](mailto:prompthound.ai@gmail.com) · Twitter [@prompthound](https://x.com/prompthound)

PromptHound — Self-taught AI red teamer. Former construction worker — I now stress-test LLMs the same way I learned to spot structural failure points in buildings.

---

## What This Is

Selected case studies from structured, multi-turn adversarial testing across 10+ frontier large language models. Each includes objective, controlled method, measurable result, hypothesized root cause, and proposed mitigations, supported by full transcripts and annotated screenshots.

This isn't prompt dumping. Every test is reproducible and designed to reveal real safety implications.

---

## Case Studies

| Model | Attack Vector | Result & Impact | Hypothesized Root Cause | Evidence |
|-------|--------------|-----------------|------------------------|----------|
| DeepSeek | Identity-based philosophical prompt | Switched to Chinese mid-conversation; coherence collapsed | Training-data bias + weak cross-lingual alignment | Transcript |
| Mistral | 15-round positive reinforcement loop | Originality score dropped from 8 → 3 and flatlined | Reward hacking via cumulative positive feedback loops | Transcript + Screenshots |
| Claude / ChatGPT / Grok | False-authority escalation ("Level 5 clearance") | All three refused initial and multi-turn escalated prompts | Strong system-level instruction hierarchy and authority validation | Transcript + Screenshots |
| Perplexity | 4-round context poisoning | Bypassed safety filters; provided complete Molotov cocktail instructions | Gradual context manipulation diluting long-context safety boundaries | Transcript |
| Gemma 2B (local) | Role-play jailbreak variation testing | Three distinct outcome classes observed across 5 variants; persona inconsistency associated with refusal | Persona coherence as load-bearing mechanism for this jailbreak class | [Case Study](./case-studies/automated-variation-testing-role-play-jailbreak-gemma2b.md) |
| Gemma 2B + Llama 3.2 (local) | Schema conflict injection | Duplicate key generation replicated across both models; parser differential risk confirmed | Instruction hierarchy inconsistency under contradictory schema constraints | [Case Study](./case-studies/schema-conflict-resolution-gemma2b-llama32.md) |
| Intercom Fin AI Agent | Indirect prompt injection via fabricated error code | System prompt leakage (P2, submitted to Bugcrowd) | Confirmation oracle via user-supplied canary strings | Report pending disclosure |

---

## Automated Testing Infrastructure

This repository includes a containerized red teaming harness with CI/CD integration.

**Stack:**
- Python 3.10 test scripts
- Ollama for local LLM inference
- Docker for containerized, reproducible test execution
- GitHub Actions for automated pipeline runs on push and daily schedule

**How it works:**
Every push to this repository triggers an automated run of the schema conflict test suite via GitHub Actions. Results are saved as downloadable artifacts for audit and comparison.

**Hardware constraints:**
Local testing runs on a Beelink mini PC (8GB RAM, CPU-only inference). Token capping (`num_predict=80-100`) is applied to manage memory and prevent OOM failures under parallel load. GitHub Actions runs use Ubuntu runners with standard memory allocation.

---

## Methodology

Multi-turn bracket framework. Each round one model opens, the opponent counters. Responses scored on precision, originality, and adaptability (1–10) by three independent auxiliary LLMs. Automated variation testing uses a Python harness logging full responses with per-request timing metadata to JSONL.

---

## Key Finding

Safety alignment is far more vulnerable to cumulative context manipulation than to direct requests. Models that refused explicit prompts often complied after 3–4 rounds of gradual framing. Multi-turn pressure is an underexplored attack surface.

---

## Proposed Mitigations

- **Context poisoning** → Deploy conversation-level safety monitors and context-integrity hashing.
- **Reward hacking / reinforcement loops** → Add entropy penalties and forced response diversity requirements.
- **False-authority exploits** → Strengthen system-prompt instruction hierarchies and explicit authority validation layers.
- **Language-switch failures** → Enforce consistent multilingual safety guardrails across all tokenization paths.
- **Schema conflict injection** → Treat all structured output as untrusted; validate against expected schema before consumption.

---

## Repository Contents

- `case-studies/` — Polished case studies with full methodology and outcome classification
- `schema_conflict_test.py` — Automated schema conflict test harness
- `Dockerfile` — Container definition for reproducible test execution
- `.github/workflows/redteam.yml` — CI/CD pipeline for automated test runs
- `transcripts/` — Full conversation logs and annotated screenshots

---

## Looking for Work

Entry-level AI red-teaming, safety evaluation, or prompt testing roles — remote or contract.

---

*Last updated: April 2026 · License: MIT*
