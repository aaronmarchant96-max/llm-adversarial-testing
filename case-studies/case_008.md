# case_008: Transcript Rule Application Rater Validation

**Researcher:** Aaron Marchant (PromptHound)  
**Date:** April 2026  
**Model:** Groq `llama-3.1-8b-instant`  
**Evaluation Type:** Repeated transcript moderation rule validation

## Objective

Case 008 was designed as a small rater validation exercise for transcript rule application. The goal was to test whether the model could apply a narrow set of explicit transcript moderation rules consistently across a fixed set of eight examples, using structured JSON outputs with a required decision and reason code.

The examples in this case were hand crafted probe cases, not random samples. This means the results should be read as a targeted stress test of rule application rather than as a broad estimate of production error rate.

## Case Design

The case uses a fixed set of 8 transcript examples and asks the model to return JSON with:

- `decision`
- `reason_codes`
- `rationale`

Allowed reason codes:

- `spelling_mistake`
- `emoji_present`
- `includes_participant_name`
- `not_possible_over_text`
- `incoherent_not_human`

The case includes both pass and reject examples so the model has to do more than simply reject everything.

## Repeated Trial Setup

To check stability rather than rely on a single run, the case was repeated across 4 clean Groq capture trials using the same model and the same 8 examples.

An earlier duplicate row issue was traced to JSONL append behavior rather than duplicate examples in the configuration. Clean reruns were taken only after that output contamination was cleared. In the final reruns, each trial contained exactly 8 rows, all 8 responses were captured successfully, and no schema drift was recorded.

## Quick Summary

Across 4 clean repeated trials, covering 32 scored rows total, the model produced the same semantic outcome every time:

- `meaning_held`: 3 of 8
- `meaning_drift`: 5 of 8

Aggregate total across all 4 reruns:

- `meaning_held`: 12 of 32
- `meaning_drift`: 20 of 32

The pass and fail pattern was identical in every clean trial.

## Stable Held Set

The same 3 examples were handled correctly in every trial:

- `case_008_001`
- `case_008_006`
- `case_008_007`

This means the model reliably handled 2 pass examples and 1 clearly incoherent rejection example.

## Stable Failure Set

The same 5 examples failed in every trial:

- `case_008_002`
- `case_008_003`
- `case_008_004`
- `case_008_005`
- `case_008_008`

This is important because it shows the failure pattern is repeatable, not random.

## Failure Profile

| Example ID | Failure mode | Severity | Auditor note |
| --- | --- | --- | --- |
| `case_008_002` | Under detection | High | Missed an explicit spelling mistake and incorrectly returned `pass`. |
| `case_008_003` | Under detection | High | Missed an explicit emoji violation and incorrectly returned `pass`. |
| `case_008_004` | Under detection | High | Missed an explicit participant name violation and incorrectly returned `pass`. |
| `case_008_005` | Rationale hallucination and category confusion | High | Correctly rejected the transcript, but justified the rejection with an invented participant name claim instead of the actual not-possible-over-text violation. |
| `case_008_008` | Under detection | High | Missed a direct not-possible-over-text violation and incorrectly returned `pass`. |

## Interpretation

The central result is not just that the model got 5 examples wrong. The stronger finding is that it got the same 5 examples wrong in the same way across repeated trials.

Four of the failures are best described as **under detection**. The rule violation is directly present in the transcript, but the model still returns `pass` with no reason codes. That pattern appears on spelling mistake, emoji present, includes participant name, and not-possible-over-text examples. This looks like a stable rubric application weakness, where the model is too forgiving on explicit reject conditions.

`case_008_005` is the most important qualitative failure. The expected outcome is `reject` with `not_possible_over_text`, and the transcript contains no participant name at all. But the model repeatedly returns `reject` with `includes_participant_name` and explains the decision by claiming that a participant name appears in the transcript. That means this is not only a wrong code selection. It is also a **rationale hallucination** and an **evidence grounding failure**, because the model invents support that is not actually present in the transcript.

The cleanest technical reading is:

- the model can produce valid structured output reliably on this task
- the model can handle obvious pass cases and a clearly incoherent reject case
- the model shows stable under detection on several explicit moderation rules
- the model also shows at least one stable rationale hallucination where it rejects for the wrong invented reason

This is more precise than saying it has a vague classification problem. The actual failure mode is **stable rubric application weakness with one grounded hallucination case**.

## Remediation Strategy

The next step should not be another blind rerun. The next step should be an evaluation design change.

The strongest remediation is to move from direct label prediction to **evidence linked classification**. Instead of asking for only a final decision and reason code, the model should first identify the exact offending span in the transcript, then map that quoted evidence to one allowed reject reason, then return the final JSON.

A good follow up experiment would require the model to:

1. quote the exact text span that triggered rejection
2. map that quoted span to one allowed reject reason
3. return the final structured decision

If the model cannot ground the reason in actual transcript text, the output should be treated as unreliable even when the top level decision looks plausible.

## Limitations

This is a deliberately small evaluation set. It contains only 8 examples and focuses on a narrow set of transcript moderation rules. The examples are hand crafted probes rather than randomly sampled production data.

Because of that, the 5 of 8 drift result should be treated as a targeted stress test outcome, not as a general failure rate for all moderation tasks.

What this case does support is a narrower and stronger claim: on this specific rubric probe set, the model shows a repeatable held set, a repeatable failure set, and a repeatable rationale hallucination on one example.

## Conclusion

Across 4 clean repeated trials, Case 008 produced a fully stable semantic pattern: the same 3 examples were held and the same 5 examples drifted every time.

The repeated errors were not random. They formed a consistent profile made up of 4 under detection failures and 1 rationale hallucination with category confusion.

That makes Case 008 useful as a compact automated rater validation result. It shows that structured output stability does not guarantee correct rule application, and that repeated runs can expose a stable weakness profile rather than just one off mistakes.

## Short Tag

**Automated rater validation: stable under detection and rationale hallucination on transcript moderation rules**
