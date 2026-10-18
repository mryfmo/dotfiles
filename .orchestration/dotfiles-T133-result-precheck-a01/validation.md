---
task_id: dotfiles-T133-result-precheck-a01
round: 1
amendment: 1
---

# Validation

Base `origin/main` 99a4a80f, worker-c worktree, inside the Claude seat's Bash sandbox. The Check runner, the mutation check and the default precheck ran on code head de167fa1; 105e42cf (Amendment 2) changes only two comment lines of `result-precheck.sh` (the diff is in the last section), the proof precheck ran on 105e42cf, and after the Bot's review the fix round a7b0da2f (last sections) re-ran the two modules and the precheck. The final commit adds only `.orchestration/dotfiles-T133-result-precheck-a01/` evidence. Every block is verbatim output with the real exit status.

## Item 0 (the parked PR)

```text
$ git ls-remote origin refs/heads/tools/omp-config-render
2e978db7c4325f477630234a78a6f7701e45c92e	refs/heads/tools/omp-config-render
exit=0
$ gh pr view 406 --json number,headRefName,headRefOid,isDraft,title,state
{"headRefName":"tools/omp-config-render","headRefOid":"2e978db7c4325f477630234a78a6f7701e45c92e","isDraft":true,"number":406,"state":"OPEN","title":"feat(agents): render omp's default model role from the manifest (T129 omp-config-render a01)"}
exit=0
```

## The Check (all but the precheck), run while the first precheck was still running

`make validate-agent-assets` failed here only because the running precheck's `precheck-unit-test.log` was not yet masked (the precheck masks its logs at the end); its rerun after the precheck, in the next block, passes. `make format` fails on `origin/main`'s own twelve files outside CI's scope (Amendment 1); CI's three commands in CI's scopes, the precheck's `format` check, pass.

