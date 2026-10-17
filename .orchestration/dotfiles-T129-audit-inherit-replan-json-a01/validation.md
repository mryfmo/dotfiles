---
task_id: dotfiles-T129-audit-inherit-replan-json-a01
seat: claude-standard-dot-a006
code_commit: ec4ba99d
---

# Validation: dotfiles-T129-audit-inherit-replan-json-a01

Every command ran from the worktree `.claude/worktrees/worker-f` on branch `tools/audit-inherit-replan-json`, inside the sandbox, captured at `ec4ba99d` by a runner that prints the command, its verbatim output and `[exit <status>]` (a pipeline's status is its last command's unless the command sets `pipefail`). `MAIN` names the main checkout, `T` the task id and `S` the seat's session scratchpad. `UV_OFFLINE=1` was set, and so were `GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=init.defaultBranch GIT_CONFIG_VALUE_0=main GIT_CONFIG_KEY_1=commit.gpgsign GIT_CONFIG_VALUE_1=false`: the CI workflows run `git config --global init.defaultBranch main` and sign nothing, while this host's global git config signs commits with a key that is absent, so the gate suite's own temporary repository gets no first commit without them (§7). The output is verbatim, with the main checkout's path replaced by `$MAIN`.

## 1. Task file and task copy

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
7ea5564f6a3f8e9054a55250ff53a35d72b0445be7841981badfb6cb70021c1d  $MAIN/.orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-a01.md
7ea5564f6a3f8e9054a55250ff53a35d72b0445be7841981badfb6cb70021c1d  .orchestration/dotfiles-T129-audit-inherit-replan-json-a01/task.md
byte-identical
[exit 0]
```

```console
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-audit-inherit-replan-json-a01.md: OK
[exit 0]
```

## 2. The six premises, replayed against origin/main

`origin/main` moved from `a0e8b8ad` (the base at dispatch) to `35ab0e95` (#385, `.orchestration` files only: `git diff --stat a0e8b8ad origin/main -- scripts tests` prints nothing) before the branch was rebased onto it. Premises 1 to 4 and 6 print their stated output. Premise 5 prints 3 on the current `origin/main` and its stated 4 at `a0e8b8ad`; the block after it names the three records that now carry a `re-plan:` body line, the migration the task leaves to the orchestrator.

premise 1:

```console
$ git show origin/main:scripts/orchestrator/chain-integrate.sh | /usr/bin/grep -c "inherited"
0
[exit 1]
```

premise 2:

```console
$ for f in scripts/require-crit-review.py scripts/regime-counters.sh; do git show origin/main:$f | /usr/bin/grep -c "re-plan: "; done | tr "\n" " " | sed "s/ $//"
1 2
[exit 0]
```

premise 3:

```console
$ git show origin/main:scripts/orchestrator/acceptance-front-matter.py | /usr/bin/grep -c "replans" || true
0
[exit 0]
```

premise 4:

```console
$ git grep -c "re-plan: " origin/main -- tests/unit/test_require_crit_review.py tests/unit/test_regime_counters.py | sed "s#^origin/main:##" | tr "\n" " " | sed "s/ $//"
tests/unit/test_regime_counters.py:7 tests/unit/test_require_crit_review.py:4
[exit 0]
```

premise 5 on the current origin/main:

```console
$ git grep -lE "^re-plan: " origin/main -- .orchestration/acceptance | wc -l | tr -d " "
3
[exit 0]
```

premise 5 at the dispatch base a0e8b8ad, and the three records now:

```console
$ git grep -lE "^re-plan: " a0e8b8ad -- .orchestration/acceptance | wc -l | tr -d " "; git grep -lE "^re-plan: " origin/main -- .orchestration/acceptance | sed "s#^origin/main:##"
4
.orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01-followup-a01.md
.orchestration/acceptance/dotfiles-T128-s1-replan-gate-a01.md
.orchestration/acceptance/dotfiles-T128-seat-launch-args-a01.md
[exit 0]
```

premise 6:

```console
$ git grep -cF 'f"audit:{head[:7]}:{n}"' origin/main -- scripts/require-crit-review.py | sed "s#^origin/main:##"
scripts/require-crit-review.py:1
[exit 0]
```

## 3. Branch and base

```console
$ git log --oneline -2; git merge-base origin/main HEAD; git rev-parse origin/main
ec4ba99d feat(orchestrator): an update-branch-only head inherits its audit, and the S1 re-plan is the record block's replans object (T129 audit-inherit replan-json a01)
35ab0e95 chore(orchestration): boundary (18) records of 2026-10-17 (plan 023 filed, the T129 task texts and their dispatch, corrections C-61, the decisions and corrections inventories) (#385)
35ab0e95a7fe27c501db3478d4f37e69a514d532
35ab0e95a7fe27c501db3478d4f37e69a514d532
[exit 0]
```

## 4. The five new tests against origin/main's four scripts (red), then restored

```console
$ for f in scripts/orchestrator/chain-integrate.sh scripts/require-crit-review.py scripts/regime-counters.sh scripts/orchestrator/acceptance-front-matter.py; do git show origin/main:$f > $f; done && git diff --stat
 scripts/orchestrator/acceptance-front-matter.py | 14 +++--------
 scripts/orchestrator/chain-integrate.sh         | 29 +++-------------------
 scripts/regime-counters.sh                      | 17 +++++++------
 scripts/require-crit-review.py                  | 33 ++++++++++---------------
 4 files changed, 29 insertions(+), 64 deletions(-)
[exit 0]
```

```console
$ set -o pipefail; uv run python -m unittest tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_inherits_the_audit_across_an_update_branch_only_head tests.unit.test_require_crit_review.ReviewGuardTest.test_s1_replan_is_read_from_the_record_block_json tests.unit.test_require_crit_review.ReviewGuardTest.test_s6_reads_an_inherited_audit_s_ids_under_the_parent_sha7 tests.unit.test_regime_counters.RegimeCountersTest.test_s1_replan_token_comes_from_the_record_block_json tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_front_matter_keeps_and_validates_the_replans_object 2>&1 | /usr/bin/grep -E '^(FAIL|ERROR):|^Ran|^FAILED|^OK'
ERROR: test_front_matter_keeps_and_validates_the_replans_object (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_front_matter_keeps_and_validates_the_replans_object)
FAIL: test_integrate_inherits_the_audit_across_an_update_branch_only_head (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_inherits_the_audit_across_an_update_branch_only_head)
FAIL: test_s1_replan_is_read_from_the_record_block_json (tests.unit.test_require_crit_review.ReviewGuardTest.test_s1_replan_is_read_from_the_record_block_json)
FAIL: test_s6_reads_an_inherited_audit_s_ids_under_the_parent_sha7 (tests.unit.test_require_crit_review.ReviewGuardTest.test_s6_reads_an_inherited_audit_s_ids_under_the_parent_sha7)
FAIL: test_s1_replan_token_comes_from_the_record_block_json (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_replan_token_comes_from_the_record_block_json) [the object]
FAIL: test_s1_replan_token_comes_from_the_record_block_json (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_replan_token_comes_from_the_record_block_json) [a body line alone]
Ran 5 tests in 8.351s
FAILED (failures=5, errors=1)
[exit 1]
```

```console
$ git checkout -- scripts && git diff --quiet && echo restored to $(git rev-parse --short HEAD)
restored to ec4ba99d
[exit 0]
```

## 5. The Check

```console
$ uv run python -m unittest tests/unit/test_chain_glue.py tests/unit/test_require_crit_review.py tests/unit/test_regime_counters.py tests/unit/test_orchestrator_tools.py -v
test_integrate_inherits_the_audit_across_an_update_branch_only_head (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_inherits_the_audit_across_an_update_branch_only_head) ... ok
test_integrate_refuses_a_main_checkout_script_that_is_not_heads (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_a_main_checkout_script_that_is_not_heads) ... ok
test_integrate_refuses_a_stale_main_checkout_after_the_restart (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_a_stale_main_checkout_after_the_restart) ... ok
test_integrate_refuses_an_absent_owner_task_before_the_advisory_step (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_an_absent_owner_task_before_the_advisory_step) ... ok
test_integrate_refuses_an_extra_tsv_outside_the_main_checkout (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_an_extra_tsv_outside_the_main_checkout) ... ok
test_integrate_refuses_when_main_is_not_on_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_when_main_is_not_on_main) ... ok
test_integrate_resolves_binaries_before_the_checkout (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_resolves_binaries_before_the_checkout) ... ok
test_integrate_restarts_after_update_branch (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restarts_after_update_branch) ... ok
test_integrate_restarts_when_the_base_moves_during_the_waits (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restarts_when_the_base_moves_during_the_waits) ... ok
test_integrate_restores_the_review_worktree_after_the_audit (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restores_the_review_worktree_after_the_audit) ... ok
test_integrate_runs_gh_without_forced_colour (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_runs_gh_without_forced_colour) ... ok
test_integrate_runs_the_steps_in_order_and_logs_each (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_runs_the_steps_in_order_and_logs_each) ... ok
test_integrate_stops_on_a_sandbox_scan_hit (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_stops_on_a_sandbox_scan_hit) ... ok
test_acceptance_record_accepts_a_dispatch_list (tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_accepts_a_dispatch_list) ... ok
test_acceptance_record_head_must_be_head (tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_head_must_be_head) ... ok
test_acceptance_record_is_not_counted_as_a_change (tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_is_not_counted_as_a_change) ... ok
test_acceptance_record_ledger_must_cover_a_badged_review_body (tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_ledger_must_cover_a_badged_review_body) ... ok
test_acceptance_record_ledger_must_cover_swept_findings (tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_ledger_must_cover_swept_findings) ... ok
test_acceptance_record_pr_must_be_the_swept_pr (tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_pr_must_be_the_swept_pr) ... ok
test_acceptance_record_prose_is_not_read (tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_prose_is_not_read) ... ok
test_acceptance_record_refuses_a_duplicate_key (tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_refuses_a_duplicate_key) ... ok
test_acceptance_record_refuses_a_non_finite_number (tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_refuses_a_non_finite_number) ... ok
test_acceptance_record_refuses_an_unknown_key (tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_refuses_an_unknown_key) ... ok
test_advanced_base_cannot_delete_collector_to_trigger_head_fallback (tests.unit.test_require_crit_review.ReviewGuardTest.test_advanced_base_cannot_delete_collector_to_trigger_head_fallback) ... ok
test_advanced_base_cannot_supply_an_untrusted_collector (tests.unit.test_require_crit_review.ReviewGuardTest.test_advanced_base_cannot_supply_an_untrusted_collector) ... ok
test_agent_lifecycle_script_change_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_script_change_requires_review) ... ok
test_agent_lifecycle_surfaces_require_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_surfaces_require_review) ... ok
test_agent_lifecycle_tokens_require_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_lifecycle_tokens_require_review) ... ok
test_agent_reviewer_rejects_empty_or_malformed_crit_data (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_reviewer_rejects_empty_or_malformed_crit_data) ... ok
test_agent_reviewer_rejects_invalid_review_outcome (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_reviewer_rejects_invalid_review_outcome) ... ok
test_agent_reviewer_with_command_string_source_still_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_command_string_source_still_requires_review) ... ok
test_agent_reviewer_with_crit_data_satisfies_required_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_crit_data_satisfies_required_review) ... ok
test_agent_reviewer_with_crit_reviewed_marker_still_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_crit_reviewed_marker_still_requires_review) ... ok
test_agent_reviewer_with_external_crit_json_still_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_external_crit_json_still_requires_review) ... ok
test_agent_reviewer_with_non_review_crit_json_object_still_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_non_review_crit_json_object_still_requires_review) ... ok
test_agent_reviewer_with_resolved_line_comment_satisfies_required_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_resolved_line_comment_satisfies_required_review) ... ok
test_agent_reviewer_with_unresolved_crit_json_still_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_reviewer_with_unresolved_crit_json_still_requires_review) ... ok
test_agent_self_review_flag_evidence_still_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_self_review_flag_evidence_still_requires_review) ... ok
test_agent_self_reviewer_evidence_still_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_agent_self_reviewer_evidence_still_requires_review) ... ok
test_audit_finding_reason_may_quote_the_grammar (tests.unit.test_require_crit_review.ReviewGuardTest.test_audit_finding_reason_may_quote_the_grammar) ... ok
test_audit_must_name_head_and_live_under_validation (tests.unit.test_require_crit_review.ReviewGuardTest.test_audit_must_name_head_and_live_under_validation) ... ok
test_base_accepts_a_correct_audit_of_head (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_accepts_a_correct_audit_of_head) ... ok
test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base) ... ok
test_base_fails_closed_when_github_metadata_is_unavailable (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_github_metadata_is_unavailable) ... ok
test_base_fails_closed_when_unresolvable_or_option_like (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_unresolvable_or_option_like) ... ok
test_base_rejects_forged_evidence_metadata (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_rejects_forged_evidence_metadata) ... ok
test_base_rejects_pr_commits_before_executing_their_collector (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_rejects_pr_commits_before_executing_their_collector) ... ok
test_base_rejects_side_branch_and_advanced_base_containing_pr_commits (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_rejects_side_branch_and_advanced_base_containing_pr_commits) ... ok
test_base_requires_an_acceptance_record_under_acceptance (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) ... ok
test_base_requires_audit_evidence_for_a_reviewed_change (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_requires_audit_evidence_for_a_reviewed_change) ... ok
test_base_requires_pr_feedback_evidence (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_requires_pr_feedback_evidence) ... ok
test_base_reviews_committed_branch_changes (tests.unit.test_require_crit_review.ReviewGuardTest.test_base_reviews_committed_branch_changes) ... ok
test_blocked_or_missing_audit_verdict_fails (tests.unit.test_require_crit_review.ReviewGuardTest.test_blocked_or_missing_audit_verdict_fails) ... ok
test_broad_diff_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_broad_diff_requires_review) ... ok
test_broad_orchestration_only_pr_needs_no_audit (tests.unit.test_require_crit_review.ReviewGuardTest.test_broad_orchestration_only_pr_needs_no_audit) ... ok
test_companion_must_be_this_audits_own_last_message (tests.unit.test_require_crit_review.ReviewGuardTest.test_companion_must_be_this_audits_own_last_message) ... ok
test_disposition_parsing_is_linear (tests.unit.test_require_crit_review.ReviewGuardTest.test_disposition_parsing_is_linear) ... ok
test_dispositions_of_2026_10_12_without_evidence_are_refused (tests.unit.test_require_crit_review.ReviewGuardTest.test_dispositions_of_2026_10_12_without_evidence_are_refused) ... ok
test_dispositions_with_an_evidence_command_are_accepted (tests.unit.test_require_crit_review.ReviewGuardTest.test_dispositions_with_an_evidence_command_are_accepted) ... ok
test_explicit_disable_skips_guard (tests.unit.test_require_crit_review.ReviewGuardTest.test_explicit_disable_skips_guard) ... ok
test_feedback_accepts_absolute_path_through_a_repository_parent_alias (tests.unit.test_require_crit_review.ReviewGuardTest.test_feedback_accepts_absolute_path_through_a_repository_parent_alias) ... ok
test_feedback_cannot_hide_an_arbitrary_path_without_base (tests.unit.test_require_crit_review.ReviewGuardTest.test_feedback_cannot_hide_an_arbitrary_path_without_base) ... ok
test_feedback_does_not_exclude_symlink_aliases_outside_validation (tests.unit.test_require_crit_review.ReviewGuardTest.test_feedback_does_not_exclude_symlink_aliases_outside_validation) ... ok
test_feedback_path_itself_must_be_under_validation (tests.unit.test_require_crit_review.ReviewGuardTest.test_feedback_path_itself_must_be_under_validation) ... ok
test_feedback_symlink_cannot_hide_a_file_outside_validation (tests.unit.test_require_crit_review.ReviewGuardTest.test_feedback_symlink_cannot_hide_a_file_outside_validation) ... ok
test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent (tests.unit.test_require_crit_review.ReviewGuardTest.test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent) ... ok
test_github_lookup_ignores_environment_repository_override (tests.unit.test_require_crit_review.ReviewGuardTest.test_github_lookup_ignores_environment_repository_override) ... ok
test_github_lookup_rejects_evidence_from_another_repository (tests.unit.test_require_crit_review.ReviewGuardTest.test_github_lookup_rejects_evidence_from_another_repository) ... ok
test_high_risk_markdown_change_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_high_risk_markdown_change_requires_review) ... ok
test_incorrect_audit_needs_audit_findings (tests.unit.test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) ... ok
test_incorrect_audit_without_findings_fails (tests.unit.test_require_crit_review.ReviewGuardTest.test_incorrect_audit_without_findings_fails) ... ok
test_large_untracked_file_requires_broad_diff_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_large_untracked_file_requires_broad_diff_review) ... ok
test_missing_base_collector_falls_back_only_after_binding (tests.unit.test_require_crit_review.ReviewGuardTest.test_missing_base_collector_falls_back_only_after_binding) ... ok
test_native_reviewed_environment_rejects_human_reviewer (tests.unit.test_require_crit_review.ReviewGuardTest.test_native_reviewed_environment_rejects_human_reviewer) ... ok
test_native_reviewed_without_evidence_still_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_native_reviewed_without_evidence_still_requires_review) ... ok
test_no_diff_does_not_require_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_no_diff_does_not_require_review) ... ok
test_older_base_must_not_be_on_the_head_first_parent_chain (tests.unit.test_require_crit_review.ReviewGuardTest.test_older_base_must_not_be_on_the_head_first_parent_chain) ... ok
test_orchestration_only_pr_needs_no_audit (tests.unit.test_require_crit_review.ReviewGuardTest.test_orchestration_only_pr_needs_no_audit) ... ok
test_pr_feedback_accepts_complete_evidence_without_a_bot_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_evidence_without_a_bot_review) ... ok
test_pr_feedback_accepts_complete_root_cause_dispositions (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_root_cause_dispositions) ... ok
test_pr_feedback_bodies_are_compared_after_secret_masking (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) ... ok
test_pr_feedback_evidence_file_is_not_counted_as_a_change (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_evidence_file_is_not_counted_as_a_change) ... ok
test_pr_feedback_fails_when_the_collector_cannot_run (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_fails_when_the_collector_cannot_run) ... ok
test_pr_feedback_fixed_commit_must_be_in_the_pr_range (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_fixed_commit_must_be_in_the_pr_range) ... ok
test_pr_feedback_matches_a_masked_path_but_not_an_edited_one (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_matches_a_masked_path_but_not_an_edited_one) ... ok
test_pr_feedback_must_be_collected_for_the_current_head (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_be_collected_for_the_current_head) ... ok
test_pr_feedback_must_cover_every_currently_collected_item (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_cover_every_currently_collected_item) ... ok
test_pr_feedback_rejects_evidence_outside_the_repository (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_evidence_outside_the_repository) ... ok
test_pr_feedback_rejects_incomplete_or_invalid_dispositions (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) ... ok
test_pr_feedback_requires_the_github_head_to_match (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_requires_the_github_head_to_match) ... ok
test_pr_feedback_uses_the_base_collector_not_the_prs_own (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_uses_the_base_collector_not_the_prs_own) ... ok
test_pr_feedback_without_base_is_only_format_checked (tests.unit.test_require_crit_review.ReviewGuardTest.test_pr_feedback_without_base_is_only_format_checked) ... ok
test_recollection_must_match_the_authenticated_repository (tests.unit.test_require_crit_review.ReviewGuardTest.test_recollection_must_match_the_authenticated_repository) ... ok
test_retired_audit_dispositions_is_not_read (tests.unit.test_require_crit_review.ReviewGuardTest.test_retired_audit_dispositions_is_not_read) ... ok
test_reviewed_environment_satisfies_required_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_reviewed_environment_satisfies_required_review) ... ok
test_reviewed_with_blank_evidence_values_still_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_reviewed_with_blank_evidence_values_still_requires_review) ... ok
test_reviewed_with_incomplete_evidence_still_requires_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_reviewed_with_incomplete_evidence_still_requires_review) ... ok
test_s1_class_at_three_with_a_missing_key_is_refused (tests.unit.test_require_crit_review.ReviewGuardTest.test_s1_class_at_three_with_a_missing_key_is_refused) ... ok
test_s1_class_at_three_with_the_four_keys_is_accepted (tests.unit.test_require_crit_review.ReviewGuardTest.test_s1_class_at_three_with_the_four_keys_is_accepted) ... ok
test_s1_class_at_three_without_a_replans_object_is_refused (tests.unit.test_require_crit_review.ReviewGuardTest.test_s1_class_at_three_without_a_replans_object_is_refused) ... ok
test_s1_replan_is_read_from_the_record_block_json (tests.unit.test_require_crit_review.ReviewGuardTest.test_s1_replan_is_read_from_the_record_block_json) ... ok
test_s6_class_at_three_with_the_matching_searches_entry_is_accepted (tests.unit.test_require_crit_review.ReviewGuardTest.test_s6_class_at_three_with_the_matching_searches_entry_is_accepted) ... ok
test_s6_class_at_three_without_a_searches_entry_is_refused (tests.unit.test_require_crit_review.ReviewGuardTest.test_s6_class_at_three_without_a_searches_entry_is_refused) ... ok
test_s6_reads_an_inherited_audit_s_ids_under_the_parent_sha7 (tests.unit.test_require_crit_review.ReviewGuardTest.test_s6_reads_an_inherited_audit_s_ids_under_the_parent_sha7) ... ok
test_s6_searches_entry_must_equal_the_recomputed_records_search (tests.unit.test_require_crit_review.ReviewGuardTest.test_s6_searches_entry_must_equal_the_recomputed_records_search) ... ok
test_small_docs_only_change_does_not_require_review (tests.unit.test_require_crit_review.ReviewGuardTest.test_small_docs_only_change_does_not_require_review) ... ok
test_swept_ids_are_exactly_the_review_comments_and_the_badged_review_body (tests.unit.test_require_crit_review.ReviewGuardTest.test_swept_ids_are_exactly_the_review_comments_and_the_badged_review_body) ... ok
test_swept_ids_come_from_authenticated_authors (tests.unit.test_require_crit_review.ReviewGuardTest.test_swept_ids_come_from_authenticated_authors) ... ok
test_the_gate_has_no_github_identity_check (tests.unit.test_require_crit_review.ReviewGuardTest.test_the_gate_has_no_github_identity_check) ... ok
test_verdict_comes_only_from_the_last_message_file (tests.unit.test_require_crit_review.ReviewGuardTest.test_verdict_comes_only_from_the_last_message_file) ... ok
test_a_600_row_history_counts_fully_through_the_storage_facade (tests.unit.test_regime_counters.RegimeCountersTest.test_a_600_row_history_counts_fully_through_the_storage_facade) ... ok
test_a_forged_acceptance_record_changes_no_count (tests.unit.test_regime_counters.RegimeCountersTest.test_a_forged_acceptance_record_changes_no_count) ... ok
test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity (tests.unit.test_regime_counters.RegimeCountersTest.test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity) ... ok
test_a_status_in_free_text_counts_nothing (tests.unit.test_regime_counters.RegimeCountersTest.test_a_status_in_free_text_counts_nothing) ... ok
test_a_store_at_another_schema_revision_is_unreadable (tests.unit.test_regime_counters.RegimeCountersTest.test_a_store_at_another_schema_revision_is_unreadable) ... ok
test_a_tab_separated_task_counts_as_an_amendment (tests.unit.test_regime_counters.RegimeCountersTest.test_a_tab_separated_task_counts_as_an_amendment) ... ok
test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id) ... ok
test_bot_heads_are_unknown_when_gh_fails (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_gh_fails) ... ok
test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit) ... ok
test_bot_heads_are_unknown_without_a_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_without_a_first_result_head) ... ok
test_bot_heads_read_every_page_through_gh_api (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_read_every_page_through_gh_api) ... ok
test_every_line_names_its_source (tests.unit.test_regime_counters.RegimeCountersTest.test_every_line_names_its_source) ... ok
test_every_result_counts_as_a_revise_whatever_its_status (tests.unit.test_regime_counters.RegimeCountersTest.test_every_result_counts_as_a_revise_whatever_its_status) ... ok
test_history_only_never_calls_gh (tests.unit.test_regime_counters.RegimeCountersTest.test_history_only_never_calls_gh) ... ok
test_list_tasks_prints_each_task_id_once (tests.unit.test_regime_counters.RegimeCountersTest.test_list_tasks_prints_each_task_id_once) ... ok
test_only_p0_and_p1_heads_after_the_first_result_head_count (tests.unit.test_regime_counters.RegimeCountersTest.test_only_p0_and_p1_heads_after_the_first_result_head_count) ... ok
test_s1_candidates_are_bot_title_classes_seen_three_times (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_candidates_are_bot_title_classes_seen_three_times) ... ok
test_s1_excludes_advisory_p2_at_three_rows (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_excludes_advisory_p2_at_three_rows) ... ok
test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects) ... ok
test_s1_quotes_a_title_with_shell_metacharacters (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_quotes_a_title_with_shell_metacharacters) ... ok
test_s1_reads_the_ledger_classes_of_the_acceptance_record (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_reads_the_ledger_classes_of_the_acceptance_record) ... ok
test_s1_replan_token_comes_from_the_record_block_json (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_replan_token_comes_from_the_record_block_json) ... ok
test_s1_reports_replan_missing_without_the_four_keys (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_reports_replan_missing_without_the_four_keys) ... ok
test_s1_reports_replan_present_for_the_class (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_reports_replan_present_for_the_class) ... ok
test_t118_fixture_counts_revises_from_results (tests.unit.test_regime_counters.RegimeCountersTest.test_t118_fixture_counts_revises_from_results) ... ok
test_t119_fixture_counts_every_task_after_the_first_as_an_amendment (tests.unit.test_regime_counters.RegimeCountersTest.test_t119_fixture_counts_every_task_after_the_first_as_an_amendment) ... ok
test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head) ... ok
test_the_boundary_check_never_passes_a_test_seam (tests.unit.test_regime_counters.RegimeCountersTest.test_the_boundary_check_never_passes_a_test_seam) ... ok
test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one (tests.unit.test_regime_counters.RegimeCountersTest.test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one) ... ok
test_thresholds_are_inv6_constants (tests.unit.test_regime_counters.RegimeCountersTest.test_thresholds_are_inv6_constants) ... ok
test_usage_errors_exit_2 (tests.unit.test_regime_counters.RegimeCountersTest.test_usage_errors_exit_2) ... ok
test_v0_fixture_counts_bot_heads_after_the_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_v0_fixture_counts_bot_heads_after_the_first_result_head) ... ok
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
test_front_matter_keeps_and_validates_the_replans_object (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_front_matter_keeps_and_validates_the_replans_object) ... ok
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
Ran 199 tests in 232.733s

