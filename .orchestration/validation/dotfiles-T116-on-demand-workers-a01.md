# Validation: dotfiles-T116-on-demand-workers-a01

Worker claude-standard-dot-a001 (worker-c), branch feat/on-demand-workers, PR #306, final head bb2edb384f8f791e46ac37a01d8884d1604b916a. Verbatim output, ANSI colour codes stripped. Sandbox-only adjustments, as in T114: commands run with GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false exported (global SSH commit signing cannot read ~/.ssh in the sandbox), uv with pypi.org/files.pythonhosted.org allowed, and mise with MISE_STATE_DIR=$TMPDIR/mise-state (its trust symlink under ~/.local/state is write-denied).

## 1. Task validation commands at the final head

```
$ git log --oneline -6
bb2edb38 test(runtime-health): pin the add-worker profile literal
dfdbb8c5 fix(herdr-agents): never take a seated claude worker for the orchestrator
60d49593 docs(regime): describe on-demand workers instead of the resident pair
04c37440 feat(regime): report a worker left seated at a boundary
93ec0b0e feat(herdr-agents): seat only the orchestrator at startup and workers on demand
02d65ca7 fix(regime): reconcile the canonical clone after a pins PR and ignore worker worktrees (#304)
$ shellcheck home/dot_local/bin/common/executable_herdr-agents scripts/check-regime-boundary.sh; echo "rc=$?"
rc=0
$ bash home/dot_local/bin/common/executable_herdr-agents --restart-worker /tmp/nonexistent; echo "rc=$?"
herdr-agents: --restart-worker is retired; run herdr-agents --remove-worker <worktree> and then herdr-agents --add-worker <worktree> [--kind …] [--profile NAME]
rc=2
$ uv run python -m unittest tests.unit.test_herdr_agents tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3
Ran 206 tests in 265.403s

FAILED (failures=28, errors=3)
$ make unit-test 2>&1 | tail -3   # run at bb2edb38 (the final head), log saved as t116-unit-final.txt

FAILED (failures=73, errors=10, skipped=2)
make: *** [unit-test] Error 1
$ uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T116-on-demand-workers-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0003cbd.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0003cbd.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0f0f2cb.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0f0f2cb.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-46a229c.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-46a229c.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-audit-282c5e8.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-audit-282c5e8.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: worker still seated at .claude/worktrees/worker-c (herdr-agents --remove-worker .claude/worktrees/worker-c)
WARN: regime-boundary: canonical clone ~/.local/share/chezmoi has unmerged entries (git ls-files -u); finish or abort its pull
WARN: regime-boundary: canonical clone ~/.local/share/chezmoi carries a stash (git stash list); drop only the autostash entry once its content is on origin/main, and leave any other stash to its owner
WARN: regime-boundary: canonical clone ~/.local/share/chezmoi differs from origin/main under home/, install/ or scripts/: home/dot_agents/agent-config.yaml,home/dot_agents/model-profiles.env,home/dot_claude/agents/project-map.md,home/dot_codex/modify_private_audit.config.toml,home/dot_mise/mise.lock,scripts/validate-agent-assets.py; carry a make upgrade diff as a pins task, or restore a merged one with git -C ~/.local/share/chezmoi restore -SW --source=origin/main -- <files> and drop its autostash
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles-conformance:claude-standard-dot-a001 (herdr-agents --remove-worker)
agent asset validation ok
rc=0
$ bash scripts/check-regime-boundary.sh --report; echo "rc=$?"
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T114-canonical-clone-reconcile-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T115-worker-audit-xhigh-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T114-canonical-clone-reconcile-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T115-worker-audit-xhigh-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T114-canonical-clone-reconcile-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T115-worker-audit-xhigh-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T114-canonical-clone-reconcile-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T115-worker-audit-xhigh-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T114-canonical-clone-reconcile-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T115-worker-audit-xhigh-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T114-canonical-clone-reconcile-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T115-worker-audit-xhigh-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T116-on-demand-workers-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0003cbd.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0003cbd.md.last.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0f0f2cb.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0f0f2cb.md.last.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-46a229c.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-46a229c.md.last.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-crit.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-pr-feedback.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-review-receipt.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-worker-crit.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-worker-review-receipt.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-audit-282c5e8.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-audit-282c5e8.md.last.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-crit.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-pr-feedback.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-review-receipt.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-worker-crit.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-worker-review-receipt.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01.md
regime-boundary: worker still seated at .claude/worktrees/worker-c (herdr-agents --remove-worker .claude/worktrees/worker-c)
regime-boundary: canonical clone ~/.local/share/chezmoi has unmerged entries (git ls-files -u); finish or abort its pull
regime-boundary: canonical clone ~/.local/share/chezmoi carries a stash (git stash list); drop only the autostash entry once its content is on origin/main, and leave any other stash to its owner
regime-boundary: canonical clone ~/.local/share/chezmoi differs from origin/main under home/, install/ or scripts/: home/dot_agents/agent-config.yaml,home/dot_agents/model-profiles.env,home/dot_claude/agents/project-map.md,home/dot_codex/modify_private_audit.config.toml,home/dot_mise/mise.lock,scripts/validate-agent-assets.py; carry a make upgrade diff as a pins task, or restore a merged one with git -C ~/.local/share/chezmoi restore -SW --source=origin/main -- <files> and drop its autostash
regime-boundary: additional worker tab still open in dotfiles: dotfiles-conformance:claude-standard-dot-a001 (herdr-agents --remove-worker)
rc=0
$ MISE_STATE_DIR=$TMPDIR/mise-state mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_config/claude/rules/agmsg-orchestration.md 2>&1 | tail -2
Checking formatting...
All matched files use Prettier code style!
```