```text
$ git rev-parse HEAD origin/main
de167fa1f48d3f7d3653b3643c43b2f7acf7e149
99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
exit=0

$ make render-check
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
exit=0

$ make validate-agent-assets > vaa.txt 2>&1
exit=2
$ grep -v '^WARN: regime-boundary' vaa.txt
uv run --offline --with pyyaml scripts/validate-agent-assets.py
ERROR: .orchestration/dotfiles-T133-result-precheck-a01/precheck-unit-test.log names a home directory; normalise it with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`
make: *** [validate-agent-assets] Error 1
$ grep T133 vaa.txt
ERROR: .orchestration/dotfiles-T133-result-precheck-a01/precheck-unit-test.log names a home directory; normalise it with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`

$ shellcheck -x scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push scripts/orchestrator/dispatch.sh
exit=0

$ shfmt -d -i 4 -sr scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push scripts/orchestrator/dispatch.sh
exit=0

$ git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs shfmt -i 4 -sr -d
exit=0

$ git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check
62 files already formatted
exit=0

$ git ls-files -z '*.md' | xargs -0 prettier --check
Checking formatting...
All matched files use Prettier code style!
exit=0

$ make format > format.txt 2>&1
exit=2
$ grep -E '^--- ' format.txt | sed 's/^--- //; s/\.orig$//' | sort -u
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
home/dot_claude/hooks/executable_project-map-reload.sh
tests/install/macos/common/brew.bats

$ uv run python -m unittest tests.unit.test_result_precheck tests.unit.test_orchestrator_tools -v
test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required (tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required) ... ok
test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure) ... ok
test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern) ... ok
test_precheck_exits_1_and_records_ok_false_for_each_failing_check (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_exits_1_and_records_ok_false_for_each_failing_check) ... ok
test_precheck_records_the_local_review_as_deferred_by_default (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_records_the_local_review_as_deferred_by_default) ... ok
test_precheck_secrets_mode_counts_and_never_prints_the_match (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_secrets_mode_counts_and_never_prints_the_match) ... ok
test_precheck_selector_proof_requires_red_on_previous_head_and_green_on_head (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_selector_proof_requires_red_on_previous_head_and_green_on_head) ... ok
test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record) ... ok
test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit) ... ok
test_boundary_commits_pushes_and_queues_the_pr (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_commits_pushes_and_queues_the_pr) ... ok
test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path) ... ok
test_boundary_deletes_a_name_with_glob_characters_literally (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_deletes_a_name_with_glob_characters_literally) ... ok
test_boundary_keeps_a_name_with_a_newline_one_path (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_keeps_a_name_with_a_newline_one_path) ... ok
test_boundary_stops_before_commit_when_the_validator_fails (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_stops_before_commit_when_the_validator_fails) ... ok
test_bus_read_closes_a_task_on_any_non_revise_acceptance (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_closes_a_task_on_any_non_revise_acceptance) ... ok
test_bus_read_ignores_closers_between_other_endpoints (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_ignores_closers_between_other_endpoints) ... ok
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event) ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_refuses_a_read_that_reaches_its_limit) ... ok
test_bus_read_skips_and_counts_malformed_rows (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_skips_and_counts_malformed_rows) ... ok
test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash) ... ok
test_design_keydiff_names_the_changed_invariant (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_design_keydiff_names_the_changed_invariant) ... ok
test_dispatch_line_grammar_table (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_line_grammar_table) ... ok
test_dispatch_passes_the_line_byte_identical (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_passes_the_line_byte_identical) ... ok
test_dispatch_reads_a_bounded_history_window (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_reads_a_bounded_history_window) ... ok
test_dispatch_record_path_tokenizes_and_locks (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_record_path_tokenizes_and_locks) ... ok
test_dispatch_records_the_sent_line_with_its_read_marker (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_records_the_sent_line_with_its_read_marker) ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file) ... ok
test_dispatch_refuses_a_line_without_a_task_id (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_line_without_a_task_id) ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_malformed_record_block_before_sending) ... ok
test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields) ... ok
test_dispatch_refuses_a_task_file_failing_the_checker (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_task_file_failing_the_checker) ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line) ... ok
test_dispatch_refuses_an_unwritable_record_before_sending (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_an_unwritable_record_before_sending) ... ok
test_dispatch_refuses_malformed_lines (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_malformed_lines) ... ok
test_dispatch_resolves_its_root_without_inherited_git_variables (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_resolves_its_root_without_inherited_git_variables) ... ok
test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state) ... ok
test_ff_main_keeps_a_local_deletion_across_the_fast_forward (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_ff_main_keeps_a_local_deletion_across_the_fast_forward) ... ok
test_ff_main_keeps_local_edits_across_the_fast_forward (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_ff_main_keeps_local_edits_across_the_fast_forward) ... ok
test_fill_sweep_fills_only_a_commented_review (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_fills_only_a_commented_review) ... ok
test_fill_sweep_fills_only_notice_annotations_and_success_statuses (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_fills_only_notice_annotations_and_success_statuses) ... ok
test_fill_sweep_ignores_a_disposition_reply_from_another_login (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_ignores_a_disposition_reply_from_another_login) ... ok
test_fill_sweep_leaves_a_badged_review_body_a_gap (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_leaves_a_badged_review_body_a_gap) ... ok
test_fill_sweep_quotes_the_url_form_evidence (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_quotes_the_url_form_evidence) ... ok
test_fill_sweep_refuses_a_not_applicable_without_evidence (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_refuses_a_not_applicable_without_evidence) ... ok
test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id) ... ok
test_fill_sweep_sees_a_collision_after_the_discussion_r_strip (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_sees_a_collision_after_the_discussion_r_strip) ... ok
test_fill_sweep_selects_a_null_url_status_by_source_and_check (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_selects_a_null_url_status_by_source_and_check) ... ok
test_orch_audit_refuses_a_ledger_check_that_differs_from_head (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_refuses_a_ledger_check_that_differs_from_head) ... ok
test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt) ... ok
test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap) ... ok
test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules) ... ok
test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout) ... ok
test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree) ... ok
test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration) ... ok
test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves) ... ok
test_orch_gate_restores_the_review_worktree_when_setup_fails (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_restores_the_review_worktree_when_setup_fails) ... ok
test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree) ... ok
test_orch_gate_runs_the_gate_under_an_explicit_environment (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_runs_the_gate_under_an_explicit_environment) ... ok
test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs) ... ok
test_replay_propagates_the_command_status (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_replay_propagates_the_command_status) ... ok
test_three_repeat_prints_body_matches_and_states_a_capped_memory_count (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_prints_body_matches_and_states_a_capped_memory_count) ... ok
test_three_repeat_prints_the_records_search_line (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_prints_the_records_search_line) ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout) ... ok

----------------------------------------------------------------------
Ran 63 tests in 139.348s

OK
exit=0

$ git status --porcelain
?? .orchestration/dotfiles-T133-result-precheck-a01/learning.md
?? .orchestration/dotfiles-T133-result-precheck-a01/precheck-unit-test.log
?? .orchestration/dotfiles-T133-result-precheck-a01/report.md
?? .orchestration/dotfiles-T133-result-precheck-a01/sandbox.md
exit=0

$ git diff --numstat origin/main...HEAD
13	0	.githooks/pre-commit
24	0	.githooks/pre-push
105	0	.orchestration/dotfiles-T133-result-precheck-a01/task.md
70	1	scripts/orchestrator/dispatch.sh
242	0	scripts/orchestrator/result-precheck.sh
284	0	tests/unit/test_result_precheck.py
exit=0

```

