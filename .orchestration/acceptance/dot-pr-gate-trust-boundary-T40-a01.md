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
- Audits (pre-screen, orchestrator-invoked): 0dfe823 **correct**, c67ec77
  **correct** (both from git objects; CI unverified by the auditor).
- 21:31:55Z PONG 661 alive: c67ec77 CI green after one transient
  ccstatusline-timeout rerun; the Codex GitHub review left four inline
  comments (two distinct valid P1s) → fixed in 10dfc10 ("fixed dispositions
  use the authenticated GitHub base range; `GH_REPO` cannot redirect
  collection"), three repros failing before the fix, 58 guard tests; PR
  #221 updated, CI running; the worker will disposition all four as
  `fixed:10dfc10` after its final sweep. Audit of 10dfc10: **correct**
  (repo binding, authenticated base range, collector arguments and
  regression tests consistent; CI unverified by the auditor). Orchestrator
  check: the base collector at bb3370a already accepts `--repo`, so the
  gate's base-collector call cannot fail on that flag.
- 21:56:11Z **RESULT 662** (ready_for_review): PR #221 head 10dfc10, CI
  green Linux+macOS, 680 tests (1 skip), positive gate exit 0 with
  `--base origin/main`, negative gate exit 1 with `--base HEAD`, eight
  artifacts synced to the main checkout, CompactionDB fdccdfbf.

## Review (orchestrator, from git objects)

- Three commits, each audited **correct** by the Codex auditor (0dfe823,
  c67ec77, 10dfc10). Diff vs main: exactly the five allowed files (393/25).
- `pr_base_errors`: repo bound through `gh repo view` with `GH_REPO`
  stripped and compared with `evidence.repo`; `gh pr view --repo <repo>`
  for head/base; `--base` accepted when equal to the GitHub base, an
  ancestor outside HEAD's first-parent chain, or an advanced base with the
  identical merge-base (the live case: GitHub base a5f33ee, local
  origin/main 5a43c85 after the T46 merge). The collector is the GitHub-base
  SHA's `scripts/pr-feedback.py` run with `--repo`, and the collected
  document's `repo`/`head_sha` are checked. `fixed:<sha>` ranges use the
  authenticated `base_sha`, not the user-selected base (Codex P1). Evidence
  path: `.orchestration/validation/*-pr-feedback.json` only, lexical and
  resolved, with repository-parent aliases (macOS `/var`) normalized above
  the repo only. `gh_graphql`: `-F` for `int` only. Orchestrator check: the
  base collector at bb3370a already takes `--repo`.
- Sweep: orchestrator re-collection of #221 at 10dfc10 is item-identical to
  the worker's evidence (20 = 20, no missing/extra). Dispositions verified:
  6 `fixed:10dfc10` (four Codex inline comments = two distinct P1s, both
  root-fixed in 10dfc10, plus their two review containers), 14
  `not-applicable` (11 runner notices, 1 Homebrew tap warning with a grep
  showing none of the taps in `home`/`install`, CodeRabbit skipped comment
  and status).
- Gate: `AGENT_REVIEWED=1 REVIEW_EVIDENCE=…-review-receipt.md BASE=origin/main
PR_FEEDBACK_EVIDENCE=…-pr-feedback.json make require-crit-review` in
  `.claude/worktrees/orchestrator-review` at 10dfc10 → exit 0 (the PR's own
  new guard, with the live advanced-base case). Orchestrator evidence
  `…-crit-comments.json` + `…-review-receipt.md`; the worker's own
  `…-review.json` + `…-receipt.md` (reviewer: codex, addressed) stay as
  process evidence.
- Protocol dispositions: (a) git metadata writes after the ruling ran under
  operator-approved escalations in the wQ pane — compliant. (b) Before the
  ruling, the worker staged with an escalation it attributed to the r2 PING
  527 ("use your normal escalation once") — a predecessor instruction that
  the current rule forbids; no harm, recorded, superseded by the ruling and
  by T50. (c) Network escalations for PyYAML (`uv run --with pyyaml` under
  `network_access = false`), `gh` lookups, and the CompactionDB writer lock
  were operator-approved per the sandbox file; the PyYAML fetch is a
  structural gap (follow-up candidate: pre-seeded uv cache or vendored
  dependency for `validate-agent-assets`), not a T40 defect.
- Learning file: four `[memory:failure]` records (merge-base ≠ collector
  authentication; validate lexical and resolved evidence paths; macOS parent
  aliases; user-selected base must not define the fixed range) — adopted
  into the consolidated decision.

**Decision: ACCEPTED** — squash-merge PR #221 without `--delete-branch`
(worker-sec holds the branch).

Post-acceptance (2026-10-02T01:3xZ, operator decision at the session
boundary): `make check-regime-boundary` reported the open `dotfiles worker
worker-sec` workspace and eight untracked artifact copies in worker-sec; the
seat was removed with `herdr-agents --remove-worker
.claude/worktrees/worker-sec --force` (`status=forced`, placement record
and identity gone, wQ closed) and the eight copies, byte-identical to the
committed files, were deleted under the hygiene exemption. The worktree and
its merged branch remain for a future `--add-worker` reseat.

cost: n/a (worker reported none)

[memory:failure] T40: a Codex worker seated in a nested worktree cannot
write the shared `.git` (refs, config) without escalation because the Codex
workspace-write sandbox is scoped to the worktree; a failed sandboxed write
can leave an empty read-only `.git/config.lock` that blocks later writes.