## 2. Failure identity: full suite at the final head vs origin/main (02d65ca7) in this sandbox

The baseline is a full `python -m unittest discover -s tests/unit -v` run on a scratch detached checkout of origin/main 02d65ca7 (created with `git worktree add --detach`, removed with `git worktree remove --force`), same environment.

```
$ tail -3 base116-unit.txt   # origin/main 02d65ca7
Ran 930 tests in 626.161s

FAILED (failures=73, errors=10, skipped=2)
$ cat t116-unit-final-head.txt; tail -3 t116-unit-final.txt   # branch
bb2edb38 test(runtime-health): pin the add-worker profile literal

FAILED (failures=73, errors=10, skipped=2)
make: *** [unit-test] Error 1
$ norm(){ sed 's/\[[0-9;]*m//g' "$1" | grep -E '^(FAIL|ERROR): test' | sed -E 's/\(tests\.unit\./(/' | sort; }
$ norm t116-unit-final.txt > t116-final-failing.txt; norm base116-unit.txt > t116-base-failing.txt
$ wc -l t116-final-failing.txt t116-base-failing.txt
      83 t116-final-failing.txt
      83 t116-base-failing.txt
     166 total
$ comm -3 t116-final-failing.txt t116-base-failing.txt; echo "comm-lines=..."
comm-lines=0
$ cat t116-final-failing.txt
ERROR: test_a_failing_chmod_fails_the_step (test_gh_auth.GhAuthTest.test_a_failing_chmod_fails_the_step)
ERROR: test_a_login_that_does_not_complete_fails (test_gh_auth.GhAuthTest.test_a_login_that_does_not_complete_fails)
ERROR: test_a_working_keyring_login_is_moved_to_the_file (test_gh_auth.GhAuthTest.test_a_working_keyring_login_is_moved_to_the_file)
ERROR: test_add_worker_derives_the_default_herdr_socket_for_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_derives_the_default_herdr_socket_for_spawn)
ERROR: test_add_worker_linkage_refuses_a_placement_conflict (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_a_placement_conflict)
ERROR: test_add_worker_linkage_resolves_an_id_keyed_placement_record (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_resolves_an_id_keyed_placement_record)
ERROR: test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state)
ERROR: test_agmsg_migration_reports_an_installer_that_mutates_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state)
ERROR: test_on_a_terminal_it_logs_in_to_gh_file_at_0600 (test_gh_auth.GhAuthTest.test_on_a_terminal_it_logs_in_to_gh_file_at_0600)
ERROR: test_setup_finds_a_mise_installed_gh_on_a_fresh_path (test_gh_auth.GhAuthTest.test_setup_finds_a_mise_installed_gh_on_a_fresh_path)
FAIL: test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits (test_herdr_agents.HerdrAgentsTest.test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits)
FAIL: test_add_worker_emits_no_override_for_an_unparseable_codex_config (test_herdr_agents.HerdrAgentsTest.test_add_worker_emits_no_override_for_an_unparseable_codex_config)
FAIL: test_add_worker_exits_zero_when_a_timed_out_spawn_still_links (test_herdr_agents.HerdrAgentsTest.test_add_worker_exits_zero_when_a_timed_out_spawn_still_links)
FAIL: test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array (test_herdr_agents.HerdrAgentsTest.test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array)
FAIL: test_add_worker_linkage_failure_prints_the_invocation_and_the_query (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_failure_prints_the_invocation_and_the_query)
FAIL: test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver)
FAIL: test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping)
FAIL: test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace)
FAIL: test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn)
FAIL: test_add_worker_linkage_ignores_a_placement_record_from_another_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_from_another_workspace)
FAIL: test_add_worker_linkage_ignores_a_pong_older_than_this_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_pong_older_than_this_ping)
FAIL: test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal)
FAIL: test_add_worker_linkage_refuses_several_orchestrator_identities (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_several_orchestrator_identities)
FAIL: test_add_worker_linkage_survives_a_non_numeric_pong_wait (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_survives_a_non_numeric_pong_wait)
FAIL: test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh)
FAIL: test_add_worker_names_the_seat_from_a_codex_orchestrator_identity (test_herdr_agents.HerdrAgentsTest.test_add_worker_names_the_seat_from_a_codex_orchestrator_identity)
FAIL: test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options (test_herdr_agents.HerdrAgentsTest.test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options)
FAIL: test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog)
FAIL: test_add_worker_reports_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_spawn)
FAIL: test_add_worker_reports_linkage_ok_after_a_ready_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_ok_after_a_ready_spawn)
FAIL: test_add_worker_reports_linkage_unreached_after_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_unreached_after_a_failed_spawn)
FAIL: test_add_worker_reports_shallow_metadata_as_not_granted (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_shallow_metadata_as_not_granted)
FAIL: test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace)
FAIL: test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args (test_herdr_agents.HerdrAgentsTest.test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args)
FAIL: test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog)
FAIL: test_added_worker_boot_keeps_the_inherited_github_environment (test_herdr_agents.HerdrAgentsTest.test_added_worker_boot_keeps_the_inherited_github_environment) (kind='claude')
FAIL: test_added_worker_boot_keeps_the_inherited_github_environment (test_herdr_agents.HerdrAgentsTest.test_added_worker_boot_keeps_the_inherited_github_environment) (kind='codex')
FAIL: test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes)
FAIL: test_agmsg_checksum_mismatch_fails_closed (test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed)
FAIL: test_agmsg_fresh_install_populates_skill_and_records_manifest (test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest)
FAIL: test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty)
FAIL: test_agmsg_reports_an_installer_that_leaves_the_wrong_version (test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version)
FAIL: test_agmsg_update_aborts_when_install_corrupts_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state)
FAIL: test_ceiling_directories_do_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_ceiling_directories_do_not_hide_the_seat)
FAIL: test_character_device_placeholder_is_skipped (test_agent_stop_gate.AgentStopGateTest.test_character_device_placeholder_is_skipped)
FAIL: test_clean_orchestrator_passes (test_agent_stop_gate.AgentStopGateTest.test_clean_orchestrator_passes)
FAIL: test_darwin_crit_checksum_failure_preserves_existing_binary (test_runtime_health.RuntimeHealthTest.test_darwin_crit_checksum_failure_preserves_existing_binary)
FAIL: test_darwin_crit_install_is_pinned_atomic_and_recorded (test_runtime_health.RuntimeHealthTest.test_darwin_crit_install_is_pinned_atomic_and_recorded)
FAIL: test_every_team_of_the_identity_is_checked (test_agent_stop_gate.AgentStopGateTest.test_every_team_of_the_identity_is_checked)
FAIL: test_gpgv_failure_preserves_existing_aws_and_skips_unzip (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_gpgv_failure_preserves_existing_aws_and_skips_unzip)
FAIL: test_inherited_git_dir_does_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_inherited_git_dir_does_not_hide_the_seat)
FAIL: test_installer_cleanup_preserves_failure_status (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_preserves_failure_status) (relative='install/common/sheldon.sh')
FAIL: test_installer_cleanup_survives_mock_function_returns (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) (relative='install/common/mise.sh')
FAIL: test_installer_cleanup_survives_mock_function_returns (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) (relative='install/common/sheldon.sh')
FAIL: test_installer_cleanup_survives_mock_function_returns (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) (relative='install/ubuntu/server/starship.sh')
FAIL: test_json_escaped_cwd_resolves (test_agent_stop_gate.AgentStopGateTest.test_json_escaped_cwd_resolves)
FAIL: test_linux_crit_install_is_pinned_atomic_and_recorded (test_runtime_health.RuntimeHealthTest.test_linux_crit_install_is_pinned_atomic_and_recorded)
FAIL: test_orchestrator_acceptance_to_another_member_keeps_the_result_open (test_agent_stop_gate.AgentStopGateTest.test_orchestrator_acceptance_to_another_member_keeps_the_result_open)
FAIL: test_project_dir_anchors_the_seat_after_a_cd (test_agent_stop_gate.AgentStopGateTest.test_project_dir_anchors_the_seat_after_a_cd)
FAIL: test_result_then_acceptance_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_acceptance_passes)
FAIL: test_result_then_revision_task_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_revision_task_passes)
FAIL: test_result_without_acceptance_blocks (test_agent_stop_gate.AgentStopGateTest.test_result_without_acceptance_blocks)
FAIL: test_sandbox_placeholders_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_are_skipped)
FAIL: test_sandbox_placeholders_on_a_separate_filesystem_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_on_a_separate_filesystem_are_skipped)
FAIL: test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude (test_herdr_agents.HerdrAgentsTest.test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude)
FAIL: test_separate_git_dir_main_worktree_is_a_seat (test_agent_stop_gate.AgentStopGateTest.test_separate_git_dir_main_worktree_is_a_seat)
FAIL: test_slow_store_blocks_within_the_budget (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget)
FAIL: test_slow_store_blocks_within_the_budget_without_timeout (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget_without_timeout)
FAIL: test_solo_unsuffixed_worker_is_gated (test_agent_stop_gate.AgentStopGateTest.test_solo_unsuffixed_worker_is_gated)
FAIL: test_sqlite_store_off_the_current_schema_is_not_initialized (test_agent_stop_gate.AgentStopGateTest.test_sqlite_store_off_the_current_schema_is_not_initialized)
FAIL: test_staged_rename_out_of_orchestration_blocks (test_agent_stop_gate.AgentStopGateTest.test_staged_rename_out_of_orchestration_blocks)
FAIL: test_stop_hook_active_skips_only_the_dirty_tree_check (test_agent_stop_gate.AgentStopGateTest.test_stop_hook_active_skips_only_the_dirty_tree_check)
FAIL: test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts (test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts)
FAIL: test_upgrade_github_extensions_are_warning_only (test_runtime_health.RuntimeHealthTest.test_upgrade_github_extensions_are_warning_only)
FAIL: test_verified_archive_runs_installer_with_user_local_update_arguments (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_verified_archive_runs_installer_with_user_local_update_arguments)
FAIL: test_worker_after_result_passes (test_agent_stop_gate.AgentStopGateTest.test_worker_after_result_passes)
FAIL: test_worker_alive_pong_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_alive_pong_keeps_the_task_open)
FAIL: test_worker_blocked_pong_closes_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_blocked_pong_closes_the_task)
FAIL: test_worker_result_to_another_member_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_result_to_another_member_keeps_the_task_open)
FAIL: test_worker_revise_acceptance_reopens_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_revise_acceptance_reopens_the_task)
FAIL: test_worker_task_closed_by_a_non_revise_acceptance (test_agent_stop_gate.AgentStopGateTest.test_worker_task_closed_by_a_non_revise_acceptance)
FAIL: test_worker_task_newer_than_result_blocks (test_agent_stop_gate.AgentStopGateTest.test_worker_task_newer_than_result_blocks)
FAIL: test_worker_tracks_each_task_id (test_agent_stop_gate.AgentStopGateTest.test_worker_tracks_each_task_id)
```