## The validator after the precheck (non-WARN lines and this task's lines)

```text
$ make validate-agent-assets > vaa.txt 2>&1
exit=0
$ grep -v '^WARN: regime-boundary' vaa.txt
uv run --offline --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
$ grep result-precheck vaa.txt
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T133-result-precheck-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T133-result-precheck-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T133-result-precheck-a01/learning.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T133-result-precheck-a01/precheck-format.log
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T133-result-precheck-a01/precheck-render-check.log
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T133-result-precheck-a01/precheck-secrets.log
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T133-result-precheck-a01/precheck-shellcheck.log
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T133-result-precheck-a01/precheck-unit-test.log
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T133-result-precheck-a01/precheck.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T133-result-precheck-a01/report.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T133-result-precheck-a01/result.txt
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-c: .orchestration/dotfiles-T133-result-precheck-a01/sandbox.md
WARN: regime-boundary: dotfiles-T133-result-precheck-a01 S2: questions 2 >= 2 source=live
```

## Mutation check (each control disabled in a backed-up copy, its test run, the file restored and its hash verified)

```text
$ bash mutate.sh
mutation : in scripts/orchestrator/dispatch.sh -> test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required exit=1 (FAILED (failures=5))
mutation exit 0 in .githooks/pre-push -> test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern exit=1 (FAILED (failures=1))
mutation if true; then in scripts/orchestrator/result-precheck.sh -> test_precheck_secrets_mode_counts_and_never_prints_the_match exit=1 (FAILED (failures=1))
mutation exit 0 in .githooks/pre-commit -> test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure exit=1 (FAILED (failures=2, errors=1))
exit=0
```

