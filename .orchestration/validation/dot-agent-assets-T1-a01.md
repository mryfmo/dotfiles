# dot-agent-assets-T1-a01 validation

## Focused test before implementation

Command:

```text
uv run python -m unittest tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_skips_add_without_configured_marketplace -v
```

Exit code: 1

```text
test_codex_superpowers_skips_add_without_configured_marketplace (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_skips_add_without_configured_marketplace) ... FAIL

======================================================================
FAIL: test_codex_superpowers_skips_add_without_configured_marketplace (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_skips_add_without_configured_marketplace)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/mryfmo/Workspace/dotfiles/.claude/worktrees/agent-assets-fix/tests/unit/test_runtime_health.py", line 260, in test_codex_superpowers_skips_add_without_configured_marketplace
    self.assertIn(
    ~~~~~~~~~~~~~^
        "Skipping Codex Superpowers plugin: openai-curated is not a "
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        "configured Git marketplace.",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        result.stdout,
        ^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'Skipping Codex Superpowers plugin: openai-curated is not a configured Git marketplace.' not found in '\n==> Codex plugins\nSkipping Codex marketplace upgrade: openai-curated is not a configured Git marketplace.\nError: plugin superpowers@openai-curated was not found\n'

----------------------------------------------------------------------
Ran 1 test in 0.018s

FAILED (failures=1)
```

## Focused test after implementation

Command:

```text
uv run python -m unittest tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_skips_add_without_configured_marketplace -v
```

Exit code: 0

```text
test_codex_superpowers_skips_add_without_configured_marketplace (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_skips_add_without_configured_marketplace) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.016s

OK
```

## Independent terminal-browser installer digest

Command:

```text
curl -fsSL https://terminal-browser.sh/install | shasum -a 256
```

Exit code: 0

```text
accb57252d6e7dde513db2a473c008d71897cf72feaaecd58c5042821d1d63f9  -
```

The installer bytes were hashed only and were not executed.

## Shell syntax

Command:

```text
bash -n scripts/lib/installer-pins.sh scripts/update-agent-assets.sh
```

Exit code: 0. stdout and stderr were empty.

## Initial shellcheck

Command:

```text
shellcheck scripts/lib/installer-pins.sh scripts/update-agent-assets.sh
```

Exit code: 1

```text

In scripts/update-agent-assets.sh line 43:
    source "${AGENT_ASSET_SCRIPT_DIR}/lib/asset-manifest.sh"
           ^-- SC1091 (info): Not following: scripts/lib/asset-manifest.sh was not specified as input (see shellcheck -x).

For more information:
  https://www.shellcheck.net/wiki/SC1091 -- Not following: scripts/lib/asset-...
```

This invocation did not follow the repository's annotated source. The required follow-source rerun is below.

## Shellcheck with annotated sources followed

Command:

```text
shellcheck -x scripts/lib/installer-pins.sh scripts/update-agent-assets.sh
```

Exit code: 0. stdout and stderr were empty.

## Shell formatting

Command:

```text
shfmt --indent 4 --space-redirects --diff scripts/lib/installer-pins.sh scripts/update-agent-assets.sh
```

Exit code: 0. stdout and stderr were empty.

## Unconfigured marketplace mock trace

Command:

```text
bash -c '
source "$1"
has_command() { return 0; }
codex_marketplace_is_configured_git_marketplace() { return 1; }
command_output_contains() { return 1; }
codex() {
    if [ "$*" = "plugin add superpowers@openai-curated" ]; then
        printf "Error: plugin superpowers@openai-curated was not found\n"
    fi
}
manifest_codex_plugin_version() { printf "unknown\n"; }
manifest_record() { :; }
update_codex_superpowers
' _ scripts/update-agent-assets.sh
```

Exit code: 0

```text

==> Codex plugins
Skipping Codex marketplace upgrade: openai-curated is not a configured Git marketplace.
Skipping Codex Superpowers plugin: openai-curated is not a configured Git marketplace.
```

No `Error:` line was emitted.

## Runtime-health unit tests

Command:

```text
uv run python -m unittest tests.unit.test_runtime_health -v
```

Exit code: 0

