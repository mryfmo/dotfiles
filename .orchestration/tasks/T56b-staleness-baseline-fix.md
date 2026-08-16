# T56b: Staleness baseline fix — per-session first-seen epoch (T61 E2E defect)

task_id: T56b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-harness-composability-integration.md (Phase 3; defect found in T61 live verification)

[memory: failure — Passing $(date +%s) at hook time made staleness detection vacuous: every SessionStart fire compared against "now", so startup sees no future updates and compact-refires miss all mid-session updates. The baseline must be the session's FIRST SessionStart epoch, persisted per session_id.]

## Defect (orchestrator-verified on the deployed hook)

The wired hook `agent-session-staleness check --since "$(date +%s)"`
evaluates the epoch at each hook execution. SessionStart fires at
startup/resume/clear/compact; with since==now, no invocation can ever see
an asset updated before it. The intended catch — a long-running session
whose assets were updated mid-session, detected at the compact/clear
refire — never triggers.

## Fix (exact)

1. Add a `hook` mode to executable_agent-session-staleness:
   `agent-session-staleness hook` reads the Claude hook JSON payload from
   stdin, extracts `session_id` (and `source` if present).
   - State dir: `~/.local/state/agent-staleness/` (0700), one file per
     session_id (0600) containing the first-seen epoch.
   - If no state file: write current epoch, output nothing, exit 0
     (baseline established at true session start).
   - If present: run the existing check logic with --since <recorded
     epoch>; output the existing `restart recommended:` lines when newer
     assets exist.
   - Prune state files older than 7 days on each invocation (bounded,
     best-effort).
   - All failure modes remain silent exit 0; 5s budget unchanged.
2. Rewire the SessionStart hook entry in agent-config.yaml to
   `agent-session-staleness hook` (no shell date substitution), async,
   timeout 5 — regenerate the managed settings template.
3. `check --since <epoch>` CLI mode and doctor integration stay unchanged
   (they are operator-driven and correct).
4. Tests: baseline-write on first call; detection on second call after a
   touched asset with mtime between the two calls; prune behavior;
   missing/garbage stdin -> silent exit 0; existing tests unchanged.

## Allowed files

- home/dot_local/bin/common/executable_agent-session-staleness
- home/dot_agents/agent-config.yaml (the one hook entry)
- home/.chezmoitemplates/claude-settings-managed.json (regenerated only)
- tests/unit/test_agent_session_staleness.py
- Your artifact paths (T56b five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; harness
internal state parsing (the hook payload session_id is documented public
input); changes to check/doctor semantics; hook reordering.

## Validation

1. `make validate-agent-assets` (incl. T55 composition) green.
2. `make unit-test` all green (totals + new count).
3. `make format` exit 0.
4. Fake-HOME two-call transcript proving baseline->detection.
5. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

Five artifacts (T56b set); T45-contract memory add executed and quoted
(the failure marker above is the durable fact — record it with
--kind failure). effects=none expected.
Reply `AGMSG-RESULT v1 task_id=T56b status=ready_for_review`. max_turns=15.
