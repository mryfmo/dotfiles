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

- 2026-10-01T17:50Z (UTC) **resumed**: Codex pause lifted by the operator.
  Seat re-created with the installed `herdr-agents --add-worker
.claude/worktrees/worker-sec --kind codex --profile security` (the
  installed launcher is the T42-era build — no socket derivation, no
  `--ready-timeout`, no `linkage=` line — so `HERDR_SOCKET_PATH` was
  exported and the linkage PING sent by hand; nothing from this seat counts
  as T45/T46 live-leg evidence). Placement record overwritten to wQ:p2
  (workspace `dotfiles worker worker-sec`); spawn.sh's `_record_placement`
  resolves the legacy path and overwrites it, so the stale wM:p2 record
  caused no conflict. `MODEL_PROFILE_SECURITY_CODEX_ARGS=--profile security`
  → `~/.codex/security.config.toml` model gpt-6-astra / high. PING 648 →
  PONG 649 (alive: WIP present at f45cf73, 620 tests OK; the worker says
  `validate-agent-assets` passed "after network escalation" and that it
  restarted an independent review after a credit error — the escalation is
  a protocol deviation to be judged at RESULT: workers must PONG blocked,
  never approve). Resume dispatched as revision 3 (task amendment r3:
  keep the WIP, rebase onto origin/main a5f33ee and name the base sha,
  PONG blocked on any denied `.git` write), msg 650, read 17:54:32Z.
  Pre-check: `git log f45cf73..origin/main -- <five allowed files>` is empty.
- 17:54:57Z PONG 651 **blocked**: `git add` of the five files failed with
  `Unable to create …/.git/worktrees/worker-sec/index.lock: Read-only file
system` (the Codex workspace-write root is the worktree; the worktree's
  git dir, objects and refs are in the main `.git`); the worker then staged
  them through an escalation it calls "r2-authorized" (PING 527 did say
  "use your normal escalation once"), and asked the orchestrator to commit
  and rebase. Diff now 294/18 after its own review fixes; 53 guard tests
  pass; review JSON + receipt present; no commits/push/PR.
- Orchestrator: an orchestrator-side `codex sandbox` probe of the writable
  paths was declined by the operator; the worker's denial text is the
  evidence. Operator decision (AskUserQuestion): **the operator answers the
  Codex escalation prompts in the wQ pane** (rule: only the human operator
  answers a permission prompt); the orchestrator does not touch worker-sec;
  the structural fix is drafted as **T50** (Codex writable roots for
  worktree git dirs). Ruling sent as ACCEPTANCE status=revise and appended
  to the task's r3 amendment.
- 21:00:56Z PONG 653 alive: operator-approved git writes done; rebased onto
  a5f33ee; head 0dfe823; PR #221 open and mergeable, CI running; `git push`
  succeeded but recording the upstream hit an existing `.git/config.lock`
  (the worker touched no lock); 625 tests passed before the rebase, rerun in
  flight; RESULT after CI and the integration gates.
- 21:01:55Z orchestrator PING 654: stale lock removed; do not set an
  upstream (`.git/config` write stays denied by design), plain push.
- 21:14:21Z PONG 656 alive: PR #221 head now c67ec77 — the first macOS CI
  run failed on a `/var` vs `/private/var` evidence-path alias; root cause
  fixed with a regression test (54 guard tests); 675 local tests on the
  prior head; CI restarted; final sweep and gates after the test jobs.
  Audit of 0dfe823 started (pre-screen); c67ec77 to be audited as well.

[memory:failure] T40: a Codex worker seated in a nested worktree cannot
write the shared `.git` (refs, config) without escalation because the Codex
workspace-write sandbox is scoped to the worktree; a failed sandboxed write
can leave an empty read-only `.git/config.lock` that blocks later writes.
