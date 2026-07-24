# T15 validation evidence

## Required commands

### `uv run python -m unittest tests.unit.test_herdr_agents -v`

Exit: 0

```text
test_attach_builds_files_then_codex_around_current_claude_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_builds_files_then_codex_around_current_claude_pane) ... ok
test_attach_complete_workspace_is_idempotent (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_complete_workspace_is_idempotent) ... ok
test_attach_noops_without_herdr_environment (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_noops_without_herdr_environment) ... ok
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
Ran 32 tests in 2.163s

OK
```

### `make unit-test`

Exit: 0

```text
uv run python -m unittest discover -s tests/unit -v
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
test_attach_builds_files_then_codex_around_current_claude_pane (test_herdr_agents.HerdrAgentsTest.test_attach_builds_files_then_codex_around_current_claude_pane) ... ok
test_attach_complete_workspace_is_idempotent (test_herdr_agents.HerdrAgentsTest.test_attach_complete_workspace_is_idempotent) ... ok
test_attach_noops_without_herdr_environment (test_herdr_agents.HerdrAgentsTest.test_attach_noops_without_herdr_environment) ... ok
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
Ran 149 tests in 12.246s

OK
```

### `uv run --with pyyaml scripts/validate-agent-assets.py`

Exit: 0

```text
agent asset validation ok
```

### `shellcheck home/dot_local/bin/common/executable_herdr-session home/dot_local/bin/common/executable_herdr-agents`

Exit: 0

```text
<no output>
```

### `bash -n home/dot_local/bin/common/executable_herdr-session home/dot_local/bin/common/executable_herdr-agents`

Exit: 0

```text
<no output>
```

### `git status --short -- home/dot_local/bin/common/executable_herdr-session home/dot_local/bin/common/executable_herdr-agents home/dot_claude/modify_private_settings.json tests/unit/test_herdr_agents.py .orchestration/reports/T15-herdr-lazy-start-attach-layout.md .orchestration/validation/T15-herdr-lazy-start-attach-layout.md .orchestration/sandboxes/T15-herdr-lazy-start-attach-layout.md .orchestration/learning/T15-herdr-lazy-start-attach-layout.md .orchestration/autoskill/runs/T15-herdr-lazy-start-attach-layout.md`

Exit: 0

```text
 M home/dot_claude/modify_private_settings.json
 M home/dot_local/bin/common/executable_herdr-agents
 M home/dot_local/bin/common/executable_herdr-session
 M tests/unit/test_herdr_agents.py
?? .orchestration/autoskill/runs/T15-herdr-lazy-start-attach-layout.md
?? .orchestration/learning/T15-herdr-lazy-start-attach-layout.md
?? .orchestration/reports/T15-herdr-lazy-start-attach-layout.md
?? .orchestration/sandboxes/T15-herdr-lazy-start-attach-layout.md
?? .orchestration/validation/T15-herdr-lazy-start-attach-layout.md
```

## Additional checks

### `shellcheck --version`

Exit: 0

```text
ShellCheck - shell script analysis tool
version: 0.11.0
license: GNU General Public License, version 3
website: https://www.shellcheck.net
```

### `git diff --check`

Exit: 0

```text
<no output>
```

## Test-first and regression evidence

- The initial RED run had three failures and one error for the new lazy-start, attach, and settings-hook expectations before implementation.
- The first repository-wide run exposed four existing Claude settings merge failures caused by unconditional hook injection. The modifier was narrowed to an existing managed `SessionStart` list, after which the focused 32-test suite, the 10 settings-merge tests, and all 149 repository unit tests passed.
- No Bats test was run locally, per repository policy.

## Review guard handoff

### `make require-crit-review`

Exit: 2

```text
Native agent review required before completion.
- review-sensitive path changed: .orchestration/acceptance/T11-agmsg-join-unique-identity-guard.md
- broad diff touches 73 files
- broad diff changes 5130 lines
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

### `crit status --json`

Exit: 0

```json
{
  "branch": "feat/herdr-lazy-start",
  "daemon": {
    "running": false
  },
  "review_file": "/Users/mryfmo/.crit/reviews/db2948e012d3/review.json",
  "review_file_exists": false,
  "vcs": "git"
}
```

The guard is intentionally not bypassed. It evaluates the shared pre-existing dirty worktree as well as T15, and no current Crit data exists; T15 is therefore handed to the orchestrator with `status=ready_for_review`.

## Authorized commit, push, and pull request

### Staged scope

```text
home/dot_claude/modify_private_settings.json
home/dot_local/bin/common/executable_herdr-agents
home/dot_local/bin/common/executable_herdr-session
tests/unit/test_herdr_agents.py
```

`git diff --cached --check` exited 0 with no output.

### Commit

```text
[feat/herdr-lazy-start 2f0d14c] feat(herdr): lazy single-terminal start with claude-triggered agent layout
 4 files changed, 203 insertions(+), 100 deletions(-)
