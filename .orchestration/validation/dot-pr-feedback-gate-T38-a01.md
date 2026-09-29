# T38 validation (dot-pr-feedback-gate-T38-a01)

Verbatim output from worker-c at PR #210 head 98991e6, except where marked as captured during the run.

## 1. Task validation commands

```
$ git merge-base --is-ancestor origin/main HEAD && echo base-ok
base-ok
exit=0

$ git rev-parse HEAD origin/main; git log --oneline origin/main..HEAD
98991e64d99b69b3cc9f869dc7523e8fbe13abb6
6fa41a508fd30d20a8752195f6a89b15b5dc42c1
98991e6 fix(gate): fail closed on an unresolvable --base
fa934f7 feat(gate): make CodeRabbit optional and drop the review auto-trigger
f7433fc feat: carry PR #182 (PR feedback sweep and merge gate) onto main
exit=0

$ git diff --stat origin/main
 .coderabbit.yaml                                   |  18 +
 .github/workflows/agent-assets.yml                 |  10 +
 AGENTS.md                                          |   1 +
 Makefile                                           |   4 +-
 README.md                                          |  81 +++++
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   3 +-
 home/dot_agents/skills/gh-first-workflow/SKILL.md  |   2 +
 .../rules/symlink_pr-integration.md.tmpl           |   1 +
 home/dot_config/claude/rules/crit-review.md        |   2 +-
 home/dot_config/claude/rules/pr-integration.md     |   7 +
 home/dot_config/codex/AGENTS.md                    |  10 +-
 scripts/pr-feedback.py                             | 339 +++++++++++++++++
 scripts/require-crit-review.py                     | 215 ++++++++++-
 tests/unit/test_pr_feedback.py                     | 404 +++++++++++++++++++++
 tests/unit/test_require_crit_review.py             | 269 +++++++++++++-
 15 files changed, 1349 insertions(+), 17 deletions(-)
exit=0

$ make unit-test   (tail; full log in section 4)
Ran 605 tests in 99.901s

OK (skipped=1)
exit=0

$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0

$ python3 scripts/generate-agent-configs.py --check
ERROR: PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py
exit=1
# NOTE: the task spells the render check with bare python3, which lacks PyYAML here; the script's own documented form (next command) is the real check and passes.

$ uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
exit=0

$ git grep -n -e 'codex review' -e 'chatgpt-codex-connector' -e 'coderabbit-trigger' -- ':!.orchestration' ; echo "grep exit $?"
README.md:596:`codex review --commit` is not used: it accepts no prompt with `--commit` and
home/dot_local/bin/common/executable_herdr-agents:1502:    # codex review neither accepts a prompt with --commit nor emits the AGENTS.md
grep exit 0
exit=0

# NOTE: both hits are already on origin/main and state that `codex review --commit` is NOT used (README:596 and executable_herdr-agents:1502, which explain why the audit lane avoids it). This branch adds no codex-review, connector or trigger logic:
$ git grep -n -e 'codex review' -e 'chatgpt-codex-connector' -e 'coderabbit-trigger' origin/main -- ':!.orchestration' | cut -c1-110
origin/main:README.md:596:`codex review --commit` is not used: it accepts no prompt with `--commit` and
origin/main:home/dot_local/bin/common/executable_herdr-agents:1502:    # codex review neither accepts a prompt
exit=0

$ git diff origin/main...HEAD | grep -E '^\+' | grep -n -i -e 'codex review' -e 'chatgpt-codex-connector' -e 'coderabbit-trigger' ; echo "added-lines grep exit $?"
added-lines grep exit 1
exit=0

$ PR_FEEDBACK_EVIDENCE=.orchestration/validation/dot-pr-feedback-gate-T38-a01-pr-feedback.json AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/claude/t38-receipt.md python3 scripts/require-crit-review.py --base origin/main ; echo "guard exit $?"   (captured during the run at head 98991e6, evidence JSON inside the worktree)
PR feedback evidence accepted: .orchestration/validation/dot-pr-feedback-gate-T38-a01-pr-feedback.json
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
guard exit 0

$ gh pr checks 210
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36548138933/job/109339402177	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402623	
private-bootstrap (ubuntu-latest, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402508	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36548138933/job/109339461940	
private-bootstrap (ubuntu-latest, server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402568	
public-bootstrap (macos-14, client)	pass	9m3s	https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402501	
public-bootstrap (ubuntu-latest, client)	pass	9m11s	https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402248	
public-bootstrap (ubuntu-latest, server)	pass	7m8s	https://github.com/mryfmo/dotfiles/actions/runs/36548138878/job/109339402414	
test (macos-14, client)	pass	3m47s	https://github.com/mryfmo/dotfiles/actions/runs/36548138933/job/109339460572	
test (ubuntu-latest, client)	pass	6m3s	https://github.com/mryfmo/dotfiles/actions/runs/36548138933/job/109339460569	
test (ubuntu-latest, server)	pass	3m22s	https://github.com/mryfmo/dotfiles/actions/runs/36548138933/job/109339460535	
validate	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/36548138987/job/109339402651	
exit=0

$ gh pr view 210 --json number,headRefOid,mergeable,state,url
{
  "headRefOid": "98991e64d99b69b3cc9f869dc7523e8fbe13abb6",
  "mergeable": "MERGEABLE",
  "number": 210,
  "state": "OPEN",
  "url": "https://github.com/mryfmo/dotfiles/pull/210"
}
exit=0

```

## 2. Step 3: collector fallback and bot-review absence

