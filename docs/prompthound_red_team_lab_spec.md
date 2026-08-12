<!--
CARDO REI methodology applied to this document.
Reference: [CARDO REI Methodology](PROMPTHOUND-DOCS/CARDO-REI.md)
-->

# PromptHound Red Team Lab

## Summary

PromptHound Red Team Lab is a small adversarial evaluation tool for testing AI systems, capturing the response, scoring what happened, logging failures as defects, and exporting a report that another person can actually use.

It is meant for QA, Trust & Safety, and vendor review work. The point is not to prove safety. The point is to document what the model does under pressure and keep that evidence easy to review.

## Problem

Flat pass/fail red-team tools hide too much. A weak attack can make a model look worse than it is, and a strong attack can make it look better than it is. The tool needs to keep both the attack quality and the model outcome visible.

## Product Goals

The tool should turn adversarial prompts into repeatable cases, capture the raw response and metadata, let a human reviewer judge expected versus actual behavior, turn failures into defects, and export a short report with the limits still visible.

## Non-Goals

It is not trying to prove safety, replace human judgment, run a full enterprise platform, or automate truth judgments. Version one is also not trying to cover every model type.

## Primary Users

The first users are QA analysts, Trust & Safety reviewers, vendor evaluation teams, and product teams checking AI risk. It also has to work for a solo builder running structured red-team tests.

## Core Workflow

The workflow is simple: pick a case, choose a target model or API, run the test, review the raw response, mark pass, fail, or partial, add rationale, generate a defect if needed, and export a report.

## Dual-Axis Model

The review uses two separate scores. One is attack quality, which says how strong, realistic, or targeted the test was. The other is outcome severity, which says how bad the model response was in context.

Attack quality should use a 1 to 5 scale, from trivial to extreme. Outcome severity should also use a 1 to 5 scale, from safe to catastrophic.

That split matters because a spicy prompt with a safe refusal is not the same thing as a strong attack that causes a real failure. The tool should keep those apart instead of flattening everything into pass or fail.

## MVP Scope

Version one should stay narrow. The first attack categories are jailbreak, prompt injection, policy override, instruction conflict, structured output drift, and hallucination trigger. The first niche should focus on prompt injection, instruction conflict, and structured output drift because those are the highest-signal cases and they line up with the rest of the repo.

## Core Modules

The attack catalog is a versioned set of cases. Each case needs an id, version, name, category, severity hint, prompt template, variables, expected failure modes, pressure level, tags, mitigation hint, and notes.

The test runner sends a prompt to a target model or API and captures the response. It should store the prompt, response, model, provider, parameters, latency, timestamp, token counts, retry count, and raw metadata.

The review step is a human check. The reviewer marks pass, fail, or partial, writes the expected and actual behavior, adds rationale, gives a confidence score, and scores attack quality and outcome severity. The computed quadrant comes from those two scores.

The defect logger turns a failed review into a defect record. It should already have the title, severity, defect type, repro steps, expected, actual, model, version, environment, reviewer notes, defect status, and patch version if there is one.

The analyst report should be a Markdown file first, with PDF later if needed. It should cover counts, pass/fail/partial summary, top defect types, repeatable patterns, critical findings, recommendations, scope limits, the dual-axis matrix, and repeatability notes.

The limits panel stays visible. It should say plainly that the test documents current behavior, does not prove safety, and only covers a limited sample under a limited scope. If the same behavior already exists in the repo’s case studies, that connection should be named directly so the continuity is obvious.

## Recommended Data Model

JSONL is the right starting point. It keeps the evidence easy to inspect, easy to diff, and easy to move later if we need SQLite for faster queries.

For version one, the storage should stay flat. Keep `AttackTemplate`, `TestRun`, `ReviewDecision`, and `Defect`. There is no need for a persistent report table yet. Reports can be rendered from a list of run IDs and generated summaries, and the quadrant should be computed during review rather than stored separately.

### AttackTemplate

```text
id: str
version: str
name: str
category: str
severity_hint: str
prompt_template: str
variables: list[str]
expected_failure_modes: list[str]
pressure_level: int
tags: list[str]
mitigation_hint: str
notes: str
```

### TestRun

