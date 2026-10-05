# Report: dotfiles-T65-agent-stop-gate-a01

- Worker: `claude-standard-dot-a007` (worktree `.claude/worktrees/worker-e`). The task file was verified against `task_rev` `sha256:f42bafa37d9a5c7c05483de9178e54f2971ca27e227778cdeafd7467cdb2f255` before any work started.
- PR: https://github.com/mryfmo/dotfiles/pull/237 (`feat/agent-stop-gate` → `main`). Final head `13340185a9f80de1095cd1a4afcf5db4f90bd189` on base `c6de5156`. CI is green on the final head; see validation.
- Status: ready_for_review.

## Before merge: two orchestrator decisions

1. **Untracked `references/*` in the main checkout.** A live dry run of the gate at the main checkout reports 34 untracked `references/*` files. They belong to the operator and have nothing to do with the regime. Following the spec, the gate counts them as dirty-tree violations. After merge, the orchestrator seat would therefore be blocked once at every stop: the next stop has `stop_hook_active` set, which skips the dirty-tree check. Claude Code also caps consecutive Stop-hook blocks at 8. Before merging, park them (for example in `.git/info/exclude`) or amend the spec with an exclude list. I did not widen the exclusions: that is outside the allowed scope.
2. **Two legacy RESULTs never got an ACCEPTANCE on the bus.** The gate now reads the full team history, and it reports `dot-claude-sandbox-T13-a01` and `dot-mosh-and-asset-bumps-T31-a01` as pending for `claude-remediation-dot`:
   - T13: a revise ACCEPTANCE was followed by a `status=blocked` RESULT, and no message came after it.
   - T31: the revision-2 RESULT was never acknowledged with an agmsg ACCEPTANCE.

   This pending-message check runs even when `stop_hook_active` is set. So until a closing `AGMSG-ACCEPTANCE v1` is sent for each, the orchestrator is blocked on every stop, up to the 8-block cap. `dotfiles-T64` also shows as pending, because its RESULT has just arrived (correct).

## Changes

- `scripts/agent-stop-gate.sh` (new, 126 lines, shdoc):
  - Reads the hook JSON with the bounded stdin and grep/sed pattern from agmsg `check-inbox.sh:75-77`.
  - Resolves the main checkout with `git rev-parse --git-common-dir`, as `check-regime-boundary.sh:28-33` does.
  - Classifies the seat. Orchestrator seat: the main checkout's own toplevel. Worker seat: a toplevel under `<main>/.claude/worktrees/`. Anything else exits 0.
- Orchestrator seat checks:
  - (a) `GIT_OPTIONAL_LOCKS=0 git status --porcelain --untracked-files=all` entries outside `.orchestration/` and `.agents/worklog/`, skipped when `stop_hook_active` is true.
  - (b) For each team of every unsuffixed claude-code identity at the main checkout: an `AGMSG-RESULT` addressed to it with no later `AGMSG-ACCEPTANCE` or `AGMSG-TASK` from it. This check ignores `stop_hook_active`.
- Worker seat check: for each claude-code identity registered at the worktree (solo or `-aNNN`), the latest `AGMSG-TASK` (or `AGMSG-ACCEPTANCE status=revise`) addressed to it must not be newer than its latest `AGMSG-RESULT` or `AGMSG-PONG status=blocked`.
- Exit 2 with one `agent-stop-gate: …` reason line per violation on stderr. Otherwise exit 0 silently. No network. The only git call uses `GIT_OPTIONAL_LOCKS=0`.
- Message source: agmsg's own storage facade, `scripts/lib/storage.sh`: `agmsg_storage_load`, `storage_store_exists`, `storage_history <team>`. This is the same read `history.sh` performs. The agmsg skill documents `history.sh` and forbids reading the database or calling `sqlite3` directly.
  - I first used `history.sh <team> "" 200`. A team-wide `history.sh` costs about 3 s on the live 600-message team because of its per-recipient unread pass, so the 200-row window was the only way to fit the budget. Codex P1 #2 showed that the window can drop an old pending RESULT.
  - The facade returns the whole history in about 0.1 s; the live hook runs in 0.18 s.
  - `history.sh <team> <agent>` is avoided on purpose: it self-names the caller's pane and session, which are writes.
  - Ceiling, marked with a `ponytail:` comment: an unreadable store blocks every turn once. Upgrade path: a timestamp cap or a fail-open switch.
