# T90b validation

No live role provisioning or ruleset mutation/merge; README responses are operator expectations, not claimed observations.

## /tmp/t90b-red.log

```text
FFFFFFFFFFF
======================================================================
FAIL: test_role_gate_update_activation_and_boundary_authorship (tests.unit.test_require_crit_review.ReviewGuardTest.test_role_gate_update_activation_and_boundary_authorship) (author='worker', approved=False, rule_type='update', path='.orchestration/reports/boundary.md')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 506, in test_role_gate_update_activation_and_boundary_authorship
    self.assertEqual(0 if expected else 1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : notice: GitHub role gate inactive: main has no enforced required approval; apply README ruleset
PR feedback evidence accepted: .orchestration/validation/test-pr-feedback.json
Review not required: no meaningful review trigger found.


======================================================================
FAIL: test_role_gate_update_activation_and_boundary_authorship (tests.unit.test_require_crit_review.ReviewGuardTest.test_role_gate_update_activation_and_boundary_authorship) (author='worker', approved=False, rule_type='update', path='docs/change.md')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 506, in test_role_gate_update_activation_and_boundary_authorship
    self.assertEqual(0 if expected else 1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : notice: GitHub role gate inactive: main has no enforced required approval; apply README ruleset
PR feedback evidence accepted: .orchestration/validation/test-pr-feedback.json
Review not required: no meaningful review trigger found.


======================================================================
FAIL: test_role_gate_update_activation_and_boundary_authorship (tests.unit.test_require_crit_review.ReviewGuardTest.test_role_gate_update_activation_and_boundary_authorship) (author='MERGER', approved=False, rule_type='update', path='docs/change.md')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 506, in test_role_gate_update_activation_and_boundary_authorship
    self.assertEqual(0 if expected else 1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : notice: GitHub role gate inactive: main has no enforced required approval; apply README ruleset
PR feedback evidence accepted: .orchestration/validation/test-pr-feedback.json
Review not required: no meaningful review trigger found.


======================================================================
FAIL: test_role_gate_update_activation_and_boundary_authorship (tests.unit.test_require_crit_review.ReviewGuardTest.test_role_gate_update_activation_and_boundary_authorship) (author='MERGER', approved=False, rule_type='pull_request', path='.orchestration/reports/boundary.md')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 506, in test_role_gate_update_activation_and_boundary_authorship
    self.assertEqual(0 if expected else 1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : PR feedback evidence is incomplete; run scripts/pr-feedback.py and disposition every item.
- GitHub role gate: PR author cannot approve/integrate their own PR; use the orchestrator login


======================================================================
FAIL: test_role_gate_requires_exact_sole_pr_bypass_actor (tests.unit.test_require_crit_review.ReviewGuardTest.test_role_gate_requires_exact_sole_pr_bypass_actor) (author='worker', actors=[])
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 519, in test_role_gate_requires_exact_sole_pr_bypass_actor
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : PR feedback evidence accepted: .orchestration/validation/test-pr-feedback.json
Review not required: no meaningful review trigger found.


======================================================================
FAIL: test_role_gate_requires_exact_sole_pr_bypass_actor (tests.unit.test_require_crit_review.ReviewGuardTest.test_role_gate_requires_exact_sole_pr_bypass_actor) (author='worker', actors=[{'actor_type': 'User', 'actor_id': 100, 'bypass_mode': 'pull_request'}, {'actor_type': 'User', 'actor_id': 200, 'bypass_mode': 'pull_request'}])
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 519, in test_role_gate_requires_exact_sole_pr_bypass_actor
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : PR feedback evidence accepted: .orchestration/validation/test-pr-feedback.json
Review not required: no meaningful review trigger found.


======================================================================
FAIL: test_role_gate_requires_exact_sole_pr_bypass_actor (tests.unit.test_require_crit_review.ReviewGuardTest.test_role_gate_requires_exact_sole_pr_bypass_actor) (author='worker', actors=[{'actor_type': 'User', 'actor_id': 200, 'bypass_mode': 'pull_request'}])
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 519, in test_role_gate_requires_exact_sole_pr_bypass_actor
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : PR feedback evidence accepted: .orchestration/validation/test-pr-feedback.json
Review not required: no meaningful review trigger found.


======================================================================
FAIL: test_role_gate_requires_exact_sole_pr_bypass_actor (tests.unit.test_require_crit_review.ReviewGuardTest.test_role_gate_requires_exact_sole_pr_bypass_actor) (author='worker', actors=[{'actor_type': 'Team', 'actor_id': 100, 'bypass_mode': 'pull_request'}])
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 519, in test_role_gate_requires_exact_sole_pr_bypass_actor
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : PR feedback evidence accepted: .orchestration/validation/test-pr-feedback.json
Review not required: no meaningful review trigger found.


======================================================================
FAIL: test_role_gate_requires_exact_sole_pr_bypass_actor (tests.unit.test_require_crit_review.ReviewGuardTest.test_role_gate_requires_exact_sole_pr_bypass_actor) (author='worker', actors=[{'actor_type': 'User', 'actor_id': 100, 'bypass_mode': 'always'}])
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 519, in test_role_gate_requires_exact_sole_pr_bypass_actor
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : PR feedback evidence accepted: .orchestration/validation/test-pr-feedback.json
Review not required: no meaningful review trigger found.


======================================================================
FAIL: test_role_gate_requires_exact_sole_pr_bypass_actor (tests.unit.test_require_crit_review.ReviewGuardTest.test_role_gate_requires_exact_sole_pr_bypass_actor) (author='worker', actors=[{'actor_type': 'User', 'actor_id': '100', 'bypass_mode': 'pull_request'}])
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 519, in test_role_gate_requires_exact_sole_pr_bypass_actor
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : PR feedback evidence accepted: .orchestration/validation/test-pr-feedback.json
Review not required: no meaningful review trigger found.


======================================================================
FAIL: test_role_gate_requires_exact_sole_pr_bypass_actor (tests.unit.test_require_crit_review.ReviewGuardTest.test_role_gate_requires_exact_sole_pr_bypass_actor) (author='worker', actors=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_require_crit_review.py", line 519, in test_role_gate_requires_exact_sole_pr_bypass_actor
    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : PR feedback evidence accepted: .orchestration/validation/test-pr-feedback.json
Review not required: no meaningful review trigger found.


----------------------------------------------------------------------
Ran 2 tests in 2.982s

FAILED (failures=11)

```

## /tmp/t90b-focused.log

```text
..........................................................................
----------------------------------------------------------------------
Ran 74 tests in 15.912s

OK

```

## /tmp/t90b-focused-final.log

```text
............................................................................
----------------------------------------------------------------------
Ran 76 tests in 17.508s

OK

```

## /tmp/t90b-unit.log

