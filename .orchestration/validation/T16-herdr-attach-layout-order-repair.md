# T16 validation evidence

All commands ran from `/Users/mryfmo/Workspace/dotfiles` on
`feat/herdr-attach-order-repair`.

## `uv run python -m unittest tests.unit.test_herdr_agents -v`

Exit code: 0

```text
test_attach_ambiguous_files_panes_skip_repair (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_ambiguous_files_panes_skip_repair) ... ok
test_attach_builds_files_then_codex_around_current_claude_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_builds_files_then_codex_around_current_claude_pane) ... ok
test_attach_complete_workspace_is_idempotent (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_complete_workspace_is_idempotent) ... ok
test_attach_correct_order_does_not_swap (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_correct_order_does_not_swap) ... ok
test_attach_noops_for_full_mode_managed_layout (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_noops_for_full_mode_managed_layout) ... ok
test_attach_noops_without_herdr_environment (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_noops_without_herdr_environment) ... ok
test_attach_repairs_files_claude_codex_order (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_repairs_files_claude_codex_order) ... ok
test_bare_herdr_in_ghostty_starts_plain_session (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bare_herdr_in_ghostty_starts_plain_session) ... ok
test_bare_herdr_outside_ghostty_uses_real_cli (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bare_herdr_outside_ghostty_uses_real_cli) ... ok
test_claude_repair_skips_just_restarted_codex_pane_without_agent_field (tests.unit.test_herdr_agents.HerdrAgentsTest.test_claude_repair_skips_just_restarted_codex_pane_without_agent_field) ... ok
test_claude_settings_add_herdr_attach_session_hook (tests.unit.test_herdr_agents.HerdrAgentsTest.test_claude_settings_add_herdr_attach_session_hook) ... ok
test_duplicate_files_panes_fail_without_mutation (tests.unit.test_herdr_agents.HerdrAgentsTest.test_duplicate_files_panes_fail_without_mutation) ... ok
test_existing_agents_workspace_focuses_without_recreating_agents (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_agents_workspace_focuses_without_recreating_agents) ... ok
test_existing_empty_files_pane_restarts_yazi_in_place (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_empty_files_pane_restarts_yazi_in_place) ... ok
test_existing_files_pane_is_not_reused_for_claude_or_split_again (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_files_pane_is_not_reused_for_claude_or_split_again) ... ok
test_existing_files_pane_with_other_process_restarts_yazi_in_place (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_files_pane_with_other_process_restarts_yazi_in_place) ... ok
test_existing_workspace_adds_missing_files_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_workspace_adds_missing_files_pane) ... ok
test_existing_workspace_restarts_missing_claude_in_empty_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_claude_in_empty_pane) ... ok
test_existing_workspace_restarts_missing_codex_agent (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_codex_agent) ... ok
test_existing_workspace_splits_when_missing_claude_has_no_empty_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_workspace_splits_when_missing_claude_has_no_empty_pane) ... ok
test_files_pane_inspection_failures_do_not_start_yazi (tests.unit.test_herdr_agents.HerdrAgentsTest.test_files_pane_inspection_failures_do_not_start_yazi) ... ok
test_files_pane_operations_propagate_failures (tests.unit.test_herdr_agents.HerdrAgentsTest.test_files_pane_operations_propagate_failures) ... ok
test_ghostty_config_does_not_auto_start_herdr_session (tests.unit.test_herdr_agents.HerdrAgentsTest.test_ghostty_config_does_not_auto_start_herdr_session) ... ok
test_ghostty_herdr_starts_plain_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_ghostty_herdr_starts_plain_workspace) ... ok
test_herdr_prefix_alt_a_runs_helper_from_active_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_alt_a_runs_helper_from_active_pane) ... ok
test_herdr_session_does_not_prebuild_agent_layout (tests.unit.test_herdr_agents.HerdrAgentsTest.test_herdr_session_does_not_prebuild_agent_layout) ... ok
test_herdr_session_execs_herdr_without_prebuilding_agents (tests.unit.test_herdr_agents.HerdrAgentsTest.test_herdr_session_execs_herdr_without_prebuilding_agents) ... ok
test_herdr_session_passes_syntax_check (tests.unit.test_herdr_agents.HerdrAgentsTest.test_herdr_session_passes_syntax_check) ... ok
test_herdr_session_rejects_arguments (tests.unit.test_herdr_agents.HerdrAgentsTest.test_herdr_session_rejects_arguments) ... ok
test_herdr_with_args_in_ghostty_uses_real_cli (tests.unit.test_herdr_agents.HerdrAgentsTest.test_herdr_with_args_in_ghostty_uses_real_cli) ... ok
test_interactive_ghostty_shell_attaches_plain_session (tests.unit.test_herdr_agents.HerdrAgentsTest.test_interactive_ghostty_shell_attaches_plain_session) ... ok
test_missing_yazi_fails_before_mutating_a_new_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_missing_yazi_fails_before_mutating_a_new_workspace) ... ok
test_missing_yazi_fails_before_mutating_an_existing_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_missing_yazi_fails_before_mutating_an_existing_workspace) ... ok
test_uses_initial_workspace_pane_for_claude_and_splits_codex_right (tests.unit.test_herdr_agents.HerdrAgentsTest.test_uses_initial_workspace_pane_for_claude_and_splits_codex_right) ... ok
test_yazi_edit_opener_prefers_zed_with_editor_fallback (tests.unit.test_herdr_agents.HerdrAgentsTest.test_yazi_edit_opener_prefers_zed_with_editor_fallback) ... ok
test_zprofile_adds_common_bin_to_login_shell_path (tests.unit.test_herdr_agents.HerdrAgentsTest.test_zprofile_adds_common_bin_to_login_shell_path) ... ok

----------------------------------------------------------------------
Ran 36 tests in 2.717s

OK
```

