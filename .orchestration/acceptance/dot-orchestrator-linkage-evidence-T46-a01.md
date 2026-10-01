# Acceptance: dot-orchestrator-linkage-evidence-T46-a01

Drafted 2026-09-30 from session fc905758's failures (blocker reported from an
inference, pane-less regime improvised, ungrounded `allowed_files`, lesson
written to auto-memory). Dispatched 2026-10-01T12:10:37Z (msg 610) after a
pre-dispatch amendment (main at 119fdc3 with T47/T49/T45; real
`agmsg-dispatch` form; keep `.claude/worktrees/orchestrator-review`; reuse the
T49 seat-lock check). Worker questions answered in-flight: the merged T45
pane-less bullet wins over the stricter Start-checklist draft (msg 612); the
`env-converge-T10` WIP is preserved on a new branch, never force-pushed
(msgs 614/616). RESULTs: msg 619 (b91f949), 627 (63c993b), 634 (b29ef04 final).
PR #220.

## Review (orchestrator, from git objects and origin refs)

- `--add-worker` ends with `linkage=ok read_at=<ts> pong=<yes|no>` or
  `linkage=unreached rc=<n> hint=<agmsg-dispatch|poke|attach-a-client|placement-conflict>`
  from an `AGMSG-PING v1 task_id=bringup reason=add-worker-linkage` sent through
  `agmsg-dispatch <team> <orchestrator> <worker> <pane_id>`; exit non-zero only
  when the PING was not read. Pane from the spawn placement record resolved by
  upstream `agmsg_spawn_path` (id-keyed or legacy), legacy path only when the
  resolver is unavailable, a resolver refusal reported as `placement-conflict`
  with nothing dispatched; never `team.sh --json` (it reads Codex panes). PONG
  counted only when `id > ping_id`; wait validated and read as decimal; exactly
  one orchestrator identity or `unreached rc=2`.
- SKILL/rule: evidence-before-blocker invariant (command, exit code,
  `read_at`/PONG query, after `agmsg-dispatch` was tried), headless/unviewed
  workspace wake with `agmsg-dispatch` (`poke.sh` 14/15 is a locator refusal),
  lessons codified in the repository not auto-memory, Start checklist
  reconciled with the T45 pane-less bullet (pair via full mode is the normal
  form; the pane-less bring-up only as T45 describes; `--add-worker` serves
  both), Stop checklist naming `make check-regime-boundary`.
- `scripts/check-regime-boundary.sh` (shdoc, `--report`): untracked
  `.orchestration` files, stray identities per `git worktree list` checkout,
  `crit _serve`, leftover `<main checkout basename> worker <name>` workspaces,
  and the bare-id seat lock by importing `orchestrator_seat_lock_warnings`;
  `make check-regime-boundary`; `validate-agent-assets` reports it as `WARN:`
  only.
- `agmsg-dispatch` `@description` names the headless-workspace wake.
- Worktrees: `worker-b` removed (untracked T17 evidence verified identical to
  main), `env-converge-T10` removed after its uncommitted `pr-feedback.py`
  work was committed as 0c12c6a and pushed to `wip/pr-feedback-codex-review-T10`
  (the push to `feat/pr-feedback-gate` was non-fast-forward; no force-push);
  `orchestrator-review` kept. `git worktree list`: main, orchestrator-review,
  worker-c, worker-sec.
- Tests: linkage ok/unreached/timeout, placement record not `team.sh`, old
  PONG ignored, id-keyed record, placement conflict, legacy fallback without
  the resolver, invalid and leading-zero wait, two leaders, boundary script
  from a worktree; 672 OK. shfmt and shellcheck clean; render-check; validate.
  CI green Linux+macOS; CLEAN.

## Codex audits (gpt-6-astra, read-only)

7d0c585 **incorrect** (P2 `team.sh` pane read, P2 PONG not correlated, P2
label prefix from the worktree) → b91f949; bec48d4 correct (shfmt); b91f949
**incorrect** (P2 hard-coded placement path) → 91cc85f; 91cc85f **incorrect**
(P2 fallback swallows the resolver refusal) → 63c993b; 63c993b correct;
00573f3 **incorrect** (P2 leading-zero octal) → b29ef04; b29ef04 correct.

## PR #220 feedback sweep (head b29ef04, 26 items)

Codex inline: "exclude the resident pair" → not-applicable (the prefix is
already `<repo> worker `; the resident `<repo> agents` label never matches);
"correlate PONGs" → fixed:b91f949; "validate the wait" → fixed:00573f3;
"ambiguous orchestrator identities" → fixed:00573f3. Four new comments on
b29ef04, all confirmed by reading the code: a delayed PONG from an earlier
worker instance written after the new PING still counts (`id > ping_id` is
not enough); a retained placement record may point at a pane in an older
workspace; the untracked-`.orchestration` probe scans only the script's own
checkout; zero identity names at an active seat are not flagged. 18
non-review items not-applicable. **Decision (round 4): REVISE r5** — nonce
`task_id`, workspace check on the record, per-worktree untracked probe,
zero-names check for the main checkout and the manifest worker worktree.
The orchestrator had written the acceptance before reading the final sweep;
corrected here.

## Effects (declared by the worker, reverse mapping)

- Remote branch `wip/pr-feedback-codex-review-T10` (0c12c6a) — the operator
  deletes it when the WIP is no longer wanted.
- Local branch ref `feat/pr-feedback-gate` moved to 0c12c6a — operator-owned.
- Two `crit _serve` processes (Plan Mode review servers of 2026-09-30) were
  stopped by the worker with SIGTERM, per the Crit rule; disclosed, no
  reverse step needed.

