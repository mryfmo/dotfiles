# T65: Pi installation base — pinned tool, dot_pi skeleton, validation category

task_id: T65
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-pi-worker-integration.md (Phase 1)
analysis: .orchestration/analysis/pi-harness-research.md

[memory: decision — Pi enters the toolchain version-pinned via mise (v0.84.2 baseline), with a chezmoi-managed ~/.pi/agent skeleton whose defaultProjectTrust denies non-interactive project-resource loading, and a validate-agent-assets category guarding the pi extension sources.]

## Goal

The install/distribution skeleton for the Pi worker plan — no Pi execution
in this task (execution starts at T67).

## Allowed files (edit boundary)

- home/dot_mise/config.toml (ONE new pinned entry:
  npm:@earendil-works/pi-coding-agent at exactly 0.84.2, following the
  existing npm-backend pin style; do NOT touch existing entries; do NOT
  regenerate mise.lock — the orchestrator does that at T72 distribution)
- home/dot_pi/agent/settings.json (NEW chezmoi source: minimal valid Pi
  settings with defaultProjectTrust set to the deny/untrusted value —
  verify the exact key/value against the pinned version's docs or source
  READ-ONLY via the GitHub raw URLs; cite the source line in the report)
- home/dot_pi/agent/extensions/.gitkeep (placeholder for T66/T69)
- scripts/validate-agent-assets.py (NEW category "pi assets": for now,
  (a) if home/dot_pi exists, settings.json parses as JSON and contains
  defaultProjectTrust with the deny value; (b) extensions dir exists;
  (c) the mise entry for pi-coding-agent is exact-version pinned (no
  ranges, no latest). Hash checks come in T66/T69.)
- tests/unit/ (matching module)
- Your artifact paths (T65 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; make upgrade or any real
install; running pi; changing existing mise pins; dependency changes.

## Work order (exact; ambiguity -> ask via agmsg)

1. Read the existing npm-backend entries in home/dot_mise/config.toml and
   add the pi pin in identical style.
2. Verify the settings key for non-interactive project trust against the
   PINNED version (raw.githubusercontent.com at the v0.84.2 tag if
   available, else main with the caveat noted): the docs call it
   `defaultProjectTrust`; confirm accepted values and pick the one that
   REFUSES loading project-local extensions/settings without a persisted
   trust decision. Quote the source in the report.
3. Author the minimal settings.json (only keys you can verify; no
   speculative config).
4. Implement the validation category + tests (fixtures for: valid tree
   passes; missing defaultProjectTrust fails; version range instead of
   exact pin fails).
5. Gates: make format / unit-test / validate-agent-assets green.

## Validation (record in validation artifact)

1. Gate outputs (all green).
2. Quoted upstream source for the trust key/value.
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

Five artifacts (T65 set); memory add with the decision fact; effects=none
(no real install happens here).
Reply `AGMSG-RESULT v1 task_id=T65 status=ready_for_review`. max_turns=20.
