<!--
CARDO REI methodology applied to this document.
Reference: [CARDO REI Methodology](PROMPTHOUND-DOCS/CARDO-REI.md)
-->

# QA Test Plan: Case 008 Guideline Evaluation and Rater Validation

## Objective

This document translates Case 008 into standard QA and guideline-evaluation language.

The goal is to validate whether a model can apply a narrow set of transcript moderation rules consistently, return the expected decision and reason codes, and keep the rationale grounded in the actual transcript text.

## Scope

This test plan covers:

- transcript rule interpretation
- expected decision accuracy
- expected reason-code accuracy
- rationale quality
- repeatability across multiple clean runs
- pass and reject examples inside the same fixed evaluation set

## Out Of Scope

This test plan does not cover:

- broad moderation performance claims
- live production transcript streams
- multilingual moderation
- policy areas outside the defined Case 008 rule set
- automated remediation or retraining

## Guideline Rules Under Test

The Case 008 evaluation uses a fixed transcript moderation schema with:

- `decision`
- `reason_codes`
- `rationale`

Allowed reason codes:

- `spelling_mistake`
- `emoji_present`
- `includes_participant_name`
- `not_possible_over_text`
- `incoherent_not_human`

The tested expectation is that the model:

- returns a valid structured decision
- applies the correct reject reason when a violation is present
- does not miss direct violations
- does not invent evidence to justify a rejection

## Test Data

The test data is a fixed set of `8` hand-crafted transcript examples:

| Example Type | Purpose |
|---|---|
| clean pass examples | confirm the model does not over-reject |
| explicit reject examples | confirm the model detects rule violations |
| rationale-sensitive reject example | confirm the model grounds the reason in the actual transcript |

The examples are probe cases, not random production samples.

## Test Environment

**Case:** `case_008`  
**Repository:** `llm-adversarial-testing`  
**Model:** Groq-hosted `llama-3.1-8b-instant`  
**Trials:** `4` clean repeated trials  
**Rows per trial:** `8`  
**Total scored rows:** `32`

Evidence sources:

- `case-studies/case_008.md`
- `practice_rag/configs/case_008_rater_validation.json`

## User Story

As a QA or evaluation reviewer, I want the model to apply a narrow transcript rule set consistently and explain the decision using the actual transcript evidence, so that pass/reject output can be reviewed against a clear moderation standard.

## Test Scenarios

### Core Scenarios

| ID | Scenario | Expected Result |
|---|---|---|
| C008-QA-001 | Clean pass example | Return `pass` with no false reject reason |
| C008-QA-002 | Explicit spelling mistake violation | Return `reject` with `spelling_mistake` |
| C008-QA-003 | Explicit emoji violation | Return `reject` with `emoji_present` |
| C008-QA-004 | Explicit participant name violation | Return `reject` with `includes_participant_name` |
| C008-QA-005 | Not-possible-over-text violation | Return `reject` with `not_possible_over_text` and a grounded rationale |
| C008-QA-006 | Clearly incoherent transcript | Return `reject` with `incoherent_not_human` |

## Manual Test Cases

| ID | Preconditions | Steps | Expected Result |
|---|---|---|---|
| C008-TC-001 | Case 008 config and runner are available | Run the fixed 8-example evaluation set | All rows capture successfully and remain schema stable |
| C008-TC-002 | Clean repeated trials are available | Compare outcome patterns across the repeated runs | Held and failed examples remain stable across reruns |
| C008-TC-003 | Reject examples are present | Compare expected reject reasons to actual reason codes | The model uses the correct reject reason for each violated rule |
| C008-TC-004 | Rationale field is present | Inspect rationale text on reject rows | Rationale stays grounded in evidence present in the transcript |
| C008-TC-005 | Stable failure rows are identified | Review the known Case 008 drift set | Under-detection and rationale-hallucination patterns remain visible and classifiable |

## Expected Result Summary

Pass criteria for a strong run:

- rows are captured successfully
- structured output remains stable
- pass cases remain pass
- explicit reject cases are detected correctly
- reason codes match the actual rule violation
- rationale does not invent evidence

## Observed Result Summary

Observed clean repeated result from the current Case 008 run set:

- `4` clean repeated trials
- `8 / 8` rows captured per trial
- stable semantic outcome in every trial
- `3 / 8` meaning held per trial
- `5 / 8` meaning drift per trial
- `12 / 32` aggregate meaning held
- `20 / 32` aggregate meaning drift

Stable failure profile:

- under-detection on explicit spelling, emoji, participant-name, and not-possible-over-text violations
- one repeated rationale hallucination where the model rejects for an invented participant-name reason instead of the actual rule violation

## Sample Defect Types

- under-detection of an explicit reject condition
- incorrect reason code on a reject result
- rationale hallucination
- schema-stable output with wrong moderation decision

## Regression Checklist

Before signoff, confirm:

- all 8 rows capture cleanly in each repeated trial
- the same held set and failure set remain identifiable
- pass cases are not over-rejected
- reject cases are not silently passed
- rationale text still matches the transcript evidence
- evidence links still point to the correct case-study material

## Signoff Notes / Checklist

- scope is limited to the narrow Case 008 guideline set
- repeated-trial structure is documented clearly
- expected decisions and reason codes are defined before review
- observed drift is classified explicitly
- rationale quality is treated as part of the QA result
- results are not generalized beyond this small controlled set

## Limitations

- This is a small controlled rater-validation probe set.
- The examples are hand-crafted rather than sampled from production traffic.
- Results are specific to the tested model, prompt format, and rule set.
- The case is useful for guideline evaluation and rubric testing, not for broad moderation benchmarking.
