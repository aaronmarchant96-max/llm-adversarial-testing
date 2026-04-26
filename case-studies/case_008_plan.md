# Case 008 Plan — Transcript Rule Application

## Goal

Design a small evaluation case that tests whether a model can apply simple transcript quality rules to short text-message conversations.

This is not a full rater exam clone. It is a narrow AI QA test focused on rule application, structured output, and consistency.

## What this case tests

The model must inspect a transcript and return a structured decision:

- pass
- reject
- reason codes
- short rationale

## Initial rule set

Keep the first version small:

- spelling_mistake
- emoji_present
- includes_participant_name
- not_possible_over_text
- incoherent_not_human

## Draft output schema

```json
{
  "decision": "pass",
  "reason_codes": [],
  "rationale": "short explanation"
}
First-version scope
8 to 10 examples total
matched expected outcomes
strict JSON output
one scoring script
one curated evidence file if results are useful
Positioning

This case connects LLM evaluation work with AI QA and response evaluation. The point is not to copy any private test. The point is to show a small, reproducible workflow for checking whether a model can apply written quality rules consistently.