## `make unit-test`

Exit code: 0

```text
uv run python -m unittest discover -s tests/unit -v
```

Complete discovered-test output:

```text
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
test_content_drift_still_fails (test_check_agent_runtime.CheckAgentRuntimeTest.test_content_drift_still_fails) ... ok
test_executable_prefix_is_compared_against_deployed_name (test_check_agent_runtime.CheckAgentRuntimeTest.test_executable_prefix_is_compared_against_deployed_name) ... ok
test_executable_prefix_requires_deployed_execute_bit (test_check_agent_runtime.CheckAgentRuntimeTest.test_executable_prefix_requires_deployed_execute_bit) ... ok
test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode (test_check_agent_runtime.CheckAgentRuntimeTest.test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode) ... ok
test_private_prefix_is_compared_against_deployed_name (test_check_agent_runtime.CheckAgentRuntimeTest.test_private_prefix_is_compared_against_deployed_name) ... ok
test_unexpected_non_runtime_file_still_fails (test_check_agent_runtime.CheckAgentRuntimeTest.test_unexpected_non_runtime_file_still_fails) ... ok
test_unmanaged_top_level_skill_dir_warns (test_check_agent_runtime.CheckAgentRuntimeTest.test_unmanaged_top_level_skill_dir_warns) ... ok
test_current_only_key_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_only_key_is_preserved) ... ok
test_desired_current_output_is_byte_identical (test_claude_settings_merge.ClaudeSettingsMergeTest.test_desired_current_output_is_byte_identical) ... ok
test_empty_stdin_outputs_managed (test_claude_settings_merge.ClaudeSettingsMergeTest.test_empty_stdin_outputs_managed) ... ok
test_enabled_plugins_are_preserved_from_current (test_claude_settings_merge.ClaudeSettingsMergeTest.test_enabled_plugins_are_preserved_from_current) ... ok
test_invalid_json_outputs_managed (test_claude_settings_merge.ClaudeSettingsMergeTest.test_invalid_json_outputs_managed) ... ok
test_managed_wins_for_managed_key (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_wins_for_managed_key) ... ok
test_merge_is_idempotent (test_claude_settings_merge.ClaudeSettingsMergeTest.test_merge_is_idempotent) ... ok
test_real_value_change_is_redumped (test_claude_settings_merge.ClaudeSettingsMergeTest.test_real_value_change_is_redumped) ... ok
test_reordered_but_equal_current_is_byte_identical (test_claude_settings_merge.ClaudeSettingsMergeTest.test_reordered_but_equal_current_is_byte_identical) ... ok
test_trailing_newline (test_claude_settings_merge.ClaudeSettingsMergeTest.test_trailing_newline) ... ok
test_current_only_runtime_tables_keep_current_group_order (test_codex_config_merge.CodexConfigMergeTest.test_current_only_runtime_tables_keep_current_group_order) ... ok
test_fresh_machine_outputs_managed_baseline (test_codex_config_merge.CodexConfigMergeTest.test_fresh_machine_outputs_managed_baseline) ... ok
test_managed_templates_are_rendered_before_merge (test_codex_config_merge.CodexConfigMergeTest.test_managed_templates_are_rendered_before_merge) ... ok
test_managed_wins_for_managed_keys (test_codex_config_merge.CodexConfigMergeTest.test_managed_wins_for_managed_keys) ... ok
test_runtime_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_are_preserved) ... ok
test_runtime_tables_seed_from_managed_when_absent (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_seed_from_managed_when_absent) ... ok
test_unknown_current_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_unknown_current_tables_are_preserved) ... ok
test_coverage_gems_are_compatible_and_exact (test_files_fixture.FilesFixtureTest.test_coverage_gems_are_compatible_and_exact) ... ok
test_fixture_uses_chezmoi_binary_outside_mise_shims (test_files_fixture.FilesFixtureTest.test_fixture_uses_chezmoi_binary_outside_mise_shims) ... ok
test_legacy_file_workflows_initialize_required_fixture_paths (test_files_fixture.FilesFixtureTest.test_legacy_file_workflows_initialize_required_fixture_paths) ... ok
test_claude_settings_renders_session_start_hooks (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_expected_outputs_uses_codex_baseline_path (test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
test_attach_ambiguous_files_panes_skip_repair (test_herdr_agents.HerdrAgentsTest.test_attach_ambiguous_files_panes_skip_repair) ... ok
test_attach_builds_files_then_codex_around_current_claude_pane (test_herdr_agents.HerdrAgentsTest.test_attach_builds_files_then_codex_around_current_claude_pane) ... ok
test_attach_complete_workspace_is_idempotent (test_herdr_agents.HerdrAgentsTest.test_attach_complete_workspace_is_idempotent) ... ok
test_attach_correct_order_does_not_swap (test_herdr_agents.HerdrAgentsTest.test_attach_correct_order_does_not_swap) ... ok
test_attach_noops_for_full_mode_managed_layout (test_herdr_agents.HerdrAgentsTest.test_attach_noops_for_full_mode_managed_layout) ... ok
test_attach_noops_without_herdr_environment (test_herdr_agents.HerdrAgentsTest.test_attach_noops_without_herdr_environment) ... ok
test_attach_repairs_files_claude_codex_order (test_herdr_agents.HerdrAgentsTest.test_attach_repairs_files_claude_codex_order) ... ok
test_bare_herdr_in_ghostty_starts_plain_session (test_herdr_agents.HerdrAgentsTest.test_bare_herdr_in_ghostty_starts_plain_session) ... ok
test_bare_herdr_outside_ghostty_uses_real_cli (test_herdr_agents.HerdrAgentsTest.test_bare_herdr_outside_ghostty_uses_real_cli) ... ok
test_claude_repair_skips_just_restarted_codex_pane_without_agent_field (test_herdr_agents.HerdrAgentsTest.test_claude_repair_skips_just_restarted_codex_pane_without_agent_field) ... ok
test_claude_settings_add_herdr_attach_session_hook (test_herdr_agents.HerdrAgentsTest.test_claude_settings_add_herdr_attach_session_hook) ... ok
test_duplicate_files_panes_fail_without_mutation (test_herdr_agents.HerdrAgentsTest.test_duplicate_files_panes_fail_without_mutation) ... ok
test_existing_agents_workspace_focuses_without_recreating_agents (test_herdr_agents.HerdrAgentsTest.test_existing_agents_workspace_focuses_without_recreating_agents) ... ok
test_existing_empty_files_pane_restarts_yazi_in_place (test_herdr_agents.HerdrAgentsTest.test_existing_empty_files_pane_restarts_yazi_in_place) ... ok
test_existing_files_pane_is_not_reused_for_claude_or_split_again (test_herdr_agents.HerdrAgentsTest.test_existing_files_pane_is_not_reused_for_claude_or_split_again) ... ok
test_existing_files_pane_with_other_process_restarts_yazi_in_place (test_herdr_agents.HerdrAgentsTest.test_existing_files_pane_with_other_process_restarts_yazi_in_place) ... ok
test_existing_workspace_adds_missing_files_pane (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_adds_missing_files_pane) ... ok
test_existing_workspace_restarts_missing_claude_in_empty_pane (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_claude_in_empty_pane) ... ok
test_existing_workspace_restarts_missing_codex_agent (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_codex_agent) ... ok
test_existing_workspace_splits_when_missing_claude_has_no_empty_pane (test_herdr_agents.HerdrAgentsTest.test_existing_workspace_splits_when_missing_claude_has_no_empty_pane) ... ok
test_files_pane_inspection_failures_do_not_start_yazi (test_herdr_agents.HerdrAgentsTest.test_files_pane_inspection_failures_do_not_start_yazi) ... ok
test_files_pane_operations_propagate_failures (test_herdr_agents.HerdrAgentsTest.test_files_pane_operations_propagate_failures) ... ok
test_ghostty_config_does_not_auto_start_herdr_session (test_herdr_agents.HerdrAgentsTest.test_ghostty_config_does_not_auto_start_herdr_session) ... ok
test_ghostty_herdr_starts_plain_workspace (test_herdr_agents.HerdrAgentsTest.test_ghostty_herdr_starts_plain_workspace) ... ok
test_herdr_prefix_alt_a_runs_helper_from_active_pane (test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_alt_a_runs_helper_from_active_pane) ... ok
test_herdr_session_does_not_prebuild_agent_layout (test_herdr_agents.HerdrAgentsTest.test_herdr_session_does_not_prebuild_agent_layout) ... ok
test_herdr_session_execs_herdr_without_prebuilding_agents (test_herdr_agents.HerdrAgentsTest.test_herdr_session_execs_herdr_without_prebuilding_agents) ... ok
test_herdr_session_passes_syntax_check (test_herdr_agents.HerdrAgentsTest.test_herdr_session_passes_syntax_check) ... ok
test_herdr_session_rejects_arguments (test_herdr_agents.HerdrAgentsTest.test_herdr_session_rejects_arguments) ... ok
test_herdr_with_args_in_ghostty_uses_real_cli (test_herdr_agents.HerdrAgentsTest.test_herdr_with_args_in_ghostty_uses_real_cli) ... ok
test_interactive_ghostty_shell_attaches_plain_session (test_herdr_agents.HerdrAgentsTest.test_interactive_ghostty_shell_attaches_plain_session) ... ok
test_missing_yazi_fails_before_mutating_a_new_workspace (test_herdr_agents.HerdrAgentsTest.test_missing_yazi_fails_before_mutating_a_new_workspace) ... ok
test_missing_yazi_fails_before_mutating_an_existing_workspace (test_herdr_agents.HerdrAgentsTest.test_missing_yazi_fails_before_mutating_an_existing_workspace) ... ok
test_uses_initial_workspace_pane_for_claude_and_splits_codex_right (test_herdr_agents.HerdrAgentsTest.test_uses_initial_workspace_pane_for_claude_and_splits_codex_right) ... ok
test_yazi_edit_opener_prefers_zed_with_editor_fallback (test_herdr_agents.HerdrAgentsTest.test_yazi_edit_opener_prefers_zed_with_editor_fallback) ... ok
test_zprofile_adds_common_bin_to_login_shell_path (test_herdr_agents.HerdrAgentsTest.test_zprofile_adds_common_bin_to_login_shell_path) ... ok
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
test_broad_diff_requires_review (test_require_crit_review.ReviewGuardTest.test_broad_diff_requires_review) ... ok
test_explicit_disable_skips_guard (test_require_crit_review.ReviewGuardTest.test_explicit_disable_skips_guard) ... ok
test_high_risk_markdown_change_requires_review (test_require_crit_review.ReviewGuardTest.test_high_risk_markdown_change_requires_review) ... ok
test_large_untracked_file_requires_broad_diff_review (test_require_crit_review.ReviewGuardTest.test_large_untracked_file_requires_broad_diff_review) ... ok
test_native_reviewed_environment_rejects_human_reviewer (test_require_crit_review.ReviewGuardTest.test_native_reviewed_environment_rejects_human_reviewer) ... ok
test_native_reviewed_without_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_native_reviewed_without_evidence_still_requires_review) ... ok
test_no_diff_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_no_diff_does_not_require_review) ... ok
test_reviewed_environment_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_reviewed_environment_satisfies_required_review) ... ok
test_reviewed_with_blank_evidence_values_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_blank_evidence_values_still_requires_review) ... ok
test_reviewed_with_incomplete_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_incomplete_evidence_still_requires_review) ... ok
test_small_docs_only_change_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_small_docs_only_change_does_not_require_review) ... ok
test_agent_fanout_preserves_caller_umask_for_child_agents (test_runtime_health.RuntimeHealthTest.test_agent_fanout_preserves_caller_umask_for_child_agents) ... ok
test_agent_fanout_refuses_symlink_artifacts (test_runtime_health.RuntimeHealthTest.test_agent_fanout_refuses_symlink_artifacts) ... ok
test_agent_fanout_restricts_preexisting_output_artifacts (test_runtime_health.RuntimeHealthTest.test_agent_fanout_restricts_preexisting_output_artifacts) ... ok
test_agent_runs_are_private_and_ignored (test_runtime_health.RuntimeHealthTest.test_agent_runs_are_private_and_ignored) ... ok
test_doctor_required_optional_and_healthy_statuses (test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_upgrade_github_extensions_are_warning_only (test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_skips_unavailable_mise_self_update (test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok
test_ci_smokes_exact_tools_with_network_denied (test_statusline_tools.StatuslineToolsTest.test_ci_smokes_exact_tools_with_network_denied) ... ok
test_direct_commands_use_offline_path_binaries (test_statusline_tools.StatuslineToolsTest.test_direct_commands_use_offline_path_binaries) ... ok
test_generated_commands_are_direct_and_static (test_statusline_tools.StatuslineToolsTest.test_generated_commands_are_direct_and_static) ... ok
test_mise_config_and_lock_pin_exact_npm_versions (test_statusline_tools.StatuslineToolsTest.test_mise_config_and_lock_pin_exact_npm_versions) ... ok
test_missing_binary_fails_immediately (test_statusline_tools.StatuslineToolsTest.test_missing_binary_fails_immediately) ... ok
test_binary_installers_replace_from_same_directory_stages (test_supply_chain_policy.SupplyChainPolicyTest.test_binary_installers_replace_from_same_directory_stages) ... ok
test_dependabot_owns_github_action_updates (test_supply_chain_policy.SupplyChainPolicyTest.test_dependabot_owns_github_action_updates) ... ok
test_executable_downloads_are_verified_and_not_piped_to_shell (test_supply_chain_policy.SupplyChainPolicyTest.test_executable_downloads_are_verified_and_not_piped_to_shell) ... ok
test_external_checksum_failure_preserves_destination (test_supply_chain_policy.SupplyChainPolicyTest.test_external_checksum_failure_preserves_destination) ... ok
test_externals_render_without_network_discovery (test_supply_chain_policy.SupplyChainPolicyTest.test_externals_render_without_network_discovery) ... ok
test_externals_use_fixed_urls_and_checksums (test_supply_chain_policy.SupplyChainPolicyTest.test_externals_use_fixed_urls_and_checksums) ... ok
test_installer_cleanup_preserves_failure_status (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_preserves_failure_status) ... ok
test_installer_cleanup_survives_mock_function_returns (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) ... ok
test_mise_lock_matches_config_and_supported_platforms (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_matches_config_and_supported_platforms) ... ok
test_mise_lock_url_entries_have_checksums (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_url_entries_have_checksums) ... ok
test_mise_main_preserves_install_failure (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_main_preserves_install_failure) ... ok
test_mise_versions_are_exact_and_locking_is_enforced (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_versions_are_exact_and_locking_is_enforced) ... ok
test_nix_inputs_lock_and_ci_use_2605 (test_supply_chain_policy.SupplyChainPolicyTest.test_nix_inputs_lock_and_ci_use_2605) ... ok
test_setup_ci_rejects_and_preserves_local_drift (test_supply_chain_policy.SupplyChainPolicyTest.test_setup_ci_rejects_and_preserves_local_drift) ... ok
test_sheldon_git_sources_have_revisions (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_git_sources_have_revisions) ... ok
test_sheldon_uses_locked_crates_io_source (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_uses_locked_crates_io_source) ... ok
test_agmsg_script_modes_accept_prefixed_entrypoints_and_lib_helpers (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_script_modes_accept_prefixed_entrypoints_and_lib_helpers) ... ok
test_agmsg_script_modes_reject_non_executable_prefixed_entrypoint (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_script_modes_reject_non_executable_prefixed_entrypoint) ... ok
test_agmsg_script_modes_reject_unprefixed_direct_entrypoint (test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_script_modes_reject_unprefixed_direct_entrypoint) ... ok
test_codex_modify_script_requires_executable_source (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_secret_scan_allows_exact_placeholder_tokens (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_rejects_placeholder_with_suffix (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_checkout_does_not_persist_credentials_without_explicit_exemption (test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

----------------------------------------------------------------------
Ran 153 tests in 13.918s

OK
```