```
$ grep -n "Prefer the base branch's collector" -A6 scripts/require-crit-review.py
408:        # Prefer the base branch's collector; only a PR that introduces it has none.
409-        collector = root / "scripts/pr-feedback.py"
410-        base_collector = run_git(["show", f"{base}:scripts/pr-feedback.py"], root)
411-        if base_collector.returncode == 0:
412-            collector = Path(temporary) / "pr-feedback.py"
413-            collector.write_text(base_collector.stdout)
414-        result = subprocess.run(
exit=0

$ git show origin/main:scripts/pr-feedback.py > /dev/null; echo "base collector on origin/main: exit $?"
fatal: path 'scripts/pr-feedback.py' exists on disk, but not in 'origin/main'
base collector on origin/main: exit 128
exit=0

$ python3 scripts/pr-feedback.py 210 --json .orchestration/validation/dot-pr-feedback-gate-T38-a01-pr-feedback.json   (captured during the run)
pr-feedback: mryfmo/dotfiles#210 head 98991e6: 15 items (annotation:notice=11, annotation:warning=1, issue_comment:comment=2, status:success=1)
exit=0

$ jq -c '{pr, head_sha, items:(.items|length), review_items:([.items[]|select(.source=="review")]|length), undispositioned:([.items[]|select((.disposition//"")=="")]|length)}' /home/moriya/Workspace/dotfiles/.orchestration/validation/dot-pr-feedback-gate-T38-a01-pr-feedback.json
{"pr":210,"head_sha":"98991e64d99b69b3cc9f869dc7523e8fbe13abb6","items":15,"review_items":0,"undispositioned":0}
exit=0

```

## 3. fix-1 (98991e6): the new test fails on the unfixed guard, passes on the fix (captured during the run)

```
$ git show HEAD:scripts/require-crit-review.py > scripts/require-crit-review.py   # HEAD was fa934f7 at the time
$ python3 -m unittest test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_unresolvable_or_option_like
FAIL: ... (base='no-such-ref')
AssertionError: 0 != 1 : PR feedback evidence accepted: .orchestration/validation/pr-feedback.json
FAIL: ... (base='--output=leak')
AssertionError: 0 != 1 : PR feedback evidence accepted: .orchestration/validation/pr-feedback.json
FAIL: ... (base='')
AssertionError: 0 != 1 : PR feedback evidence format checked only: .orchestration/validation/pr-feedback.json (set BASE=<ref> to bind it to HEAD, re-collect it, and check fixed: commits)
Ran 1 test in 0.164s
FAILED (failures=3)
$ (fixed guard restored) python3 -m unittest ...test_base_fails_closed_when_unresolvable_or_option_like
OK

$ python3 scripts/require-crit-review.py --base=no-such-ref; echo "exit $?"
--base 'no-such-ref' does not resolve to a commit; fetch it or fix BASE
exit 1
exit=0

$ python3 scripts/require-crit-review.py --base=--output=leak; echo "exit $?"; test -e leak && echo "leak exists" || echo "no file named leak was created"
--base '--output=leak' is not a git ref; pass a branch or commit such as BASE=origin/main
exit 1
no file named leak was created
exit=0

```

## 4. Full `make unit-test` log at 98991e6

