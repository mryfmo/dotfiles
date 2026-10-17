---
task_id: dotfiles-T129-anthropic-auth-runtime-check-a01
round: 1
status: local-validated
---

# Validation

Every command below ran from the worker-c worktree at the code commit 8cb93567 on base `origin/main` a8a747af, inside the Claude seat's sandbox. Each block is the verbatim output, with the real exit status printed by the runner script (`run-checks.sh` in the session scratchpad, pasted at the end with the probe it calls). Bats is not run locally (Test Policy); CI runs `bats -r "tests/install/common/"` through `scripts/run_unit_test.sh` and the RESULT names that run.

The full `tests/unit/test_runtime_health.py` run fails 8 of 55 tests, all `test_agmsg_*` installer tests of `scripts/update-agent-assets.sh`, none of them in this diff. They fail on `mktemp: mkstemp failed on /var/folders/...: Operation not permitted`, the seat's sandbox denying the system temp directory. The same module on a detached scratch worktree at `origin/main` a8a747af fails the identical 8 tests (second section), so they predate this change; the doctor fixture this task edits (`test_doctor_required_optional_and_healthy_statuses`) passes in both runs, and again with `ANTHROPIC_OAUTH_TOKEN` and `PI_CODING_AGENT_DIR` exported (item 3). CI's Python unit test job is the authority for the 8.

## The Check

