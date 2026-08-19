# Follow-ups — llm-adversarial-testing (hiring-manager pass)

Paused 2026-08-12. Revisit when back on this repo.

## Assessment summary
Repo is decent for junior/entry AI-eval + QA. Strongest signal = framing discipline
(no overclaiming, case_002 falsifies its own earlier idea). Cleanup already removed the
red CI badge + recovered uncommitted work.

## Open items (in priority order)
1. Add `requirements.txt` (or `pyproject.toml`) — pydantic + any other deps. Makes the
   red_team_lab + dataset_guard runnable without guessing deps. ~5 min, low risk.
2. Populate one real run through `prompt_hound_red_team_lab` — write actual
   `data/runs/*.jsonl` + `data/reports/*.md`. Turns the scaffolding into evidence.
3. Merge PORTFOLIO.md into README (or make PORTFOLIO.md the sole "for recruiters" entry
   point) — currently two overlapping docs compete for the same job.

## Other notes
- `public_transit_guard/` is an empty dir (stray transit* files already removed).
- CI: GitHub Actions billing-locked; three workflow checks (structure/JSON/syntax) are
  reproducible locally.