```text
uv run python -m unittest discover -s tests/unit -v
test_bounded_scan_finishes_under_wall_limit (test_agent_session_staleness.AgentSessionStalenessTest.test_bounded_scan_finishes_under_wall_limit) ... ok
test_check_is_silent_when_assets_predate_session (test_agent_session_staleness.AgentSessionStalenessTest.test_check_is_silent_when_assets_predate_session) ... ok
test_check_reports_new_versions_and_mtimes_deduplicated_by_root (test_agent_session_staleness.AgentSessionStalenessTest.test_check_reports_new_versions_and_mtimes_deduplicated_by_root) ... ok
test_doctor_delegates_session_staleness_to_installed_script (test_agent_session_staleness.AgentSessionStalenessTest.test_doctor_delegates_session_staleness_to_installed_script) ... ok
test_hook_first_call_writes_private_baseline_and_is_silent (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_first_call_writes_private_baseline_and_is_silent) ... ok
test_hook_missing_or_garbage_stdin_is_silent_success (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_missing_or_garbage_stdin_is_silent_success) ... ok
test_hook_prunes_state_files_older_than_seven_days (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_prunes_state_files_older_than_seven_days) ... ok
test_hook_second_call_detects_asset_updated_after_baseline (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_second_call_detects_asset_updated_after_baseline) ... ok
test_internal_failure_is_silent_success_with_one_stderr_line (test_agent_session_staleness.AgentSessionStalenessTest.test_internal_failure_is_silent_success_with_one_stderr_line) ... ok
test_no_arguments_prints_ten_recent_updates (test_agent_session_staleness.AgentSessionStalenessTest.test_no_arguments_prints_ten_recent_updates) ... ok
test_runtime_state_and_sqlite_files_are_excluded (test_agent_session_staleness.AgentSessionStalenessTest.test_runtime_state_and_sqlite_files_are_excluded) ... ok
test_ceiling_directories_do_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_ceiling_directories_do_not_hide_the_seat) ... ok
test_character_device_placeholder_is_skipped (test_agent_stop_gate.AgentStopGateTest.test_character_device_placeholder_is_skipped) ... ok
test_checkout_outside_any_seat_passes (test_agent_stop_gate.AgentStopGateTest.test_checkout_outside_any_seat_passes) ... ok
test_clean_orchestrator_passes (test_agent_stop_gate.AgentStopGateTest.test_clean_orchestrator_passes) ... ok
test_every_team_of_the_identity_is_checked (test_agent_stop_gate.AgentStopGateTest.test_every_team_of_the_identity_is_checked) ... ok
test_failing_git_status_blocks (test_agent_stop_gate.AgentStopGateTest.test_failing_git_status_blocks) ... ok
test_failing_identity_lookup_blocks_once (test_agent_stop_gate.AgentStopGateTest.test_failing_identity_lookup_blocks_once) ... ok
test_inherited_alternate_index_does_not_hide_a_staged_change (test_agent_stop_gate.AgentStopGateTest.test_inherited_alternate_index_does_not_hide_a_staged_change) ... ok
test_inherited_git_dir_does_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_inherited_git_dir_does_not_hide_the_seat) ... ok
test_injected_git_config_does_not_hide_untracked_files (test_agent_stop_gate.AgentStopGateTest.test_injected_git_config_does_not_hide_untracked_files) ... ok
test_json_escaped_cwd_resolves (test_agent_stop_gate.AgentStopGateTest.test_json_escaped_cwd_resolves) ... ok
test_missing_agmsg_install_passes (test_agent_stop_gate.AgentStopGateTest.test_missing_agmsg_install_passes) ... ok
test_mountinfo_cannot_be_redirected_through_the_environment (test_agent_stop_gate.AgentStopGateTest.test_mountinfo_cannot_be_redirected_through_the_environment) ... ok
test_null_device_of_another_filesystem_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_null_device_of_another_filesystem_is_not_a_placeholder) ... ok
test_orchestrator_acceptance_to_another_member_keeps_the_result_open (test_agent_stop_gate.AgentStopGateTest.test_orchestrator_acceptance_to_another_member_keeps_the_result_open) ... ok
test_project_dir_anchors_the_seat_after_a_cd (test_agent_stop_gate.AgentStopGateTest.test_project_dir_anchors_the_seat_after_a_cd) ... ok
test_read_only_bind_of_another_empty_file_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_read_only_bind_of_another_empty_file_is_not_a_placeholder) ... ok
test_read_write_mount_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_read_write_mount_is_not_a_placeholder) ... ok
test_result_then_acceptance_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_acceptance_passes) ... ok
test_result_then_revision_task_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_revision_task_passes) ... ok
test_result_without_acceptance_blocks (test_agent_stop_gate.AgentStopGateTest.test_result_without_acceptance_blocks) ... ok
test_same_named_file_bound_from_elsewhere_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_same_named_file_bound_from_elsewhere_is_not_a_placeholder) ... ok
test_sandbox_placeholders_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_are_skipped) ... ok
test_sandbox_placeholders_on_a_separate_filesystem_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_on_a_separate_filesystem_are_skipped) ... ok
test_separate_git_dir_main_worktree_is_a_seat (test_agent_stop_gate.AgentStopGateTest.test_separate_git_dir_main_worktree_is_a_seat) ... ok
test_slow_store_blocks_within_the_budget (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget) ... ok
test_slow_store_blocks_within_the_budget_with_gtimeout_only (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget_with_gtimeout_only) ... ok
test_slow_store_blocks_within_the_budget_without_timeout (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget_without_timeout) ... ok
test_solo_unsuffixed_worker_is_gated (test_agent_stop_gate.AgentStopGateTest.test_solo_unsuffixed_worker_is_gated) ... ok
test_sqlite_store_off_the_current_schema_is_not_initialized (test_agent_stop_gate.AgentStopGateTest.test_sqlite_store_off_the_current_schema_is_not_initialized) ... ok
test_staged_rename_out_of_orchestration_blocks (test_agent_stop_gate.AgentStopGateTest.test_staged_rename_out_of_orchestration_blocks) ... ok
test_stop_hook_active_skips_only_the_dirty_tree_check (test_agent_stop_gate.AgentStopGateTest.test_stop_hook_active_skips_only_the_dirty_tree_check) ... ok
test_unreadable_store_blocks_once (test_agent_stop_gate.AgentStopGateTest.test_unreadable_store_blocks_once) ... ok
test_untracked_file_outside_orchestration_blocks (test_agent_stop_gate.AgentStopGateTest.test_untracked_file_outside_orchestration_blocks) ... ok
test_untracked_symlink_to_a_mount_point_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_untracked_symlink_to_a_mount_point_is_not_a_placeholder) ... ok
test_untrusted_filenames_are_quoted (test_agent_stop_gate.AgentStopGateTest.test_untrusted_filenames_are_quoted) ... ok
test_user_bind_mount_of_a_real_file_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_user_bind_mount_of_a_real_file_is_not_a_placeholder) ... ok
test_whole_filesystem_bind_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_whole_filesystem_bind_is_not_a_placeholder) ... ok
test_worker_after_result_passes (test_agent_stop_gate.AgentStopGateTest.test_worker_after_result_passes) ... ok
test_worker_alive_pong_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_alive_pong_keeps_the_task_open) ... ok
test_worker_blocked_pong_closes_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_blocked_pong_closes_the_task) ... ok
test_worker_result_to_another_member_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_result_to_another_member_keeps_the_task_open) ... ok
test_worker_revise_acceptance_reopens_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_revise_acceptance_reopens_the_task) ... ok
test_worker_task_closed_by_a_non_revise_acceptance (test_agent_stop_gate.AgentStopGateTest.test_worker_task_closed_by_a_non_revise_acceptance) ... ok
test_worker_task_newer_than_result_blocks (test_agent_stop_gate.AgentStopGateTest.test_worker_task_newer_than_result_blocks) ... ok
test_worker_tracks_each_task_id (test_agent_stop_gate.AgentStopGateTest.test_worker_tracks_each_task_id) ... ok
test_default_store_uses_shared_helper (test_agmsg_dispatch.AgmsgDispatchTest.test_default_store_uses_shared_helper) ... ok
test_idle_wakes_once_and_reads (test_agmsg_dispatch.AgmsgDispatchTest.test_idle_wakes_once_and_reads) ... ok
test_invalid_timeout_does_not_send (test_agmsg_dispatch.AgmsgDispatchTest.test_invalid_timeout_does_not_send) ... ok
test_missing_pane_inserts_nothing (test_agmsg_dispatch.AgmsgDispatchTest.test_missing_pane_inserts_nothing) ... ok
test_rejects_identifiers_outside_the_strict_grammar (test_agmsg_dispatch.AgmsgDispatchTest.test_rejects_identifiers_outside_the_strict_grammar) ... ok
test_retry_does_not_wake_newly_working_pane (test_agmsg_dispatch.AgmsgDispatchTest.test_retry_does_not_wake_newly_working_pane) ... ok
test_timeout_is_one_shared_budget (test_agmsg_dispatch.AgmsgDispatchTest.test_timeout_is_one_shared_budget) ... ok
test_unread_retries_once_then_fails (test_agmsg_dispatch.AgmsgDispatchTest.test_unread_retries_once_then_fails) ... /home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3df4efc40>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3df4efb50>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def58d60>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def58f40>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def59030>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def59120>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def59210>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def59300>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def593f0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def594e0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def595d0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def596c0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def597b0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def598a0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def59990>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_wake_failure_identifies_sent_message (test_agmsg_dispatch.AgmsgDispatchTest.test_wake_failure_identifies_sent_message) ... ok
test_worker_becoming_idle_after_send_is_woken (test_agmsg_dispatch.AgmsgDispatchTest.test_worker_becoming_idle_after_send_is_woken) ... ok
test_working_does_not_wake (test_agmsg_dispatch.AgmsgDispatchTest.test_working_does_not_wake) ... ok
test_working_unread_never_wakes (test_agmsg_dispatch.AgmsgDispatchTest.test_working_unread_never_wakes) ... ok
test_docs_no_longer_name_codex_review_commit (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_docs_no_longer_name_codex_review_commit) ... ok
test_rule_and_skill_share_the_audit_gate_and_bot_wait_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_audit_gate_and_bot_wait_invariants) ... ok
test_rule_and_skill_share_the_parallel_execution_and_routing_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_parallel_execution_and_routing_invariants) ... ok
test_rule_and_skill_share_the_registration_and_delivery_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_registration_and_delivery_invariants) ... ok
test_rule_drops_the_worker_network_escalation (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_drops_the_worker_network_escalation) ... ok
test_skill_drops_the_pane_status_gate_and_raw_pane_wakes (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_skill_drops_the_pane_status_gate_and_raw_pane_wakes) ... ok
test_doctor_fails_when_bwrap_is_missing_with_codex (test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_bwrap_is_missing_with_codex) ... ok
test_doctor_fails_when_the_bwrap_probe_fails (test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_the_bwrap_probe_fails) ... ok
test_doctor_is_not_applicable_without_the_restriction (test_apparmor_userns.AppArmorUsernsTest.test_doctor_is_not_applicable_without_the_restriction) ... ok
test_doctor_passes_when_the_bwrap_probe_succeeds (test_apparmor_userns.AppArmorUsernsTest.test_doctor_passes_when_the_bwrap_probe_succeeds) ... ok
test_doctor_warns_optionally_when_codex_is_missing (test_apparmor_userns.AppArmorUsernsTest.test_doctor_warns_optionally_when_codex_is_missing) ... ok
test_installer_copies_and_reloads_the_profile_with_sudo (test_apparmor_userns.AppArmorUsernsTest.test_installer_copies_and_reloads_the_profile_with_sudo) ... ok
test_installer_fails_when_loading_the_profile_fails (test_apparmor_userns.AppArmorUsernsTest.test_installer_fails_when_loading_the_profile_fails) ... ok
test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) ... ok
test_installer_leaves_the_profile_pending_without_cached_sudo (test_apparmor_userns.AppArmorUsernsTest.test_installer_leaves_the_profile_pending_without_cached_sudo) ... ok
test_wrapper_re_renders_when_prerequisites_change (test_apparmor_userns.AppArmorUsernsTest.test_wrapper_re_renders_when_prerequisites_change) ... ok
test_chezmoi_rendered_updater_uses_exported_source_root (test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_exported_source_root) ... ok
test_chezmoi_rendered_updater_uses_inlined_manifest_library (test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_inlined_manifest_library) ... ok
test_chezmoi_wrapper_renders_shebang_and_source_root (test_asset_manifest.AssetManifestTest.test_chezmoi_wrapper_renders_shebang_and_source_root) ... ok
test_failed_atomic_commit_leaves_previous_manifest_intact (test_asset_manifest.AssetManifestTest.test_failed_atomic_commit_leaves_previous_manifest_intact) ... ok
test_records_schema_two_steps_and_replaces_one_whole_entry (test_asset_manifest.AssetManifestTest.test_records_schema_two_steps_and_replaces_one_whole_entry) ... ok
test_rendered_updater_fails_when_no_source_root_is_valid (test_asset_manifest.AssetManifestTest.test_rendered_updater_fails_when_no_source_root_is_valid) ... ok
test_same_run_mise_repairs_preserve_both_identity_steps (test_asset_manifest.AssetManifestTest.test_same_run_mise_repairs_preserve_both_identity_steps) ... ok
test_two_real_install_steps_record_under_fake_home (test_asset_manifest.AssetManifestTest.test_two_real_install_steps_record_under_fake_home) ... ok
test_unwritable_destination_warns_once_without_failing (test_asset_manifest.AssetManifestTest.test_unwritable_destination_warns_once_without_failing) ... ok
test_updater_direct_source_resolves_repository_root (test_asset_manifest.AssetManifestTest.test_updater_direct_source_resolves_repository_root) ... ok
test_updater_has_one_recording_call_for_each_install_step (test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... ok
test_exit_zero_install_with_expected_fake_binary_passes_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_install_with_expected_fake_binary_passes_postcondition) ... ok
test_exit_zero_install_with_wrong_version_fails_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_install_with_wrong_version_fails_postcondition) ... ok
test_exit_zero_partial_install_without_binary_fails_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_partial_install_without_binary_fails_postcondition) ... ok
test_gpgv_failure_preserves_existing_aws_and_skips_unzip (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_gpgv_failure_preserves_existing_aws_and_skips_unzip) ... ok
test_key_metadata_failures_stop_before_dearmor_and_gpgv (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_key_metadata_failures_stop_before_dearmor_and_gpgv) ... ok
test_linux_urls_are_versioned_and_unknown_architecture_fails (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_linux_urls_are_versioned_and_unknown_architecture_fails) ... ok
test_platform_package_managers_and_wrapper_own_aws_cli (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_platform_package_managers_and_wrapper_own_aws_cli) ... ok
test_repository_key_has_expected_current_fingerprint (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_repository_key_has_expected_current_fingerprint) ... ok
test_verified_archive_runs_installer_with_user_local_update_arguments (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_verified_archive_runs_installer_with_user_local_update_arguments) ... ok
test_wrong_staged_version_preserves_existing_aws_and_skips_installer (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_wrong_staged_version_preserves_existing_aws_and_skips_installer) ... ok
test_agmsg_runtime_paths_are_ignored_on_both_sides (test_check_agent_runtime.CheckAgentRuntimeTest.test_agmsg_runtime_paths_are_ignored_on_both_sides) ... ok
test_agmsg_separate_store_prefix_is_ignored (test_check_agent_runtime.CheckAgentRuntimeTest.test_agmsg_separate_store_prefix_is_ignored) ... ok
test_asset_repair_invokes_only_the_detected_step (test_check_agent_runtime.CheckAgentRuntimeTest.test_asset_repair_invokes_only_the_detected_step) ... ok
test_check_includes_ua_core_warnings (test_check_agent_runtime.CheckAgentRuntimeTest.test_check_includes_ua_core_warnings) ... /home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3df4efb50>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3df4efc40>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3df8476a0>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3df46b880>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_check_uses_same_modified_for_codex_profiles (test_check_agent_runtime.CheckAgentRuntimeTest.test_check_uses_same_modified_for_codex_profiles) ... ok
test_chezmoi_drift_status_failure_is_warning (test_check_agent_runtime.CheckAgentRuntimeTest.test_chezmoi_drift_status_failure_is_warning) ... ok
test_chezmoi_drift_warnings_classify_status_and_mode_only (test_check_agent_runtime.CheckAgentRuntimeTest.test_chezmoi_drift_warnings_classify_status_and_mode_only) ... ok
test_compare_claude_skills_ignores_cowork_synced_subtree (test_check_agent_runtime.CheckAgentRuntimeTest.test_compare_claude_skills_ignores_cowork_synced_subtree) ... ok
test_content_drift_still_fails (test_check_agent_runtime.CheckAgentRuntimeTest.test_content_drift_still_fails) ... ok
test_crit_codex_skills_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_crit_codex_skills_are_not_orphans) ... ok
test_deleted_shared_skill_file_repair_converges (test_check_agent_runtime.CheckAgentRuntimeTest.test_deleted_shared_skill_file_repair_converges) ... ok
test_every_generated_chezmoi_repair_action_is_forced (test_check_agent_runtime.CheckAgentRuntimeTest.test_every_generated_chezmoi_repair_action_is_forced) ... ok
test_executable_prefix_is_compared_against_deployed_name (test_check_agent_runtime.CheckAgentRuntimeTest.test_executable_prefix_is_compared_against_deployed_name) ... ok
test_executable_prefix_requires_deployed_execute_bit (test_check_agent_runtime.CheckAgentRuntimeTest.test_executable_prefix_requires_deployed_execute_bit) ... ok
test_execute_repair_calls_each_mapped_command_once (test_check_agent_runtime.CheckAgentRuntimeTest.test_execute_repair_calls_each_mapped_command_once) ... ok
test_ignored_paths_suppress_receipt_linked_tree_entries (test_check_agent_runtime.CheckAgentRuntimeTest.test_ignored_paths_suppress_receipt_linked_tree_entries) ... ok
test_installed_manifest_integrity_reasons (test_check_agent_runtime.CheckAgentRuntimeTest.test_installed_manifest_integrity_reasons) ... ok
test_installer_owned_agmsg_skill_and_backups_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_installer_owned_agmsg_skill_and_backups_are_not_orphans) ... ok
test_invalid_manifest_is_one_error_and_skips_dependent_checks (test_check_agent_runtime.CheckAgentRuntimeTest.test_invalid_manifest_is_one_error_and_skips_dependent_checks) ... ok
test_json_modifier_accepts_cosmetic_reserialization (test_check_agent_runtime.CheckAgentRuntimeTest.test_json_modifier_accepts_cosmetic_reserialization) ... ok
test_json_modifier_rejects_real_value_drift (test_check_agent_runtime.CheckAgentRuntimeTest.test_json_modifier_rejects_real_value_drift) ... ok
test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode (test_check_agent_runtime.CheckAgentRuntimeTest.test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode) ... ok
test_manifest_drift_requires_recorded_step_with_missing_path (test_check_agent_runtime.CheckAgentRuntimeTest.test_manifest_drift_requires_recorded_step_with_missing_path) ... ok
test_missing_crit_asset_is_repairable (test_check_agent_runtime.CheckAgentRuntimeTest.test_missing_crit_asset_is_repairable) ... ok
test_missing_terminal_browser_receipt_is_harmless (test_check_agent_runtime.CheckAgentRuntimeTest.test_missing_terminal_browser_receipt_is_harmless) ... ok
test_only_exact_agmsg_root_legacy_database_names_are_ignored (test_check_agent_runtime.CheckAgentRuntimeTest.test_only_exact_agmsg_root_legacy_database_names_are_ignored) ... ok
test_orchestrator_seat_lock_is_quiet_for_a_composite_id_or_no_live_session (test_check_agent_runtime.CheckAgentRuntimeTest.test_orchestrator_seat_lock_is_quiet_for_a_composite_id_or_no_live_session) ... ok
test_orchestrator_seat_lock_warns_on_a_bare_session_id (test_check_agent_runtime.CheckAgentRuntimeTest.test_orchestrator_seat_lock_warns_on_a_bare_session_id) ... ok
test_orphan_detection_classifies_accounted_stale_and_orphan (test_check_agent_runtime.CheckAgentRuntimeTest.test_orphan_detection_classifies_accounted_stale_and_orphan) ... ok
test_parameterized_mise_step_uses_key_identity (test_check_agent_runtime.CheckAgentRuntimeTest.test_parameterized_mise_step_uses_key_identity) ... ok
test_private_prefix_is_compared_against_deployed_name (test_check_agent_runtime.CheckAgentRuntimeTest.test_private_prefix_is_compared_against_deployed_name) ... ok
test_repair_actions_map_only_detected_file_drift (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_actions_map_only_detected_file_drift) ... ok
test_repair_mode_converges_once_and_reports_each_action (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_converges_once_and_reports_each_action) ... ok
test_repair_mode_fails_after_one_non_convergent_round (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_fails_after_one_non_convergent_round) ... ok
test_repair_mode_never_acts_on_stale_or_orphan_warnings (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_never_acts_on_stale_or_orphan_warnings) ... ok
test_repair_unset_is_byte_identical_and_never_mutates (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_unset_is_byte_identical_and_never_mutates) ... ok
test_sourced_asset_repair_runs_no_main_or_sibling_step (test_check_agent_runtime.CheckAgentRuntimeTest.test_sourced_asset_repair_runs_no_main_or_sibling_step) ... ok
test_terminal_browser_receipt_links_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_terminal_browser_receipt_links_are_not_orphans) ... ok
test_ua_core_is_quiet_when_dist_is_fresh_or_no_clone_exists (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_is_quiet_when_dist_is_fresh_or_no_clone_exists) ... ok
test_ua_core_warns_when_dist_is_older_than_src (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_dist_is_older_than_src) ... ok
test_ua_core_warns_when_dist_is_older_than_the_root_lockfile (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_dist_is_older_than_the_root_lockfile) ... ok
test_ua_core_warns_when_the_codex_clone_has_no_built_dist (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_the_codex_clone_has_no_built_dist) ... ok
test_unexpected_non_runtime_file_still_fails (test_check_agent_runtime.CheckAgentRuntimeTest.test_unexpected_non_runtime_file_still_fails) ... ok
test_unmanaged_top_level_skill_dir_warns (test_check_agent_runtime.CheckAgentRuntimeTest.test_unmanaged_top_level_skill_dir_warns) ... ok
test_apply_removes_the_symlink_farm_and_keeps_installer_owned_paths (test_chezmoiremove_agmsg.ChezmoiRemoveAgmsgTest.test_apply_removes_the_symlink_farm_and_keeps_installer_owned_paths) ... ok
test_retired_targets_are_listed_and_have_no_source (test_chezmoiremove_agmsg.ChezmoiRemoveRetiredShellFilesTest.test_retired_targets_are_listed_and_have_no_source) ... ok
test_current_only_key_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_only_key_is_preserved) ... ok
test_current_session_start_order_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_session_start_order_is_preserved)
Order is preserved; a stale bare herdr-agents command still migrates. ... ok
test_desired_current_output_is_byte_identical (test_claude_settings_merge.ClaudeSettingsMergeTest.test_desired_current_output_is_byte_identical) ... ok
test_empty_stdin_outputs_managed (test_claude_settings_merge.ClaudeSettingsMergeTest.test_empty_stdin_outputs_managed) ... ok
test_enabled_plugins_are_preserved_from_current (test_claude_settings_merge.ClaudeSettingsMergeTest.test_enabled_plugins_are_preserved_from_current) ... ok
test_invalid_json_outputs_managed (test_claude_settings_merge.ClaudeSettingsMergeTest.test_invalid_json_outputs_managed) ... ok
test_managed_hook_object_key_order_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_hook_object_key_order_is_preserved) ... ok
test_managed_permgate_replaces_stale_current_ccgate_hook (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_permgate_replaces_stale_current_ccgate_hook) ... ok
test_managed_session_start_replacement_keeps_hook_order (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replacement_keeps_hook_order)
Replacing a managed entry must not reorder SessionStart. ... ok
test_managed_session_start_replaces_stale_hard_coded_home_hook (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replaces_stale_hard_coded_home_hook)
Upgrade path: a machine that received the old hard-coded managed hook. ... ok
test_managed_wins_for_managed_key (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_wins_for_managed_key) ... ok
test_merge_is_idempotent (test_claude_settings_merge.ClaudeSettingsMergeTest.test_merge_is_idempotent) ... ok
test_permission_merge_preserves_custom_hook_in_mixed_entry (test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_custom_hook_in_mixed_entry) ... ok
test_permission_merge_preserves_unrelated_current_hooks (test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_unrelated_current_hooks) ... ok
test_real_template_preserves_herdr_matcher_and_converges (test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_template_preserves_herdr_matcher_and_converges) ... ok
test_real_value_change_is_redumped (test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_value_change_is_redumped) ... ok
test_reordered_but_equal_current_is_byte_identical (test_claude_settings_merge.ClaudeSettingsMergeTest.test_reordered_but_equal_current_is_byte_identical) ... ok
test_runtime_enabled_plugins_survive_a_managed_file_without_the_key (test_claude_settings_merge.ClaudeSettingsMergeTest.test_runtime_enabled_plugins_survive_a_managed_file_without_the_key) ... ok
test_trailing_newline (test_claude_settings_merge.ClaudeSettingsMergeTest.test_trailing_newline) ... ok
test_current_only_runtime_tables_keep_current_group_order (test_codex_config_merge.CodexConfigMergeTest.test_current_only_runtime_tables_keep_current_group_order) ... ok
test_fresh_machine_outputs_managed_baseline (test_codex_config_merge.CodexConfigMergeTest.test_fresh_machine_outputs_managed_baseline) ... ok
test_managed_permgate_replaces_stale_private_ccgate_hook (test_codex_config_merge.CodexConfigMergeTest.test_managed_permgate_replaces_stale_private_ccgate_hook) ... ok
test_managed_templates_are_rendered_before_merge (test_codex_config_merge.CodexConfigMergeTest.test_managed_templates_are_rendered_before_merge) ... ok
test_managed_wins_for_managed_keys (test_codex_config_merge.CodexConfigMergeTest.test_managed_wins_for_managed_keys) ... ok
test_repeated_runtime_tables_are_preserved_in_order (test_codex_config_merge.CodexConfigMergeTest.test_repeated_runtime_tables_are_preserved_in_order) ... ok
test_retired_disabled_mcp_servers_are_purged_and_enabled_ones_kept (test_codex_config_merge.CodexConfigMergeTest.test_retired_disabled_mcp_servers_are_purged_and_enabled_ones_kept) ... ok
test_runtime_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_are_preserved) ... ok
test_runtime_tables_seed_from_managed_when_absent (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_seed_from_managed_when_absent) ... ok
test_unknown_current_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_unknown_current_tables_are_preserved) ... ok
test_working_tree_placeholder_falls_back_to_source_dir_parent (test_codex_config_merge.CodexConfigMergeTest.test_working_tree_placeholder_falls_back_to_source_dir_parent) ... ok
test_working_tree_placeholder_prefers_env_override (test_codex_config_merge.CodexConfigMergeTest.test_working_tree_placeholder_prefers_env_override) ... ok
test_rules_are_forbidden_only_and_cover_the_declared_prefixes (test_codex_execpolicy.CodexExecpolicyTest.test_rules_are_forbidden_only_and_cover_the_declared_prefixes) ... ok
test_missing_trusted_runtime_is_silent (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_missing_trusted_runtime_is_silent) ... ok
test_non_opted_project_is_silent_even_with_trusted_runtime (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_non_opted_project_is_silent_even_with_trusted_runtime) ... ok
test_project_cli_is_data_only_and_trusted_cli_gets_explicit_root (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_project_cli_is_data_only_and_trusted_cli_gets_explicit_root) ... ok
test_coverage_gems_are_compatible_and_exact (test_files_fixture.FilesFixtureTest.test_coverage_gems_are_compatible_and_exact) ... ok
test_fixture_uses_chezmoi_binary_outside_mise_shims (test_files_fixture.FilesFixtureTest.test_fixture_uses_chezmoi_binary_outside_mise_shims) ... ok
test_legacy_file_workflows_initialize_required_fixture_paths (test_files_fixture.FilesFixtureTest.test_legacy_file_workflows_initialize_required_fixture_paths) ... ok
test_a_missing_formatter_is_reported_without_a_traceback (test_format_edited_files_hook.FormatEditedFilesHookTest.test_a_missing_formatter_is_reported_without_a_traceback) ... ok
test_formatters_run_from_the_edited_files_repository_root (test_format_edited_files_hook.FormatEditedFilesHookTest.test_formatters_run_from_the_edited_files_repository_root) ... ok
test_a_declare_r_assignment_must_appear_exactly_once (test_generate_agent_configs.GenerateAgentConfigsTest.test_a_declare_r_assignment_must_appear_exactly_once) ... ok
test_a_list_render_writes_one_pin_into_several_files_and_declare_r (test_generate_agent_configs.GenerateAgentConfigsTest.test_a_list_render_writes_one_pin_into_several_files_and_declare_r) ... ok
test_absent_worker_profile_renders_no_env_line (test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_profile_renders_no_env_line) ... ok
test_absent_worker_worktree_renders_no_env_line (test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_worktree_renders_no_env_line) ... ok
test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map (test_generate_agent_configs.GenerateAgentConfigsTest.test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map) ... ok
test_asset_constant_must_be_assigned_exactly_once (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constant_must_be_assigned_exactly_once) ... ok
test_asset_constants_render_into_their_files (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constants_render_into_their_files) ... ok
test_asset_pin_must_be_a_plain_value (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_pin_must_be_a_plain_value) ... ok
test_audit_profile_renders_read_only_sandbox_override (test_generate_agent_configs.GenerateAgentConfigsTest.test_audit_profile_renders_read_only_sandbox_override) ... ok
test_bootstrap_pins_render_into_setup_and_their_installers (test_generate_agent_configs.GenerateAgentConfigsTest.test_bootstrap_pins_render_into_setup_and_their_installers) ... ok
test_check_reports_asset_render_drift (test_generate_agent_configs.GenerateAgentConfigsTest.test_check_reports_asset_render_drift) ... ok
test_claude_deny_rules_use_edit_for_file_mutations (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_deny_rules_use_edit_for_file_mutations) ... ok
test_claude_sandbox_renders_optional_socket_and_extra_write_keys (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_optional_socket_and_extra_write_keys) ... ok
test_claude_settings_render_interactive_advisor_only_when_set (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_interactive_advisor_only_when_set) ... ok
test_claude_settings_render_the_format_hook_from_its_path (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_the_format_hook_from_its_path) ... ok
test_claude_settings_renders_session_start_hooks (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_settings_use_interactive_profile_with_permgate (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_use_interactive_profile_with_permgate) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_codex_config_renders_permgate_permission_request (test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_permgate_permission_request) ... ok
test_codex_config_renders_working_tree_project_key (test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_working_tree_project_key) ... ok
test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot (test_generate_agent_configs.GenerateAgentConfigsTest.test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot) ... ok
test_expected_outputs_uses_codex_baseline_path (test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
test_managed_claude_sandbox_excludes_agmsg_dispatch (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_claude_sandbox_excludes_agmsg_dispatch) ... ok
test_managed_codex_path_includes_installed_common_bin (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_path_includes_installed_common_bin) ... ok
test_managed_hooks_use_installed_permgate_paths (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_hooks_use_installed_permgate_paths) ... ok
test_manifest_keeps_model_ids_only_in_profiles (test_generate_agent_configs.GenerateAgentConfigsTest.test_manifest_keeps_model_ids_only_in_profiles) ... ok
test_model_profiles_env_renders_claude_advisor_only_when_set (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_claude_advisor_only_when_set) ... ok
test_model_profiles_env_renders_worker_kind (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_kind) ... ok
test_model_profiles_env_renders_worker_profile (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_profile) ... ok
test_model_profiles_env_renders_worker_worktree (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_worktree) ... ok
test_model_profiles_reject_incomplete_or_unsafe_entries (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_invalid_sandbox_mode (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_invalid_sandbox_mode) ... ok
test_model_profiles_reject_unsafe_advisor (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_profile_modify_scripts_are_byte_idempotent_with_runtime_state (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_byte_idempotent_with_runtime_state) ... ok
test_profile_modify_scripts_are_quiet_for_matching_hook_trust (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_quiet_for_matching_hook_trust) ... ok
test_profile_modify_scripts_preserve_repeated_runtime_tables (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_repeated_runtime_tables) ... ok
test_profile_modify_scripts_preserve_runtime_state (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_runtime_state) ... ok
test_profile_modify_scripts_seed_base_hook_trust (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_seed_base_hook_trust) ... ok
test_profile_modify_scripts_warn_on_hook_trust_divergence (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_warn_on_hook_trust_divergence) ... ok
test_repository_marketplace_is_a_runtime_owned_seed (test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... ok
test_security_profile_renders_launcher_and_expanded_notify (test_generate_agent_configs.GenerateAgentConfigsTest.test_security_profile_renders_launcher_and_expanded_notify) ... ok
test_set_asset_field_rejects_unknown_targets_and_unsafe_values (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rejects_unknown_targets_and_unsafe_values) ... ok
test_set_asset_field_rewrites_only_the_named_scalar (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rewrites_only_the_named_scalar) ... ok
test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid) ... ok
test_set_asset_refuses_fields_other_than_pins_and_checksums (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_refuses_fields_other_than_pins_and_checksums) ... ok
test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string) ... ok
test_set_asset_reports_an_unparsable_manifest_without_a_traceback (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_reports_an_unparsable_manifest_without_a_traceback) ... ok
test_set_asset_updates_the_manifest_and_renders_its_pins (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_updates_the_manifest_and_renders_its_pins) ... ok
test_unknown_interactive_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_worker_kind_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config) ... ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ok
test_worker_kind_defaults_to_codex (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_kind_defaults_to_codex) ... ok
test_worker_worktree_outside_claude_worktrees_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_worktree_outside_claude_worktrees_fails) ... ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ok
test_a_real_directory_of_that_name_stays_visible (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_a_real_directory_of_that_name_stays_visible) ... ok
test_claude_settings_stay_visible (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_claude_settings_stay_visible) ... ok
test_empty_placeholder_files_on_disk_leave_status_clean (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_empty_placeholder_files_on_disk_leave_status_clean) ... ok
test_every_placeholder_is_ignored_at_the_root_only (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_every_placeholder_is_ignored_at_the_root_only) ... ok
test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits (test_herdr_agents.HerdrAgentsTest.test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits) ... ok
test_add_worker_derives_the_default_herdr_socket_for_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_derives_the_default_herdr_socket_for_spawn) ... ok
test_add_worker_emits_no_override_for_an_unparseable_codex_config (test_herdr_agents.HerdrAgentsTest.test_add_worker_emits_no_override_for_an_unparseable_codex_config) ... ok
test_add_worker_exits_zero_when_a_timed_out_spawn_still_links (test_herdr_agents.HerdrAgentsTest.test_add_worker_exits_zero_when_a_timed_out_spawn_still_links) ... ok
test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array (test_herdr_agents.HerdrAgentsTest.test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array) ... ok
test_add_worker_linkage_failure_prints_the_invocation_and_the_query (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_failure_prints_the_invocation_and_the_query) ... ok
test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver) ... ok
test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping) ... ok
test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace) ... ok
test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn) ... ok
test_add_worker_linkage_ignores_a_placement_record_from_another_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_from_another_workspace) ... ok
test_add_worker_linkage_ignores_a_pong_older_than_this_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_pong_older_than_this_ping) ... ok
test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal) ... ok
test_add_worker_linkage_refuses_a_placement_conflict (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_a_placement_conflict) ... ok
test_add_worker_linkage_refuses_several_orchestrator_identities (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_several_orchestrator_identities) ... ok
test_add_worker_linkage_resolves_an_id_keyed_placement_record (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_resolves_an_id_keyed_placement_record) ... ok
test_add_worker_linkage_survives_a_non_numeric_pong_wait (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_survives_a_non_numeric_pong_wait) ... ok
test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh) ... ok
test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options (test_herdr_agents.HerdrAgentsTest.test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options) ... ok
test_add_worker_refuses_an_undefined_profile_before_any_change (test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_an_undefined_profile_before_any_change) ... ok
test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found (test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found) ... ok
test_add_worker_rejects_a_worktree_outside_claude_worktrees (test_herdr_agents.HerdrAgentsTest.test_add_worker_rejects_a_worktree_outside_claude_worktrees) ... ok
test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog) ... ok
test_add_worker_reports_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_spawn) ... ok
test_add_worker_reports_linkage_ok_after_a_ready_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_ok_after_a_ready_spawn) ... ok
test_add_worker_reports_linkage_unreached_after_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_unreached_after_a_failed_spawn) ... ok
test_add_worker_reports_shallow_metadata_as_not_granted (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_shallow_metadata_as_not_granted) ... ok
test_add_worker_reuses_a_seat_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seat_tab_in_the_pair_workspace) ... ok
test_add_worker_reuses_a_seated_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seated_workspace) ... ok
test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace) ... ok
test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args (test_herdr_agents.HerdrAgentsTest.test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args) ... ok
test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog) ... ok
test_added_worker_github_environment_reaches_boot (test_herdr_agents.HerdrAgentsTest.test_added_worker_github_environment_reaches_boot) ... ok
test_agent_name_taken_gives_up_after_bounded_wait (test_herdr_agents.HerdrAgentsTest.test_agent_name_taken_gives_up_after_bounded_wait) ... ok
test_another_team_members_pane_is_not_a_second_worker (test_herdr_agents.HerdrAgentsTest.test_another_team_members_pane_is_not_a_second_worker) ... ok
test_attach_bootstraps_agmsg_after_codex_reuse (test_herdr_agents.HerdrAgentsTest.test_attach_bootstraps_agmsg_after_codex_reuse) ... ok
test_attach_bootstraps_agmsg_after_codex_start (test_herdr_agents.HerdrAgentsTest.test_attach_bootstraps_agmsg_after_codex_start) ... ok
test_attach_builds_codex_right_of_current_claude_pane (test_herdr_agents.HerdrAgentsTest.test_attach_builds_codex_right_of_current_claude_pane) ... ok
test_attach_complete_workspace_is_idempotent (test_herdr_agents.HerdrAgentsTest.test_attach_complete_workspace_is_idempotent) ... ok
test_attach_completes_bootstrap_on_a_self_named_pair (test_herdr_agents.HerdrAgentsTest.test_attach_completes_bootstrap_on_a_self_named_pair) ... ok
test_attach_correct_order_does_not_swap (test_herdr_agents.HerdrAgentsTest.test_attach_correct_order_does_not_swap) ... ok
test_attach_does_not_restart_codex_agent_from_another_tab (test_herdr_agents.HerdrAgentsTest.test_attach_does_not_restart_codex_agent_from_another_tab) ... ok
test_attach_equal_halves_does_not_resize (test_herdr_agents.HerdrAgentsTest.test_attach_equal_halves_does_not_resize) ... ok
test_attach_from_the_self_named_worker_pane_exits_quietly (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_self_named_worker_pane_exits_quietly) ... ok
test_attach_from_the_worker_pane_does_not_relabel_it (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_pane_does_not_relabel_it) ... ok
test_attach_from_the_worker_worktree_exits_quietly (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_worktree_exits_quietly) ... ok
test_attach_ignores_agmsg_bootstrap_failure (test_herdr_agents.HerdrAgentsTest.test_attach_ignores_agmsg_bootstrap_failure) ... ok
test_attach_ignores_extra_panes_on_other_tabs (test_herdr_agents.HerdrAgentsTest.test_attach_ignores_extra_panes_on_other_tabs) ... ok
test_attach_leaves_a_self_named_pair_alone (test_herdr_agents.HerdrAgentsTest.test_attach_leaves_a_self_named_pair_alone) ... ok
test_attach_legacy_files_pane_refuses_repair_without_layout_mutation (test_herdr_agents.HerdrAgentsTest.test_attach_legacy_files_pane_refuses_repair_without_layout_mutation) ... ok
test_attach_lowercases_and_validates_derived_agent_name (test_herdr_agents.HerdrAgentsTest.test_attach_lowercases_and_validates_derived_agent_name) ... ok
test_attach_noops_for_full_mode_managed_layout (test_herdr_agents.HerdrAgentsTest.test_attach_noops_for_full_mode_managed_layout) ... ok
test_attach_ratio_repair_skips_unsafe_layouts (test_herdr_agents.HerdrAgentsTest.test_attach_ratio_repair_skips_unsafe_layouts) ... ok
test_attach_rejects_invalid_derived_agent_name (test_herdr_agents.HerdrAgentsTest.test_attach_rejects_invalid_derived_agent_name) ... ok
test_attach_repair_splits_the_missing_worker_pane_in_its_worktree (test_herdr_agents.HerdrAgentsTest.test_attach_repair_splits_the_missing_worker_pane_in_its_worktree) ... ok
test_attach_repairs_codex_claude_order_with_one_swap (test_herdr_agents.HerdrAgentsTest.test_attach_repairs_codex_claude_order_with_one_swap) ... ok
test_attach_repairs_skewed_widths_to_equal_halves (test_herdr_agents.HerdrAgentsTest.test_attach_repairs_skewed_widths_to_equal_halves) ... ok
test_attach_reports_agmsg_skip_when_not_installed (test_herdr_agents.HerdrAgentsTest.test_attach_reports_agmsg_skip_when_not_installed) ... ok
test_attach_skips_delivery_when_turn_hook_exists (test_herdr_agents.HerdrAgentsTest.test_attach_skips_delivery_when_turn_hook_exists) ... ok
test_attach_warns_after_one_nonconverging_resize (test_herdr_agents.HerdrAgentsTest.test_attach_warns_after_one_nonconverging_resize) ... ok
test_attach_warns_when_multiple_agmsg_identities_exist (test_herdr_agents.HerdrAgentsTest.test_attach_warns_when_multiple_agmsg_identities_exist) ... ok
test_attach_without_herdr_environment_names_the_seated_worker (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_names_the_seated_worker) ... ok
test_attach_without_herdr_environment_prints_the_bring_up_summary (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_prints_the_bring_up_summary) ... ok
test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree) ... ok
test_audit_accepts_a_dir_with_an_apostrophe_quoted_intact (test_herdr_agents.HerdrAgentsTest.test_audit_accepts_a_dir_with_an_apostrophe_quoted_intact) ... ok
test_audit_creates_the_audit_tab_once_and_reuses_it (test_herdr_agents.HerdrAgentsTest.test_audit_creates_the_audit_tab_once_and_reuses_it) ... ok
test_audit_exits_2_without_a_managed_workspace (test_herdr_agents.HerdrAgentsTest.test_audit_exits_2_without_a_managed_workspace) ... ok
test_audit_fails_as_unmasked_when_masking_fails (test_herdr_agents.HerdrAgentsTest.test_audit_fails_as_unmasked_when_masking_fails) ... ok
test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info (test_herdr_agents.HerdrAgentsTest.test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info) ... ok
test_audit_finds_the_self_named_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_audit_finds_the_self_named_pair_workspace) ... ok
test_audit_gates_on_the_concluding_line_of_the_last_message (test_herdr_agents.HerdrAgentsTest.test_audit_gates_on_the_concluding_line_of_the_last_message) ... ok
test_audit_marker_detection_reads_unwrapped_snapshots (test_herdr_agents.HerdrAgentsTest.test_audit_marker_detection_reads_unwrapped_snapshots) ... ok
test_audit_masks_evidence_before_the_verdict_gate (test_herdr_agents.HerdrAgentsTest.test_audit_masks_evidence_before_the_verdict_gate) ... ok
test_audit_masks_evidence_even_when_the_audit_exit_is_nonzero (test_herdr_agents.HerdrAgentsTest.test_audit_masks_evidence_even_when_the_audit_exit_is_nonzero) ... ok
test_audit_nonzero_exit_marker_fails_the_helper (test_herdr_agents.HerdrAgentsTest.test_audit_nonzero_exit_marker_fails_the_helper) ... ok
test_audit_pane_command_tees_evidence_and_waits_for_a_fresh_marker (test_herdr_agents.HerdrAgentsTest.test_audit_pane_command_tees_evidence_and_waits_for_a_fresh_marker) ... ok
test_audit_quotes_a_non_ascii_out_path_under_the_c_locale (test_herdr_agents.HerdrAgentsTest.test_audit_quotes_a_non_ascii_out_path_under_the_c_locale) ... ok
test_audit_quotes_the_last_message_path_for_a_non_ascii_out (test_herdr_agents.HerdrAgentsTest.test_audit_quotes_the_last_message_path_for_a_non_ascii_out) ... ok
test_audit_refuses_a_busy_audit_pane (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_a_busy_audit_pane) ... ok
test_audit_refuses_a_tracked_masker_missing_from_the_tree (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_a_tracked_masker_missing_from_the_tree) ... ok
test_audit_refuses_an_uncommitted_or_untracked_masker (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_an_uncommitted_or_untracked_masker) ... ok
test_audit_refuses_the_masker_from_the_audited_commit (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_the_masker_from_the_audited_commit) ... ok
test_audit_rejects_unsafe_arguments_before_calling_herdr (test_herdr_agents.HerdrAgentsTest.test_audit_rejects_unsafe_arguments_before_calling_herdr) ... ok
test_audit_runs_codex_exec_with_the_prompt_and_last_message_file (test_herdr_agents.HerdrAgentsTest.test_audit_runs_codex_exec_with_the_prompt_and_last_message_file) ... ok
test_audit_runs_in_dir_even_when_the_reused_pane_moved (test_herdr_agents.HerdrAgentsTest.test_audit_runs_in_dir_even_when_the_reused_pane_moved) ... ok
test_audit_skips_masking_without_a_repo_validator (test_herdr_agents.HerdrAgentsTest.test_audit_skips_masking_without_a_repo_validator) ... ok
test_audit_tab_does_not_break_attach_order_and_ratio_repair (test_herdr_agents.HerdrAgentsTest.test_audit_tab_does_not_break_attach_order_and_ratio_repair) ... ok
test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard (test_herdr_agents.HerdrAgentsTest.test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard) ... ok
test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff (test_herdr_agents.HerdrAgentsTest.test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff) ... ok
test_audit_task_names_a_txt_artifact_when_no_md_one_exists (test_herdr_agents.HerdrAgentsTest.test_audit_task_names_a_txt_artifact_when_no_md_one_exists) ... ok
test_audit_task_names_only_the_task_file_when_no_artifact_exists (test_herdr_agents.HerdrAgentsTest.test_audit_task_names_only_the_task_file_when_no_artifact_exists) ... ok
test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work (test_herdr_agents.HerdrAgentsTest.test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work) ... ok
test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot (test_herdr_agents.HerdrAgentsTest.test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot) ... ok
test_audit_uses_manifest_audit_codex_args (test_herdr_agents.HerdrAgentsTest.test_audit_uses_manifest_audit_codex_args) ... ok
test_audit_verdict_gate_reads_only_the_final_codex_block (test_herdr_agents.HerdrAgentsTest.test_audit_verdict_gate_reads_only_the_final_codex_block) ... ok
test_audit_waits_for_the_prompt_on_a_new_audit_tab (test_herdr_agents.HerdrAgentsTest.test_audit_waits_for_the_prompt_on_a_new_audit_tab) ... ok
test_bootstrap_accepts_same_identity_in_multiple_teams (test_herdr_agents.HerdrAgentsTest.test_bootstrap_accepts_same_identity_in_multiple_teams) ... ok
test_bootstrap_leaves_a_foreign_pre_push_hook_alone (test_herdr_agents.HerdrAgentsTest.test_bootstrap_leaves_a_foreign_pre_push_hook_alone) ... ok
test_bootstrap_only_creates_missing_herdr_log_directory (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_creates_missing_herdr_log_directory) ... ok
test_bootstrap_only_does_not_call_herdr_or_agents (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_does_not_call_herdr_or_agents) ... ok
test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing) ... ok
test_bootstrap_only_sets_each_missing_delivery_once (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_sets_each_missing_delivery_once) ... ok
test_bootstrap_only_skips_all_delivery_when_both_hooks_exist (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_all_delivery_when_both_hooks_exist) ... ok
test_bootstrap_only_skips_home_without_agmsg_calls (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_home_without_agmsg_calls) ... ok
test_bootstrap_only_warns_for_missing_claude_identity_without_joining (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_missing_claude_identity_without_joining) ... ok
test_bootstrap_only_warns_for_multiple_claude_identities (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_multiple_claude_identities) ... ok
test_bootstrap_removes_its_retired_pre_push_stub (test_herdr_agents.HerdrAgentsTest.test_bootstrap_removes_its_retired_pre_push_stub) ... ok
test_bootstrap_with_claude_worker_accepts_two_claude_identities (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_accepts_two_claude_identities) ... ok
test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity) ... ok
test_bootstrap_with_claude_worker_leaves_codex_hooks_alone (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_leaves_codex_hooks_alone) ... ok
test_claude_agent_accepts_manifest_profile_arguments_for_e2e (test_herdr_agents.HerdrAgentsTest.test_claude_agent_accepts_manifest_profile_arguments_for_e2e) ... ok
test_claude_repair_skips_just_restarted_codex_pane_without_agent_field (test_herdr_agents.HerdrAgentsTest.test_claude_repair_skips_just_restarted_codex_pane_without_agent_field) ... ok
test_claude_settings_add_herdr_attach_session_hook (test_herdr_agents.HerdrAgentsTest.test_claude_settings_add_herdr_attach_session_hook) ... ok
test_claude_worker_sharing_the_orchestrator_identity_is_refused (test_herdr_agents.HerdrAgentsTest.test_claude_worker_sharing_the_orchestrator_identity_is_refused) ... ok
test_claude_worker_with_a_registered_worker_identity_proceeds (test_herdr_agents.HerdrAgentsTest.test_claude_worker_with_a_registered_worker_identity_proceeds) ... ok
test_codex_profile_defaults_to_generated_interactive_profile (test_herdr_agents.HerdrAgentsTest.test_codex_profile_defaults_to_generated_interactive_profile) ... ok
test_codex_worker_is_not_subject_to_the_identity_guard (test_herdr_agents.HerdrAgentsTest.test_codex_worker_is_not_subject_to_the_identity_guard) ... ok
test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again (test_herdr_agents.HerdrAgentsTest.test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again) ... ok
test_existing_two_pane_workspace_repairs_skewed_widths (test_herdr_agents.HerdrAgentsTest.test_existing_two_pane_workspace_repairs_skewed_widths) ... ok
test_existing_workspace_matches_canonical_macos_workdir (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_matches_canonical_macos_workdir) ... ok
test_existing_workspace_restarts_missing_claude_in_empty_pane (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_claude_in_empty_pane) ... ok
test_existing_workspace_restarts_missing_codex_agent (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_codex_agent) ... ok
test_existing_workspace_splits_when_missing_claude_has_no_empty_pane (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_splits_when_missing_claude_has_no_empty_pane) ... ok
test_existing_workspace_with_legacy_files_pane_focuses_without_mutation (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_with_legacy_files_pane_focuses_without_mutation) ... ok
test_explicit_worker_kind_and_profile_survive_seat_label_loading (test_herdr_agents.HerdrAgentsTest.test_explicit_worker_kind_and_profile_survive_seat_label_loading) ... ok
test_file_viewer_plugin_config_sets_micro_editor (test_herdr_agents.HerdrAgentsTest.test_file_viewer_plugin_config_sets_micro_editor) ... ok
test_full_and_restart_modes_refuse_duplicate_managed_workspaces (test_herdr_agents.HerdrAgentsTest.test_full_and_restart_modes_refuse_duplicate_managed_workspaces) ... ok
test_full_mode_does_not_duplicate_a_solo_codex_worker_seat (test_herdr_agents.HerdrAgentsTest.test_full_mode_does_not_duplicate_a_solo_codex_worker_seat) ... ok
test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots (test_herdr_agents.HerdrAgentsTest.test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots) ... ok
test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree) ... ok
test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane) ... ok
test_full_mode_heal_never_starts_the_worker_in_the_audit_pane (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_starts_the_worker_in_the_audit_pane) ... ok
test_full_mode_heals_nothing_in_a_healthy_self_named_pair (test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_nothing_in_a_healthy_self_named_pair) ... ok
test_full_mode_heals_the_orchestrator_beside_a_live_added_claude_worker (test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_the_orchestrator_beside_a_live_added_claude_worker) ... ok
test_full_mode_reuses_agentless_worker_pane_in_attach_labeled_workspace (test_herdr_agents.HerdrAgentsTest.test_full_mode_reuses_agentless_worker_pane_in_attach_labeled_workspace) ... ok
test_full_mode_skips_agmsg_bootstrap_for_home (test_herdr_agents.HerdrAgentsTest.test_full_mode_skips_agmsg_bootstrap_for_home) ... ok
test_full_mode_splits_the_worker_pane_in_its_worktree (test_herdr_agents.HerdrAgentsTest.test_full_mode_splits_the_worker_pane_in_its_worktree) ... ok
test_ghostty_config_does_not_auto_start_herdr_session (test_herdr_agents.HerdrAgentsTest.test_ghostty_config_does_not_auto_start_herdr_session) ... ok
test_herdr_prefix_alt_a_runs_helper_from_active_pane (test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_alt_a_runs_helper_from_active_pane) ... ok
test_herdr_prefix_f_opens_file_viewer_popup (test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_f_opens_file_viewer_popup) ... ok
test_make_update_and_upgrade_include_agmsg_bootstrap (test_herdr_agents.HerdrAgentsTest.test_make_update_and_upgrade_include_agmsg_bootstrap) ... ok
test_mixed_legacy_and_seat_labels_are_one_pair (test_herdr_agents.HerdrAgentsTest.test_mixed_legacy_and_seat_labels_are_one_pair) ... ok
test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout (test_herdr_agents.HerdrAgentsTest.test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout) ... ok
test_orchestrator_pane_appends_claude_args_after_profile_args (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_appends_claude_args_after_profile_args) ... ok
test_orchestrator_pane_start_claims_the_seat_with_the_composite_id (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_start_claims_the_seat_with_the_composite_id) ... ok
test_orchestrator_pane_start_without_a_session_claims_nothing (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_start_without_a_session_claims_nothing) ... ok
test_orchestrator_pane_uses_interactive_profile_args (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_uses_interactive_profile_args) ... ok
test_pane_creation_propagates_explicit_fpath (test_herdr_agents.HerdrAgentsTest.test_pane_creation_propagates_explicit_fpath) ... ok
test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat) ... ok
test_regime_boundary_check_finds_worker_workspaces_from_a_worktree (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_finds_worker_workspaces_from_a_worktree) ... ok
test_regime_boundary_check_flags_empty_seats_only (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_empty_seats_only) ... ok
test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout) ... ok
test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace) ... ok
test_regime_boundary_check_scans_every_worktree_for_untracked_evidence (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_scans_every_worktree_for_untracked_evidence) ... ok
test_registered_agent_not_ready_waits_for_idle_without_duplicate_start (test_herdr_agents.HerdrAgentsTest.test_registered_agent_not_ready_waits_for_idle_without_duplicate_start) ... ok
test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record (test_herdr_agents.HerdrAgentsTest.test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record) ... ok
test_remove_worker_closes_only_its_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_remove_worker_closes_only_its_tab_in_the_pair_workspace) ... ok
test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes (test_herdr_agents.HerdrAgentsTest.test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes) ... ok
test_remove_worker_force_retries_a_failed_graceful_despawn (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_retries_a_failed_graceful_despawn) ... ok
test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds) ... ok
test_remove_worker_forces_despawn_when_graceful_reports_needs_force (test_herdr_agents.HerdrAgentsTest.test_remove_worker_forces_despawn_when_graceful_reports_needs_force) ... ok
test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent (test_herdr_agents.HerdrAgentsTest.test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent) ... ok
test_remove_worker_refuses_a_dirty_worktree_without_force (test_herdr_agents.HerdrAgentsTest.test_remove_worker_refuses_a_dirty_worktree_without_force) ... ok
test_remove_worker_stops_when_a_graceful_despawn_fails (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_a_graceful_despawn_fails) ... ok
test_remove_worker_stops_when_the_forced_retry_also_fails (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_the_forced_retry_also_fails) ... ok
test_restart_worker_confirms_the_exit_dialog_once (test_herdr_agents.HerdrAgentsTest.test_restart_worker_confirms_the_exit_dialog_once) ... ok
test_restart_worker_exits_2_without_a_managed_workspace (test_herdr_agents.HerdrAgentsTest.test_restart_worker_exits_2_without_a_managed_workspace) ... ok
test_restart_worker_finds_a_solo_codex_worker_seat (test_herdr_agents.HerdrAgentsTest.test_restart_worker_finds_a_solo_codex_worker_seat) ... ok
test_restart_worker_finds_the_worker_by_its_seat_label (test_herdr_agents.HerdrAgentsTest.test_restart_worker_finds_the_worker_by_its_seat_label) ... ok
test_restart_worker_never_treats_the_audit_pane_as_the_worker (test_herdr_agents.HerdrAgentsTest.test_restart_worker_never_treats_the_audit_pane_as_the_worker) ... ok
test_restart_worker_passes_manifest_advisor_args_to_claude_worker (test_herdr_agents.HerdrAgentsTest.test_restart_worker_passes_manifest_advisor_args_to_claude_worker) ... ok
test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs) ... ok
test_restart_worker_refuses_unmanaged_extra_panes (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_unmanaged_extra_panes) ... ok
test_restart_worker_refuses_when_the_pane_never_reaches_a_shell (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_when_the_pane_never_reaches_a_shell) ... ok
test_restart_worker_relaunches_the_worker_in_its_existing_pane (test_herdr_agents.HerdrAgentsTest.test_restart_worker_relaunches_the_worker_in_its_existing_pane) ... ok
test_restart_worker_repairs_a_legacy_orchestrator_label_on_the_worker_pane (test_herdr_agents.HerdrAgentsTest.test_restart_worker_repairs_a_legacy_orchestrator_label_on_the_worker_pane) ... ok
test_restart_worker_reseats_a_main_path_worker_into_its_worktree (test_herdr_agents.HerdrAgentsTest.test_restart_worker_reseats_a_main_path_worker_into_its_worktree) ... ok
test_restart_worker_waits_for_stale_registration_then_retries_once (test_herdr_agents.HerdrAgentsTest.test_restart_worker_waits_for_stale_registration_then_retries_once) ... ok
test_seat_claim_fails_when_a_later_team_is_held_by_another_session (test_herdr_agents.HerdrAgentsTest.test_seat_claim_fails_when_a_later_team_is_held_by_another_session) ... ok
test_seat_claim_held_by_another_session_fails_without_release (test_herdr_agents.HerdrAgentsTest.test_seat_claim_held_by_another_session_fails_without_release) ... ok
test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude (test_herdr_agents.HerdrAgentsTest.test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude) ... ok
test_seat_claim_replaces_a_same_session_bare_lock (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_bare_lock) ... ok
test_seat_claim_replaces_a_same_session_composite_lock_of_a_dead_pid (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_composite_lock_of_a_dead_pid) ... ok
test_seat_claim_replaces_a_same_session_composite_lock_of_a_recycled_pid (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_composite_lock_of_a_recycled_pid) ... ok
test_seat_claim_replaces_same_session_bare_locks_in_every_team (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_same_session_bare_locks_in_every_team) ... ok
test_session_start_attach_bounds_a_trickling_hook_payload (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_bounds_a_trickling_hook_payload) ... ok
test_session_start_attach_claims_the_seat_in_a_managed_pane (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_claims_the_seat_in_a_managed_pane) ... ok
test_session_start_attach_claims_when_the_hook_keeps_stdin_open (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_claims_when_the_hook_keeps_stdin_open) ... ok
test_session_start_attach_prints_no_directive_for_a_pane_that_is_not_the_orchestrator (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_prints_no_directive_for_a_pane_that_is_not_the_orchestrator) ... ok
test_session_start_attach_prints_the_regime_directive_with_a_worker_seat (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_prints_the_regime_directive_with_a_worker_seat) ... ok
test_session_start_attach_reads_the_hook_payload_and_herdr_pid (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_reads_the_hook_payload_and_herdr_pid) ... ok
test_session_start_attach_skips_a_pane_that_is_not_the_orchestrator (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_skips_a_pane_that_is_not_the_orchestrator) ... ok
test_start_keeps_node_global_without_mise_tool_install (test_herdr_agents.HerdrAgentsTest.test_start_keeps_node_global_without_mise_tool_install) ... ok
test_start_removes_node_global_agent_clis_shadowing_mise (test_herdr_agents.HerdrAgentsTest.test_start_removes_node_global_agent_clis_shadowing_mise) ... ok
test_start_skips_node_global_removal_without_stray (test_herdr_agents.HerdrAgentsTest.test_start_skips_node_global_removal_without_stray) ... ok
test_successful_agent_start_does_not_poll_agent_list (test_herdr_agents.HerdrAgentsTest.test_successful_agent_start_does_not_poll_agent_list) ... ok
test_two_self_named_pair_workspaces_still_refuse (test_herdr_agents.HerdrAgentsTest.test_two_self_named_pair_workspaces_still_refuse) ... ok
test_uses_initial_workspace_pane_for_claude_and_splits_codex_right (test_herdr_agents.HerdrAgentsTest.test_uses_initial_workspace_pane_for_claude_and_splits_codex_right) ... ok
test_worker_github_pair_env (test_herdr_agents.HerdrAgentsTest.test_worker_github_pair_env) ... ok
test_worker_kind_claude_accepts_a_workspace_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_accepts_a_workspace_trust_dialog) ... ok
test_worker_kind_claude_appends_extra_worker_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_appends_extra_worker_args) ... ok
test_worker_kind_claude_does_not_require_codex (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_does_not_require_codex) ... ok
test_worker_kind_claude_skips_send_keys_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_skips_send_keys_without_a_trust_dialog) ... ok
test_worker_kind_claude_starts_a_claude_worker_pane_with_profile_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_starts_a_claude_worker_pane_with_profile_args) ... ok
test_worker_kind_claude_starts_with_no_resolved_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_starts_with_no_resolved_args) ... ok
test_worker_kind_defaults_to_generated_env_fragment (test_herdr_agents.HerdrAgentsTest.test_worker_kind_defaults_to_generated_env_fragment) ... ok
test_worker_kind_env_override_wins_over_generated_env_fragment (test_herdr_agents.HerdrAgentsTest.test_worker_kind_env_override_wins_over_generated_env_fragment) ... ok
test_worker_kind_rejects_an_unknown_value (test_herdr_agents.HerdrAgentsTest.test_worker_kind_rejects_an_unknown_value) ... ok
test_worker_profile_defaults_to_generated_worker_profile (test_herdr_agents.HerdrAgentsTest.test_worker_profile_defaults_to_generated_worker_profile) ... ok
test_worker_profile_env_override_wins_over_generated_worker_profile (test_herdr_agents.HerdrAgentsTest.test_worker_profile_env_override_wins_over_generated_worker_profile) ... ok
test_worker_seat_ambiguity_leaves_no_worktree_behind (test_herdr_agents.HerdrAgentsTest.test_worker_seat_ambiguity_leaves_no_worktree_behind) ... ok
test_worker_seat_is_skipped_in_a_non_git_directory (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_in_a_non_git_directory) ... ok
test_worker_seat_is_skipped_in_an_unregistered_repository (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_in_an_unregistered_repository) ... ok
test_worker_seat_is_skipped_outside_a_git_main_checkout (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_outside_a_git_main_checkout) ... ok
test_worker_seat_label_comes_from_the_worker_worktree_registration (test_herdr_agents.HerdrAgentsTest.test_worker_seat_label_comes_from_the_worker_worktree_registration) ... ok
test_worker_seat_refuses_a_path_that_is_not_a_worktree (test_herdr_agents.HerdrAgentsTest.test_worker_seat_refuses_a_path_that_is_not_a_worktree) ... ok
test_worker_seat_refuses_an_ambiguous_orchestrator_identity (test_herdr_agents.HerdrAgentsTest.test_worker_seat_refuses_an_ambiguous_orchestrator_identity) ... ok
test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree (test_herdr_agents.HerdrAgentsTest.test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree) ... ok
test_yazi_edit_opener_prefers_zed_with_editor_fallback (test_herdr_agents.HerdrAgentsTest.test_yazi_edit_opener_prefers_zed_with_editor_fallback) ... ok
test_zprofile_adds_common_bin_to_login_shell_path (test_herdr_agents.HerdrAgentsTest.test_zprofile_adds_common_bin_to_login_shell_path) ... ok
test_allow_pattern_rejects_shell_chaining (test_permgate.PermgateTest.test_allow_pattern_rejects_shell_chaining) ... ok
test_apply_patch_is_never_deterministically_allowed (test_permgate.PermgateTest.test_apply_patch_is_never_deterministically_allowed) ... ok
test_bash_credentials_fall_through_without_logging_them (test_permgate.PermgateTest.test_bash_credentials_fall_through_without_logging_them) ... ok
test_claude_and_codex_hook_outputs_match_golden_bytes (test_permgate.PermgateTest.test_claude_and_codex_hook_outputs_match_golden_bytes) ... ok
test_git_diff_output_option_is_never_automatically_allowed (test_permgate.PermgateTest.test_git_diff_output_option_is_never_automatically_allowed) ... ok
test_invalid_policy_fields_fail_closed (test_permgate.PermgateTest.test_invalid_policy_fields_fail_closed) ... ok
test_invalid_policy_returns_ask_and_logs_config_error (test_permgate.PermgateTest.test_invalid_policy_returns_ask_and_logs_config_error) ... ok
test_layer_one_allows_documented_claude_and_codex_contracts (test_permgate.PermgateTest.test_layer_one_allows_documented_claude_and_codex_contracts) ... ok
test_layer_one_deny_uses_both_hook_output_schemas (test_permgate.PermgateTest.test_layer_one_deny_uses_both_hook_output_schemas) ... ok
test_log_shape_redacts_command_and_output (test_permgate.PermgateTest.test_log_shape_redacts_command_and_output) ... ok
test_mutating_or_executable_read_options_fall_through (test_permgate.PermgateTest.test_mutating_or_executable_read_options_fall_through) ... ok
test_recursion_sentinel_is_a_complete_no_op (test_permgate.PermgateTest.test_recursion_sentinel_is_a_complete_no_op) ... ok
test_repository_policy_allows_and_falls_through (test_permgate.PermgateTest.test_repository_policy_allows_and_falls_through) ... ok
test_script_named_version_is_not_a_version_check (test_permgate.PermgateTest.test_script_named_version_is_not_a_version_check) ... ok
test_structured_secret_is_redacted_from_the_summary (test_permgate.PermgateTest.test_structured_secret_is_redacted_from_the_summary) ... ok
test_unconstrained_native_reads_fall_through (test_permgate.PermgateTest.test_unconstrained_native_reads_fall_through) ... ok
test_undecided_request_falls_through_to_the_native_prompt (test_permgate.PermgateTest.test_undecided_request_falls_through_to_the_native_prompt) ... ok
test_annotations_keep_every_level_even_on_passing_checks (test_pr_feedback.PrFeedbackTest.test_annotations_keep_every_level_even_on_passing_checks) ... ok
test_bots_are_detected_from_type_login_or_app (test_pr_feedback.PrFeedbackTest.test_bots_are_detected_from_type_login_or_app) ... ok
test_collects_every_feedback_source_for_the_head (test_pr_feedback.PrFeedbackTest.test_collects_every_feedback_source_for_the_head) ... ok
test_collects_the_github_base_with_the_head (test_pr_feedback.PrFeedbackTest.test_collects_the_github_base_with_the_head) ... ok
test_commit_status_keeps_the_latest_state_per_context (test_pr_feedback.PrFeedbackTest.test_commit_status_keeps_the_latest_state_per_context) ... ok
test_every_item_carries_the_disposition_schema (test_pr_feedback.PrFeedbackTest.test_every_item_carries_the_disposition_schema) ... ok
test_gh_never_receives_forced_colour (test_pr_feedback.PrFeedbackTest.test_gh_never_receives_forced_colour) ... ok
test_graphql_strings_are_raw_and_only_integers_are_typed (test_pr_feedback.PrFeedbackTest.test_graphql_strings_are_raw_and_only_integers_are_typed) ... ok
test_main_writes_the_document_to_json (test_pr_feedback.PrFeedbackTest.test_main_writes_the_document_to_json) ... ok
test_only_non_passing_check_runs_become_items (test_pr_feedback.PrFeedbackTest.test_only_non_passing_check_runs_become_items) ... ok
test_review_comments_carry_thread_resolution_across_pages (test_pr_feedback.PrFeedbackTest.test_review_comments_carry_thread_resolution_across_pages) ... ok
test_thread_state_covers_comments_beyond_the_first_page (test_pr_feedback.PrFeedbackTest.test_thread_state_covers_comments_beyond_the_first_page) ... ok
test_unauthenticated_gh_exits_non_zero (test_pr_feedback.PrFeedbackTest.test_unauthenticated_gh_exits_non_zero) ... ok
test_rule_mirrors_and_skills_carry_the_same_requirements (test_pr_feedback.PrIntegrationRuleParityTest.test_rule_mirrors_and_skills_carry_the_same_requirements) ... ok
test_rule_symlink_points_at_the_rule (test_pr_feedback.PrIntegrationRuleParityTest.test_rule_symlink_points_at_the_rule) ... ok
test_bump_writes_only_the_five_pins_through_set_asset (test_release_asset_pins.ReleaseAssetPinsTest.test_bump_writes_only_the_five_pins_through_set_asset) ... ok
test_window_never_moves_a_pin_backwards (test_release_asset_pins.ReleaseAssetPinsTest.test_window_never_moves_a_pin_backwards) ... ok
test_window_rejects_an_unknown_current_pin (test_release_asset_pins.ReleaseAssetPinsTest.test_window_rejects_an_unknown_current_pin) ... ok
test_window_skips_a_young_release_and_takes_an_older_one (test_release_asset_pins.ReleaseAssetPinsTest.test_window_skips_a_young_release_and_takes_an_older_one) ... ok
test_all_paths_are_preflighted_before_any_deletion (test_remove_agent_asset.RemoveAgentAssetTest.test_all_paths_are_preflighted_before_any_deletion) ... ok
test_brew_refuses_ambiguous_formula (test_remove_agent_asset.RemoveAgentAssetTest.test_brew_refuses_ambiguous_formula) ... ok
test_brew_uses_uninstall_for_unambiguous_formula (test_remove_agent_asset.RemoveAgentAssetTest.test_brew_uses_uninstall_for_unambiguous_formula) ... ok
test_crit_plugin_falls_back_to_data_path_but_not_config (test_remove_agent_asset.RemoveAgentAssetTest.test_crit_plugin_falls_back_to_data_path_but_not_config) ... ok
test_default_and_explicit_dry_run_print_without_mutating (test_remove_agent_asset.RemoveAgentAssetTest.test_default_and_explicit_dry_run_print_without_mutating) ... ok
test_integration_uses_verified_herdr_uninstall (test_remove_agent_asset.RemoveAgentAssetTest.test_integration_uses_verified_herdr_uninstall) ... ok
test_invalid_manifest_is_rejected (test_remove_agent_asset.RemoveAgentAssetTest.test_invalid_manifest_is_rejected) ... ok
test_parameterized_step_removal_preserves_sibling_identity (test_remove_agent_asset.RemoveAgentAssetTest.test_parameterized_step_removal_preserves_sibling_identity) ... ok
test_plugin_uses_verified_claude_uninstall (test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_claude_uninstall) ... ok
test_plugin_uses_verified_codex_remove (test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_codex_remove) ... ok
test_recorded_symlink_is_removed_without_following_target (test_remove_agent_asset.RemoveAgentAssetTest.test_recorded_symlink_is_removed_without_following_target) ... ok
test_tampered_manifest_outside_safe_roots_is_refused (test_remove_agent_asset.RemoveAgentAssetTest.test_tampered_manifest_outside_safe_roots_is_refused) ... ok
test_unknown_step_lists_known_steps_without_guessing (test_remove_agent_asset.RemoveAgentAssetTest.test_unknown_step_lists_known_steps_without_guessing) ... ok
test_yes_removes_only_recorded_path_and_preserves_other_steps (test_remove_agent_asset.RemoveAgentAssetTest.test_yes_removes_only_recorded_path_and_preserves_other_steps) ... ok
test_advanced_base_cannot_delete_collector_to_trigger_head_fallback (test_require_crit_review.ReviewGuardTest.test_advanced_base_cannot_delete_collector_to_trigger_head_fallback) ... ok
test_advanced_base_cannot_supply_an_untrusted_collector (test_require_crit_review.ReviewGuardTest.test_advanced_base_cannot_supply_an_untrusted_collector) ... ok
test_agent_lifecycle_script_change_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_script_change_requires_review) ... ok
test_agent_lifecycle_surfaces_require_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_surfaces_require_review) ... ok
test_agent_lifecycle_tokens_require_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_tokens_require_review) ... ok
test_agent_reviewer_rejects_empty_or_malformed_crit_data (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_rejects_empty_or_malformed_crit_data) ... ok
test_agent_reviewer_rejects_invalid_review_outcome (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_rejects_invalid_review_outcome) ... ok
test_agent_reviewer_with_command_string_source_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_command_string_source_still_requires_review) ... ok
test_agent_reviewer_with_crit_data_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_crit_data_satisfies_required_review) ... ok
test_agent_reviewer_with_crit_reviewed_marker_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_crit_reviewed_marker_still_requires_review) ... ok
test_agent_reviewer_with_external_crit_json_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_external_crit_json_still_requires_review) ... ok
test_agent_reviewer_with_non_review_crit_json_object_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_non_review_crit_json_object_still_requires_review) ... ok
test_agent_reviewer_with_resolved_line_comment_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_resolved_line_comment_satisfies_required_review) ... ok
test_agent_reviewer_with_unresolved_crit_json_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_unresolved_crit_json_still_requires_review) ... ok
test_agent_self_review_flag_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_self_review_flag_evidence_still_requires_review) ... ok
test_agent_self_reviewer_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_self_reviewer_evidence_still_requires_review) ... ok
test_audit_must_name_head_and_live_under_validation (test_require_crit_review.ReviewGuardTest.test_audit_must_name_head_and_live_under_validation) ... ok
test_base_accepts_a_correct_audit_of_head (test_require_crit_review.ReviewGuardTest.test_base_accepts_a_correct_audit_of_head) ... ok
test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base (test_require_crit_review.ReviewGuardTest.test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base) ... ok
test_base_fails_closed_when_github_metadata_is_unavailable (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_github_metadata_is_unavailable) ... ok
test_base_fails_closed_when_unresolvable_or_option_like (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_unresolvable_or_option_like) ... ok
test_base_rejects_forged_evidence_metadata (test_require_crit_review.ReviewGuardTest.test_base_rejects_forged_evidence_metadata) ... ok
test_base_rejects_pr_commits_before_executing_their_collector (test_require_crit_review.ReviewGuardTest.test_base_rejects_pr_commits_before_executing_their_collector) ... ok
test_base_rejects_side_branch_and_advanced_base_containing_pr_commits (test_require_crit_review.ReviewGuardTest.test_base_rejects_side_branch_and_advanced_base_containing_pr_commits) ... ok
test_base_requires_audit_evidence_for_a_reviewed_change (test_require_crit_review.ReviewGuardTest.test_base_requires_audit_evidence_for_a_reviewed_change) ... ok
test_base_requires_pr_feedback_evidence (test_require_crit_review.ReviewGuardTest.test_base_requires_pr_feedback_evidence) ... ok
test_base_reviews_committed_branch_changes (test_require_crit_review.ReviewGuardTest.test_base_reviews_committed_branch_changes) ... ok
test_blocked_or_missing_audit_verdict_fails (test_require_crit_review.ReviewGuardTest.test_blocked_or_missing_audit_verdict_fails) ... ok
test_broad_diff_requires_review (test_require_crit_review.ReviewGuardTest.test_broad_diff_requires_review) ... ok
test_broad_orchestration_only_pr_needs_no_audit (test_require_crit_review.ReviewGuardTest.test_broad_orchestration_only_pr_needs_no_audit) ... ok
test_companion_must_be_this_audits_own_last_message (test_require_crit_review.ReviewGuardTest.test_companion_must_be_this_audits_own_last_message) ... ok
test_explicit_disable_skips_guard (test_require_crit_review.ReviewGuardTest.test_explicit_disable_skips_guard) ... ok
test_feedback_accepts_absolute_path_through_a_repository_parent_alias (test_require_crit_review.ReviewGuardTest.test_feedback_accepts_absolute_path_through_a_repository_parent_alias) ... ok
test_feedback_cannot_hide_an_arbitrary_path_without_base (test_require_crit_review.ReviewGuardTest.test_feedback_cannot_hide_an_arbitrary_path_without_base) ... ok
test_feedback_does_not_exclude_symlink_aliases_outside_validation (test_require_crit_review.ReviewGuardTest.test_feedback_does_not_exclude_symlink_aliases_outside_validation) ... ok
test_feedback_path_itself_must_be_under_validation (test_require_crit_review.ReviewGuardTest.test_feedback_path_itself_must_be_under_validation) ... ok
test_feedback_symlink_cannot_hide_a_file_outside_validation (test_require_crit_review.ReviewGuardTest.test_feedback_symlink_cannot_hide_a_file_outside_validation) ... ok
test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent (test_require_crit_review.ReviewGuardTest.test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent) ... ok
test_github_identity_gate_activation_and_current_head_approval (test_require_crit_review.ReviewGuardTest.test_github_identity_gate_activation_and_current_head_approval) ... ok
test_github_lookup_ignores_environment_repository_override (test_require_crit_review.ReviewGuardTest.test_github_lookup_ignores_environment_repository_override) ... ok
test_github_lookup_rejects_evidence_from_another_repository (test_require_crit_review.ReviewGuardTest.test_github_lookup_rejects_evidence_from_another_repository) ... ok
test_high_risk_markdown_change_requires_review (test_require_crit_review.ReviewGuardTest.test_high_risk_markdown_change_requires_review) ... ok
test_incorrect_audit_needs_not_applicable_dispositions (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_not_applicable_dispositions) ... ok
test_incorrect_audit_without_findings_fails (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_without_findings_fails) ... ok
test_large_untracked_file_requires_broad_diff_review (test_require_crit_review.ReviewGuardTest.test_large_untracked_file_requires_broad_diff_review) ... ok
test_missing_base_collector_falls_back_only_after_binding (test_require_crit_review.ReviewGuardTest.test_missing_base_collector_falls_back_only_after_binding) ... ok
test_native_reviewed_environment_rejects_human_reviewer (test_require_crit_review.ReviewGuardTest.test_native_reviewed_environment_rejects_human_reviewer) ... ok
test_native_reviewed_without_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_native_reviewed_without_evidence_still_requires_review) ... ok
test_no_diff_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_no_diff_does_not_require_review) ... ok
test_older_base_must_not_be_on_the_head_first_parent_chain (test_require_crit_review.ReviewGuardTest.test_older_base_must_not_be_on_the_head_first_parent_chain) ... ok
test_orchestration_only_pr_needs_no_audit (test_require_crit_review.ReviewGuardTest.test_orchestration_only_pr_needs_no_audit) ... ok
test_pr_feedback_accepts_complete_evidence_without_a_bot_review (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_evidence_without_a_bot_review) ... ok
test_pr_feedback_accepts_complete_root_cause_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_root_cause_dispositions) ... ok
test_pr_feedback_bodies_are_compared_after_secret_masking (test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) ... ok
test_pr_feedback_evidence_file_is_not_counted_as_a_change (test_require_crit_review.ReviewGuardTest.test_pr_feedback_evidence_file_is_not_counted_as_a_change) ... ok
test_pr_feedback_fails_when_the_collector_cannot_run (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fails_when_the_collector_cannot_run) ... ok
test_pr_feedback_fixed_commit_must_be_in_the_pr_range (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fixed_commit_must_be_in_the_pr_range) ... ok
test_pr_feedback_matches_a_masked_path_but_not_an_edited_one (test_require_crit_review.ReviewGuardTest.test_pr_feedback_matches_a_masked_path_but_not_an_edited_one) ... ok
test_pr_feedback_must_be_collected_for_the_current_head (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_be_collected_for_the_current_head) ... ok
test_pr_feedback_must_cover_every_currently_collected_item (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_cover_every_currently_collected_item) ... ok
test_pr_feedback_rejects_evidence_outside_the_repository (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_evidence_outside_the_repository) ... ok
test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) ... ok
test_pr_feedback_requires_the_github_head_to_match (test_require_crit_review.ReviewGuardTest.test_pr_feedback_requires_the_github_head_to_match) ... ok
test_pr_feedback_uses_the_base_collector_not_the_prs_own (test_require_crit_review.ReviewGuardTest.test_pr_feedback_uses_the_base_collector_not_the_prs_own) ... ok
test_pr_feedback_without_base_is_only_format_checked (test_require_crit_review.ReviewGuardTest.test_pr_feedback_without_base_is_only_format_checked) ... ok
test_recollection_must_match_the_authenticated_repository (test_require_crit_review.ReviewGuardTest.test_recollection_must_match_the_authenticated_repository) ... ok
test_reviewed_environment_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_reviewed_environment_satisfies_required_review) ... ok
test_reviewed_with_blank_evidence_values_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_blank_evidence_values_still_requires_review) ... ok
test_reviewed_with_incomplete_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_incomplete_evidence_still_requires_review) ... ok
test_role_gate_boundary_exemption_checks_complete_committed_diff (test_require_crit_review.ReviewGuardTest.test_role_gate_boundary_exemption_checks_complete_committed_diff) ... ok
test_role_gate_requires_exact_sole_pr_bypass_actor (test_require_crit_review.ReviewGuardTest.test_role_gate_requires_exact_sole_pr_bypass_actor) ... ok
test_role_gate_update_activation_and_boundary_authorship (test_require_crit_review.ReviewGuardTest.test_role_gate_update_activation_and_boundary_authorship) ... ok
test_small_docs_only_change_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_small_docs_only_change_does_not_require_review) ... ok
test_verdict_comes_only_from_the_last_message_file (test_require_crit_review.ReviewGuardTest.test_verdict_comes_only_from_the_last_message_file) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok
test_agent_asset_update_runs_gh_extension_ensure (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_launchers_do_not_hardcode_model_ids (test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes) ... ok
test_agmsg_already_pinned_skips_download (test_runtime_health.RuntimeHealthTest.test_agmsg_already_pinned_skips_download) ... ok
test_agmsg_checksum_mismatch_fails_closed (test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed) ... ok
test_agmsg_fresh_install_populates_skill_and_records_manifest (test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest) ... ok
test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state) ... ok
test_agmsg_migration_reports_an_installer_that_mutates_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state) ... ok
test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty) ... ok
test_agmsg_refuses_to_install_without_tar (test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_without_tar) ... ok
test_agmsg_reports_an_installer_that_leaves_the_wrong_version (test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version) ... ok
test_agmsg_update_aborts_when_install_corrupts_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state) ... ok
test_agmsg_update_never_touches_teams_db_run (test_runtime_health.RuntimeHealthTest.test_agmsg_update_never_touches_teams_db_run) ... ok
test_client_bashrc_treats_private_sources_as_optional (test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... ok
test_codex_crit_normalizes_managed_marketplace_mode (test_runtime_health.RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode) ... ok
test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... ok
test_darwin_crit_checksum_failure_preserves_existing_binary (test_runtime_health.RuntimeHealthTest.test_darwin_crit_checksum_failure_preserves_existing_binary) ... ok
test_darwin_crit_install_is_pinned_atomic_and_recorded (test_runtime_health.RuntimeHealthTest.test_darwin_crit_install_is_pinned_atomic_and_recorded) ... ok
test_doctor_github_role_activation_and_file_storage (test_runtime_health.RuntimeHealthTest.test_doctor_github_role_activation_and_file_storage) ... ok
test_doctor_reports_claude_sandbox_prerequisites (test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_doctor_required_optional_and_healthy_statuses (test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_linux_crit_checksum_failure_preserves_existing_binary (test_runtime_health.RuntimeHealthTest.test_linux_crit_checksum_failure_preserves_existing_binary) ... ok
test_linux_crit_correct_version_is_download_free (test_runtime_health.RuntimeHealthTest.test_linux_crit_correct_version_is_download_free) ... ok
test_linux_crit_failure_does_not_leak_cleanup_trap (test_runtime_health.RuntimeHealthTest.test_linux_crit_failure_does_not_leak_cleanup_trap) ... ok
test_linux_crit_install_is_pinned_atomic_and_recorded (test_runtime_health.RuntimeHealthTest.test_linux_crit_install_is_pinned_atomic_and_recorded) ... ok
test_linux_crit_prefers_pinned_target_over_older_path_binary (test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_update_pulls_clean_main_before_apply (test_runtime_health.RuntimeHealthTest.test_make_update_pulls_clean_main_before_apply) ... ok
test_make_update_reports_unmerged_feature_branch_before_branch_notice (test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_feature_branch_before_branch_notice) ... ok
test_make_update_reports_unmerged_index_before_dirty_notice (test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_index_before_dirty_notice) ... ok
test_make_update_skips_dirty_main_with_manual_pull_notice (test_runtime_health.RuntimeHealthTest.test_make_update_skips_dirty_main_with_manual_pull_notice) ... ok
test_upgrade_applies_mise_only_from_successful_canonical_checkout (test_runtime_health.RuntimeHealthTest.test_upgrade_applies_mise_only_from_successful_canonical_checkout) ... ok
test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts (test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts) ... ok
test_upgrade_changes_checkout_not_live_mise_symlink_target (test_runtime_health.RuntimeHealthTest.test_upgrade_changes_checkout_not_live_mise_symlink_target) ... ok
test_upgrade_github_extensions_are_warning_only (test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_self_updates_mise_to_the_manifest_pin (test_runtime_health.RuntimeHealthTest.test_upgrade_self_updates_mise_to_the_manifest_pin) ... ok
test_upgrade_skips_unavailable_mise_self_update (test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok
test_upgrade_uses_current_mise_node_after_runtime_replacement (test_runtime_health.RuntimeHealthTest.test_upgrade_uses_current_mise_node_after_runtime_replacement)
Reject ambient npm after mise replaces the active Node runtime. ... ok
test_ci_smokes_exact_tools_with_network_denied (test_statusline_tools.StatuslineToolsTest.test_ci_smokes_exact_tools_with_network_denied) ... ok
test_direct_commands_use_offline_path_binaries (test_statusline_tools.StatuslineToolsTest.test_direct_commands_use_offline_path_binaries) ... ok
test_generated_commands_are_direct_and_static (test_statusline_tools.StatuslineToolsTest.test_generated_commands_are_direct_and_static) ... ok
test_mise_config_and_lock_pin_exact_npm_versions (test_statusline_tools.StatuslineToolsTest.test_mise_config_and_lock_pin_exact_npm_versions) ... ok
test_missing_binary_fails_immediately (test_statusline_tools.StatuslineToolsTest.test_missing_binary_fails_immediately) ... ok
test_binary_installers_replace_from_same_directory_stages (test_supply_chain_policy.SupplyChainPolicyTest.test_binary_installers_replace_from_same_directory_stages) ... ok
test_executable_downloads_are_verified_and_not_piped_to_shell (test_supply_chain_policy.SupplyChainPolicyTest.test_executable_downloads_are_verified_and_not_piped_to_shell) ... ok
test_external_checksum_failure_preserves_destination (test_supply_chain_policy.SupplyChainPolicyTest.test_external_checksum_failure_preserves_destination) ... ok
test_externals_render_without_network_discovery (test_supply_chain_policy.SupplyChainPolicyTest.test_externals_render_without_network_discovery) ... ok
test_externals_use_fixed_urls_and_checksums (test_supply_chain_policy.SupplyChainPolicyTest.test_externals_use_fixed_urls_and_checksums) ... ok
test_installer_cleanup_preserves_failure_status (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_preserves_failure_status) ... ok
test_installer_cleanup_survives_mock_function_returns (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) ... ok
test_mise_apply_replaces_live_symlinks_with_independent_copies (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_apply_replaces_live_symlinks_with_independent_copies) ... ok
test_mise_lock_matches_config_and_supported_platforms (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_matches_config_and_supported_platforms) ... ok
test_mise_lock_url_entries_have_checksums (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_url_entries_have_checksums) ... ok
test_mise_main_preserves_install_failure (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_main_preserves_install_failure) ... ok
test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts) ... ok
test_mise_versions_are_exact_and_locking_is_enforced (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_versions_are_exact_and_locking_is_enforced) ... ok
test_renovate_owns_dependency_update_notifications (test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications) ... ok
test_setup_ci_rejects_and_preserves_local_drift (test_supply_chain_policy.SupplyChainPolicyTest.test_setup_ci_rejects_and_preserves_local_drift) ... ok
test_sheldon_git_sources_have_revisions (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_git_sources_have_revisions) ... ok
test_sheldon_uses_locked_crates_io_source (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_uses_locked_crates_io_source) ... ok
test_absent_path_without_old_ref_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_absent_path_without_old_ref_is_regression) ... ok
test_chmod_only_change_keeps_the_source_unchanged_note (test_ua_symbol_coverage.UaSymbolCoverageTest.test_chmod_only_change_keeps_the_source_unchanged_note) ... ok
test_comment_lines_are_not_definitions (test_ua_symbol_coverage.UaSymbolCoverageTest.test_comment_lines_are_not_definitions) ... ok
test_def_column_reads_the_new_graph_revision (test_ua_symbol_coverage.UaSymbolCoverageTest.test_def_column_reads_the_new_graph_revision) ... ok
test_deleted_path_with_old_ref_is_explained (test_ua_symbol_coverage.UaSymbolCoverageTest.test_deleted_path_with_old_ref_is_explained) ... ok
test_flags_unexplained_symbol_loss_only (test_ua_symbol_coverage.UaSymbolCoverageTest.test_flags_unexplained_symbol_loss_only) ... ok
test_grammar_file_missing_from_graph_fails_in_covered_directories (test_ua_symbol_coverage.UaSymbolCoverageTest.test_grammar_file_missing_from_graph_fails_in_covered_directories) ... ok
test_low_similarity_move_with_no_symbols_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_low_similarity_move_with_no_symbols_is_regression) ... ok
test_partial_deletion_in_changed_source_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_partial_deletion_in_changed_source_is_regression) ... ok
test_partially_covered_new_file_is_not_flagged (test_ua_symbol_coverage.UaSymbolCoverageTest.test_partially_covered_new_file_is_not_flagged) ... ok
test_python_defs_inside_strings_do_not_count (test_ua_symbol_coverage.UaSymbolCoverageTest.test_python_defs_inside_strings_do_not_count) ... ok
test_rename_dropping_symbols_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_rename_dropping_symbols_is_regression) ... ok
test_rename_preserving_symbols_is_ok (test_ua_symbol_coverage.UaSymbolCoverageTest.test_rename_preserving_symbols_is_ok) ... ok
test_ruby_visibility_prefixed_defs_are_counted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_ruby_visibility_prefixed_defs_are_counted) ... ok
test_shell_names_with_punctuation_are_counted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_shell_names_with_punctuation_are_counted) ... ok
test_unchanged_source_loss_is_noted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unchanged_source_loss_is_noted) ... ok
test_unreadable_candidate_fails_closed (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unreadable_candidate_fails_closed) ... ok
test_unresolvable_ref_fails_closed (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unresolvable_ref_fails_closed) ... ok
test_uv_run_script_shebang_is_python (test_ua_symbol_coverage.UaSymbolCoverageTest.test_uv_run_script_shebang_is_python) ... ok
test_builds_in_the_clone_when_no_release_artifact_exists (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_builds_in_the_clone_when_no_release_artifact_exists) ... ok
test_builds_missing_core_in_the_release_artifact_then_copies_it (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_builds_missing_core_in_the_release_artifact_then_copies_it) ... ok
test_doctor_stale_warning_is_cleared_by_the_update_build (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_doctor_stale_warning_is_cleared_by_the_update_build) ... ok
test_frozen_install_failure_falls_back_to_plain_install (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_frozen_install_failure_falls_back_to_plain_install) ... ok
test_make_update_installs_the_pinned_pnpm (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_make_update_installs_the_pinned_pnpm) ... ok
test_prefers_mise_exec_over_an_unbacked_pnpm_shim (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_prefers_mise_exec_over_an_unbacked_pnpm_shim) ... ok
test_rebuilds_a_release_dist_older_than_its_sources (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_rebuilds_a_release_dist_older_than_its_sources) ... ok
test_skips_the_build_when_the_release_artifact_already_has_dist (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_skips_the_build_when_the_release_artifact_already_has_dist) ... ok
test_uses_mise_exec_when_pnpm_is_not_on_path (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_uses_mise_exec_when_pnpm_is_not_on_path) ... ok
test_uses_path_pnpm_only_when_mise_is_absent (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_uses_path_pnpm_only_when_mise_is_absent) ... ok
test_warns_and_continues_when_no_pnpm_is_resolvable (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_warns_and_continues_when_no_pnpm_is_resolvable) ... ok
test_warns_and_continues_when_the_build_fails (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_warns_and_continues_when_the_build_fails) ... ok
test_candidate_is_no_when_another_claude_family_is_larger (test_usage_review.UsageReviewTests.test_candidate_is_no_when_another_claude_family_is_larger) ... ok
test_malformed_latest_snapshot_warns_and_never_raises (test_usage_review.UsageReviewTests.test_malformed_latest_snapshot_warns_and_never_raises) ... ok
test_report_computes_share_ratio_and_baseline_deltas (test_usage_review.UsageReviewTests.test_report_computes_share_ratio_and_baseline_deltas) ... ok
test_report_emits_due_windows_and_matching_notes_suppress_them (test_usage_review.UsageReviewTests.test_report_emits_due_windows_and_matching_notes_suppress_them) ... ok
test_snapshot_does_not_rewrite_existing_daily_file (test_usage_review.UsageReviewTests.test_snapshot_does_not_rewrite_existing_daily_file) ... ok
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... <frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3df382d40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3df3832e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def59a80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def598a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def58f40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def5a890>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def5b3d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def59120>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def5ac50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def59030>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def58a90>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3df3835b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def59300>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3df2b5c60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def5b2e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def58c70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def59210>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3def58b80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3d120>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3d3f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3d030>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3ce50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3cd60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3c040>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3cc70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3cb80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3c130>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3c310>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3c8b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3c400>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3c220>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3ca90>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3d5d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3d6c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3d990>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3dc60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3dd50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3de40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3df30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3e020>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3e110>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3e200>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3e2f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xeec3ded3e3e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_masking_keeps_the_escape_before_the_key (test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_restart_worker (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_restart_worker) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_reject_a_malformed_render_entry (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_codex_modify_script_requires_executable_source (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_hook_composition_accepts_managed_source_fixture (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_nested_git_trees_only (test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/validate-agent-assets-test-o5js_2v8/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: /Users/mryfmo/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_secret_scan_allows_exact_placeholder_tokens (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_reads_json_per_key_and_string_value (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_placeholder_with_suffix (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok
test_checkout_does_not_persist_credentials_without_explicit_exemption (test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

----------------------------------------------------------------------
Ran 781 tests in 199.044s

OK

```

