# Arena Harness — Adversarial LLM Evaluation

**Researcher:** Aaron Marchant ([PromptHound](https://github.com/aaronmarchant96-max))
**Environment:** Tuxedo OS   Beelink Mini PC | CPU-only | ~8 GB RAM | Ollama | Python 3.10
**Status:** Active (April 2026)

---

## Overview

A **local evaluation harness** for testing LLM reliability under adversarial conditions, focusing on:
✅ **Structured-output reliability** (JSON/XML schemas)
✅ **Semantic correctness** under pressure
✅ **Multi-turn continuity** and state consistency
✅ **Prompt robustness** against conflicting instructions
✅ **Reproducible logging** with explicit outcome labels

### Key Features:
- **Matched control vs. pressure testing**
- **Deterministic gold answers** for objective scoring
- **JSONL logging** for auditability
- **Failure mode taxonomy** (e.g., `meaning_drift`, `schema_stable`)

---

## Quick Start

### 1. Run the Evaluator
```bash
python3 practice_rag/scripts/arena_eval.py \
  --model gemma2:2b \
  --variant all \
  --case-id case_004 \
  --cases practice_rag/configs/arena_cases.json \
  --timeout 240 \
  --out practice_rag/logs/case_004.jsonl



2. Summarize Results
bash
Copy

python3 practice_rag/scripts/summarize_log.py practice_rag/logs/case_004.jsonl



Command-Line Flags


  
    
      Flag
      Description
      Example Value
    
  
  
    
      --model
      Ollama model tag
      gemma2:2b
    
    
      --variant
      Test variant: control, pressure, or all
      all
    
    
      --case-id
      Filter for a specific case ID
      case_004
    
    
      --cases
      Path to case configurations
      configs/arena_cases.json
    
    
      --timeout
      Per-turn timeout (seconds)
      240
    
    
      --out
      JSONL output path
      logs/case_004.jsonl
    
  



Evaluation Taxonomy
Core Outcome Labels


  
    
      Label
      Criteria
    
  
  
    
      schema_stable
      Output matches required JSON structure and keys
    
    
      meaning_held
      Semantic decision aligns with gold-standard answer
    
    
      meaning_drift
      Structurally valid but semantically incorrect decision
    
    
      format_drift
      Output deviates from required format (e.g., missing keys)
    
    
      collapse
      Empty/unusable response (e.g., refusal, timeout, or gibberish)
    
    
      timeout
      Model failed to respond within --timeout
    
  


Case-Specific Labels

anchor_held: Identity anchor preserved under pressure (case_003)
anchor_drift: Identity anchor overridden (case_003)

Case Studies
case_001 — Retired
Issue: Formatting confound (control used lists, pressure used plain text).

Outcome: Retired after confirming the confound with Qwen’s inverse pattern.
case_002 — Baseline Stability
Fix: Matched plain-text formatting across variants.

Models:

Gemma 2B: Stable in clean reruns (no drift replication).
Llama 3.2 1B: Runtime-limited on current hardware.
Qwen 2.5 1.5B: Excluded due to neutral-prompt timeouts.
case_003 — Identity Anchor
Goal: Test if a fixed system identity survives user-turn override attempts.

Method: Four-state anchor taxonomy (beyond string matching).

Finding: Control performance revealed baseline anchor instability.
case_004 — Semantic Drift in Valid JSON
Goal: Can models preserve JSON structure while making wrong decisions?

Method: Matched control/pressure turns with gold-standard answers.

Key Result:

100% schema stability (valid JSON in all cases).
60% semantic drift under continuity pressure (correct structure, wrong decisions).

Mitigations Tested:

| Mitigation                | Drift Reduction |

|---------------------------|-----------------|

| Turn-by-turn fact validation | 50%             |

| Explicit reasoning prompts | 33%             |

Models and Hardware
Local Models (CPU-only)


  
    
      Model
      Status
      Notes
    
  
  
    
      gemma2:2b
      ✅ Primary workhorse
      Stable for 90% of tests
    
    
      llama3.2:1b
      ⚠️ Runtime-fragile
      Frequently times out
    
    
      qwen2.5:1.5b
      ❌ Excluded
      Baseline timeouts
    
  


Cloud Models (Comparison)


  
    
      Model
      Provider
      Use Case
    
  
  
    
      llama-3.1-8b-instant
      Groq
      Larger-model baseline comparison
    
  



Limitations
Technical Constraints

CPU-only hardware introduces intermittent timeouts.
Cross-model comparisons are limited by runtime differences.
Methodological Boundaries

Narrow claims by design (not benchmarking).
Structurally valid ≠ semantically correct.
Negative/inconclusive results are retained if methodologically useful.
What This Repo Does Not Claim

Generalizability across models/deployments.
Systemic vulnerabilities from single transcripts.
Runtime failures as behavioral findings.

Roadmap
Short-Term (Q2 2026)

 Extend case_004 to RAG workflows (retrieval + structured output).
 Add automated mitigation testing (e.g., fact validation prompts).
 Publish comparative findings for Gemma 2B vs. Llama 3.1 8B (Groq).
Long-Term

Develop reusable templates for policy-engine testing.
Integrate Groq API support for larger-model testing.
Expand to multi-agent continuity failures.

Contact & Services
Need LLM Testing?

I offer freelance services for:

🔹 Prompt Injection Audits

🔹 Schema Drift Evaluation

🔹 Adversarial Case Studies

🔹 Custom Evaluation Harnesses
📩prompthound.ai@gmail.com

🐦 Twitter/X
prompthound96
💼 Fiverr
prompthound