The full run at 60d49593 had one extra failure, `test_runtime_health.test_agent_launchers_do_not_hardcode_model_ids` (it pinned the retired start_worker_agent line); Amendment 1 allowed the fix in bb2edb38, and the comparison above is after it.

## 3. The new and changed tests fail without the change

```
$ git show origin/main:home/dot_local/bin/common/executable_herdr-agents > home/dot_local/bin/common/executable_herdr-agents  # then the new launcher tests
$ uv run python -m unittest tests.unit.test_herdr_agents -k retired_and_touches -k starts_only_the_orchestrator -k linked_worker_worktree -k bootstraps_agmsg_without -k never_sets_codex -k heal_with_a_live -k never_puts_the_orchestrator -k defaults_to_the_manifest_worktree -k regime_directive_with 2>&1 | <filter>
FAIL: test_add_worker_defaults_to_the_manifest_worktree_and_refuses_a_non_worktree_path
FAIL: test_attach_bootstraps_agmsg_without_starting_a_worker
FAIL: test_attach_in_a_linked_worker_worktree_exits_quietly
FAIL: test_bootstrap_only_never_sets_codex_delivery_in_the_main_checkout
FAIL: test_full_mode_heal_never_puts_the_orchestrator_in_the_audit_or_an_added_worker_tab
FAIL: test_full_mode_heal_with_a_live_orchestrator_starts_nothing
FAIL: test_full_mode_starts_only_the_orchestrator_in_the_initial_pane
FAIL: test_restart_worker_is_retired_and_touches_nothing
FAIL: test_session_start_attach_prints_the_regime_directive_with_a_worker_seat
Ran 9 tests in 11.790s
FAILED (failures=9)
$ git show origin/main:scripts/check-regime-boundary.sh > scripts/check-regime-boundary.sh  # then the changed boundary tests
$ uv run python -m unittest tests.unit.test_herdr_agents -k across_runtime_types_at_the_main_seat -k empty_manifest_worker_worktree -k added_worker_tab 2>&1 | <filter>
FAIL: test_regime_boundary_check_accepts_an_empty_manifest_worker_worktree
FAIL: test_regime_boundary_check_counts_names_across_runtime_types_at_the_main_seat
FAIL: test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace
Ran 4 tests in 3.514s
FAILED (failures=3)
$ git status --porcelain; git log --oneline -1
60d49593 docs(regime): describe on-demand workers instead of the resident pair

$ git show 60d49593:home/dot_local/bin/common/executable_herdr-agents > home/dot_local/bin/common/executable_herdr-agents; uv run python -m unittest tests.unit.test_herdr_agents -k normalized_claude_worker -k refuses_to_seat_the_orchestrator 2>&1 | <filter>
FAIL: test_full_mode_never_takes_a_normalized_claude_worker_for_the_orchestrator
FAIL: test_full_mode_refuses_to_seat_the_orchestrator_in_a_worker_tab
Ran 2 tests in 0.869s
FAILED (failures=2)
```

