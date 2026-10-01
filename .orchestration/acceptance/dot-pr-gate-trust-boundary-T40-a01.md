# Acceptance: dot-pr-gate-trust-boundary-T40-a01

Revision 2 dispatched 2026-09-29T20:59Z to `codex-security-dot-a006`
(security profile, gpt-6-astra, workspace wM, worktree worker-sec) via
`poke.sh --body-file` plus a bus record (message 524; 523 was a truncated
duplicate caused by the sandboxed/unsandboxed `$TMPDIR` split — ignore).

## Timeline

- 21:00Z PONG blocked: the Codex sandbox treats the shared `.git` (outside
  the worktree) as read-only; an escalated retry then hit a stale, empty
  `.git/config.lock`; the branch came out as `pr-gate-trust-boundary`.
- 21:01Z RESULT status=blocked (crossed the orchestrator's PING 527).
- 21:01Z orchestrator: removed the empty lock (hygiene exemption), ruled:
  rename the branch yourself; worklog plan/todo WAIVED for T40; review JSON
  and receipt go to `.orchestration/validation/…-review.json` / `-receipt.md`;
  CompactionDB add and artifact copies to the main checkout are the
  sanctioned exceptions to work-only-in-worker-sec. Sent as ACCEPTANCE
  status=revise (529).
- 21:02Z PONG alive: branch `fix/pr-gate-trust-boundary` restored at
  f45cf73; design posted (query `gh pr view baseRefName/baseRefOid/headRefOid`
  before running any collector; accept the exact base or a safe older
  ancestor outside the PR-only first-parent chain).
- 21:08Z **PAUSED at the operator's instruction (Codex rate limit).** The
  worker holds uncommitted edits in worker-sec (`pr-integration.md`,
  `pr-feedback.py`, `require-crit-review.py`, both tests) plus the five
  artifact drafts. The seat is left in place so no work is lost; nothing is
  sent to it until the operator lifts the pause. The Codex audit lane shares
  the same account, so audits of pending RESULTs (T43 rev2) also queue.

[memory:failure] T40: a Codex worker seated in a nested worktree cannot
write the shared `.git` (refs, config) without escalation because the Codex
workspace-write sandbox is scoped to the worktree; a failed sandboxed write
can leave an empty read-only `.git/config.lock` that blocks later writes.