## `uv run --with pyyaml scripts/validate-agent-assets.py`

Exit code: 0

```text
agent asset validation ok
```

## `shellcheck home/dot_local/bin/common/executable_herdr-agents`

Availability: available. Exit code: 0.

```text
```

## `bash -n home/dot_local/bin/common/executable_herdr-agents`

Exit code: 0.

```text
```

## `git status --short`

Exit code: 0. Task-owned paths are marked with `# T16`; all remaining entries
were documented by the orchestrator as pre-existing and were not modified by
this worker.

```text
 M home/dot_local/bin/common/executable_herdr-agents # T16
 M home/dot_mise/config.toml
 M home/dot_mise/mise.lock
 M tests/unit/test_herdr_agents.py # T16
?? .orchestration/acceptance/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/acceptance/T13-agmsg-orchestration-rule-file.md
?? .orchestration/acceptance/T14-t13-pr-lifecycle.md
?? .orchestration/acceptance/T15-herdr-lazy-start-attach-layout.md
?? .orchestration/acceptance/plan-001.md
?? .orchestration/acceptance/plan-002.md
?? .orchestration/acceptance/plan-003-final-pr.md
?? .orchestration/acceptance/plan-003-review-round-1.md
?? .orchestration/acceptance/plan-003-review-round-2.md
?? .orchestration/acceptance/plan-003.md
?? .orchestration/autoskill/runs/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/autoskill/runs/T13-agmsg-orchestration-rule-file.md
?? .orchestration/autoskill/runs/T14-t13-pr-lifecycle.md
?? .orchestration/autoskill/runs/T15-herdr-lazy-start-attach-layout.md
?? .orchestration/autoskill/runs/T16-herdr-attach-layout-order-repair.md # T16
?? .orchestration/autoskill/runs/plan-001.md
?? .orchestration/autoskill/runs/plan-002.md
?? .orchestration/autoskill/runs/plan-003.md
?? .orchestration/learning/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/learning/T13-agmsg-orchestration-rule-file.md
?? .orchestration/learning/T14-t13-pr-lifecycle.md
?? .orchestration/learning/T15-herdr-lazy-start-attach-layout.md
?? .orchestration/learning/T16-herdr-attach-layout-order-repair.md # T16
?? .orchestration/learning/plan-001.md
?? .orchestration/learning/plan-002.md
?? .orchestration/learning/plan-003.md
?? .orchestration/learning/plan-004.md
?? .orchestration/reports/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/reports/T13-agmsg-orchestration-rule-file.md
?? .orchestration/reports/T14-t13-pr-lifecycle.md
?? .orchestration/reports/T15-herdr-lazy-start-attach-layout.md
?? .orchestration/reports/T16-herdr-attach-layout-order-repair.md # T16
?? .orchestration/reports/plan-001.md
?? .orchestration/reports/plan-002.md
?? .orchestration/reports/plan-003.md
?? .orchestration/reports/plan-004-inventory.md
?? .orchestration/reports/plan-004-stop.md
?? .orchestration/reports/plan-004.md
?? .orchestration/sandboxes/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/sandboxes/T13-agmsg-orchestration-rule-file.md
?? .orchestration/sandboxes/T14-t13-pr-lifecycle.md
?? .orchestration/sandboxes/T15-herdr-lazy-start-attach-layout.md
?? .orchestration/sandboxes/T16-herdr-attach-layout-order-repair.md # T16
?? .orchestration/sandboxes/plan-001.md
?? .orchestration/sandboxes/plan-002.md
?? .orchestration/sandboxes/plan-003.md
?? .orchestration/sandboxes/plan-004.md
?? .orchestration/tasks/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/tasks/T13-agmsg-orchestration-rule-file.md
?? .orchestration/tasks/T14-t13-pr-lifecycle.md
?? .orchestration/tasks/T15-herdr-lazy-start-attach-layout.md
?? .orchestration/tasks/T16-herdr-attach-layout-order-repair.md
?? .orchestration/tasks/T17-herdr-attach-agmsg-bootstrap.md
?? .orchestration/tasks/plan-001.md
?? .orchestration/tasks/plan-002.md
?? .orchestration/tasks/plan-003.md
?? .orchestration/validation/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/validation/T13-agmsg-orchestration-rule-file.md
?? .orchestration/validation/T14-t13-pr-lifecycle.md
?? .orchestration/validation/T15-V1-verify.md
?? .orchestration/validation/T15-herdr-lazy-start-attach-layout.md
?? .orchestration/validation/T16-herdr-attach-layout-order-repair.md # T16
?? .orchestration/validation/plan-001.md
?? .orchestration/validation/plan-002-crit-comments.json
?? .orchestration/validation/plan-002-crit-structure.json
?? .orchestration/validation/plan-002.md
?? .orchestration/validation/plan-003-pr-final.md
?? .orchestration/validation/plan-003.md
?? .orchestration/validation/plan-004.md
?? docs/verification/
?? plans/
```