```bash
#!/usr/bin/env bash
# Disable one control at a time in a backed-up file, run the test that should catch it, restore and verify the hash.
set -u
mutate() {
    local file=$1 old=$2 new=$3 test=$4 backup sum rc
    backup="$(mktemp "${TMPDIR%/}/mutate.XXXXXX")"
    cp -p -- "${file}" "${backup}"
    sum="$(shasum -a 256 "${file}" | cut -d' ' -f1)"
    uv run --no-project python -c 'import sys; p, o, n = sys.argv[1:4]; t = open(p).read(); assert t.count(o) == 1, o; open(p, "w").write(t.replace(o, n))' "${file}" "${old}" "${new}"
    uv run python -m unittest "tests.unit.test_result_precheck.ResultPrecheckTest.${test}" > "${backup}.log" 2>&1
    rc=$?
    cp -p -- "${backup}" "${file}"
    [[ "$(shasum -a 256 "${file}" | cut -d' ' -f1)" == "${sum}" ]] || echo "RESTORE FAILED: ${file}"
    printf 'mutation %s in %s -> %s exit=%s (%s)\n' "${new}" "${file}" "${test}" "${rc}" "$(grep -E '^(OK|FAILED)' "${backup}.log")"
    rm -f -- "${backup}" "${backup}.log"
}
mutate scripts/orchestrator/dispatch.sh 'precheck_gate "${window}"' ':' test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required
mutate .githooks/pre-push 'status=0' 'exit 0' test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern
mutate scripts/orchestrator/result-precheck.sh 'if [[ ${out} != '"'"'masker failed'"'"' ]] && cmp -s -- "$1" "${work}/copy"; then' 'if true; then' test_precheck_secrets_mode_counts_and_never_prints_the_match
mutate .githooks/pre-commit 'set -euo pipefail' 'exit 0' test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure
```

## The precheck on this head, default form (the Check's command before Amendment 2)

`unit-test` (`make unit-test`) fails 296 tests inside the sandbox; the next block shows the identical 296 fail on a pristine `origin/main` worktree in the same sandbox, none in this task's modules. The record of this run is kept below (precheck.json verbatim). Amendment 2 decided option (a) of the question of message 2111: the committed record is the `--tests` run in the last section.

```text
$ scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a01
result-precheck: unit-test exit 2
result-precheck: render-check exit 0
result-precheck: format exit 0
result-precheck: shellcheck exit 0
result-precheck: secrets exit 0
precheck=c9c80f1fde3fb65d0d0e8dd42cc73afc07a92cd6a31b60a5014124b4092fe9b1
exit=1
$ grep -E '^Ran |^(OK|FAILED)' precheck-unit-test.log
Ran 1183 tests in 825.663s
FAILED (failures=189, errors=107, skipped=2)
$ cat precheck.json
{
  "head": "de167fa1f48d3f7d3653b3643c43b2f7acf7e149",
  "tree": "2d0f51b1f5315c5fff7b55158718dcafb565bddc",
  "generated_at": "2026-10-18T05:12:05Z",
  "checks": [
    {
      "name": "unit-test",
      "ok": false,
      "exit": 2,
      "output_sha256": "bb9b8838ca0345d974dca39feb339483c3c0db2c012e94364c14f94feeaed3e1"
    },
    {
      "name": "render-check",
      "ok": true,
      "exit": 0,
      "output_sha256": "3cc07aa4e482b20772e8ba404d3c0d9e338adcd0cd2d4ff6edf14de8bf23db93"
    },
    {
      "name": "format",
      "ok": true,
      "exit": 0,
      "output_sha256": "f170e34f5d9c464c7dd7be27fb8f87bb26969019903d50b6636103c97a779796"
    },
    {
      "name": "shellcheck",
      "ok": true,
      "exit": 0,
      "output_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "name": "secrets",
      "ok": true,
      "exit": 0,
      "output_sha256": "ec427b4abbf24ab3958dd1498e28cc76113d99c85519521cfc6951635053f42a"
    },
    {
      "name": "local-review",
      "ok": null,
      "deferred": "orchestrator"
    }
  ],
  "selectors": []
}
$ cat result.txt
AGMSG-RESULT v1 task_id=dotfiles-T133-result-precheck-a01 status=blocked head=de167fa1f48d3f7d3653b3643c43b2f7acf7e149 precheck=c9c80f1fde3fb65d0d0e8dd42cc73afc07a92cd6a31b60a5014124b4092fe9b1 task_copy=247e7a44f764f3d939f18278c10e380a92909cce38583e28b1cd07d2d7a5a7a8 report=.orchestration/dotfiles-T133-result-precheck-a01/report.md validation=.orchestration/dotfiles-T133-result-precheck-a01/validation.md sandbox=.orchestration/dotfiles-T133-result-precheck-a01/sandbox.md learning=.orchestration/dotfiles-T133-result-precheck-a01/learning.md
```