```text
id: str
attack_id: str
attack_version: str
target: dict
prompt: str
response: str
latency_ms: int
token_count: dict
retry_count: int
raw_metadata: dict
timestamp: str
```

### ReviewDecision

```text
id: str
test_run_id: str
status: "pass" | "fail" | "partial"
expected_behavior: str
actual_behavior: str
rationale: str
attack_quality: int
outcome_severity: int
confidence: int
quadrant: str
reviewer: str
timestamp: str
```

### Defect

```text
id: str
test_run_id: str
review_decision_id: str
title: str
severity: str
defect_type: str
repro_steps: str
expected: str
actual: str
model: str
version: str
environment: str
reviewer_notes: str
status: str
model_patch_version: str | null
attack_quality: int
outcome_severity: int
```

## Storage Strategy

### MVP

- JSONL for test runs, reviews, and defects
- human-readable
- easy to inspect with `jq`, `grep`, and plain text tools
- suggested folder layout:
  - `data/templates/`
  - `data/runs/`
  - `data/decisions/`
  - `data/defects/`
  - `data/reports/`

### Later

- SQLite for metadata queries and richer filtering
- optional hybrid mode: JSONL for raw logs, SQLite for indexed summaries

## Suggested Stack

- Python
- LiteLLM for model abstraction
- JSONL storage
- Pydantic for schema validation
- Typer or Click for CLI commands
- Rich for terminal output
- Jinja2 for report templates
- Streamlit or Gradio for a small review UI

## Suggested CLI

- `run` - execute an attack against a model
- `review` - score the response and add rationale
- `defect` - generate a defect record
- `report` - export a summary report
- `catalog` - list or add attack templates

## Repo Lineage

The UI should make the connection to `llm-adversarial-testing` obvious in both language and structure.

Use repo language where it fits:

- case
- evidence
- review
- defect
- methodology
- limits

The intent is for someone who knows the repo to recognize the workflow in under 30 seconds.

## Front-End Layout

The front end should feel like a review console, not a marketing site.
It should visibly reflect the same practices already used in `llm-adversarial-testing`:

- narrow case design
- control vs pressure testing
- structured logs
- human review
- defect-style writeups
- explicit limits
- repeatability notes

The user should be able to see that this tool is the productized version of the repo's existing evaluation workflow.
If that continuity is not obvious on screen, the UI is not doing its job.

### Desktop Layout

Use a three-part desktop structure:

- Left sidebar for navigation
- Center pane for test setup and raw response
- Right pane for review, scoring, and defect generation

### Top Bar

The top bar should make the current context obvious at a glance.

Include:

- project name
- current case
- target model and version
- provider
- run state
- `Run Test`
- `Review`
- `Export`

The run state should be shown as a compact status pill, such as:

- `Idle`
- `Running`
- `Completed`

If useful, include a short latency indicator in the status area.
The current model and version should be visible before any scoring controls.

### Left Sidebar

The sidebar should provide stable orientation and quick navigation.

Include:

- Cases / Attack Catalog
- Evidence Runs
- Defects
- Reports
- Limits / Methodology
- Settings

If the repo already uses terms like `case`, `evidence`, `methodology`, and `qa_artifacts`, keep those terms visible in the UI so the product feels like the same system, not a new unrelated app.
If a label can be expressed in repo language, use the repo language.

### Center Pane

The center pane should support the main workflow:

1. Choose an attack
2. Edit variables
3. Preview the prompt
4. Select the target model
5. Run the test

The center pane should also show the raw response after a run, so the reviewer can inspect the output before scoring it.
The raw response should be the first thing the reviewer sees after a run.

The labels should match the repo's evaluation language where possible:

- case id
- attack template
- pressure case
- control case
- evidence row
- structured output

### Right Pane

The right pane should focus on review and scoring.

Show:

- raw response, if not already visible in the center pane
- expected behavior
- actual behavior
- status: pass, fail, or partial
- attack quality score
- outcome severity score
- reviewer confidence
- rationale
- `Save Review`
- `Generate Defect`

The raw response should be visible before the scoring controls whenever possible.
If scoring appears before evidence, the layout is wrong.

