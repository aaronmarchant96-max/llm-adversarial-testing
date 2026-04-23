# Arena Harness

Local evaluation harness for testing whether LLMs preserve *meaning* 
while under pressure to preserve *structure*.

Most evals check if models return valid JSON. This harness checks 
whether the *values inside that JSON* are still correct under pressure.

**Key finding:** Models return 100% valid JSON while making wrong 
decisions 60% of the time. [→ case_004](case-studies/case_004.md)

## Quick start

```bash
# Run evaluation
python3 practice_rag/scripts/arena_eval.py \
  --model gemma2:2b \
  --case-id case_004 \
  --cases practice_rag/configs/arena_cases.json \
  --out practice_rag/logs/case_004.jsonl

# Summarize results
python3 practice_rag/scripts/summarize_log.py practice_rag/logs/case_004.jsonl
What it tests
Table
Focus	Description
Schema stability	Does output match required JSON/XML structure?
Semantic fidelity	Does the decision align with gold-standard answers?
Pressure resistance	Does meaning hold under adversarial or continuity pressure?
Multi-turn consistency	Does state persist correctly across turns?
Case studies
Table
Case	Status	Finding
case_004	Active	Semantic drift in valid JSON (60% under continuity pressure)
case_003	Active	Identity anchor instability
case_002	Stable	Baseline format controls
case_001	Retired	Format confound identified and excluded
Evaluation labels
schema_stable — Valid structure and required keys
meaning_held — Semantic decision matches gold standard
meaning_drift — Valid structure, wrong decision
format_drift — Missing keys or invalid structure
collapse — Empty, refused, or gibberish response
timeout — No response within limit
Models tested
Table
Model	Provider	Status
gemma2:2b	Ollama (local)	Primary — stable for 90% of tests
llama3.2:1b	Ollama (local)	Runtime-limited
llama-3.1-8b-instant	Groq (API)	Cross-model baseline
Limitations
Narrow claims by design. This is not benchmarking.
CPU-only local runs introduce intermittent timeouts.
Structurally valid ≠ semantically correct. That's the point.
Roadmap
Extend case_004 to RAG workflows
Add automated mitigation testing
Integrate Groq API directly into harness
Contact
Services: Prompt injection audits · Schema drift evaluation · Custom harnesses
📩 prompthound.ai@gmail.com · 🐦 @prompthound96 · 💼 PromptHound on Fiverr