(The second block ran before the P1 fix was committed, against the 60d49593 launcher; the working tree was restored to the uncommitted fix afterwards, then committed as dfdbb8c5.)

## 4. Test inventory (origin/main → final head, tests/unit/test_herdr_agents.py)

```
$ comm -23 <origin/main test names> <head test names> | wc -l; comm -13 ... | wc -l
66 removed by name, 15 added by name
--- deleted (retired behaviour, 55):
test_attach_builds_codex_right_of_current_claude_pane
test_attach_lowercases_and_validates_derived_agent_name
test_attach_rejects_invalid_derived_agent_name
test_attach_repairs_codex_claude_order_with_one_swap
test_attach_repairs_skewed_widths_to_equal_halves
test_attach_warns_after_one_nonconverging_resize
test_attach_ratio_repair_skips_unsafe_layouts
test_attach_legacy_files_pane_refuses_repair_without_layout_mutation
test_attach_does_not_restart_codex_agent_from_another_tab
test_attach_bootstraps_agmsg_after_codex_reuse
test_attach_warns_when_multiple_agmsg_identities_exist
test_codex_profile_defaults_to_generated_interactive_profile
test_worker_profile_defaults_to_generated_worker_profile
test_worker_profile_env_override_wins_over_generated_worker_profile
test_worker_kind_defaults_to_generated_env_fragment
test_worker_kind_env_override_wins_over_generated_env_fragment
test_worker_kind_rejects_an_unknown_value
test_worker_kind_claude_starts_a_claude_worker_pane_with_profile_args
test_worker_kind_claude_starts_with_no_resolved_args
test_worker_kind_claude_appends_extra_worker_args
test_claude_worker_sharing_the_orchestrator_identity_is_refused
test_claude_worker_with_a_registered_worker_identity_proceeds
test_codex_worker_is_not_subject_to_the_identity_guard
test_bootstrap_with_claude_worker_accepts_two_claude_identities
test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity
test_worker_kind_claude_accepts_a_workspace_trust_dialog
test_worker_kind_claude_skips_send_keys_without_a_trust_dialog
test_restart_worker_reseats_a_main_path_worker_into_its_worktree
test_worker_seat_reuses_the_identity_and_hook_already_at_the_worktree
test_full_mode_splits_the_worker_pane_in_its_worktree
test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots
test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree
test_worker_seat_is_skipped_in_an_unregistered_repository
test_worker_seat_is_skipped_in_a_non_git_directory
test_worker_seat_ambiguity_leaves_no_worktree_behind
test_attach_repair_splits_the_missing_worker_pane_in_its_worktree
test_restart_worker_refuses_to_start_outside_the_seat_when_the_pane_hangs
test_restart_worker_relaunches_the_worker_in_its_existing_pane
test_restart_worker_waits_for_stale_registration_then_retries_once
test_restart_worker_passes_manifest_advisor_args_to_claude_worker
test_restart_worker_confirms_the_exit_dialog_once
test_restart_worker_refuses_when_the_pane_never_reaches_a_shell
test_restart_worker_repairs_a_legacy_orchestrator_label_on_the_worker_pane
test_restart_worker_refuses_unmanaged_extra_panes
test_full_mode_reuses_agentless_worker_pane_in_attach_labeled_workspace
test_restart_worker_finds_the_worker_by_its_seat_label
test_another_team_members_pane_is_not_a_second_worker
test_mixed_legacy_and_seat_labels_are_one_pair
test_restart_worker_finds_a_solo_codex_worker_seat
test_explicit_worker_kind_and_profile_survive_seat_label_loading
test_audit_tab_does_not_break_attach_order_and_ratio_repair
test_restart_worker_never_treats_the_audit_pane_as_the_worker
test_existing_two_pane_workspace_repairs_skewed_widths
test_existing_workspace_restarts_missing_codex_agent
test_claude_repair_skips_just_restarted_codex_pane_without_agent_field
--- renamed or converted (11 old names → rewritten tests):
test_attach_bootstraps_agmsg_after_codex_start
test_bootstrap_only_sets_each_missing_delivery_once
test_codex_orchestrator_kind_refuses_the_claude_pair_before_herdr
test_full_and_restart_modes_refuse_duplicate_managed_workspaces
test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane
test_full_mode_heal_never_starts_the_worker_in_the_audit_pane
test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat
test_restart_worker_exits_2_without_a_managed_workspace
test_uses_initial_workspace_pane_for_claude_and_splits_codex_right
test_worker_seat_refuses_a_path_that_is_not_a_worktree
test_worker_seat_refuses_an_ambiguous_orchestrator_identity
--- added names (15, of which 11 are the rewrites above):
test_add_worker_defaults_to_the_manifest_worktree_and_refuses_a_non_worktree_path
test_add_worker_without_a_worktree_refuses_an_ambiguous_orchestrator_identity
test_attach_bootstraps_agmsg_without_starting_a_worker
test_attach_in_a_linked_worker_worktree_exits_quietly
test_bootstrap_only_never_sets_codex_delivery_in_the_main_checkout
test_codex_orchestrator_kind_refuses_the_claude_orchestrator_before_herdr
test_full_mode_heal_never_puts_the_orchestrator_in_the_audit_or_an_added_worker_tab
test_full_mode_heal_with_a_live_orchestrator_starts_nothing
test_full_mode_never_takes_a_normalized_claude_worker_for_the_orchestrator
test_full_mode_refuses_duplicate_managed_workspaces
test_full_mode_refuses_to_seat_the_orchestrator_in_a_worker_tab
test_full_mode_starts_only_the_orchestrator_in_the_initial_pane
test_regime_boundary_check_accepts_an_empty_manifest_worker_worktree
test_regime_boundary_check_counts_names_across_runtime_types_at_the_main_seat
test_restart_worker_is_retired_and_touches_nothing
```