OK
[exit 0]
```

```console
$ shellcheck scripts/orchestrator/chain-integrate.sh scripts/regime-counters.sh && echo clean
clean
[exit 0]
```

The linters CI runs on these files (`make format`'s shfmt, `ruff format --check` and prettier):

```console
$ shfmt -i 4 -sr -d scripts/orchestrator/chain-integrate.sh scripts/regime-counters.sh && echo clean
clean
[exit 0]
```

```console
$ ruff format --config ruff.toml --check scripts/require-crit-review.py scripts/orchestrator/acceptance-front-matter.py tests/unit/test_chain_glue.py tests/unit/test_require_crit_review.py tests/unit/test_regime_counters.py tests/unit/test_orchestrator_tools.py
6 files already formatted
[exit 0]
```

```console
$ prettier --check tests/fixtures/gate-evidence/acceptance-s6-present.md
Checking formatting...
All matched files use Prettier code style!
[exit 0]
```

## 6. Mutation check

Each mutant is applied alone as a literal replacement asserted to match once, its test run, and the file restored with `git checkout`; then the baseline of the six tests. The script, `$S/mutate-t129.py`:

```python
"""Apply each mutant alone as a literal replacement (asserted to match once), run its test, restore with git checkout.

Run from the worktree root: python mutate-t129.py. Prints one `mutant <n> rc=<test status> <file>: <label>` line per
mutant (a caught mutant is rc=1) and a final baseline line.
"""

