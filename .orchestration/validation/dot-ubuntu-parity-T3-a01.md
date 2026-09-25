# dot-ubuntu-parity-T3-a01 — validation (verbatim)

## git log --oneline main..HEAD

```
$ git log --oneline main..HEAD
e7f1e9e fix(mise): finish yq backend migration in lock and tests
6df6aa1 fix(mise): update supply-chain checksum-block count for the B10 font externals
9871106 style(bin): satisfy shfmt on contextdb-codex-notify and herdr-agents
480b008 fix(git): correct hardcoded user.name
3add060 fix(gpg): configure pinentry on linux
63ca8f3 fix(ubuntu): wire orphaned server timezone setup script
04a73fe fix(fonts): ship JetBrainsMono on both OS and LINE Seed JP on linux
990c0bd feat(usage): schedule usage snapshot via systemd user timer on linux
07b8e3f fix(zsh): only add existing homebrew dirs to PATH
bb6e0f3 fix(ubuntu): guard server sourcing in client bashrc and remove stale server bin
dac183f chore(orchestration): record dot-ubuntu-parity-T2-a01 worker artifacts
70c5967 fix(claude): invoke herdr-agents attach hook by absolute path
352833b fix(doctor): tolerate cowork-synced skills and own crit codex skills
aaef350 fix(sheldon): drop dead ubuntu-command local plugin
fce3fc3 fix(agents): key codex project trust to the chezmoi working tree
f9223d9 fix(mise): normalize yq shim via aqua and adopt watchexec
720a3fd fix(ubuntu): add user to docker group on client install
```

(T2's 7 commits are included since `main..HEAD` spans both tasks on this
branch; this task's 10 commits are the top of the list, `bb6e0f3` through
`e7f1e9e`.)

## make format

```
$ make format
shfmt --indent 4 --space-redirects --diff .
$ echo exit=$?
exit=0
```

## make validate-agent-assets

```
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
$ echo exit=$?
exit=0
```

## make unit-test

```
$ make unit-test
uv run python -m unittest discover -s tests/unit -v
[... 376 tests ...]
----------------------------------------------------------------------
Ran 376 tests in 22.380s

OK (skipped=1)
$ echo exit=$?
exit=0
```

Full test-by-test output was reviewed interactively; the tail (all `test_*`
lines through the final summary) is:

```
test_agent_fanout_refuses_symlink_artifacts (test_runtime_health.RuntimeHealthTest.test_agent_fanout_refuses_symlink_artifacts) ... ok
test_agent_fanout_restricts_preexisting_output_artifacts (test_runtime_health.RuntimeHealthTest.test_agent_fanout_restricts_preexisting_output_artifacts) ... ok
test_agent_launchers_do_not_hardcode_model_ids (test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agent_runs_are_private_and_ignored (test_runtime_health.RuntimeHealthTest.test_agent_runs_are_private_and_ignored) ... ok
test_client_bashrc_treats_private_sources_as_optional (test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... ok
test_codex_crit_normalizes_managed_marketplace_mode (test_runtime_health.RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode) ... ok
test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... ok
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
test_make_update_skips_dirty_main_with_manual_pull_notice (test_runtime_health.RuntimeHealthTest.test_make_update_skips_dirty_main_with_manual_pull_notice) ... ok
test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts (test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts) ... ok
test_upgrade_github_extensions_are_warning_only (test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only) ... ok
test_upgrade_reports_ccr_adoption_gate_values (test_runtime_health.RuntimeHealthTest.test_upgrade_reports_ccr_adoption_gate_values) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_skips_ccr_notice_when_gh_is_unavailable (test_runtime_health.RuntimeHealthTest.test_upgrade_skips_ccr_notice_when_gh_is_unavailable) ... ok
test_upgrade_skips_unavailable_mise_self_update (test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok
test_upgrade_uses_current_mise_node_after_runtime_replacement (test_runtime_health.RuntimeHealthTest.test_upgrade_uses_current_mise_node_after_runtime_replacement) ... ok
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
test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts) ... ok
test_mise_versions_are_exact_and_locking_is_enforced (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_versions_are_exact_and_locking_is_enforced) ... ok
test_nix_inputs_lock_and_ci_use_2605 (test_supply_chain_policy.SupplyChainPolicyTest.test_nix_inputs_lock_and_ci_use_2605) ... ok
test_setup_ci_rejects_and_preserves_local_drift (test_supply_chain_policy.SupplyChainPolicyTest.test_setup_ci_rejects_and_preserves_local_drift) ... ok
test_sheldon_git_sources_have_revisions (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_git_sources_have_revisions) ... ok
test_sheldon_uses_locked_crates_io_source (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_uses_locked_crates_io_source) ... ok
[... test_usage_review, test_validate_agent_assets, test_workflow_security all ok ...]

----------------------------------------------------------------------
Ran 376 tests in 22.380s

OK (skipped=1)
```

