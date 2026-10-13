# Validation: dotfiles-T128-gate-evidence-a03

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `regime/gate-evidence` (PR #329), except §10, run in the main checkout. Test runs set `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` (sandbox record). Scratch file names (`numstat.txt`, `caps.py`, `mutate6.sh`, `mutations.py`, `fail-*.txt`) live in the session's `$TMPDIR`. This branch copy covers the code head `f5f980f9`; the main-checkout copy adds the final head, CI and the Bot wait.

## 1. Task file and the a01, a02 history copies

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-gate-evidence-a03.md .orchestration/dotfiles-T128-gate-evidence-a03/task.md | cut -c1-64
686806a1b6cff143eef371f518098ac8b926fbe91462c1f8a5ac67d6e07c482e
686806a1b6cff143eef371f518098ac8b926fbe91462c1f8a5ac67d6e07c482e
$ git diff --quiet 61d90302 HEAD -- .orchestration/dotfiles-T128-gate-evidence-a01/ .orchestration/dotfiles-T128-gate-evidence-a02/ && echo "a01 and a02 records unchanged since 61d90302"
a01 and a02 records unchanged since 61d90302
```

## 2. Baseline: the module on `origin/main` inside the sandbox

```
$ uv run --no-project python -m unittest tests/unit/test_require_crit_review.py 2>&1 | tail -4   # at origin/main 683384ea, the sandbox's default git config
----------------------------------------------------------------------
Ran 71 tests in 37.721s

FAILED (failures=73)
$ d=$(mktemp -d "$TMPDIR/gtest.XXXX"); git -C "$d" init -q; git -C "$d" config user.email a@b; git -C "$d" config user.name A; echo x > "$d/README.md"; git -C "$d" add README.md; git -C "$d" commit -qm init; echo "commit rc=$?"   # the fixture's first commit, reproduced; the home directory is shown as ~ (the masker's normalisation)
error: Couldn't load public key ~/.ssh/id_ed25519.pub: No such file or directory?

fatal: failed to write commit object
commit rc=128
$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false uv run --no-project python -m unittest tests/unit/test_require_crit_review.py 2>&1 | tail -4   # at origin/main 683384ea
----------------------------------------------------------------------
Ran 71 tests in 59.577s

OK
```

## 3. The module at the code head (86 tests; 71 on origin/main, §2)

```
$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false uv run --no-project python -m unittest tests/unit/test_require_crit_review.py -v 2>&1 | sed -E 's/ \(tests[^)]*\)//' | grep -E ' \.\.\. |^Ran|^OK|^FAILED'   # the working tree that became f5f980f9
test_acceptance_record_head_must_be_head ... ok
test_acceptance_record_is_not_counted_as_a_change ... ok
test_acceptance_record_pr_must_be_the_swept_pr ... ok
test_acceptance_record_prose_is_not_read ... ok
test_acceptance_record_refuses_a_duplicate_key ... ok
test_acceptance_record_refuses_a_non_finite_number ... ok
test_advanced_base_cannot_delete_collector_to_trigger_head_fallback ... ok
test_advanced_base_cannot_supply_an_untrusted_collector ... ok
test_agent_lifecycle_script_change_requires_review ... ok
test_agent_lifecycle_surfaces_require_review ... ok
test_agent_lifecycle_tokens_require_review ... ok
test_agent_reviewer_rejects_empty_or_malformed_crit_data ... ok
test_agent_reviewer_rejects_invalid_review_outcome ... ok
test_agent_reviewer_with_command_string_source_still_requires_review ... ok
test_agent_reviewer_with_crit_data_satisfies_required_review ... ok
test_agent_reviewer_with_crit_reviewed_marker_still_requires_review ... ok
test_agent_reviewer_with_external_crit_json_still_requires_review ... ok
test_agent_reviewer_with_non_review_crit_json_object_still_requires_review ... ok
test_agent_reviewer_with_resolved_line_comment_satisfies_required_review ... ok
test_agent_reviewer_with_unresolved_crit_json_still_requires_review ... ok
test_agent_self_review_flag_evidence_still_requires_review ... ok
test_agent_self_reviewer_evidence_still_requires_review ... ok
test_audit_finding_reason_may_quote_the_grammar ... ok
test_audit_must_name_head_and_live_under_validation ... ok
test_base_accepts_a_correct_audit_of_head ... ok
test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base ... ok
test_base_fails_closed_when_github_metadata_is_unavailable ... ok
test_base_fails_closed_when_unresolvable_or_option_like ... ok
test_base_rejects_forged_evidence_metadata ... ok
test_base_rejects_pr_commits_before_executing_their_collector ... ok
test_base_rejects_side_branch_and_advanced_base_containing_pr_commits ... ok
test_base_requires_an_acceptance_record_under_acceptance ... ok
test_base_requires_audit_evidence_for_a_reviewed_change ... ok
test_base_requires_pr_feedback_evidence ... ok
test_base_reviews_committed_branch_changes ... ok
test_blocked_or_missing_audit_verdict_fails ... ok
test_broad_diff_requires_review ... ok
test_broad_orchestration_only_pr_needs_no_audit ... ok
test_companion_must_be_this_audits_own_last_message ... ok
test_disposition_parsing_is_linear ... ok
test_dispositions_of_2026_10_12_without_evidence_are_refused ... ok
test_dispositions_with_an_evidence_command_are_accepted ... ok
test_explicit_disable_skips_guard ... ok
test_feedback_accepts_absolute_path_through_a_repository_parent_alias ... ok
test_feedback_cannot_hide_an_arbitrary_path_without_base ... ok
test_feedback_does_not_exclude_symlink_aliases_outside_validation ... ok
test_feedback_path_itself_must_be_under_validation ... ok
test_feedback_symlink_cannot_hide_a_file_outside_validation ... ok
test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent ... ok
test_github_lookup_ignores_environment_repository_override ... ok
test_github_lookup_rejects_evidence_from_another_repository ... ok
test_high_risk_markdown_change_requires_review ... ok
test_incorrect_audit_needs_audit_findings ... ok
test_incorrect_audit_without_findings_fails ... ok
test_large_untracked_file_requires_broad_diff_review ... ok
test_missing_base_collector_falls_back_only_after_binding ... ok
test_native_reviewed_environment_rejects_human_reviewer ... ok
test_native_reviewed_without_evidence_still_requires_review ... ok
test_no_diff_does_not_require_review ... ok
test_older_base_must_not_be_on_the_head_first_parent_chain ... ok
test_orchestration_only_pr_needs_no_audit ... ok
test_pr_feedback_accepts_complete_evidence_without_a_bot_review ... ok
test_pr_feedback_accepts_complete_root_cause_dispositions ... ok
test_pr_feedback_bodies_are_compared_after_secret_masking ... ok
test_pr_feedback_evidence_file_is_not_counted_as_a_change ... ok
test_pr_feedback_fails_when_the_collector_cannot_run ... ok
test_pr_feedback_fixed_commit_must_be_in_the_pr_range ... ok
test_pr_feedback_matches_a_masked_path_but_not_an_edited_one ... ok
test_pr_feedback_must_be_collected_for_the_current_head ... ok
test_pr_feedback_must_cover_every_currently_collected_item ... ok
test_pr_feedback_rejects_evidence_outside_the_repository ... ok
test_pr_feedback_rejects_incomplete_or_invalid_dispositions ... ok
test_pr_feedback_requires_the_github_head_to_match ... ok
test_pr_feedback_uses_the_base_collector_not_the_prs_own ... ok
test_pr_feedback_without_base_is_only_format_checked ... ok
test_recollection_must_match_the_authenticated_repository ... ok
test_retired_audit_dispositions_is_not_read ... ok
test_reviewed_environment_satisfies_required_review ... ok
test_reviewed_with_blank_evidence_values_still_requires_review ... ok
test_reviewed_with_incomplete_evidence_still_requires_review ... ok
test_s6_class_at_three_with_the_matching_searches_entry_is_accepted ... ok
test_s6_class_at_three_without_a_searches_entry_is_refused ... ok
test_s6_searches_entry_must_equal_the_recomputed_records_search ... ok
test_small_docs_only_change_does_not_require_review ... ok
test_the_gate_has_no_github_identity_check ... ok
test_verdict_comes_only_from_the_last_message_file ... ok
Ran 86 tests in 79.812s
OK
```

## 4. Each rule fails a test when broken

```
$ bash mutate6.sh | grep -v '^AssertionError'   # runs the 17 new or changed tests on this change; on origin/main's guard (M0), on a02's final head 61d90302 (M1) and on the YAML form 7581d590 (M1b); and on nineteen mutations of this guard (M2 to M20, mutations.py); it restores the guard and checks it with cmp
== control: this change
Ran 17 tests in 27.685s
OK
== M0 origin/main guard
ERROR: test_disposition_parsing_is_linear
FAIL: test_dispositions_of_2026_10_12_without_evidence_are_refused
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='no evidence clause')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='empty evidence command')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='empty reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='a second evidence delimiter as the reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='a second evidence delimiter padding a failure reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short failure reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short in-progress reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short cancelled reason')
FAIL: test_s6_class_at_three_without_a_searches_entry_is_refused
FAIL: test_s6_class_at_three_with_the_matching_searches_entry_is_accepted
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a record missing]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a record too many]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [another class's entry]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a pasted command for its records]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/validation/test.md')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/other.md')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/alias.md')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/test.md')
FAIL: test_base_requires_an_acceptance_record_under_acceptance [no block]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [not JSON]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [a list, not an object]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [a non-finite number]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [a duplicate key]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [format]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [task]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [head]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [pr]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [pr of another PR]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [ledger id]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [ledger class]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [searches records]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [searches twice for one class]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [audit_findings entry]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [S6]
FAIL: test_acceptance_record_head_must_be_head
FAIL: test_acceptance_record_prose_is_not_read
FAIL: test_audit_finding_reason_may_quote_the_grammar
FAIL: test_acceptance_record_pr_must_be_the_swept_pr
FAIL: test_acceptance_record_refuses_a_duplicate_key
FAIL: test_acceptance_record_refuses_a_non_finite_number
FAIL: test_incorrect_audit_needs_audit_findings [no audit_findings]
FAIL: test_incorrect_audit_needs_audit_findings [a fix]
FAIL: test_incorrect_audit_needs_audit_findings [short reason]
FAIL: test_incorrect_audit_needs_audit_findings [no evidence]
FAIL: test_incorrect_audit_needs_audit_findings [empty evidence]
FAIL: test_incorrect_audit_needs_audit_findings [one missing]
FAIL: test_incorrect_audit_needs_audit_findings [same finding twice]
FAIL: test_incorrect_audit_needs_audit_findings [out of range]
FAIL: test_incorrect_audit_needs_audit_findings [accepted]
FAIL: test_acceptance_record_is_not_counted_as_a_change
FAIL: test_retired_audit_dispositions_is_not_read
Ran 17 tests in 29.569s
FAILED (failures=54, errors=1)
== M1 guard at 61d90302 (a02's final head)
ERROR: test_disposition_parsing_is_linear
FAIL: test_s6_class_at_three_without_a_searches_entry_is_refused
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a record missing]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a record too many]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [another class's entry]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a pasted command for its records]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search
FAIL: test_base_requires_an_acceptance_record_under_acceptance [no block]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [not JSON]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [a list, not an object]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [a non-finite number]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [a duplicate key]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [format]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [task]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [head]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [pr]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [pr of another PR]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [ledger id]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [ledger class]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [searches records]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [searches twice for one class]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [audit_findings entry]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [S6]
FAIL: test_acceptance_record_head_must_be_head
FAIL: test_acceptance_record_prose_is_not_read
FAIL: test_audit_finding_reason_may_quote_the_grammar
FAIL: test_acceptance_record_pr_must_be_the_swept_pr
FAIL: test_acceptance_record_refuses_a_duplicate_key
FAIL: test_acceptance_record_refuses_a_non_finite_number
FAIL: test_incorrect_audit_needs_audit_findings [no audit_findings]
FAIL: test_incorrect_audit_needs_audit_findings [a fix]
FAIL: test_incorrect_audit_needs_audit_findings [short reason]
FAIL: test_incorrect_audit_needs_audit_findings [no evidence]
FAIL: test_incorrect_audit_needs_audit_findings [empty evidence]
FAIL: test_incorrect_audit_needs_audit_findings [one missing]
FAIL: test_incorrect_audit_needs_audit_findings [same finding twice]
FAIL: test_incorrect_audit_needs_audit_findings [out of range]
FAIL: test_incorrect_audit_needs_audit_findings [accepted]
FAIL: test_retired_audit_dispositions_is_not_read
Ran 17 tests in 30.695s
FAILED (failures=38, errors=1)
== M1b guard at 7581d590 (a03 fix round 1, the YAML form before amendment 1)
FAIL: test_dispositions_with_an_evidence_command_are_accepted
FAIL: test_s6_class_at_three_without_a_searches_entry_is_refused
FAIL: test_s6_class_at_three_with_the_matching_searches_entry_is_accepted
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [the matching set]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [none where nothing matches]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a record missing]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a record too many]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [another class's entry]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a pasted command for its records]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search
FAIL: test_base_requires_an_acceptance_record_under_acceptance [no block]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [not JSON]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [a list, not an object]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [a non-finite number]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [a duplicate key]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [format]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [task]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [head]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [pr]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [pr of another PR]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [ledger id]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [ledger class]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [searches records]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [searches twice for one class]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [audit_findings entry]
FAIL: test_base_requires_an_acceptance_record_under_acceptance [S6]
FAIL: test_acceptance_record_head_must_be_head
FAIL: test_acceptance_record_prose_is_not_read
FAIL: test_audit_finding_reason_may_quote_the_grammar
FAIL: test_acceptance_record_pr_must_be_the_swept_pr
FAIL: test_acceptance_record_refuses_a_duplicate_key
FAIL: test_acceptance_record_refuses_a_non_finite_number
FAIL: test_incorrect_audit_needs_audit_findings [no audit_findings]
FAIL: test_incorrect_audit_needs_audit_findings [a fix]
FAIL: test_incorrect_audit_needs_audit_findings [short reason]
FAIL: test_incorrect_audit_needs_audit_findings [no evidence]
FAIL: test_incorrect_audit_needs_audit_findings [empty evidence]
FAIL: test_incorrect_audit_needs_audit_findings [one missing]
FAIL: test_incorrect_audit_needs_audit_findings [same finding twice]
FAIL: test_incorrect_audit_needs_audit_findings [out of range]
FAIL: test_incorrect_audit_needs_audit_findings [accepted]
FAIL: test_acceptance_record_is_not_counted_as_a_change
FAIL: test_retired_audit_dispositions_is_not_read
Ran 17 tests in 406.506s
FAILED (failures=43)
== M2 a second delimiter allowed
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='a second evidence delimiter padding a failure reason')
FAIL: test_disposition_parsing_is_linear
Ran 17 tests in 17.560s
FAILED (failures=2)
== M3 an empty command allowed
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='empty evidence command')
Ran 17 tests in 17.347s
FAILED (failures=1)
== M4 head not compared
FAIL: test_base_requires_an_acceptance_record_under_acceptance [head]
FAIL: test_acceptance_record_head_must_be_head
Ran 17 tests in 17.347s
FAILED (failures=2)
== M5 task not compared
FAIL: test_base_requires_an_acceptance_record_under_acceptance [task]
Ran 17 tests in 17.338s
FAILED (failures=1)
== M6 format not checked
FAIL: test_base_requires_an_acceptance_record_under_acceptance [format]
Ran 17 tests in 17.477s
FAILED (failures=1)
== M7 ledger id not checked
FAIL: test_base_requires_an_acceptance_record_under_acceptance [ledger id]
Ran 17 tests in 17.385s
FAILED (failures=1)
== M8 ledger class not checked
FAIL: test_base_requires_an_acceptance_record_under_acceptance [ledger class]
Ran 17 tests in 17.369s
FAILED (failures=1)
== M9 searches set not compared
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a record missing]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a record too many]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [a pasted command for its records]
Ran 17 tests in 17.683s
FAILED (failures=3)
== M10 a missing records directory searched as empty
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search
Ran 17 tests in 18.408s
FAILED (failures=1)
== M11 audit coverage not checked
FAIL: test_incorrect_audit_needs_audit_findings [one missing]
Ran 17 tests in 17.906s
FAILED (failures=1)
== M12 a finding dispositioned twice
FAIL: test_incorrect_audit_needs_audit_findings [same finding twice]
Ran 17 tests in 17.946s
FAILED (failures=1)
== M13 a fixed entry not named
FAIL: test_base_requires_an_acceptance_record_under_acceptance [audit_findings entry]
FAIL: test_incorrect_audit_needs_audit_findings [a fix]
Ran 17 tests in 18.325s
FAILED (failures=2)
== M14 short audit reasons accepted
FAIL: test_incorrect_audit_needs_audit_findings [short reason]
Ran 17 tests in 17.357s
FAILED (failures=1)
== M15 a classes: line not required at the line start
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search [the matching set]
Ran 17 tests in 17.723s
FAILED (failures=1)
== M16 record not bound to the task
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/other.md')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/alias.md')
Ran 17 tests in 18.510s
FAILED (failures=2)
== M17 record counted as a change
FAIL: test_acceptance_record_is_not_counted_as_a_change
Ran 17 tests in 25.299s
FAILED (failures=1)
== M18 duplicate keys kept
FAIL: test_base_requires_an_acceptance_record_under_acceptance [a duplicate key]
FAIL: test_acceptance_record_refuses_a_duplicate_key
Ran 17 tests in 25.227s
FAILED (failures=2)
== M19 pr not compared with the swept pr
FAIL: test_base_requires_an_acceptance_record_under_acceptance [pr of another PR]
FAIL: test_acceptance_record_pr_must_be_the_swept_pr
Ran 17 tests in 17.973s
FAILED (failures=2)
== M20 non-finite numbers accepted
FAIL: test_base_requires_an_acceptance_record_under_acceptance [a non-finite number]
FAIL: test_acceptance_record_refuses_a_non_finite_number
Ran 17 tests in 16.945s
FAILED (failures=2)
guard restored
```

## 5. Fixture provenance, the right fixture's evidence commands, the gate's standard-library imports, thread 4248232955's evidence, the present fixture's records, prettier and the JSON block, the YAML form's pruned uv cache (thread 4250238721), fixture size

```
$ uv run --no-project python -c 'import json,sys; d=json.load(open(sys.argv[1])); print("head_sha", d["head_sha"], "generated_at", d["generated_at"]); [print(i["url"].rsplit("_r",1)[1], i["disposition"]) for i in d["items"] if (i.get("url") or "").endswith(("r4244248692","r4244378809"))]' ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-pr-feedback.json
head_sha 3a54d340e9078ba3565237f6d73a00d8fc2d75e9 generated_at 2026-10-12T03:21:31+00:00
4244248692 not-applicable:the table's unit is a controlled path; the forced removal is an orchestrator control-plane action behind the human-only permission gate, covered by the SKILL row
4244378809 not-applicable:the first RESULT's head binding to the PR head is the orchestrator's acceptance check, performed before every acceptance action; the table's unit is a PR-controlled path
$ uv run --no-project python -c 'import json,sys; [print(i["url"].rsplit("_r",1)[1], i["disposition"]) for i in json.load(open(sys.argv[1]))["items"]]' tests/fixtures/gate-evidence/pr-feedback-wrong.json
4244248692 not-applicable:the table's unit is a controlled path; the forced removal is an orchestrator control-plane action behind the human-only permission gate, covered by the SKILL row
4244378809 not-applicable:the first RESULT's head binding to the PR head is the orchestrator's acceptance check, performed before every acceptance action; the table's unit is a PR-controlled path
$ uv run --no-project python -c 'import json,sys; w,r=[json.load(open(p))["items"] for p in sys.argv[1:]]; strip=lambda xs:[{k:v for k,v in x.items() if k!="disposition"} for x in xs]; print("same-items=%s right-extends-wrong=%s" % (strip(w)==strip(r), all(b["disposition"].startswith(a["disposition"]+"; evidence=") for a,b in zip(w,r))))' tests/fixtures/gate-evidence/pr-feedback-wrong.json tests/fixtures/gate-evidence/pr-feedback-right.json
same-items=True right-extends-wrong=True
$ grep -n -E '"defaultMode"|"ask"' home/.chezmoitemplates/claude-settings-managed.json
31:    "defaultMode": "auto",
32:    "ask": []
$ sed -n '114p' scripts/regime-counters.sh
     head: ($results[0] // null | if . then tok("head") else null end | if . and test("^[0-9a-f]{7,40}$") then . else null end),
$ grep -n -E '^(import|from) ' scripts/require-crit-review.py; grep -c -E 'yaml|"uv"|subprocess.run\(\s*\["grep"' scripts/require-crit-review.py   # the gate's imports: the standard library only
4:from __future__ import annotations
6:import argparse
7:import importlib.util
8:import json
9:import os
10:import re
11:import subprocess
12:import tempfile
13:from collections import Counter
14:from functools import cache
15:import sys
16:from pathlib import Path
1
$ grep -n 'ACCEPTANCE_EVIDENCE' .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md   # main checkout; thread 4248232955's evidence
83:6. Orchestrator Playbook step 10.4 (line 170): the gate command gains `ACCEPTANCE_EVIDENCE=<acceptance record>` beside `PR_FEEDBACK_EVIDENCE` (required in PR mode once `dotfiles-T128-gate-evidence-a02` lands; the record whose ledger and `search:` line the g
$ grep -rl 'classes:.*class-count-scope' .orchestration/learning/mistakes/; echo rc=$?   # main checkout: the present fixture's records
.orchestration/learning/mistakes/M-20261012-3.md
rc=0
$ printf -- "---
{<a one-line JSON record with a two-row ledger>}
---

# prose
" > default/r.md; cp it to fixtures/r.md beside a copy of tests/fixtures/gate-evidence/.prettierrc; prettier --write */r.md; then for each: cat r.md; json.loads(the block)
== default/r.md after prettier --write
---
{
  "format": 1,
  "task": "test",
  "head": "HEAD",
  "pr": 1,
  "ledger":
    [
      { "id": 4244128846, "class": "class-count-scope" },
      { "id": "audit:3a54d34:2", "class": "class-count-scope" },
    ],
  "searches": [],
}
---

# prose
json.decoder.JSONDecodeError: Illegal trailing comma before end of array: line 9 column 64 (char 203)
== fixtures/r.md after prettier --write (with .prettierrc trailingComma none)
---
{
  "format": 1,
  "task": "test",
  "head": "HEAD",
  "pr": 1,
  "ledger":
    [
      { "id": 4244128846, "class": "class-count-scope" },
      { "id": "audit:3a54d34:2", "class": "class-count-scope" }
    ],
  "searches": []
}
---

# prose
json.loads: ok
$ cat tests/fixtures/gate-evidence/.prettierrc; prettier --check tests/fixtures/gate-evidence/*.md
{ "trailingComma": "none" }
All matched files use Prettier code style!
# The YAML form before amendment 1 (b2b3db45 to 7581d590): the pruned uv cache, thread 4250238721
$ uv run --no-project python - <<'PY'   # 00:5xZ: the gate's offline YAML command, as load_yaml runs it, from a temporary cwd
rc 1
out 
err error: No solution found when resolving `--with` dependencies
  cause: Because pyyaml was not found in the cache and you require pyyaml, we can conclude that your requirements are unsatisfiable.

hint: Packages were unavailable because the network was disabled. When the network is disabled, registry packages may only be read from the cache.
$ uv cache dir; UV_OFFLINE=1 uv run --no-project --with pyyaml python -c 'import yaml; print(yaml.__version__)' 2>&1 | tail -2; du -sh "$(uv cache dir)"
~/.cache/uv

hint: Packages were unavailable because the network was disabled. When the network is disabled, registry packages may only be read from the cache.
 38M	~/.cache/uv
$ uv run --no-project --with pyyaml python -c 'import yaml; print("pyyaml", yaml.__version__)' 2>&1 | tail -2; UV_OFFLINE=1 uv run --no-project --with pyyaml python -c 'import yaml; print("offline ok", yaml.__version__)' 2>&1 | tail -1   # allowed_domains pypi.org, files.pythonhosted.org
pyyaml 6.0.3
offline ok 6.0.3
$ wc -l tests/fixtures/gate-evidence/*
      18 tests/fixtures/gate-evidence/acceptance-duplicate-key.md
      20 tests/fixtures/gate-evidence/acceptance-finding-quotes-grammar.md
      12 tests/fixtures/gate-evidence/acceptance-nan.md
      18 tests/fixtures/gate-evidence/acceptance-s6-missing.md
      18 tests/fixtures/gate-evidence/acceptance-s6-present.md
      12 tests/fixtures/gate-evidence/acceptance-stale-head.md
      12 tests/fixtures/gate-evidence/acceptance-wrong-pr.md
       4 tests/fixtures/gate-evidence/pr-feedback-right.json
       4 tests/fixtures/gate-evidence/pr-feedback-wrong.json
     118 total
```

## 6. `make require-crit-review` without `BASE` on a records-only tree (step 4)

```
$ git -C <scratch> rev-parse --short HEAD; git -C <scratch> status --short; make -C <scratch> require-crit-review; echo rc=$?
f5f980f9
?? .orchestration/reports/probe.md
Review not required: no meaningful review trigger found.
rc=0
$ git -C <scratch> rev-parse --short HEAD; git -C <scratch> status --short; make -C <scratch> require-crit-review; echo rc=$?
ce0af5d0
?? .orchestration/reports/probe.md
Review not required: no meaningful review trigger found.
rc=0
```

## 7. Full unit suite at the code head against `origin/main`

```
$ git rev-parse --short HEAD && UV_OFFLINE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false uv run --no-project --with pyyaml python -m unittest discover -s tests/unit > unit-all-am.txt 2>&1; echo "rc=$?"; tail -3 unit-all-am.txt; grep -E '^(FAIL|ERROR): .*\(' unit-all-am.txt | grep -oE '\(([a-z_]+\.)*test_[a-z_0-9]+\.[A-Za-z]+\.[a-z_0-9]+\)' | tr -d '()' | sed 's/^tests\.unit\.//' | sort > fail-am.txt; wc -l < fail-am.txt; cmp fail-base.txt fail-am.txt && echo "identical to the origin/main failing set"
f5f980f9
rc=1
Ran 1011 tests in 539.686s

FAILED (failures=68, errors=10, skipped=2)
      78
identical to the origin/main failing set

$ git worktree add --detach basewt origin/main; cd basewt && UV_OFFLINE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false uv run --no-project --with pyyaml python -m unittest tests.unit.test_agent_stop_gate tests.unit.test_aws_cli_acquisition tests.unit.test_gh_auth tests.unit.test_herdr_agents tests.unit.test_runtime_health tests.unit.test_supply_chain_policy > unit-base6.txt 2>&1; echo "rc=$?"; tail -3 unit-base6.txt   # at 683384ea; fail-base.txt holds its FAIL/ERROR test ids, extracted as above
683384ea
rc=1
Ran 335 tests in 335.301s

FAILED (failures=68, errors=10, skipped=1)

$ cut -d. -f1 fail-base.txt | uniq -c
  28 test_agent_stop_gate
   2 test_aws_cli_acquisition
   5 test_gh_auth
  31 test_herdr_agents
   8 test_runtime_health
   4 test_supply_chain_policy
```

## 8. Format and lint

```
$ ruff format --config ruff.toml --check scripts/require-crit-review.py tests/unit/test_require_crit_review.py
2 files already formatted
$ prettier --check README.md tests/fixtures/gate-evidence/*.md .orchestration/dotfiles-T128-gate-evidence-a03/*.md
Checking formatting...
All matched files use Prettier code style!
$ ruff check --config ruff.toml --output-format concise scripts/require-crit-review.py tests/unit/test_require_crit_review.py | sed -E "s/:[0-9]+:[0-9]+:/:/" | sort | uniq -c   # not a CI gate (CI runs ruff format --check)
   1 [*] 3 fixable with `--fix` (3 unsafe fixes available with `--fix --unsafe-fixes`).
   1 Found 6 errors.
   1 scripts/require-crit-review.py: FURB167 [*] Use of regular expression alias `re.M`
   1 scripts/require-crit-review.py: I001 [*] Import block is un-sorted or un-formatted
   2 scripts/require-crit-review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   1 tests/unit/test_require_crit_review.py: I001 [*] Import block is un-sorted or un-formatted
   1 tests/unit/test_require_crit_review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
$ (the same ruff check on the origin/main copies of both files, in a scratch directory)
   1 [*] 4 fixable with `--fix` (3 unsafe fixes available with `--fix --unsafe-fixes`).
   1 Found 7 errors.
   1 scripts/require-crit-review.py: FURB167 [*] Use of regular expression alias `re.M`
   1 scripts/require-crit-review.py: FURB167 [*] Use of regular expression alias `re.S`
   1 scripts/require-crit-review.py: I001 [*] Import block is un-sorted or un-formatted
   2 scripts/require-crit-review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   1 tests/unit/test_require_crit_review.py: I001 [*] Import block is un-sorted or un-formatted
   1 tests/unit/test_require_crit_review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
```

## 9. The replay onto the merge head, the diff size (INV-2: at most 15 files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`) and the moved base

```
$ git log --oneline -6; git diff --quiet 3c67f512 b2b3db45 -- . ':!.orchestration' && echo "b2b3db45's content outside .orchestration is the tested 3c67f512's (the replay onto 4e2266aa)"
f5f980f9 feat(gate): read the acceptance record's JSON block with the standard library (a03 amendment 1)
3c20b0ca docs(orchestration): gate-evidence a03 evidence at fix round 1 (7581d590)
7581d590 fix(gate): bind the record's pr to the swept PR and refuse duplicate YAML keys (a03 fix round 1)
c36fcd35 docs(orchestration): gate-evidence a03 branch evidence (b2b3db45)
b2b3db45 feat(gate): read the acceptance record as a YAML front matter bound to HEAD (a03)
4e2266aa Merge branch 'main' into regime/gate-evidence
b2b3db45's content outside .orchestration is the tested 3c67f512's (the replay onto 4e2266aa)
$ git merge-tree --write-tree origin/main f5f980f9 >/dev/null && echo "merges cleanly"; git rev-parse --short origin/main
merges cleanly
ce0af5d0
$ git diff --numstat origin/main...f5f980f9 > numstat.txt; cat numstat.txt
3	0	.orchestration/dotfiles-T128-gate-evidence-a01/autoskill.md
7	0	.orchestration/dotfiles-T128-gate-evidence-a01/learning.md
44	0	.orchestration/dotfiles-T128-gate-evidence-a01/report.md
15	0	.orchestration/dotfiles-T128-gate-evidence-a01/sandbox.md
94	0	.orchestration/dotfiles-T128-gate-evidence-a01/task.md
287	0	.orchestration/dotfiles-T128-gate-evidence-a01/validation.md
3	0	.orchestration/dotfiles-T128-gate-evidence-a02/autoskill.md
11	0	.orchestration/dotfiles-T128-gate-evidence-a02/learning.md
95	0	.orchestration/dotfiles-T128-gate-evidence-a02/report.md
16	0	.orchestration/dotfiles-T128-gate-evidence-a02/sandbox.md
98	0	.orchestration/dotfiles-T128-gate-evidence-a02/task.md
431	0	.orchestration/dotfiles-T128-gate-evidence-a02/validation.md
3	0	.orchestration/dotfiles-T128-gate-evidence-a03/autoskill.md
12	0	.orchestration/dotfiles-T128-gate-evidence-a03/learning.md
120	0	.orchestration/dotfiles-T128-gate-evidence-a03/report.md
18	0	.orchestration/dotfiles-T128-gate-evidence-a03/sandbox.md
104	0	.orchestration/dotfiles-T128-gate-evidence-a03/task.md
498	0	.orchestration/dotfiles-T128-gate-evidence-a03/validation.md
3	3	Makefile
5	5	README.md
270	68	scripts/require-crit-review.py
1	0	tests/fixtures/gate-evidence/.prettierrc
18	0	tests/fixtures/gate-evidence/acceptance-duplicate-key.md
20	0	tests/fixtures/gate-evidence/acceptance-finding-quotes-grammar.md
12	0	tests/fixtures/gate-evidence/acceptance-nan.md
18	0	tests/fixtures/gate-evidence/acceptance-s6-missing.md
18	0	tests/fixtures/gate-evidence/acceptance-s6-present.md
12	0	tests/fixtures/gate-evidence/acceptance-stale-head.md
12	0	tests/fixtures/gate-evidence/acceptance-wrong-pr.md
4	0	tests/fixtures/gate-evidence/pr-feedback-right.json
4	0	tests/fixtures/gate-evidence/pr-feedback-wrong.json
415	39	tests/unit/test_require_crit_review.py
$ uv run --no-project python caps.py numstat.txt   # caps.py: count files outside .orchestration/, added lines outside tests/, added lines under tests/
files outside .orchestration: 14
added outside tests/ (and .orchestration): 278
added under tests/: 534

```

## 10. CompactionDB (main checkout, through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T128-gate-evidence-a01 (PR 329): scripts/require-crit-review.py accepts a not-applicable disposition only as not-applicable:<reason>; evidence=<command> (pr-feedback items and AUDIT_DISPOSITIONS audit-finding lines), and requires ACCEPTANCE_EVIDENCE=<acceptance record> under .orchestration/acceptance/ whenever BASE is set; a ledger class at three or more rows needs a search: line naming the class token, grep -l 'classes: over .orchestration/learning/mistakes/ and contextdb_cli.py memory search, else 'S6: class <slug> at <n> without a pasted search'." 2>&1 | tail -3   # under a01, 12:4xZ
7f2f0c0b-6d20-42af-97ac-c5cfcfe62ea7
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content "Claude worker sandbox: the global commit.gpgsign reads ~/.ssh/id_ed25519.pub, which the sandbox denies, so every git commit inside unit-test fixture repos fails (tests/unit/test_require_crit_review.py: 73 failures on unmodified origin/main); run such modules with GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false and establish the base result before attributing a failure to the change." 2>&1 | tail -3   # same call
f939c61c-9822-407c-9928-d67bec0531c6
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T128-gate-evidence-a02 (PR 329, 379845f7): ACCEPTANCE_EVIDENCE must be .orchestration/acceptance/<task>.md for the task named by the <task>-pr-feedback.json file (name and resolved name); every audit-finding line of that record carrying not-applicable needs '; evidence=<command>' whatever the audit verdict; the record is excluded from diff sizing; the S6 search line takes grep -rl 'classes:...' .orchestration/learning/mistakes/ or grep -l 'classes:...' .orchestration/learning/mistakes/*.md (grep -l on the bare directory exits 2, Is a directory) plus contextdb_cli.py memory search." 2>&1 | tail -2   # under a02
43f0ce26-7095-45a2-a86c-d8bfbe197b1d
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T128-gate-evidence-a02 amendment 1 (PR 329, c6cf0548): S6 reads no pasted command text; for each ledger class at three rows the gate runs grep -rl 'classes:.*<slug>' .orchestration/learning/mistakes/ from the repo root without a shell (slug must be [a-z0-9-], grep exit 2 refuses) and requires 'search: <slug> -> <basenames or none>' with the same set; the contextdb line is not validated. A not-applicable splits at its first '; evidence=' and a second delimiter is refused everywhere the gate reads one." 2>&1 | tail -1   # under a02 amendment 1
e74368c4-1073-4761-b26f-a4c9c735f0e3
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T128-gate-evidence-a03 (PR 329): the acceptance record (ACCEPTANCE_EVIDENCE=.orchestration/acceptance/<task>.md) starts with a YAML front matter the gate loads via uv run --no-config --no-project --with pyyaml python -I (temp cwd) and checks field by field: format 1, task, head == HEAD, pr, ledger [{id, class}], searches [{class, records}] equal as a set to the gate's own grep -rl 'classes:.*<class>' .orchestration/learning/mistakes/ for each class at three, audit_findings [{n, reason, evidence}] covering an incorrect audit; prose is not read; AUDIT_DISPOSITIONS is retired; a not-applicable is one split on the first '; evidence=' with a second delimiter refused." 2>&1 | tail -1   # under a03
00b54b12-cc2a-4bdb-9aaf-825ab367db47
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T128-gate-evidence-a03 amendment 1 (plan 013 A', PR 329): the acceptance record's machine-read part is one JSON object between its first two --- lines, read by scripts/require-crit-review.py with json.loads(object_pairs_hook refusing duplicate keys, parse_constant refusing NaN/Infinity), no PyYAML, no uv, no subprocess; the identity triple task/head/pr (pr = the swept PR) is checked first; S6 recomputes the mistake records with pathlib (a line beginning classes: containing the class). Fixtures under tests/fixtures/gate-evidence/ carry a .prettierrc with trailingComma none, because prettier formats the block as YAML front matter and would add trailing commas." 2>&1 | tail -1   # under a03 amendment 1
4ea2924d-1d6f-41f7-a14f-e4a5b9cf81f8
```