The review fields should echo the existing artifact style from `llm-adversarial-testing` and `qa_artifacts`:

- expected vs actual
- rationale
- conservative interpretation
- note on limitations
- repeatability note

### Limits Panel

The Limits Panel must always be easy to find.

Requirements:

- visible by default on desktop
- collapsible, but reopenable with one click
- compact inline version shown inside test setup and review panes
- full version available in the limits or methodology view

Required limit language:

- This test documents current behavior.
- It does not prove safety.
- Results may vary across models, prompts, and settings.
- Sample size and scope are limited.
- Results may repeat across runs, but that is still only evidence within scope.

If the same behavior appears in the source repo's case studies, name that connection directly so users can see continuity between the research harness and the productized tool.
The compact limit banner should always stay visible in the main view, with one click to the full methodology section.

### Defect Drawer

When a review fails, the defect drawer should open with as much data pre-filled as possible.

Prefill:

- title
- severity
- defect type
- repro steps
- expected
- actual
- attack quality
- outcome severity
- reviewer notes
- case id
- test run id
- methodology reference, if available

This should feel like a continuation of the review flow, not a separate chore.
The defect should feel like the natural next step after review.

### Report View

The report view should be a dedicated screen.

Include:

- summary counts
- quadrant matrix
- repeatability notes
- critical findings
- recommendations
- limits
- `Re-run with same seed`
- `Export evidence pack`

The evidence pack should include raw JSONL plus the Markdown report.
If useful, the pack can also be zipped, but the core deliverable stays Markdown plus raw JSONL.

The report should use the same style as the repo's existing QA and case-study artifacts:

- plain-language summary
- explicit counts
- defect-style findings
- methodology notes
- limits
- repeatability
- conservative claims
The report should keep methodology visible and should not bury limits after the findings.

### Mobile and Tablet

On tablet:

- keep the two-column main flow if space allows
- collapse the sidebar into a drawer if needed

On mobile:

- stack the workflow vertically
- keep the top bar compact
- make the limits banner persistent but small
- prioritize review readability over dense layout

### Visual Style

The visual style should be:

- dark
- dense but readable
- technical
- high contrast
- low animation
- minimal decoration

The overall feel should be a QA or incident review console, not a consumer app.

The visual hierarchy should make the relationship to the existing repo obvious:

- research case at the top
- evidence in the middle
- review and defect handling on the right
- methodology and limits always visible

## Report Shape

The report should answer:

- What was tested?
- What failed?
- How severe was the failure?
- Was the attack itself strong enough to trust the signal?
- What patterns repeated?
- What should a reviewer do next?
- Can the same failure be reproduced across runs?

Suggested sections:

1. Executive summary
2. Scope
3. Test matrix
4. Dual-axis summary
5. Defects
6. Repeatable patterns
7. Recommendations
8. Limits

### Repeatability

If the same attack fails the same way across three or more runs on the same model and version, call it out explicitly. This supports stable-failure analysis without overclaiming beyond the sample.

## Success Criteria

The MVP is successful if:

- a reviewer can run a first test with no code changes
- the response is captured cleanly
- the reviewer can score it quickly
- a defect record is generated from a failure
- a readable report is exported
- the limits stay visible throughout
- repeated runs can be compared without manual spreadsheet cleanup

## Reuse Existing Work

This tool should not start from zero.

Useful prior art already exists in the portfolio:

- `llm-adversarial-testing` for attack patterns, labels, and conservative writeups
- `qa_artifacts` for defect-style Markdown and job-facing test language
- `dual_axis_arena` for dual-axis thinking and report structure

The best path is a new repo for the productized tool, with a `research/` or `prior_art/` folder that points back to the earlier case studies and templates.

## Peer Review Questions

- Is the dual-axis model clear and useful?
- Are attack quality and model severity distinct enough?
- Is JSONL enough for v1?
- Is LiteLLM the right adapter layer?
- Is the report format useful for QA and Trust & Safety reviewers?
- Is the MVP narrow enough to ship quickly?

## Bottom Line

PromptHound Red Team Lab should be a small, practical evaluation tool that helps teams run adversarial tests, score the outcomes, log defects, and export evidence without pretending the results prove safety.
