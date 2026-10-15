---
task_id: dotfiles-T128-seat-liveness-a01
seat: claude-standard-dot-a003
commit: 89a55bbd
---

# Validation: dotfiles-T128-seat-liveness-a01

## 1. The Check's outputs

The task copy's hash, the four premises (1, 0, 189 and 9, as the task states), the base, the two test modules, shellcheck and shfmt on the two scripts, and the size:

```text
$ shasum -a 256 .orchestration/dotfiles-T128-seat-liveness-a01/task.md
eb50e54f2427d9acc5fd9f0f1fb1e6f934828cf5c47c8530e5cca1da065ae9c9  .orchestration/dotfiles-T128-seat-liveness-a01/task.md
$ the four premises
1
0
189
9
$ git merge-base HEAD origin/main
59599783

$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest -v tests/unit/test_check_regime_boundary.py tests/unit/test_herdr_agents.py  # the new tests, the summary, the failing names
(rc=1)
test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal ... ok
test_attach_names_stale_seats ... ok
test_remove_worker_stale_retires_a_seat_whose_pane_is_gone ... ok
Ran 201 tests in 234.267s
FAILED (failures=28, errors=3)
failing here: 31

$ the same command on origin/main in a scratch worktree (git worktree add --detach; removed after), then diff of the failing names
FAILED
Ran 198 tests in 238.406s
identical failure sets (31 names)

$ shellcheck scripts/check-regime-boundary.sh home/dot_local/bin/common/executable_herdr-agents; shfmt -d (the same two)
(rc=0)
$ ruff format --check (the two test modules)
2 files already formatted

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
112	14	home/dot_local/bin/common/executable_herdr-agents
34	2	scripts/check-regime-boundary.sh
41	0	tests/unit/test_check_regime_boundary.py
99	0	tests/unit/test_herdr_agents.py
files: 4; changed lines outside tests/ and .orchestration/: 162; added under tests/: 140
```

**The three new tests pass.** The modules run all 201 tests: the 198 existing plus the three new ones.

**The 31 failures are the environment's.** In this seat's sandbox, 28 tests fail and 3 error, all in `test_herdr_agents.py`'s `--add-worker` and seat-claim groups. The same command on `origin/main`, in a scratch worktree, fails the identical 31 names out of its 198. So this seat's sandbox fails them, not this change. CI runs both modules on GitHub.

**Commit signing is off for this run.** The tests make commits, and commit signing from the global git configuration fails in this sandbox: `git commit` exits 128 there. The runs set `commit.gpgsign=false` through git's environment configuration, which is what CI's unsigned runner amounts to.

## 2. Mutation proofs

Each mutant is applied to the working file, its test runs (with the same git environment), and the file is restored byte for byte:

```text
S1 boundary: every state reads unknown -> test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal: killed (FAILED (failures=1))
S2 boundary: unknown counts as gone -> test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal: killed (FAILED (failures=1))
S3 launcher: no seat_stale= lines -> test_attach_names_stale_seats: killed (FAILED (failures=1))
S4 launcher: seat_stale= also for a skipped claim -> test_attach_names_stale_seats: killed (FAILED (failures=1))
S5 launcher: --stale skips the state check -> test_remove_worker_stale_retires_a_seat_whose_pane_is_gone: killed (FAILED (failures=1))
S6 launcher: the record is not moved -> test_remove_worker_stale_retires_a_seat_whose_pane_is_gone: killed (FAILED (failures=1))
S7 launcher: --stale still despawns -> test_remove_worker_stale_retires_a_seat_whose_pane_is_gone: killed (FAILED (failures=1))
S8 launcher: unknown counts as gone -> test_attach_names_stale_seats: killed (FAILED (failures=1))
mutants 8/8 killed; tree restored
```

A first run had S4 and S8 survive: the attach test then had no `unknown` case and no skipped-claim case. Both cases were added before the commit, and the run above is the final one.

## 3. The repository validator

```text
$ UV_OFFLINE=1 uv run --no-project --with pyyaml scripts/validate-agent-assets.py 2>&1 | tail -1  # on 89a55bbd, before the commit
agent asset validation ok
(rc=0)
```

## 4. Revise round 2 (`3cc248cb`)

