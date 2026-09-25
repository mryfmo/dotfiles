# T4 RESULT
status: ready_for_review
cost: n/a

## Changes
Worktree: `/Users/mryfmo/Workspace/dotfiles/.claude/worktrees/agmsg-dispatch`, branch `feat/agmsg-dispatch`. No commit/push/PR.
- Added one bash dispatch helper using installed agmsg identifier/storage helpers, send.sh, sqlite3, jq and herdr.
- Idle pane receives metadata-only wake; working pane receives none. Polls read_at every five seconds, bounded by timeout (default 120 seconds per round); idle wake gets one retry.
- Six stdlib tests exercise idle read, working read, idle unread/retry, working unread/no wake, default storage and invalid timeout. Alternate storage is used in the main fixture.
- One paragraph in Orchestrator Playbook step 6 establishes dispatch use. Skill is not generated; asset and skill validators pass.

## Evidence
Red-first missing-script failures preceded implementation. Fixture quote escaping was corrected after first green attempt failed at send.
401 unit tests passed; shellcheck, shfmt, asset validator, skill validator, diff check and evidence-backed Crit gate passed. Full output: `.orchestration/validation/dot-agmsg-dispatch-T4-a01.md`.
Crit JSON: `/Users/mryfmo/Workspace/dotfiles/.claude/worktrees/agmsg-dispatch/.agents/worklog/codex/t4-crit.json`; receipt alongside it.

## Limits / integration
- Wake command includes BOTH team and recipient: actual inbox.sh requires two arguments, unlike task shorthand.
- Matching-route max(id) follows task specification and assumes serialized sends for one team/from/to route. Concurrent same-route senders would require send.sh to return the insertion id; external script edits were forbidden.
- No operator-home apply or real worker wake was performed. Native read-only pane listing confirmed result.panes[].agent_status shape; behavior was tested with fake CLIs and a real temporary SQLite schema.
- read_at means inbox consumption, not task completion. Orchestrator remains responsible for RESULT/acceptance and integration/live verification.
- No external agmsg asset edits or new dependencies.

## Durable decision
[memory:decision] Orchestrators dispatch to Codex workers with agmsg-dispatch, which sends, wakes idle panes and blocks for read_at; bare send.sh to an idle worker is a protocol violation.
Memory ID: 7ffc6b62-a536-4423-8d9d-10810066514a.
Exact memory command and output are in validation; command executed in canonical repository:
`python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'Orchestrators dispatch to Codex workers with agmsg-dispatch, which sends through agmsg, wakes an idle pane, and blocks until read_at is set; a bare send.sh to an idle worker is a protocol violation. Introduced by dot-agmsg-dispatch-T4-a01; integration pending orchestrator acceptance.'`

## PR173 revision (2026-09-25; supersedes original timeout/retry description)
status: ready_for_review
cost: n/a

All four findings addressed in agmsg-dispatch worktree, without commit/push:
- Resolve exactly one pane and its status before send; missing/unavailable pane exits 1 and inserts nothing.
- One receipt-wait deadline spans both rounds. At the midpoint, re-query status before deciding whether to wake; this handles working-to-idle and avoids waking an idle-to-working pane again.
- EXIT diagnostics identify sent message ID on post-send delivery failures and tell callers to verify receipt before resending. If DB lookup itself fails before recovering the ID, diagnostic explicitly says unknown; never claim unsent.
- Step 6 requires dispatch for Herdr-backed workers, while pane-less workers retain send.sh with explicit read_at verification.

Five new tests failed red-first; 11 focused tests and all 406 unit tests passed. Shellcheck/shfmt/validator/diff/Crit gate passed. Shellcheck SC2329 for the EXIT-only callback was scoped-suppressed with its invocation reason. No live wake from this revision; tests use fake CLIs and temporary SQLite. Existing serialized-sender correlation ceiling remains.
Timeout bounds receipt polling; external herdr/send CLI latency is not a subprocess execution timeout.
Review evidence: .claude/worktrees/agmsg-dispatch/.agents/worklog/codex/t4-revise-crit.json, receipt alongside.

[memory:decision] Validate pane before send, refresh status before retry, share one receipt timeout, retain sent-ID failure diagnostics and pane-less delivery support.
Memory command (canonical repo): `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'PR173 revision: validate Herdr pane before dispatch send; recheck status at the midpoint retry and share one receipt-wait deadline. Post-send delivery failures identify the sent message so callers verify it before resending. Herdr-backed workers require agmsg-dispatch; pane-less workers retain send.sh and explicit read_at verification.'`
Memory ID: 95e4a7ea-7a8c-48e3-b184-f63a8ae02e60.
