# Validation: dotfiles-T128-gate-evidence-a01

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `regime/gate-evidence` (PR #329). Test runs set `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` (sandbox record). This branch copy covers the code head `9a860c95`; the main-checkout copy adds the final head, CI, the Bot wait and the CompactionDB `memory add`.

## 1. Task file (amendment 1) and the first copy

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md .orchestration/dotfiles-T128-gate-evidence-a01/task.md | cut -c1-64
d1b6fcf3f1f7aada49c8a38e79fae57525d135d59d9c44a3ef5ebc87e79a8d26
d1b6fcf3f1f7aada49c8a38e79fae57525d135d59d9c44a3ef5ebc87e79a8d26
$ git show 7f763b7f:.orchestration/dotfiles-T128-gate-evidence-a01/task.md | shasum -a 256 | cut -c1-64
73514492be0d1c9855e1d2d73eb40cbcddc8c6a1f011ad671df141dd4a491e8e
```

## 2. Baseline: the module on `origin/main` inside the sandbox

```
$ uv run --no-project python -m unittest tests/unit/test_require_crit_review.py 2>&1 | tail -4   # origin/main 683384ea, the sandbox's default git config
----------------------------------------------------------------------
Ran 71 tests in 37.721s

FAILED (failures=73)
$ d=$(mktemp -d "$TMPDIR/gtest.XXXX"); git -C "$d" init -q; …; git -C "$d" commit -qm init; echo "commit rc=$?"   # the fixture's first commit, reproduced
error: Couldn't load public key ~/.ssh/id_ed25519.pub: No such file or directory?

fatal: failed to write commit object
commit rc=128
$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false uv run --no-project python -m unittest tests/unit/test_require_crit_review.py 2>&1 | tail -4   # origin/main 683384ea
----------------------------------------------------------------------
Ran 71 tests in 59.577s

OK
```

## 3. The module at the code head (77 tests; the six new ones are `test_dispositions_*`, `test_s6_*` and `test_base_requires_an_acceptance_record_under_acceptance`)

```
$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false uv run --no-project python -m unittest tests/unit/test_require_crit_review.py -v 2>&1 | sed -E 's/ \(tests[^)]*\)//' | grep -E ' \.\.\. |^Ran|^OK|^FAILED'   # at 9a860c95
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
test_incorrect_audit_needs_not_applicable_dispositions ... ok
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
test_reviewed_environment_satisfies_required_review ... ok
test_reviewed_with_blank_evidence_values_still_requires_review ... ok
test_reviewed_with_incomplete_evidence_still_requires_review ... ok
test_s6_class_at_three_with_a_pasted_search_is_accepted ... ok
test_s6_class_at_three_without_a_pasted_search_is_refused ... ok
test_s6_search_line_names_the_class_token_and_both_commands ... ok
test_small_docs_only_change_does_not_require_review ... ok
test_the_gate_has_no_github_identity_check ... ok
test_verdict_comes_only_from_the_last_message_file ... ok
Ran 77 tests in 65.050s
OK
```

## 4. Each new check fails its test when broken

```
$ bash mutate.sh   # runs the 8 changed or new tests on this change, on origin/main's guard (M0), and on three one-line mutations of this guard (M1 evidence clause optional, M2 slug matched as a substring, M3 any one search part suffices); restores the guard and checks it with cmp
== control: this change
   1 OK
   1 Ran 8 tests in 14.228s
== M0 origin/main guard
   1 FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/none.md')
   1 FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/validation/test.md')
   1 FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='')
   1 FAIL: test_dispositions_of_2026_10_12_without_evidence_are_refused
   1 FAIL: test_incorrect_audit_needs_not_applicable_dispositions [no evidence clause]
   1 FAIL: test_incorrect_audit_needs_not_applicable_dispositions [short reason]
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='empty evidence command')
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='empty reason')
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='no evidence clause')
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short cancelled reason')
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short failure reason')
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short in-progress reason')
   1 FAIL: test_s6_class_at_three_with_a_pasted_search_is_accepted
   1 FAIL: test_s6_class_at_three_without_a_pasted_search_is_refused
   1 FAIL: test_s6_search_line_names_the_class_token_and_both_commands [another class's slug]
   1 FAIL: test_s6_search_line_names_the_class_token_and_both_commands [grep outside the mistake records]
   1 FAIL: test_s6_search_line_names_the_class_token_and_both_commands [not at the line start]
   1 FAIL: test_s6_search_line_names_the_class_token_and_both_commands [one command only]
   1 FAIL: test_s6_search_line_names_the_class_token_and_both_commands [pre-amendment grep -rl]
   1 FAILED (failures=19)
   1 Ran 8 tests in 16.142s
== M1 evidence clause optional
   1 FAIL: test_dispositions_of_2026_10_12_without_evidence_are_refused
   1 FAIL: test_incorrect_audit_needs_not_applicable_dispositions [no evidence clause]
   1 FAIL: test_incorrect_audit_needs_not_applicable_dispositions [short reason]
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='empty evidence command')
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='empty reason')
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='no evidence clause')
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short cancelled reason')
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short failure reason')
   1 FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short in-progress reason')
   1 FAILED (failures=9)
   1 Ran 8 tests in 14.155s