```text
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok
test_agent_fanout_applies_profile_args_from_generated_fragment (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_fanout_applies_profile_args_from_generated_fragment) ... ok
test_agent_fanout_preserves_caller_umask_for_child_agents (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_fanout_preserves_caller_umask_for_child_agents) ... ok
test_agent_fanout_refuses_symlink_artifacts (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_fanout_refuses_symlink_artifacts) ... ok
test_agent_fanout_restricts_preexisting_output_artifacts (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_fanout_restricts_preexisting_output_artifacts) ... ok
test_agent_launchers_do_not_hardcode_model_ids (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agent_runs_are_private_and_ignored (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_runs_are_private_and_ignored) ... ok
test_codex_superpowers_skips_add_without_configured_marketplace (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_skips_add_without_configured_marketplace) ... ok
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_upgrade_bumps_terminal_tool_pins_from_fetched_installers (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_tool_pins_from_fetched_installers) ... ok
test_upgrade_github_extensions_are_warning_only (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only) ... ok
test_upgrade_reports_ccr_adoption_gate_values (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_reports_ccr_adoption_gate_values) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_skips_ccr_notice_when_gh_is_unavailable (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_ccr_notice_when_gh_is_unavailable) ... ok
test_upgrade_skips_unavailable_mise_self_update (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok
test_upgrade_uses_current_mise_node_after_runtime_replacement (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_uses_current_mise_node_after_runtime_replacement)
Reject ambient npm after mise replaces the active Node runtime. ... ok

----------------------------------------------------------------------
Ran 20 tests in 6.854s

OK
```

## Supply-chain unit tests

Command:

```text
uv run python -m unittest tests.unit.test_supply_chain_policy -v
```

Exit code: 0

```text
test_binary_installers_replace_from_same_directory_stages (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_binary_installers_replace_from_same_directory_stages) ... ok
test_dependabot_owns_github_action_updates (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_dependabot_owns_github_action_updates) ... ok
test_executable_downloads_are_verified_and_not_piped_to_shell (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_executable_downloads_are_verified_and_not_piped_to_shell) ... ok
test_external_checksum_failure_preserves_destination (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_external_checksum_failure_preserves_destination) ... ok
test_externals_render_without_network_discovery (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_externals_render_without_network_discovery) ... ok
test_externals_use_fixed_urls_and_checksums (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_externals_use_fixed_urls_and_checksums) ... ok
test_installer_cleanup_preserves_failure_status (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_preserves_failure_status) ... ok
test_installer_cleanup_survives_mock_function_returns (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) ... ok
test_mise_lock_matches_config_and_supported_platforms (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_matches_config_and_supported_platforms) ... ok
test_mise_lock_url_entries_have_checksums (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_lock_url_entries_have_checksums) ... ok
test_mise_main_preserves_install_failure (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_main_preserves_install_failure) ... ok
test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts) ... ok
test_mise_versions_are_exact_and_locking_is_enforced (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_mise_versions_are_exact_and_locking_is_enforced) ... ok
test_nix_inputs_lock_and_ci_use_2605 (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_nix_inputs_lock_and_ci_use_2605) ... ok
test_setup_ci_rejects_and_preserves_local_drift (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_setup_ci_rejects_and_preserves_local_drift) ... ok
test_sheldon_git_sources_have_revisions (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_git_sources_have_revisions) ... ok
test_sheldon_uses_locked_crates_io_source (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_uses_locked_crates_io_source) ... ok

----------------------------------------------------------------------
Ran 17 tests in 0.373s

OK
```

## Diff whitespace check

Command:

```text
git diff --check
```

Exit code: 0. stdout and stderr were empty.

## CompactionDB decision

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'terminal-browser installer is pinned at v0.11.1 with SHA-256 accb57252d6e7dde513db2a473c008d71897cf72feaaecd58c5042821d1d63f9; Codex Superpowers plugin installation is skipped unless openai-curated is a configured Git marketplace, while already-installed detection remains active.'
```

Exit code: 0

```text
efab8207-2839-456f-96de-2207b9eb8d52
```

## Initial review gate

Command:

```text
make require-crit-review
```

Exit code: 2

```text
Native agent review required before completion.
- agent lifecycle path changed: scripts/lib/installer-pins.sh
- broad diff touches 9 files
- broad diff changes 394 lines
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

## Review gate with Crit data evidence

Command:

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/dot-agent-assets-T1-a01-receipt.md make require-crit-review
```

Exit code: 0

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```
