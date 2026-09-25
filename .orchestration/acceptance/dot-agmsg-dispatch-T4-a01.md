# Acceptance: dot-agmsg-dispatch-T4-a01

status: accepted
date: 2026-09-25
reviewer: claude-deep-dot (orchestrator, adversarial review)
cost: n/a

## Independent re-derivation

- Script read in full: send → max(id) on the route → pane status → wake if not working → poll read_at (≤5 s steps, bounded) → one idle retry → exit 1. Body never printed. Storage via `lib/storage.sh` (AGMSG_STORAGE_PATH honored).
- Live E2E: orchestrator ran the worktree script against the real worker (AGMSG-PING); read_at within 5 s, exit 0.
- `make unit-test` OK (401 incl. 6 new), shellcheck, shfmt, asset validator, diff check, review guard with `t4-review.md`.
- Known limit (accepted): a missing pane id makes `jq -e` fail under `set -e` without a specific message; max(id) assumes serialized sends per route (documented in the script).

## Integration

Committed on `feat/agmsg-dispatch`, PR #173.

## Revision 1 (PR #173 Codex bot review, commit 71fc1b2) — all four valid

1. dispatch:71 — re-query pane status before the retry decision (a pane that went idle after send is exactly the stall this helper exists to prevent).
2. dispatch:73 — one overall deadline shared by both waits (currently ~2× timeout).
3. dispatch:44 — resolve/validate the pane BEFORE send.sh so a bad pane id cannot leave an inserted-but-unannounced message; on post-send failures print the message id.
4. SKILL.md:118 — dispatch is required for herdr-pane-backed workers; for pane-less workers keep `send.sh` + read_at verification as the documented path.

## Revision 1 result

status: accepted — pane validated before send (missing pane inserts nothing), single shared deadline with halfway status recheck, EXIT trap reports the sent id on any post-send failure, skill keeps send.sh for pane-less workers. Five new unit cases; orchestrator reran unit suite OK, shellcheck, shfmt, validator, diff check. Pushed as 9188003 on PR #173.