## CompactionDB

Worker decision `85a51aeb…` in the main DB stands.

cost: worker ~70k context tokens r1 + revise rounds (session counters; no per-task figure)

**Decision (round 4): REVISE r5** (see the sweep section).

## Rounds 5–7 (RESULTs msg 638 9e36e63, 642 2721f0c, 646 d806a3d)

- r5 9e36e63: the four r5 items (current PING task_id, missing identities,
  all worktrees probed, placement panes checked against the workspace).
  Audit correct. Codex GitHub review: P2 matching pane CWD → r6.
- r6 2721f0c: workspace filter by pane cwd under the main checkout. Audit
  correct. Codex GitHub review: three P2s (mixed-runtime identities on an
  active seat, stale pane in the same workspace, seat-lock check given
  `root`) → r7.
- r7 d806a3d: all three fixed with one test each; negative check 4/4 fail at
  2721f0c; 679 tests OK; CI green Linux+macOS; CLEAN. Audit **correct**.
  Sweep (36 items): 11 fixed, resident-pair comment refuted (prefix is
  `<repo> worker `), rest not-applicable, and three new Codex P2s on d806a3d
  that I could not refute: a placement pane that pre-dates this spawn is
  accepted (`known` never consulted), a failed dispatch hides the invocation
  and query the blocker invariant demands, and the pane-less bullet still
  sends the PING with `poke.sh`. Plus the two residuals the worker disclosed
  (shdoc header, teardown wording).

**Decision (round 7): REVISE r8** — five items, one commit (task amendment
r8).

## Round 8 (RESULT msg 655, 98ea49f)

All five r8 items verified in the diff: `jq … '$pane | IN($known[])'`
rejects a pre-spawn record pane; a failed `agmsg-dispatch` keeps its stderr
and the check prints the exact invocation, exit code and the `read_at`/PONG
query (or that the db path is unresolved) before the unchanged stdout line;
SKILL pane-less clause rewritten (no `poke.sh … --body-file` PING), teardown
clause scoped (per type at non-seat worktrees, one name across types at an
active seat); shdoc header. Two new tests, negative check at d806a3d; 681
OK; CI green Linux+macOS; CLEAN. Codex audit of 98ea49f: **incorrect**, one
P2 (high confidence): the SKILL recovery command `agmsg-dispatch <team>
<orchestrator> <worker> <pane>` lacks the fifth (message) argument and exits
1 with usage — valid, a doc defect introduced in r8. Worker observation
accepted: the same bullet still says to confirm placement with `team.sh
--json`, which reads Codex panes. No Codex GitHub review of 98ea49f had
posted by 21:15Z.

**Decision (round 8): REVISE r9** — two SKILL sentences, one commit (task
amendment r9).

## Round 9 (RESULT msg 658, a71e78d) and acceptance

- a71e78d: one-line SKILL change, verified in the diff: the re-wake reads
  `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1
task_id=<id> reason=<reason>'`; placement is confirmed from the
  `run/spawn.*` record (`agmsg_spawn_path`) and the `linkage=` line, "never
  from `team.sh <team> --json`, which observes Codex members by reading
  their pane". No test pins the old wording (grep pasted). render-check and
  validate exit 0; CI green Linux+macOS; CLEAN. Codex audit of a71e78d:
  **correct**.
- Audit ledger (12 non-merge commits, `origin/main..branch`): 7d0c585,
  b91f949, 91cc85f, 00573f3, 98ea49f **incorrect** — every finding fixed in
  the next commit (b91f949, 91cc85f, 63c993b, b29ef04, a71e78d); bec48d4,
  63c993b, b29ef04, 9e36e63, 2721f0c, d806a3d, a71e78d **correct**.
  Transcripts in `…-audit-<sha>.md(.last.md)`.
- Sweep on a71e78d (`…-pr-feedback.json`, 36 items): 14 `fixed:<sha>`
  (b91f949 1, 00573f3 2, 9e36e63 4, 2721f0c 1, d806a3d 3, 98ea49f 3), 22
  `not-applicable` (11 runner-image notices, 1 Homebrew tap warning, 7 Codex
  review containers, CodeRabbit skipped comment + status, and the
  resident-pair comment refuted by the `<repo> worker ` prefix). No Codex
  GitHub review posted for 98ea49f or a71e78d by 21:30Z.
- Gate: `AGENT_REVIEWED=1 REVIEW_EVIDENCE=…-review-receipt.md BASE=origin/main
PR_FEEDBACK_EVIDENCE=…-pr-feedback.json make require-crit-review` in
  `.claude/worktrees/orchestrator-review` at a71e78d → exit 0 ("PR feedback
  evidence accepted"; "Review requirement satisfied"). Evidence:
  `…-crit-comments.json` (one resolved review-scope record), receipt
  `review_surface: crit-data`, `reviewer: claude-code`, `review_outcome:
approved`.
- Protocol notes: the installed `herdr-agents` on this machine is still the
  T42 build until `make -C ~/.local/share/chezmoi update`; nothing in this
  task is live-leg evidence for the new linkage line. The worker-sec reseat
  for T40 (2026-10-01T17:50Z) used that old build with a manual PING.

**Decision: ACCEPTED** — squash-merge PR #220 without `--delete-branch`
(worker-c holds the branch). CompactionDB: consolidated orchestrator
decision added at acceptance (command in the boundary-commit log). Next: T50
dispatch (worker-c), T40 acceptance (PR #221), T47/T49 live legs at the
operator's relaunch.