```

### Push

```text
remote:
remote: Create a pull request for 'feat/herdr-lazy-start' on GitHub by visiting:
remote:      https://github.com/mryfmo/dotfiles/pull/new/feat/herdr-lazy-start
remote:
To github.com:mryfmo/dotfiles.git
 * [new branch]      feat/herdr-lazy-start -> feat/herdr-lazy-start
branch 'feat/herdr-lazy-start' set up to track 'origin/feat/herdr-lazy-start'.
```

### Pull request creation

The sandboxed first `gh pr create` attempt exited 1:

```text
error connecting to api.github.com
check your internet connection or https://githubstatus.com
```

The authorized network retry exited 0:

```text
https://github.com/mryfmo/dotfiles/pull/75
```

`gh pr view 75 --json url,title,body,baseRefName,headRefName,commits,files`
confirmed:

- URL: `https://github.com/mryfmo/dotfiles/pull/75`
- Base/head: `main` / `feat/herdr-lazy-start`
- Title: `feat(herdr): lazy single-terminal start with claude-triggered agent layout`
- Commit: `2f0d14cd4d591cb33490c5ba202add828448394d`
- Files: the same four authorized files
- The full English body covers lazy startup, the Claude SessionStart hook,
  idempotent 40/40/20 attachment, preserved full mode, and validation, and
  ends with the required Claude Code generation line.

### Initial GitHub Actions status

`gh pr checks 75` exited 8 because required jobs were still pending:

```text
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/29552213269/job/87797028771
test (ubuntu-latest, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/29552213269/job/87797028786
test (ubuntu-latest, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/29552213269/job/87797028809
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/29552213269/job/87797029348
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/29552213267/job/87797014498
public-bootstrap (ubuntu-latest, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/29552213267/job/87797014494
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/29552213321/job/87797014412
private-bootstrap (macos-14, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/29552213267/job/87797014481
public-bootstrap (ubuntu-latest, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/29552213267/job/87797014514
changes	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/29552213269/job/87797014423
private-bootstrap (ubuntu-latest, client)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/29552213267/job/87797014511
private-bootstrap (ubuntu-latest, server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/29552213267/job/87797014506
```

Per the acceptance instruction, no merge or CI/bot response was attempted.

### Final local/remote branch evidence

```text
2f0d14cd4d591cb33490c5ba202add828448394d
2f0d14cd4d591cb33490c5ba202add828448394d
2f0d14c (HEAD -> feat/herdr-lazy-start, origin/feat/herdr-lazy-start) feat(herdr): lazy single-terminal start with claude-triggered agent layout
 home/dot_claude/modify_private_settings.json       |  14 ++
 home/dot_local/bin/common/executable_herdr-agents  | 103 +++++++++---
 home/dot_local/bin/common/executable_herdr-session |  14 +-
 tests/unit/test_herdr_agents.py                    | 172 +++++++++++++--------
 4 files changed, 203 insertions(+), 100 deletions(-)
```

The scoped status for the four committed source/test files is clean.

## Full-mode layout race gate revision

The follow-up adds `HERDR_AGENTS_LAYOUT=managed` to every full-mode Claude
command and makes `--attach` exit before Herdr calls when that sentinel is
present.

### Test-first evidence

Before implementation, the focused suite ran 33 tests and exited 1 with six
expected failures: the new managed-layout no-op test and five full-mode Claude
command expectations.

### Final validation

- `uv run python -m unittest tests.unit.test_herdr_agents -v`: exit 0; 33
  tests passed.
- `make unit-test`: exit 0; 150 tests passed.
- `bash -n home/dot_local/bin/common/executable_herdr-agents && shellcheck
  home/dot_local/bin/common/executable_herdr-agents`: exit 0; no output.
- `UV_CACHE_DIR="$(mktemp -d)" uv run --with pyyaml
  scripts/validate-agent-assets.py`: true validator exit 0.

```text
Installed 1 package in 2ms
agent asset validation ok
exit=0
```