## 5. Bot P1 4225776337 (two --config overrides through spawn options): the installed upstream parser keeps both

```
$ cat spawn-opts.yaml
codex:
  --profile: standard
  --sandbox: workspace-write
  --ask-for-approval: never
  --config: sandbox_workspace_write.network_access=true
  --config: sandbox_workspace_write.writable_roots=["/a","/b"]
$ AGMSG_SPAWN_OPTIONS_FILE=spawn-opts.yaml bash -c 'source ~/.agents/skills/agmsg/scripts/lib/spawn-options.sh; agmsg_spawn_options_tokens codex'
--profile
standard
--sandbox
workspace-write
--ask-for-approval
never
--config
sandbox_workspace_write.network_access=true
--config
sandbox_workspace_write.writable_roots=["/a","/b"]
$ cat ~/.agents/skills/agmsg/VERSION
1.5.0
```

## 6. Push, PR, CI and Bot

```
$ GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles feat/on-demand-workers 2>&1 | tail -1   # first push
 * [new branch]        feat/on-demand-workers -> feat/on-demand-workers
$ gh pr create --base main --head feat/on-demand-workers --title 'feat(herdr-agents): seat only the orchestrator at startup and workers on demand' --body-file <body>
https://github.com/mryfmo/dotfiles/pull/306
$ <CI watch and bounded Bot wait on 60d49593>
head=60d4959322a8548efcb3ccc4ce29c245f4443e99
checks-rc=1
test (ubuntu-24.04, client)	fail	3m46s	https://github.com/mryfmo/dotfiles/actions/runs/37869336530/job/113623581848	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37869336530/job/113623543249	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37869336529/job/113623544003	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37869336529/job/113623543991	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/37869336529/job/113623544050	
public-bootstrap (macos-14, client)	pass	8m8s	https://github.com/mryfmo/dotfiles/actions/runs/37869336529/job/113623543999	
public-bootstrap (ubuntu-24.04, client)	pass	7m39s	https://github.com/mryfmo/dotfiles/actions/runs/37869336529/job/113623543733	
public-bootstrap (ubuntu-24.04, server)	pass	7m35s	https://github.com/mryfmo/dotfiles/actions/runs/37869336529/job/113623544076	
validate	pass	48s	https://github.com/mryfmo/dotfiles/actions/runs/37869336542/job/113623543361	
test (macos-14, client)	fail	4m2s	https://github.com/mryfmo/dotfiles/actions/runs/37869336530/job/113623581861	
test (ubuntu-24.04, server)	fail	4m1s	https://github.com/mryfmo/dotfiles/actions/runs/37869336530/job/113623581882	
test (ubuntu-26.04, client)	fail	3m59s	https://github.com/mryfmo/dotfiles/actions/runs/37869336530/job/113623581904	
2026-10-09T01:29:33Z reviews:
chatgpt-codex-connector[bot]	60d4959322a8548efcb3ccc4ce29c245f4443e99	2026-10-09T01:27:44Z	COMMENTED
comments:
4225776331	60d4959322a8548efcb3ccc4ce29c245f4443e99	home/dot_local/bin/common/executable_herdr-agents	chatgpt-codex-connector[bot]
4225776337	60d4959322a8548efcb3ccc4ce29c245f4443e99	home/dot_local/bin/common/executable_herdr-agents	chatgpt-codex-connector[bot]
rc=0

$ gh run view 37869336530 --log-failed | grep -E "(FAIL|ERROR): test" | sort | uniq -c
   1 FAIL: test_agent_launchers_do_not_hardcode_model_ids (test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids)
$ <second push>
   60d49593..bb2edb38  feat/on-demand-workers -> feat/on-demand-workers
$ <CI watch and bounded Bot wait on bb2edb38>
head=bb2edb384f8f791e46ac37a01d8884d1604b916a
checks-rc=0
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37871306063/job/113629799927	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/37871306061/job/113629800154	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37871306061/job/113629799986	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37871306061/job/113629800048	
public-bootstrap (macos-14, client)	pass	9m8s	https://github.com/mryfmo/dotfiles/actions/runs/37871306061/job/113629800146	
public-bootstrap (ubuntu-24.04, client)	pass	10m27s	https://github.com/mryfmo/dotfiles/actions/runs/37871306061/job/113629800139	
public-bootstrap (ubuntu-24.04, server)	pass	6m47s	https://github.com/mryfmo/dotfiles/actions/runs/37871306061/job/113629800001	
test (macos-14, client)	pass	5m43s	https://github.com/mryfmo/dotfiles/actions/runs/37871306063/job/113629834626	
test (ubuntu-24.04, client)	pass	8m4s	https://github.com/mryfmo/dotfiles/actions/runs/37871306063/job/113629834627	
test (ubuntu-24.04, server)	pass	4m53s	https://github.com/mryfmo/dotfiles/actions/runs/37871306063/job/113629834685	
test (ubuntu-26.04, client)	pass	8m3s	https://github.com/mryfmo/dotfiles/actions/runs/37871306063/job/113629834745	
validate	pass	1m25s	https://github.com/mryfmo/dotfiles/actions/runs/37871306062/job/113629799814	
2026-10-09T02:11:22Z reviews:
bot: none
comments:
rc=0

$ <recheck: every Bot review and top-level Bot comment on PR 306>
2026-10-09T02:11:47Z
60d49593	2026-10-09T01:27:44Z	COMMENTED
4225776331	60d49593	home/dot_local/bin/common/executable_herdr-agents
4225776337	60d49593	home/dot_local/bin/common/executable_herdr-agents
rc=0
```