## Additional test-first evidence

Before implementation, the three new tests were run alone. The wrong-order
case failed because no swaps were emitted, and the duplicate-files case failed
because attach exited 1. After implementation the same command passed all
three tests.

## `make require-crit-review`

Exit code: 2 (review required; expected at worker handoff).

```text
Native agent review required before completion.
- review-sensitive path changed: .orchestration/acceptance/T11-agmsg-join-unique-identity-guard.md
- broad diff touches 80 files
- broad diff changes 6373 lines
Use the active agent's review path, not a browser by default:
- Codex: retrieve Crit comments/status data, review it inside the task, then address findings.
- Claude Code: retrieve Crit comments/status data, review it inside the task, then address findings.
- Use browser Crit review only when the user explicitly asks for Crit web UI or Crit data is unavailable.
Record a receipt with `review_surface:`, `reviewer:`, and `review_outcome:`.
For agent judgment, locate the review with `crit status --json`, then save `crit comments --all --json <review.json>` to a repo-local JSON file.
Evidence must contain at least one resolved record; for a finding-free review, add and resolve one review-scope approval record.
This local evidence is process evidence, not reviewer authentication.
Then use `review_surface: crit-data`, `reviewer: codex` or `reviewer: claude-code`, and `review_source: <json path>`.
After addressing review feedback, rerun with AGENT_REVIEWED=1 or CRIT_REVIEWED=1 plus REVIEW_EVIDENCE=<path>.
make: *** [require-crit-review] Error 1
```

