
## Revision 4 (T34) — review (2026-09-29)

RESULT 03:50:07Z from claude-standard-dot-a005 (worker-c): PR #206 head e226c27a756fcdc921d831bec320db37b2dc1c3a, branch feat/herdr-agents-worker-seat from origin/main e0b7fb9; commits 3eeaeee (deliverable A), 9d5cf7c (deliverable B), e226c27 (independent-review fixes).

### Rulings during the task (addendum committed as e0b7fb9)
1. `home/dot_agents/model-profiles.env` (rendered) allowed, regenerated only. 2. Identity naming: reuse the single existing worktree seat, else derive `<kind>-<profile>-<suffix>-aNNN`, refuse on ambiguity. 3. Upstream #367: `.claude/worktrees/` cwd gets TURN-only delivery (Stop hook); acceptance criterion = PING arrives without `inbox.sh`. 4. `claude-standard-dot-a006` is removed by the orchestrator at acceptance. 5. Design notes and the `spawn.sh` options-file route approved (spawn splices every `$AGMSG_SPAWN_OPTIONS_FILE` token, so full profile args carry).

### Adversarial review (orchestrator, from origin refs and the orchestrator-review worktree)
- Scope: 11 files (+1035/−26), all within revision 4 + addendum allowed_files (manifest field `worker_worktree`, rendered env line `HERDR_AGENTS_WORKER_WORKTREE=".claude/worktrees/worker-c"`, generator + validator + their tests, herdr-agents, its tests, README, SKILL, rule).
- Deliverable A: `prepare_worker_seat` runs before every worker start (full-mode new/heal variants, attach repair, `--restart-worker`); worktree created detached from origin/main, non-worktree path refused; identity joined with `AGMSG_RESOLVE_PROJECT=0` at the worktree or the existing seat reused; delivery `both` claude-code / `turn` codex at the worktree; pane split `--cwd <worktree>`; reused panes get `cd -- <worktree>` via `pane run`; the worker's own `--attach` exits quietly; the T14 guard is scoped to the legacy seat; docs state turn-only delivery per #367 and retire the interim inbox rule for worktree-seated workers.
- Deliverable B: `--add-worker` requires a main checkout, refuses an undefined profile first, creates worktree + identity (`--no-join`) + delivery, creates the workspace `<repo> worker <name>` with managed layout / `AGMSG_RESOLVE_PROJECT=0` / keep-alive, runs `spawn.sh <type> <name> --project <wt> --team <team> --terminal-driver herdr --window` with a generated options YAML, no-op when already seated; `--remove-worker` refuses a dirty worktree unless `--force`, despawns (forced for codex), then delivery off, leave, workspace close, worktree kept.
- Independent re-derivation at e226c27: `make validate-agent-assets` ok; 561 unit tests OK; `shellcheck -x` clean; PR CI 12/12 pass (nix skipped). Mutation baselines pasted (A 6/7, B 8/8, review tests 7/9 on the respective prior scripts). Worker-side independent review returned "incorrect" (P1: heal path started the worker in the main checkout; 3 P2; 6 P3) — all fixed in e226c27 with 9 tests and resolved crit records. CompactionDB f568614e present.
- Refutation attempts found no correctness, security, or omission issue in the change itself.

