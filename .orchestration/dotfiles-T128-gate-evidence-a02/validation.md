# Validation: dotfiles-T128-gate-evidence-a02

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `regime/gate-evidence` (PR #329), except §10, run in the main checkout. Test runs set `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` (sandbox record). Scratch file names (`numstat.txt`, `caps.py`, `mutate3.sh`, `fail-*.txt`) live in the session's `$TMPDIR`. This branch copy covers the code head `379845f7`; the main-checkout copy adds the final head, CI and the Bot wait.

## 1. Task file and the a01 history copy

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-gate-evidence-a02.md .orchestration/dotfiles-T128-gate-evidence-a02/task.md | cut -c1-64
930f570b9a44114ab68062575b212fdcbd959653cebb1f3f7c710d717f033ddf
930f570b9a44114ab68062575b212fdcbd959653cebb1f3f7c710d717f033ddf
$ git diff --quiet 5971fffe HEAD -- .orchestration/dotfiles-T128-gate-evidence-a01/ && echo "a01 records unchanged since 5971fffe"; shasum -a 256 .orchestration/dotfiles-T128-gate-evidence-a01/task.md | cut -c1-64
a01 records unchanged since 5971fffe
d1b6fcf3f1f7aada49c8a38e79fae57525d135d59d9c44a3ef5ebc87e79a8d26
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

## 3. The module at the code head (79 tests; new: `test_dispositions_*`, `test_s6_*`, `test_base_requires_an_acceptance_record_under_acceptance`, `test_acceptance_record_*`)

```
$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false uv run --no-project python -m unittest tests/unit/test_require_crit_review.py -v 2>&1 | sed -E 's/ \(tests[^)]*\)//' | grep -E ' \.\.\. |^Ran|^OK|^FAILED'   # at 379845f7
test_acceptance_record_is_not_counted_as_a_change ... ok
test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict ... ok
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
Ran 79 tests in 64.369s
OK
```

## 4. Each new check fails a test when broken

```
$ bash mutate3.sh   # runs the 10 new or changed tests on this change; on origin/main's guard (M0) and on a01's head 5971fffe (M1); and on eight one-line mutations of this guard (M2 to M8 as labelled); it restores the guard and checks it with cmp
== control: this change
Ran 10 tests in 17.936s
OK
== M0 origin/main guard
FAIL: test_dispositions_of_2026_10_12_without_evidence_are_refused
FAIL: test_s6_class_at_three_without_a_pasted_search_is_refused
FAIL: test_s6_class_at_three_with_a_pasted_search_is_accepted (form="grep -rl 'classes:.*class-count-scope' .orchestration/learning/mistakes/")
FAIL: test_s6_class_at_three_with_a_pasted_search_is_accepted (form="grep -l 'classes:.*class-count-scope' .orchestration/learning/mistakes/*.md")
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [another class's slug]
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [one command only]
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [grep outside the mistake records]
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [grep given the bare directory]
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [pre-amendment grep -rl]
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [not at the line start]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='', content='')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/validation/test.md', content='')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/other.md', content='')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/alias.md', content='')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/test.md', content='')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/test.md', content='# Acceptance: test (S6 fixture')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/test.md', content='audit-finding: 1 not-applicabl')
FAIL: test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict [no evidence clause]
FAIL: test_acceptance_record_is_not_counted_as_a_change
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='no evidence clause')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='empty evidence command')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='empty reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short failure reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short in-progress reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short cancelled reason')
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [short reason]
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [no evidence clause]
Ran 10 tests in 19.145s
FAILED (failures=27)
== M1 guard at 5971fffe (a01 head, before the round-1 fixes)
FAIL: test_dispositions_with_an_evidence_command_are_accepted
FAIL: test_s6_class_at_three_with_a_pasted_search_is_accepted (form="grep -rl 'classes:.*class-count-scope' .orchestration/learning/mistakes/")
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [grep given the bare directory]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/other.md', content='')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/alias.md', content='')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/test.md', content='audit-finding: 1 not-applicabl')
FAIL: test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict [no evidence clause]
FAIL: test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict [evidence clause]
FAIL: test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict [a fixed finding in prose]
FAIL: test_acceptance_record_is_not_counted_as_a_change
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [no dispositions]
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [fixed commit]
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [short reason]
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [no evidence clause]
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [one missing]
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [unnumbered repeat]
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [same finding twice]
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [out of range]
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [accepted]
Ran 10 tests in 17.273s
FAILED (failures=19)
== M2 evidence clause optional
FAIL: test_dispositions_of_2026_10_12_without_evidence_are_refused
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/test.md', content='audit-finding: 1 not-applicabl')
FAIL: test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict [no evidence clause]
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='no evidence clause')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='empty evidence command')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='empty reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short failure reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short in-progress reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (case='short cancelled reason')
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [short reason]
FAIL: test_incorrect_audit_needs_not_applicable_dispositions [no evidence clause]
Ran 10 tests in 18.082s
FAILED (failures=11)
== M3 slug matched as a substring
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [another class's slug]
Ran 10 tests in 17.912s
FAILED (failures=1)
== M4 no grep form required
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [grep outside the mistake records]
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [grep given the bare directory]
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [pre-amendment grep -rl]
Ran 10 tests in 17.013s
FAILED (failures=3)
== M5 grep -l accepted on the bare directory
FAIL: test_s6_search_line_names_the_class_token_and_both_commands [grep given the bare directory]
Ran 10 tests in 18.476s
FAILED (failures=1)
== M6 record not bound to the task
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/other.md', content='')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/alias.md', content='')
Ran 10 tests in 18.253s
FAILED (failures=2)
== M7 record not-applicable lines unchecked
FAIL: test_base_requires_an_acceptance_record_under_acceptance (value='.orchestration/acceptance/test.md', content='audit-finding: 1 not-applicabl')
FAIL: test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict [no evidence clause]
Ran 10 tests in 18.918s
FAILED (failures=2)
== M8 record counted as a change
FAIL: test_acceptance_record_is_not_counted_as_a_change
Ran 10 tests in 17.682s
FAILED (failures=1)
guard restored
```

## 5. Fixture provenance, the right fixture's evidence commands, the two search forms, thread 4248232955's evidence, fixture size

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
$ grep -n 'ACCEPTANCE_EVIDENCE' .orchestration/tasks/dotfiles-T128-playbook-rules-a02.md   # main checkout
79:6. Orchestrator Playbook step 10.4 (line 170): the gate command gains `ACCEPTANCE_EVIDENCE=<acceptance record>` beside `PR_FEEDBACK_EVIDENCE` (required in PR mode once `dotfiles-T128-gate-evidence-a01` lands; the record whose ledger and `search:` line the gate reads); any existing token test that asserts that sentence is updated to the new text in the same commit.
$ grep -rl 'classes:.*class-count-scope' .orchestration/learning/mistakes/; echo rc=$?   # main checkout
.orchestration/learning/mistakes/M-20261012-3.md
rc=0
$ grep -l 'classes:.*class-count-scope' .orchestration/learning/mistakes/*.md; echo rc=$?
.orchestration/learning/mistakes/M-20261012-3.md
rc=0
$ grep -l 'classes:.*class-count-scope' .orchestration/learning/mistakes/; echo rc=$?
grep: .orchestration/learning/mistakes/: Is a directory
rc=2
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
379845f7
?? .orchestration/reports/probe.md
Review not required: no meaningful review trigger found.
rc=0
$ git -C <scratch> rev-parse --short HEAD; git -C <scratch> status --short; make -C <scratch> require-crit-review; echo rc=$?
7cbe5405
?? .orchestration/reports/probe.md
Review not required: no meaningful review trigger found.
rc=0
```

## 7. Full unit suite at the code head against `origin/main`

```
$ git rev-parse --short HEAD && UV_OFFLINE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false uv run --no-project --with pyyaml python -m unittest discover -s tests/unit > unit-all-a02.txt 2>&1; echo "rc=$?"; tail -3 unit-all-a02.txt; grep -E '^(FAIL|ERROR): .*\(' unit-all-a02.txt | grep -oE '\(([a-z_]+\.)*test_[a-z_0-9]+\.[A-Za-z]+\.[a-z_0-9]+\)' | tr -d '()' | sed 's/^tests\.unit\.//' | sort > fail-a02.txt; wc -l < fail-a02.txt; cmp fail-base.txt fail-a02.txt && echo "identical to the origin/main failing set"
379845f7
rc=1
Ran 1004 tests in 530.665s

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
$ prettier --check README.md tests/fixtures/gate-evidence/*.md .orchestration/dotfiles-T128-gate-evidence-a02/*.md
Checking formatting...
All matched files use Prettier code style!
$ ruff check --config ruff.toml --output-format concise scripts/require-crit-review.py tests/unit/test_require_crit_review.py | sed -E "s/:[0-9]+:[0-9]+:/:/" | sort | uniq -c   # not a CI gate (CI runs ruff format --check)
   1 [*] 4 fixable with the `--fix` option (3 hidden fixes can be enabled with the `--unsafe-fixes` option).
   1 Found 7 errors.
   1 scripts/require-crit-review.py: FURB167 [*] Use of regular expression alias `re.M`
   1 scripts/require-crit-review.py: FURB167 [*] Use of regular expression alias `re.S`
   1 scripts/require-crit-review.py: I001 [*] Import block is un-sorted or un-formatted
   2 scripts/require-crit-review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   1 tests/unit/test_require_crit_review.py: I001 [*] Import block is un-sorted or un-formatted
   1 tests/unit/test_require_crit_review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
$ (the same ruff check on the origin/main copies of both files, in a scratch directory)
   1 [*] 4 fixable with the `--fix` option (3 hidden fixes can be enabled with the `--unsafe-fixes` option).
   1 Found 7 errors.
   1 scripts/require-crit-review.py: FURB167 [*] Use of regular expression alias `re.M`
   1 scripts/require-crit-review.py: FURB167 [*] Use of regular expression alias `re.S`
   1 scripts/require-crit-review.py: I001 [*] Import block is un-sorted or un-formatted
   2 scripts/require-crit-review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
   1 tests/unit/test_require_crit_review.py: I001 [*] Import block is un-sorted or un-formatted
   1 tests/unit/test_require_crit_review.py: UP022 Prefer `capture_output` over sending `stdout` and `stderr` to `PIPE`
```

## 9. Diff size (INV-2: at most 15 files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`) and the moved base

```
$ git diff --numstat origin/main...379845f7 > numstat.txt; cat numstat.txt
3	0	.orchestration/dotfiles-T128-gate-evidence-a01/autoskill.md
7	0	.orchestration/dotfiles-T128-gate-evidence-a01/learning.md
44	0	.orchestration/dotfiles-T128-gate-evidence-a01/report.md
15	0	.orchestration/dotfiles-T128-gate-evidence-a01/sandbox.md
94	0	.orchestration/dotfiles-T128-gate-evidence-a01/task.md
287	0	.orchestration/dotfiles-T128-gate-evidence-a01/validation.md
98	0	.orchestration/dotfiles-T128-gate-evidence-a02/task.md
3	3	Makefile
5	5	README.md
93	17	scripts/require-crit-review.py
8	0	tests/fixtures/gate-evidence/acceptance-s6-missing.md
10	0	tests/fixtures/gate-evidence/acceptance-s6-present.md
4	0	tests/fixtures/gate-evidence/pr-feedback-right.json
4	0	tests/fixtures/gate-evidence/pr-feedback-wrong.json
230	17	tests/unit/test_require_crit_review.py
$ uv run --no-project python caps.py numstat.txt   # caps.py: count files outside .orchestration/, added lines outside tests/, added lines under tests/
files outside .orchestration: 8
added outside tests/ (and .orchestration): 101
added under tests/: 256
$ git log --oneline 683384ea..origin/main; git diff --stat 683384ea origin/main -- README.md Makefile scripts/require-crit-review.py tests/unit/test_require_crit_review.py tests/fixtures/gate-evidence; git merge-tree --write-tree origin/main 379845f7 >/dev/null && echo "merges cleanly"
7cbe5405 chore(orchestration): boundary commit 2026-10-12 (7): design v21 (gate-evidence-a02 map entry, round 24), T702 reset to a02 (INV-6), M-17/C-19, T714 draft fix (#331)
4cf1d4e2 chore(orchestration): boundary commit 2026-10-12 (6): T703 reset to a02 (INV-6), classes field on the mistake records, M-14 to M-16, C-16 to C-18, amendment 1 of T702, drafts for T714/T716/T718, operator patches (#330)
merges cleanly
```

## 10. CompactionDB (main checkout, through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T128-gate-evidence-a01 (PR 329): scripts/require-crit-review.py accepts a not-applicable disposition only as not-applicable:<reason>; evidence=<command> (pr-feedback items and AUDIT_DISPOSITIONS audit-finding lines), and requires ACCEPTANCE_EVIDENCE=<acceptance record> under .orchestration/acceptance/ whenever BASE is set; a ledger class at three or more rows needs a search: line naming the class token, grep -l 'classes: over .orchestration/learning/mistakes/ and contextdb_cli.py memory search, else 'S6: class <slug> at <n> without a pasted search'." 2>&1 | tail -3   # under a01, 12:4xZ
7f2f0c0b-6d20-42af-97ac-c5cfcfe62ea7
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content "Claude worker sandbox: the global commit.gpgsign reads ~/.ssh/id_ed25519.pub, which the sandbox denies, so every git commit inside unit-test fixture repos fails (tests/unit/test_require_crit_review.py: 73 failures on unmodified origin/main); run such modules with GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false and establish the base result before attributing a failure to the change." 2>&1 | tail -3   # same call
f939c61c-9822-407c-9928-d67bec0531c6
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T128-gate-evidence-a02 (PR 329, 379845f7): ACCEPTANCE_EVIDENCE must be .orchestration/acceptance/<task>.md for the task named by the <task>-pr-feedback.json file (name and resolved name); every audit-finding line of that record carrying not-applicable needs '; evidence=<command>' whatever the audit verdict; the record is excluded from diff sizing; the S6 search line takes grep -rl 'classes:...' .orchestration/learning/mistakes/ or grep -l 'classes:...' .orchestration/learning/mistakes/*.md (grep -l on the bare directory exits 2, Is a directory) plus contextdb_cli.py memory search." 2>&1 | tail -2   # under a02
43f0ce26-7095-45a2-a86c-d8bfbe197b1d
```