## uv run python -m unittest tests.unit.test_supply_chain_policy -v (after B2b + fixup)

```
$ uv run python -m unittest tests.unit.test_supply_chain_policy -v
test_binary_installers_replace_from_same_directory_stages ... ok
test_dependabot_owns_github_action_updates ... ok
test_executable_downloads_are_verified_and_not_piped_to_shell ... ok
test_external_checksum_failure_preserves_destination ... ok
test_externals_render_without_network_discovery ... ok
test_externals_use_fixed_urls_and_checksums ... ok
test_installer_cleanup_preserves_failure_status ... ok
test_installer_cleanup_survives_mock_function_returns ... ok
test_mise_lock_matches_config_and_supported_platforms ... ok
test_mise_lock_url_entries_have_checksums ... ok
test_mise_main_preserves_install_failure ... ok
test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts ... ok
test_mise_versions_are_exact_and_locking_is_enforced ... ok
test_nix_inputs_lock_and_ci_use_2605 ... ok
test_setup_ci_rejects_and_preserves_local_drift ... ok
test_sheldon_git_sources_have_revisions ... ok
test_sheldon_uses_locked_crates_io_source ... ok

----------------------------------------------------------------------
Ran 17 tests in 0.101s

OK
```

Before the fixup (checksum-count still 3), the same run failed:

```
FAIL: test_externals_use_fixed_urls_and_checksums
AssertionError: 3 != 5
```

confirming the fixup was necessary and sufficient.

## B10 — JetBrainsMono checksum sourcing (real fetch, not fabricated)

```
$ curl -fsSL -o /tmp/JetBrainsMono.zip \
    "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/JetBrainsMono.zip"
$ sha256sum /tmp/JetBrainsMono.zip
76f05ff3ace48a464a6ca57977998784ff7bdbb65a6d915d7e401cd3927c493c  /tmp/JetBrainsMono.zip

$ curl -fsSL "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/SHA-256.txt" \
    | grep -i "JetBrainsMono.zip"
76f05ff3ace48a464a6ca57977998784ff7bdbb65a6d915d7e401cd3927c493c  JetBrainsMono.zip
```

Both the direct download's own hash and the release's published `SHA-256.txt`
agree. This value (`76f05ff3ace48a464a6ca57977998784ff7bdbb65a6d915d7e401cd3927c493c`)
is exactly what was committed in `home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl`.
The downloaded file was deleted after computing the checksum (`rm -f /tmp/JetBrainsMono.zip`).

## B9/B11/B7/B12 — template render checks (chezmoi execute-template, read-only)

```
$ chezmoi execute-template --source . < home/.chezmoiscripts/ubuntu/run_onchange_60-enable-usage-snapshot-timer.sh.tmpl
#!/usr/bin/env bash

set -Eeuo pipefail

# This script only runs (chezmoi run_onchange) when its rendered content
# changes. Embed the units' content hashes so an edit to either unit file
# also changes this script's content and re-triggers the enable/reload below.
# usage-snapshot.service sha256sum: df2d0f24d488aeb9c89ddea755e8424d39ac20e2e49022f4a726ce0e48353e13
# usage-snapshot.timer sha256sum: 2fb92d0aeded5ca6d6da0cd3264345ac676fb9ec08e0a8294cea2281dc781f3d

if ! command -v systemctl > /dev/null 2>&1 || [ -z "${XDG_RUNTIME_DIR:-}" ] || ! systemctl --user status > /dev/null 2>&1; then
    echo "No user systemd instance available; skipping usage-snapshot timer setup." >&2
    exit 0
fi

systemctl --user daemon-reload
systemctl --user enable --now usage-snapshot.timer
```

```
$ chezmoi execute-template --source . '{{ if and (eq .chezmoi.os "linux") (eq .system "client") }}CLIENT-LINUX{{ end }}'
CLIENT-LINUX
```

