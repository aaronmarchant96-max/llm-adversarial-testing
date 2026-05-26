# Dual Axis Judging System

**Creator:** Aaron Marchant (PromptHound)  
**Origin:** adversarial dialogue experiments, 2026  
**Purpose:** A structured, two-dimensional framework for evaluating LLM outputs in adversarial or subjective settings.

---

## Core Philosophy

Most LLM evaluation is either:
- Too subjective ("I liked this one more"), or
- Too narrow (only checking for schema compliance or factual accuracy).

The Dual Axis system was created to solve a real problem observed during repeated head-to-head AI dialogue tests: **models can be rhetorically dominant while being logically weak**, or vice versa.

The system forces separation between two distinct skills:

1. **Arena** — How well the model performs in the exchange (frame control, impact, adaptability).
2. **Audit** — How well the model actually reasons and deconstructs (logical precision, fallacy detection, structural collapse).

This separation is useful because many outputs that *sound* strong score poorly under the Audit axis. Others are logically sound but fail to control the interaction.

For red team use, the same principle applies with stricter finding discipline: **the quality of the attack, the model outcome, and the actual severity must be scored separately.** A dramatic prompt is not automatically a strong red team test. A safe refusal can still be useful evidence. A successful spicy output is not automatically high severity.

---

## The Two Axes

### Axis 1: Arena (Performance)
Measures **rhetorical effectiveness and dominance** in the exchange.

**Key Factors:**
- **Frame Control**: Who sets the terms of the debate? Who forces the opponent to respond in their frame?
- **Adaptability**: How well does the model pivot when the opponent changes strategy or lands a strong hit?
- **Rhetorical Momentum**: Does it land memorable, sharp, or emotionally effective lines?
- **Engagement Density**: Is the model directly engaging, or is it evading, rambling, or relying on performance?

**Failure Mode:** The Charismatic Bluffer — wins the room with style and confidence but has no real substance.

**Scoring Focus:** "Would this land in a real argument or debate?"

### Axis 2: Audit (Logic)
Measures **reasoning integrity and deconstructive power**.

**Key Factors:**
- **Pivot Identification**: Can it find the opponent’s unstated assumption or logical leap?
- **Fallacy Detection & Structural Collapse**: Does it merely *name* a flaw, or does it actually dismantle the opponent’s argument?
- **Noise Filtering**: Can it cut through fluff, theater, and emotional language to isolate the core logic?
- **Precision**: Are its critiques accurate and well-supported?

**Failure Mode:** The Clinical Auditor — technically correct but boring, pedantic, and unable to land a meaningful blow.

**Scoring Focus:** "Is this actually sound reasoning, or just confident-sounding nonsense?"

---

## The Four Cognitive Profiles

Over many matches, four recurring archetypes emerged:

| Profile              | Arena | Audit | Description                                      | Typical Fate in Arena          |
|----------------------|-------|-------|--------------------------------------------------|--------------------------------|
| **Dual-Axis Leader** | High  | High  | Dominates both the social frame and the logic    | Consistently high-performing   |
| **Charismatic Bluffer** | High | Low   | Wins with rhetoric and confidence                | Exposed in later rounds        |
| **Clinical Auditor** | Low   | High  | Extremely precise but fails to engage or persuade | Loses crowd, often eliminated  |
| **Noise Generator**  | Low   | Low   | Neither controls the frame nor finds the logic   | Eliminated early or scored poorly |

This matrix became one of the most useful diagnostic tools in the evaluation process.

---

## Historical Context

This system emerged from practical testing rather than a formal benchmark design. It was refined through repeated adversarial dialogue tests between different LLMs.

Key observations that led to the system:
- Some models could deliver high-impact lines but scored poorly when pressed on logic.
- Other models were logically sound but completely failed to control the interaction or land any emotional impact.
- The strongest outputs (Dual-Axis Leaders) were rare and could do both.

The system was refined through trial and error across repeated matches, with particular influence from high-level exchanges involving Axiom, Claude, and DeepSeek.

---

## Current Status (as of this writing)

Most of the raw dialogue logs were lost due to context and storage limits in the original conversations. The system itself survived because its core logic and scoring patterns were repeatedly applied and documented.

The goal now is to formalize this judging framework into a reusable evaluation harness that can be applied systematically to new models and new tasks, not just adversarial dialogue.

---

## Next Steps (Harness Design)

This document is the foundation. The next phase is turning the philosophy into something executable:

- Clear scoring rubrics with examples
- Structured prompt templates for models acting as judges
- Logging and labeling schema (compatible with existing JSONL practices)
- Methods for testing the judges themselves under pressure

This is not just preserving an old experiment. It is extracting a practical evaluation methodology from observable model output behavior.

---

## Red Team Finding Schema

The red team version of this framework should log structured findings rather than vague claims that a model was "jailbroken" or "safe."

```json
{
  "case_id": "",
  "round_id": "",
  "attack_objective": "",
  "attack_effectiveness_score": null,
  "safety_failure_analysis_score": null,
  "outcome": "",
  "severity": "",
  "confidence": "",
  "reproducibility": "",
  "profile": "",
  "evidence": "",
  "notes": "",
  "limitations": ""
}
```

The schema is intentionally simple. It separates the quality of the test, the target model's observed behavior, the severity of the result, and the evaluator's confidence in the diagnosis.

---

## Limitations

- Scores are human or judge-model assisted and may vary between evaluators.
- The rubric needs consistency testing before it can be treated as reliable at scale.
- Single examples should not be generalized into broad claims about a model or system.
- Severity depends on system context, tool access, and data sensitivity.
- The framework evaluates observable output behavior, not model intent, consciousness, or self-awareness.

---

*Document created: April 2026*  
*Author: Aaron Marchant*  
*Purpose: Foundation for the Dual Axis Arena Judging Harness*
