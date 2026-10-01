# Report: dot-orchestrator-linkage-evidence-T46-a01

- status: ready_for_review
- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: bc52ce08…efb5 at dispatch, then amended by the orchestrator's answers: 2f8a866a… (msg 612, the Start checklist) and ce77a308… / 7cc7f7ec… (deliverable 8 and the push target). The current file was verified before committing.
- branch: `fix/orchestrator-linkage-evidence` from origin/main 119fdc3, with **7d0c585** (deliverables) and **bec48d4** (shfmt style fix for CI).
- head sha: `b91f949ad1b0cd5714e5d2800dbd1865894135bd` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN)
- PR: https://github.com/mryfmo/dotfiles/pull/220
- cost: 0 subagent dispatches; about 70k context tokens consumed (session budget counter; no per-task figure exposed)

## Deliverables

1. **`--add-worker` linkage check** (`check_worker_linkage`, called after spawn.sh returns on both outcomes).
   - **The PING:** it sends `AGMSG-PING v1 task_id=bringup reason=add-worker-linkage` through `agmsg-dispatch <team> <orchestrator> <worker> <pane_id>`. This is the real form per the amendment; the pane id looks like `wP:p2`.
   - **Where the pane comes from:** the worker's spawn placement record `~/.agents/skills/agmsg/run/spawn.<team>__<worker>`, whose field 1 is `herdr:<socket>:<pane>`, reduced to `<ws>:<pN>`; else the workspace's first new pane. r2 removed the `team.sh --json` call (see below).
   - **Evidence:** after a read PING, it takes `read_at` from messages.db (through agmsg's own `lib/validate.sh` + `lib/storage.sh` `agmsg_db_path`) and polls for `AGMSG-PONG v1 task_id=bringup…` for `HERDR_AGENTS_LINKAGE_PONG_WAIT` seconds (default 30).
   - **Final line:** `linkage=ok read_at=<ts> pong=<yes|no>` or `linkage=unreached rc=<n> hint=…`. The hint is:
     - `agmsg-dispatch` when it is not installed or there is no orchestrator identity;
     - `poke` when a placement record exists;
     - `attach-a-client` otherwise (view the headless workspace).
   - **Exit code:** non-zero only when the PING was not read. Then it is spawn's own code if spawn failed, else the dispatch code. A timed-out spawn whose worker reads the PING exits 0, with the spawn warning still on stderr.
   - "Herdr agents worker added" is printed only for a successful spawn. The worker pane is never read.
2. **SKILL** (built on the T49 and T45 bullets: adds, no duplicates or contradictions):
   - Orchestrator Playbook step 6 gains the headless or unviewed seating case: `poke.sh` 14/15 is a locator refusal, so use `agmsg-dispatch` and verify `read_at`.
   - "Regime activation" gains the evidence-before-blocker invariant, which names the `linkage=` line, and the **Start checklist**. Per the orchestrator's answer (msg 612): the pair via full mode is the normal form; the T45 pane-less bring-up is the only alternative; `--add-worker` serves both; nothing else is improvised. It cross-references the T45 bullet.
   - The boundary bullet gains "lessons are codified in the repo, not auto-memory", and a new **Stop checklist** bullet names `make check-regime-boundary`.
3. **Rule** (`home/dot_config/claude/rules/agmsg-orchestration.md`): bullets for evidence before blocker reports; the headless-workspace `agmsg-dispatch` wake; codifying lessons in the repo with the Stop checklist and check; and the Start checklist.
4. **`agmsg-dispatch` `@description`:** it is also the wake path for unviewed or headless workspaces, where `poke.sh` exits 14/15.
5. **Tests:**
   - `test_add_worker_reports_linkage_ok_after_a_ready_spawn` checks `linkage=ok read_at=2026-10-01T00:00:00Z pong=yes` as the last line, and the exact `agmsg-dispatch …` PING call on `w-test:p9`.
   - `test_add_worker_reports_linkage_unreached_after_a_failed_spawn` checks `linkage=unreached rc=1 hint=attach-a-client` with exit 3 (spawn's code).
   - `test_add_worker_exits_zero_when_a_timed_out_spawn_still_links` checks exit 0 with `pong=no`.
   - The shared `write_seat_lifecycle_fakes` gained a fake `agmsg-dispatch` on PATH, a temporary messages.db (sqlite3), fake `lib/validate.sh`/`lib/storage.sh`, and a default spawn pane `w-test:p9`. `run_helper` sets the PONG wait to 0.
   - The T45 test `…reports_a_failed_claude_spawn_without_a_trust_dialog` now also makes the worker unreachable, so spawn's exit 3 still stands. Under T46, a reachable worker after a failed spawn exits 0.
6. **Check script:** `scripts/check-regime-boundary.sh` (shdoc header, `--report` option), wired as `make check-regime-boundary`, with `validate-agent-assets.py` `report_regime_boundary()` printing its lines as `WARN:` and never failing.
   - It checks: untracked `.orchestration` files; more than one identity name per `git worktree list` checkout (claude-code and codex); `crit _serve`; `<repo> worker <name>` Herdr workspaces when `herdr` is reachable; and the bare-id orchestrator lock by **importing** `orchestrator_seat_lock_warnings` from `scripts/check-agent-runtime.py`. That is one implementation, not two.
   - Every probe is read-only, and a missing tool skips its check.
7. **Gates:** CI on 7d0c585 failed only at `Run shfmt` (exit 123). The pinned shfmt 3.14.1 (`-i 4 -sr`) wants the heredoc inside the process substitution on its own line in `scripts/check-regime-boundary.sh`; bec48d4 applies exactly that formatting, and the repo-wide `shfmt -d` is now clean (exit 0). Local gates: `make unit-test` (663 tests OK), `make validate-agent-assets` (ok, plus one non-blocking `WARN: regime-boundary`), `make render-check`, and `shellcheck` on all three scripts all pass. PR #220 is open.
8. **Legacy worktrees:**
   - **`worker-b` removed.** Its six untracked T17 files were verified byte-identical to origin/main first (`cmp`); `--force` was needed only because they were untracked.
   - **`env-converge-T10`** held **uncommitted** tracked work, not on main: `pr-feedback.py`, +59/−3, `--require-codex-review`. I reported it (PONG) rather than destroy it. Per the orchestrator:
     - I committed it on its branch as **0c12c6a** ("wip(pr-feedback): preserve the unreviewed T10 --require-codex-review draft").
     - The push to `feat/pr-feedback-gate` was **rejected as non-fast-forward**, because the remote has 10 later commits. Force-push is forbidden. On the orchestrator's second answer, I pushed it to a **new branch, `wip/pr-feedback-codex-review-T10` (0c12c6a)**.
     - Remote `feat/pr-feedback-gate` is untouched at b25c005.
     - Then I removed the worktree.
     - The local branch ref `feat/pr-feedback-gate` is kept. It now points at 0c12c6a, the WIP commit, instead of fd549f5.
   - **`orchestrator-review` kept**, per the amendment. `worker-sec` and `worker-c` were not touched.
   - **Result:** `git worktree list` shows main, `orchestrator-review`, `worker-c` and `worker-sec`.
   - **No PR** was opened for the WIP branch.

## `make check-regime-boundary` findings on this machine

Before cleanup, it found worker-c's untracked T45 sandbox record and two running `crit _serve` servers. Those were T47 plan-mode review servers from this session, started 2026-09-30 13:03 and 13:09 JST. Per the global Crit rule (close a Crit session opened by the Plan Mode hook once its review is done), I stopped them with SIGTERM on their two PIDs, not `crit stop --all`.

After cleanup, the only finding is the worker-c T45 sandbox record. It is kept as the orchestrator asked and differs from the main-checkout copy, which extends it. The script checks the repository it lives in, so the run "from the main checkout" also inspected worker-c.

## Notes

- **Understand-Anything hook:** it fired after the commit. I did not act on it.
- **Forbidden actions honoured:** no edits to upstream agmsg or `poke.sh`, no pane read, no merge, no force-push.

[memory:decision] T46: `herdr-agents --add-worker` ends with a `linkage=` line from an agmsg-dispatch PING; a blocker report needs command, exit code and read_at/PONG evidence; unviewed Herdr workspaces are woken with `agmsg-dispatch`; regime lessons are codified in rules/skills/checks, never only in auto-memory (operator 2026-09-30).

## CompactionDB (main checkout)

Memory id **85a51aeb-9a9b-494e-b66f-3fca94d147b6**. The command and output are in the validation file.

## Effects

Outside the working tree:
- the remote branch `wip/pr-feedback-codex-review-T10`, which the operator decides about;
- the local branch ref `feat/pr-feedback-gate`, moved to 0c12c6a;
- two worktrees removed;
- two Crit servers stopped.

The other changes take effect at `chezmoi apply`.

## Revision 2 (amendment r2, task_rev b8d7dcbf…3466 verified; PING 12:42:47Z)

One more commit, **b91f949**, on bec48d4. There was no force push. PR #220 head: `b91f949ad1b0cd5714e5d2800dbd1865894135bd` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

The audit of 7d0c585 found three P2s; all are fixed:

1. **No pane read in the linkage check.**
   - **The problem:** `team.sh --json` observes Codex members through `terminal_peek` → `herdr pane read`, which the regime forbids.
   - **The fix:** the pane now comes from the spawn placement record `run/spawn.<team>__<worker>` (`herdr:<socket>:<pane>`, `<ws>:<pN>` tail). It falls back to the workspace's new pane. The linkage check makes no `team.sh` call.
   - **Test:** `test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh` writes a record for `w-test:p7` while the new pane is `p9`, and checks that the dispatch targets `w-test:p7` and that the logging `team.sh` fake shows no call after `spawn`. Before spawn, `ensure_worker_identity` legitimately uses `team.sh` for the next `-aNNN`.
2. **The PONG is correlated to this PING.**
   - **The fix:** right after the dispatch, it reads `max(id)` of the orchestrator-to-worker rows as this PING's id. `read_at` comes from that row, and only PONGs with `id > <ping id>` count.
   - **Test:** `test_add_worker_linkage_ignores_a_pong_older_than_this_ping` pre-inserts an earlier `AGMSG-PONG v1 task_id=bringup` row and expects `pong=no`.
3. **Boundary script label prefix.**
   - **The fix:** `check-regime-boundary.sh` derives the main checkout from `git rev-parse --path-format=absolute --git-common-dir` (stripping `/.git`) and uses its basename for the `<repo> worker ` prefix.
   - **Test:** `test_regime_boundary_check_finds_worker_workspaces_from_a_worktree` runs the script from a fake `dotfiles/.claude/worktrees/wt`. It reports `dotfiles worker x` and not `wt worker y`.

**Negative check against bec48d4:** all three tests fail there, each in the audited way:
- the PING went to `p9`, not `p7`;
- the old PONG made it `pong=yes`;
- only `wt worker y` was reported.

**Checks at b91f949:**
- `make render-check`, `make unit-test` (666 tests OK, 1 skipped) and `make validate-agent-assets`: all exit 0.
- Repo-wide `shfmt -d`: exit 0.
- `shellcheck` on all three scripts: exit 0.
- `make check-regime-boundary`: exit 2, with one finding, the untracked worker-c T45 sandbox record, kept as asked.
- CI: in the validation file.

## Revision 3 (orchestrator status=revise 13:25:21Z; amendment r3; task_rev 8169b137…9611 verified)

One commit, **91cc85f**, on b91f949. There was no force push. PR #220 head: `63c993b32b58a6a95ee781c465c918fe3ad89e5b` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

**The problem** (audit of b91f949, P2): the placement record path was hard-coded as `run/spawn.<team>__<worker>`, but agmsg 1.5.0 also writes id-keyed records.

**The fix:** the record path now comes from upstream `agmsg_spawn_path` (`lib/actas-lock.sh`), which resolves the id-keyed form or the legacy one.
- It runs in a separate `bash -c` with `SKILL_DIR` passed through `env`. A `( export SKILL_DIR … )` subshell like the one in `claim_orchestrator_seat` would make shellcheck report SC2030/SC2031 across the two subshells.
- The single-quoted inner script carries one intended `# shellcheck disable=SC2016`.
- When the library is absent, it falls back to the legacy path; the workspace-new-pane fallback is unchanged.

**Test:** `test_add_worker_linkage_resolves_an_id_keyed_placement_record`. A fake `agmsg_spawn_path` answers `run/spawn.k-team__k-member`, which holds `herdr:…:w-test:p7`, and the dispatch fails. The test expects `linkage=unreached rc=1 hint=poke`, exit 1, and a dispatch to `w-test:p7`.
- **Negative check against b91f949:** it **fails** there with `hint=attach-a-client`, because the record wasn't found.
- The legacy-record test from r2 still passes through the fallback.

**Checks at 91cc85f:**
- `make render-check`: exit 0.
- `make unit-test`: 667 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- Repo-wide `shfmt -d`: exit 0.
- `shellcheck` on all three scripts: exit 0.
- `make check-regime-boundary`: exit 2, with only the kept worker-c T45 sandbox record.
- CI: in the validation file.

## Revision 3-b (amendment r3-b, task_rev 9d9af86e…4587 verified; PING 13:51:56Z)

One more commit, **63c993b**, on 91cc85f. There was no force push. PR #220 head: `63c993b32b58a6a95ee781c465c918fe3ad89e5b` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

**The problem** (audit of 91cc85f, P2): the `|| record=<legacy>` fallback also ran when upstream `agmsg_spawn_path` **refused**, which happens when both an id-keyed and a legacy record exist, so a stale legacy pane could be dispatched to.

**The fix:** the legacy path is used only when the resolver is unavailable, meaning `lib/actas-lock.sh` is unreadable or `declare -F agmsg_spawn_path` fails in that bash. When the resolver runs and fails, the check:
- prints its first stderr line to stderr;
- prints `linkage=unreached rc=<rc> hint=placement-conflict`;
- dispatches nothing;
- returns that rc.

**A bug the new test caught before commit:** `if ! record=$(…); then rc=$?` saw the negated status (0), so the add-worker exited 0. The exit code is now captured with `|| rc=$?`.

**Tests:**
- `test_add_worker_linkage_refuses_a_placement_conflict`: a fake resolver prints upstream's refusal and returns 1. Expected: `linkage=unreached rc=1 hint=placement-conflict`, the refusal on stderr, no `agmsg-dispatch` call, exit 1.
- `test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver`: the library exists but has no `agmsg_spawn_path`. Expected: the legacy record's `w-test:p5` is dispatched to, exit 0.
- The r2 legacy-record test still covers a missing library file.
- **Negative check against 91cc85f:** the conflict test **fails** there (it dispatched to the legacy pane and exited 0). The fallback test passes on both versions, as the outcome is unchanged.

**Checks at 63c993b:**
- `make render-check`: exit 0.
- `make unit-test`: 669 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- Repo-wide `shfmt -d`: exit 0.
- `shellcheck` on all three scripts: exit 0.
- `make check-regime-boundary`: exit 2, with only the kept worker-c T45 record.
- CI: in the validation file.

## Revision 4 (orchestrator status=revise 14:23:45Z; amendment r4; task_rev de7b97e0…d88c verified)

One commit, **00573f3**, on 63c993b. There was no force push. PR #220 head: `b29ef04f80d9f2da085045a56ed8a1f9370079e9` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

1. **The PONG wait is validated** (`:889`).
   - **The problem:** `HERDR_AGENTS_LINKAGE_PONG_WAIT` was used in arithmetic unvalidated, so a non-numeric value aborted the `set -u` launcher after the PING was read, and the `linkage=` line never printed.
   - **The fix:** the value must match `^[0-9]+$`. Otherwise the default 30 applies, with one stderr warning (`must be a whole number of seconds; got 'foo', using 30.`).
   - **Test:** `test_add_worker_linkage_survives_a_non_numeric_pong_wait` sets `HERDR_AGENTS_LINKAGE_PONG_WAIT=foo` and expects `linkage=ok … pong=no`, exit 0, and the warning. It takes about 30 s because the fallback really waits; I kept `pong=no` as the amendment states.
2. **Exactly one orchestrator for the PING** (`:1820`).
   - **The problem:** the PING's sender was `head -n 1` of the team's non-`-aNNN` claude-code identities.
   - **The fix:** exactly one is now required, the same rule `claim_orchestrator_seat` applies. With none or several, a stderr line names the state (for several: `several orchestrator claude-code identities in team dotfiles … (claude-remediation-dot claude-second-dot); linkage PING not sent.`), the check prints `linkage=unreached rc=2 hint=agmsg-dispatch`, and nothing is dispatched.
   - **Test:** `test_add_worker_linkage_refuses_several_orchestrator_identities`. The worker seat is pre-registered at its worktree, because naming a new worker already refuses two leaders earlier in `ensure_worker_identity`. The test expects that line, exit 2, and no `agmsg-dispatch` call.

**Negative check against 63c993b:** both tests **fail** there:
- the non-numeric wait gives exit 1 with no linkage line;
- two leaders give exit 0 with the PING sent.

**Checks at 00573f3:**
- `make render-check`: exit 0.
- `make unit-test`: 671 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- Repo-wide `shfmt -d`: exit 0.
- `shellcheck` on all three scripts: exit 0.
- `make check-regime-boundary`: exit 2, with only the kept worker-c T45 record.
- CI: in the validation file.

## Revision 4-b (amendment r4-b, task_rev c4cdc516…8f59 verified; PING 14:51:11Z)

One more commit, **b29ef04**, on 00573f3. There was no force push. PR #220 head: `b29ef04f80d9f2da085045a56ed8a1f9370079e9` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

**The problem** (audit of 00573f3, P2): `^[0-9]+$` accepts `08` and `010`, and bash arithmetic reads them as octal.

**The fix:** the deadline now uses `$((SECONDS + 10#${wait_seconds}))`, so a leading zero is decimal.

**Test:** `test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal` sets `HERDR_AGENTS_LINKAGE_PONG_WAIT=08` and answers the PONG early, so the test stays fast. It expects `linkage=ok … pong=yes`, exit 0, and no "value too great for base".

**Negative check against 00573f3:** the test **fails** there. The failure is worse than a missing line: the octal error escaped the add-worker block, the launcher fell through into the **full-mode** code path, and its last line was `Herdr agents workspace: w-test`. In real use, `--add-worker` with `08` would have gone on to create or repair a pair workspace. After the fix, the add-worker block ends with its own exit as intended.

**Checks at b29ef04:**
- `make render-check`: exit 0.
- `make unit-test`: 672 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- Repo-wide `shfmt -d`: exit 0.
- `shellcheck` on all three scripts: exit 0.
- `make check-regime-boundary`: exit 2, with only the kept worker-c T45 record.
- CI: in the validation file.

## Revision 5 (orchestrator status=revise 15:28:37Z; amendment r5; task_rev dbf627b7…0525 verified)

One commit, **9e36e63**, on b29ef04. There was no force push. PR #220 head: `9e36e63352938520e426aa5e112a1c68a9107770` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

1. **Per-invocation PING task_id** (`:897`).
   - **The fix:** the PING is now `AGMSG-PING v1 task_id=bringup-<epoch>-<pid> reason=add-worker-linkage`. Only a PONG whose body is exactly `AGMSG-PONG v1 task_id=<that id>`, or starts with that and a space, and whose `id` is greater than the PING's, counts.
   - **Docs:** the docstring names the per-invocation id. The SKILL and rule never named `task_id=bringup`, so they needed no change.
   - **Fixture:** the fake `agmsg-dispatch` PONG now echoes the PING's task_id, as a worker does. A `pong_task_id` override simulates a delayed PONG from an earlier instance.
   - **Test:** `test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping` inserts a PONG for `bringup-1-1` after this PING and expects `pong=no`.
   - The older PING assertions now match `task_id=bringup-\d+-\d+`.
2. **Same-workspace placement only** (`:857`).
   - **The fix:** a placement record is accepted only when its `<ws>` part equals the new seat's `workspace_id`. Otherwise stderr says `placement record for <worker> names workspace <ws>, not <new>; using the new pane.`, and the new-pane lookup decides.
   - **Test:** `test_add_worker_linkage_ignores_a_placement_record_from_another_workspace`. A `w-old:p3` record leads to dispatch to `w-test:p9` and never to `w-old:p3`.
3. **Untracked evidence in every worktree** (`:37`).
   - **The fix:** `check-regime-boundary.sh` runs the untracked-`.orchestration` probe for every path in `git worktree list --porcelain`, falling back to its own checkout. The line now names the checkout: `untracked .orchestration file in <checkout>: <path>`.
   - **Test:** `test_regime_boundary_check_scans_every_worktree_for_untracked_evidence` runs the script from `wt` and reports a file in the sibling `review` worktree.
4. **Empty active seats are flagged** (`:45`).
   - **The fix:** besides "more than one name per checkout", the check reports `no claude-code identity at the main checkout <main>`, and, when `~/.agents/model-profiles.env` sets `HERDR_AGENTS_WORKER_WORKTREE` and that directory exists, `no worker identity at the manifest worker_worktree <path>` (claude-code plus codex names equal 0).
   - Other worktrees, for example `orchestrator-review`, are not seats and stay exempt.
   - **Test:** `test_regime_boundary_check_flags_empty_seats_only`. With a fake `identities.sh` that returns nothing, the main checkout is reported and the `review` worktree is not.

**Negative check against b29ef04:** all four tests **fail** there:
- the delayed PONG counted (`pong=yes`);
- the dispatch went to the old workspace's pane;
- nothing was reported for the sibling worktree;
- the empty main seat was not reported.

**Checks at 9e36e63:**
- `make render-check`, `make unit-test` (676 tests OK, 1 skipped) and `make validate-agent-assets`: all exit 0.
- Repo-wide `shfmt -d`: exit 0.
- `shellcheck` on all three scripts: exit 0.
- `make check-regime-boundary`: exit 2. The per-worktree probe now reports the real mid-session state:
  - the main checkout's untracked T46 artifacts and the orchestrator's audit and receipt files, which the next boundary commit absorbs;
  - worker-sec's paused T40 evidence;
  - worker-c's kept T45 record.

  There are no empty-seat findings on this machine.
- CI: in the validation file.

## Revision 6 (orchestrator status=revise 16:08:00Z; amendment r6; task_rev 3c794f35…ba36 verified)

One commit, **2721f0c**, on 9e36e63. There was no force push. PR #220 head: `2721f0c1091154b5c4d667886df6a197d2cb7e24` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

**The problem** (Codex GitHub review of 9e36e63, P2, `check-regime-boundary.sh:88`): the leftover-worker check matched workspaces by the `<basename> worker ` label alone, so a second clone with the same basename made this repository's boundary check fail.

**The fix:** a label-matched workspace now counts only when at least one of its panes has a `cwd` equal to the main checkout or under `<main>/`. The check queries each candidate with `herdr pane list --workspace <ws>`, the same disambiguation `find_managed_workspaces` applies in `executable_herdr-agents`. Workspaces whose panes are elsewhere are skipped. The workspace list is read as `workspace_id` + `label` pairs.

**Test:** `test_regime_boundary_check_finds_worker_workspaces_from_a_worktree` is rewritten around a per-workspace fake `herdr`:
- `w1` is `dotfiles worker x` with a pane under this checkout;
- `w2` has the same label with a pane under `/elsewhere/dotfiles/…`;
- `w3` is `wt worker y`.

Exactly one line is reported, for `w1`.

**Negative check against 9e36e63:** the test **fails** there, because both `dotfiles worker x` workspaces are reported.

**Checks at 2721f0c:**
- `make render-check`, `make unit-test` (676 tests OK, 1 skipped) and `make validate-agent-assets`: all exit 0.
- Repo-wide `shfmt -d`: exit 0.
- `shellcheck` on all three scripts: exit 0.
- `make check-regime-boundary`: exit 2, with the same mid-session untracked-evidence findings as at r5 and no worker-workspace finding.
- CI: in the validation file.

## Revision 7 (orchestrator status=revise 17:03:28Z; amendment r7; task_rev 768edbdc…badf81 verified)

One commit, **d806a3d**, on 2721f0c, pushed without `-u`. There was no force push. PR #220 head: `d806a3d2a697c82956e707ea7d36de25e2c26a8e`. All CI checks pass on Linux and macOS (details in the validation file).

**Fixes**, one per finding from the Codex GitHub review of 2721f0c:

1. **Mixed-runtime identities on an active seat** (`check-regime-boundary.sh`): the two active seats are the main checkout and the manifest `worker_worktree` from `~/.agents/model-profiles.env`. The check now counts the distinct `identities.sh` names across claude-code and codex at each seat.
   - 0 names: `no agmsg identity at the active seat <path> (expected one)`.
   - More than one: `stray identities at the active seat <path>: N names across claude-code and codex (expected one)`.
   - Other worktrees keep the per-type `>1` check. A seat is skipped there by resolved path, so it is never reported twice.
   - Seats are queried with their registered (unresolved) paths.
   - The empty-seat message wording changed with this fix, and its test was updated to match.
2. **Stale pane in the same workspace** (`executable_herdr-agents`, `check_worker_linkage`): a placement record in the current workspace is now used only when `herdr pane list --workspace <ws>` still lists its pane id.
   - Otherwise the check prints `placement record for <worker> names pane <P>, which is not in workspace <W>; using the new pane.` to stderr and falls back to the new-pane lookup.
3. **Seat-lock check given `root`**: the inline Python now receives `"${root}" "${main}"`. `root` only locates `scripts/check-agent-runtime.py`; `orchestrator_seat_lock_warnings` is called with `Path(main)`.

**Tests** (new):
- `test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat`: one claude-code name plus one codex name everywhere, with manifest `worker_worktree=.claude/worktrees/wt`. Both seats (main and wt) are reported, and `review` is not.
- `test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace`: the record names `w-test:p3`, but the workspace lists only `w-test:p9`. The stderr line is printed, the PING is dispatched to p9, and no call names p3.
- `test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout`: a fake `check-agent-runtime.py` in the worktree records the path it was given, which must equal the main checkout.

**Fixture change:** `write_seat_lifecycle_fakes` gained `spawn_panes`, the post-spawn pane list (default `w-test:p9`). The three record-based tests (p7, id-keyed p7, legacy p5) now list their pane as present.

**Negative check against 2721f0c:** I swapped in the 2721f0c scripts, then restored them (`cmp` exit 0 for both). All four affected tests **fail** there: the three new tests plus the empty-seat test with its new wording.

**Checks at d806a3d:**
- `make render-check`: exit 0.
- `make unit-test`: 679 tests OK, 1 skipped; exit 0.
- `make validate-agent-assets`: exit 0.
- Repo-wide `shfmt -d` (3.14.1): exit 0.
- `shellcheck` on both scripts: exit 0.
- `make check-regime-boundary` (live): exit 2. Its findings are only the expected mid-session untracked evidence: T46 artifacts and audits in the main checkout, the kept T45 record in worker-c, and T40 in worker-sec. There are no identity findings, so the main checkout and worker-c each hold exactly one name across both types.

**Residuals** (left out to keep this a single commit; for the orchestrator to decide):
- The shdoc header of `check-regime-boundary.sh` (lines 7-12) still describes only "more than one agmsg identity name per registered checkout". It names neither the active-seat rule (exactly one name across both types) nor the empty-seat check.
- The agmsg-orchestration SKILL.md and its rule still describe teardown verification as a per-type `identities.sh <project> <type>` count where "one distinct name is healthy". That is now the non-seat rule. At an active seat the count spans both types.

**CompactionDB:** the r1 memory (85a51aeb-9a9b-494e-b66f-3fca94d147b6) stands. No new memory was added for r7; its three rules are in the learning file (items 15-17) for acceptance-time consolidation.

cost: n/a

## Revision 8 (orchestrator status=revise 17:44:52Z; amendment r8; task_rev 9a2d0e86…13b5 verified)

One commit, **98ea49f**, on d806a3d, pushed without `-u`. There was no force push. PR #220 head: `98ea49fa2fa1d3ea4c1cc4099c7287c1540de143`. CI results are in the validation file.

**Fixes** (the three P2s from the Codex GitHub review of d806a3d, plus the two r7 residuals):

1. **Pre-spawn record pane** (`check_worker_linkage`): a same-workspace placement record whose pane is still listed but was already in `known` (the pre-spawn pane ids) is now treated as stale.
   - stderr: `placement record for <worker> names pane <P>, which existed before this spawn; using the new pane.`
   - The check then falls back to the new-pane lookup.
2. **Dispatch failure evidence** (`check_worker_linkage`): `agmsg-dispatch` now keeps its own stderr; only stdout is silenced. The db path is resolved before the failure branch. On a non-zero exit, the check prints to stderr:
   - the exact invocation and its exit code: `linkage PING failed: agmsg-dispatch <team> <orch> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=add-worker-linkage' exited <rc>.`;
   - the `read_at`/PONG query against that db: `sqlite3 '<db>' "SELECT id, from_agent, read_at, body FROM messages WHERE team=… AND ((PING by task_id) OR (PONG by task_id));"`, or a line saying the db path could not be resolved.

   The stdout `linkage=unreached rc=<n> hint=<…>` line is unchanged.
3. **SKILL.md pane-less bullet:** the `poke.sh <team> <worker> --body-file` PING clause now reads: treat the `linkage=` line from `--add-worker` as the PING evidence; on `pong=no` or `linkage=unreached`, wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane>` and verify `read_at`; `poke.sh` only for a viewed workspace. "dispatch no AGMSG-TASK before its AGMSG-PONG arrives" is kept.
4. **`check-regime-boundary.sh` shdoc:** `@description` now names the untracked scan of every registered checkout and the active-seat rule (exactly one name across claude-code and codex at the main checkout and manifest `worker_worktree`; an empty seat is reported). It also names the per-type ">1" rule elsewhere.
5. **SKILL.md teardown bullet:** "one distinct name per type is healthy" is now scoped to non-seat worktrees. An active seat holds exactly one name across both types, which `make check-regime-boundary` enforces.
   - Rule file confirmed: `home/dot_config/claude/rules/agmsg-orchestration.md` has no `identities.sh`, distinct-name or `poke.sh <team> <worker>` wording (grep: no match).
   - No test or script pins the old wording.

**Tests:**
- `test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn`: `known` = [p1]; after spawn the workspace lists p1 and p9, and the record names p1. The stderr line is printed, the PING goes to p9, and nothing is dispatched to p1.
- `test_add_worker_linkage_failure_prints_the_invocation_and_the_query`: dispatch exits 4. The stdout line is `linkage=unreached rc=4 hint=attach-a-client`, and stderr carries:
  - the fake dispatch's own `agmsg-dispatch: fake wake refused`;
  - the exact invocation with `exited 4.`;
  - the query naming the fake db, with this PING's task_id in both the PING and the PONG predicates.
- **Fixture change:** a failing fake `agmsg-dispatch` now writes one stderr line.

**Negative check against d806a3d:** with the d806a3d `herdr-agents` swapped in and then restored (`cmp` exit 0), both new tests **fail**.

**Checks at 98ea49f:**
- `make render-check`: exit 0.
- `make unit-test`: 681 tests OK, 1 skipped; exit 0.
- `make validate-agent-assets`: exit 0.
- Repo-wide `shfmt -d` (3.14.1): exit 0.
- `shellcheck` on both scripts: exit 0.
- `make check-regime-boundary` (live): exit 2. It reports only the 35 expected mid-session untracked-evidence lines and no identity, crit, workspace or lock findings.

**Observation outside r8** (for the orchestrator): the same pane-less bullet still tells the orchestrator to "confirm that `team.sh <team> --json` shows the worker's `run/spawn.*` placement". That is the call an earlier revision removed from the linkage check because it observes Codex members by reading their pane. I left it unchanged because the amendment scoped only the PING clause.

**CompactionDB:** the r1 memory (85a51aeb-9a9b-494e-b66f-3fca94d147b6) stands. The r8 rules are in the learning file (item 18) for acceptance-time consolidation.

cost: n/a

## Revision 9 (orchestrator status=revise 21:14:34Z; amendment r9; task_rev 91da5b64…8d5a verified)

One commit, **a71e78d**, on 98ea49f, pushed without `-u`. There was no force push. PR #220 head: `a71e78defb5f07c2977b3e2f39bb89003bbcec0d`. CI results are in the validation file.

Both items are in `home/dot_agents/skills/agmsg-orchestration/SKILL.md` line 22, the pane-less bullet:

1. **Audit P2:** the recovery wake is now `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'`, with the message as the required fifth argument.
2. **Placement check:** the bullet no longer says to confirm placement via `team.sh <team> --json`. It now reads: confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and from the `linkage=` line printed by `--add-worker`. It also states why `team.sh --json` is not used: it observes Codex members by reading their pane.

**No pinning test:** `grep -rn` over `tests scripts Makefile` for `team.sh <team> --json`, `agmsg-dispatch <team> <orchestrator> <worker> <pane>` and ``terminal`/`pane` fields`` finds no match (exit 1, pasted in the validation file).

**Checks at a71e78d:** `make render-check` exit 0 and `make validate-agent-assets` exit 0, both run in worker-c.

**Codex GitHub review:** none was posted for 98ea49f before the push. The latest PR comment or review is from 17:31:00Z, before 98ea49f existed. Any later item is left to the orchestrator's sweep.

**CompactionDB:** the r1 memory (85a51aeb-9a9b-494e-b66f-3fca94d147b6) stands. No new memory was added for r9.

cost: n/a
