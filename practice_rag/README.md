# Arena Harness — AI QA and LLM Evaluation

**Researcher:** Aaron Marchant (PromptHound)
**Environment:** Tuxedo OS, Beelink mini PC, CPU-only, ~8 GB RAM, Ollama, Python 3.10
**Status:** Active — April 2026

---

## What This Is

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
```bash
python3 practice_rag/scripts/arena_eval.py \
  --model gemma2:2b \
  --variant all \
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