import subprocess
import sys
from pathlib import Path

GLUE = "tests.unit.test_chain_glue.ChainIntegrateTest."
GATE = "tests.unit.test_require_crit_review.ReviewGuardTest."
COUNT = "tests.unit.test_regime_counters.RegimeCountersTest."
TOOLS = "tests.unit.test_orchestrator_tools.OrchestratorToolsTest."
INHERIT = GLUE + "test_integrate_inherits_the_audit_across_an_update_branch_only_head"
MUTANTS = [
    (
        "scripts/orchestrator/chain-integrate.sh",
        'if [[ -n ${old} && ${old%% *} == "${new%% *}" ]]; then',
        "if [[ -n ${old} ]]; then",
        "the patch-id comparison dropped",
        INHERIT,
    ),
    (
        "scripts/orchestrator/chain-integrate.sh",
        '{ [[ $(head -n 1 -- "${from}${s}") == inherited-from:* ]] || echo',
        "{ false || echo",
        "a parent's marker no longer kept",
        INHERIT,
    ),
    (
        "scripts/require-crit-review.py",
        "sha7 = marker.group(1) if marker else head[:7]",
        "sha7 = head[:7]",
        "the inherited marker ignored by S6",
        GATE + "test_s6_reads_an_inherited_audit_s_ids_under_the_parent_sha7",
    ),
    (
        "scripts/require-crit-review.py",
        "return isinstance(entry, dict) and all(is_text(entry.get(key)) for key in REPLAN_KEYS)",
        "return isinstance(entry, dict)",
        "S1 takes any replans entry",
        GATE + "test_s1_replan_is_read_from_the_record_block_json",
    ),
    (
        "scripts/require-crit-review.py",
        "if not isinstance(replans, dict) or not all(\n        CLASS_SLUG.fullmatch(cls) and isinstance(entry, dict) for cls, entry in replans.items()\n    ):",
        "if False:",
        "the malformed-block check dropped",
        GATE + "test_s1_replan_is_read_from_the_record_block_json",
    ),
    (
        "scripts/regime-counters.sh",
        '($rec.rec.replans | if type == "object" then .[$class] else null end) as $r',
        "null as $r",
        "the counters read no replans",
        COUNT + "test_s1_replan_token_comes_from_the_record_block_json",
    ),
    (
        "scripts/regime-counters.sh",
        '| $r[$k] | type == "string" and test("\\\\S")] | all)) as $replan',
        "| true] | all)) as $replan",
        "the counters take any part",
        COUNT + "test_s1_reports_replan_missing_without_the_four_keys",
    ),
    (
        "scripts/orchestrator/acceptance-front-matter.py",
        " or set(entry) != set(gate.REPLAN_KEYS)",
        "",
        "the writer takes extra parts",
        TOOLS + "test_front_matter_keeps_and_validates_the_replans_object",
    ),
    (
        "scripts/orchestrator/acceptance-front-matter.py",
        "audit_findings=findings, replans=replans)",
        "audit_findings=findings)",
        "the writer writes no replans",
        TOOLS + "test_front_matter_keeps_and_validates_the_replans_object",
    ),
]


