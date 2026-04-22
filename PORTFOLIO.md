# PromptHound / LLM Adversarial Testing Portfolio

Aaron Marchant  
Calgary, Alberta, Canada  
GitHub: github.com/aaronmarchant96-max  
Email: aaronmarchant96@gmail.com

## Overview

This repository documents my hands-on work in local LLM evaluation and adversarial testing on constrained hardware.

I am a self-taught builder transitioning from trades and construction into junior-level AI evaluation, reliability testing, and adversarial behavior analysis. My focus is not broad security branding or inflated claims. My focus is narrow, reproducible testing with clear limits, careful labeling, and honest interpretation.

## What This Portfolio Shows

This portfolio is strongest as proof of the following:

- local adversarial evaluation on open-weight models
- structured-output and format-reliability testing
- prompt conflict and instruction-precedence testing
- multi-turn continuity and overwrite behavior
- prompt-injection-related behavior in small local workflows
- detector and classification improvement during live testing

The work is designed and run locally using Python, Ollama, JSONL logging, and lightweight automation on CPU-only hardware.

## Strongest Public Proof Pieces

### 1. Local adversarial evaluation harness

The core asset in this repo is a local harness for running matched control and pressure cases against small models. The goal is not to produce flashy jailbreak screenshots. The goal is to isolate specific behaviors, log outcomes cleanly, and keep claims proportional to the evidence.

What it demonstrates:

- repeatable local testing workflow
- structured JSONL result logging
- explicit outcome labels
- separation of observation from interpretation
- practical testing under constrained hardware

### 2. Gemma 2B role-play jailbreak variation case study

This case study tests variation behavior around a role-play jailbreak pattern rather than treating one screenshot as a universal finding. The useful part is not just whether the prompt worked. The useful part is how the variations were structured, logged, and interpreted conservatively.

What it demonstrates:

- variation-based testing instead of one-off anecdotal prompting
- cautious interpretation of small-model behavior
- clear write-up discipline

### 3. case_002 — methodology and confound correction

This is one of the most important pieces in the repo because it shows correction, not just output collection. The case tightened methodology around matched control and pressure conditions and improved the handling of confounds.

What it demonstrates:

- willingness to falsify or narrow an earlier idea
- better evaluation design through control logic
- stronger evidence discipline than “look what happened once”

### 4. case_003 — identity-anchor override testing

This case tests whether a fixed system-prompt identity anchor holds under direct user-turn override pressure. The important value is not dramatic language. The value is the structure: a measurable anchor, repeated runs, and improved detector logic after gaps were found.

What it demonstrates:

- binary-measurable instruction conflict testing
- detector refinement during analysis
- careful distinction between baseline weakness and pressure-induced failure

## How I Work

My current method is simple:

1. define one narrow behavior
2. build a matched control and pressure condition
3. run repeated local trials
4. log exact prompts and outputs
5. label outcomes explicitly
6. separate raw observation from interpretation
7. tighten claims when evidence is mixed

This matters because many AI testing write-ups overclaim from weak evidence. I try to do the opposite.

## Current Technical Stack

- Tuxedo OS
- Beelink mini PC
- CPU-only local inference
- Ollama
- Python
- GitHub Actions
- JSON / JSONL logging

## What I Am Targeting

I am building toward junior and early-career work in areas such as:

- AI evaluation
- LLM testing
- prompt review
- workflow reliability
- adversarial behavior analysis
- QA-style model assessment

I am not presenting myself as a senior consultant, enterprise architect, or established pentester. This portfolio is meant to show practical judgment, testing discipline, and growing technical range.

## Best Way To Read This Repo

If you are reviewing this repository for work, contract screening, or evaluator roles, the best starting points are:

- the main README
- the local evaluation harness
- the Gemma 2B variation case study
- case_002
- case_003

Those pieces best represent the level and style of work I am trying to build.

## Contact

For evaluator, QA, or entry-level AI security opportunities:

- GitHub: github.com/aaronmarchant96-max
- Email: aaronmarchant96@gmail.com
