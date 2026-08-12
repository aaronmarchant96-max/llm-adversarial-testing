<!--
CARDO REI methodology applied to this document.
Reference: [CARDO REI Methodology](PROMPTHOUND-DOCS/CARDO-REI.md)
-->

# Debate Furnace UAT Test Plan

## Purpose

This document is a junior QA-style manual test plan for the Debate Furnace app.

The goal is to show how the app can be checked from a user and business workflow perspective: core flows, expected behavior, visible failure states, and basic regression coverage.

## Scope

This test plan covers:

- initial app load
- switching between Debate Furnace and Story Forge
- entering a debate topic
- generating a debate when AI is available
- local fallback behavior when AI is unavailable
- report section rendering
- Story Forge seed interaction
- copy actions
- basic mobile layout checks
- visible error-state clarity

## Out Of Scope

This test plan does not cover:

- backend load testing
- Gemini model quality benchmarking
- browser compatibility across every supported browser version
- accessibility audit beyond basic visual/manual checks
- security testing
- automated test implementation
- Story Forge content quality scoring

## Test Environment

**Application:** Debate Furnace / Story Forge  
**Repository:** `debate-furnace`  
**Primary environment:** Vercel deployment for Gemini-backed custom debates  
**Secondary environment:** local Vite dev for UI/manual checks  
**Device coverage:** desktop viewport and mobile viewport  
**Browser coverage:** current Chromium-based browser

Notes:

- Local Vite development does not serve the `/api/debate` route by itself.
- Custom debates in plain local dev may use the local fallback path unless the API route is available through deployment.

## User Flows

### Flow 1: Open Debate Furnace and run a debate

1. Open the app.
2. Confirm Debate Furnace is visible.
3. Select or enter a debate topic.
4. Run the debate.
5. Review the generated report.

### Flow 2: Switch to Story Forge and interact with a seed

1. Open the app.
2. Switch from Debate Furnace to Story Forge.
3. Review the current seed.
4. Click `Random seed`.
5. Confirm the seed changes and visible context updates.

### Flow 3: Copy and share user-facing output

1. Generate a debate or story output.
2. Use the copy action.
3. Confirm content is copied or a visible success/failure state appears.

### Flow 4: Validate understandable failure handling

1. Trigger a custom debate when the AI path is unavailable.
2. Confirm the app falls back cleanly.
3. Confirm the error notice explains the failure class in understandable terms.

## Manual Test Cases

| ID | Area | Preconditions | Steps | Expected Result |
|---|---|---|---|---|
| DF-UAT-001 | App load | App URL is available | Open the app landing view | App loads without blank screen; Debate Furnace is visible by default |
| DF-UAT-002 | Tool switching | App is loaded | Switch between Debate Furnace and Story Forge | Selected tool opens cleanly; no broken layout or stale overlay remains |
| DF-UAT-003 | Debate input | Debate Furnace is open | Enter a custom topic in the debate input | Input accepts text and keeps the entered topic visible |
| DF-UAT-004 | Starter debate generation | Debate Furnace is open | Select a starter question and run the debate | Debate rounds and report sections render without error |
| DF-UAT-005 | Custom debate with AI available | Deployment environment has working Gemini path | Enter a custom debate topic and run it | Custom debate returns generated content instead of immediate fallback |
| DF-UAT-006 | Custom debate fallback | AI path is unavailable or request fails | Enter a custom debate topic and run it | App uses local fallback and shows a readable failure notice |
| DF-UAT-007 | Report rendering | A debate has been generated | Scroll through the result view | Hinge, key takeaways, strongest cases, cracks, and transcript sections render in order |
| DF-UAT-008 | Story Forge open | App is loaded | Open Story Forge | Story Forge renders without layout break and current seed is visible |
| DF-UAT-009 | Random seed | Story Forge is open | Click `Random seed` multiple times | Seed changes; same seed is not repeated back-to-back when alternatives exist; visible source context updates |
| DF-UAT-010 | Copy button behavior | Debate or story output is present | Click available copy buttons | Copy action succeeds or shows understandable failure feedback; app does not freeze |
| DF-UAT-011 | Mobile layout | Mobile-sized viewport is active | Open both tools and scroll main flows | No obvious horizontal overflow; controls remain reachable; text remains readable |
| DF-UAT-012 | Error-state clarity | Trigger a failed custom debate request | Observe the fallback/error message | Message explains whether the issue is missing key, missing route, failed request, rate limit, or server error |

## Expected Results

The app should behave like a stable prototype:

- core screens should load without runtime breakage
- each tool should open without stale state leaking across views
- starter debates should render a complete report
- custom debates should either generate content or fail into a clear fallback path
- Story Forge should update visible seed context when the random seed changes
- copy actions should behave predictably
- mobile usage should remain readable and usable

## Sample Defect Report

**Defect ID:** DF-BUG-001  
**Title:** Custom debate in local Vite dev always falls back to local engine  
**Environment:** local dev, Chromium, mobile and desktop reproducible  
**Severity:** Medium  
**Priority:** Medium

**Steps to Reproduce**

1. Run the app with `npm run dev`.
2. Open Debate Furnace.
3. Enter a custom debate topic.
4. Click the generate action.

**Expected Result**

If custom debate generation is unavailable, the app should explain why clearly. If the environment is expected to support AI generation, the request should reach the debate API.

**Actual Result**

The app falls back because local Vite dev does not serve `/api/debate` by itself. The UI now reports the failure class, but the custom debate path is still unavailable in plain local dev.

**Business Impact**

A tester or reviewer may assume the AI path is broken when the issue is actually environment setup. This can cause false bug reports and confusion during demos.

**Suggested Follow-Up**

Document the difference between deployed API behavior and plain local Vite behavior in setup notes or tester instructions.

## Regression Checklist

- app still loads into Debate Furnace by default
- switching tools still works
- starter debates still generate reports
- custom debate fallback still renders safely
- failure messages remain understandable
- Story Forge `Random seed` still changes the seed and visible context
- Blueprint, Remix, Source Trail, and copy actions still function
- copy report still works in Debate Furnace
- mobile layout still avoids horizontal scrolling
- no obvious console-blocking runtime error appears during core flows

## UAT Signoff Checklist

- core user flow was executed end to end
- visible output matched the expected workflow
- fallback behavior was understandable
- known limitations were documented
- at least one desktop run was completed
- at least one mobile-sized run was completed
- open defects were recorded with steps and impact
- no blocker issue remains for basic demo use

## Limitations

- This is a manual test artifact, not an automated suite.
- Results depend on environment setup, especially for Gemini-backed custom debates.
- The plan checks product behavior and clarity, not whether debate conclusions are objectively correct.
- Mobile coverage here is basic viewport validation, not full device-lab testing.