## The same unit suite on `origin/main` (baselines)

```text
$ base=$(mktemp -d)/wt; git worktree add --detach "$base" origin/main; (cd "$base" && make unit-test > unit.log 2>&1); git worktree remove --force "$base"
base=99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
make unit-test exit=2
removed=0
$ grep -E '^Ran |^(OK|FAILED)' unit.log
Ran 1176 tests in 407.430s
FAILED (failures=189, errors=107, skipped=2)
$ grep -oE '^(FAIL|ERROR): test_[A-Za-z0-9_]+ \([A-Za-z0-9_.]+\)' <log> | sort, for this head and for origin/main
296 and 296 lines
cmp: identical failing sets
$ grep -c test_result_precheck\|test_orchestrator_tools <head set>
0
$ the failing set by module (this head)
 136 (test_require_crit_review.
  82 (test_herdr_agents.
  28 (test_agent_stop_gate.
  19 (test_ua_symbol_coverage.
  12 (test_update_agent_assets.
   8 (test_runtime_health.
   5 (test_gh_auth.
   4 (test_supply_chain_policy.
   2 (test_aws_cli_acquisition.
```

## The precheck in Amendment 2's form on 105e42cf (superseded by the fix round below)

```text
$ scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a01 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools
result-precheck: unit-test exit 0
result-precheck: render-check exit 0
result-precheck: format exit 0
result-precheck: shellcheck exit 0
result-precheck: secrets exit 0
precheck=862c3566250a09767c00e329a4f47c7bee1f992cb128c6400a57a0c79f476f14
exit=0
$ cat precheck.json
{
  "head": "105e42cf7f3ff4abc29eb5dfe66b90d1824321ee",
  "tree": "73c6f1d642f11aceded624b933fba9607524bf28",
  "generated_at": "2026-10-18T05:43:37Z",
  "checks": [
    {
      "name": "unit-test",
      "ok": true,
      "exit": 0,
      "output_sha256": "edbc8833dc6523c75651dc8e0546e3d035fc876e681857db778b133a93667606"
    },
    {
      "name": "render-check",
      "ok": true,
      "exit": 0,
      "output_sha256": "3cc07aa4e482b20772e8ba404d3c0d9e338adcd0cd2d4ff6edf14de8bf23db93"
    },
    {
      "name": "format",
      "ok": true,
      "exit": 0,
      "output_sha256": "f170e34f5d9c464c7dd7be27fb8f87bb26969019903d50b6636103c97a779796"
    },
    {
      "name": "shellcheck",
      "ok": true,
      "exit": 0,
      "output_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "name": "secrets",
      "ok": true,
      "exit": 0,
      "output_sha256": "ec427b4abbf24ab3958dd1498e28cc76113d99c85519521cfc6951635053f42a"
    },
    {
      "name": "local-review",
      "ok": null,
      "deferred": "orchestrator"
    }
  ],
  "selectors": []
}
$ cat result.txt
AGMSG-RESULT v1 task_id=dotfiles-T133-result-precheck-a01 status=ready_for_review head=105e42cf7f3ff4abc29eb5dfe66b90d1824321ee precheck=862c3566250a09767c00e329a4f47c7bee1f992cb128c6400a57a0c79f476f14 task_copy=05caa77f064b809185138817d869ae0b4fc52ef76863715d1e6d998134ac011f report=.orchestration/dotfiles-T133-result-precheck-a01/report.md validation=.orchestration/dotfiles-T133-result-precheck-a01/validation.md sandbox=.orchestration/dotfiles-T133-result-precheck-a01/sandbox.md learning=.orchestration/dotfiles-T133-result-precheck-a01/learning.md
```