The gate evaluated the orchestrator-documented pre-existing dirty worktree,
not a clean T16-only diff. Creating Crit evidence outside the task's
`allowed_files` is forbidden, and the worker protocol explicitly hands off
`ready_for_review`.

## Revision validation after `AGMSG-ACCEPTANCE status=revise`

Test-first failure:

```text
test_attach_ignores_extra_panes_on_other_tabs ... FAIL
AssertionError: 'pane rename w-attach:p1 claude-orchestrator' not found in
['pane list --workspace w-attach', 'agent get codex-worker-w-attach']
Ran 1 test in 0.045s
FAILED (failures=1)
```

After filtering the workspace pane list to the current Claude pane's tab:

```text
test_attach_ignores_extra_panes_on_other_tabs ... ok
Ran 1 test in 0.125s
OK
```

Re-run results:

```text
$ uv run python -m unittest tests.unit.test_herdr_agents -v
Ran 37 tests in 3.221s
OK

$ make unit-test
uv run python -m unittest discover -s tests/unit -v
Ran 154 tests in 13.722s
OK

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok

$ shellcheck home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output

$ bash -n home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output

$ git diff --check
# exit 0, no output
```

`make require-crit-review` was re-run after this revision and again requested
orchestrator review for the shared pre-existing 80-file worktree (6602 lines).