### Live-acceptance blocker found during review (not a T34 defect)
Upstream agmsg 1.5.0 self-naming relabeled the live pair panes to `dotfiles:claude-remediation-dot` / `dotfiles:claude-standard-dot-a005` and the workspace label is now `dotfiles`, so `herdr-agents` (label-based `single_managed_workspace`, `claude-orchestrator`/`claude-worker` roles) reports "no managed Herdr workspace" — the visible audit lane refused, and `--restart-worker` (T34's live E2E) would too. Tasked as dot-herdr-agents-seat-labels-T35-a01. T34's live E2E (re-seat + PING via Stop hook without inbox.sh) is deferred until T35 is merged; the pre-merge audit ran headless.

### Pre-merge Codex audit (head e226c27, headless with the lane's prompt and `-o` channel; the visible lane refused the relabeled workspace)

`Verdict: incorrect`, one **P2 (high)** — `--remove-worker` forces the codex despawn unconditionally; upstream registers the identity before writing the placement record, and `despawn --force` FAILS when the record is absent while graceful returns ok, so after a failed spawn the removal exits before delivery-off / leave / workspace-close, and a `--force` retry fails the same way. Orchestrator: CONFIRMED against the upstream despawn semantics the worker itself cited (`despawn.sh` header: a free lock with a placement record → `needs-force`; absent record → force fails). ACCEPTED → revise: probe the placement record, graceful first, force only when requested or reported `needs-force`, keep the full cleanup sequence in every path, tests for the absent-record and graceful-then-force paths, baseline vs e226c27.

**Decision on revision 4: REVISE (one round; T35 runs first on the same worker).**

## Revision 5 — reviewed (2026-09-29)

RESULT 05:19:01Z: head 16d095f182e5f8085965ce61f1d8058933e95f75 (+108/−35). `despawn_worker_seat` is graceful-first per upstream `despawn.sh`: graceful `ok` (incl. a member without a placement record after a failed spawn) is done; `status=needs-force` or an explicit `--force` retries with `--force`; anything else stops with a hint and no cleanup; every completed despawn runs delivery-off / leave / workspace-close. File mode restored to 100644 (matches main). Orchestrator: 151 herdr-agents tests OK at 16d095f, `shellcheck -x` clean, baseline 4/5 fail on e226c27 (one guard), CI 12/12 pass after one external rerun (curl HTTP 500 in public-bootstrap, both runs pasted).

Headless Codex audit of 16d095f (`-audit-r5.md`): `Verdict: correct` — "the graceful-first helper matches upstream despawn behavior, preserves cleanup after success, and stops cleanup after failed retries."

Rebase ruling: after T35 (#207 → 2e0c6f4) landed, the branch became DIRTY (one conflict: both PRs added the first bullet under SKILL "Parallel workers"). Ruled: rebase now onto 2e0c6f4 keeping both bullets in T34→T35 order, full unit suite, force-with-lease on the worker's own branch, RESULT revision 6 with the new head; the orchestrator audits the rebased head before merge.

## Revision 6 (rebased) — ACCEPTED (2026-09-29)

RESULT 05:40:17Z: head 9da17b9d263638937cb25bdc26893a13c06a4d60 on origin/main 2e0c6f4 (commit mapping 3eeaeee→019ee6d, 9d5cf7c→8c16ef6, e226c27→fd0b050, 16d095f→02768d9, plus 9da17b9); both SKILL "Parallel workers" bullets kept (T34 then T35); integration fix: `load_seat_labels` runs after the worker's quiet `--attach` exit and before `worker_seat_applies`, the T14 guard and the pair modes (the full suite had caught 2–3 extra read-only lookups per worker SessionStart). Orchestrator: validate ok, 577 unit tests OK, `shellcheck -x` clean, mode 100644, CI 12/12 pass, merge state CLEAN.

Headless Codex audit of 9da17b9 (`-audit-r6.md`): `Verdict: correct` — "the relocated lookup preserves label initialization for continuing paths and skips it on the worker's quiet exit."

### Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-r4-orchestrator-receipt.md (resolved review-scope approval record r_213b6d, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-herdr-agents-add-worker-T22-a01-r4-orchestrator-crit.json).

**Decision: ACCEPTED.** Merge #206 --squash (no --delete-branch while worker-c holds the branch); deploy T34+T35 with `chezmoi apply` from the canonical clone; live E2E: (1) `herdr-agents --audit <PR head>` finds the relabeled pair (T35); (2) `herdr-agents --restart-worker` re-seats the worker into `.claude/worktrees/worker-c`; (3) a PING via `agmsg-dispatch` arrives as a Stop-hook turn delivery WITHOUT the worker running `inbox.sh`; (4) `identities.sh <worktree> claude-code` shows one seat, then `leave.sh dotfiles claude-standard-dot-a006` — recorded below.

[memory:decision] T34 (T22 revision 4) accepted 2026-09-29: the herdr-agents pair worker is seated in its own worktree (manifest `worker_worktree` → `HERDR_AGENTS_WORKER_WORKTREE`), its identity registered there with `AGMSG_RESOLVE_PROJECT=0` and delivery set on that path (turn-only per upstream #367), so dispatches reach the worker without `inbox.sh`; parallel workers are added/removed only via `herdr-agents --add-worker/--remove-worker` on upstream `spawn.sh`/`despawn.sh` (graceful-first despawn). PR #206 squash-merged.

cost: n/a (worker report gives no token figures)

### Deployment and live E2E (orchestrator, 2026-09-29, after merge 2cdd435 together with T35 2e0c6f4)

- `chezmoi apply` from the canonical clone: drift 0; `~/.agents/model-profiles.env` renders `HERDR_AGENTS_WORKER_WORKTREE=".claude/worktrees/worker-c"`; installed `herdr-agents` matches main.
- (T35) `herdr-agents --audit 9da17b9` on the relabeled pair (`dotfiles:claude-remediation-dot` / `dotfiles:claude-standard-dot-a005`, workspace label `dotfiles`): workspace found, existing audit tab reused, `Audit verdict: correct`, 1m06s — the visible lane is back.
- (T34) `herdr-agents --restart-worker` → "worker seat: …/.claude/worktrees/worker-c (agmsg claude-standard-dot-a005)", worker restarted in wJ:p2; afterwards the pane and agent cwd are the worktree, `identities.sh <worktree> claude-code` returns exactly `claude-standard-dot-a005`, `delivery.sh status` at the worktree is `both` with the hooks file present.
- Acceptance criterion: a PING sent with `send.sh --body-file` plus a generic wake prompt (no inbox instruction). Worker turn 1: PING not delivered mid-turn (it saw it unread via read-only `history.sh`, did not run `inbox.sh`). At the end of turn 1 the worktree Stop hook (`check-inbox.sh claude-code <worktree>`) blocked the stop and delivered the PING verbatim ("1 new message(s) in dotfiles") — **turn delivery CONFIRMED without `inbox.sh` or a Monitor**, exactly the #367 turn-only path documented in the PR. The a005 delivery miss (T30/T31/T32/T33x) is closed.
- Ruling 4 executed: `leave.sh dotfiles claude-standard-dot-a006` removed the now-unused second main-path identity; the main checkout carries only `claude-remediation-dot`.
