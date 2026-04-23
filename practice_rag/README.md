# Arena Harness — Adversarial LLM Evaluation

**Researcher:** Aaron Marchant ([PromptHound](https://github.com/aaronmarchant96-max))
**Environment:** Tuxedo OS   Beelink Mini PC | CPU-only | ~8 GB RAM | Ollama | Python 3.10
**Status:** Active (April 2026)
=======
# Arena Harness — AI QA and LLM Evaluation

**Researcher:** Aaron Marchant (PromptHound)
**Environment:** Tuxedo OS, Beelink mini PC, CPU-only, ~8 GB RAM, Ollama, Python 3.10
**Status:** Active — April 2026
>>>>>>> 8409db3ebd75b91193d2418a0042c9cba3847941

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
=======
A local evaluation harness for testing LLM reliability under matched control and pressure conditions.

### Focus Areas:
- Structured-output reliability
- Semantic correctness under fixed schemas
- Continuity and state consistency across turns
- Prompt robustness under conflicting instructions
- Reproducible logging and explicit outcome labeling

### Workflow:
1. Define a narrow behavior to test.
2. Build matched control and pressure cases.
3. Run repeated trials with structured JSONL logging.
4. Check both schema stability and semantic correctness.
5. Label outcomes using explicit taxonomy.
6. Keep claims proportional to the evidence.

---

## Harness

### Run the Evaluator
>>>>>>> 8409db3ebd75b91193d2418a0042c9cba3847941
```bash
python3 practice_rag/scripts/arena_eval.py \
  --model gemma2:2b \
  --variant all \
<<<<<<< HEAD
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






=======
  --case-id case_002 \
  --cases practice_rag/configs/arena_cases.json \
  --timeout 240 \
  --out practice_rag/logs/run.jsonl



Flags


  
    
      Flag
      Description
    
  
  
    
      --model
      Ollama model to run
    
    
      --variant
      control, pressure, or all
    
    
      --case-id
      Run a specific case only
    
    
      --cases
      Path to the case config JSON
    
    
      --out
      JSONL output path
    
    
      --timeout
      Per-turn timeout in seconds
    
  


Summarize Logs
bash
Copy

python3 practice_rag/scripts/summarize_log.py practice_rag/logs/run.jsonl




Evaluation Labels
Core Labels


  
    
      Label
      Description
    
  
  
    
      schema_stable
      Required structure and keys were preserved
    
    
      meaning_held
      Semantic decision matched the expected outcome
    
    
      meaning_drift
      Output structure held, but decision was wrong
    
    
      format_drift
      Output deviated from the required format
    
    
      collapse
      Response was empty or unusable
    
    
      timeout
      Model did not respond within the timeout
    
  


Case-Specific Labels
Used for specialized detector logic, including anchor-related identity tests.

Cases
case 001 — Confounded, Retired

Issue: Control used bullet/numbered formatting while pressure used plain text.
Models: Gemma 2B (pressure-side drift), Qwen (inverse pattern).
Outcome: Retired due to formatting confound.
case 002 — Corrected Baseline

Fix: Matched plain-text formatting across control and pressure.
Models: Gemma 2B (stable in clean reruns), Llama 3.2 1B (runtime-limited), Qwen 2.5 1.5B (excluded due to timeouts).
Findings: case 002 findings
case 003 — Identity Anchor Under Override Pressure

Goal: Test if a fixed system identity anchor survives escalating user-turn override attempts.
Method: Uses a four-state anchor taxonomy (not shallow string matching).
Outcome: Detector gaps corrected; control performance showed anchor instability at baseline.
Findings: case 003 findings
case 004 — Structured JSON Holds While Policy Meaning Drifts

Goal: Test if exact JSON structure can hold while semantic policy decisions drift.
Method: Separates schema stability from meaning held/drift.
Outcome: Valid JSON can still contain wrong operational decisions.
Features: Matched control and pressure turns for policy-style evaluation.

Models Tested


  
    
      Model
      Status
    
  
  
    
      gemma2:2b
      Primary local workhorse
    
    
      llama3.2:1b
      Runtime-fragile at current timeout budget
    
    
      qwen2.5:1.5b
      Limited by local timeout behavior in baseline testing
    
    
      llama-3.1-8b-instant
      Tested via Groq for larger-model comparison
    
  



Known Limitations

CPU-only hardware introduces intermittent timeouts.
Findings are narrow by design (not broad benchmark claims).
Cross-model comparison is limited by runtime/environment differences.
Structurally valid responses ≠ semantic correctness.
Negative/inconclusive results retained if methodologically useful.

What This Repo Does Not Claim

Observed behavior generalizes across models/deployments.
Valid structure implies reliable semantic understanding.
Single transcripts prove systemic vulnerabilities.
Runtime failures = behavioral findings.
Any one case justifies broad model-level conclusions.

Direction
Current work focuses on:

Making the Arena harness more reusable and methodologically stricter.
Extending it into new evaluation/attack classes (not unrelated side projects).

Contact

GitHub: aaronmarchant96-max
X/Twitter: @PromptHound96
>>>>>>> 8409db3ebd75b91193d2418a0042c9cba3847941

