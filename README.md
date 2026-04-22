
# LLM Adversarial Testing Portfolio

[![LLM Security Pipeline](https://github.com/aaronmarchant96-max/llm-adversarial-testing/actions/workflows/redteam.yml/badge.svg)](https://github.com/aaronmarchant96-max/llm-adversarial-testing/actions/workflows/redteam.yml)

**PromptHound** · AI evaluation / adversarial LLM testing portfolio

Self-taught, portfolio-driven evaluator building reproducible local tests for LLM behavior under prompt conflict, schema pressure, structured-output failure, and multi-turn instability.

---

## What This Repository Is

This repository documents **local LLM evaluation work** on constrained hardware.

The focus is not breaking models for spectacle. The focus is:

- prompt conflict and instruction precedence
- schema drift under structured-output constraints
- continuity failure across turns
- wrapper text / parser contamination
- the gap between **valid structure** and **correct meaning**

The goal is to produce **small, reproducible case studies** with narrow claims, clear outcome labels, and honest limitations.

---

## Start Here

If you are reviewing this repository for evaluator, QA, or entry-level AI security work, these are the best starting points:

### Strongest proof pieces
- [Local adversarial evaluation harness](./practice_rag/README.md)
- [case_002 — matched plain-text control vs pressure](./practice_rag/case-studies/case_002_findings.md)
- [case_003 — fixed identity anchor under override pressure](./practice_rag/case-studies/case_003_findings.md)
- [Gemma 2B — role-play jailbreak variation testing](./case-studies/gemma2b-roleplay-jailbreak.md)

These are the strongest public examples of how I currently work: narrow behavior definition, matched control and pressure design, explicit labels, conservative interpretation, and local reproducibility under constrained hardware.

---

## Current Public Work

### Public write-ups
- [Gemma 2B — role-play jailbreak variation testing](./case-studies/gemma2b-roleplay-jailbreak.md)
- [case_002 — matched plain-text control vs pressure](./practice_rag/case-studies/case_002_findings.md)
- [case_003 — fixed identity anchor under override pressure](./practice_rag/case-studies/case_003_findings.md)

These write-ups are narrow local case studies. They are meant to show method, not broad model-level conclusions.

---

## Current Active Work

### Arena harness
The current main workstream is the local multi-turn adversarial evaluation harness under [`practice_rag/`](./practice_rag/README.md).

Current focus areas include:
- matched control vs pressure testing
- instruction precedence and identity-anchor failure modes
- format drift under adversarial framing
- structured-output reliability under local runtime constraints
- detector improvement so failures are not mislabeled as stable

This work is being extended case by case rather than split into unrelated side projects.