- `.claude/settings.json`: one new `Stop` group, `{"type":"command","command":"bash","args":["${CLAUDE_PROJECT_DIR}/scripts/agent-stop-gate.sh"],"timeout":5}`. It uses the same exec form as the contextdb entries and is not async, so it can block.
- `tests/unit/test_agent_stop_gate.py` (new, 15 cases): a fixture repo with a nested `.claude/worktrees/x` worktree, a fake `identities.sh` (asserts `AGMSG_RESOLVE_PROJECT=0`) and a fake `lib/storage.sh` (asserts the team-wide read).
  - Cases from the spec: clean orchestrator, untracked file outside `.orchestration`, pending RESULT, RESULT then ACCEPTANCE, RESULT then revision TASK, worker TASK newer than RESULT, worker after RESULT, `stop_hook_active` skipping only the dirty-tree check.
  - Cases from the Codex findings: alive PONG, blocked PONG, revise ACCEPTANCE, solo unsuffixed worker, multi-team identity, unreadable store, non-seat checkout.

## Deviations from the task text (deliberate, from the Codex P1 review)

- Worker identity: the spec says "the `-aNNN` identity". The gate takes any claude-code identity at the worktree, so a solo worker is gated too (Codex P1).
- Worker "RESULT/PONG": only `PONG status=blocked` clears a task, and `ACCEPTANCE status=revise` reopens one (Codex P1 ×2). The orchestrator side clears on any `AGMSG-TASK` re-dispatch from it, not only one carrying `revision=`.
- Message source: the storage facade replaces the `history.sh` CLI, as explained above.

## Codex review dispositions (PR #237)

All five findings are P1 on `e11659ac` and all are `fixed:13340185a9f80de1095cd1a4afcf5db4f90bd189`. I replied inline to each and resolved no threads.

- 4175354523 handle all team memberships: fixed.
- 4175354526 200-message window: fixed by reading the full history through the facade.
- 4175354530 unsuffixed solo worker: fixed.
- 4175354531 PONG `status=alive` is not completion: fixed.
- 4175354533 revise ACCEPTANCE reopens the task: fixed.

A re-review on the final head was requested with `@codex review` (review 5403473331, 23:36Z). It raised no P0/P1, only two lower-priority findings. Both are left open for the orchestrator's disposition, since the task mandate covers P0/P1 fixes only:

- **4175410263, P2: fail closed when `identities.sh` cannot run.** Today a missing or failing lookup is indistinguishable from a non-seat, so the hook exits 0. Failing closed would block every stop on a machine or checkout without agmsg, including plain non-regime sessions. That is a policy tradeoff. Suggested: `not-applicable` with that reason, or a follow-up task that fails closed only when the `.claude/worktrees` / main-checkout seat is known to be registered.
- **4175410266, P3: JSON-escaped `cwd`.** A checkout path containing `"` or `\` would bypass the gate. Suggested: a follow-up that falls back to `$PWD`, which Claude Code sets to the project directory, or parses with `jq`. Not a P0/P1 risk here.

`mergeable_state` is `blocked` only because the review threads are unresolved. The ruleset requires resolution, and the task forbids the worker from resolving them. CI is green, and the branch is up to date with `main` (`c6de5156`).

## VERIFY (Claude Code hooks docs)

- Stop stdin: `stop_hook_active`, `last_assistant_message`, `background_tasks` and `session_crons`, plus the common `session_id`, `transcript_path`, `cwd`, `permission_mode` and `hook_event_name`. Source: https://code.claude.com/docs/en/hooks#stop. Quote: "Stop hooks receive `stop_hook_active`, `last_assistant_message`, `background_tasks`, and `session_crons`. The `stop_hook_active` field is `true` when Claude Code is already continuing as a result of a stop hook."
- Exit 2 on Stop: blocks the stop, and stderr reaches Claude. Source: https://code.claude.com/docs/en/hooks#exit-code-2-behavior-per-event. Quotes: "`Stop` | Yes | Prevents Claude from stopping, continues the conversation"; "Claude receives the stderr message as the explanation for why it should continue." Consecutive blocks are capped at 8 (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`). Exit 0 stderr only goes to the debug log.
- Trust: there is no per-change approval. Hooks from any settings file run only after the one-time workspace trust dialog for the folder, and `/hooks` is a read-only browser. Edits are picked up by the settings file watcher. Source: https://code.claude.com/docs/en/hooks#workspace-trust. Quote: "Claude Code holds back hooks from every settings file … until you accept the workspace trust dialog for the folder"; "Direct edits to hooks in settings files are normally picked up automatically by the file watcher."
- The exec form `args` array is documented at https://code.claude.com/docs/en/hooks#exec-form-and-shell-form ("Set `args` whenever the hook references a path placeholder").
- Live confirmation: the edited worktree `settings.json` took effect in this running session. The Stop hook blocked this seat with exactly the T65 reason line.

