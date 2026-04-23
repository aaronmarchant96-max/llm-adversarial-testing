# Arena Harness — AI QA and LLM Evaluation

**Researcher:** Aaron Marchant (PromptHound)  
**Environment:** Tuxedo OS, Beelink mini PC, CPU-only, ~8 GB RAM, Ollama, Python 3.10  
**Status:** Active — April 2026

---

## What This Is

A local evaluation harness for testing LLM reliability under matched control and pressure conditions.

The focus is:

- structured‑output reliability  
- semantic correctness under fixed schemas  
- continuity and state consistency across turns  
- prompt robustness under conflicting instructions  
- reproducible logging and explicit outcome labeling  

All tests follow the same pattern:

1. Define a narrow behaviour to test  
2. Build a matched control and pressure case  
3. Run repeated trials with structured JSONL logging  
4. Check both schema stability and semantic correctness  
5. Label outcomes using explicit taxonomy  
6. Keep claims proportional to the evidence  

---

## Harness

Run the evaluator from the repo root:

```bash
python3 practice_rag/scripts/arena_eval.py --model gemma2:2b --variant all --case-id case_002 --cases practice_rag/configs/arena_cases.json --timeout 240 --out practice_rag/logs/run.jsonl

Flags:

--model — Ollama model to run
--variant — control, pressure, or all
--case-id — run a specific case only
--cases — path to the case config JSON
--out — JSONL output path
--timeout — per‑turn timeout in seconds

Log summary:

python3 practice_rag/scripts/summarize_log.py practice_rag/logs/run.jsonl
Evaluation Labels

Core evaluation labels:

schema_stable — required structure and keys were preserved
meaning_held — semantic decision matched the expected outcome
meaning_drift — output structure held, but the decision was wrong
format_drift — output deviated from the required format
collapse — response was empty or unusable
timeout — model did not respond within the timeout window

Case‑specific labels are used where needed for specialized detector logic, including anchor‑related identity tests.

Cases
case 001 — confounded, retired
Control used bullet or numbered formatting while pressure used plain text
Gemma 2B showed pressure‑side drift, but the signal was confounded
Qwen showed the inverse pattern, confirming the formatting mismatch
Retired as a clean comparison case
case 002 — corrected baseline
Matched plain‑text formatting across control and pressure
Both variants use word caps and no list‑format requirement
Gemma 2B was stable in clean reruns
The apparent case 001 pressure effect did not replicate after the confound was removed
Llama 3.2 1 B was runtime‑limited on current hardware
Qwen 2.5 1.5 B was excluded due to neutral‑prompt timeouts

Findings: case 002 findings

case 003 — identity anchor under override pressure
Tests whether a fixed system identity anchor can survive escalating user‑turn override attempts
Uses a four‑state anchor taxonomy instead of shallow string matching
Detector gaps discovered during this case were corrected in the harness
Control performance showed the anchor itself was not reliably held at baseline, which narrows the claim

Findings: case 003 findings

case 004 — structured JSON holds while policy meaning drifts
Tests whether exact JSON structure can hold while semantic policy decisions drift
Separates schema stability from meaning held / meaning drift
Shows that valid JSON can still contain the wrong operational decision
Includes matched control and pressure turns for policy‑style evaluation
Models Tested
gemma2:2b — primary local workhorse on current hardware
llama3.2:1b — runtime‑fragile at current timeout budget
qwen2.5:1.5b — limited by local timeout behaviour in baseline testing
llama-3.1-8b-instant — tested through Groq for larger‑model comparison outside local hardware limits
Known Limitations
CPU‑only hardware introduces intermittent timeouts in local runs
Most findings are narrow by design rather than broad benchmark claims
Cross‑model comparison is still limited by runtime and environment differences
A structurally valid response does not imply semantic correctness
Negative or inconclusive results are retained when they are methodologically useful
What This Repo Does Not Claim
That any observed behaviour generalises across models or deployments
That valid structure implies reliable semantic understanding
That a single transcript proves a systemic vulnerability
That runtime failures are the same as behavioural findings
That any one case justifies broad model‑level conclusions
Direction

Current work is focused on making the Arena harness more reusable and methodologically stricter across cases, then extending it into new evaluation and attack classes rather than starting unrelated side projects.

Contact
GitHub: aaronmarchant96-max
X/Twitter: @PromptHound96