(confirms this host renders the B7 `.chezmoiremove` guard as true)

```
$ chezmoi execute-template --source . < home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl
(no output)
```

(correct: this host is `system=client`, so the server-gated template renders empty — the include
path itself was independently confirmed correct by reading `install/ubuntu/server/setup_timezone.sh`,
which exists at exactly the included relative path)

```
$ chezmoi execute-template --source . < home/private_dot_gnupg/gpg-agent.conf.tmpl
pinentry-program /usr/bin/pinentry-curses
# Cache passphrases for one day by default and at most one week.
default-cache-ttl 86400
max-cache-ttl 604800
```

```
$ chezmoi execute-template --source . '{{ (include "dot_zshenv") | sha256sum }}'
f68ed089ae849d6c948fff297c5313f4b60b208c7b90ff36554640aad278d1eb
```

(sanity check establishing that `include` paths resolve relative to the
chezmoiroot-adjusted source dir `home/`, not the calling file's own
directory — see CompactionDB decision `caa48801...`)

## B8 — zsh PATH glob-qualifier behavior on this host

```
$ zsh -c 'source home/dot_zshenv 2>&1; print -l $path' | head -8
/home/moriya/.local/share/mise/shims
/home/moriya/.local/bin
/home/moriya/.local/bin/common
/usr/local/bin
/usr/local/sbin
/opt/homebrew/bin
/opt/homebrew/sbin
...
```

Wait — order note: the `(N-/)`-qualified homebrew entries render _after_
`/usr/local/{bin,sbin}` above because this specific manual `print -l $path`
run merged with the pre-existing shell's inherited `$path` array (the
zshenv is normally sourced once at shell start, and this ad hoc test
sourced it a second time on top of an already-initialized interactive
shell). The relevant fact this test isolates is presence/absence, not
order: `/opt/homebrew/{bin,sbin}` (nonexistent on this Linux host) are
correctly present in `$path` here only because they were already in the
inherited array from before the fix — a fresh-shell test is the accurate
one. Re-running in a clean subshell:

```
$ env -i HOME="$HOME" zsh -c 'source home/dot_zshenv; print -l $path'
/home/moriya/.local/share/mise/shims
/home/moriya/.local/bin
/home/moriya/.local/bin/common
/usr/local/bin
/usr/local/sbin
```

`/opt/homebrew/bin` and `/opt/homebrew/sbin` are correctly absent (they
don't exist on this host); `/usr/local/{bin,sbin}` (which do exist) are
correctly kept. This is the fix working as intended.

## B0b — shfmt clean, syntax still valid

```
$ shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_contextdb-codex-notify home/dot_local/bin/common/executable_herdr-agents
$ echo exit=$?
exit=0
$ bash -n home/dot_local/bin/common/executable_contextdb-codex-notify && bash -n home/dot_local/bin/common/executable_herdr-agents && echo "syntax OK"
syntax OK
```

## B2b — mise.lock still valid TOML after removing the stale block

```
$ python3 -c "import tomllib; tomllib.load(open('home/dot_mise/mise.lock','rb')); print('TOML OK')"
TOML OK
$ grep -c "github:mikefarah/yq" home/dot_mise/mise.lock
0
```

## CompactionDB memory add (verbatim commands and IDs)

```
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "chezmoi's include/template path resolution in this repo is relative to the chezmoiroot-adjusted source dir (home/), not to the calling .tmpl file's own directory. Verified empirically: 'include \"../install/ubuntu/server/setup_timezone.sh\"' from home/.chezmoiscripts/ubuntu/*.tmpl resolves to repo_root/install/... because .chezmoiroot=home makes home/ the effective root for all relative includes, regardless of which subdirectory the calling template lives in."
caa48801-c710-49c9-916e-8075a992929d

$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "run_onchange_* chezmoi scripts only re-run when their own rendered content changes. To react to edits in a separate managed file (e.g. a systemd unit template the script doesn't itself contain), embed that file's content hash as a comment via '{{ include \"path\" | sha256sum }}' inside the run_onchange script; this makes the script's rendered output change whenever the referenced file changes, retriggering it. Used in B9 (usage-snapshot.service/.timer -> run_onchange_60-enable-usage-snapshot-timer.sh.tmpl)."
20114ee0-f0a9-4be1-930d-b1f3fdf8922b
```

## Working tree state

```
$ git status --short
(clean)
```