## CompactionDB

The decision was recorded in the main checkout:

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T65 (operator 2026-10-03): a project-level Stop hook scripts/agent-stop-gate.sh blocks the orchestrator seat from stopping with repository changes outside .orchestration or with a RESULT lacking an ACCEPTANCE, and blocks a worker seat from stopping with a TASK lacking a RESULT/PONG; exit 2 with reasons, no prompt.'
```

Output: `1680aee8-ce0c-4f11-83c6-915814de3eb2` (pasted in validation).

[memory:decision] dotfiles-T65: the Stop gate reads agmsg history through the storage facade `lib/storage.sh` `storage_history <team>` (the `history.sh` read without its unread pass), never `history.sh <team> <agent>` (it self-names the pane) and never the database directly.

## Notes

- The Understand-Anything hook did not fire during this task.
- One CI flake was re-run: `public-bootstrap (ubuntu-24.04, client)` got a connection reset downloading the `Hack.zip` release asset, and fail-fast cancelled the other two bootstrap jobs. All passed on re-run.
- Sandbox artefacts (`.git/config.lock` stub, 0-byte placeholders in worker-e): see the sandbox file.

cost: n/a (Claude Code does not expose session token or cost figures to the worker)

## Revise round 1

`task_rev` `sha256:5b7750b5…0205692` was verified before work started. Status: ready_for_review.

- One fix commit, `5a9f35f5be91dfa9e18ee94aa54f6823a1e079ac`:
  - **P2 (4175410263), failing identity lookup.** If `${scripts}/identities.sh` does not exist, the hook exits 0: this is not a regime machine, and the check runs before the dirty-tree check. If the script exists and exits non-zero, the hook blocks with `agmsg identity lookup failed for <top>; check …/identities.sh`, unless `stop_hook_active` is set. The exit status is captured in a variable rather than read through a process substitution.
  - **P3 (4175410266), JSON-escaped `cwd`.** `cwd` and `stop_hook_active` are parsed with `jq -r '.cwd // empty'` and `jq -r '.stop_hook_active // false'`, and the `${PWD}` fallback is kept.
  - **Tests (18 now):** `test_failing_identity_lookup_blocks_once`, `test_missing_agmsg_install_passes` and `test_json_escaped_cwd_resolves`. For the last one, the fixture repository path now contains a quote and a backslash, so every case exercises JSON-escaped paths. Both new fix tests fail against the previous head's script (2 failures, pasted in validation).
- `main` moved to `a575b3cc` (#236), so I ran `gh pr update-branch 237`. The final head is `1ee605c6183c9e4afaa212d5247ce78a2dcffa0a` (a GitHub merge commit on top of `5a9f35f5`).
- Results on the final head: local `make unit-test` 731 OK, `make validate-agent-assets` ok, and CI all green; all pasted in validation.
- I replied `fixed:5a9f35f5…` to both threads and resolved none.
- **Codex re-review of `1ee605c6`** (review 5403515715) raised one new finding, which I left for disposition and did not fix. The revise round asked for exactly the two open findings in one commit, and the base mandate is P0/P1:
  - **4175454186, P2: inspect both sides of a rename.** For a staged rename row `R  .orchestration/x -> src/y`, `path` starts with the exempt old name, so the row is skipped. Effect: an orchestrator could stop with a staged rename that moves a file out of `.orchestration/` into a source path. This needs a staged `git mv` in the main checkout, which the orchestrator never performs under the delegation mandate.
  - Fix if wanted (about 5 lines plus one test): read `git status --porcelain -z`, take the rename's destination entry, and exempt a row only when both endpoints are under the exempt prefixes.
  - Suggested disposition: `not-applicable` (the orchestrator does not stage renames in the main checkout), or a follow-up revise round.
- CompactionDB: no new decision for this round. The task's `[memory:decision]` is unchanged and was recorded as `1680aee8-ce0c-4f11-83c6-915814de3eb2`.

cost: n/a

## Revise round 2

`task_rev` `sha256:bafce42b…dce4e33` was verified before work started. Status: ready_for_review.

- **Rename fix, commit `775a527ad70153679362d3cd2220a3ebe1f15a2e` (the round-2 commit).** The dirty-tree check reads `git status --porcelain -z`. A rename or copy row consumes its source record and is exempt only when both endpoints are under `.orchestration/` or `.agents/worklog/`. Otherwise the gate reports `<dest> (from <src>)`. Test: `test_staged_rename_out_of_orchestration_blocks`, which fails on the round-1 script.
- **Codex review of `2e455e8a`** raised a **P1** (4175508812: worker completion must be tracked per task_id) and a P2 (4175508814: a failed `git status` is swallowed). Under the base Completion rule ("fix P0/P1 and repeat") I fixed both in **`8433a01b158856a8ef26254ebb59de63ae759389`**. I included the P2 because every earlier round converted the open P2s anyway.
  - The worker seat now keeps a pending set keyed by task_id.
  - A trailing `rc=<n>` NUL record carries git's exit status; a failure blocks unless `stop_hook_active`.
  - Tests: `test_worker_tracks_each_task_id` and `test_failing_git_status_blocks`. Both fail on `775a527a`.
  - Codex then reported "Didn't find any major issues" on `8433a01b`.
- **Codex auto-review of the merge head `110c0500`** raised two P2s. I fixed both in **`a62fce9da1cceb44d78ae1b11623fe12a574ebb7`**:
  - 4175589471, `storage_history` → `storage_init` writes to an off-revision store. For the sqlite driver, the hook first reads `PRAGMA user_version`, the same read as `storage_init`'s fast path. A truncated, corrupt or stale store is reported as unreadable instead of being re-initialized. The live store is at rev 1 of 1 and passes.
  - 4175589472, a busy store outlives the 5 s hook timeout. The read sets agmsg's documented `AGMSG_BUSY_TIMEOUT=1000`.
  - Test: `test_sqlite_store_off_the_current_schema_is_not_initialized`, which fails on `8433a01b`. The fake storage asserts the busy timeout in every test.
- `main` moved three times (#238, #239, #241). After each move I ran `gh pr update-branch`. The final head is **`2da1794604c8f684377e8b4ac0f8c058436d6d65`**.
- Results on the final head: CI green, 22 gate tests, `make unit-test` 744 OK, `make validate-agent-assets` ok. Every fixed thread has a `fixed:<sha>` reply, and no thread is resolved.

### Pre-merge item: stale open worker tasks (per-task_id tracking)

With per-task_id tracking, a worker task stays open until **the worker itself** sends a RESULT or a `PONG status=blocked` for that id. Nothing the orchestrator sends closes it on the worker seat.

Several times in the past the orchestrator withdrew a task with `AGMSG-ACCEPTANCE status=revise` (for example `task-withdrawn`, `lane-reclaimed`). The gate counts those as reopening the task, so they stay open forever. Live run of the final-head script (see validation), seated worktrees only:

| Seat | Open task_ids | Last message (UTC) | State |
|---|---|---|---|
| worker-c / a005 | `dot-ua-incremental-T20-a01` | 2026-09-26T03:55Z, ACCEPTANCE revise ("task-withdrawn …") | stale |
| worker-c / a005 | `dot-orchestrator-guardrails-T21-a01` | 2026-09-26T03:13Z, ACCEPTANCE revise ("lane-reclaimed …") | stale |
| worker-c / a005 | `dotfiles-T67` | current dispatch | in flight |
| worker-d / a006 | `dotfiles-T88` | current dispatch | in flight |
| worker-e / a007 | `dotfiles-T65` | this task | in flight until this RESULT |

The earlier simulation also found T89 for a005 and T66 for a006, both dispatched today; they are no longer open. Identities a001–a004 aren't registered at any worktree, so the gate never applies to them.

Until T20 and T21 are closed, a005 is blocked at every stop, up to the 8-block cap per turn. The orchestrator has two options:

- Have a005 send `AGMSG-PONG v1 task_id=<id> status=blocked note=withdrawn` for each of the two ids.
- Or add a state-machine rule in a follow-up: an ACCEPTANCE `status=accepted` addressed to the worker closes that id. That is one awk branch, and no round has asked for it.

### Open Codex findings on the final head (review 5403719541), left for disposition

These two arrived after five fix commits; each new head has drawn fresh P2s, so I stopped the loop rather than chase them unasked. Both are review-level comments (line `null`).

- **4175647967, P2: fail closed when a registered team's store is missing.** agmsg's own `history.sh` treats a missing store as "the ordinary state of a freshly joined team rather than a broken install" and reads it as empty history. Blocking on it would gate every newly joined seat until its first message. Suggested: `not-applicable` with that reason.
- **4175647971, P2: `GIT_DIR`/`GIT_WORK_TREE` inherited from the launcher.** Valid in principle; neither `herdr-agents` nor Claude Code sets them for these seats. If wanted, it is a one-line fix: `unset GIT_DIR GIT_WORK_TREE` before the `rev-parse` probes. Suggested: fix it in a final round, or `not-applicable` because seats are launched only through `herdr-agents`.

cost: n/a

## Revise round 3 and addendum

`task_rev` `53d1a4a3…` (round 3) and `96d5939b…` (addendum) were both verified. Status: ready_for_review.

- **Round 3, commit `ea112e2e56f67fd56a2f99ae72b13d660286f439`:**
  - `unset GIT_DIR GIT_WORK_TREE` runs before the `rev-parse` probes. `GIT_INDEX_FILE` is kept, as instructed. Test: `test_inherited_git_dir_does_not_hide_the_seat`.
  - On a worker seat, an `AGMSG-ACCEPTANCE` addressed to the worker with any status other than `revise` closes that task_id; `status=revise` still reopens it. Test: `test_worker_task_closed_by_a_non_revise_acceptance`, which covers both cases.
  - Missing store (4175647967): no code change, `not-applicable` as agreed. I replied `fixed:ea112e2e…` on 4175647971 only, resolved no threads, and left 4175647967 to the orchestrator.
- **Addendum, commit `a9a85ecf4eb7427dea440c81e117087acfa94dcf`:**
  - **Budget.** All history reads share one 3 s deadline inside the 5 s hook timeout. Each read runs under `timeout <remaining>`, and a spent budget never calls `timeout 0`, which would mean no limit. On expiry the gate adds `agmsg history read exceeded the hook budget; retry` and exits 2 immediately. Test: `test_slow_store_blocks_within_the_budget`, with a sleeping fake, blocks in about 3 s.
  - **Test strength.** The fake storage records every `storage_history` call and no longer rejects stale revisions itself. The schema test asserts `storage_history` was **not** called on a revision mismatch. With the production preflight disabled, the test fails.
  - **Preflight race, not-applicable (upstream limitation).** `storage_history` always runs `storage_init`, and `storage_init`'s own revision read can fail under `SQLITE_BUSY` and fall through to its write batch. The mitigations are the gate's preflight `PRAGMA user_version` read and `AGMSG_BUSY_TIMEOUT=1000`. Only an upstream non-initializing history read closes the race, for example a `storage_history --no-init` / read-only `storage_history` in agmsg's `lib/storage.sh` facade. This is documented at `read_history`.
- **Two CI-driven follow-up commits (same task):**
  - `4dfceb6e2f955ffd02f0c5d26c937adabdb12e3b`. CI's ShellCheck 0.9.0 flagged the body of the exported `read_history`, which only ran through `bash -c`, as unreachable (SC2317), and the ShellCheck step exited 123. The gate now calls itself as `--read-history <team>` under `timeout`, documented as an internal `@option`. The function is called directly, inherits `pipefail`, and needs no disable directive.
  - `cb3ded43538bf3136ea768d6b46f0eb3b5e40a72`. Stock macOS has no `timeout(1)`, so on `test (macos-14, client)` every read exited 127 and all gate tests failed. Like agmsg's `check-inbox.sh`, the gate now falls back to an uncapped read when `timeout` is missing; that is a `ponytail:` ceiling, where the budget is checked only between teams. The slow-store test is skipped there. Locally, with `timeout` removed from PATH: 24 OK, 1 skipped.
- **Codex.** It reported "Didn't find any major issues" on `9f27743b`. The `@codex review` on `cb3ded43`, at 02:16:52Z, got no reaction and no review within 20 minutes. The delta from `9f27743b` is only the macOS fallback.
- **Local results on `cb3ded43`:** 25 gate tests, `make unit-test` 751 OK, `make validate-agent-assets` ok, ShellCheck and shfmt clean. *(Corrected in round 6: I originally wrote "no `shellcheck disable` in the script", which was false. One intended `# shellcheck disable=SC1091` precedes the `source` of the agmsg storage facade, whose path is resolved at runtime. The validation output always showed the count as 1. What round 3 removed were the SC2317/SC2329/SC2016 disables for the old `bash -c` read.)*
  - Two earlier `make unit-test` runs failed in `test_herdr_agents` regime-boundary tests because `pgrep -f 'crit _serve'` matched. The first was **this session's own leftover Plan Mode Crit server** (pid 4150161, for the actas plan), which I stopped. The cause of the second failure is unconfirmed. The third run passed. All three are pasted in validation.