## /tmp/t90b-format-python.log

```text
2 files reformatted
1 file reformatted

```

## /tmp/t90b-format-docs.log

```text
README.md 136ms
home/dot_agents/skills/agmsg-orchestration/SKILL.md 65ms (unchanged)
home/dot_config/claude/rules/agmsg-orchestration.md 11ms (unchanged)
README.md 136ms
home/dot_agents/skills/agmsg-orchestration/SKILL.md 64ms (unchanged)
home/dot_config/claude/rules/agmsg-orchestration.md 11ms (unchanged)

```

## /tmp/t90b-crit-status.log

```text
{
  "branch": "feat/ruleset-sole-merger",
  "daemon": {
    "running": false
  },
  "review_file": "/home/moriya/.crit/reviews/38a07fafd366/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}

```

## /tmp/t90b-live-rules.json

```text
[{"type":"deletion","ruleset_source_type":"Repository","ruleset_source":"mryfmo/dotfiles","ruleset_id":24397953},{"type":"non_fast_forward","ruleset_source_type":"Repository","ruleset_source":"mryfmo/dotfiles","ruleset_id":24397953},{"type":"pull_request","parameters":{"required_approving_review_count":0,"dismiss_stale_reviews_on_push":true,"required_reviewers":[],"require_code_owner_review":false,"require_last_push_approval":false,"required_review_thread_resolution":true,"require_extra_approval_for_unattributed_changes":true,"allowed_merge_methods":["merge","squash","rebase"]},"ruleset_source_type":"Repository","ruleset_source":"mryfmo/dotfiles","ruleset_id":24397953},{"type":"required_status_checks","parameters":{"strict_required_status_checks_policy":true,"do_not_enforce_on_create":false,"required_status_checks":[{"context":"validate"},{"context":"test (ubuntu-24.04, server)"},{"context":"test (ubuntu-24.04, client)"},{"context":"test (macos-14, client)"},{"context":"public-bootstrap (ubuntu-24.04, server)"},{"context":"public-bootstrap (ubuntu-24.04, client)"},{"context":"public-bootstrap (macos-14, client)"}]},"ruleset_source_type":"Repository","ruleset_source":"mryfmo/dotfiles","ruleset_id":24397953}]
```