def test(name):
    return subprocess.run(
        [sys.executable, "-m", "unittest", name], capture_output=True, text=True
    ).returncode


for n, (rel, old, new, label, name) in enumerate(MUTANTS, 1):
    path = Path(rel)
    text = path.read_text()
    assert text.count(old) == 1, (rel, label, text.count(old))
    path.write_text(text.replace(old, new))
    rc = test(name)
    subprocess.run(["git", "checkout", "--", rel], check=True)
    print(f"mutant {n} rc={rc} {rel}: {label} ({name.rsplit('.', 1)[1]})", flush=True)
baseline = [name for *_, name in MUTANTS]
rc = subprocess.run(
    [sys.executable, "-m", "unittest", *dict.fromkeys(baseline)],
    capture_output=True,
    text=True,
).returncode
print(
    f"baseline rc={rc}: the {len(dict.fromkeys(baseline))} tests on the unmutated tree"
)
```

```console
$ uv run python "$S/mutate-t129.py"
mutant 1 rc=1 scripts/orchestrator/chain-integrate.sh: the patch-id comparison dropped (test_integrate_inherits_the_audit_across_an_update_branch_only_head)
mutant 2 rc=1 scripts/orchestrator/chain-integrate.sh: a parent's marker no longer kept (test_integrate_inherits_the_audit_across_an_update_branch_only_head)
mutant 3 rc=1 scripts/require-crit-review.py: the inherited marker ignored by S6 (test_s6_reads_an_inherited_audit_s_ids_under_the_parent_sha7)
mutant 4 rc=1 scripts/require-crit-review.py: S1 takes any replans entry (test_s1_replan_is_read_from_the_record_block_json)
mutant 5 rc=1 scripts/require-crit-review.py: the malformed-block check dropped (test_s1_replan_is_read_from_the_record_block_json)
mutant 6 rc=1 scripts/regime-counters.sh: the counters read no replans (test_s1_replan_token_comes_from_the_record_block_json)
mutant 7 rc=1 scripts/regime-counters.sh: the counters take any part (test_s1_reports_replan_missing_without_the_four_keys)
mutant 8 rc=1 scripts/orchestrator/acceptance-front-matter.py: the writer takes extra parts (test_front_matter_keeps_and_validates_the_replans_object)
mutant 9 rc=1 scripts/orchestrator/acceptance-front-matter.py: the writer writes no replans (test_front_matter_keeps_and_validates_the_replans_object)
baseline rc=0: the 6 tests on the unmutated tree
[exit 0]
```

## 7. Caps, and the test environment

```console
$ git status --porcelain -- scripts tests; git diff --numstat origin/main...HEAD
11	3	scripts/orchestrator/acceptance-front-matter.py
25	4	scripts/orchestrator/chain-integrate.sh
8	9	scripts/regime-counters.sh
20	13	scripts/require-crit-review.py
12	3	tests/fixtures/gate-evidence/acceptance-s6-present.md
56	0	tests/unit/test_chain_glue.py
30	0	tests/unit/test_orchestrator_tools.py
33	29	tests/unit/test_regime_counters.py
71	45	tests/unit/test_require_crit_review.py
[exit 0]
```

Caps: outside `tests/` and `.orchestration/`, 64 added and 29 deleted lines, 93 changed (cap 200); under `tests/`, 202 added and 77 deleted (cap 1000 added).

The test environment. Before the override above, the gate suite failed on an unmodified `origin/main` checkout (a scratch worktree at `$S/om`, removed afterwards with `git worktree remove`) as on this branch: `(cd "$S/om" && UV_OFFLINE=1 uv run python -m unittest tests/unit/test_require_crit_review.py > "$S/rcr-main.out" 2>&1)`, 132 of its 136 failures `--base 'main' does not resolve to a commit`. One of those tests also failed outside the sandbox, so the sandbox is not the cause; with the override the same run (to `$S/rcr-main3.out`) passed. The whole suite on this branch's code (before the rebase, the same tree for `scripts/` and `tests/`; to `$S/all.out`) has 68 failures and 10 errors in six modules this task does not touch, and the same six modules fail alike on `origin/main` (to `$S/six-main.out`). The summaries, read back from those files:

```console
$ /usr/bin/grep -E "^Ran|^OK|^FAILED" "$S/rcr-main.out"; /usr/bin/grep -c "does not resolve to a commit" "$S/rcr-main.out"
Ran 96 tests in 32.131s
FAILED (failures=136)
132
[exit 0]
```
```console
$ /usr/bin/grep -E "^Ran|^OK|^FAILED" "$S/rcr-main3.out"
Ran 96 tests in 59.860s
OK
[exit 0]
```
```console
$ /usr/bin/grep -E "^Ran|^OK|^FAILED" "$S/all.out"; /usr/bin/grep -E "^(FAIL|ERROR): test" "$S/all.out" | sed -E "s/.*[(]([a-z_]+)[.].*/\1/" | sort | uniq -c | sort -r
Ran 1162 tests in 636.893s
FAILED (failures=68, errors=10, skipped=2)
  31 test_herdr_agents
  28 test_agent_stop_gate
   8 test_runtime_health
   5 test_gh_auth
   4 test_supply_chain_policy
   2 test_aws_cli_acquisition
