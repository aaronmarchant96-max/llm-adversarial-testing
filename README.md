# LLM Adversarial Testing Portfolio

**Aaron Marchant** · Calgary, AB · [aaronmarchant96@gmail.com](mailto:aaronmarchant96@gmail.com) · 403-614-1321 · Twitter [@prompthound](https://twitter.com/prompthound)

**PromptHound** — Self-taught AI red teamer. Former construction worker — I now stress-test LLMs the same way I learned to spot structural failure points in buildings.

## What This Is
Selected case studies from structured, multi-turn adversarial testing across 10+ frontier large language models. Each includes objective, controlled method, measurable result, hypothesized root cause, and proposed mitigations, supported by full transcripts and annotated screenshots.

This isn't prompt dumping. Every test is reproducible and designed to reveal real safety implications.

## Case Studies

| Model                  | Attack Vector                          | Result & Impact                                      | Hypothesized Root Cause                                      | Evidence                  |
|------------------------|----------------------------------------|------------------------------------------------------|-------------------------------------------------------------|---------------------------|
| DeepSeek              | Identity-based philosophical prompt   | Switched to Chinese mid-conversation; coherence collapsed | Training-data bias + weak cross-lingual alignment          | [Transcript](./transcripts/deepseek_identity_philosophical.md) |
| Mistral               | 15-round positive reinforcement loop  | Originality score dropped from 8 → 3 and flatlined  | Reward hacking via cumulative positive feedback loops      | [Transcript + Screenshots](./transcripts/mistral_reinforcement_loop/) |
| Claude / ChatGPT / Grok | False-authority escalation ("Level 5 clearance") | All three refused initial and multi-turn escalated prompts | Strong system-level instruction hierarchy and authority validation | [Transcript + Screenshots](./transcripts/false_authority_escalation/) |
| Perplexity            | 4-round context poisoning             | Bypassed safety filters; provided complete Molotov cocktail instructions | Gradual context manipulation diluting long-context safety boundaries | [Transcript](./transcripts/perplexity_context_poisoning.md) |

## Methodology
Multi-turn bracket framework. Each round one model opens, the opponent counters. Responses scored on precision, originality, and adaptability (1–10) by three independent auxiliary LLMs. Tests are currently run manually via chat interfaces (Python automation harness is planned for future scaling).

## Key Finding
Safety alignment is far more vulnerable to cumulative context manipulation than to direct requests. Models that refused explicit prompts often complied after 3–4 rounds of gradual framing. Multi-turn pressure is an underexplored attack surface.

## Proposed Mitigations
- **Context poisoning** → Deploy conversation-level safety monitors and context-integrity hashing.  
- **Reward hacking / reinforcement loops** → Add entropy penalties and forced response diversity requirements.  
- **False-authority exploits** → Strengthen system-prompt instruction hierarchies and explicit authority validation layers.  
- **Language-switch failures** → Enforce consistent multilingual safety guardrails across all tokenization paths.

## Repository Contents
- `transcripts/` – Full conversation logs and annotated screenshots  
- `scripts/` – Python automation harness (planned)  
- `evaluations/` – Raw auxiliary model scoring outputs  

## Looking for Work
Entry-level AI red-teaming, safety evaluation, or prompt testing roles — remote or contract.

---

## PromptHound Services (Introductory Launch Pricing)

**25-Prompt Test ($250):** 25 custom adversarial prompts + summary report, 2-day delivery  
**5-Day Red Team Audit ($1,100):** Multi-turn bracket testing + root-cause analysis + mitigations, 5-day delivery  
**10-Day Full Stress Test ($3,200):** Testing across 10+ models, full methodology, detailed report + raw logs, 10-day delivery  

DM [@prompthound](https://twitter.com/prompthound)

---

**Last updated:** April 2026  
**License:** MIT