## /tmp/t90b-live-ruleset.json

```text
{"id":24397953,"name":"main integration gate","target":"branch","source_type":"Repository","source":"mryfmo/dotfiles","enforcement":"active","conditions":{"ref_name":{"exclude":[],"include":["~DEFAULT_BRANCH"]}},"rules":[{"type":"deletion"},{"type":"non_fast_forward"},{"type":"pull_request","parameters":{"required_approving_review_count":0,"dismiss_stale_reviews_on_push":true,"required_reviewers":[],"require_code_owner_review":false,"require_last_push_approval":false,"required_review_thread_resolution":true,"require_extra_approval_for_unattributed_changes":true,"allowed_merge_methods":["merge","squash","rebase"]}},{"type":"required_status_checks","parameters":{"strict_required_status_checks_policy":true,"do_not_enforce_on_create":false,"required_status_checks":[{"context":"validate"},{"context":"test (ubuntu-24.04, server)"},{"context":"test (ubuntu-24.04, client)"},{"context":"test (macos-14, client)"},{"context":"public-bootstrap (ubuntu-24.04, server)"},{"context":"public-bootstrap (ubuntu-24.04, client)"},{"context":"public-bootstrap (macos-14, client)"}]}}],"node_id":"RRS_lACqUmVwb3NpdG9yec5IzIBXzgF0SIE","created_at":"2026-10-03T09:00:22.897+09:00","updated_at":"2026-10-03T09:00:22.960+09:00","current_user_can_bypass":"never","_links":{"self":{"href":"https://api.github.com/repos/mryfmo/dotfiles/rulesets/24397953"},"html":{"href":"https://github.com/mryfmo/dotfiles/rules/24397953"}}}
```

## /tmp/t90b-orchestrator-user.json

```text
{"id":11512262,"login":"mryfmo"}

```

## /tmp/t90b-gh-version.log

```text
gh version 2.101.0 (2026-09-15)
https://github.com/cli/cli/releases/tag/v2.101.0

```

## /tmp/t90b-gh-merge-preflight.log

```text
	}

	_ = m.warnf("%s Pull request %s#%d (%s) has diverged from local branch\n", m.cs.Yellow("!"), ghrepo.FullName(m.baseRepo), m.pr.Number, m.pr.Title)
}

// Check if the current state of the pull request allows for merging
func (m *mergeContext) canMerge() error {
	if m.mergeQueueRequired {
		// Requesting branch deletion on a PR with a merge queue
		// policy is not allowed. Doing so can unexpectedly
		// delete branches before merging, close the PR, and remove
		// the PR from the merge queue.
		if m.opts.DeleteBranch {
			return fmt.Errorf("%s Cannot use `-d` or `--delete-branch` when merge queue enabled", m.cs.FailureIcon())
		}
		// Otherwise, a pull request can always be added to the merge queue
		return nil
	}

	reason := blockedReason(m.pr.MergeStateStatus, m.opts.UseAdmin)

	if reason == "" || m.autoMerge || m.merged {
		return nil
	}

	_ = m.warnf("%s Pull request %s#%d is not mergeable: %s.\n", m.cs.FailureIcon(), ghrepo.FullName(m.baseRepo), m.pr.Number, reason)
	_ = m.warnf("To have the pull request merged after all the requirements have been met, add the `--auto` flag.\n")
	if remote := remoteForMergeConflictResolution(m.baseRepo, m.pr, m.opts); remote != nil {
		mergeOrRebase := "merge"
		if m.opts.MergeMethod == PullRequestMergeMethodRebase {
			mergeOrRebase = "rebase"
		}
		fetchBranch := fmt.Sprintf("%s %s", remote.Name, m.pr.BaseRefName)
		mergeBranch := fmt.Sprintf("%s %s/%s", mergeOrRebase, remote.Name, m.pr.BaseRefName)
		cmd := fmt.Sprintf("gh pr checkout %d && git fetch %s && git %s", m.pr.Number, fetchBranch, mergeBranch)
		_ = m.warnf("Run the following to resolve the merge conflicts locally:\n  %s\n", m.cs.Bold(cmd))
	}
	if !m.opts.UseAdmin && allowsAdminOverride(m.pr.MergeStateStatus) {
		// TODO: show this flag only to repo admins
		_ = m.warnf("To use administrator privileges to immediately merge the pull request, add the `--admin` flag.\n")
	}
	return cmdutil.SilentError

```

## /tmp/t90b-gh-bypass-issue.json