The ACCEPTANCE `status=revise` of 07:49:10Z (previous head `cb9ea17c`, the orchestrator's update-branch merge onto `907522c2`) carries two audit findings:

- **The P2.** On the `--stale` path, a failed `delivery.sh set off` or `leave.sh` was suppressed, and the record still moved.
- **The P3.** §1's baseline claim lacked the pasted names.

**The fix.** On the `--stale` path both steps now run before the record is touched. A failure prints `herdr-agents: <step> failed; <name> keeps its placement record.` on stderr, keeps the record and exits 1. The despawn path is unchanged.

**The check.** `test_remove_worker_stale_keeps_the_record_when_cleanup_fails` uses a fake `leave.sh` that exits 1. It asserts exit 1, the stderr line, the record byte-identical, no `stale/` directory and no retired line, and the delivery and leave calls in order with no despawn.

```text
U1 the leave.sh failure suppressed (the audited behaviour) -> test_remove_worker_stale_keeps_the_record_when_cleanup_fails: killed (FAILED (failures=1)); file restored: True
```

### The baseline comparison, pasted (the P3)

The two modules ran on this branch, in the working tree at `cb9ea17c` with the round's edits (committed right after as `3cc248cb`). They also ran on `origin/main` (`907522c2`) in a scratch worktree, which was added with `git worktree add --detach` and removed with `git worktree remove`. Both runs used the same git environment.

Here are the failing names of each run and their diff. The diff is empty: both runs fail the same 31 names. The branch runs 202 tests (198 plus 4 new), and all four new ones pass.

```text
$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_check_regime_boundary.py tests/unit/test_herdr_agents.py
# on this branch, cb9ea17c
Ran 202 tests in 250.332s
FAILED (failures=28, errors=3)
# on origin/main, 907522c2, in a scratch worktree
Ran 198 tests in 207.837s
FAILED (failures=28, errors=3)
# the failing names on this branch (31)
ERROR: test_add_worker_derives_the_default_herdr_socket_for_spawn
ERROR: test_add_worker_linkage_refuses_a_placement_conflict
ERROR: test_add_worker_linkage_resolves_an_id_keyed_placement_record
FAIL: test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits
FAIL: test_add_worker_emits_no_override_for_an_unparseable_codex_config
FAIL: test_add_worker_exits_zero_when_a_timed_out_spawn_still_links
FAIL: test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array
FAIL: test_add_worker_linkage_failure_prints_the_invocation_and_the_query
FAIL: test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver
FAIL: test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping
FAIL: test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace
FAIL: test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn
FAIL: test_add_worker_linkage_ignores_a_placement_record_from_another_workspace
FAIL: test_add_worker_linkage_ignores_a_pong_older_than_this_ping
FAIL: test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal
FAIL: test_add_worker_linkage_refuses_several_orchestrator_identities
FAIL: test_add_worker_linkage_survives_a_non_numeric_pong_wait
FAIL: test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh
FAIL: test_add_worker_names_the_seat_from_a_codex_orchestrator_identity
FAIL: test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options
FAIL: test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog
FAIL: test_add_worker_reports_a_failed_spawn
FAIL: test_add_worker_reports_linkage_ok_after_a_ready_spawn
FAIL: test_add_worker_reports_linkage_unreached_after_a_failed_spawn
FAIL: test_add_worker_reports_shallow_metadata_as_not_granted
FAIL: test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace
FAIL: test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args
FAIL: test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog
FAIL: test_added_worker_boot_keeps_the_inherited_github_environment
FAIL: test_added_worker_boot_keeps_the_inherited_github_environment
FAIL: test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude
# the failing names on origin/main (31)
ERROR: test_add_worker_derives_the_default_herdr_socket_for_spawn
ERROR: test_add_worker_linkage_refuses_a_placement_conflict
ERROR: test_add_worker_linkage_resolves_an_id_keyed_placement_record
FAIL: test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits
FAIL: test_add_worker_emits_no_override_for_an_unparseable_codex_config
FAIL: test_add_worker_exits_zero_when_a_timed_out_spawn_still_links
FAIL: test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array
FAIL: test_add_worker_linkage_failure_prints_the_invocation_and_the_query
FAIL: test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver
FAIL: test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping
FAIL: test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace
FAIL: test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn
FAIL: test_add_worker_linkage_ignores_a_placement_record_from_another_workspace
FAIL: test_add_worker_linkage_ignores_a_pong_older_than_this_ping
FAIL: test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal
FAIL: test_add_worker_linkage_refuses_several_orchestrator_identities
FAIL: test_add_worker_linkage_survives_a_non_numeric_pong_wait
FAIL: test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh
FAIL: test_add_worker_names_the_seat_from_a_codex_orchestrator_identity
FAIL: test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options
FAIL: test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog
FAIL: test_add_worker_reports_a_failed_spawn
FAIL: test_add_worker_reports_linkage_ok_after_a_ready_spawn
FAIL: test_add_worker_reports_linkage_unreached_after_a_failed_spawn
FAIL: test_add_worker_reports_shallow_metadata_as_not_granted
FAIL: test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace
FAIL: test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args
FAIL: test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog
FAIL: test_added_worker_boot_keeps_the_inherited_github_environment
FAIL: test_added_worker_boot_keeps_the_inherited_github_environment
FAIL: test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude
$ diff <origin/main names> <branch names>
(diff rc=0)
```