The complete verbose output remained identical to the transcripts above except
for the added passing
`test_attach_ignores_extra_panes_on_other_tabs` line and totals increasing from
36/153 to 37/154.

`make require-crit-review` was re-run after the revision and again requested
orchestrator review because the shared pre-existing worktree spans 80 files
(6535 lines). No out-of-scope Crit evidence was created.

## Second revision validation: rename stdout pollution

After the fake Herdr `pane rename` began returning realistic JSON, the
pre-existing restarted-Codex regression failed before the implementation fix:

```text
test_claude_repair_skips_just_restarted_codex_pane_without_agent_field ... FAIL
AssertionError: 1 != 0 :
{"id":"cli:pane:rename","result":{"pane":{"pane_id":"w-old:p2"}}}
Unable to read files pane id from:
{"id":"cli:pane:split","result":{"pane":{"pane_id":"{"id":p3"}}}
Ran 1 test in 0.119s
FAILED (failures=1)
```

After redirecting `start_codex_agent`'s rename stdout:

```text
test_claude_repair_skips_just_restarted_codex_pane_without_agent_field ... ok
Ran 1 test in 0.170s
OK

$ uv run python -m unittest tests.unit.test_herdr_agents -v
Ran 37 tests in 3.366s
OK

$ make unit-test
Ran 154 tests in 14.987s
OK

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok

$ shellcheck home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output

$ bash -n home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output

$ git diff --check
# exit 0, no output
```