```text
{"body":"  ### Description\n\n  When the calling user has ruleset bypass authority that would resolve a `mergeStateStatus: BLOCKED` PR (e.g., via `bypass_actors` with `bypass_mode:\n  pull_request` matching the user's `RepositoryRole`), `gh pr merge` refuses at pre-flight rather than attempting the merge. The error offers `--admin`\n  or `--auto` as escape hatches, neither of which fits what the user actually needs.\n\n  The underlying REST API merge endpoint (`PUT /repos/{owner}/{repo}/pulls/{n}/merge`) **does** engage bypass correctly when called directly. So the gap\n   is in `gh pr merge`'s pre-flight logic, not in the API.\n\n  For repositories using rulesets with `bypass_actors` as a deliberate design choice — codifying who can self-merge per design intent rather than via\n  admin override — this means every PR by a bypass-eligible user falls back to `--admin`. Bypass becomes configured-but-unused; admin overrides\n  accumulate as if the rule were misconfigured.\n\n  ### Reproduction\n\n  1. Configure a ruleset on `main` with `required_approving_review_count: 1` and:\n\n     ```json\n     \"bypass_actors\": [\n       {\n         \"actor_id\": 5,\n         \"actor_type\": \"RepositoryRole\",\n         \"bypass_mode\": \"pull_request\"\n       }\n     ]\n\n  2. As the bypass-eligible user (here, a repo admin — RepositoryRole=5), open a PR. The PR will have:\n    - mergeStateStatus: BLOCKED\n    - reviewDecision: REVIEW_REQUIRED\n    - reviewCount: 0\n  3. Confirm bypass eligibility — GET /repos/{owner}/{repo}/rulesets/{id} returns:\n\n  \"current_user_can_bypass\": \"pull_requests_only\"\n  4. Try gh pr merge:\n\n  $ gh pr merge <PR#> --squash --delete-branch\n  X Pull request <owner>/<repo>#<PR#> is not mergeable: the base branch policy prohibits the merge.\n  To have the pull request merged after all the requirements have been met, add the `--auto` flag.\n  To use administrator privileges to immediately merge the pull request, add the `--admin` flag.\n  5. Call the REST merge endpoint directly — succeeds, bypass engages:\n\n  $ gh api repos/<owner>/<repo>/pulls/<PR#>/merge -X PUT -f merge_method=squash\n  {\"sha\":\"...\",\"merged\":true,\"message\":\"Pull Request successfully merged\"}\n\n  Expected behavior\n\n  gh pr merge should detect bypass eligibility before refusing. Two reasonable fix shapes:\n\n  - Conservative: if mergeStateStatus: BLOCKED but current_user_can_bypass indicates bypass-via-pull_request, attempt the merge — the API will engage\n  bypass automatically.\n  - Simpler: always attempt the API merge and let GitHub's response be authoritative. Bypass engages or it doesn't, and either way the API's response is\n   meaningful (success, or a real error worth surfacing). The current pre-flight refusal pre-empts an outcome the API would have produced correctly.\n\n  Actual behavior\n\n  gh pr merge refuses based purely on mergeStateStatus: BLOCKED without checking bypass authority. Suggested escape hatches:\n\n  - --admin works but is structurally the wrong fit — admin override loudly overrides a rule that the user is in fact authorized to bypass per design.\n  - --auto doesn't engage bypass either; auto-merge waits for the original blockers to resolve, which (with bypass authority) won't happen organically.\n\n  gh version\n\n  gh version 2.90.0 (2026-04-16)\n\n  Why this matters\n\n  Rulesets with bypass_actors are a natural way to encode \"who can self-merge\" per design intent for repos with mixed-author models (e.g., bot-authored\n  PRs requiring review; human-authored PRs not). When gh pr merge doesn't respect bypass, the design becomes ceremony that doesn't deliver: operators\n  fall back to --admin per PR, repeated admin override erodes the rule's authority, and the codified bypass goes unused.\n\n  Current workaround: shell wrapper around gh api .../pulls/{n}/merge -X PUT. Functional but loses the ergonomic value of gh pr merge (mergeStateStatus\n  visibility, branch deletion semantics, default merge method from repo settings, etc.).\n\n  Upstream context\n\n  - GitHub Rulesets REST API: https://docs.github.com/en/rest/repos/rules\n  - current_user_can_bypass field: returned on GET /repos/{owner}/{repo}/rulesets/{id} — could serve as the pre-flight signal gh pr merge is currently\n  missing\n  EOF\n\n","state":"OPEN","title":"gh pr merge refuses when ruleset bypass authority would resolve the block","url":"https://github.com/cli/cli/issues/13388"}

```

## /tmp/t90b-auto-bypass-issue.json

```text
{"body":"### Page(s) affected\n\n- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository\n- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets (bypass list / pull request rule sections)\n\n### What's wrong\n\nThe Rulesets documentation describes `bypass_actors` (a Team, Role, GitHub App/Integration, etc. added to a ruleset's bypass list) as being able to bypass a rule such as \"Require a pull request before merging\" / \"Require review from Code Owners\". It does not document an important limitation we've confirmed by testing: **the bypass grant is only honored by a synchronous, direct merge call — it is not consulted by GitHub's async auto-merge completion process (`gh pr merge --auto`, `enablePullRequestAutoMerge`, or the \"Merge when ready\" UI button).**\n\n### Repro / evidence\n\n- Ruleset: `pull_request` rule, `require_code_owner_review: true`, `required_approving_review_count: 1`, with a GitHub App added to `bypass_actors` (`Integration` type; tested both `bypass_mode: \"always\"` and `\"pull_request\"`).\n- A PR approved by the bypass-listed actor with auto-merge enabled (`gh pr merge --auto --squash`) stayed `mergeStateStatus: BLOCKED` / `reviewDecision: REVIEW_REQUIRED` indefinitely — confirmed via a clean 10-minute poll (every 20s, 30/30 polls) with a fresh trigger event and zero manual intervention.\n- The same PR, same bypass-eligible actor, merged **instantly** when calling the merge endpoint directly instead:\n  ```\n  gh api repos/OWNER/REPO/pulls/N/merge -X PUT -f merge_method=squash\n  ```\n\nSo the bypass mechanism works, but only for one of the two documented ways to merge a PR, and the docs don't call this out anywhere.\n\n### What we'd like to see\n\nA note on the bypass_actors / rules pages clarifying that bypass grants are not currently honored by auto-merge completion, and that automation relying on bypass should call the merge endpoint directly rather than enabling auto-merge, until/unless this is fixed at the platform level.\n\n### Related reports (same underlying platform behavior, not a docs-only issue)\n\n- https://github.com/orgs/community/discussions/162623\n- https://github.com/orgs/community/discussions/190610\n- https://github.com/orgs/community/discussions/113172\n- https://github.com/orgs/community/discussions/167357\n- https://github.com/orgs/community/discussions/136531\n- https://github.com/cli/cli/issues/13388\n- https://github.com/cli/cli/issues/13458","state":"OPEN","title":"Rulesets docs don't disclose that bypass_actors is not honored by auto-merge completion","url":"https://github.com/github/docs/issues/45265"}

```

## /tmp/t90b-unit-final.log

```text
uv run python -m unittest discover -s tests/unit -v
test_bounded_scan_finishes_under_wall_limit (test_agent_session_staleness.AgentSessionStalenessTest.test_bounded_scan_finishes_under_wall_limit) ... ok
test_check_is_silent_when_assets_predate_session (test_agent_session_staleness.AgentSessionStalenessTest.test_check_is_silent_when_assets_predate_session) ... ok
test_check_reports_new_versions_and_mtimes_deduplicated_by_root (test_agent_session_staleness.AgentSessionStalenessTest.test_check_reports_new_versions_and_mtimes_deduplicated_by_root) ... ok
test_doctor_delegates_session_staleness_to_installed_script (test_agent_session_staleness.AgentSessionStalenessTest.test_doctor_delegates_session_staleness_to_installed_script) ... ok
test_hook_first_call_writes_private_baseline_and_is_silent (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_first_call_writes_private_baseline_and_is_silent) ... ok
test_hook_missing_or_garbage_stdin_is_silent_success (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_missing_or_garbage_stdin_is_silent_success) ... ok
test_hook_prunes_state_files_older_than_seven_days (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_prunes_state_files_older_than_seven_days) ... ok
test_hook_second_call_detects_asset_updated_after_baseline (test_agent_session_staleness.AgentSessionStalenessTest.test_hook_second_call_detects_asset_updated_after_baseline) ... ok
test_internal_failure_is_silent_success_with_one_stderr_line (test_agent_session_staleness.AgentSessionStalenessTest.test_internal_failure_is_silent_success_with_one_stderr_line) ... ok
test_no_arguments_prints_ten_recent_updates (test_agent_session_staleness.AgentSessionStalenessTest.test_no_arguments_prints_ten_recent_updates) ... ok
test_runtime_state_and_sqlite_files_are_excluded (test_agent_session_staleness.AgentSessionStalenessTest.test_runtime_state_and_sqlite_files_are_excluded) ... ok
test_ceiling_directories_do_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_ceiling_directories_do_not_hide_the_seat) ... ok
test_character_device_placeholder_is_skipped (test_agent_stop_gate.AgentStopGateTest.test_character_device_placeholder_is_skipped) ... ok
test_checkout_outside_any_seat_passes (test_agent_stop_gate.AgentStopGateTest.test_checkout_outside_any_seat_passes) ... ok
test_clean_orchestrator_passes (test_agent_stop_gate.AgentStopGateTest.test_clean_orchestrator_passes) ... ok
test_every_team_of_the_identity_is_checked (test_agent_stop_gate.AgentStopGateTest.test_every_team_of_the_identity_is_checked) ... ok
test_failing_git_status_blocks (test_agent_stop_gate.AgentStopGateTest.test_failing_git_status_blocks) ... ok
test_failing_identity_lookup_blocks_once (test_agent_stop_gate.AgentStopGateTest.test_failing_identity_lookup_blocks_once) ... ok
test_inherited_alternate_index_does_not_hide_a_staged_change (test_agent_stop_gate.AgentStopGateTest.test_inherited_alternate_index_does_not_hide_a_staged_change) ... ok
test_inherited_git_dir_does_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_inherited_git_dir_does_not_hide_the_seat) ... ok
test_injected_git_config_does_not_hide_untracked_files (test_agent_stop_gate.AgentStopGateTest.test_injected_git_config_does_not_hide_untracked_files) ... ok
test_json_escaped_cwd_resolves (test_agent_stop_gate.AgentStopGateTest.test_json_escaped_cwd_resolves) ... ok
test_missing_agmsg_install_passes (test_agent_stop_gate.AgentStopGateTest.test_missing_agmsg_install_passes) ... ok
test_mountinfo_cannot_be_redirected_through_the_environment (test_agent_stop_gate.AgentStopGateTest.test_mountinfo_cannot_be_redirected_through_the_environment) ... ok
test_null_device_of_another_filesystem_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_null_device_of_another_filesystem_is_not_a_placeholder) ... ok
test_orchestrator_acceptance_to_another_member_keeps_the_result_open (test_agent_stop_gate.AgentStopGateTest.test_orchestrator_acceptance_to_another_member_keeps_the_result_open) ... ok
test_project_dir_anchors_the_seat_after_a_cd (test_agent_stop_gate.AgentStopGateTest.test_project_dir_anchors_the_seat_after_a_cd) ... ok
test_read_only_bind_of_another_empty_file_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_read_only_bind_of_another_empty_file_is_not_a_placeholder) ... ok
test_read_write_mount_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_read_write_mount_is_not_a_placeholder) ... ok
test_result_then_acceptance_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_acceptance_passes) ... ok
test_result_then_revision_task_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_revision_task_passes) ... ok
test_result_without_acceptance_blocks (test_agent_stop_gate.AgentStopGateTest.test_result_without_acceptance_blocks) ... ok
test_same_named_file_bound_from_elsewhere_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_same_named_file_bound_from_elsewhere_is_not_a_placeholder) ... ok
test_sandbox_placeholders_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_are_skipped) ... ok
test_sandbox_placeholders_on_a_separate_filesystem_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_on_a_separate_filesystem_are_skipped) ... ok
test_separate_git_dir_main_worktree_is_a_seat (test_agent_stop_gate.AgentStopGateTest.test_separate_git_dir_main_worktree_is_a_seat) ... ok
test_slow_store_blocks_within_the_budget (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget) ... ok
test_slow_store_blocks_within_the_budget_with_gtimeout_only (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget_with_gtimeout_only) ... ok
test_slow_store_blocks_within_the_budget_without_timeout (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget_without_timeout) ... ok
test_solo_unsuffixed_worker_is_gated (test_agent_stop_gate.AgentStopGateTest.test_solo_unsuffixed_worker_is_gated) ... ok
test_sqlite_store_off_the_current_schema_is_not_initialized (test_agent_stop_gate.AgentStopGateTest.test_sqlite_store_off_the_current_schema_is_not_initialized) ... ok
test_staged_rename_out_of_orchestration_blocks (test_agent_stop_gate.AgentStopGateTest.test_staged_rename_out_of_orchestration_blocks) ... ok
test_stop_hook_active_skips_only_the_dirty_tree_check (test_agent_stop_gate.AgentStopGateTest.test_stop_hook_active_skips_only_the_dirty_tree_check) ... ok
test_unreadable_store_blocks_once (test_agent_stop_gate.AgentStopGateTest.test_unreadable_store_blocks_once) ... ok
test_untracked_file_outside_orchestration_blocks (test_agent_stop_gate.AgentStopGateTest.test_untracked_file_outside_orchestration_blocks) ... ok
test_untracked_symlink_to_a_mount_point_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_untracked_symlink_to_a_mount_point_is_not_a_placeholder) ... ok
test_untrusted_filenames_are_quoted (test_agent_stop_gate.AgentStopGateTest.test_untrusted_filenames_are_quoted) ... ok
test_user_bind_mount_of_a_real_file_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_user_bind_mount_of_a_real_file_is_not_a_placeholder) ... ok
test_whole_filesystem_bind_is_not_a_placeholder (test_agent_stop_gate.AgentStopGateTest.test_whole_filesystem_bind_is_not_a_placeholder) ... ok
test_worker_after_result_passes (test_agent_stop_gate.AgentStopGateTest.test_worker_after_result_passes) ... ok
test_worker_alive_pong_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_alive_pong_keeps_the_task_open) ... ok
test_worker_blocked_pong_closes_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_blocked_pong_closes_the_task) ... ok
test_worker_result_to_another_member_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_result_to_another_member_keeps_the_task_open) ... ok
test_worker_revise_acceptance_reopens_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_revise_acceptance_reopens_the_task) ... ok
test_worker_task_closed_by_a_non_revise_acceptance (test_agent_stop_gate.AgentStopGateTest.test_worker_task_closed_by_a_non_revise_acceptance) ... ok
test_worker_task_newer_than_result_blocks (test_agent_stop_gate.AgentStopGateTest.test_worker_task_newer_than_result_blocks) ... ok
test_worker_tracks_each_task_id (test_agent_stop_gate.AgentStopGateTest.test_worker_tracks_each_task_id) ... ok
test_default_store_uses_shared_helper (test_agmsg_dispatch.AgmsgDispatchTest.test_default_store_uses_shared_helper) ... ok
test_idle_wakes_once_and_reads (test_agmsg_dispatch.AgmsgDispatchTest.test_idle_wakes_once_and_reads) ... ok
test_invalid_timeout_does_not_send (test_agmsg_dispatch.AgmsgDispatchTest.test_invalid_timeout_does_not_send) ... ok
test_missing_pane_inserts_nothing (test_agmsg_dispatch.AgmsgDispatchTest.test_missing_pane_inserts_nothing) ... ok
test_rejects_identifiers_outside_the_strict_grammar (test_agmsg_dispatch.AgmsgDispatchTest.test_rejects_identifiers_outside_the_strict_grammar) ... ok
test_retry_does_not_wake_newly_working_pane (test_agmsg_dispatch.AgmsgDispatchTest.test_retry_does_not_wake_newly_working_pane) ... ok
test_timeout_is_one_shared_budget (test_agmsg_dispatch.AgmsgDispatchTest.test_timeout_is_one_shared_budget) ... ok
test_unread_retries_once_then_fails (test_agmsg_dispatch.AgmsgDispatchTest.test_unread_retries_once_then_fails) ... /home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff4ea3c40>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff4ea3b50>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490cd60>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490cf40>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d030>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d120>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d210>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d300>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d3f0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d4e0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d5d0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d6c0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d7b0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d8a0>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/contextlib.py:552: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d990>
  def _push_exit_callback(self, callback, is_sync=True):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_wake_failure_identifies_sent_message (test_agmsg_dispatch.AgmsgDispatchTest.test_wake_failure_identifies_sent_message) ... ok
test_worker_becoming_idle_after_send_is_woken (test_agmsg_dispatch.AgmsgDispatchTest.test_worker_becoming_idle_after_send_is_woken) ... ok
test_working_does_not_wake (test_agmsg_dispatch.AgmsgDispatchTest.test_working_does_not_wake) ... ok
test_working_unread_never_wakes (test_agmsg_dispatch.AgmsgDispatchTest.test_working_unread_never_wakes) ... ok
test_docs_no_longer_name_codex_review_commit (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_docs_no_longer_name_codex_review_commit) ... ok
test_rule_and_skill_share_the_audit_gate_and_bot_wait_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_audit_gate_and_bot_wait_invariants) ... ok
test_rule_and_skill_share_the_parallel_execution_and_routing_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_parallel_execution_and_routing_invariants) ... ok
test_rule_and_skill_share_the_registration_and_delivery_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_registration_and_delivery_invariants) ... ok
test_rule_drops_the_worker_network_escalation (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_drops_the_worker_network_escalation) ... ok
test_skill_drops_the_pane_status_gate_and_raw_pane_wakes (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_skill_drops_the_pane_status_gate_and_raw_pane_wakes) ... ok
test_doctor_fails_when_bwrap_is_missing_with_codex (test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_bwrap_is_missing_with_codex) ... ok
test_doctor_fails_when_the_bwrap_probe_fails (test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_the_bwrap_probe_fails) ... ok
test_doctor_is_not_applicable_without_the_restriction (test_apparmor_userns.AppArmorUsernsTest.test_doctor_is_not_applicable_without_the_restriction) ... ok
test_doctor_passes_when_the_bwrap_probe_succeeds (test_apparmor_userns.AppArmorUsernsTest.test_doctor_passes_when_the_bwrap_probe_succeeds) ... ok
test_doctor_warns_optionally_when_codex_is_missing (test_apparmor_userns.AppArmorUsernsTest.test_doctor_warns_optionally_when_codex_is_missing) ... ok
test_installer_copies_and_reloads_the_profile_with_sudo (test_apparmor_userns.AppArmorUsernsTest.test_installer_copies_and_reloads_the_profile_with_sudo) ... ok
test_installer_fails_when_loading_the_profile_fails (test_apparmor_userns.AppArmorUsernsTest.test_installer_fails_when_loading_the_profile_fails) ... ok
test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) ... ok
test_installer_leaves_the_profile_pending_without_cached_sudo (test_apparmor_userns.AppArmorUsernsTest.test_installer_leaves_the_profile_pending_without_cached_sudo) ... ok
test_wrapper_re_renders_when_prerequisites_change (test_apparmor_userns.AppArmorUsernsTest.test_wrapper_re_renders_when_prerequisites_change) ... ok
test_chezmoi_rendered_updater_uses_exported_source_root (test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_exported_source_root) ... ok
test_chezmoi_rendered_updater_uses_inlined_manifest_library (test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_inlined_manifest_library) ... ok
test_chezmoi_wrapper_renders_shebang_and_source_root (test_asset_manifest.AssetManifestTest.test_chezmoi_wrapper_renders_shebang_and_source_root) ... ok
test_failed_atomic_commit_leaves_previous_manifest_intact (test_asset_manifest.AssetManifestTest.test_failed_atomic_commit_leaves_previous_manifest_intact) ... ok
test_records_schema_two_steps_and_replaces_one_whole_entry (test_asset_manifest.AssetManifestTest.test_records_schema_two_steps_and_replaces_one_whole_entry) ... ok
test_rendered_updater_fails_when_no_source_root_is_valid (test_asset_manifest.AssetManifestTest.test_rendered_updater_fails_when_no_source_root_is_valid) ... ok
test_same_run_mise_repairs_preserve_both_identity_steps (test_asset_manifest.AssetManifestTest.test_same_run_mise_repairs_preserve_both_identity_steps) ... ok
test_two_real_install_steps_record_under_fake_home (test_asset_manifest.AssetManifestTest.test_two_real_install_steps_record_under_fake_home) ... ok
test_unwritable_destination_warns_once_without_failing (test_asset_manifest.AssetManifestTest.test_unwritable_destination_warns_once_without_failing) ... ok
test_updater_direct_source_resolves_repository_root (test_asset_manifest.AssetManifestTest.test_updater_direct_source_resolves_repository_root) ... ok
test_updater_has_one_recording_call_for_each_install_step (test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... ok
test_exit_zero_install_with_expected_fake_binary_passes_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_install_with_expected_fake_binary_passes_postcondition) ... ok
test_exit_zero_install_with_wrong_version_fails_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_install_with_wrong_version_fails_postcondition) ... ok
test_exit_zero_partial_install_without_binary_fails_postcondition (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_partial_install_without_binary_fails_postcondition) ... ok
test_gpgv_failure_preserves_existing_aws_and_skips_unzip (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_gpgv_failure_preserves_existing_aws_and_skips_unzip) ... ok
test_key_metadata_failures_stop_before_dearmor_and_gpgv (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_key_metadata_failures_stop_before_dearmor_and_gpgv) ... ok
test_linux_urls_are_versioned_and_unknown_architecture_fails (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_linux_urls_are_versioned_and_unknown_architecture_fails) ... ok
test_platform_package_managers_and_wrapper_own_aws_cli (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_platform_package_managers_and_wrapper_own_aws_cli) ... ok
test_repository_key_has_expected_current_fingerprint (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_repository_key_has_expected_current_fingerprint) ... ok
test_verified_archive_runs_installer_with_user_local_update_arguments (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_verified_archive_runs_installer_with_user_local_update_arguments) ... ok
test_wrong_staged_version_preserves_existing_aws_and_skips_installer (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_wrong_staged_version_preserves_existing_aws_and_skips_installer) ... ok
test_agmsg_runtime_paths_are_ignored_on_both_sides (test_check_agent_runtime.CheckAgentRuntimeTest.test_agmsg_runtime_paths_are_ignored_on_both_sides) ... ok
test_agmsg_separate_store_prefix_is_ignored (test_check_agent_runtime.CheckAgentRuntimeTest.test_agmsg_separate_store_prefix_is_ignored) ... ok
test_asset_repair_invokes_only_the_detected_step (test_check_agent_runtime.CheckAgentRuntimeTest.test_asset_repair_invokes_only_the_detected_step) ... ok
test_check_includes_ua_core_warnings (test_check_agent_runtime.CheckAgentRuntimeTest.test_check_includes_ua_core_warnings) ... /home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff4ea3b50>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff4ea3c40>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff51d76a0>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/glob.py:456: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff4e1f880>
  entries = list(scandir_it)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_check_uses_same_modified_for_codex_profiles (test_check_agent_runtime.CheckAgentRuntimeTest.test_check_uses_same_modified_for_codex_profiles) ... ok