```diff
$ git diff de167fa1 105e42cf -- scripts .githooks tests
diff --git a/scripts/orchestrator/result-precheck.sh b/scripts/orchestrator/result-precheck.sh
index c5854818..864f8dbf 100755
--- a/scripts/orchestrator/result-precheck.sh
+++ b/scripts/orchestrator/result-precheck.sh
@@ -19,6 +19,7 @@
 #   `head=` set to that commit. A masker failure removes the logs instead. `--secrets <file>` (the pre-push hook) and
 #   `--staged` (`format` and `shellcheck` on the staged files, the pre-commit hook) run only those checks.
 # shortcut: a Claude seat cannot run codex inside its Bash sandbox (local-review.sh's header), so the orchestrator's acceptance runs the local review on the head as today; upgrade to seat when the seats run omp (plan 024 phase 2 B)
+# shortcut: inside a Claude seat's sandbox the full suite fails on sandbox-denied operations, so a seat runs the precheck with --tests on its task's modules and CI runs the full suite; upgrade when the seats run omp (plan 024 phase 2 B)
 # @arg $1 string Task id: letters, digits, `.`, `_` and `-`.
 # @option --tests <module>... Unittest modules to run instead of `make unit-test`.
 # @option --previous-head <sha40> The `previous_head=` of a `status=revise` ACCEPTANCE; needs `--check`.
@@ -205,7 +206,6 @@ mask "${logs[@]}" > /dev/null || {
     echo "result-precheck: the masker failed; the logs are removed and no record is written" >&2
     exit 1
 }
-# Writes precheck.json and result.txt, prints the precheck= line, and exits 1 when a check or a selector failed.
 read -r -d '' writer << 'PY' || true
 import hashlib, json, os, sys
 from datetime import UTC, datetime
```

## Bot fix round a7b0da2f (threads 4305945403 and 4305945407)

Each extended test run against the pre-fix script of 1763da66 (restored afterwards, hash verified), then the two modules and the precheck on a7b0da2f.

```text
$ bash red-old.sh 1763da66ae0d86ad2e7d481072cba27be41dfc71
.githooks/pre-push at 1763da66 -> test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern exit=1
FAIL: test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern (branch='removed')
FAILED (failures=1)
scripts/orchestrator/dispatch.sh at 1763da66 -> test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required exit=1
FAIL: test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required (field='precheck.json:checks')
FAIL: test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required (field='result the newest')
FAILED (failures=2)
exit=0

$ git diff --stat 105e42cf a7b0da2f -- scripts .githooks tests
 .githooks/pre-push                 | 10 ++++----
 scripts/orchestrator/dispatch.sh   | 43 ++++++++++++++++------------------
 tests/unit/test_result_precheck.py | 47 +++++++++++++++++++++++++-------------
 3 files changed, 56 insertions(+), 44 deletions(-)
exit=0

$ uv run python -m unittest tests.unit.test_result_precheck tests.unit.test_orchestrator_tools
Ran 63 tests in 58.105s
OK
exit=0

$ scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a01 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools
result-precheck: unit-test exit 0
result-precheck: render-check exit 0
result-precheck: format exit 0
result-precheck: shellcheck exit 0
result-precheck: secrets exit 0
precheck=24beae719509c95f0ce01317ab24675b7e6db1152b9cb1d44d3cf5095a282f32
exit=0
$ cat precheck.json
{
  "head": "a7b0da2f60e4e11af879cdc9b73a4b90cf423d03",
  "tree": "3bcc2b188ddaf345c00817e9170140ea542adef9",
  "generated_at": "2026-10-18T06:07:54Z",
  "checks": [
    {
      "name": "unit-test",
      "ok": true,
      "exit": 0,
      "output_sha256": "b3dadb74c4315f43676628119eb8a503974e3180e7680dd6372b42fa012dc514"
    },
    {
      "name": "render-check",
      "ok": true,
      "exit": 0,
      "output_sha256": "3cc07aa4e482b20772e8ba404d3c0d9e338adcd0cd2d4ff6edf14de8bf23db93"
    },
    {
      "name": "format",
      "ok": true,
      "exit": 0,
      "output_sha256": "f170e34f5d9c464c7dd7be27fb8f87bb26969019903d50b6636103c97a779796"
    },
    {
      "name": "shellcheck",
      "ok": true,
      "exit": 0,
      "output_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "name": "secrets",
      "ok": true,
      "exit": 0,
      "output_sha256": "ec427b4abbf24ab3958dd1498e28cc76113d99c85519521cfc6951635053f42a"
    },
    {
      "name": "local-review",
      "ok": null,
      "deferred": "orchestrator"
    }
  ],
  "selectors": []
}
$ cat result.txt
AGMSG-RESULT v1 task_id=dotfiles-T133-result-precheck-a01 status=ready_for_review head=a7b0da2f60e4e11af879cdc9b73a4b90cf423d03 precheck=24beae719509c95f0ce01317ab24675b7e6db1152b9cb1d44d3cf5095a282f32 task_copy=05caa77f064b809185138817d869ae0b4fc52ef76863715d1e6d998134ac011f report=.orchestration/dotfiles-T133-result-precheck-a01/report.md validation=.orchestration/dotfiles-T133-result-precheck-a01/validation.md sandbox=.orchestration/dotfiles-T133-result-precheck-a01/sandbox.md learning=.orchestration/dotfiles-T133-result-precheck-a01/learning.md
```