An earlier exit-preserving wrapper used zsh's read-only `status` variable:
the validator itself printed `agent asset validation ok`, but the wrapper
exited 1. The recorded final rerun uses `rc`, prints `exit=0`, and exits with
that same true code.

### Race gate commit and push

Only the two authorized files were staged:

```text
home/dot_local/bin/common/executable_herdr-agents
tests/unit/test_herdr_agents.py
```

```text
[feat/herdr-lazy-start 2de9122] fix(herdr): gate attach hook against full-mode layout race
 2 files changed, 20 insertions(+), 9 deletions(-)
```

```text
To github.com:mryfmo/dotfiles.git
   2f0d14c..2de9122  feat/herdr-lazy-start -> feat/herdr-lazy-start
```

New HEAD: `2de91223ec5ceb6e2f719a704cc39b1cd3be7031`.

### Updated full PR description

After the follow-up push, `gh pr view 75` confirmed the two-commit PR and its
four-file aggregate diff. The PR body was refreshed to include the sentinel
race gate and updated 33/150 test totals while retaining the full original
behavior summary and required final generation line.

The sandboxed `gh pr edit` attempt failed to connect to `api.github.com`; the
authorized network retry succeeded and returned:

```text
https://github.com/mryfmo/dotfiles/pull/75
```

Final `gh pr view 75` evidence:

```text
headRefOid=2de91223ec5ceb6e2f719a704cc39b1cd3be7031
title=feat(herdr): lazy single-terminal start with claude-triggered agent layout
url=https://github.com/mryfmo/dotfiles/pull/75
```

The post-push check showed CodeRabbit, changes, validate, two Ubuntu tests, and
all private-bootstrap jobs passing; macOS/public-bootstrap jobs remained
pending. No CI/bot reply or merge was performed.

## Authorized final PR phase

### Inline reply

The exact authorized response was posted to comment `3600174892`:

```text
id=3600299320
in_reply_to_id=3600174892
url=https://github.com/mryfmo/dotfiles/pull/75#discussion_r3600299320
body=Fixed in 2de91223: full mode now marks its Claude process with HERDR_AGENTS_LAYOUT=managed and the attach hook no-ops on that sentinel, removing the duplication race deterministically (timing-independent; lazy-path behavior unchanged).
```

### Thread resolution

`resolveReviewThread` returned:

```json
{"data":{"resolveReviewThread":{"thread":{"id":"PRRT_kwDOSMyAV86RpDht","isResolved":true,"resolvedBy":{"login":"mryfmo"}}}}}
```

The follow-up thread-aware read confirmed:

```json
{
  "pull_request": {
    "number": 75,
    "url": "https://github.com/mryfmo/dotfiles/pull/75",
    "state": "OPEN"
  },
  "unresolved": []
}
```

### Final checks

`gh pr checks 75` exited 0. CodeRabbit, changes, validate, all three test
jobs, all five bootstrap jobs, and their platform variants passed; the
intentional nix job was skipped.

### Squash merge

`gh pr merge 75 --squash --delete-branch` exited 0:

```text
From https://github.com/mryfmo/dotfiles
 * branch            main       -> FETCH_HEAD
   1c2943e..cab6de1  main       -> origin/main
Updating 1c2943e..cab6de1
Created autostash: dff7685
Fast-forward
 home/dot_claude/modify_private_settings.json       |  14 ++
 home/dot_local/bin/common/executable_herdr-agents  | 106 ++++++++---
 home/dot_local/bin/common/executable_herdr-session |  14 +-
 tests/unit/test_herdr_agents.py                    | 194 +++++++++++++--------
 4 files changed, 221 insertions(+), 107 deletions(-)
Applied autostash.
```

Final PR metadata:

```json
{"baseRefName":"main","headRefName":"feat/herdr-lazy-start","mergeCommit":{"oid":"cab6de14430e5c0807c0adee8a8f0ab0d181fbfd"},"mergedAt":"2026-07-17T04:13:16Z","state":"MERGED","url":"https://github.com/mryfmo/dotfiles/pull/75"}
```

- Merge SHA: `cab6de14430e5c0807c0adee8a8f0ab0d181fbfd`
- Current branch: `main`
- `HEAD`, local `main`, and `origin/main` all resolve to the merge SHA.
- The four merged source/test paths are clean.
- `git ls-remote --heads origin feat/herdr-lazy-start` returned no output,
  confirming remote deletion; `git fetch --prune origin` removed the stale
  remote-tracking ref.
- The merge-created autostash was reapplied, preserving pre-existing dirty
  and orchestration files.
