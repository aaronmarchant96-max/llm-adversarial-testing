# case_001 to case_002 methodology note

## Purpose
This note records why case_001 was revised into case_002 and what changed in the findings after the revision.

## case_001 problem
case_001 did not isolate adversarial pressure cleanly because the control and pressure variants used different output-format demands.

- Control used stricter bullet or numbered formatting.
- Pressure used plain text only.
- This made it possible for format difficulty to drive apparent differences between variants.

## Why case_002 was created
case_002 was created to remove that formatting confound.

Both control and pressure in case_002 use:
- plain text only
- word caps
- three turns
- similar structural constraints

The goal was to test framing effects more cleanly by keeping output requirements matched across variants.

## What changed in the results

### Gemma 2B
In case_001, Gemma showed repeated pressure-side format drift.

In case_002, Gemma completed two full repeated runs with stable behavior across both control and pressure:
- case_002_control_eb6a91b7 and case_002_pressure_898c1ed0
- case_002_control_0c43bd7f and case_002_pressure_e6203b3a

This means the earlier case_001 Gemma pressure effect did not replicate once formatting was matched.

### Llama 3.2 1B
Llama produced one partly usable run, but repeated case_002 runs were dominated by timeout/collapse behavior.

This means Llama case_002 results on the current hardware are not clean enough for strong behavioral comparison.

## Current defensible conclusion
case_001 contained a formatting confound.

case_002 corrected that confound by matching output requirements across control and pressure.

Under case_002, Gemma's earlier case_001 pressure effect did not replicate in repeated clean runs.

Cross-model comparison is still limited by runtime instability, especially for Llama 3.2 1B on the current hardware and timeout settings.

## Current limitation
Runtime instability is now the main bottleneck.

Observed issues include:
- timeout-driven collapse
- mixed run quality across repeated files
- hardware sensitivity for slower models

## Next steps
1. Keep case_002 frozen as the corrected comparison case.
2. Improve runtime reliability before making stronger cross-model claims.
3. Keep using run -> log -> summarize as the standard workflow.
4. Build case_003 as a stronger matched-format pressure case rather than editing case_002.