[exit 0]
```
```console
$ /usr/bin/grep -E "^Ran|^OK|^FAILED" "$S/six-main.out"
Ran 343 tests in 370.884s
FAILED (failures=68, errors=10, skipped=1)
[exit 0]
```

The CompactionDB entry, in the worktree's own database (the orchestrator consolidates at acceptance):

```console
$ UV_OFFLINE=1 uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] The S1 re-plan is the record block replans object {<class>: {specification, design, implementation, verification}}, written by acceptance-front-matter.py (exit 2 on another shape), read by require-crit-review.py and regime-counters.sh; no prose re-plan line is parsed. chain-integrate.sh lets an update-branch-only head (second parent an ancestor of origin/main, same PR patch-id) inherit its parent audit with a first line inherited-from: <sha7>, kept through a chain of inheritances; the gate keys its finding ids under that sha7. (T129 audit-inherit replan-json a01, ec4ba99d)"
e0e1d43c-9ac6-4cd0-a64c-935ab3ef7871
[exit 0]
```
```console
$ UV_OFFLINE=1 uv run --no-project .claude/hooks/contextdb_cli.py memory search replans
e0e1d43c-9ac6-4cd0-a64c-935ab3ef7871 [project/decision] [memory:decision] The S1 re-plan is the record block replans object {<class>: {specification, design, implementation, verification}}, written by acceptance-front-matter.py (exit 2 on another shape), read by require-crit-review.py and regime-counters.sh; no prose re-plan line is parsed. chain-integrate.sh lets an update-branch-only head (second parent an ancestor of origin/main, same PR patch-id) inherit its parent audit with a first line inherited-from: <sha7>, kept through …
[exit 0]
```
