# QA Artifacts

This folder holds small manual QA and UAT-style artifacts that support the broader evaluation side of the portfolio.

These files are not LLM case studies. They are examples of adjacent QA work: test planning, expected-vs-actual thinking, regression coverage, and defect-oriented documentation.

Current artifacts:

- `debate_furnace_uat_test_plan.md` — a junior QA-style manual test plan for the Debate Furnace app, including scope, user flows, manual test cases, expected results, a sample defect report, a regression checklist, and UAT signoff notes.
- `case_007_uat_test_plan.md` — a job-facing UAT test plan that translates the Case 007 refund authorization boundary scenario into standard QA language with business rules, test scenarios, manual cases, pass criteria, and signoff checks.
- `case_007_test_execution_report.md` — a job-facing execution report showing the observed results from the hosted Case 007 run set, including expected vs actual outcomes, execution summary, and QA signoff notes.
- `defect_report_pack.md` — a small pack of example QA defect reports based on portfolio model-failure patterns, written in standard expected vs actual bug-report language.

The purpose of this folder is to show that the same workflow used in the LLM evaluation repos also carries into product testing:

1. define the behavior worth checking
2. make the scope clear
3. test the visible workflow
4. record expected vs actual behavior
5. keep limitations visible

These artifacts are meant to be practical and job-facing, not inflated into formal QA claims.