== M2 slug as substring
   1 FAIL: test_s6_search_line_names_the_class_token_and_both_commands [another class's slug]
   1 FAILED (failures=1)
   1 Ran 8 tests in 13.705s
== M3 one command suffices
   1 FAIL: test_s6_search_line_names_the_class_token_and_both_commands [grep outside the mistake records]
   1 FAIL: test_s6_search_line_names_the_class_token_and_both_commands [one command only]
   1 FAIL: test_s6_search_line_names_the_class_token_and_both_commands [pre-amendment grep -rl]
   1 FAILED (failures=3)
   1 Ran 8 tests in 13.623s
guard restored
```

## 5. Fixture provenance, the right fixture's evidence commands, fixture size

```
$ python3 -c "<print id + disposition of 4244248692 and 4244378809>" ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-pr-feedback.json
head_sha 3a54d340e9078ba3565237f6d73a00d8fc2d75e9 generated_at 2026-10-12T03:21:31+00:00
4244248692 not-applicable:the table's unit is a controlled path; the forced removal is an orchestrator control-plane action behind the human-only permission gate, covered by the SKILL row
4244378809 not-applicable:the first RESULT's head binding to the PR head is the orchestrator's acceptance check, performed before every acceptance action; the table's unit is a PR-controlled path
$ python3 -c "<same, from the wrong fixture>" tests/fixtures/gate-evidence/pr-feedback-wrong.json
4244248692 not-applicable:the table's unit is a controlled path; the forced removal is an orchestrator control-plane action behind the human-only permission gate, covered by the SKILL row
4244378809 not-applicable:the first RESULT's head binding to the PR head is the orchestrator's acceptance check, performed before every acceptance action; the table's unit is a PR-controlled path
$ uv run --no-project python - <<'PY'  # wrong vs right: items equal without disposition; each right disposition is the wrong one plus '; evidence=<command>'
same-items=True right-extends-wrong=True
$ grep -n -E '"defaultMode"|"ask"' home/.chezmoitemplates/claude-settings-managed.json
31:    "defaultMode": "auto",
32:    "ask": []
$ sed -n '114p' scripts/regime-counters.sh
     head: ($results[0] // null | if . then tok("head") else null end | if . and test("^[0-9a-f]{7,40}$") then . else null end),
$ wc -l tests/fixtures/gate-evidence/*
       8 tests/fixtures/gate-evidence/acceptance-s6-missing.md
      10 tests/fixtures/gate-evidence/acceptance-s6-present.md
       4 tests/fixtures/gate-evidence/pr-feedback-right.json
       4 tests/fixtures/gate-evidence/pr-feedback-wrong.json
      26 total
```

## 6. `make require-crit-review` without `BASE` on a records-only tree (step 4)

```
$ git -C <scratch> rev-parse --short HEAD; git -C <scratch> status --short; make -C <scratch> require-crit-review; echo rc=$?
9a860c95
?? .orchestration/reports/probe.md
Review not required: no meaningful review trigger found.
rc=0
$ git -C <scratch> rev-parse --short HEAD; git -C <scratch> status --short; make -C <scratch> require-crit-review; echo rc=$?
683384ea
?? .orchestration/reports/probe.md
Review not required: no meaningful review trigger found.
rc=0
```

## 7. Full unit suite at the code head against `origin/main`

```
$ git rev-parse --short HEAD && UV_OFFLINE=1 GIT_CONFIG_…=false uv run --no-project --with pyyaml python -m unittest discover -s tests/unit > unit-all-head.txt 2>&1; echo "rc=$?"; tail -3 unit-all-head.txt; <FAIL/ERROR test ids> > fail-head.txt; wc -l < fail-head.txt; cmp fail-base.txt fail-head.txt && echo "identical to the origin/main failing set"
9a860c95
rc=1
Ran 1002 tests in 528.352s

FAILED (failures=68, errors=10, skipped=2)
      78
identical to the origin/main failing set

$ git worktree add --detach basewt origin/main; cd basewt && UV_OFFLINE=1 GIT_CONFIG_…=false uv run --no-project --with pyyaml python -m unittest tests.unit.test_agent_stop_gate tests.unit.test_aws_cli_acquisition tests.unit.test_gh_auth tests.unit.test_herdr_agents tests.unit.test_runtime_health tests.unit.test_supply_chain_policy > unit-base6.txt 2>&1; echo "rc=$?"; tail -3 unit-base6.txt   # fail-base.txt is its FAIL/ERROR test ids
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
$ prettier --check README.md tests/fixtures/gate-evidence/*.md .orchestration/dotfiles-T128-gate-evidence-a01/*.md
Checking formatting...
All matched files use Prettier code style!
$ ruff check --config ruff.toml --output-format concise <both files> | sed -E "s/:[0-9]+:[0-9]+:/:/" | sort | uniq -c   # this branch, not a CI gate (CI runs ruff format --check)
   1 [*] 4 fixable with the `--fix` option (3 hidden fixes can be enabled with the `--unsafe-fixes` option).
   1 Found 7 errors.
   1 scripts/require-crit-review.py: FURB167 [*] Use of regular expression alias `re.M`
   1 scripts/require-crit-review.py: FURB167 [*] Use of regular expression alias `re.S`
   1 scripts/require-crit-review.py: I001 [*] Import block is un-sorted or un-formatted
   2 scripts/require-crit-review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   1 tests/unit/test_require_crit_review.py: I001 [*] Import block is un-sorted or un-formatted
   1 tests/unit/test_require_crit_review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
$ (same, on the origin/main copies of both files in a scratch dir)
   1 [*] 4 fixable with the `--fix` option (3 hidden fixes can be enabled with the `--unsafe-fixes` option).
   1 Found 7 errors.
   1 scripts/require-crit-review.py: FURB167 [*] Use of regular expression alias `re.M`
   1 scripts/require-crit-review.py: FURB167 [*] Use of regular expression alias `re.S`
   1 scripts/require-crit-review.py: I001 [*] Import block is un-sorted or un-formatted
   2 scripts/require-crit-review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   1 tests/unit/test_require_crit_review.py: I001 [*] Import block is un-sorted or un-formatted
   1 tests/unit/test_require_crit_review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
```

## 9. Diff size (INV-2: at most 15 files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`)

```
$ git diff --numstat 683384ea...9a860c95 > numstat.txt; cat numstat.txt
94	0	.orchestration/dotfiles-T128-gate-evidence-a01/task.md
3	3	Makefile
5	5	README.md
53	5	scripts/require-crit-review.py
8	0	tests/fixtures/gate-evidence/acceptance-s6-missing.md
10	0	tests/fixtures/gate-evidence/acceptance-s6-present.md
4	0	tests/fixtures/gate-evidence/pr-feedback-right.json
4	0	tests/fixtures/gate-evidence/pr-feedback-wrong.json
174	17	tests/unit/test_require_crit_review.py
$ uv run --no-project python caps.py numstat.txt   # caps.py: count files outside .orchestration/, added lines outside tests/, added lines under tests/
files outside .orchestration: 8
added outside tests/ (and .orchestration): 61
added under tests/: 200
```