## 7. CompactionDB memory add (main checkout, through the permission gate)

```
$ cat memadd116.sh
#!/usr/bin/env bash
M=~/Workspace/dotfiles
uv run --no-project "$M/.claude/hooks/contextdb_cli.py" --project-root "$M" memory add --kind decision --scope project --content "dotfiles-T116 (orchestrator 2026-10-09): Claude Code startup seats only the orchestrator; workers are seated on demand with \`herdr-agents --add-worker [<worktree>]\` (default: the manifest worker_worktree) and removed with \`--remove-worker\`; \`--restart-worker\` is retired; a worker identity left at a worktree at a boundary is a violation; the cap stays at three concurrent workers."
echo "rc=$?"
$ bash memadd116.sh
0a4b804a-1356-4b94-8188-93c1aeb684a9
rc=0
```

## Revise round 1 (2026-10-09)

The three stale `--restart-worker` sites, nothing else (commit ff4ffa0f).

```
$ git diff --stat bb2edb38 ff4ffa0f
 home/dot_agents/skills/agmsg-orchestration/SKILL.md |  2 +-
 home/dot_codex/rules/default.rules                  |  4 ++--
 scripts/validate-agent-assets.py                    |  4 ++--
 tests/unit/test_validate_agent_assets.py            | 11 +++++++----
 4 files changed, 12 insertions(+), 9 deletions(-)
$ make render-check; echo "rc=$?"
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
rc=0
$ uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T116-on-demand-workers-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T116-on-demand-workers-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T116-on-demand-workers-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T116-on-demand-workers-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T116-on-demand-workers-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0003cbd.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0003cbd.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0f0f2cb.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-0f0f2cb.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-46a229c.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-audit-46a229c.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T114-canonical-clone-reconcile-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-audit-282c5e8.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-audit-282c5e8.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T116-on-demand-workers-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T116-on-demand-workers-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T116-on-demand-workers-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T116-on-demand-workers-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T116-on-demand-workers-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T116-on-demand-workers-a01.md
WARN: regime-boundary: worker still seated at .claude/worktrees/worker-c (herdr-agents --remove-worker .claude/worktrees/worker-c)
WARN: regime-boundary: canonical clone ~/.local/share/chezmoi has unmerged entries (git ls-files -u); finish or abort its pull
WARN: regime-boundary: canonical clone ~/.local/share/chezmoi carries a stash (git stash list); drop only the autostash entry once its content is on origin/main, and leave any other stash to its owner
WARN: regime-boundary: canonical clone ~/.local/share/chezmoi differs from origin/main under home/, install/ or scripts/: home/dot_agents/agent-config.yaml,home/dot_agents/model-profiles.env,home/dot_claude/agents/project-map.md,home/dot_codex/modify_private_audit.config.toml,home/dot_mise/mise.lock,scripts/validate-agent-assets.py; carry a make upgrade diff as a pins task, or restore a merged one with git -C ~/.local/share/chezmoi restore -SW --source=origin/main -- <files> and drop its autostash
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles-conformance:claude-standard-dot-a001 (herdr-agents --remove-worker)
agent asset validation ok
rc=0
$ uv run python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3
Ran 112 tests in 1.398s

OK
$ MISE_STATE_DIR=$TMPDIR/mise-state mise x node npm:prettier -- prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -2
Checking formatting...
All matched files use Prettier code style!
$ make render-check > render.txt 2>&1; echo "rc=$?"; cat render.txt
rc=0
uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
$ git show HEAD:scripts/validate-agent-assets.py > scripts/validate-agent-assets.py; uv run python -m unittest tests.unit.test_validate_agent_assets -k on_demand_seating -k exact_security_profile_set 2>&1 | <filter>; (validator restored afterwards)
ERROR: README.md must document herdr-agents --restart-worker for worker relaunches
ERROR: test_agent_manifest_accepts_exact_security_profile_set
FAIL: test_agent_manifest_requires_readme_to_document_on_demand_seating
Ran 2 tests in 0.020s
FAILED (failures=1, errors=1)
$ git diff --stat
 home/dot_agents/skills/agmsg-orchestration/SKILL.md |  2 +-
 home/dot_codex/rules/default.rules                  |  4 ++--
 scripts/validate-agent-assets.py                    |  4 ++--
 tests/unit/test_validate_agent_assets.py            | 11 +++++++----
 4 files changed, 12 insertions(+), 9 deletions(-)
$ git log --oneline -1; GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles feat/on-demand-workers 2>&1 | tail -1; echo "rc=$?"
ff4ffa0f fix(regime): retire the remaining --restart-worker prescriptions
   bb2edb38..ff4ffa0f  feat/on-demand-workers -> feat/on-demand-workers
rc=0
$ <gh pr checks 306 --watch until no check is pending, then the bounded 15-minute Bot wait on ff4ffa0f>
head=ff4ffa0f55a09c36db2467f2568914608aaec4d4
checks-rc=0
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37873985165/job/113638195866	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37873985176/job/113638195840	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/37873985176/job/113638195841	
private-bootstrap (ubuntu-24.04, server)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/37873985176/job/113638195925	
public-bootstrap (macos-14, client)	pass	8m3s	https://github.com/mryfmo/dotfiles/actions/runs/37873985176/job/113638195769	
public-bootstrap (ubuntu-24.04, client)	pass	9m53s	https://github.com/mryfmo/dotfiles/actions/runs/37873985176/job/113638195976	
public-bootstrap (ubuntu-24.04, server)	pass	7m47s	https://github.com/mryfmo/dotfiles/actions/runs/37873985176/job/113638195844	
test (macos-14, client)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37873985165/job/113638243302	
test (ubuntu-24.04, client)	pass	8m5s	https://github.com/mryfmo/dotfiles/actions/runs/37873985165/job/113638243329	
test (ubuntu-24.04, server)	pass	4m45s	https://github.com/mryfmo/dotfiles/actions/runs/37873985165/job/113638243244	
test (ubuntu-26.04, client)	pass	8m33s	https://github.com/mryfmo/dotfiles/actions/runs/37873985165/job/113638243369	
validate	pass	1m15s	https://github.com/mryfmo/dotfiles/actions/runs/37873985214/job/113638195720	
2026-10-09T02:44:30Z reviews:
bot: none
comments:
rc=0

$ <recheck: every Bot review and top-level Bot comment on PR 306>
2026-10-09T02:44:45Z
60d49593	2026-10-09T01:27:44Z	COMMENTED
4225776331	60d49593	home/dot_local/bin/common/executable_herdr-agents
4225776337	60d49593	home/dot_local/bin/common/executable_herdr-agents
rc=0
```

The first `make render-check` line above was piped through the colour filter, so its `rc=` is the filter's; the unpiped run in the second block exits 0.