```
$ make unit-test
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
test_default_store_uses_shared_helper (test_agmsg_dispatch.AgmsgDispatchTest.test_default_store_uses_shared_helper) ... ok
test_idle_wakes_once_and_reads (test_agmsg_dispatch.AgmsgDispatchTest.test_idle_wakes_once_and_reads) ... ok
test_invalid_timeout_does_not_send (test_agmsg_dispatch.AgmsgDispatchTest.test_invalid_timeout_does_not_send) ... ok
test_missing_pane_inserts_nothing (test_agmsg_dispatch.AgmsgDispatchTest.test_missing_pane_inserts_nothing) ... ok
test_rejects_identifiers_outside_the_strict_grammar (test_agmsg_dispatch.AgmsgDispatchTest.test_rejects_identifiers_outside_the_strict_grammar) ... ok
test_retry_does_not_wake_newly_working_pane (test_agmsg_dispatch.AgmsgDispatchTest.test_retry_does_not_wake_newly_working_pane) ... ok
test_timeout_is_one_shared_budget (test_agmsg_dispatch.AgmsgDispatchTest.test_timeout_is_one_shared_budget) ... ok
test_unread_retries_once_then_fails (test_agmsg_dispatch.AgmsgDispatchTest.test_unread_retries_once_then_fails) ... ok
test_wake_failure_identifies_sent_message (test_agmsg_dispatch.AgmsgDispatchTest.test_wake_failure_identifies_sent_message) ... ok
test_worker_becoming_idle_after_send_is_woken (test_agmsg_dispatch.AgmsgDispatchTest.test_worker_becoming_idle_after_send_is_woken) ... ok
test_working_does_not_wake (test_agmsg_dispatch.AgmsgDispatchTest.test_working_does_not_wake) ... ok
test_working_unread_never_wakes (test_agmsg_dispatch.AgmsgDispatchTest.test_working_unread_never_wakes) ... ok
test_rule_and_skill_share_the_registration_and_delivery_invariants (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_rule_and_skill_share_the_registration_and_delivery_invariants) ... ok
test_skill_drops_the_pane_status_gate_and_raw_pane_wakes (test_agmsg_orchestration_docs.AgmsgOrchestrationDocsParityTest.test_skill_drops_the_pane_status_gate_and_raw_pane_wakes) ... ok
test_doctor_fails_when_bwrap_is_missing_with_codex (test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_bwrap_is_missing_with_codex) ... ok
test_doctor_fails_when_the_bwrap_probe_fails (test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_the_bwrap_probe_fails) ... ok
test_doctor_is_not_applicable_without_the_restriction (test_apparmor_userns.AppArmorUsernsTest.test_doctor_is_not_applicable_without_the_restriction) ... ok
test_doctor_passes_when_the_bwrap_probe_succeeds (test_apparmor_userns.AppArmorUsernsTest.test_doctor_passes_when_the_bwrap_probe_succeeds) ... ok
test_doctor_warns_optionally_when_codex_is_missing (test_apparmor_userns.AppArmorUsernsTest.test_doctor_warns_optionally_when_codex_is_missing) ... ok
test_installer_copies_and_reloads_the_profile_with_sudo (test_apparmor_userns.AppArmorUsernsTest.test_installer_copies_and_reloads_the_profile_with_sudo) ... ok
test_installer_fails_when_loading_the_profile_fails (test_apparmor_userns.AppArmorUsernsTest.test_installer_fails_when_loading_the_profile_fails) ... ok
test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) ... ok
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
test_check_includes_ua_core_warnings (test_check_agent_runtime.CheckAgentRuntimeTest.test_check_includes_ua_core_warnings) ... /home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a490d7f10>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a490d7c40>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9c040>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a490d7e20>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9c220>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9c130>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9c400>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9c310>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9c5e0>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9c6d0>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9c7c0>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9c8b0>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9c4f0>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9c9a0>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9ca90>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9cb80>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9cc70>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a48f9ce50>
  return list(dict.fromkeys(items))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/home/moriya/.local/share/uv/python/cpython-3.13.15-linux-aarch64-gnu/lib/python3.13/re/_parser.py:449: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xee1a49548c70>
  return list(dict.fromkeys(items))
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
test_trailing_newline (test_claude_settings_merge.ClaudeSettingsMergeTest.test_trailing_newline) ... ok
test_current_only_runtime_tables_keep_current_group_order (test_codex_config_merge.CodexConfigMergeTest.test_current_only_runtime_tables_keep_current_group_order) ... ok
test_fresh_machine_outputs_managed_baseline (test_codex_config_merge.CodexConfigMergeTest.test_fresh_machine_outputs_managed_baseline) ... ok
test_managed_permgate_replaces_stale_private_ccgate_hook (test_codex_config_merge.CodexConfigMergeTest.test_managed_permgate_replaces_stale_private_ccgate_hook) ... ok
test_managed_templates_are_rendered_before_merge (test_codex_config_merge.CodexConfigMergeTest.test_managed_templates_are_rendered_before_merge) ... ok
test_managed_wins_for_managed_keys (test_codex_config_merge.CodexConfigMergeTest.test_managed_wins_for_managed_keys) ... ok
test_repeated_runtime_tables_are_preserved_in_order (test_codex_config_merge.CodexConfigMergeTest.test_repeated_runtime_tables_are_preserved_in_order) ... ok
test_runtime_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_are_preserved) ... ok
test_runtime_tables_seed_from_managed_when_absent (test_codex_config_merge.CodexConfigMergeTest.test_runtime_tables_seed_from_managed_when_absent) ... ok
test_unknown_current_tables_are_preserved (test_codex_config_merge.CodexConfigMergeTest.test_unknown_current_tables_are_preserved) ... ok
test_working_tree_placeholder_falls_back_to_source_dir_parent (test_codex_config_merge.CodexConfigMergeTest.test_working_tree_placeholder_falls_back_to_source_dir_parent) ... ok
test_working_tree_placeholder_prefers_env_override (test_codex_config_merge.CodexConfigMergeTest.test_working_tree_placeholder_prefers_env_override) ... ok
test_missing_trusted_runtime_is_silent (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_missing_trusted_runtime_is_silent) ... ok
test_non_opted_project_is_silent_even_with_trusted_runtime (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_non_opted_project_is_silent_even_with_trusted_runtime) ... ok
test_project_cli_is_data_only_and_trusted_cli_gets_explicit_root (test_contextdb_codex_notify.ContextdbCodexNotifyTest.test_project_cli_is_data_only_and_trusted_cli_gets_explicit_root) ... ok
test_coverage_gems_are_compatible_and_exact (test_files_fixture.FilesFixtureTest.test_coverage_gems_are_compatible_and_exact) ... ok
test_fixture_uses_chezmoi_binary_outside_mise_shims (test_files_fixture.FilesFixtureTest.test_fixture_uses_chezmoi_binary_outside_mise_shims) ... ok
test_legacy_file_workflows_initialize_required_fixture_paths (test_files_fixture.FilesFixtureTest.test_legacy_file_workflows_initialize_required_fixture_paths) ... ok
test_absent_worker_profile_renders_no_env_line (test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_profile_renders_no_env_line) ... ok
test_absent_worker_worktree_renders_no_env_line (test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_worktree_renders_no_env_line) ... ok
test_asset_constant_must_be_assigned_exactly_once (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constant_must_be_assigned_exactly_once) ... ok
test_asset_constants_render_into_their_files (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constants_render_into_their_files) ... ok
test_asset_pin_must_be_a_plain_value (test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_pin_must_be_a_plain_value) ... ok
test_audit_profile_renders_read_only_sandbox_override (test_generate_agent_configs.GenerateAgentConfigsTest.test_audit_profile_renders_read_only_sandbox_override) ... ok
test_check_reports_asset_render_drift (test_generate_agent_configs.GenerateAgentConfigsTest.test_check_reports_asset_render_drift) ... ok
test_claude_deny_rules_use_edit_for_file_mutations (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_deny_rules_use_edit_for_file_mutations) ... ok
test_claude_settings_render_interactive_advisor_only_when_set (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_interactive_advisor_only_when_set) ... ok
test_claude_settings_renders_session_start_hooks (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_settings_use_interactive_profile_with_permgate (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_use_interactive_profile_with_permgate) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_codex_config_renders_permgate_permission_request (test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_permgate_permission_request) ... ok
test_codex_config_renders_working_tree_project_key (test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_working_tree_project_key) ... ok
test_expected_outputs_uses_codex_baseline_path (test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
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
test_worker_kind_defaults_to_codex (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_kind_defaults_to_codex) ... ok
test_worker_worktree_outside_claude_worktrees_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_worktree_outside_claude_worktrees_fails) ... ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ok
test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options (test_herdr_agents.HerdrAgentsTest.test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options) ... ok
test_add_worker_refuses_an_undefined_profile_before_any_change (test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_an_undefined_profile_before_any_change) ... ok
test_add_worker_rejects_a_worktree_outside_claude_worktrees (test_herdr_agents.HerdrAgentsTest.test_add_worker_rejects_a_worktree_outside_claude_worktrees) ... ok
test_add_worker_reuses_a_seated_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seated_workspace) ... ok
test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args (test_herdr_agents.HerdrAgentsTest.test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args) ... ok
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
test_attach_noops_without_herdr_environment (test_herdr_agents.HerdrAgentsTest.test_attach_noops_without_herdr_environment) ... ok
test_attach_ratio_repair_skips_unsafe_layouts (test_herdr_agents.HerdrAgentsTest.test_attach_ratio_repair_skips_unsafe_layouts) ... ok
test_attach_rejects_invalid_derived_agent_name (test_herdr_agents.HerdrAgentsTest.test_attach_rejects_invalid_derived_agent_name) ... ok
test_attach_repair_splits_the_missing_worker_pane_in_its_worktree (test_herdr_agents.HerdrAgentsTest.test_attach_repair_splits_the_missing_worker_pane_in_its_worktree) ... ok
test_attach_repairs_codex_claude_order_with_one_swap (test_herdr_agents.HerdrAgentsTest.test_attach_repairs_codex_claude_order_with_one_swap) ... ok
test_attach_repairs_skewed_widths_to_equal_halves (test_herdr_agents.HerdrAgentsTest.test_attach_repairs_skewed_widths_to_equal_halves) ... ok
test_attach_reports_agmsg_skip_when_not_installed (test_herdr_agents.HerdrAgentsTest.test_attach_reports_agmsg_skip_when_not_installed) ... ok
test_attach_skips_delivery_when_turn_hook_exists (test_herdr_agents.HerdrAgentsTest.test_attach_skips_delivery_when_turn_hook_exists) ... ok
test_attach_warns_after_one_nonconverging_resize (test_herdr_agents.HerdrAgentsTest.test_attach_warns_after_one_nonconverging_resize) ... ok
test_attach_warns_when_multiple_agmsg_identities_exist (test_herdr_agents.HerdrAgentsTest.test_attach_warns_when_multiple_agmsg_identities_exist) ... ok
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
test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot (test_herdr_agents.HerdrAgentsTest.test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot) ... ok
test_audit_uses_manifest_audit_codex_args (test_herdr_agents.HerdrAgentsTest.test_audit_uses_manifest_audit_codex_args) ... ok
test_audit_verdict_gate_reads_only_the_final_codex_block (test_herdr_agents.HerdrAgentsTest.test_audit_verdict_gate_reads_only_the_final_codex_block) ... ok
test_audit_waits_for_the_prompt_on_a_new_audit_tab (test_herdr_agents.HerdrAgentsTest.test_audit_waits_for_the_prompt_on_a_new_audit_tab) ... ok
test_bare_herdr_in_ghostty_starts_plain_session (test_herdr_agents.HerdrAgentsTest.test_bare_herdr_in_ghostty_starts_plain_session) ... ok
test_bare_herdr_outside_ghostty_uses_real_cli (test_herdr_agents.HerdrAgentsTest.test_bare_herdr_outside_ghostty_uses_real_cli) ... ok
test_bootstrap_accepts_same_identity_in_multiple_teams (test_herdr_agents.HerdrAgentsTest.test_bootstrap_accepts_same_identity_in_multiple_teams) ... ok
test_bootstrap_only_creates_missing_herdr_log_directory (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_creates_missing_herdr_log_directory) ... ok
test_bootstrap_only_does_not_call_herdr_or_agents (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_does_not_call_herdr_or_agents) ... ok
test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing) ... ok
test_bootstrap_only_sets_each_missing_delivery_once (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_sets_each_missing_delivery_once) ... ok
test_bootstrap_only_skips_all_delivery_when_both_hooks_exist (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_all_delivery_when_both_hooks_exist) ... ok
test_bootstrap_only_skips_home_without_agmsg_calls (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_home_without_agmsg_calls) ... ok
test_bootstrap_only_warns_for_missing_claude_identity_without_joining (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_missing_claude_identity_without_joining) ... ok
test_bootstrap_only_warns_for_multiple_claude_identities (test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_multiple_claude_identities) ... ok
test_bootstrap_with_claude_worker_accepts_two_claude_identities (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_accepts_two_claude_identities) ... ok
test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_hints_at_a_missing_worker_identity) ... ok
test_bootstrap_with_claude_worker_leaves_codex_hooks_alone (test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_leaves_codex_hooks_alone) ... ok
test_claude_agent_accepts_manifest_profile_arguments_for_e2e (test_herdr_agents.HerdrAgentsTest.test_claude_agent_accepts_manifest_profile_arguments_for_e2e) ... ok
test_claude_repair_skips_just_restarted_codex_pane_without_agent_field (test_herdr_agents.HerdrAgentsTest.test_claude_repair_skips_just_restarted_codex_pane_without_agent_field) ... ok
test_claude_settings_add_herdr_attach_session_hook (test_herdr_agents.HerdrAgentsTest.test_claude_settings_add_herdr_attach_session_hook) ... ok
test_claude_worker_sharing_the_orchestrator_identity_is_refused (test_herdr_agents.HerdrAgentsTest.test_claude_worker_sharing_the_orchestrator_identity_is_refused) ... ok
test_claude_worker_with_a_registered_worker_identity_proceeds (test_herdr_agents.HerdrAgentsTest.test_claude_worker_with_a_registered_worker_identity_proceeds) ... ok
test_codex_profile_defaults_to_generated_interactive_profile (test_herdr_agents.HerdrAgentsTest.test_codex_profile_defaults_to_generated_interactive_profile) ... ok
test_codex_profile_env_override_wins_over_generated_profile (test_herdr_agents.HerdrAgentsTest.test_codex_profile_env_override_wins_over_generated_profile) ... ok
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
test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_moves_a_reused_empty_pane_into_the_worktree) ... ok
test_full_mode_heal_never_starts_the_worker_in_the_audit_pane (test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_starts_the_worker_in_the_audit_pane) ... ok
test_full_mode_heals_nothing_in_a_healthy_self_named_pair (test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_nothing_in_a_healthy_self_named_pair) ... ok
test_full_mode_reuses_agentless_worker_pane_in_attach_labeled_workspace (test_herdr_agents.HerdrAgentsTest.test_full_mode_reuses_agentless_worker_pane_in_attach_labeled_workspace) ... ok
test_full_mode_skips_agmsg_bootstrap_for_home (test_herdr_agents.HerdrAgentsTest.test_full_mode_skips_agmsg_bootstrap_for_home) ... ok
test_full_mode_splits_the_worker_pane_in_its_worktree (test_herdr_agents.HerdrAgentsTest.test_full_mode_splits_the_worker_pane_in_its_worktree) ... ok
test_ghostty_config_does_not_auto_start_herdr_session (test_herdr_agents.HerdrAgentsTest.test_ghostty_config_does_not_auto_start_herdr_session) ... ok
test_ghostty_herdr_starts_plain_workspace (test_herdr_agents.HerdrAgentsTest.test_ghostty_herdr_starts_plain_workspace) ... ok
test_herdr_prefix_alt_a_runs_helper_from_active_pane (test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_alt_a_runs_helper_from_active_pane) ... ok
test_herdr_prefix_f_opens_file_viewer_popup (test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_f_opens_file_viewer_popup) ... ok
test_herdr_session_does_not_prebuild_agent_layout (test_herdr_agents.HerdrAgentsTest.test_herdr_session_does_not_prebuild_agent_layout) ... ok
test_herdr_session_execs_herdr_without_prebuilding_agents (test_herdr_agents.HerdrAgentsTest.test_herdr_session_execs_herdr_without_prebuilding_agents) ... ok
test_herdr_session_passes_syntax_check (test_herdr_agents.HerdrAgentsTest.test_herdr_session_passes_syntax_check) ... ok
test_herdr_session_rejects_arguments (test_herdr_agents.HerdrAgentsTest.test_herdr_session_rejects_arguments) ... ok
test_herdr_with_args_in_ghostty_uses_real_cli (test_herdr_agents.HerdrAgentsTest.test_herdr_with_args_in_ghostty_uses_real_cli) ... ok
test_interactive_ghostty_shell_attaches_plain_session (test_herdr_agents.HerdrAgentsTest.test_interactive_ghostty_shell_attaches_plain_session) ... ok
test_make_update_and_upgrade_include_agmsg_bootstrap (test_herdr_agents.HerdrAgentsTest.test_make_update_and_upgrade_include_agmsg_bootstrap) ... ok
test_mixed_legacy_and_seat_labels_are_one_pair (test_herdr_agents.HerdrAgentsTest.test_mixed_legacy_and_seat_labels_are_one_pair) ... ok
test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout (test_herdr_agents.HerdrAgentsTest.test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout) ... ok
test_pane_creation_propagates_explicit_fpath (test_herdr_agents.HerdrAgentsTest.test_pane_creation_propagates_explicit_fpath) ... ok
test_registered_agent_not_ready_waits_for_idle_without_duplicate_start (test_herdr_agents.HerdrAgentsTest.test_registered_agent_not_ready_waits_for_idle_without_duplicate_start) ... ok
test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record (test_herdr_agents.HerdrAgentsTest.test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record) ... ok
test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes (test_herdr_agents.HerdrAgentsTest.test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes) ... ok
test_remove_worker_force_retries_a_failed_graceful_despawn (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_retries_a_failed_graceful_despawn) ... ok
test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds) ... ok
test_remove_worker_forces_despawn_when_graceful_reports_needs_force (test_herdr_agents.HerdrAgentsTest.test_remove_worker_forces_despawn_when_graceful_reports_needs_force) ... ok
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
test_start_keeps_node_global_without_mise_tool_install (test_herdr_agents.HerdrAgentsTest.test_start_keeps_node_global_without_mise_tool_install) ... ok
test_start_removes_node_global_agent_clis_shadowing_mise (test_herdr_agents.HerdrAgentsTest.test_start_removes_node_global_agent_clis_shadowing_mise) ... ok
test_start_skips_node_global_removal_without_stray (test_herdr_agents.HerdrAgentsTest.test_start_skips_node_global_removal_without_stray) ... ok
test_successful_agent_start_does_not_poll_agent_list (test_herdr_agents.HerdrAgentsTest.test_successful_agent_start_does_not_poll_agent_list) ... ok
test_two_self_named_pair_workspaces_still_refuse (test_herdr_agents.HerdrAgentsTest.test_two_self_named_pair_workspaces_still_refuse) ... ok
test_uses_initial_workspace_pane_for_claude_and_splits_codex_right (test_herdr_agents.HerdrAgentsTest.test_uses_initial_workspace_pane_for_claude_and_splits_codex_right) ... ok
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
test_worker_profile_env_takes_priority_over_deprecated_codex_alias (test_herdr_agents.HerdrAgentsTest.test_worker_profile_env_takes_priority_over_deprecated_codex_alias) ... ok
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
test_bash_credentials_skip_classifier (test_permgate.PermgateTest.test_bash_credentials_skip_classifier) ... ok
test_bench_runs_five_layer_two_fixtures (test_permgate.PermgateTest.test_bench_runs_five_layer_two_fixtures) ... ok
test_bench_with_no_eligible_fixtures_is_not_ready (test_permgate.PermgateTest.test_bench_with_no_eligible_fixtures_is_not_ready) ... ok
test_classifier_receives_metadata_without_raw_values (test_permgate.PermgateTest.test_classifier_receives_metadata_without_raw_values) ... ok
test_classifier_rejects_path_qualified_executables (test_permgate.PermgateTest.test_classifier_rejects_path_qualified_executables) ... ok
test_claude_and_codex_hook_outputs_match_golden_bytes (test_permgate.PermgateTest.test_claude_and_codex_hook_outputs_match_golden_bytes) ... ok
test_cli_bash_send_lane_is_removed (test_permgate.PermgateTest.test_cli_bash_send_lane_is_removed) ... ok
test_cli_catastrophic_deny_precedes_workspace (test_permgate.PermgateTest.test_cli_catastrophic_deny_precedes_workspace) ... ok
test_cli_policy_pins_shared_layers_and_disables_llm (test_permgate.PermgateTest.test_cli_policy_pins_shared_layers_and_disables_llm) ... ok
test_cli_protocol_emits_each_compact_decision (test_permgate.PermgateTest.test_cli_protocol_emits_each_compact_decision) ... ok
test_cli_protocol_internal_failure_is_nonzero (test_permgate.PermgateTest.test_cli_protocol_internal_failure_is_nonzero) ... ok
test_cli_protocol_rejects_malformed_normalized_action (test_permgate.PermgateTest.test_cli_protocol_rejects_malformed_normalized_action) ... ok
test_cli_read_allows_plain_resolvable_path_outside_workspace (test_permgate.PermgateTest.test_cli_read_allows_plain_resolvable_path_outside_workspace) ... ok
test_cli_read_denies_each_sensitive_path_family (test_permgate.PermgateTest.test_cli_read_denies_each_sensitive_path_family) ... ok
test_cli_read_resolves_symlinks_and_asks_for_unresolvable_paths (test_permgate.PermgateTest.test_cli_read_resolves_symlinks_and_asks_for_unresolvable_paths) ... ok
test_cli_reuses_every_shared_bash_allow_pattern (test_permgate.PermgateTest.test_cli_reuses_every_shared_bash_allow_pattern) ... ok
test_cli_workspace_allows_in_cwd_read_write_and_edit (test_permgate.PermgateTest.test_cli_workspace_allows_in_cwd_read_write_and_edit) ... ok
test_cli_workspace_asks_for_looping_or_missing_parent (test_permgate.PermgateTest.test_cli_workspace_asks_for_looping_or_missing_parent) ... ok
test_cli_workspace_never_writes_through_final_symlink (test_permgate.PermgateTest.test_cli_workspace_never_writes_through_final_symlink) ... ok
test_cli_workspace_rejects_path_escapes_root_and_symlink_escape (test_permgate.PermgateTest.test_cli_workspace_rejects_path_escapes_root_and_symlink_escape) ... ok
test_cli_workspace_resolves_macos_var_alias_identically (test_permgate.PermgateTest.test_cli_workspace_resolves_macos_var_alias_identically) ... skipped 'macOS /var alias only'
test_codex_classifier_is_ephemeral_read_only_and_hook_free (test_permgate.PermgateTest.test_codex_classifier_is_ephemeral_read_only_and_hook_free) ... ok
test_codex_classifier_never_reads_the_callers_open_stdin (test_permgate.PermgateTest.test_codex_classifier_never_reads_the_callers_open_stdin) ... ok
test_each_agent_uses_only_its_own_authenticated_cli (test_permgate.PermgateTest.test_each_agent_uses_only_its_own_authenticated_cli) ... ok
test_enabled_classifier_only_allows_whitelisted_confident_category (test_permgate.PermgateTest.test_enabled_classifier_only_allows_whitelisted_confident_category) ... ok
test_git_diff_output_option_is_never_automatically_allowed (test_permgate.PermgateTest.test_git_diff_output_option_is_never_automatically_allowed) ... ok
test_invalid_classifier_policy_fields_fail_closed (test_permgate.PermgateTest.test_invalid_classifier_policy_fields_fail_closed) ... ok
test_invalid_policy_returns_ask_and_logs_config_error (test_permgate.PermgateTest.test_invalid_policy_returns_ask_and_logs_config_error) ... ok
test_layer_one_allows_documented_claude_and_codex_contracts (test_permgate.PermgateTest.test_layer_one_allows_documented_claude_and_codex_contracts) ... ok
test_layer_one_deny_uses_both_hook_output_schemas (test_permgate.PermgateTest.test_layer_one_deny_uses_both_hook_output_schemas) ... ok
test_log_shape_redacts_command_and_output (test_permgate.PermgateTest.test_log_shape_redacts_command_and_output) ... ok
test_malformed_classifier_output_returns_ask (test_permgate.PermgateTest.test_malformed_classifier_output_returns_ask) ... ok
test_missing_or_nonzero_classifier_returns_ask (test_permgate.PermgateTest.test_missing_or_nonzero_classifier_returns_ask) ... ok
test_mutating_or_executable_read_options_never_reach_classifier (test_permgate.PermgateTest.test_mutating_or_executable_read_options_never_reach_classifier) ... ok
test_provider_enablement_never_enables_the_sibling_provider (test_permgate.PermgateTest.test_provider_enablement_never_enables_the_sibling_provider) ... ok
test_recursion_sentinel_is_a_complete_no_op (test_permgate.PermgateTest.test_recursion_sentinel_is_a_complete_no_op) ... ok
test_script_named_version_is_not_a_version_check (test_permgate.PermgateTest.test_script_named_version_is_not_a_version_check) ... ok
test_shadow_log_contains_reviewable_non_secret_classification (test_permgate.PermgateTest.test_shadow_log_contains_reviewable_non_secret_classification) ... ok
test_structured_secret_skips_classifier_and_redacts_summary (test_permgate.PermgateTest.test_structured_secret_skips_classifier_and_redacts_summary) ... ok
test_timeout_returns_ask_within_hook_cap (test_permgate.PermgateTest.test_timeout_returns_ask_within_hook_cap) ... ok
test_unconstrained_native_reads_never_reach_classifier (test_permgate.PermgateTest.test_unconstrained_native_reads_never_reach_classifier) ... ok
test_unknown_shadow_classification_returns_native_ask (test_permgate.PermgateTest.test_unknown_shadow_classification_returns_native_ask) ... ok
test_annotations_keep_every_level_even_on_passing_checks (test_pr_feedback.PrFeedbackTest.test_annotations_keep_every_level_even_on_passing_checks) ... ok
test_bots_are_detected_from_type_login_or_app (test_pr_feedback.PrFeedbackTest.test_bots_are_detected_from_type_login_or_app) ... ok
test_collects_every_feedback_source_for_the_head (test_pr_feedback.PrFeedbackTest.test_collects_every_feedback_source_for_the_head) ... ok
test_commit_status_keeps_the_latest_state_per_context (test_pr_feedback.PrFeedbackTest.test_commit_status_keeps_the_latest_state_per_context) ... ok
test_every_item_carries_the_disposition_schema (test_pr_feedback.PrFeedbackTest.test_every_item_carries_the_disposition_schema) ... ok
test_gh_never_receives_forced_colour (test_pr_feedback.PrFeedbackTest.test_gh_never_receives_forced_colour) ... ok
test_main_writes_the_document_to_json (test_pr_feedback.PrFeedbackTest.test_main_writes_the_document_to_json) ... ok
test_only_non_passing_check_runs_become_items (test_pr_feedback.PrFeedbackTest.test_only_non_passing_check_runs_become_items) ... ok
test_review_comments_carry_thread_resolution_across_pages (test_pr_feedback.PrFeedbackTest.test_review_comments_carry_thread_resolution_across_pages) ... ok
test_thread_state_covers_comments_beyond_the_first_page (test_pr_feedback.PrFeedbackTest.test_thread_state_covers_comments_beyond_the_first_page) ... ok
test_unauthenticated_gh_exits_non_zero (test_pr_feedback.PrFeedbackTest.test_unauthenticated_gh_exits_non_zero) ... ok
test_rule_mirrors_and_skills_carry_the_same_requirements (test_pr_feedback.PrIntegrationRuleParityTest.test_rule_mirrors_and_skills_carry_the_same_requirements) ... ok
test_rule_symlink_points_at_the_rule (test_pr_feedback.PrIntegrationRuleParityTest.test_rule_symlink_points_at_the_rule) ... ok
test_bump_writes_only_the_four_pins_through_set_asset (test_release_asset_pins.ReleaseAssetPinsTest.test_bump_writes_only_the_four_pins_through_set_asset) ... ok
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
test_base_fails_closed_when_unresolvable_or_option_like (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_unresolvable_or_option_like) ... ok
test_base_requires_pr_feedback_evidence (test_require_crit_review.ReviewGuardTest.test_base_requires_pr_feedback_evidence) ... ok
test_base_reviews_committed_branch_changes (test_require_crit_review.ReviewGuardTest.test_base_reviews_committed_branch_changes) ... ok
test_broad_diff_requires_review (test_require_crit_review.ReviewGuardTest.test_broad_diff_requires_review) ... ok
test_explicit_disable_skips_guard (test_require_crit_review.ReviewGuardTest.test_explicit_disable_skips_guard) ... ok
test_high_risk_markdown_change_requires_review (test_require_crit_review.ReviewGuardTest.test_high_risk_markdown_change_requires_review) ... ok
test_large_untracked_file_requires_broad_diff_review (test_require_crit_review.ReviewGuardTest.test_large_untracked_file_requires_broad_diff_review) ... ok
test_native_reviewed_environment_rejects_human_reviewer (test_require_crit_review.ReviewGuardTest.test_native_reviewed_environment_rejects_human_reviewer) ... ok
test_native_reviewed_without_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_native_reviewed_without_evidence_still_requires_review) ... ok
test_no_diff_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_no_diff_does_not_require_review) ... ok
test_pr_feedback_accepts_complete_evidence_without_a_bot_review (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_evidence_without_a_bot_review) ... ok
test_pr_feedback_accepts_complete_root_cause_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_root_cause_dispositions) ... ok
test_pr_feedback_evidence_file_is_not_counted_as_a_change (test_require_crit_review.ReviewGuardTest.test_pr_feedback_evidence_file_is_not_counted_as_a_change) ... ok
test_pr_feedback_fails_when_the_collector_cannot_run (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fails_when_the_collector_cannot_run) ... ok
test_pr_feedback_fixed_commit_must_be_in_the_pr_range (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fixed_commit_must_be_in_the_pr_range) ... ok
test_pr_feedback_must_be_collected_for_the_current_head (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_be_collected_for_the_current_head) ... ok
test_pr_feedback_must_cover_every_currently_collected_item (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_cover_every_currently_collected_item) ... ok
test_pr_feedback_rejects_evidence_outside_the_repository (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_evidence_outside_the_repository) ... ok
test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) ... ok
test_pr_feedback_requires_the_github_head_to_match (test_require_crit_review.ReviewGuardTest.test_pr_feedback_requires_the_github_head_to_match) ... ok
test_pr_feedback_uses_the_base_collector_not_the_prs_own (test_require_crit_review.ReviewGuardTest.test_pr_feedback_uses_the_base_collector_not_the_prs_own) ... ok
test_pr_feedback_without_base_is_only_format_checked (test_require_crit_review.ReviewGuardTest.test_pr_feedback_without_base_is_only_format_checked) ... ok
test_reviewed_environment_satisfies_required_review (test_require_crit_review.ReviewGuardTest.test_reviewed_environment_satisfies_required_review) ... ok
test_reviewed_with_blank_evidence_values_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_blank_evidence_values_still_requires_review) ... ok
test_reviewed_with_incomplete_evidence_still_requires_review (test_require_crit_review.ReviewGuardTest.test_reviewed_with_incomplete_evidence_still_requires_review) ... ok
test_small_docs_only_change_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_small_docs_only_change_does_not_require_review) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok
test_agent_asset_update_runs_gh_extension_ensure (test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_fanout_applies_profile_args_from_generated_fragment (test_runtime_health.RuntimeHealthTest.test_agent_fanout_applies_profile_args_from_generated_fragment) ... ok
test_agent_fanout_preserves_caller_umask_for_child_agents (test_runtime_health.RuntimeHealthTest.test_agent_fanout_preserves_caller_umask_for_child_agents) ... ok
test_agent_fanout_refuses_symlink_artifacts (test_runtime_health.RuntimeHealthTest.test_agent_fanout_refuses_symlink_artifacts) ... ok
test_agent_fanout_restricts_preexisting_output_artifacts (test_runtime_health.RuntimeHealthTest.test_agent_fanout_restricts_preexisting_output_artifacts) ... ok
test_agent_launchers_do_not_hardcode_model_ids (test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agent_runs_are_private_and_ignored (test_runtime_health.RuntimeHealthTest.test_agent_runs_are_private_and_ignored) ... ok
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
test_upgrade_reports_ccr_adoption_gate_values (test_runtime_health.RuntimeHealthTest.test_upgrade_reports_ccr_adoption_gate_values) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_skips_ccr_notice_when_gh_is_unavailable (test_runtime_health.RuntimeHealthTest.test_upgrade_skips_ccr_notice_when_gh_is_unavailable) ... ok
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
test_nix_inputs_lock_and_ci_use_2605 (test_supply_chain_policy.SupplyChainPolicyTest.test_nix_inputs_lock_and_ci_use_2605) ... ok
test_renovate_owns_dependency_update_notifications (test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications) ... ok
test_setup_ci_rejects_and_preserves_local_drift (test_supply_chain_policy.SupplyChainPolicyTest.test_setup_ci_rejects_and_preserves_local_drift) ... ok
test_sheldon_git_sources_have_revisions (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_git_sources_have_revisions) ... ok
test_sheldon_uses_locked_crates_io_source (test_supply_chain_policy.SupplyChainPolicyTest.test_sheldon_uses_locked_crates_io_source) ... ok
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
test_leaves_allowed_placeholders_the_scan_accepts (test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_every_match_in_place_and_reports_counts (test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_missing_file_exits_2_without_touching_others (test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
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
test_assets_reject_each_incomplete_declaration (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
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
test_recursive_scans_skip_nested_git_trees_only (test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/validate-agent-assets-test-7lacmcxh/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: /Users/mryfmo/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
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
Ran 605 tests in 99.901s

OK (skipped=1)
exit=0
```