test_chezmoi_drift_status_failure_is_warning (test_check_agent_runtime.CheckAgentRuntimeTest.test_chezmoi_drift_status_failure_is_warning) ... ok
test_chezmoi_drift_warnings_classify_status_and_mode_only (test_check_agent_runtime.CheckAgentRuntimeTest.test_chezmoi_drift_warnings_classify_status_and_mode_only) ... ok
test_compare_claude_skills_ignores_cowork_synced_subtree (test_check_agent_runtime.CheckAgentRuntimeTest.test_compare_claude_skills_ignores_cowork_synced_subtree) ... ok
test_content_drift_still_fails (test_check_agent_runtime.CheckAgentRuntimeTest.test_content_drift_still_fails) ... ok
test_crit_codex_skills_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_crit_codex_skills_are_not_orphans) ... ok
test_deleted_shared_skill_file_repair_converges (test_check_agent_runtime.CheckAgentRuntimeTest.test_deleted_shared_skill_file_repair_converges) ... ok
test_every_generated_chezmoi_repair_action_is_forced (test_check_agent_runtime.CheckAgentRuntimeTest.test_every_generated_chezmoi_repair_action_is_forced) ... ok
test_executable_prefix_is_compared_against_deployed_name (test_check_agent_runtime.CheckAgentRuntimeTest.test_executable_prefix_is_compared_against_deployed_name) ... ok
test_executable_prefix_requires_deployed_execute_bit (test_check_agent_runtime.CheckAgentRuntimeTest.test_executable_prefix_requires_deployed_execute_bit) ... ok
test_execute_repair_calls_each_mapped_command_once (test_check_agent_runtime.CheckAgentRuntimeTest.test_execute_repair_calls_each_mapped_command_once) ... ok
test_ignored_paths_suppress_receipt_linked_tree_entries (test_check_agent_runtime.CheckAgentRuntimeTest.test_ignored_paths_suppress_receipt_linked_tree_entries) ... ok
test_installed_manifest_integrity_reasons (test_check_agent_runtime.CheckAgentRuntimeTest.test_installed_manifest_integrity_reasons) ... ok
test_installer_owned_agmsg_skill_and_backups_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_installer_owned_agmsg_skill_and_backups_are_not_orphans) ... ok
test_invalid_manifest_is_one_error_and_skips_dependent_checks (test_check_agent_runtime.CheckAgentRuntimeTest.test_invalid_manifest_is_one_error_and_skips_dependent_checks) ... ok
test_json_modifier_accepts_cosmetic_reserialization (test_check_agent_runtime.CheckAgentRuntimeTest.test_json_modifier_accepts_cosmetic_reserialization) ... ok
test_json_modifier_rejects_real_value_drift (test_check_agent_runtime.CheckAgentRuntimeTest.test_json_modifier_rejects_real_value_drift) ... ok
test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode (test_check_agent_runtime.CheckAgentRuntimeTest.test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode) ... ok
test_manifest_drift_requires_recorded_step_with_missing_path (test_check_agent_runtime.CheckAgentRuntimeTest.test_manifest_drift_requires_recorded_step_with_missing_path) ... ok
test_missing_crit_asset_is_repairable (test_check_agent_runtime.CheckAgentRuntimeTest.test_missing_crit_asset_is_repairable) ... ok
test_missing_terminal_browser_receipt_is_harmless (test_check_agent_runtime.CheckAgentRuntimeTest.test_missing_terminal_browser_receipt_is_harmless) ... ok
test_only_exact_agmsg_root_legacy_database_names_are_ignored (test_check_agent_runtime.CheckAgentRuntimeTest.test_only_exact_agmsg_root_legacy_database_names_are_ignored) ... ok
test_orchestrator_seat_lock_is_quiet_for_a_composite_id_or_no_live_session (test_check_agent_runtime.CheckAgentRuntimeTest.test_orchestrator_seat_lock_is_quiet_for_a_composite_id_or_no_live_session) ... ok
test_orchestrator_seat_lock_warns_on_a_bare_session_id (test_check_agent_runtime.CheckAgentRuntimeTest.test_orchestrator_seat_lock_warns_on_a_bare_session_id) ... ok
test_orphan_detection_classifies_accounted_stale_and_orphan (test_check_agent_runtime.CheckAgentRuntimeTest.test_orphan_detection_classifies_accounted_stale_and_orphan) ... ok
test_parameterized_mise_step_uses_key_identity (test_check_agent_runtime.CheckAgentRuntimeTest.test_parameterized_mise_step_uses_key_identity) ... ok
test_private_prefix_is_compared_against_deployed_name (test_check_agent_runtime.CheckAgentRuntimeTest.test_private_prefix_is_compared_against_deployed_name) ... ok
test_repair_actions_map_only_detected_file_drift (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_actions_map_only_detected_file_drift) ... ok
test_repair_mode_converges_once_and_reports_each_action (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_converges_once_and_reports_each_action) ... ok
test_repair_mode_fails_after_one_non_convergent_round (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_fails_after_one_non_convergent_round) ... ok
test_repair_mode_never_acts_on_stale_or_orphan_warnings (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_mode_never_acts_on_stale_or_orphan_warnings) ... ok
test_repair_unset_is_byte_identical_and_never_mutates (test_check_agent_runtime.CheckAgentRuntimeTest.test_repair_unset_is_byte_identical_and_never_mutates) ... ok
test_sourced_asset_repair_runs_no_main_or_sibling_step (test_check_agent_runtime.CheckAgentRuntimeTest.test_sourced_asset_repair_runs_no_main_or_sibling_step) ... ok
test_terminal_browser_receipt_links_are_not_orphans (test_check_agent_runtime.CheckAgentRuntimeTest.test_terminal_browser_receipt_links_are_not_orphans) ... ok
test_ua_core_is_quiet_when_dist_is_fresh_or_no_clone_exists (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_is_quiet_when_dist_is_fresh_or_no_clone_exists) ... ok
test_ua_core_warns_when_dist_is_older_than_src (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_dist_is_older_than_src) ... ok
test_ua_core_warns_when_dist_is_older_than_the_root_lockfile (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_dist_is_older_than_the_root_lockfile) ... ok
test_ua_core_warns_when_the_codex_clone_has_no_built_dist (test_check_agent_runtime.CheckAgentRuntimeTest.test_ua_core_warns_when_the_codex_clone_has_no_built_dist) ... ok
test_unexpected_non_runtime_file_still_fails (test_check_agent_runtime.CheckAgentRuntimeTest.test_unexpected_non_runtime_file_still_fails) ... ok
test_unmanaged_top_level_skill_dir_warns (test_check_agent_runtime.CheckAgentRuntimeTest.test_unmanaged_top_level_skill_dir_warns) ... ok
test_apply_removes_the_symlink_farm_and_keeps_installer_owned_paths (test_chezmoiremove_agmsg.ChezmoiRemoveAgmsgTest.test_apply_removes_the_symlink_farm_and_keeps_installer_owned_paths) ... ok
test_retired_targets_are_listed_and_have_no_source (test_chezmoiremove_agmsg.ChezmoiRemoveRetiredShellFilesTest.test_retired_targets_are_listed_and_have_no_source) ... ok
test_current_only_key_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_only_key_is_preserved) ... ok
test_current_session_start_order_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_session_start_order_is_preserved)
Order is preserved; a stale bare herdr-agents command still migrates. ... ok
test_desired_current_output_is_byte_identical (test_claude_settings_merge.ClaudeSettingsMergeTest.test_desired_current_output_is_byte_identical) ... ok
test_empty_stdin_outputs_managed (test_claude_settings_merge.ClaudeSettingsMergeTest.test_empty_stdin_outputs_managed) ... ok
test_enabled_plugins_are_preserved_from_current (test_claude_settings_merge.ClaudeSettingsMergeTest.test_enabled_plugins_are_preserved_from_current) ... ok
test_invalid_json_outputs_managed (test_claude_settings_merge.ClaudeSettingsMergeTest.test_invalid_json_outputs_managed) ... ok
test_managed_hook_object_key_order_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_hook_object_key_order_is_preserved) ... ok
test_managed_permgate_replaces_stale_current_ccgate_hook (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_permgate_replaces_stale_current_ccgate_hook) ... ok
test_managed_session_start_replacement_keeps_hook_order (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replacement_keeps_hook_order)
Replacing a managed entry must not reorder SessionStart. ... ok
test_managed_session_start_replaces_stale_hard_coded_home_hook (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replaces_stale_hard_coded_home_hook)
Upgrade path: a machine that received the old hard-coded managed hook. ... ok
test_managed_wins_for_managed_key (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_wins_for_managed_key) ... ok
test_merge_is_idempotent (test_claude_settings_merge.ClaudeSettingsMergeTest.test_merge_is_idempotent) ... ok
test_permission_merge_preserves_custom_hook_in_mixed_entry (test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_custom_hook_in_mixed_entry) ... ok
test_permission_merge_preserves_unrelated_current_hooks (test_claude_settings_merge.ClaudeSettingsMergeTest.test_permission_merge_preserves_unrelated_current_hooks) ... ok
test_real_template_preserves_herdr_matcher_and_converges (test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_template_preserves_herdr_matcher_and_converges) ... ok
test_real_value_change_is_redumped (test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_value_change_is_redumped) ... ok
test_reordered_but_equal_current_is_byte_identical (test_claude_settings_merge.ClaudeSettingsMergeTest.test_reordered_but_equal_current_is_byte_identical) ... ok
test_runtime_enabled_plugins_survive_a_managed_file_without_the_key (test_claude_settings_merge.ClaudeSettingsMergeTest.test_runtime_enabled_plugins_survive_a_managed_file_without_the_key) ... ok
test_trailing_newline (test_claude_settings_merge.ClaudeSettingsMergeTest.test_trailing_newline) ... ok
test_current_only_runtime_tables_keep_current_group_order (test_codex_config_merge.CodexConfigMergeTest.test_current_only_runtime_tables_keep_current_group_order) ... ok
test_fresh_machine_outputs_managed_baseline (test_codex_config_merge.CodexConfigMergeTest.test_fresh_machine_outputs_managed_baseline) ... ok
test_managed_permgate_replaces_stale_private_ccgate_hook (test_codex_config_merge.CodexConfigMergeTest.test_managed_permgate_replaces_stale_private_ccgate_hook) ... ok
test_managed_templates_are_rendered_before_merge (test_codex_config_merge.CodexConfigMergeTest.test_managed_templates_are_rendered_before_merge) ... ok
test_managed_wins_for_managed_keys (test_codex_config_merge.CodexConfigMergeTest.test_managed_wins_for_managed_keys) ... ok
test_repeated_runtime_tables_are_preserved_in_order (test_codex_config_merge.CodexConfigMergeTest.test_repeated_runtime_tables_are_preserved_in_order) ... ok
test_retired_disabled_mcp_servers_are_purged_and_enabled_ones_kept (test_codex_config_merge.CodexConfigMergeTest.test_retired_disabled_mcp_servers_are_purged_and_enabled_ones_kept) ... ok
test_runtime_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_are_preserved) ... ok
test_runtime_tables_seed_from_managed_when_absent (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_seed_from_managed_when_absent) ... ok
test_unknown_current_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_unknown_current_tables_are_preserved) ... ok
test_working_tree_placeholder_falls_back_to_source_dir_parent (test_codex_config_merge.CodexConfigMergeTest.test_working_tree_placeholder_falls_back_to_source_dir_parent) ... ok
test_working_tree_placeholder_prefers_env_override (test_codex_config_merge.CodexConfigMergeTest.test_working_tree_placeholder_prefers_env_override) ... ok
test_rules_are_forbidden_only_and_cover_the_declared_prefixes (test_codex_execpolicy.CodexExecpolicyTest.test_rules_are_forbidden_only_and_cover_the_declared_prefixes) ... ok
test_missing_trusted_runtime_is_silent (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_missing_trusted_runtime_is_silent) ... ok
test_non_opted_project_is_silent_even_with_trusted_runtime (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_non_opted_project_is_silent_even_with_trusted_runtime) ... ok
test_project_cli_is_data_only_and_trusted_cli_gets_explicit_root (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_project_cli_is_data_only_and_trusted_cli_gets_explicit_root) ... ok
test_coverage_gems_are_compatible_and_exact (test_files_fixture.FilesFixtureTest.test_coverage_gems_are_compatible_and_exact) ... ok
test_fixture_uses_chezmoi_binary_outside_mise_shims (test_files_fixture.FilesFixtureTest.test_fixture_uses_chezmoi_binary_outside_mise_shims) ... ok
test_legacy_file_workflows_initialize_required_fixture_paths (test_files_fixture.FilesFixtureTest.test_legacy_file_workflows_initialize_required_fixture_paths) ... ok
test_a_missing_formatter_is_reported_without_a_traceback (test_format_edited_files_hook.FormatEditedFilesHookTest.test_a_missing_formatter_is_reported_without_a_traceback) ... ok
test_formatters_run_from_the_edited_files_repository_root (test_format_edited_files_hook.FormatEditedFilesHookTest.test_formatters_run_from_the_edited_files_repository_root) ... ok
test_a_declare_r_assignment_must_appear_exactly_once (test_generate_agent_configs.GenerateAgentConfigsTest.test_a_declare_r_assignment_must_appear_exactly_once) ... ok
test_a_list_render_writes_one_pin_into_several_files_and_declare_r (test_generate_agent_configs.GenerateAgentConfigsTest.test_a_list_render_writes_one_pin_into_several_files_and_declare_r) ... ok
test_absent_worker_profile_renders_no_env_line (test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_profile_renders_no_env_line) ... ok
test_absent_worker_worktree_renders_no_env_line (test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_worktree_renders_no_env_line) ... ok
test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map (test_generate_agent_configs.GenerateAgentConfigsTest.test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map) ... ok
test_asset_constant_must_be_assigned_exactly_once (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constant_must_be_assigned_exactly_once) ... ok
test_asset_constants_render_into_their_files (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constants_render_into_their_files) ... ok
test_asset_pin_must_be_a_plain_value (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_pin_must_be_a_plain_value) ... ok
test_audit_profile_renders_read_only_sandbox_override (test_generate_agent_configs.GenerateAgentConfigsTest.test_audit_profile_renders_read_only_sandbox_override) ... ok
test_bootstrap_pins_render_into_setup_and_their_installers (test_generate_agent_configs.GenerateAgentConfigsTest.test_bootstrap_pins_render_into_setup_and_their_installers) ... ok
test_check_reports_asset_render_drift (test_generate_agent_configs.GenerateAgentConfigsTest.test_check_reports_asset_render_drift) ... ok
test_claude_deny_rules_use_edit_for_file_mutations (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_deny_rules_use_edit_for_file_mutations) ... ok
test_claude_sandbox_renders_optional_socket_and_extra_write_keys (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_optional_socket_and_extra_write_keys) ... ok
test_claude_settings_render_interactive_advisor_only_when_set (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_interactive_advisor_only_when_set) ... ok
test_claude_settings_render_the_format_hook_from_its_path (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_the_format_hook_from_its_path) ... ok
test_claude_settings_renders_session_start_hooks (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_settings_use_interactive_profile_with_permgate (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_use_interactive_profile_with_permgate) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_codex_config_renders_permgate_permission_request (test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_permgate_permission_request) ... ok
test_codex_config_renders_working_tree_project_key (test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_working_tree_project_key) ... ok
test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot (test_generate_agent_configs.GenerateAgentConfigsTest.test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot) ... ok
test_expected_outputs_uses_codex_baseline_path (test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
test_managed_claude_sandbox_excludes_agmsg_dispatch (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_claude_sandbox_excludes_agmsg_dispatch) ... ok
test_managed_codex_path_includes_installed_common_bin (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_path_includes_installed_common_bin) ... ok
test_managed_hooks_use_installed_permgate_paths (test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_hooks_use_installed_permgate_paths) ... ok
test_manifest_keeps_model_ids_only_in_profiles (test_generate_agent_configs.GenerateAgentConfigsTest.test_manifest_keeps_model_ids_only_in_profiles) ... ok
test_model_profiles_env_renders_claude_advisor_only_when_set (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_claude_advisor_only_when_set) ... ok
test_model_profiles_env_renders_worker_kind (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_kind) ... ok
test_model_profiles_env_renders_worker_profile (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_profile) ... ok
test_model_profiles_env_renders_worker_worktree (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_worktree) ... ok
test_model_profiles_reject_incomplete_or_unsafe_entries (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_invalid_sandbox_mode (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_invalid_sandbox_mode) ... ok
test_model_profiles_reject_unsafe_advisor (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_profile_modify_scripts_are_byte_idempotent_with_runtime_state (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_byte_idempotent_with_runtime_state) ... ok
test_profile_modify_scripts_are_quiet_for_matching_hook_trust (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_quiet_for_matching_hook_trust) ... ok
test_profile_modify_scripts_preserve_repeated_runtime_tables (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_repeated_runtime_tables) ... ok
test_profile_modify_scripts_preserve_runtime_state (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_runtime_state) ... ok
test_profile_modify_scripts_seed_base_hook_trust (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_seed_base_hook_trust) ... ok
test_profile_modify_scripts_warn_on_hook_trust_divergence (test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_warn_on_hook_trust_divergence) ... ok
test_repository_marketplace_is_a_runtime_owned_seed (test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... ok
test_security_profile_renders_launcher_and_expanded_notify (test_generate_agent_configs.GenerateAgentConfigsTest.test_security_profile_renders_launcher_and_expanded_notify) ... ok
test_set_asset_field_rejects_unknown_targets_and_unsafe_values (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rejects_unknown_targets_and_unsafe_values) ... ok
test_set_asset_field_rewrites_only_the_named_scalar (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rewrites_only_the_named_scalar) ... ok
test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid) ... ok
test_set_asset_refuses_fields_other_than_pins_and_checksums (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_refuses_fields_other_than_pins_and_checksums) ... ok
test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string) ... ok
test_set_asset_reports_an_unparsable_manifest_without_a_traceback (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_reports_an_unparsable_manifest_without_a_traceback) ... ok
test_set_asset_updates_the_manifest_and_renders_its_pins (test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_updates_the_manifest_and_renders_its_pins) ... ok
test_unknown_interactive_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_worker_kind_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_gh_dir_is_shell_safe_and_defaults_to_separate_config) ... ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ERROR: worker_gh_config_dir must be an absolute or ~/ path without control characters
ok
test_worker_kind_defaults_to_codex (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_kind_defaults_to_codex) ... ok
test_worker_worktree_outside_claude_worktrees_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_worktree_outside_claude_worktrees_fails) ... ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ok
test_a_real_directory_of_that_name_stays_visible (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_a_real_directory_of_that_name_stays_visible) ... ok
test_claude_settings_stay_visible (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_claude_settings_stay_visible) ... ok
test_empty_placeholder_files_on_disk_leave_status_clean (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_empty_placeholder_files_on_disk_leave_status_clean) ... ok
test_every_placeholder_is_ignored_at_the_root_only (test_gitignore_sandbox_placeholders.SandboxPlaceholderIgnoreTest.test_every_placeholder_is_ignored_at_the_root_only) ... ok
test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits (test_herdr_agents.HerdrAgentsTest.test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits) ... ok
test_add_worker_derives_the_default_herdr_socket_for_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_derives_the_default_herdr_socket_for_spawn) ... ok
test_add_worker_emits_no_override_for_an_unparseable_codex_config (test_herdr_agents.HerdrAgentsTest.test_add_worker_emits_no_override_for_an_unparseable_codex_config) ... ok
test_add_worker_exits_zero_when_a_timed_out_spawn_still_links (test_herdr_agents.HerdrAgentsTest.test_add_worker_exits_zero_when_a_timed_out_spawn_still_links) ... ok
test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array (test_herdr_agents.HerdrAgentsTest.test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array) ... ok
test_add_worker_linkage_failure_prints_the_invocation_and_the_query (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_failure_prints_the_invocation_and_the_query) ... ok
test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver) ... ok
test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping) ... ok
test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace) ... ok
test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn) ... ok
test_add_worker_linkage_ignores_a_placement_record_from_another_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_from_another_workspace) ... ok
test_add_worker_linkage_ignores_a_pong_older_than_this_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_pong_older_than_this_ping) ... ok
test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal) ... ok
test_add_worker_linkage_refuses_a_placement_conflict (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_a_placement_conflict) ... ok
test_add_worker_linkage_refuses_several_orchestrator_identities (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_several_orchestrator_identities) ... ok
test_add_worker_linkage_resolves_an_id_keyed_placement_record (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_resolves_an_id_keyed_placement_record) ... ok
test_add_worker_linkage_survives_a_non_numeric_pong_wait (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_survives_a_non_numeric_pong_wait) ... ok
test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh) ... ok
test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options (test_herdr_agents.HerdrAgentsTest.test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options) ... ok
test_add_worker_refuses_an_undefined_profile_before_any_change (test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_an_undefined_profile_before_any_change) ... ok
test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found (test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found) ... ok
test_add_worker_rejects_a_worktree_outside_claude_worktrees (test_herdr_agents.HerdrAgentsTest.test_add_worker_rejects_a_worktree_outside_claude_worktrees) ... ok
test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog) ... ok
test_add_worker_reports_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_spawn) ... ok
test_add_worker_reports_linkage_ok_after_a_ready_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_ok_after_a_ready_spawn) ... ok
test_add_worker_reports_linkage_unreached_after_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_unreached_after_a_failed_spawn) ... ok
test_add_worker_reports_shallow_metadata_as_not_granted (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_shallow_metadata_as_not_granted) ... ok
test_add_worker_reuses_a_seat_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seat_tab_in_the_pair_workspace) ... ok
test_add_worker_reuses_a_seated_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seated_workspace) ... ok
test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace) ... ok
test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args (test_herdr_agents.HerdrAgentsTest.test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args) ... ok
test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog) ... ok
test_added_worker_github_environment_reaches_boot (test_herdr_agents.HerdrAgentsTest.test_added_worker_github_environment_reaches_boot) ... ok
test_agent_name_taken_gives_up_after_bounded_wait (test_herdr_agents.HerdrAgentsTest.test_agent_name_taken_gives_up_after_bounded_wait) ... ok
test_another_team_members_pane_is_not_a_second_worker (test_herdr_agents.HerdrAgentsTest.test_another_team_members_pane_is_not_a_second_worker) ... ok
test_attach_bootstraps_agmsg_after_codex_reuse (test_herdr_agents.HerdrAgentsTest.test_attach_bootstraps_agmsg_after_codex_reuse) ... ok
test_attach_bootstraps_agmsg_after_codex_start (test_herdr_agents.HerdrAgentsTest.test_attach_bootstraps_agmsg_after_codex_start) ... ok
test_attach_builds_codex_right_of_current_claude_pane (test_herdr_agents.HerdrAgentsTest.test_attach_builds_codex_right_of_current_claude_pane) ... ok
test_attach_complete_workspace_is_idempotent (test_herdr_agents.HerdrAgentsTest.test_attach_complete_workspace_is_idempotent) ... ok
test_attach_completes_bootstrap_on_a_self_named_pair (test_herdr_agents.HerdrAgentsTest.test_attach_completes_bootstrap_on_a_self_named_pair) ... ok
test_attach_correct_order_does_not_swap (test_herdr_agents.HerdrAgentsTest.test_attach_correct_order_does_not_swap) ... ok
test_attach_does_not_restart_codex_agent_from_another_tab (test_herdr_agents.HerdrAgentsTest.test_attach_does_not_restart_codex_agent_from_another_tab) ... ok
test_attach_equal_halves_does_not_resize (test_herdr_agents.HerdrAgentsTest.test_attach_equal_halves_does_not_resize) ... ok
test_attach_from_the_self_named_worker_pane_exits_quietly (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_self_named_worker_pane_exits_quietly) ... ok
test_attach_from_the_worker_pane_does_not_relabel_it (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_pane_does_not_relabel_it) ... ok
test_attach_from_the_worker_worktree_exits_quietly (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_worktree_exits_quietly) ... ok
test_attach_ignores_agmsg_bootstrap_failure (test_herdr_agents.HerdrAgentsTest.test_attach_ignores_agmsg_bootstrap_failure) ... ok
test_attach_ignores_extra_panes_on_other_tabs (test_herdr_agents.HerdrAgentsTest.test_attach_ignores_extra_panes_on_other_tabs) ... ok
test_attach_leaves_a_self_named_pair_alone (test_herdr_agents.HerdrAgentsTest.test_attach_leaves_a_self_named_pair_alone) ... ok
test_attach_legacy_files_pane_refuses_repair_without_layout_mutation (test_herdr_agents.HerdrAgentsTest.test_attach_legacy_files_pane_refuses_repair_without_layout_mutation) ... ok
test_attach_lowercases_and_validates_derived_agent_name (test_herdr_agents.HerdrAgentsTest.test_attach_lowercases_and_validates_derived_agent_name) ... ok
test_attach_noops_for_full_mode_managed_layout (test_herdr_agents.HerdrAgentsTest.test_attach_noops_for_full_mode_managed_layout) ... ok
test_attach_ratio_repair_skips_unsafe_layouts (test_herdr_agents.HerdrAgentsTest.test_attach_ratio_repair_skips_unsafe_layouts) ... ok
test_attach_rejects_invalid_derived_agent_name (test_herdr_agents.HerdrAgentsTest.test_attach_rejects_invalid_derived_agent_name) ... ok
test_attach_repair_splits_the_missing_worker_pane_in_its_worktree (test_herdr_agents.HerdrAgentsTest.test_attach_repair_splits_the_missing_worker_pane_in_its_worktree) ... ok
test_attach_repairs_codex_claude_order_with_one_swap (test_herdr_agents.HerdrAgentsTest.test_attach_repairs_codex_claude_order_with_one_swap) ... ok
test_attach_repairs_skewed_widths_to_equal_halves (test_herdr_agents.HerdrAgentsTest.test_attach_repairs_skewed_widths_to_equal_halves) ... ok
test_attach_reports_agmsg_skip_when_not_installed (test_herdr_agents.HerdrAgentsTest.test_attach_reports_agmsg_skip_when_not_installed) ... ok
test_attach_skips_delivery_when_turn_hook_exists (test_herdr_agents.HerdrAgentsTest.test_attach_skips_delivery_when_turn_hook_exists) ... ok
test_attach_warns_after_one_nonconverging_resize (test_herdr_agents.HerdrAgentsTest.test_attach_warns_after_one_nonconverging_resize) ... ok
test_attach_warns_when_multiple_agmsg_identities_exist (test_herdr_agents.HerdrAgentsTest.test_attach_warns_when_multiple_agmsg_identities_exist) ... ok
test_attach_without_herdr_environment_names_the_seated_worker (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_names_the_seated_worker) ... ok
test_attach_without_herdr_environment_prints_the_bring_up_summary (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_prints_the_bring_up_summary) ... ok
test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree) ... ok
test_audit_accepts_a_dir_with_an_apostrophe_quoted_intact (test_herdr_agents.HerdrAgentsTest.test_audit_accepts_a_dir_with_an_apostrophe_quoted_intact) ... ok
test_audit_creates_the_audit_tab_once_and_reuses_it (test_herdr_agents.HerdrAgentsTest.test_audit_creates_the_audit_tab_once_and_reuses_it) ... ok
test_audit_exits_2_without_a_managed_workspace (test_herdr_agents.HerdrAgentsTest.test_audit_exits_2_without_a_managed_workspace) ... ok
test_audit_fails_as_unmasked_when_masking_fails (test_herdr_agents.HerdrAgentsTest.test_audit_fails_as_unmasked_when_masking_fails) ... ok
test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info (test_herdr_agents.HerdrAgentsTest.test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info) ... ok
test_audit_finds_the_self_named_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_audit_finds_the_self_named_pair_workspace) ... ok
test_audit_gates_on_the_concluding_line_of_the_last_message (test_herdr_agents.HerdrAgentsTest.test_audit_gates_on_the_concluding_line_of_the_last_message) ... ok
test_audit_marker_detection_reads_unwrapped_snapshots (test_herdr_agents.HerdrAgentsTest.test_audit_marker_detection_reads_unwrapped_snapshots) ... ok
test_audit_masks_evidence_before_the_verdict_gate (test_herdr_agents.HerdrAgentsTest.test_audit_masks_evidence_before_the_verdict_gate) ... ok
test_audit_masks_evidence_even_when_the_audit_exit_is_nonzero (test_herdr_agents.HerdrAgentsTest.test_audit_masks_evidence_even_when_the_audit_exit_is_nonzero) ... ok
test_audit_nonzero_exit_marker_fails_the_helper (test_herdr_agents.HerdrAgentsTest.test_audit_nonzero_exit_marker_fails_the_helper) ... ok
test_audit_pane_command_tees_evidence_and_waits_for_a_fresh_marker (test_herdr_agents.HerdrAgentsTest.test_audit_pane_command_tees_evidence_and_waits_for_a_fresh_marker) ... ok
test_audit_quotes_a_non_ascii_out_path_under_the_c_locale (test_herdr_agents.HerdrAgentsTest.test_audit_quotes_a_non_ascii_out_path_under_the_c_locale) ... ok
test_audit_quotes_the_last_message_path_for_a_non_ascii_out (test_herdr_agents.HerdrAgentsTest.test_audit_quotes_the_last_message_path_for_a_non_ascii_out) ... ok
test_audit_refuses_a_busy_audit_pane (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_a_busy_audit_pane) ... ok
test_audit_refuses_a_tracked_masker_missing_from_the_tree (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_a_tracked_masker_missing_from_the_tree) ... ok
test_audit_refuses_an_uncommitted_or_untracked_masker (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_an_uncommitted_or_untracked_masker) ... ok
test_audit_refuses_the_masker_from_the_audited_commit (test_herdr_agents.HerdrAgentsTest.test_audit_refuses_the_masker_from_the_audited_commit) ... ok
test_audit_rejects_unsafe_arguments_before_calling_herdr (test_herdr_agents.HerdrAgentsTest.test_audit_rejects_unsafe_arguments_before_calling_herdr) ... ok
test_audit_runs_codex_exec_with_the_prompt_and_last_message_file (test_herdr_agents.HerdrAgentsTest.test_audit_runs_codex_exec_with_the_prompt_and_last_message_file) ... ok
test_audit_runs_in_dir_even_when_the_reused_pane_moved (test_herdr_agents.HerdrAgentsTest.test_audit_runs_in_dir_even_when_the_reused_pane_moved) ... ok
test_audit_skips_masking_without_a_repo_validator (test_herdr_agents.HerdrAgentsTest.test_audit_skips_masking_without_a_repo_validator) ... ok
test_audit_tab_does_not_break_attach_order_and_ratio_repair (test_herdr_agents.HerdrAgentsTest.test_audit_tab_does_not_break_attach_order_and_ratio_repair) ... ok
test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard (test_herdr_agents.HerdrAgentsTest.test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard) ... ok
test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff (test_herdr_agents.HerdrAgentsTest.test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff) ... ok
test_audit_task_names_a_txt_artifact_when_no_md_one_exists (test_herdr_agents.HerdrAgentsTest.test_audit_task_names_a_txt_artifact_when_no_md_one_exists) ... ok
test_audit_task_names_only_the_task_file_when_no_artifact_exists (test_herdr_agents.HerdrAgentsTest.test_audit_task_names_only_the_task_file_when_no_artifact_exists) ... ok
test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work (test_herdr_agents.HerdrAgentsTest.test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work) ... ok
test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot (test_herdr_agents.HerdrAgentsTest.test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot) ... ok
test_audit_uses_manifest_audit_codex_args (test_herdr_agents.HerdrAgentsTest.test_audit_uses_manifest_audit_codex_args) ... ok
test_audit_verdict_gate_reads_only_the_final_codex_block (test_herdr_agents.HerdrAgentsTest.test_audit_verdict_gate_reads_only_the_final_codex_block) ... ok
test_audit_waits_for_the_prompt_on_a_new_audit_tab (test_herdr_agents.HerdrAgentsTest.test_audit_waits_for_the_prompt_on_a_new_audit_tab) ... ok
test_bootstrap_accepts_same_identity_in_multiple_teams (test_herdr_agents.HerdrAgentsTest.test_bootstrap_accepts_same_identity_in_multiple_teams) ... ok
test_bootstrap_leaves_a_foreign_pre_push_hook_alone (test_herdr_agents.HerdrAgentsTest.test_bootstrap_leaves_a_foreign_pre_push_hook_alone) ... ok
test_bootstrap_only_creates_missing_herdr_log_directory (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_creates_missing_herdr_log_directory) ... ok
test_bootstrap_only_does_not_call_herdr_or_agents (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_does_not_call_herdr_or_agents) ... ok
test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing) ... ok
test_bootstrap_only_sets_each_missing_delivery_once (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_sets_each_missing_delivery_once) ... ok
test_bootstrap_only_skips_all_delivery_when_both_hooks_exist (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_all_delivery_when_both_hooks_exist) ... ok
test_bootstrap_only_skips_home_without_agmsg_calls (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_home_without_agmsg_calls) ... ok
test_bootstrap_only_warns_for_missing_claude_identity_without_joining (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_missing_claude_identity_without_joining) ... ok
test_bootstrap_only_warns_for_multiple_claude_identities (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_multiple_claude_identities) ... ok
test_bootstrap_removes_its_retired_pre_push_stub (test_herdr_agents.HerdrAgentsTest.test_bootstrap_removes_its_retired_pre_push_stub) ... ok
test_bootstrap_with_claude_worker_accepts_two_claude_identities (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_accepts_two_claude_identities) ... ok
test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity) ... ok
test_bootstrap_with_claude_worker_leaves_codex_hooks_alone (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_leaves_codex_hooks_alone) ... ok
test_claude_agent_accepts_manifest_profile_arguments_for_e2e (test_herdr_agents.HerdrAgentsTest.test_claude_agent_accepts_manifest_profile_arguments_for_e2e) ... ok
test_claude_repair_skips_just_restarted_codex_pane_without_agent_field (test_herdr_agents.HerdrAgentsTest.test_claude_repair_skips_just_restarted_codex_pane_without_agent_field) ... ok
test_claude_settings_add_herdr_attach_session_hook (test_herdr_agents.HerdrAgentsTest.test_claude_settings_add_herdr_attach_session_hook) ... ok
test_claude_worker_sharing_the_orchestrator_identity_is_refused (test_herdr_agents.HerdrAgentsTest.test_claude_worker_sharing_the_orchestrator_identity_is_refused) ... ok
test_claude_worker_with_a_registered_worker_identity_proceeds (test_herdr_agents.HerdrAgentsTest.test_claude_worker_with_a_registered_worker_identity_proceeds) ... ok
test_codex_profile_defaults_to_generated_interactive_profile (test_herdr_agents.HerdrAgentsTest.test_codex_profile_defaults_to_generated_interactive_profile) ... ok
test_codex_worker_is_not_subject_to_the_identity_guard (test_herdr_agents.HerdrAgentsTest.test_codex_worker_is_not_subject_to_the_identity_guard) ... ok
test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again (test_herdr_agents.HerdrAgentsTest.test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again) ... ok
test_existing_two_pane_workspace_repairs_skewed_widths (test_herdr_agents.HerdrAgentsTest.test_existing_two_pane_workspace_repairs_skewed_widths) ... ok
test_existing_workspace_matches_canonical_macos_workdir (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_matches_canonical_macos_workdir) ... ok
test_existing_workspace_restarts_missing_claude_in_empty_pane (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_claude_in_empty_pane) ... ok
test_existing_workspace_restarts_missing_codex_agent (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_codex_agent) ... ok
test_existing_workspace_splits_when_missing_claude_has_no_empty_pane (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_splits_when_missing_claude_has_no_empty_pane) ... ok
test_existing_workspace_with_legacy_files_pane_focuses_without_mutation (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_with_legacy_files_pane_focuses_without_mutation) ... ok
test_explicit_worker_kind_and_profile_survive_seat_label_loading (test_herdr_agents.HerdrAgentsTest.test_explicit_worker_kind_and_profile_survive_seat_label_loading) ... ok
test_file_viewer_plugin_config_sets_micro_editor (test_herdr_agents.HerdrAgentsTest.test_file_viewer_plugin_config_sets_micro_editor) ... ok
test_full_and_restart_modes_refuse_duplicate_managed_workspaces (test_herdr_agents.HerdrAgentsTest.test_full_and_restart_modes_refuse_duplicate_managed_workspaces) ... ok
test_full_mode_does_not_duplicate_a_solo_codex_worker_seat (test_herdr_agents.HerdrAgentsTest.test_full_mode_does_not_duplicate_a_solo_codex_worker_seat) ... ok
test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots (test_herdr_agents.HerdrAgentsTest.test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots) ... ok
test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree) ... ok
test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane) ... ok
test_full_mode_heal_never_starts_the_worker_in_the_audit_pane (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_starts_the_worker_in_the_audit_pane) ... ok
test_full_mode_heals_nothing_in_a_healthy_self_named_pair (test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_nothing_in_a_healthy_self_named_pair) ... ok
test_full_mode_heals_the_orchestrator_beside_a_live_added_claude_worker (test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_the_orchestrator_beside_a_live_added_claude_worker) ... ok
test_full_mode_reuses_agentless_worker_pane_in_attach_labeled_workspace (test_herdr_agents.HerdrAgentsTest.test_full_mode_reuses_agentless_worker_pane_in_attach_labeled_workspace) ... ok
test_full_mode_skips_agmsg_bootstrap_for_home (test_herdr_agents.HerdrAgentsTest.test_full_mode_skips_agmsg_bootstrap_for_home) ... ok
test_full_mode_splits_the_worker_pane_in_its_worktree (test_herdr_agents.HerdrAgentsTest.test_full_mode_splits_the_worker_pane_in_its_worktree) ... ok
test_ghostty_config_does_not_auto_start_herdr_session (test_herdr_agents.HerdrAgentsTest.test_ghostty_config_does_not_auto_start_herdr_session) ... ok
test_herdr_prefix_alt_a_runs_helper_from_active_pane (test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_alt_a_runs_helper_from_active_pane) ... ok
test_herdr_prefix_f_opens_file_viewer_popup (test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_f_opens_file_viewer_popup) ... ok
test_make_update_and_upgrade_include_agmsg_bootstrap (test_herdr_agents.HerdrAgentsTest.test_make_update_and_upgrade_include_agmsg_bootstrap) ... ok
test_mixed_legacy_and_seat_labels_are_one_pair (test_herdr_agents.HerdrAgentsTest.test_mixed_legacy_and_seat_labels_are_one_pair) ... ok
test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout (test_herdr_agents.HerdrAgentsTest.test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout) ... ok
test_orchestrator_pane_appends_claude_args_after_profile_args (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_appends_claude_args_after_profile_args) ... ok
test_orchestrator_pane_start_claims_the_seat_with_the_composite_id (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_start_claims_the_seat_with_the_composite_id) ... ok
test_orchestrator_pane_start_without_a_session_claims_nothing (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_start_without_a_session_claims_nothing) ... ok
test_orchestrator_pane_uses_interactive_profile_args (test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_uses_interactive_profile_args) ... ok
test_pane_creation_propagates_explicit_fpath (test_herdr_agents.HerdrAgentsTest.test_pane_creation_propagates_explicit_fpath) ... ok
test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat) ... ok
test_regime_boundary_check_finds_worker_workspaces_from_a_worktree (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_finds_worker_workspaces_from_a_worktree) ... ok
test_regime_boundary_check_flags_empty_seats_only (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_empty_seats_only) ... ok
test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout) ... ok
test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace) ... ok
test_regime_boundary_check_scans_every_worktree_for_untracked_evidence (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_scans_every_worktree_for_untracked_evidence) ... ok
test_registered_agent_not_ready_waits_for_idle_without_duplicate_start (test_herdr_agents.HerdrAgentsTest.test_registered_agent_not_ready_waits_for_idle_without_duplicate_start) ... ok
test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record (test_herdr_agents.HerdrAgentsTest.test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record) ... ok
test_remove_worker_closes_only_its_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_remove_worker_closes_only_its_tab_in_the_pair_workspace) ... ok
test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes (test_herdr_agents.HerdrAgentsTest.test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes) ... ok
test_remove_worker_force_retries_a_failed_graceful_despawn (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_retries_a_failed_graceful_despawn) ... ok
test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds) ... ok
test_remove_worker_forces_despawn_when_graceful_reports_needs_force (test_herdr_agents.HerdrAgentsTest.test_remove_worker_forces_despawn_when_graceful_reports_needs_force) ... ok
test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent (test_herdr_agents.HerdrAgentsTest.test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent) ... ok
test_remove_worker_refuses_a_dirty_worktree_without_force (test_herdr_agents.HerdrAgentsTest.test_remove_worker_refuses_a_dirty_worktree_without_force) ... ok
test_remove_worker_stops_when_a_graceful_despawn_fails (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_a_graceful_despawn_fails) ... ok
test_remove_worker_stops_when_the_forced_retry_also_fails (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_the_forced_retry_also_fails) ... ok
test_restart_worker_confirms_the_exit_dialog_once (test_herdr_agents.HerdrAgentsTest.test_restart_worker_confirms_the_exit_dialog_once) ... ok
test_restart_worker_exits_2_without_a_managed_workspace (test_herdr_agents.HerdrAgentsTest.test_restart_worker_exits_2_without_a_managed_workspace) ... ok
test_restart_worker_finds_a_solo_codex_worker_seat (test_herdr_agents.HerdrAgentsTest.test_restart_worker_finds_a_solo_codex_worker_seat) ... ok
test_restart_worker_finds_the_worker_by_its_seat_label (test_herdr_agents.HerdrAgentsTest.test_restart_worker_finds_the_worker_by_its_seat_label) ... ok
test_restart_worker_never_treats_the_audit_pane_as_the_worker (test_herdr_agents.HerdrAgentsTest.test_restart_worker_never_treats_the_audit_pane_as_the_worker) ... ok
test_restart_worker_passes_manifest_advisor_args_to_claude_worker (test_herdr_agents.HerdrAgentsTest.test_restart_worker_passes_manifest_advisor_args_to_claude_worker) ... ok
test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs) ... ok
test_restart_worker_refuses_unmanaged_extra_panes (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_unmanaged_extra_panes) ... ok
test_restart_worker_refuses_when_the_pane_never_reaches_a_shell (test_herdr_agents.HerdrAgentsTest.test_restart_worker_refuses_when_the_pane_never_reaches_a_shell) ... ok
test_restart_worker_relaunches_the_worker_in_its_existing_pane (test_herdr_agents.HerdrAgentsTest.test_restart_worker_relaunches_the_worker_in_its_existing_pane) ... ok
test_restart_worker_repairs_a_legacy_orchestrator_label_on_the_worker_pane (test_herdr_agents.HerdrAgentsTest.test_restart_worker_repairs_a_legacy_orchestrator_label_on_the_worker_pane) ... ok
test_restart_worker_reseats_a_main_path_worker_into_its_worktree (test_herdr_agents.HerdrAgentsTest.test_restart_worker_reseats_a_main_path_worker_into_its_worktree) ... ok
test_restart_worker_waits_for_stale_registration_then_retries_once (test_herdr_agents.HerdrAgentsTest.test_restart_worker_waits_for_stale_registration_then_retries_once) ... ok
test_seat_claim_fails_when_a_later_team_is_held_by_another_session (test_herdr_agents.HerdrAgentsTest.test_seat_claim_fails_when_a_later_team_is_held_by_another_session) ... ok
test_seat_claim_held_by_another_session_fails_without_release (test_herdr_agents.HerdrAgentsTest.test_seat_claim_held_by_another_session_fails_without_release) ... ok
test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude (test_herdr_agents.HerdrAgentsTest.test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude) ... ok
test_seat_claim_replaces_a_same_session_bare_lock (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_bare_lock) ... ok
test_seat_claim_replaces_a_same_session_composite_lock_of_a_dead_pid (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_composite_lock_of_a_dead_pid) ... ok
test_seat_claim_replaces_a_same_session_composite_lock_of_a_recycled_pid (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_composite_lock_of_a_recycled_pid) ... ok
test_seat_claim_replaces_same_session_bare_locks_in_every_team (test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_same_session_bare_locks_in_every_team) ... ok
test_session_start_attach_bounds_a_trickling_hook_payload (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_bounds_a_trickling_hook_payload) ... ok
test_session_start_attach_claims_the_seat_in_a_managed_pane (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_claims_the_seat_in_a_managed_pane) ... ok
test_session_start_attach_claims_when_the_hook_keeps_stdin_open (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_claims_when_the_hook_keeps_stdin_open) ... ok
test_session_start_attach_prints_no_directive_for_a_pane_that_is_not_the_orchestrator (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_prints_no_directive_for_a_pane_that_is_not_the_orchestrator) ... ok
test_session_start_attach_prints_the_regime_directive_with_a_worker_seat (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_prints_the_regime_directive_with_a_worker_seat) ... ok
test_session_start_attach_reads_the_hook_payload_and_herdr_pid (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_reads_the_hook_payload_and_herdr_pid) ... ok
test_session_start_attach_skips_a_pane_that_is_not_the_orchestrator (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_skips_a_pane_that_is_not_the_orchestrator) ... ok
test_start_keeps_node_global_without_mise_tool_install (test_herdr_agents.HerdrAgentsTest.test_start_keeps_node_global_without_mise_tool_install) ... ok
test_start_removes_node_global_agent_clis_shadowing_mise (test_herdr_agents.HerdrAgentsTest.test_start_removes_node_global_agent_clis_shadowing_mise) ... ok
test_start_skips_node_global_removal_without_stray (test_herdr_agents.HerdrAgentsTest.test_start_skips_node_global_removal_without_stray) ... ok
test_successful_agent_start_does_not_poll_agent_list (test_herdr_agents.HerdrAgentsTest.test_successful_agent_start_does_not_poll_agent_list) ... ok
test_two_self_named_pair_workspaces_still_refuse (test_herdr_agents.HerdrAgentsTest.test_two_self_named_pair_workspaces_still_refuse) ... ok
test_uses_initial_workspace_pane_for_claude_and_splits_codex_right (test_herdr_agents.HerdrAgentsTest.test_uses_initial_workspace_pane_for_claude_and_splits_codex_right) ... ok
test_worker_github_pair_env (test_herdr_agents.HerdrAgentsTest.test_worker_github_pair_env) ... ok
test_worker_kind_claude_accepts_a_workspace_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_accepts_a_workspace_trust_dialog) ... ok
test_worker_kind_claude_appends_extra_worker_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_appends_extra_worker_args) ... ok
test_worker_kind_claude_does_not_require_codex (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_does_not_require_codex) ... ok
test_worker_kind_claude_skips_send_keys_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_skips_send_keys_without_a_trust_dialog) ... ok
test_worker_kind_claude_starts_a_claude_worker_pane_with_profile_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_starts_a_claude_worker_pane_with_profile_args) ... ok
test_worker_kind_claude_starts_with_no_resolved_args (test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_starts_with_no_resolved_args) ... ok
test_worker_kind_defaults_to_generated_env_fragment (test_herdr_agents.HerdrAgentsTest.test_worker_kind_defaults_to_generated_env_fragment) ... ok
test_worker_kind_env_override_wins_over_generated_env_fragment (test_herdr_agents.HerdrAgentsTest.test_worker_kind_env_override_wins_over_generated_env_fragment) ... ok
test_worker_kind_rejects_an_unknown_value (test_herdr_agents.HerdrAgentsTest.test_worker_kind_rejects_an_unknown_value) ... ok
test_worker_profile_defaults_to_generated_worker_profile (test_herdr_agents.HerdrAgentsTest.test_worker_profile_defaults_to_generated_worker_profile) ... ok
test_worker_profile_env_override_wins_over_generated_worker_profile (test_herdr_agents.HerdrAgentsTest.test_worker_profile_env_override_wins_over_generated_worker_profile) ... ok
test_worker_seat_ambiguity_leaves_no_worktree_behind (test_herdr_agents.HerdrAgentsTest.test_worker_seat_ambiguity_leaves_no_worktree_behind) ... ok
test_worker_seat_is_skipped_in_a_non_git_directory (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_in_a_non_git_directory) ... ok
test_worker_seat_is_skipped_in_an_unregistered_repository (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_in_an_unregistered_repository) ... ok
test_worker_seat_is_skipped_outside_a_git_main_checkout (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_outside_a_git_main_checkout) ... ok
test_worker_seat_label_comes_from_the_worker_worktree_registration (test_herdr_agents.HerdrAgentsTest.test_worker_seat_label_comes_from_the_worker_worktree_registration) ... ok
test_worker_seat_refuses_a_path_that_is_not_a_worktree (test_herdr_agents.HerdrAgentsTest.test_worker_seat_refuses_a_path_that_is_not_a_worktree) ... ok
test_worker_seat_refuses_an_ambiguous_orchestrator_identity (test_herdr_agents.HerdrAgentsTest.test_worker_seat_refuses_an_ambiguous_orchestrator_identity) ... ok
test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree (test_herdr_agents.HerdrAgentsTest.test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree) ... ok
test_yazi_edit_opener_prefers_zed_with_editor_fallback (test_herdr_agents.HerdrAgentsTest.test_yazi_edit_opener_prefers_zed_with_editor_fallback) ... ok
test_zprofile_adds_common_bin_to_login_shell_path (test_herdr_agents.HerdrAgentsTest.test_zprofile_adds_common_bin_to_login_shell_path) ... ok
test_allow_pattern_rejects_shell_chaining (test_permgate.PermgateTest.test_allow_pattern_rejects_shell_chaining) ... ok
test_apply_patch_is_never_deterministically_allowed (test_permgate.PermgateTest.test_apply_patch_is_never_deterministically_allowed) ... ok
test_bash_credentials_fall_through_without_logging_them (test_permgate.PermgateTest.test_bash_credentials_fall_through_without_logging_them) ... ok
test_claude_and_codex_hook_outputs_match_golden_bytes (test_permgate.PermgateTest.test_claude_and_codex_hook_outputs_match_golden_bytes) ... ok
test_git_diff_output_option_is_never_automatically_allowed (test_permgate.PermgateTest.test_git_diff_output_option_is_never_automatically_allowed) ... ok
test_invalid_policy_fields_fail_closed (test_permgate.PermgateTest.test_invalid_policy_fields_fail_closed) ... ok
test_invalid_policy_returns_ask_and_logs_config_error (test_permgate.PermgateTest.test_invalid_policy_returns_ask_and_logs_config_error) ... ok
test_layer_one_allows_documented_claude_and_codex_contracts (test_permgate.PermgateTest.test_layer_one_allows_documented_claude_and_codex_contracts) ... ok
test_layer_one_deny_uses_both_hook_output_schemas (test_permgate.PermgateTest.test_layer_one_deny_uses_both_hook_output_schemas) ... ok
test_log_shape_redacts_command_and_output (test_permgate.PermgateTest.test_log_shape_redacts_command_and_output) ... ok
test_mutating_or_executable_read_options_fall_through (test_permgate.PermgateTest.test_mutating_or_executable_read_options_fall_through) ... ok
test_recursion_sentinel_is_a_complete_no_op (test_permgate.PermgateTest.test_recursion_sentinel_is_a_complete_no_op) ... ok
test_repository_policy_allows_and_falls_through (test_permgate.PermgateTest.test_repository_policy_allows_and_falls_through) ... ok
test_script_named_version_is_not_a_version_check (test_permgate.PermgateTest.test_script_named_version_is_not_a_version_check) ... ok
test_structured_secret_is_redacted_from_the_summary (test_permgate.PermgateTest.test_structured_secret_is_redacted_from_the_summary) ... ok
test_unconstrained_native_reads_fall_through (test_permgate.PermgateTest.test_unconstrained_native_reads_fall_through) ... ok
test_undecided_request_falls_through_to_the_native_prompt (test_permgate.PermgateTest.test_undecided_request_falls_through_to_the_native_prompt) ... ok
test_annotations_keep_every_level_even_on_passing_checks (test_pr_feedback.PrFeedbackTest.test_annotations_keep_every_level_even_on_passing_checks) ... ok
test_bots_are_detected_from_type_login_or_app (test_pr_feedback.PrFeedbackTest.test_bots_are_detected_from_type_login_or_app) ... ok
test_collects_every_feedback_source_for_the_head (test_pr_feedback.PrFeedbackTest.test_collects_every_feedback_source_for_the_head) ... ok
test_collects_the_github_base_with_the_head (test_pr_feedback.PrFeedbackTest.test_collects_the_github_base_with_the_head) ... ok
test_commit_status_keeps_the_latest_state_per_context (test_pr_feedback.PrFeedbackTest.test_commit_status_keeps_the_latest_state_per_context) ... ok
test_every_item_carries_the_disposition_schema (test_pr_feedback.PrFeedbackTest.test_every_item_carries_the_disposition_schema) ... ok
test_gh_never_receives_forced_colour (test_pr_feedback.PrFeedbackTest.test_gh_never_receives_forced_colour) ... ok
test_graphql_strings_are_raw_and_only_integers_are_typed (test_pr_feedback.PrFeedbackTest.test_graphql_strings_are_raw_and_only_integers_are_typed) ... ok
test_main_writes_the_document_to_json (test_pr_feedback.PrFeedbackTest.test_main_writes_the_document_to_json) ... ok
test_only_non_passing_check_runs_become_items (test_pr_feedback.PrFeedbackTest.test_only_non_passing_check_runs_become_items) ... ok
test_review_comments_carry_thread_resolution_across_pages (test_pr_feedback.PrFeedbackTest.test_review_comments_carry_thread_resolution_across_pages) ... ok
test_thread_state_covers_comments_beyond_the_first_page (test_pr_feedback.PrFeedbackTest.test_thread_state_covers_comments_beyond_the_first_page) ... ok
test_unauthenticated_gh_exits_non_zero (test_pr_feedback.PrFeedbackTest.test_unauthenticated_gh_exits_non_zero) ... ok
test_rule_mirrors_and_skills_carry_the_same_requirements (test_pr_feedback.PrIntegrationRuleParityTest.test_rule_mirrors_and_skills_carry_the_same_requirements) ... ok
test_rule_symlink_points_at_the_rule (test_pr_feedback.PrIntegrationRuleParityTest.test_rule_symlink_points_at_the_rule) ... ok
test_bump_writes_only_the_five_pins_through_set_asset (test_release_asset_pins.ReleaseAssetPinsTest.test_bump_writes_only_the_five_pins_through_set_asset) ... ok
test_window_never_moves_a_pin_backwards (test_release_asset_pins.ReleaseAssetPinsTest.test_window_never_moves_a_pin_backwards) ... ok
test_window_rejects_an_unknown_current_pin (test_release_asset_pins.ReleaseAssetPinsTest.test_window_rejects_an_unknown_current_pin) ... ok
test_window_skips_a_young_release_and_takes_an_older_one (test_release_asset_pins.ReleaseAssetPinsTest.test_window_skips_a_young_release_and_takes_an_older_one) ... ok
test_all_paths_are_preflighted_before_any_deletion (test_remove_agent_asset.RemoveAgentAssetTest.test_all_paths_are_preflighted_before_any_deletion) ... ok
test_brew_refuses_ambiguous_formula (test_remove_agent_asset.RemoveAgentAssetTest.test_brew_refuses_ambiguous_formula) ... ok
test_brew_uses_uninstall_for_unambiguous_formula (test_remove_agent_asset.RemoveAgentAssetTest.test_brew_uses_uninstall_for_unambiguous_formula) ... ok
test_crit_plugin_falls_back_to_data_path_but_not_config (test_remove_agent_asset.RemoveAgentAssetTest.test_crit_plugin_falls_back_to_data_path_but_not_config) ... ok
test_default_and_explicit_dry_run_print_without_mutating (test_remove_agent_asset.RemoveAgentAssetTest.test_default_and_explicit_dry_run_print_without_mutating) ... ok
test_integration_uses_verified_herdr_uninstall (test_remove_agent_asset.RemoveAgentAssetTest.test_integration_uses_verified_herdr_uninstall) ... ok
test_invalid_manifest_is_rejected (test_remove_agent_asset.RemoveAgentAssetTest.test_invalid_manifest_is_rejected) ... ok
test_parameterized_step_removal_preserves_sibling_identity (test_remove_agent_asset.RemoveAgentAssetTest.test_parameterized_step_removal_preserves_sibling_identity) ... ok
test_plugin_uses_verified_claude_uninstall (test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_claude_uninstall) ... ok
test_plugin_uses_verified_codex_remove (test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_codex_remove) ... ok
test_recorded_symlink_is_removed_without_following_target (test_remove_agent_asset.RemoveAgentAssetTest.test_recorded_symlink_is_removed_without_following_target) ... ok
test_tampered_manifest_outside_safe_roots_is_refused (test_remove_agent_asset.RemoveAgentAssetTest.test_tampered_manifest_outside_safe_roots_is_refused) ... ok
test_unknown_step_lists_known_steps_without_guessing (test_remove_agent_asset.RemoveAgentAssetTest.test_unknown_step_lists_known_steps_without_guessing) ... ok
test_yes_removes_only_recorded_path_and_preserves_other_steps (test_remove_agent_asset.RemoveAgentAssetTest.test_yes_removes_only_recorded_path_and_preserves_other_steps) ... ok
test_advanced_base_cannot_delete_collector_to_trigger_head_fallback (test_require_crit_review.ReviewGuardTest.test_advanced_base_cannot_delete_collector_to_trigger_head_fallback) ... ok
test_advanced_base_cannot_supply_an_untrusted_collector (test_require_crit_review.ReviewGuardTest.test_advanced_base_cannot_supply_an_untrusted_collector) ... ok
test_agent_lifecycle_script_change_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_script_change_requires_review) ... ok
test_agent_lifecycle_surfaces_require_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_surfaces_require_review) ... ok
test_agent_lifecycle_tokens_require_review (test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_tokens_require_review) ... ok
test_agent_reviewer_rejects_empty_or_malformed_crit_data (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_rejects_empty_or_malformed_crit_data) ... ok
test_agent_reviewer_rejects_invalid_review_outcome (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_rejects_invalid_review_outcome) ... ok
test_agent_reviewer_with_command_string_source_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_command_string_source_still_requires_review) ... ok
test_agent_reviewer_with_crit_data_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_crit_data_satisfies_required_review) ... ok
test_agent_reviewer_with_crit_reviewed_marker_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_crit_reviewed_marker_still_requires_review) ... ok
test_agent_reviewer_with_external_crit_json_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_external_crit_json_still_requires_review) ... ok
test_agent_reviewer_with_non_review_crit_json_object_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_non_review_crit_json_object_still_requires_review) ... ok
test_agent_reviewer_with_resolved_line_comment_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_resolved_line_comment_satisfies_required_review) ... ok
test_agent_reviewer_with_unresolved_crit_json_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_unresolved_crit_json_still_requires_review) ... ok
test_agent_self_review_flag_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_self_review_flag_evidence_still_requires_review) ... ok
test_agent_self_reviewer_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_agent_self_reviewer_evidence_still_requires_review) ... ok
test_audit_must_name_head_and_live_under_validation (test_require_crit_review.ReviewGuardTest.test_audit_must_name_head_and_live_under_validation) ... ok
test_base_accepts_a_correct_audit_of_head (test_require_crit_review.ReviewGuardTest.test_base_accepts_a_correct_audit_of_head) ... ok
test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base (test_require_crit_review.ReviewGuardTest.test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base) ... ok
test_base_fails_closed_when_github_metadata_is_unavailable (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_github_metadata_is_unavailable) ... ok
test_base_fails_closed_when_unresolvable_or_option_like (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_unresolvable_or_option_like) ... ok
test_base_rejects_forged_evidence_metadata (test_require_crit_review.ReviewGuardTest.test_base_rejects_forged_evidence_metadata) ... ok
test_base_rejects_pr_commits_before_executing_their_collector (test_require_crit_review.ReviewGuardTest.test_base_rejects_pr_commits_before_executing_their_collector) ... ok
test_base_rejects_side_branch_and_advanced_base_containing_pr_commits (test_require_crit_review.ReviewGuardTest.test_base_rejects_side_branch_and_advanced_base_containing_pr_commits) ... ok
test_base_requires_audit_evidence_for_a_reviewed_change (test_require_crit_review.ReviewGuardTest.test_base_requires_audit_evidence_for_a_reviewed_change) ... ok
test_base_requires_pr_feedback_evidence (test_require_crit_review.ReviewGuardTest.test_base_requires_pr_feedback_evidence) ... ok
test_base_reviews_committed_branch_changes (test_require_crit_review.ReviewGuardTest.test_base_reviews_committed_branch_changes) ... ok
test_blocked_or_missing_audit_verdict_fails (test_require_crit_review.ReviewGuardTest.test_blocked_or_missing_audit_verdict_fails) ... ok
test_broad_diff_requires_review (test_require_crit_review.ReviewGuardTest.test_broad_diff_requires_review) ... ok
test_broad_orchestration_only_pr_needs_no_audit (test_require_crit_review.ReviewGuardTest.test_broad_orchestration_only_pr_needs_no_audit) ... ok
test_companion_must_be_this_audits_own_last_message (test_require_crit_review.ReviewGuardTest.test_companion_must_be_this_audits_own_last_message) ... ok
test_explicit_disable_skips_guard (test_require_crit_review.ReviewGuardTest.test_explicit_disable_skips_guard) ... ok
test_feedback_accepts_absolute_path_through_a_repository_parent_alias (test_require_crit_review.ReviewGuardTest.test_feedback_accepts_absolute_path_through_a_repository_parent_alias) ... ok
test_feedback_cannot_hide_an_arbitrary_path_without_base (test_require_crit_review.ReviewGuardTest.test_feedback_cannot_hide_an_arbitrary_path_without_base) ... ok
test_feedback_does_not_exclude_symlink_aliases_outside_validation (test_require_crit_review.ReviewGuardTest.test_feedback_does_not_exclude_symlink_aliases_outside_validation) ... ok
test_feedback_path_itself_must_be_under_validation (test_require_crit_review.ReviewGuardTest.test_feedback_path_itself_must_be_under_validation) ... ok
test_feedback_symlink_cannot_hide_a_file_outside_validation (test_require_crit_review.ReviewGuardTest.test_feedback_symlink_cannot_hide_a_file_outside_validation) ... ok
test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent (test_require_crit_review.ReviewGuardTest.test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent) ... ok
test_github_identity_gate_activation_and_current_head_approval (test_require_crit_review.ReviewGuardTest.test_github_identity_gate_activation_and_current_head_approval) ... ok
test_github_lookup_ignores_environment_repository_override (test_require_crit_review.ReviewGuardTest.test_github_lookup_ignores_environment_repository_override) ... ok
test_github_lookup_rejects_evidence_from_another_repository (test_require_crit_review.ReviewGuardTest.test_github_lookup_rejects_evidence_from_another_repository) ... ok
test_high_risk_markdown_change_requires_review (test_require_crit_review.ReviewGuardTest.test_high_risk_markdown_change_requires_review) ... ok
test_incorrect_audit_needs_not_applicable_dispositions (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_not_applicable_dispositions) ... ok
test_incorrect_audit_without_findings_fails (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_without_findings_fails) ... ok
test_large_untracked_file_requires_broad_diff_review (test_require_crit_review.ReviewGuardTest.test_large_untracked_file_requires_broad_diff_review) ... ok
test_missing_base_collector_falls_back_only_after_binding (test_require_crit_review.ReviewGuardTest.test_missing_base_collector_falls_back_only_after_binding) ... ok
test_native_reviewed_environment_rejects_human_reviewer (test_require_crit_review.ReviewGuardTest.test_native_reviewed_environment_rejects_human_reviewer) ... ok
test_native_reviewed_without_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_native_reviewed_without_evidence_still_requires_review) ... ok
test_no_diff_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_no_diff_does_not_require_review) ... ok
test_older_base_must_not_be_on_the_head_first_parent_chain (test_require_crit_review.ReviewGuardTest.test_older_base_must_not_be_on_the_head_first_parent_chain) ... ok
test_orchestration_only_pr_needs_no_audit (test_require_crit_review.ReviewGuardTest.test_orchestration_only_pr_needs_no_audit) ... ok
test_pr_feedback_accepts_complete_evidence_without_a_bot_review (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_evidence_without_a_bot_review) ... ok
test_pr_feedback_accepts_complete_root_cause_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_root_cause_dispositions) ... ok
test_pr_feedback_bodies_are_compared_after_secret_masking (test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) ... ok
test_pr_feedback_evidence_file_is_not_counted_as_a_change (test_require_crit_review.ReviewGuardTest.test_pr_feedback_evidence_file_is_not_counted_as_a_change) ... ok
test_pr_feedback_fails_when_the_collector_cannot_run (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fails_when_the_collector_cannot_run) ... ok
test_pr_feedback_fixed_commit_must_be_in_the_pr_range (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fixed_commit_must_be_in_the_pr_range) ... ok
test_pr_feedback_matches_a_masked_path_but_not_an_edited_one (test_require_crit_review.ReviewGuardTest.test_pr_feedback_matches_a_masked_path_but_not_an_edited_one) ... ok
test_pr_feedback_must_be_collected_for_the_current_head (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_be_collected_for_the_current_head) ... ok
test_pr_feedback_must_cover_every_currently_collected_item (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_cover_every_currently_collected_item) ... ok
test_pr_feedback_rejects_evidence_outside_the_repository (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_evidence_outside_the_repository) ... ok
test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) ... ok
test_pr_feedback_requires_the_github_head_to_match (test_require_crit_review.ReviewGuardTest.test_pr_feedback_requires_the_github_head_to_match) ... ok
test_pr_feedback_uses_the_base_collector_not_the_prs_own (test_require_crit_review.ReviewGuardTest.test_pr_feedback_uses_the_base_collector_not_the_prs_own) ... ok
test_pr_feedback_without_base_is_only_format_checked (test_require_crit_review.ReviewGuardTest.test_pr_feedback_without_base_is_only_format_checked) ... ok
test_recollection_must_match_the_authenticated_repository (test_require_crit_review.ReviewGuardTest.test_recollection_must_match_the_authenticated_repository) ... ok
test_reviewed_environment_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_reviewed_environment_satisfies_required_review) ... ok
test_reviewed_with_blank_evidence_values_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_blank_evidence_values_still_requires_review) ... ok
test_reviewed_with_incomplete_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_incomplete_evidence_still_requires_review) ... ok
test_role_gate_boundary_exemption_checks_complete_committed_diff (test_require_crit_review.ReviewGuardTest.test_role_gate_boundary_exemption_checks_complete_committed_diff) ... ok
test_role_gate_boundary_rejects_cross_boundary_rename_and_empty_diff (test_require_crit_review.ReviewGuardTest.test_role_gate_boundary_rejects_cross_boundary_rename_and_empty_diff) ... ok
test_role_gate_combined_rulesets_and_unverifiable_metadata (test_require_crit_review.ReviewGuardTest.test_role_gate_combined_rulesets_and_unverifiable_metadata) ... ok
test_role_gate_requires_exact_sole_pr_bypass_actor (test_require_crit_review.ReviewGuardTest.test_role_gate_requires_exact_sole_pr_bypass_actor) ... ok
test_role_gate_update_activation_and_boundary_authorship (test_require_crit_review.ReviewGuardTest.test_role_gate_update_activation_and_boundary_authorship) ... ok
test_small_docs_only_change_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_small_docs_only_change_does_not_require_review) ... ok
test_verdict_comes_only_from_the_last_message_file (test_require_crit_review.ReviewGuardTest.test_verdict_comes_only_from_the_last_message_file) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok
test_agent_asset_update_runs_gh_extension_ensure (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_launchers_do_not_hardcode_model_ids (test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes) ... ok
test_agmsg_already_pinned_skips_download (test_runtime_health.RuntimeHealthTest.test_agmsg_already_pinned_skips_download) ... ok
test_agmsg_checksum_mismatch_fails_closed (test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed) ... ok
test_agmsg_fresh_install_populates_skill_and_records_manifest (test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest) ... ok
test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state) ... ok
test_agmsg_migration_reports_an_installer_that_mutates_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state) ... ok
test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty) ... ok
test_agmsg_refuses_to_install_without_tar (test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_without_tar) ... ok
test_agmsg_reports_an_installer_that_leaves_the_wrong_version (test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version) ... ok
test_agmsg_update_aborts_when_install_corrupts_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state) ... ok
test_agmsg_update_never_touches_teams_db_run (test_runtime_health.RuntimeHealthTest.test_agmsg_update_never_touches_teams_db_run) ... ok
test_client_bashrc_treats_private_sources_as_optional (test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... ok
test_codex_crit_normalizes_managed_marketplace_mode (test_runtime_health.RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode) ... ok
test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... ok
test_darwin_crit_checksum_failure_preserves_existing_binary (test_runtime_health.RuntimeHealthTest.test_darwin_crit_checksum_failure_preserves_existing_binary) ... ok
test_darwin_crit_install_is_pinned_atomic_and_recorded (test_runtime_health.RuntimeHealthTest.test_darwin_crit_install_is_pinned_atomic_and_recorded) ... ok
test_doctor_github_role_activation_and_file_storage (test_runtime_health.RuntimeHealthTest.test_doctor_github_role_activation_and_file_storage) ... ok
test_doctor_reports_claude_sandbox_prerequisites (test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_doctor_required_optional_and_healthy_statuses (test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_linux_crit_checksum_failure_preserves_existing_binary (test_runtime_health.RuntimeHealthTest.test_linux_crit_checksum_failure_preserves_existing_binary) ... ok
test_linux_crit_correct_version_is_download_free (test_runtime_health.RuntimeHealthTest.test_linux_crit_correct_version_is_download_free) ... ok
test_linux_crit_failure_does_not_leak_cleanup_trap (test_runtime_health.RuntimeHealthTest.test_linux_crit_failure_does_not_leak_cleanup_trap) ... ok
test_linux_crit_install_is_pinned_atomic_and_recorded (test_runtime_health.RuntimeHealthTest.test_linux_crit_install_is_pinned_atomic_and_recorded) ... ok
test_linux_crit_prefers_pinned_target_over_older_path_binary (test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_update_pulls_clean_main_before_apply (test_runtime_health.RuntimeHealthTest.test_make_update_pulls_clean_main_before_apply) ... ok
test_make_update_reports_unmerged_feature_branch_before_branch_notice (test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_feature_branch_before_branch_notice) ... ok
test_make_update_reports_unmerged_index_before_dirty_notice (test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_index_before_dirty_notice) ... ok
test_make_update_skips_dirty_main_with_manual_pull_notice (test_runtime_health.RuntimeHealthTest.test_make_update_skips_dirty_main_with_manual_pull_notice) ... ok
test_upgrade_applies_mise_only_from_successful_canonical_checkout (test_runtime_health.RuntimeHealthTest.test_upgrade_applies_mise_only_from_successful_canonical_checkout) ... ok
test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts (test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts) ... ok
test_upgrade_changes_checkout_not_live_mise_symlink_target (test_runtime_health.RuntimeHealthTest.test_upgrade_changes_checkout_not_live_mise_symlink_target) ... ok
test_upgrade_github_extensions_are_warning_only (test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_self_updates_mise_to_the_manifest_pin (test_runtime_health.RuntimeHealthTest.test_upgrade_self_updates_mise_to_the_manifest_pin) ... ok
test_upgrade_skips_unavailable_mise_self_update (test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok
test_upgrade_uses_current_mise_node_after_runtime_replacement (test_runtime_health.RuntimeHealthTest.test_upgrade_uses_current_mise_node_after_runtime_replacement)
Reject ambient npm after mise replaces the active Node runtime. ... ok
test_ci_smokes_exact_tools_with_network_denied (test_statusline_tools.StatuslineToolsTest.test_ci_smokes_exact_tools_with_network_denied) ... ok
test_direct_commands_use_offline_path_binaries (test_statusline_tools.StatuslineToolsTest.test_direct_commands_use_offline_path_binaries) ... ok
test_generated_commands_are_direct_and_static (test_statusline_tools.StatuslineToolsTest.test_generated_commands_are_direct_and_static) ... ok
test_mise_config_and_lock_pin_exact_npm_versions (test_statusline_tools.StatuslineToolsTest.test_mise_config_and_lock_pin_exact_npm_versions) ... ok
test_missing_binary_fails_immediately (test_statusline_tools.StatuslineToolsTest.test_missing_binary_fails_immediately) ... ok
test_binary_installers_replace_from_same_directory_stages (test_supply_chain_policy.SupplyChainPolicyTest.test_binary_installers_replace_from_same_directory_stages) ... ok
test_executable_downloads_are_verified_and_not_piped_to_shell (test_supply_chain_policy.SupplyChainPolicyTest.test_executable_downloads_are_verified_and_not_piped_to_shell) ... ok
test_external_checksum_failure_preserves_destination (test_supply_chain_policy.SupplyChainPolicyTest.test_external_checksum_failure_preserves_destination) ... ok
test_externals_render_without_network_discovery (test_supply_chain_policy.SupplyChainPolicyTest.test_externals_render_without_network_discovery) ... ok
test_externals_use_fixed_urls_and_checksums (test_supply_chain_policy.SupplyChainPolicyTest.test_externals_use_fixed_urls_and_checksums) ... ok
test_installer_cleanup_preserves_failure_status (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_preserves_failure_status) ... ok
test_installer_cleanup_survives_mock_function_returns (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) ... ok
test_mise_apply_replaces_live_symlinks_with_independent_copies (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_apply_replaces_live_symlinks_with_independent_copies) ... ok
test_mise_lock_matches_config_and_supported_platforms (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_matches_config_and_supported_platforms) ... ok
test_mise_lock_url_entries_have_checksums (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_url_entries_have_checksums) ... ok
test_mise_main_preserves_install_failure (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_main_preserves_install_failure) ... ok
test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts) ... ok
test_mise_versions_are_exact_and_locking_is_enforced (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_versions_are_exact_and_locking_is_enforced) ... ok
test_renovate_owns_dependency_update_notifications (test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications) ... ok
test_setup_ci_rejects_and_preserves_local_drift (test_supply_chain_policy.SupplyChainPolicyTest.test_setup_ci_rejects_and_preserves_local_drift) ... ok
test_sheldon_git_sources_have_revisions (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_git_sources_have_revisions) ... ok
test_sheldon_uses_locked_crates_io_source (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_uses_locked_crates_io_source) ... ok
test_absent_path_without_old_ref_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_absent_path_without_old_ref_is_regression) ... ok
test_chmod_only_change_keeps_the_source_unchanged_note (test_ua_symbol_coverage.UaSymbolCoverageTest.test_chmod_only_change_keeps_the_source_unchanged_note) ... ok
test_comment_lines_are_not_definitions (test_ua_symbol_coverage.UaSymbolCoverageTest.test_comment_lines_are_not_definitions) ... ok
test_def_column_reads_the_new_graph_revision (test_ua_symbol_coverage.UaSymbolCoverageTest.test_def_column_reads_the_new_graph_revision) ... ok
test_deleted_path_with_old_ref_is_explained (test_ua_symbol_coverage.UaSymbolCoverageTest.test_deleted_path_with_old_ref_is_explained) ... ok
test_flags_unexplained_symbol_loss_only (test_ua_symbol_coverage.UaSymbolCoverageTest.test_flags_unexplained_symbol_loss_only) ... ok
test_grammar_file_missing_from_graph_fails_in_covered_directories (test_ua_symbol_coverage.UaSymbolCoverageTest.test_grammar_file_missing_from_graph_fails_in_covered_directories) ... ok
test_low_similarity_move_with_no_symbols_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_low_similarity_move_with_no_symbols_is_regression) ... ok
test_partial_deletion_in_changed_source_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_partial_deletion_in_changed_source_is_regression) ... ok
test_partially_covered_new_file_is_not_flagged (test_ua_symbol_coverage.UaSymbolCoverageTest.test_partially_covered_new_file_is_not_flagged) ... ok
test_python_defs_inside_strings_do_not_count (test_ua_symbol_coverage.UaSymbolCoverageTest.test_python_defs_inside_strings_do_not_count) ... ok
test_rename_dropping_symbols_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_rename_dropping_symbols_is_regression) ... ok
test_rename_preserving_symbols_is_ok (test_ua_symbol_coverage.UaSymbolCoverageTest.test_rename_preserving_symbols_is_ok) ... ok
test_ruby_visibility_prefixed_defs_are_counted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_ruby_visibility_prefixed_defs_are_counted) ... ok
test_shell_names_with_punctuation_are_counted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_shell_names_with_punctuation_are_counted) ... ok
test_unchanged_source_loss_is_noted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unchanged_source_loss_is_noted) ... ok
test_unreadable_candidate_fails_closed (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unreadable_candidate_fails_closed) ... ok
test_unresolvable_ref_fails_closed (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unresolvable_ref_fails_closed) ... ok
test_uv_run_script_shebang_is_python (test_ua_symbol_coverage.UaSymbolCoverageTest.test_uv_run_script_shebang_is_python) ... ok
test_builds_in_the_clone_when_no_release_artifact_exists (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_builds_in_the_clone_when_no_release_artifact_exists) ... ok
test_builds_missing_core_in_the_release_artifact_then_copies_it (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_builds_missing_core_in_the_release_artifact_then_copies_it) ... ok
test_doctor_stale_warning_is_cleared_by_the_update_build (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_doctor_stale_warning_is_cleared_by_the_update_build) ... ok
test_frozen_install_failure_falls_back_to_plain_install (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_frozen_install_failure_falls_back_to_plain_install) ... ok
test_make_update_installs_the_pinned_pnpm (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_make_update_installs_the_pinned_pnpm) ... ok
test_prefers_mise_exec_over_an_unbacked_pnpm_shim (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_prefers_mise_exec_over_an_unbacked_pnpm_shim) ... ok
test_rebuilds_a_release_dist_older_than_its_sources (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_rebuilds_a_release_dist_older_than_its_sources) ... ok
test_skips_the_build_when_the_release_artifact_already_has_dist (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_skips_the_build_when_the_release_artifact_already_has_dist) ... ok
test_uses_mise_exec_when_pnpm_is_not_on_path (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_uses_mise_exec_when_pnpm_is_not_on_path) ... ok
test_uses_path_pnpm_only_when_mise_is_absent (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_uses_path_pnpm_only_when_mise_is_absent) ... ok
test_warns_and_continues_when_no_pnpm_is_resolvable (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_warns_and_continues_when_no_pnpm_is_resolvable) ... ok
test_warns_and_continues_when_the_build_fails (test_update_agent_assets_ua_core.UnderstandAnythingCoreBuildTest.test_warns_and_continues_when_the_build_fails) ... ok
test_candidate_is_no_when_another_claude_family_is_larger (test_usage_review.UsageReviewTests.test_candidate_is_no_when_another_claude_family_is_larger) ... ok
test_malformed_latest_snapshot_warns_and_never_raises (test_usage_review.UsageReviewTests.test_malformed_latest_snapshot_warns_and_never_raises) ... ok
test_report_computes_share_ratio_and_baseline_deltas (test_usage_review.UsageReviewTests.test_report_computes_share_ratio_and_baseline_deltas) ... ok
test_report_emits_due_windows_and_matching_notes_suppress_them (test_usage_review.UsageReviewTests.test_report_emits_due_windows_and_matching_notes_suppress_them) ... ok
test_snapshot_does_not_rewrite_existing_daily_file (test_usage_review.UsageReviewTests.test_snapshot_does_not_rewrite_existing_daily_file) ... ok
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... <frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff4d36d40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff4d372e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490da80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d8a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490cf40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490e890>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490f3d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d120>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490ec50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d030>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490ca90>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff4d375b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d300>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff4c69c60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490f2e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490cc70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490d210>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff490cb80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f5120>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f53f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f5030>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f4e50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f4d60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f4040>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f4c70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f4b80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f4130>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f4310>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f48b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f4400>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f4220>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f4a90>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f55d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f56c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f5990>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f5c60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f5d50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f5e40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f5f30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f6020>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f6110>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f6200>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f62f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap_external>:781: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xe5eff46f63e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_masking_keeps_the_escape_before_the_key (test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_restart_worker (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_restart_worker) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_reject_a_malformed_render_entry (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_codex_modify_script_requires_executable_source (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_hook_composition_accepts_managed_source_fixture (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_nested_git_trees_only (test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/validate-agent-assets-test-3q34z30h/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: /Users/mryfmo/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_secret_scan_allows_exact_placeholder_tokens (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_reads_json_per_key_and_string_value (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_placeholder_with_suffix (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok
test_checkout_does_not_persist_credentials_without_explicit_exemption (test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

----------------------------------------------------------------------
Ran 783 tests in 200.299s

OK

```

## /tmp/t90b-assets.log

```text
uv run --with pyyaml scripts/validate-agent-assets.py
Installed 1 package in 2ms
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles:codex-security-dot-a007 (herdr-agents --remove-worker)
agent asset validation ok

```

## /tmp/t90b-prettier-final.log

```text
Checking formatting...
All matched files use Prettier code style!

```

## /tmp/t90b-ruff.log

```text
2 files already formatted

```

## /tmp/t90b-diffcheck-final.log

```text

```

## /tmp/t90b-diffstat.log

```text
 README.md                                          | 227 +++++++++++++++++----
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   8 +-
 .../dot_config/claude/rules/agmsg-orchestration.md |   2 +-
 scripts/require-crit-review.py                     |  42 +++-
 tests/unit/test_require_crit_review.py             | 124 ++++++++++-
 5 files changed, 344 insertions(+), 59 deletions(-)

```

## /tmp/t90b-payload-check.log

```text
README payloads parse; integrity has zero bypass actors and seven strict checks; merge control has exactly User11512262 PR-only bypass, update=false, approval=1; both target main.

```

## /tmp/t90b-gate.log

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.

```

## /tmp/t90b-prettier-final.log

```text
Checking formatting...
All matched files use Prettier code style!

```

## /tmp/t90b-diffstat.log

```text
 README.md                                          | 227 +++++++++++++++++----
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   8 +-
 .../dot_config/claude/rules/agmsg-orchestration.md |   4 +-
 scripts/require-crit-review.py                     |  42 +++-
 tests/unit/test_require_crit_review.py             | 124 ++++++++++-
 5 files changed, 345 insertions(+), 60 deletions(-)

```

## /tmp/t90b-commit.log

```text
[feat/ruleset-sole-merger 5db32001] feat: restrict main merges to the orchestrator identity
 5 files changed, 345 insertions(+), 60 deletions(-)
5db320019d4c63f31eed9bfc1cea88ddade0a7cb

```

## /tmp/t90b-push.log

```text
remote: 
remote: Create a pull request for 'feat/ruleset-sole-merger' on GitHub by visiting:        
remote:      https://github.com/mryfmo/dotfiles/pull/new/feat/ruleset-sole-merger        
remote: 
To github.com:mryfmo/dotfiles.git
 * [new branch]        feat/ruleset-sole-merger -> feat/ruleset-sole-merger

```

## /tmp/t90b-pr-create.log

```text
https://github.com/mryfmo/dotfiles/pull/265

```

## PR creation metadata

```json
{"baseRefOid":"4c38dea07ff2cf448909c0773f6e8332930be090","headRefOid":"5db320019d4c63f31eed9bfc1cea88ddade0a7cb","mergeStateStatus":"BLOCKED","mergeable":"MERGEABLE","url":"https://github.com/mryfmo/dotfiles/pull/265"}

```

## /tmp/t90b-assets-final.log

```text
uv run --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles:codex-security-dot-a007 (herdr-agents --remove-worker)
agent asset validation ok

```

## /tmp/t90b-ci.log

```text
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
test (macos-14, client)	pass	6m33s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
test (macos-14, client)	pass	6m33s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
test (macos-14, client)	pass	6m33s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
test (macos-14, client)	pass	6m33s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
test (macos-14, client)	pass	6m33s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pass	7m35s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (macos-14, client)	pass	6m33s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-26.04, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pass	7m35s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (macos-14, client)	pass	6m33s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-26.04, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pass	7m35s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (macos-14, client)	pass	6m33s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-26.04, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pass	7m35s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (macos-14, client)	pass	6m33s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
test (ubuntu-24.04, client)	pass	8m0s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-26.04, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pass	7m35s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (macos-14, client)	pass	6m33s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
test (ubuntu-24.04, client)	pass	8m0s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-26.04, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	

```

## /tmp/t90b-ci-final.log

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503460859	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460920	
private-bootstrap (ubuntu-24.04, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460753	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460935	
public-bootstrap (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460926	
public-bootstrap (ubuntu-24.04, client)	pass	7m41s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460933	
public-bootstrap (ubuntu-24.04, server)	pass	7m35s	https://github.com/mryfmo/dotfiles/actions/runs/37225251308/job/111503460998	
test (macos-14, client)	pass	6m33s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488353	
test (ubuntu-24.04, client)	pass	8m0s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488317	
test (ubuntu-24.04, server)	pass	4m48s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488540	
test (ubuntu-26.04, client)	pass	7m28s	https://github.com/mryfmo/dotfiles/actions/runs/37225251325/job/111503488365	
validate	pass	25s	https://github.com/mryfmo/dotfiles/actions/runs/37225251268/job/111503460600	

```

## /tmp/t90b-mergeable-final.json

```json
{"base":"4c38dea07ff2cf448909c0773f6e8332930be090","head":"5db320019d4c63f31eed9bfc1cea88ddade0a7cb","mergeable":true,"mergeable_state":"clean","number":265}

```

## /tmp/t90b-ci-progress.json

```json
{"jobs":[{"name":"changes","status":"completed","step":null},{"name":"test (ubuntu-24.04, client)","status":"in_progress","step":"Run Python unit tests"},{"name":"test (macos-14, client)","status":"in_progress","step":"Run Python unit tests"},{"name":"test (ubuntu-26.04, client)","status":"in_progress","step":"Run Python unit tests"},{"name":"test (ubuntu-24.04, server)","status":"in_progress","step":"Run Python unit tests"}],"status":"in_progress"}

```

## /tmp/t90b-gate-final.log

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.

```

## /tmp/t90b-bot.log

```text
Diff head: 5db320019d4c63f31eed9bfc1cea88ddade0a7cb
Wait started: 2026-10-04T18:39:32.744634+00:00
bot: none (15-minute bounded wait)
Wait finished: 2026-10-04T18:54:33.631613+00:00

```

## /tmp/t90b-threads-final.json

```json
{"data":{"repository":{"pullRequest":{"reviewThreads":{"pageInfo":{"hasNextPage":false},"nodes":[]}}}}}
```

## /tmp/t90b-mergeable-final.json

```json
{"base":"4c38dea07ff2cf448909c0773f6e8332930be090","head":"5db320019d4c63f31eed9bfc1cea88ddade0a7cb","mergeable":true,"mergeable_state":"clean","number":265}

```

## Final artifact validation

```text
uv run --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-507e9c1.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90-github-identity-separation-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T90b-ruleset-sole-merger-a01.md
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles:codex-security-dot-a007 (herdr-agents --remove-worker)
agent asset validation ok

```