- **Branch.** I updated onto `a5c30b6d` (#240); the merge head is `cd612f62cfe6f7499876641b8ca1f69fafbea7e2` and CI is all green on it. `main` has since moved to `138e6a72`, so the PR shows `behind`. Other workers keep merging, so I stopped chasing the base. No merge so far has touched the PR's files. **Run `gh pr update-branch 237` once at merge time.**
- **Script size.** It is now 189 lines, beyond the original 150-line target. The growth is entirely from fixes asked for in the review rounds.
- **Live seats** (message checks only; see validation):
  - worker-c / a005: T20 and T21 are still open until the orchestrator sends the planned `status=withdrawn` ACCEPTANCEs, plus the in-flight `dotfiles-T91`.
  - worker-d / a006: `dotfiles-T88`.
  - worker-e / a007: `dotfiles-T65`, until this RESULT.

cost: n/a

## Revise round 4 and addendum

`task_rev` `051ac01e…` (round 4) and `d5844f02…` (addendum) were both verified. Status: ready_for_review.

**Correction of the round-3 report.** It said "no Bot response on cb3ded43". That was wrong. The Bot had reviewed `cb3ded43` (02:21:40Z) and `cd612f62` (02:46:48Z). My queries were not paginated: replies count as reviews and comments, so after more than 30 of each the newest entries fell off the first page. Every listing below uses `--paginate`, plus the GraphQL `reviewThreads.isResolved` query.

### Commits

- `bc636cb795171cd1ea2b64039b1527ab4061d169` (round 4):
  - **Peer correlation.** `pending[id]` stores the counterparty, and only a message between the seat and that peer closes the task. Tests cover both seats.
  - **Git overrides.** The gate unsets `GIT_DIR GIT_WORK_TREE GIT_COMMON_DIR GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES`. Test: an inherited alternate index that matches HEAD, while the real index holds a staged change, now blocks. The git-status failure test now corrupts `.git/index` instead of relying on `GIT_INDEX_FILE`.
  - **Main worktree, deviating from the instruction.** I did not use `git worktree list`. For a `--separate-git-dir` main worktree it prints the metadata dir (`…/sep.git`, pasted in validation), so it cannot fix 4175883204. The seat is classified by Git's layout instead:
    - main worktree: `--git-dir` equals `--git-common-dir`;
    - worker: the toplevel is under `<main>/.claude/worktrees/`, and `<main>`'s git dir is that common dir.

    Test: `test_separate_git_dir_main_worktree_is_a_seat`. Parity gap for a follow-up: `scripts/check-regime-boundary.sh` still uses `${common%/.git}`.
  - **Timeout runner.** `runner="$(command -v timeout || command -v gtimeout || true)"` serves both bounded reads.
- `1845139e3e2449408be571b330be496e36b03591` (addendum): when neither `timeout` nor `gtimeout` exists, the history read runs as a background child with a sleep-and-kill watchdog, and an expiry maps to exit 124.
  - The reader writes to a temp file, so a leftover grandchild cannot hold the pipe.
  - The uncapped fallback and its `ponytail:` comment are gone.
  - The slow-store test runs on every platform, with variants for a PATH without `timeout` (watchdog) and a PATH with `gtimeout` only. The stand-in `gtimeout` is a wrapper script, because Ubuntu 26.04's multicall coreutils dispatches on argv[0], which made a symlink fail on that CI job.
  - The stdin read keeps runner-or-uncapped: bash gives background jobs `/dev/null` as stdin, so a watchdog cannot bound it.
- `3568b7e228e69aa5f8a74a36838ece87e386b02a`, from the Bot reviews of `b49f5630` and `1845139e`:
  - **P1 4175978489.** The seat is classified from `CLAUDE_PROJECT_DIR` before the hook `cwd`. Tests strip this session's own `CLAUDE_PROJECT_DIR` from the environment.
  - **4175949364.** `GIT_CEILING_DIRECTORIES` is unset. A variant, but a one-word fix in the same line.
  - **4175949366.** Reported paths are quoted with `printf %q`. This is a trust boundary: repository data reaches Claude through stderr.
- `8262be37669f69924f9d94b31d6bbe02e8208277`: the macOS CI job showed a watchdog race. `wait` could return before the watchdog subshell exited, so the expiry read as "unreadable". Exit status 143 (only the watchdog sends TERM) now maps to 124. macOS CI is green since then.
- After `main` moved, I updated the branch twice (`b49f5630`, `dece585f`). Final head: **`dece585f5a9d6ec4ee717e8fc06aebe82277ac0c`**. CI is all green there, and the branch is current with `main` `8922f13b`.

### Test results on the final head

- 34 gate tests pass. With `timeout` and `gtimeout` removed from PATH: 33 OK, and only the gtimeout-wrapper test is skipped.
- `make unit-test`: 734 OK. `make validate-agent-assets`: ok.
- Every new test fails against the script it fixes (pasted in validation).

### Every unresolved thread on the final head

The list comes from GraphQL `isResolved == false`. Threads I fixed have inline replies; no thread is resolved.

| Thread | Finding | Disposition |
|---|---|---|
| 4175723393 | Clear all Git repository overrides | `fixed:bc636cb795171cd1ea2b64039b1527ab4061d169` |
| 4175816307 | Clear `GIT_INDEX_FILE` | `fixed:bc636cb795171cd1ea2b64039b1527ab4061d169` |
| 4175883202 (P1) | Correlate completion with the peer | `fixed:bc636cb795171cd1ea2b64039b1527ab4061d169` |
| 4175883204 | Main worktree without a `.git` suffix | `fixed:bc636cb795171cd1ea2b64039b1527ab4061d169` (git-dir == common-dir, not `worktree list`) |
| 4175949364 | `GIT_CEILING_DIRECTORIES` | `fixed:3568b7e228e69aa5f8a74a36838ece87e386b02a` |
| 4175949366 | Escape untrusted filenames | `fixed:3568b7e228e69aa5f8a74a36838ece87e386b02a` |
| 4175978489 (P1) | Anchor to the project root | `fixed:3568b7e228e69aa5f8a74a36838ece87e386b02a` |
| 4175949362 | Bound the `git status` scan | proposed `not-applicable:` a variant of the budget class. The orchestrator checkout is this dotfiles repo, whose untracked scan takes milliseconds (build and cache trees are gitignored). Bounding it needs a second watchdog path for one probe. |
| 4176012055 | Quote `${top}` in the identity-lookup reason | proposed `not-applicable:` `top` is the operator's own project path (`CLAUDE_PROJECT_DIR`), not repository or agmsg content. A variant of 4175949366; one `printf %q` line if wanted. |
| 4176012056 | Bound `identities.sh` | proposed `not-applicable:` a variant of the budget class. `identities.sh` scans the local team config files only, with no store wait; one call per stop, in milliseconds. |
| 4176012058 | Fail closed when Git discovery fails | proposed `not-applicable:` a project whose Git metadata cannot be read has no seat to gate. Failing closed would trap every session in a broken or non-git checkout, and the 8-block cap would only delay that. |
| 4176012060 | Validate the protocol version | proposed `not-applicable:` `v1` is the only contract, and senders are authenticated team members. A malformed RESULT is a protocol violation that the orchestrator's acceptance review catches; the Stop gate is not a message validator. |
| 4176044539 (P1) | Keep merge-directed workers pending | proposed `not-applicable:` contradicts the round-3 rule (any non-`revise` ACCEPTANCE addressed to the worker closes the task; that is how withdrawal works). In this regime, acceptance merges are the orchestrator's (`gh pr merge --squash`). A worker task that must continue is re-dispatched as `status=revise` or a new TASK. `T21-model-profiles-pr.md` is a pre-regime record. |
| 4176068447 | Escape task IDs and team names | proposed `not-applicable:` a variant of 4175949366. `jq @tsv` escapes `\n`, `\r`, `\t` and `\\`, so a task_id cannot carry a line break into stderr. ANSI bytes from an authenticated team peer are a peer-trust question, not this gate's; a one-line `printf %q` per value if wanted. |
| 4176068448 | Clear injected Git configuration (`GIT_CONFIG_COUNT`/`KEY_n`/`VALUE_n`, `GIT_CONFIG_PARAMETERS`) | proposed `not-applicable:` a variant of the override class. Note that the Claude Code sandbox itself injects `GIT_CONFIG_PARAMETERS` (a credential helper) into Bash commands, so blanket-clearing needs care. Suggested follow-up: run the `git status` probe with `env -u GIT_CONFIG_PARAMETERS -u GIT_CONFIG_COUNT`. |

Resolved by the orchestrator before this list was taken: 4175687782 (multi-team budget; I replied `fixed:a9a85ecf4eb7427dea440c81e117087acfa94dcf`) and 4175723390 (portable runner; I replied `fixed:1845139e3e2449408be571b330be496e36b03591`).

### Pre-merge item from peer correlation

The orchestrator seat still shows `dot-claude-sandbox-T13-a01` as pending. Its RESULT came from **`claude-standard-dot-a003`**, but the closing `AGMSG-ACCEPTANCE … status=closed-historical` (2026-10-03T23:44:26Z) went to **`claude-standard-dot-a005`**. Under peer correlation, only an ACCEPTANCE to `claude-standard-dot-a003` closes it.

worker-c (a005) now passes, because the T20 and T21 withdrawals landed.

cost: n/a

## Revise round 5

`task_rev` `88744dc8…` was verified, and no addendum arrived before the push. Status: ready_for_review.

- **Fix commit `92cad328e0ea5d7d0b1a862b16557c6d832df571`:** `unset GIT_CONFIG_PARAMETERS GIT_CONFIG_COUNT` runs alongside the other overrides. The comment notes that Git ignores the numbered `GIT_CONFIG_KEY_n`/`VALUE_n` pairs once the count is unset.
- **Test deviation, with evidence:** the suggested `status.showUntrackedFiles=no` cannot fail the old script. The probe passes `--untracked-files=all`, which overrides it; a first version of the test passed on `dece585f` too, and a direct `git status` still lists the file. The test instead injects `core.excludesFile=<ignore-all>`, through both `GIT_CONFIG_COUNT/KEY_0/VALUE_0` and `GIT_CONFIG_PARAMETERS`. It fails on the `dece585f` script and passes now.
- **Hook environment:** the Claude Code process (pid 4144333) environment has no `GIT_CONFIG*` variables. The sandbox's credential helper is injected into sandboxed Bash commands only, so a plain `unset` is correct and `env -u` on the probes is not needed.
- **Final head `92cad328`:**
  - Every CI check passes (13 pass; `nix` is skipped).
  - The Codex Bot posted "Didn't find any major issues", with "Reviewed commit: 92cad328e0", at 04:25:29Z, and opened no new top-level threads.
  - The branch is up to date with `main` (`8922f13b`). `mergeable_state` is `blocked` only by the one unresolved thread below.
- **Local:** 35 gate tests pass; with `timeout`/`gtimeout` removed from PATH, 34 OK and 1 skipped. `make unit-test`: 735 OK. `make validate-agent-assets`: ok.
- **Remaining unresolved thread:** 4176068448 → `fixed:92cad328e0ea5d7d0b1a862b16557c6d832df571`. I replied inline and did not resolve it.
- **Live checks:** the orchestrator seat no longer lists T13, so the closure re-sent to a003 took effect. It now shows only current RESULTs (T68, T74, T75, T88).

cost: n/a

## Revise round 6

`task_rev` `dffb6d5e…` was verified. Status: ready_for_review.

- **Item 2: "never writes" was a false claim.** Commit `fd8aa360d0b1b5f942603f4a1588b5a02fcc361f` changes only the `@description`. It now says the hook never writes to the agmsg store or the repository, and needs no network. It also says that only the watchdog fallback, used when neither `timeout` nor `gtimeout` exists, creates one private `mktemp` file under `TMPDIR`, removed before it returns.
- **Item 4: the report claimed "no shellcheck disable".** That was false, and the claim is corrected in place in the round-3 section of this report. One intended `# shellcheck disable=SC1091` precedes `source "${scripts}/lib/storage.sh"`, whose path is resolved at runtime. Round 3 removed only the SC2317/SC2329/SC2016 disables. The validation file always showed the count as `1`, and it now carries a note saying so.
- **Items 1 and 3:** no change, as dispositioned (protocol version `not-applicable`; the line limit was waived).
- **Final head `fd8aa360`:**
  - CI is all green, and the branch is up to date with `main` `8922f13b`.
  - The Codex Bot posted "Didn't find any major issues" with "Reviewed commit: fd8aa360d0" at 05:09:26Z, and opened no new top-level threads.
  - Local: 35 gate tests pass, `make unit-test` 735 OK, `make validate-agent-assets` ok.

cost: n/a