```text
$ make render-check
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
exit=0

$ shellcheck -x scripts/check-tools.sh
exit=0

$ shfmt --indent 4 --space-redirects --diff scripts/check-tools.sh
exit=0

$ uvx ruff format --config ruff.toml --check tests/unit/test_runtime_health.py
1 file already formatted
exit=0

$ uv run python -m unittest tests/unit/test_runtime_health.py -v
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok
test_agent_asset_update_runs_gh_extension_ensure (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_launchers_do_not_hardcode_model_ids (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes) ... FAIL
test_agmsg_already_pinned_skips_download (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_already_pinned_skips_download) ... ok
test_agmsg_checksum_mismatch_fails_closed (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed) ... FAIL
test_agmsg_fresh_install_populates_skill_and_records_manifest (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest) ... FAIL
test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state) ... ERROR
test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state) ... ERROR
test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty) ... FAIL
test_agmsg_refuses_to_install_without_tar (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_without_tar) ... ok
test_agmsg_reports_an_installer_that_leaves_the_wrong_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version) ... FAIL
test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state) ... FAIL
test_agmsg_update_never_touches_teams_db_run (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_never_touches_teams_db_run) ... ok
test_client_bashrc_treats_private_sources_as_optional (tests.unit.test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... ok
test_codex_crit_normalizes_managed_marketplace_mode (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode) ... ok
test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... ok
test_crit_fails_without_an_install_when_the_download_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_fails_without_an_install_when_the_download_fails) ... ok
test_crit_never_promotes_a_staged_binary_that_prints_the_banner_but_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_never_promotes_a_staged_binary_that_prints_the_banner_but_fails) ... ok
test_crit_refuses_a_replaced_release_whose_checksums_txt_matches (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_refuses_a_replaced_release_whose_checksums_txt_matches) ... ok
test_crit_replaces_an_installed_binary_that_cannot_report_its_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_replaces_an_installed_binary_that_cannot_report_its_version) ... ok
test_crit_replaces_an_installed_binary_that_prints_the_banner_but_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_replaces_an_installed_binary_that_prints_the_banner_but_fails) ... ok
test_darwin_crit_checksum_failure_preserves_existing_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_darwin_crit_checksum_failure_preserves_existing_binary) ... ok
test_darwin_crit_install_is_pinned_atomic_and_recorded (tests.unit.test_runtime_health.RuntimeHealthTest.test_darwin_crit_install_is_pinned_atomic_and_recorded) ... ok
test_doctor_has_no_github_role_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_has_no_github_role_check) ... ok
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_linux_crit_checksum_failure_preserves_existing_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_checksum_failure_preserves_existing_binary) ... ok
test_linux_crit_correct_version_is_download_free (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_correct_version_is_download_free) ... ok
test_linux_crit_failure_does_not_leak_cleanup_trap (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_failure_does_not_leak_cleanup_trap) ... ok
test_linux_crit_install_is_pinned_atomic_and_recorded (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_install_is_pinned_atomic_and_recorded) ... ok
test_linux_crit_prefers_pinned_target_over_older_path_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_update_pulls_clean_main_before_apply (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_pulls_clean_main_before_apply) ... ok
test_make_update_reports_unmerged_feature_branch_before_branch_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_feature_branch_before_branch_notice) ... ok
test_make_update_reports_unmerged_index_before_dirty_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_index_before_dirty_notice) ... ok
test_make_update_skips_dirty_main_with_manual_pull_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_skips_dirty_main_with_manual_pull_notice) ... ok
test_upgrade_fails_and_keeps_the_backup_when_a_partial_install_cannot_be_removed (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_and_keeps_the_backup_when_a_partial_install_cannot_be_removed) ... ok
test_upgrade_fails_when_the_final_install_fails_after_a_rebuild (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_when_the_final_install_fails_after_a_rebuild) ... ok
test_upgrade_fails_when_the_node_marker_cannot_be_written (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_when_the_node_marker_cannot_be_written) ... ok
test_upgrade_failure_after_a_successful_install_only_warns (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_failure_after_a_successful_install_only_warns) ... ok
test_upgrade_homebrew_verifies_attestations_when_gh_is_present (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_homebrew_verifies_attestations_when_gh_is_present) ... ok
test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs) ... ok
test_upgrade_never_restores_an_undeletable_backup_over_a_completed_rebuild (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_never_restores_an_undeletable_backup_over_a_completed_rebuild) ... ok
test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run) ... ok
test_upgrade_restores_the_npm_tool_when_the_rebuild_is_interrupted (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_restores_the_npm_tool_when_the_rebuild_is_interrupted) ... ok
test_upgrade_runs_mise_against_the_applied_host_config_and_edits_no_file (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_runs_mise_against_the_applied_host_config_and_edits_no_file) ... ok
test_upgrade_self_updates_mise_to_its_latest_release (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_self_updates_mise_to_its_latest_release) ... ok
test_upgrade_skips_every_phase_when_ci_is_true (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_every_phase_when_ci_is_true) ... ok
test_upgrade_skips_unavailable_mise_self_update (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok

======================================================================
ERROR: test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 912, in test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state
    log = (repo / "commands.log").read_text()
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 986, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 970, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-501/runtime-health-test-0d1l43xd/agmsg-repo/commands.log'

======================================================================
ERROR: test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 978, in test_agmsg_migration_reports_an_installer_that_mutates_live_state
    self.assertNotIn("update=true", (repo / "commands.log").read_text())
                                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 986, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 970, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-501/runtime-health-test-5s5rxgar/agmsg-repo/commands.log'

======================================================================
FAIL: test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1014, in test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes
    self.assertNotIn("installer failed", output)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'installer failed' unexpectedly found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.0U0tVRvsCf: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-90gd49h4/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_checksum_mismatch_fails_closed (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 860, in test_agmsg_checksum_mismatch_fails_closed
    self.assertIn("checksum mismatch", result.stdout + result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'checksum mismatch' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.eMNlfF73ZL: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_fresh_install_populates_skill_and_records_manifest (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 819, in test_agmsg_fresh_install_populates_skill_and_records_manifest
    self.assertNotIn("installer failed", result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'installer failed' unexpectedly found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.jhDc2h9JYD: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1063, in test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty
    self.assertIn("hashed fewer live-state files than exist", output)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'hashed fewer live-state files than exist' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.LAYXOWgaUQ: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-5rm_b4b1/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: 1.0.0); see the reason above.\n'

======================================================================
FAIL: test_agmsg_reports_an_installer_that_leaves_the_wrong_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1033, in test_agmsg_reports_an_installer_that_leaves_the_wrong_version
    self.assertIn(
    ~~~~~~~~~~~~~^
        "agmsg: install.sh --cmd agmsg --agent-type claude-code left VERSION 9.9.9 (want 1.5.0)",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        output,
        ^^^^^^^
    )
    ^
AssertionError: 'agmsg: install.sh --cmd agmsg --agent-type claude-code left VERSION 9.9.9 (want 1.5.0)' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.KqUBl9qbyV: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 946, in test_agmsg_update_aborts_when_install_corrupts_live_state
    self.assertIn(
    ~~~~~~~~~~~~~^
        "install.sh --update --cmd agmsg --agent-type claude-code changed or removed existing live state", output
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'install.sh --update --cmd agmsg --agent-type claude-code changed or removed existing live state' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.VZZTaU8hst: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-v5o_u1lw/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: 1.0.0); see the reason above.\n'

----------------------------------------------------------------------
Ran 55 tests in 36.344s

FAILED (failures=6, errors=2)
exit=1

$ ANTHROPIC_OAUTH_TOKEN=fixture-not-a-token PI_CODING_AGENT_DIR="${TMPDIR%/}/elsewhere" uv run python -m unittest tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses -v
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok

----------------------------------------------------------------------
Ran 1 test in 2.547s

OK
exit=0

$ bash /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles--claude-worktrees-worker-c/e89c4c61-7403-4e9b-b587-9b8ae7c34d13/scratchpad/probe-auth-route.sh ~/Workspace/dotfiles/.claude/worktrees/worker-c/scripts/check-tools.sh
== (a)
required failed: ANTHROPIC_OAUTH_TOKEN is set; Anthropic goes through ANTHROPIC_API_KEY only (unset it)
not applicable: omp auth store (/tmp/claude-501/arc-probe.Txox4m/empty/.omp/agent/agent.db absent)
required_failures=1
exit=0 leaked=no
== (a2) empty value counts
required failed: ANTHROPIC_OAUTH_TOKEN is set; Anthropic goes through ANTHROPIC_API_KEY only (unset it)
not applicable: omp auth store (/tmp/claude-501/arc-probe.Txox4m/empty/.omp/agent/agent.db absent)
required_failures=1
exit=0 leaked=no
== (b)
found:   ANTHROPIC_OAUTH_TOKEN -> unset
not applicable: omp auth store (/tmp/claude-501/arc-probe.Txox4m/empty/.omp/agent/agent.db absent)
required_failures=0
exit=0 leaked=no
== (e)
found:   ANTHROPIC_OAUTH_TOKEN -> unset
required failed: omp auth store at /tmp/claude-501/arc-probe.Txox4m/e/.omp/agent/agent.db could not be verified (sqlite3 missing or its schema changed); remove the Anthropic login in omp or make the store readable
required_failures=1
exit=0 leaked=no
== (c)
found:   ANTHROPIC_OAUTH_TOKEN -> unset
required failed: omp auth store holds 1 Anthropic OAuth credential(s) at /tmp/claude-501/arc-probe.Txox4m/c/.omp/agent/agent.db; remove the Anthropic login in omp and use ANTHROPIC_API_KEY
required_failures=1
exit=0 leaked=no
== (d)
found:   ANTHROPIC_OAUTH_TOKEN -> unset
found:   omp auth store -> /tmp/claude-501/arc-probe.Txox4m/d/agent.db (no Anthropic OAuth credential)
required_failures=0
exit=0 leaked=no
== no sqlite3 on PATH
found:   ANTHROPIC_OAUTH_TOKEN -> unset
required failed: omp auth store at /tmp/claude-501/arc-probe.Txox4m/c/.omp/agent/agent.db could not be verified (sqlite3 missing or its schema changed); remove the Anthropic login in omp or make the store readable
required_failures=1
exit=0 leaked=no
== foreign schema
found:   ANTHROPIC_OAUTH_TOKEN -> unset
required failed: omp auth store at /tmp/claude-501/arc-probe.Txox4m/f/.omp/agent/agent.db could not be verified (sqlite3 missing or its schema changed); remove the Anthropic login in omp or make the store readable
required_failures=1
exit=0 leaked=no
exit=0

$ git diff --numstat origin/main...HEAD
100	0	.orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/task.md
34	0	scripts/check-tools.sh
38	0	tests/install/common/check_tools.bats
1	1	tests/unit/test_runtime_health.py
exit=0

$ git rev-parse HEAD origin/main
8cb93567fb3bb383964f5190433545e3cc8348bd
a8a747af06b32ff1d0d1720467892f34d9465ae4
exit=0

```