## The runner

```bash
#!/usr/bin/env bash
# Run T133's Check commands (all but the precheck itself) from the worktree root; print each verbatim with its exit.
set -u
out_dir=$1 mutate=$2
grep() { /usr/bin/grep "$@"; }
run() {
    printf '$ %s\n' "$*"
    "$@" 2>&1
    printf 'exit=%s\n\n' "$?"
}
new=(scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push)
run git rev-parse HEAD origin/main
run make render-check
printf '$ make validate-agent-assets > vaa.txt 2>&1\n'
make validate-agent-assets > "${out_dir}/vaa.txt" 2>&1
printf 'exit=%s\n' "$?"
printf "\$ grep -v '^WARN: regime-boundary' vaa.txt\n"
grep -v '^WARN: regime-boundary' "${out_dir}/vaa.txt"
printf '$ grep T133 vaa.txt\n'
grep T133 "${out_dir}/vaa.txt"
printf '\n'
run shellcheck -x "${new[@]}" scripts/orchestrator/dispatch.sh
run shfmt -d -i 4 -sr "${new[@]}" scripts/orchestrator/dispatch.sh
printf "\$ git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs shfmt -i 4 -sr -d\n"
git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs shfmt -i 4 -sr -d 2>&1
printf 'exit=%s\n\n' "$?"
printf "\$ git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check\n"
git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check 2>&1
printf 'exit=%s\n\n' "$?"
printf "\$ git ls-files -z '*.md' | xargs -0 prettier --check\n"
git ls-files -z '*.md' | xargs -0 prettier --check 2>&1
printf 'exit=%s\n\n' "$?"
printf '$ make format > format.txt 2>&1\n'
make format > "${out_dir}/format.txt" 2>&1
printf 'exit=%s\n' "$?"
printf "\$ grep -E '^--- ' format.txt | sed 's/^--- //; s/\\\\.orig\$//' | sort -u\n"
grep -E '^--- ' "${out_dir}/format.txt" | sed 's/^--- //; s/\.orig$//' | sort -u
printf '\n'
run uv run python -m unittest tests.unit.test_result_precheck tests.unit.test_orchestrator_tools -v
if [[ -n ${mutate} ]]; then
    printf '$ bash mutate.sh\n'
    bash "${mutate}" 2>&1
    printf 'exit=%s\n\n' "$?"
fi
run git status --porcelain
run git diff --numstat origin/main...HEAD
```
