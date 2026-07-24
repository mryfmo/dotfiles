# T23: Fix worker-wake guidance in the shared agmsg-orchestration skill

## Objective

The shared skill documents an unreliable wake procedure. Replace it with the
verified-correct one so any orchestrator wakes workers reliably.

## Background (verified 2026-07-23)

- `pane send-text` followed by `send-keys Enter` races the codex TUI composer:
  the Enter can be consumed before the text is registered, leaving the prompt
  unsubmitted. With turn-based delivery this deadlocks the worker (observed:
  worked twice, then failed 3 consecutive times on T22 acceptance delivery).
- `herdr pane run <pane_id> "<text>"` sends text plus Enter in one call and
  delivered on the first attempt. `herdr agent --help` states: "agent send
  writes literal text; use pane run when you want command text plus Enter".

## Change

In `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, replace Orchestrator
Playbook item 4:

> 4. Start worker panes if needed. With herdr, send the worker prompt text into the pane and submit it with a carriage return; sending text alone may leave it unsubmitted.

with:

> 4. Start worker panes if needed. With herdr, wake or prompt a worker with `herdr pane run <pane_id> "<text>"` (text plus Enter in one call). Do not use `pane send-text` followed by `send-keys Enter`; the separate Enter races the TUI composer and fails nondeterministically. After every wake, verify delivery via the messages.db `read_at` column and only escalate to a pane restart if a verified `pane run` wake stays undelivered.

Also update the Pitfalls bullet:

> - Do not assume `herdr` text injection submits automatically; send Enter/CR.

to:

> - Do not wake workers with `pane send-text` + `send-keys Enter`; use `herdr pane run` and verify `read_at` in messages.db.

If `home/dot_agents/skills/agmsg/SKILL.md` (or its scripts' docs) documents the
same send-text+Enter pattern, apply the same correction there; otherwise leave
it untouched.

## Verification

- `uv run --with pyyaml scripts/generate-agent-configs.py --check` (skill
  symlink outputs unchanged or regenerated cleanly).
- `make unit-test` green; `make validate-agent-assets` green.
- Branch `docs/agmsg-nudge-pane-run` from origin/main in a separate worktree,
  single commit `docs(agmsg): wake workers with pane run and verify read_at`,
  push, English PR, CI green. Do NOT merge before acceptance; after acceptance
  merge + guarded main sync as in T21/T22.

## Allowed files

- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `home/dot_agents/skills/agmsg/SKILL.md` (only if it repeats the bad pattern)
- Regenerated `home/dot_claude/skills/**/symlink_*.tmpl` if the generator
  requires it (it should not for content-only edits).
- Artifacts below.

## Forbidden actions

- Any behavior/code change (docs only), local bats, make upgrade, merging
  before acceptance, committing `.orchestration/` or `.agents/`, secrets.

## Expected artifacts

- report: .orchestration/reports/T23-agmsg-nudge-guidance.md
- validation: .orchestration/validation/T23-agmsg-nudge-guidance.txt
- sandbox: .orchestration/sandboxes/T23-agmsg-nudge-guidance.md
- learning: .orchestration/learning/T23-agmsg-nudge-guidance.md
- autoskill: .orchestration/autoskill/runs/T23-agmsg-nudge-guidance.md

## Done signal

AGMSG-RESULT v1 status=ready_for_review. max_turns=15