## The same module on `origin/main` (baseline for the 8 sandbox failures)

```text
$ base="$(mktemp -d "${TMPDIR%/}/rh-base.XXXXXX")/wt"; git worktree add --detach "$base" origin/main; (cd "$base" && uv run python -m unittest tests/unit/test_runtime_health.py -v); git worktree remove "$base"
base=a8a747af06b32ff1d0d1720467892f34d9465ae4
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
ERROR: test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state)
ERROR: test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state)
FAIL: test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes)
FAIL: test_agmsg_checksum_mismatch_fails_closed (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed)
FAIL: test_agmsg_fresh_install_populates_skill_and_records_manifest (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest)
FAIL: test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty)
FAIL: test_agmsg_reports_an_installer_that_leaves_the_wrong_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version)
FAIL: test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state)
Ran 55 tests in 24.428s
FAILED (failures=6, errors=2)
exit=1
removed=0

$ cmp <head FAIL/ERROR lines, sorted> <base FAIL/ERROR lines, sorted>
identical failing sets (       8 tests)
```

## The runner and the probe

```bash
#!/usr/bin/env bash
# Run the task's Check commands from the worktree root and print each verbatim with its exit status.
set -u
probe="$1"
run() {
    printf '$ %s\n' "$*"
    "$@" 2>&1
    printf 'exit=%s\n\n' "$?"
}
run make render-check
run shellcheck -x scripts/check-tools.sh
run shfmt --indent 4 --space-redirects --diff scripts/check-tools.sh
run uvx ruff format --config ruff.toml --check tests/unit/test_runtime_health.py
run uv run python -m unittest tests/unit/test_runtime_health.py -v
printf '$ ANTHROPIC_OAUTH_TOKEN=fixture-not-a-token PI_CODING_AGENT_DIR="${TMPDIR%%/}/elsewhere" uv run python -m unittest tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses -v\n'
ANTHROPIC_OAUTH_TOKEN=fixture-not-a-token PI_CODING_AGENT_DIR="${TMPDIR%/}/elsewhere" uv run python -m unittest tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses -v 2>&1
printf 'exit=%s\n\n' "$?"
run bash "$probe" "$PWD/scripts/check-tools.sh"
run git diff --numstat origin/main...HEAD
run git rev-parse HEAD origin/main
```

```bash
#!/usr/bin/env bash
# Local plain-bash probe of check_anthropic_auth_route (bats is CI-only); fixtures only, no host store.
set -u
S="$1"
T="$(mktemp -d "${TMPDIR%/}/arc-probe.XXXXXX")"
schema="CREATE TABLE IF NOT EXISTS auth_credentials (id INTEGER PRIMARY KEY AUTOINCREMENT, provider TEXT NOT NULL, credential_type TEXT NOT NULL, data TEXT NOT NULL, disabled_cause TEXT DEFAULT NULL, identity_key TEXT DEFAULT NULL, created_at INTEGER NOT NULL DEFAULT (CAST(strftime('%s','now') AS INTEGER)), updated_at INTEGER NOT NULL DEFAULT (CAST(strftime('%s','now') AS INTEGER)))"
probe() {
    local want="$1" out rc
    shift
    out="$(env -u ANTHROPIC_OAUTH_TOKEN -u PI_CODING_AGENT_DIR "$@" bash -c 'source "$1"; check_anthropic_auth_route; echo "required_failures=$required_failures"; [ "$required_failures" -eq "$2" ]' bash "$S" "$want" 2>&1)"
    rc=$?
    printf '%s\nexit=%s leaked=%s\n' "$out" "$rc" "$([[ $out == *never-printed* ]] && echo yes || echo no)"
}
mkdir -p "$T/e/.omp/agent" "$T/c/.omp/agent" "$T/d" "$T/f/.omp/agent"
echo "== (a)"; probe 1 ANTHROPIC_OAUTH_TOKEN=never-printed HOME="$T/empty"
echo "== (a2) empty value counts"; probe 1 ANTHROPIC_OAUTH_TOKEN= HOME="$T/empty"
echo "== (b)"; probe 0 HOME="$T/empty"
echo "== (e)"; : > "$T/e/.omp/agent/agent.db"; probe 1 HOME="$T/e"
echo "== (c)"; sqlite3 "$T/c/.omp/agent/agent.db" "$schema; INSERT INTO auth_credentials (provider, credential_type, data) VALUES ('anthropic', 'oauth', 'never-printed')"; probe 1 HOME="$T/c"
echo "== (d)"; sqlite3 "$T/d/agent.db" "$schema; INSERT INTO auth_credentials (provider, credential_type, data) VALUES ('openai-codex', 'oauth', 'never-printed'), ('anthropic', 'api_key', 'never-printed')"; probe 0 PI_CODING_AGENT_DIR="$T/d" HOME="$T/empty"
echo "== no sqlite3 on PATH"; probe 1 HOME="$T/c" PATH=/bin
echo "== foreign schema"; sqlite3 "$T/f/.omp/agent/agent.db" "CREATE TABLE auth_credentials (x TEXT)"; probe 1 HOME="$T/f"
```

## Records, masker, asset validator and prettier

Run after the four records were written, from the worktree root. The asset validator printed 1518 lines; the block shows the exact filters over its saved output: the lines that are not `WARN: regime-boundary` counter warnings, their count, and the warnings naming this task: twelve untracked-file warnings, eight for the orchestrator's own files in the main checkout and four for these records before their commit, none a failure.

```text
$ uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <report.md> <validation.md> <sandbox.md> <learning.md>
masked 0 match(es) in .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/report.md
masked 13 match(es) in .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/validation.md
masked 0 match(es) in .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/sandbox.md
masked 0 match(es) in .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/learning.md
exit=0

$ make validate-agent-assets > vaa.txt 2>&1
exit=0
$ wc -l < vaa.txt
1518
$ grep -vc '^WARN: regime-boundary' vaa.txt
2
$ grep -v '^WARN: regime-boundary' vaa.txt
uv run --offline --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
$ grep -c anthropic-auth-runtime-check vaa.txt
12
$ grep anthropic-auth-runtime-check vaa.txt
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T129-anthropic-auth-runtime-check-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T129-anthropic-auth-runtime-check-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-claude-r1.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-claude-r2.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-codex-r1.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-codex-r1.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-codex-r2.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-codex-r2.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/learning.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/report.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/sandbox.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/validation.md

$ mise x node npm:prettier -- prettier --check .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/report.md .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/validation.md .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/sandbox.md .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/learning.md .orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/task.md
Checking formatting...
All matched files use Prettier code style!
exit=0
```
