---
task_id: dotfiles-T133-verdict-audit-pool-a01
seat: claude-standard-dot-a008
head: f6adaea8
---

# Validation: dotfiles-T133-verdict-audit-pool-a01

Every command ran from the worktree `.claude/worktrees/worker-f` on the branch `tools/verdict-audit-pool-a01` at `f6adaea8`, inside the sandbox, through a generator that prints each command, its verbatim output and its exit status (a block's status is its last command's), except §12, run outside the sandbox for gh and pasted from its saved output, and §7a, assembled from §7's output and the origin/main run of the same modules. `MAIN` names the main checkout and `T` the task id. The scratch worktrees of §5 to §5c live under `$TMPDIR` and are removed after their block with `git worktree remove --force`. §7 and §9 fail on files and modules this PR does not touch, the same on origin/main (§7a, §9).

## 1. Task file (Amendment 1, sha256 2919563b…) and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
2919563b9f8d47825cf13e251055c7955f5fc975b28896058acd5568ba2d6f59  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a01.md
2919563b9f8d47825cf13e251055c7955f5fc975b28896058acd5568ba2d6f59  .orchestration/dotfiles-T133-verdict-audit-pool-a01/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T133-verdict-audit-pool-a01.md: OK
[exit 0]
```
## 2. Premises 1 to 4, replayed on origin/main
```console
$ B=$(git rev-parse origin/main); echo "origin/main=$B"; git show "$B:scripts/orchestrator/orch-audit.sh" | /usr/bin/grep -c "usage: orch-audit.sh <task> <pr-worktree> <pr>"; git show "$B:scripts/pr-feedback.py" > "$TMPDIR/pf.py"; uv run --no-project python "$TMPDIR/pf.py" --help | /usr/bin/grep -c -- "--json JSON"; git show "$B:scripts/regime-counters.sh" | /usr/bin/grep -c -- "--history-only) history_only=true"; git ls-tree -r --name-only "$B" -- .schemas scripts/orchestrator/verdict.sh scripts/orchestrator/audit-pool.sh | wc -l
origin/main=99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
1
2
1
       0
[exit 0]
```
## 3. Branch, base and commits
```console
$ git branch --show-current; git rev-parse HEAD origin/main; git log --oneline origin/main..HEAD
tools/verdict-audit-pool-a01
f6adaea80dea9c170caecac4a264303ee3d27490
99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
f6adaea8 fix(orchestrator): --apply needs scripts and task files equal to origin/main, a record ledger is required (T133 verdict-audit-pool a01 worker re-review)
be70b5c8 test(orchestrator): a failed audit's queue log holds no transcript text (T133 verdict-audit-pool a01 worker review)
f2d1ffd2 fix(orchestrator): every verdict condition is ok only on a positive check of a read input (T133 verdict-audit-pool a01 worker review)
2ff92578 fix(orchestrator): verdict.sh holds on a missing record or an unfetched head instead of failing open (T133 verdict-audit-pool a01)
fada8070 feat(orchestrator): verdict.sh, the nine acceptance conditions as one accept, revise or hold verdict (T133 verdict-audit-pool a01)
beb0b0c7 feat(orchestrator): audit and verdict schemas, the class vocabulary, orch-audit json mode and the audit pool (T133 verdict-audit-pool a01)
[exit 0]
```
## 4. The ledger classes of the records against .schemas/classes.yaml (the helper below, then its run)
```console
$ cat "$TMPDIR/seed133.sh"; echo "--- run"; bash "$TMPDIR/seed133.sh"
#!/bin/bash
# The ledger classes of the records (the task's for-loop), in the main checkout and over the tracked records, against .schemas/classes.yaml.
MAIN=~/Workspace/dotfiles
seed() {
    for f in "$@"; do
        uv run --no-project python -I -c 'import json,sys; t=open(sys.argv[1]).read().split("\n---\n"); b=json.loads(t[0].lstrip("-\n")) if t[0].strip("-\n").startswith("{") else {}; print("\n".join(r["class"] for r in b.get("ledger",[])))' "$f"
    done | sort -u | /usr/bin/grep -v '^$'
}
seed "$MAIN"/.orchestration/acceptance/*.md > "$TMPDIR/seed-main.txt"
seed $(git ls-files '.orchestration/acceptance/*.md') > "$TMPDIR/seed-tracked.txt"
uv run --no-project --with pyyaml python -I -c 'import yaml; print("\n".join(sorted(yaml.safe_load(open(".schemas/classes.yaml")))))' > "$TMPDIR/keys.txt"
echo "classes in the main checkout's records: $(wc -l < "$TMPDIR/seed-main.txt"); in the tracked records: $(wc -l < "$TMPDIR/seed-tracked.txt"); keys of classes.yaml: $(wc -l < "$TMPDIR/keys.txt")"
echo "--- main-checkout classes missing from classes.yaml:"; comm -23 "$TMPDIR/seed-main.txt" "$TMPDIR/keys.txt"
echo "--- tracked-record classes missing from classes.yaml:"; comm -23 "$TMPDIR/seed-tracked.txt" "$TMPDIR/keys.txt"
echo "--- classes.yaml keys beyond the main-checkout seed (the named extras):"; comm -13 "$TMPDIR/seed-main.txt" "$TMPDIR/keys.txt"
echo "--- the seed list:"; tr '\n' ' ' < "$TMPDIR/seed-main.txt"; echo
--- run
classes in the main checkout's records:      134; in the tracked records:      120; keys of classes.yaml:      137
--- main-checkout classes missing from classes.yaml:
--- tracked-record classes missing from classes.yaml:
--- classes.yaml keys beyond the main-checkout seed (the named extras):
ps-output-parsing
records-form
string-form-comparison
--- the seed list:
acceptance-dispositions acceptance-order acceptance-record-binding action-cdp-omission advisory-deferral advisory-deferral-objection advisory-owner-misassignment advisory-p2 advisory-policy-reading advisory-read-as-deferral argv-diagnostic-disclosure argv-text-mismatch bot-rounds-count boundary-cadence-vs-skill boundary-checker-overclaim c50-clause-skipped closed-row-coverage collision-key-order consumer-half contract-type-mismatch counter-evidence counters-not-pasted counters-unknown-components cross-script-grammar deleted-path-handling dispatch-evidence disposition-backtick-truncation disposition-key disposition-range docs-role-efforts duplicate-managed-flags env-s-quoting environment-inheritance equals-form-flag evidence-checkpoint evidence-claim evidence-command-null-url evidence-command-unlanded-owner evidence-diagnosis evidence-layout evidence-not-committed evidence-shell-interpolation evidence-stale evidence-url-interpolation evidence-validation-stale fail-open-on-error filename-suffix-parse fixture-missing graphql-id-interpolation hand-parser input-validation install-receipt-artifact interpreter-discovery inv3-overlay-reading inv6-count inv6-counts-amendments inv6-counts-reseat inv6-waiver-mechanism inv6-waiver-missing inv7-review-effort invariants-key-absent-short-form json-interpolation ledger-completeness ledger-fidelity ledger-id-type live-verification match-any-part mise-config-steer missing-counter-evidence missing-owner-task nested-command-exclusion nul-delimited-paths owner-not-on-main owner-row-location owner-scope-unexecutable owner-section-location path-coverage path-form-normalisation path-shadowed-binary path-shim-discovery path-traversal pathspec-globbing precheck-trusts-pr-controlled-input predicate-shape-overmatch procedure-migration process-visibility profile-name-grammar record-copy-drops-rows record-counting record-decision-missing replan-word-boundary reply-template-unparseable report-base-sha resolve-response-unchecked restore-trap result-selection reuse-keyed-by-sha7 review-binary-shim review-body-findings revise-check-not-discriminating revise-line-contract routing-boundary s6-search-missing sandbox-count-understated sandbox-record-incomplete scope search-command-scan search-procedure sed-path-interpolation stale-audit-dispositions stale-dir-order stale-evidence stale-no-identity-rows stale-path-cleanup-failure stale-record-block stale-review-file-on-error stale-security-docs stale-threat-row synthetic-id-namespace sys-path-shadowing tab-url-not-matched-to-event target-id-validation task-arg-traversal task-scope-amended test-order-unproven threat-row-missing threat-rows-per-path tool-environment trap-restores-on-refusal trust-boundary-dispositions trusted-checkout unbound-evidence unsupported-claim worker-sandbox-discipline 
[exit 0]
```
## 5. RED: test_audit_pool.py against origin/main's orch-audit.sh (no --head, --json or --validate), in a scratch worktree at HEAD
```console
$ git -C "$R" status --short; uv run --no-project python -I "$R/tests/unit/test_audit_pool.py" -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"
 M scripts/orchestrator/orch-audit.sh
test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class (__main__.AuditPoolTest.test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class) ... 
  test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class (__main__.AuditPoolTest.test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class) (cls='records-form') ... FAIL
  test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class (__main__.AuditPoolTest.test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class) (cls='no-such-class') ... FAIL
test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius (__main__.AuditPoolTest.test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius) ... ok
test_orch_audit_json_mode_extracts_the_final_json_block_and_keeps_every_refusal (__main__.AuditPoolTest.test_orch_audit_json_mode_extracts_the_final_json_block_and_keeps_every_refusal) ... FAIL
test_pool_retries_a_429_three_times_then_blocks (__main__.AuditPoolTest.test_pool_retries_a_429_three_times_then_blocks) ... 
  test_pool_retries_a_429_three_times_then_blocks (__main__.AuditPoolTest.test_pool_retries_a_429_three_times_then_blocks) (failures='2') ... FAIL
  test_pool_retries_a_429_three_times_then_blocks (__main__.AuditPoolTest.test_pool_retries_a_429_three_times_then_blocks) (failures='4') ... ERROR
test_pool_runs_at_most_max_audits_and_the_third_request_waits (__main__.AuditPoolTest.test_pool_runs_at_most_max_audits_and_the_third_request_waits) ... FAIL
test_pool_saves_only_schema_valid_audit_json_and_blocks_a_rejected_request (__main__.AuditPoolTest.test_pool_saves_only_schema_valid_audit_json_and_blocks_a_rejected_request) ... FAIL
test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree (__main__.AuditPoolTest.test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree) ... 
  test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree (__main__.AuditPoolTest.test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree) (rows=1) ... ERROR
  test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree (__main__.AuditPoolTest.test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree) (rows=2) ... ERROR
Ran 7 tests in 5.679s
FAILED (failures=6, errors=3)
[exit 0]
```
## 5a. RED: test_verdict.py at HEAD against fada8070's verdict.sh (before the missing-record and unfetched-head fixes), in a scratch worktree
```console
$ git -C "$Q" status --short; uv run --no-project python -I "$Q/tests/unit/test_verdict.py" -v 2>&1 | /usr/bin/grep -E "\.\.\. |^FAIL:|AssertionError|^Ran|^(OK|FAILED)"
 M scripts/orchestrator/verdict.sh
test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) ... 
  test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=2, condition=2) ... FAIL
  test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=5, condition=4) ... FAIL
  test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=8, condition=5) ... FAIL
  test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=9, condition=6) ... FAIL
  test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=13, condition=9) ... FAIL
test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto (__main__.VerdictTest.test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto) ... FAIL
test_verdict_condition_1_is_a_warning_under_precheck_required_0 (__main__.VerdictTest.test_verdict_condition_1_is_a_warning_under_precheck_required_0) ... ok
test_verdict_holds_on_a_missing_or_schema_failing_input (__main__.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input) ... 
  test_verdict_holds_on_a_missing_or_schema_failing_input (__main__.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input) (condition=2) ... FAIL
  test_verdict_holds_on_a_missing_or_schema_failing_input (__main__.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input) (condition=3) ... FAIL
test_verdict_holds_on_a_missing_or_schema_failing_input (__main__.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input) ... FAIL
test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold (__main__.VerdictTest.test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold) ... ok
test_verdict_shadow_appends_the_machine_column_only (__main__.VerdictTest.test_verdict_shadow_appends_the_machine_column_only) ... ok
FAIL: test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=2, condition=2)
AssertionError: 10 != 0 : verdict: accept .orchestration/validation/t1-a01-verdict-811ab97.json
FAIL: test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=5, condition=4)
AssertionError: 10 != 0 : verdict: accept .orchestration/validation/t1-a01-verdict-811ab97.json
FAIL: test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=8, condition=5)
AssertionError: 10 != 0 : verdict: accept .orchestration/validation/t1-a01-verdict-811ab97.json
FAIL: test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=9, condition=6)
AssertionError: 20 != 0 : verdict: accept .orchestration/validation/t1-a01-verdict-811ab97.json
FAIL: test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=13, condition=9)
AssertionError: 10 != 0 : verdict: accept .orchestration/validation/t1-a01-verdict-811ab97.json
FAIL: test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto (__main__.VerdictTest.test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto)
AssertionError: 'four agreeing' not found in ''
FAIL: test_verdict_holds_on_a_missing_or_schema_failing_input (__main__.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input) (condition=2)
AssertionError: 20 != 0 : verdict: accept .orchestration/validation/t1-a01-verdict-3c866e7.json
FAIL: test_verdict_holds_on_a_missing_or_schema_failing_input (__main__.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input) (condition=3)
AssertionError: 20 != 10 : verdict: revise .orchestration/validation/t1-a01-verdict-3c866e7.json
FAIL: test_verdict_holds_on_a_missing_or_schema_failing_input (__main__.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input)
AssertionError: 20 != 0 : verdict: accept .orchestration/validation/t1-a01-verdict-3c866e7.json
Ran 6 tests in 39.053s
FAILED (failures=9)
[exit 0]
```
## 5b. RED: both test files at HEAD against 2ff92578's three scripts (before the worker review's re-plan), in a scratch worktree
```console
$ git -C "$P" status --short; uv run --no-project python -I -m unittest discover -s "$P/tests/unit" -p "test_verdict.py" -v 2>&1 | /usr/bin/grep -E "^FAIL:|^Ran|^(OK|FAILED)"; uv run --no-project python -I "$P/tests/unit/test_audit_pool.py" -v 2>&1 | /usr/bin/grep -E "^FAIL:|^Ran|^(OK|FAILED)"
 M scripts/orchestrator/audit-pool.sh
 M scripts/orchestrator/orch-audit.sh
 M scripts/orchestrator/verdict.sh
FAIL: test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (test_verdict.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=2, condition=2)
FAIL: test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (test_verdict.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=5, condition=4)
FAIL: test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (test_verdict.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=8, condition=5)
FAIL: test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (test_verdict.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=9, condition=6)
FAIL: test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (test_verdict.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=13, condition=9)
FAIL: test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto (test_verdict.VerdictTest.test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto)
FAIL: test_verdict_holds_on_a_missing_or_schema_failing_input (test_verdict.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input) (condition=2)
FAIL: test_verdict_holds_on_a_missing_or_schema_failing_input (test_verdict.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input) (condition=3)
FAIL: test_verdict_holds_on_a_missing_or_schema_failing_input (test_verdict.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input)
Ran 6 tests in 35.753s
FAILED (failures=9)
FAIL: test_pool_retries_a_429_three_times_then_blocks (__main__.AuditPoolTest.test_pool_retries_a_429_three_times_then_blocks) (failures='4')
Ran 7 tests in 17.341s
FAILED (failures=1)
[exit 0]
```
## 5c. RED: test_verdict.py at HEAD against f2d1ffd2's verdict.sh (before the worker re-review's fixes), in a scratch worktree
```console
$ git -C "$O" status --short; uv run --no-project python -I "$O/tests/unit/test_verdict.py" -v 2>&1 | /usr/bin/grep -E "^FAIL:|^Ran|^(OK|FAILED)"
 M scripts/orchestrator/verdict.sh
FAIL: test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (__main__.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) (case=2, condition=2)
FAIL: test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto (__main__.VerdictTest.test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto)
FAIL: test_verdict_holds_on_a_missing_or_schema_failing_input (__main__.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input)
Ran 6 tests in 42.690s
FAILED (failures=3)
[exit 0]
```
## 6. GREEN: the Check's unit-test command on HEAD
```console
$ uv run python -m unittest tests.unit.test_verdict tests.unit.test_audit_pool -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"
test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (tests.unit.test_verdict.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) ... ok
test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto (tests.unit.test_verdict.VerdictTest.test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto) ... ok
test_verdict_condition_1_is_a_warning_under_precheck_required_0 (tests.unit.test_verdict.VerdictTest.test_verdict_condition_1_is_a_warning_under_precheck_required_0) ... ok
test_verdict_holds_on_a_missing_or_schema_failing_input (tests.unit.test_verdict.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input) ... ok
test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold (tests.unit.test_verdict.VerdictTest.test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold) ... ok
test_verdict_shadow_appends_the_machine_column_only (tests.unit.test_verdict.VerdictTest.test_verdict_shadow_appends_the_machine_column_only) ... ok
test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class (tests.unit.test_audit_pool.AuditPoolTest.test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class) ... ok
test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius (tests.unit.test_audit_pool.AuditPoolTest.test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius) ... ok
test_orch_audit_json_mode_extracts_the_final_json_block_and_keeps_every_refusal (tests.unit.test_audit_pool.AuditPoolTest.test_orch_audit_json_mode_extracts_the_final_json_block_and_keeps_every_refusal) ... ok
test_pool_retries_a_429_three_times_then_blocks (tests.unit.test_audit_pool.AuditPoolTest.test_pool_retries_a_429_three_times_then_blocks) ... ok
test_pool_runs_at_most_max_audits_and_the_third_request_waits (tests.unit.test_audit_pool.AuditPoolTest.test_pool_runs_at_most_max_audits_and_the_third_request_waits) ... ok
test_pool_saves_only_schema_valid_audit_json_and_blocks_a_rejected_request (tests.unit.test_audit_pool.AuditPoolTest.test_pool_saves_only_schema_valid_audit_json_and_blocks_a_rejected_request) ... ok
test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree (tests.unit.test_audit_pool.AuditPoolTest.test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree) ... ok
Ran 13 tests in 58.074s
OK
[exit 0]
```
## 7. make unit-test on HEAD (its last lines, and every FAIL or ERROR test line)
```console
$ make unit-test > "$TMPDIR/unit-final.txt" 2>&1; rc=$?; tail -n 4 "$TMPDIR/unit-final.txt"; /usr/bin/grep -E "^(FAIL|ERROR): " "$TMPDIR/unit-final.txt"; exit $rc
Ran 1189 tests in 578.657s

FAILED (failures=189, errors=107, skipped=2)
make: *** [unit-test] Error 1
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ERROR: test_a_failing_chmod_fails_the_step (test_gh_auth.GhAuthTest.test_a_failing_chmod_fails_the_step)
ERROR: test_a_login_that_does_not_complete_fails (test_gh_auth.GhAuthTest.test_a_login_that_does_not_complete_fails)
ERROR: test_a_working_keyring_login_is_moved_to_the_file (test_gh_auth.GhAuthTest.test_a_working_keyring_login_is_moved_to_the_file)
ERROR: test_on_a_terminal_it_logs_in_to_gh_file_at_0600 (test_gh_auth.GhAuthTest.test_on_a_terminal_it_logs_in_to_gh_file_at_0600)
ERROR: test_setup_finds_a_mise_installed_gh_on_a_fresh_path (test_gh_auth.GhAuthTest.test_setup_finds_a_mise_installed_gh_on_a_fresh_path)
ERROR: test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits (test_herdr_agents.HerdrAgentsTest.test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits)
ERROR: test_add_worker_defaults_to_the_manifest_worktree_and_refuses_a_non_worktree_path (test_herdr_agents.HerdrAgentsTest.test_add_worker_defaults_to_the_manifest_worktree_and_refuses_a_non_worktree_path)
ERROR: test_add_worker_derives_the_default_herdr_socket_for_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_derives_the_default_herdr_socket_for_spawn)
ERROR: test_add_worker_emits_no_override_for_an_unparseable_codex_config (test_herdr_agents.HerdrAgentsTest.test_add_worker_emits_no_override_for_an_unparseable_codex_config)
ERROR: test_add_worker_exits_zero_when_a_timed_out_spawn_still_links (test_herdr_agents.HerdrAgentsTest.test_add_worker_exits_zero_when_a_timed_out_spawn_still_links)
ERROR: test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array (test_herdr_agents.HerdrAgentsTest.test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array)
ERROR: test_add_worker_linkage_failure_prints_the_invocation_and_the_query (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_failure_prints_the_invocation_and_the_query)
ERROR: test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver)
ERROR: test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping)
ERROR: test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace)
ERROR: test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn)
ERROR: test_add_worker_linkage_ignores_a_placement_record_from_another_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_from_another_workspace)
ERROR: test_add_worker_linkage_ignores_a_pong_older_than_this_ping (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_pong_older_than_this_ping)
ERROR: test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal)
ERROR: test_add_worker_linkage_refuses_a_placement_conflict (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_a_placement_conflict)
ERROR: test_add_worker_linkage_refuses_several_orchestrator_identities (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_several_orchestrator_identities)
ERROR: test_add_worker_linkage_resolves_an_id_keyed_placement_record (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_resolves_an_id_keyed_placement_record)
ERROR: test_add_worker_linkage_survives_a_non_numeric_pong_wait (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_survives_a_non_numeric_pong_wait)
ERROR: test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh (test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh)
ERROR: test_add_worker_names_the_seat_from_a_codex_orchestrator_identity (test_herdr_agents.HerdrAgentsTest.test_add_worker_names_the_seat_from_a_codex_orchestrator_identity)
ERROR: test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options (test_herdr_agents.HerdrAgentsTest.test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options)
ERROR: test_add_worker_refuses_an_undefined_profile_before_any_change (test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_an_undefined_profile_before_any_change)
ERROR: test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found (test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found)
ERROR: test_add_worker_rejects_a_worktree_outside_claude_worktrees (test_herdr_agents.HerdrAgentsTest.test_add_worker_rejects_a_worktree_outside_claude_worktrees)
ERROR: test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog)
ERROR: test_add_worker_reports_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_spawn)
ERROR: test_add_worker_reports_linkage_ok_after_a_ready_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_ok_after_a_ready_spawn)
ERROR: test_add_worker_reports_linkage_unreached_after_a_failed_spawn (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_unreached_after_a_failed_spawn)
ERROR: test_add_worker_reports_shallow_metadata_as_not_granted (test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_shallow_metadata_as_not_granted)
ERROR: test_add_worker_reuses_a_seat_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seat_tab_in_the_pair_workspace)
ERROR: test_add_worker_reuses_a_seated_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seated_workspace)
ERROR: test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace)
ERROR: test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args (test_herdr_agents.HerdrAgentsTest.test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args)
ERROR: test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog (test_herdr_agents.HerdrAgentsTest.test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog)
ERROR: test_add_worker_without_a_worktree_refuses_an_ambiguous_orchestrator_identity (test_herdr_agents.HerdrAgentsTest.test_add_worker_without_a_worktree_refuses_an_ambiguous_orchestrator_identity)
ERROR: test_added_worker_boot_keeps_the_inherited_github_environment (test_herdr_agents.HerdrAgentsTest.test_added_worker_boot_keeps_the_inherited_github_environment)
ERROR: test_attach_from_the_worker_worktree_exits_quietly (test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_worktree_exits_quietly)
ERROR: test_attach_in_a_linked_worker_worktree_exits_quietly (test_herdr_agents.HerdrAgentsTest.test_attach_in_a_linked_worker_worktree_exits_quietly)
ERROR: test_attach_names_stale_seats (test_herdr_agents.HerdrAgentsTest.test_attach_names_stale_seats)
ERROR: test_attach_without_herdr_environment_names_the_seated_worker (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_names_the_seated_worker)
ERROR: test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree (test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree)
ERROR: test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff (test_herdr_agents.HerdrAgentsTest.test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff)
ERROR: test_audit_task_names_a_txt_artifact_when_no_md_one_exists (test_herdr_agents.HerdrAgentsTest.test_audit_task_names_a_txt_artifact_when_no_md_one_exists)
ERROR: test_audit_task_names_only_the_task_file_when_no_artifact_exists (test_herdr_agents.HerdrAgentsTest.test_audit_task_names_only_the_task_file_when_no_artifact_exists)
ERROR: test_audit_task_normalises_home_paths_with_the_repository_masker (test_herdr_agents.HerdrAgentsTest.test_audit_task_normalises_home_paths_with_the_repository_masker)
ERROR: test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work (test_herdr_agents.HerdrAgentsTest.test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work)
ERROR: test_bootstrap_adds_claude_worker_merge_denials (test_herdr_agents.HerdrAgentsTest.test_bootstrap_adds_claude_worker_merge_denials)
ERROR: test_codex_orchestrator_kind_leaves_a_worker_worktree_attach_quiet (test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_leaves_a_worker_worktree_attach_quiet)
ERROR: test_codex_orchestrator_kind_refuses_attach_in_another_linked_worktree (test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_refuses_attach_in_another_linked_worktree)
ERROR: test_directive_looks_up_a_codex_orchestrator_identity (test_herdr_agents.HerdrAgentsTest.test_directive_looks_up_a_codex_orchestrator_identity)
ERROR: test_directive_prints_the_regime_line_without_herdr (test_herdr_agents.HerdrAgentsTest.test_directive_prints_the_regime_line_without_herdr)
ERROR: test_regime_boundary_check_accepts_a_clean_canonical_clone (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_accepts_a_clean_canonical_clone)
ERROR: test_regime_boundary_check_accepts_an_empty_manifest_worker_worktree (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_accepts_an_empty_manifest_worker_worktree)
ERROR: test_regime_boundary_check_counts_names_across_runtime_types_at_the_main_seat (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_counts_names_across_runtime_types_at_the_main_seat)
ERROR: test_regime_boundary_check_finds_worker_workspaces_from_a_worktree (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_finds_worker_workspaces_from_a_worktree)
ERROR: test_regime_boundary_check_flags_a_seated_main_checkout_off_main (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_a_seated_main_checkout_off_main)
ERROR: test_regime_boundary_check_flags_empty_seats_only (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_empty_seats_only)
ERROR: test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout)
ERROR: test_regime_boundary_check_leaves_an_unseated_detached_checkout_alone (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_leaves_an_unseated_detached_checkout_alone)
ERROR: test_regime_boundary_check_reports_a_canonical_clone_that_differs_from_origin_main (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_canonical_clone_that_differs_from_origin_main)
ERROR: test_regime_boundary_check_reports_a_staged_only_change_in_the_canonical_clone (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_staged_only_change_in_the_canonical_clone)
ERROR: test_regime_boundary_check_reports_a_stale_canonical_head_whose_dirty_bytes_match_origin_main (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_stale_canonical_head_whose_dirty_bytes_match_origin_main)
ERROR: test_regime_boundary_check_reports_a_stash_in_the_canonical_clone (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_stash_in_the_canonical_clone)
ERROR: test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace)
ERROR: test_regime_boundary_check_scans_every_worktree_for_untracked_evidence (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_scans_every_worktree_for_untracked_evidence)
ERROR: test_regime_boundary_check_skips_a_canonical_clone_that_is_the_working_clone (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_skips_a_canonical_clone_that_is_the_working_clone)
ERROR: test_regime_boundary_check_skips_the_canonical_clone_without_chezmoi (test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_skips_the_canonical_clone_without_chezmoi)
ERROR: test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record (test_herdr_agents.HerdrAgentsTest.test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record)
ERROR: test_remove_worker_closes_only_its_tab_in_the_pair_workspace (test_herdr_agents.HerdrAgentsTest.test_remove_worker_closes_only_its_tab_in_the_pair_workspace)
ERROR: test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes (test_herdr_agents.HerdrAgentsTest.test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes)
ERROR: test_remove_worker_force_retries_a_failed_graceful_despawn (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_retries_a_failed_graceful_despawn)
ERROR: test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds (test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds)
ERROR: test_remove_worker_forces_despawn_when_graceful_reports_needs_force (test_herdr_agents.HerdrAgentsTest.test_remove_worker_forces_despawn_when_graceful_reports_needs_force)
ERROR: test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent (test_herdr_agents.HerdrAgentsTest.test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent)
ERROR: test_remove_worker_refuses_a_dirty_worktree_without_force (test_herdr_agents.HerdrAgentsTest.test_remove_worker_refuses_a_dirty_worktree_without_force)
ERROR: test_remove_worker_stale_keeps_the_record_when_cleanup_fails (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stale_keeps_the_record_when_cleanup_fails)
ERROR: test_remove_worker_stale_prepares_the_archive_before_cleanup_and_refuses_without_identity_rows (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stale_prepares_the_archive_before_cleanup_and_refuses_without_identity_rows)
ERROR: test_remove_worker_stale_retires_a_seat_whose_pane_is_gone (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stale_retires_a_seat_whose_pane_is_gone)
ERROR: test_remove_worker_stops_when_a_graceful_despawn_fails (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_a_graceful_despawn_fails)
ERROR: test_remove_worker_stops_when_the_forced_retry_also_fails (test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_the_forced_retry_also_fails)
ERROR: test_worker_seat_is_skipped_outside_a_git_main_checkout (test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_outside_a_git_main_checkout)
ERROR: test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state)
ERROR: test_agmsg_migration_reports_an_installer_that_mutates_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state)
ERROR: test_absent_path_without_old_ref_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_absent_path_without_old_ref_is_regression)
ERROR: test_chmod_only_change_keeps_the_source_unchanged_note (test_ua_symbol_coverage.UaSymbolCoverageTest.test_chmod_only_change_keeps_the_source_unchanged_note)
ERROR: test_comment_lines_are_not_definitions (test_ua_symbol_coverage.UaSymbolCoverageTest.test_comment_lines_are_not_definitions)
ERROR: test_def_column_reads_the_new_graph_revision (test_ua_symbol_coverage.UaSymbolCoverageTest.test_def_column_reads_the_new_graph_revision)
ERROR: test_deleted_path_with_old_ref_is_explained (test_ua_symbol_coverage.UaSymbolCoverageTest.test_deleted_path_with_old_ref_is_explained)
ERROR: test_flags_unexplained_symbol_loss_only (test_ua_symbol_coverage.UaSymbolCoverageTest.test_flags_unexplained_symbol_loss_only)
ERROR: test_grammar_file_missing_from_graph_fails_in_covered_directories (test_ua_symbol_coverage.UaSymbolCoverageTest.test_grammar_file_missing_from_graph_fails_in_covered_directories)
ERROR: test_low_similarity_move_with_no_symbols_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_low_similarity_move_with_no_symbols_is_regression)
ERROR: test_partial_deletion_in_changed_source_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_partial_deletion_in_changed_source_is_regression)
ERROR: test_partially_covered_new_file_is_not_flagged (test_ua_symbol_coverage.UaSymbolCoverageTest.test_partially_covered_new_file_is_not_flagged)
ERROR: test_python_defs_inside_strings_do_not_count (test_ua_symbol_coverage.UaSymbolCoverageTest.test_python_defs_inside_strings_do_not_count)
ERROR: test_rename_dropping_symbols_is_regression (test_ua_symbol_coverage.UaSymbolCoverageTest.test_rename_dropping_symbols_is_regression)
ERROR: test_rename_preserving_symbols_is_ok (test_ua_symbol_coverage.UaSymbolCoverageTest.test_rename_preserving_symbols_is_ok)
ERROR: test_ruby_visibility_prefixed_defs_are_counted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_ruby_visibility_prefixed_defs_are_counted)
ERROR: test_shell_names_with_punctuation_are_counted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_shell_names_with_punctuation_are_counted)
ERROR: test_unchanged_source_loss_is_noted (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unchanged_source_loss_is_noted)
ERROR: test_unreadable_candidate_fails_closed (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unreadable_candidate_fails_closed)
ERROR: test_unresolvable_ref_fails_closed (test_ua_symbol_coverage.UaSymbolCoverageTest.test_unresolvable_ref_fails_closed)
ERROR: test_uv_run_script_shebang_is_python (test_ua_symbol_coverage.UaSymbolCoverageTest.test_uv_run_script_shebang_is_python)
FAIL: test_ceiling_directories_do_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_ceiling_directories_do_not_hide_the_seat)
FAIL: test_character_device_placeholder_is_skipped (test_agent_stop_gate.AgentStopGateTest.test_character_device_placeholder_is_skipped)
FAIL: test_clean_orchestrator_passes (test_agent_stop_gate.AgentStopGateTest.test_clean_orchestrator_passes)
FAIL: test_every_team_of_the_identity_is_checked (test_agent_stop_gate.AgentStopGateTest.test_every_team_of_the_identity_is_checked)
FAIL: test_inherited_git_dir_does_not_hide_the_seat (test_agent_stop_gate.AgentStopGateTest.test_inherited_git_dir_does_not_hide_the_seat)
FAIL: test_json_escaped_cwd_resolves (test_agent_stop_gate.AgentStopGateTest.test_json_escaped_cwd_resolves)
FAIL: test_orchestrator_acceptance_to_another_member_keeps_the_result_open (test_agent_stop_gate.AgentStopGateTest.test_orchestrator_acceptance_to_another_member_keeps_the_result_open)
FAIL: test_project_dir_anchors_the_seat_after_a_cd (test_agent_stop_gate.AgentStopGateTest.test_project_dir_anchors_the_seat_after_a_cd)
FAIL: test_result_then_acceptance_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_acceptance_passes)
FAIL: test_result_then_revision_task_passes (test_agent_stop_gate.AgentStopGateTest.test_result_then_revision_task_passes)
FAIL: test_result_without_acceptance_blocks (test_agent_stop_gate.AgentStopGateTest.test_result_without_acceptance_blocks)
FAIL: test_sandbox_placeholders_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_are_skipped)
FAIL: test_sandbox_placeholders_on_a_separate_filesystem_are_skipped (test_agent_stop_gate.AgentStopGateTest.test_sandbox_placeholders_on_a_separate_filesystem_are_skipped)
FAIL: test_separate_git_dir_main_worktree_is_a_seat (test_agent_stop_gate.AgentStopGateTest.test_separate_git_dir_main_worktree_is_a_seat)
FAIL: test_slow_store_blocks_within_the_budget (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget)
FAIL: test_slow_store_blocks_within_the_budget_without_timeout (test_agent_stop_gate.AgentStopGateTest.test_slow_store_blocks_within_the_budget_without_timeout)
FAIL: test_solo_unsuffixed_worker_is_gated (test_agent_stop_gate.AgentStopGateTest.test_solo_unsuffixed_worker_is_gated)
FAIL: test_sqlite_store_off_the_current_schema_is_not_initialized (test_agent_stop_gate.AgentStopGateTest.test_sqlite_store_off_the_current_schema_is_not_initialized)
FAIL: test_staged_rename_out_of_orchestration_blocks (test_agent_stop_gate.AgentStopGateTest.test_staged_rename_out_of_orchestration_blocks)
FAIL: test_stop_hook_active_skips_only_the_dirty_tree_check (test_agent_stop_gate.AgentStopGateTest.test_stop_hook_active_skips_only_the_dirty_tree_check)
FAIL: test_worker_after_result_passes (test_agent_stop_gate.AgentStopGateTest.test_worker_after_result_passes)
FAIL: test_worker_alive_pong_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_alive_pong_keeps_the_task_open)
FAIL: test_worker_blocked_pong_closes_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_blocked_pong_closes_the_task)
FAIL: test_worker_result_to_another_member_keeps_the_task_open (test_agent_stop_gate.AgentStopGateTest.test_worker_result_to_another_member_keeps_the_task_open)
FAIL: test_worker_revise_acceptance_reopens_the_task (test_agent_stop_gate.AgentStopGateTest.test_worker_revise_acceptance_reopens_the_task)
FAIL: test_worker_task_closed_by_a_non_revise_acceptance (test_agent_stop_gate.AgentStopGateTest.test_worker_task_closed_by_a_non_revise_acceptance)
FAIL: test_worker_task_newer_than_result_blocks (test_agent_stop_gate.AgentStopGateTest.test_worker_task_newer_than_result_blocks)
FAIL: test_worker_tracks_each_task_id (test_agent_stop_gate.AgentStopGateTest.test_worker_tracks_each_task_id)
FAIL: test_gpgv_failure_preserves_existing_aws_and_skips_unzip (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_gpgv_failure_preserves_existing_aws_and_skips_unzip)
FAIL: test_verified_archive_runs_installer_with_user_local_update_arguments (test_aws_cli_acquisition.AwsCliAcquisitionTest.test_verified_archive_runs_installer_with_user_local_update_arguments)
FAIL: test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude (test_herdr_agents.HerdrAgentsTest.test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude)
FAIL: test_acceptance_record_accepts_a_dispatch_list (test_require_crit_review.ReviewGuardTest.test_acceptance_record_accepts_a_dispatch_list)
FAIL: test_acceptance_record_head_must_be_head (test_require_crit_review.ReviewGuardTest.test_acceptance_record_head_must_be_head)
FAIL: test_acceptance_record_is_not_counted_as_a_change (test_require_crit_review.ReviewGuardTest.test_acceptance_record_is_not_counted_as_a_change)
FAIL: test_acceptance_record_ledger_must_cover_a_badged_review_body (test_require_crit_review.ReviewGuardTest.test_acceptance_record_ledger_must_cover_a_badged_review_body)
FAIL: test_acceptance_record_ledger_must_cover_swept_findings (test_require_crit_review.ReviewGuardTest.test_acceptance_record_ledger_must_cover_swept_findings)
FAIL: test_acceptance_record_pr_must_be_the_swept_pr (test_require_crit_review.ReviewGuardTest.test_acceptance_record_pr_must_be_the_swept_pr)
FAIL: test_acceptance_record_prose_is_not_read (test_require_crit_review.ReviewGuardTest.test_acceptance_record_prose_is_not_read)
FAIL: test_acceptance_record_refuses_a_duplicate_key (test_require_crit_review.ReviewGuardTest.test_acceptance_record_refuses_a_duplicate_key)
FAIL: test_acceptance_record_refuses_a_non_finite_number (test_require_crit_review.ReviewGuardTest.test_acceptance_record_refuses_a_non_finite_number)
FAIL: test_acceptance_record_refuses_an_unknown_key (test_require_crit_review.ReviewGuardTest.test_acceptance_record_refuses_an_unknown_key)
FAIL: test_audit_finding_reason_may_quote_the_grammar (test_require_crit_review.ReviewGuardTest.test_audit_finding_reason_may_quote_the_grammar)
FAIL: test_audit_must_name_head_and_live_under_validation (test_require_crit_review.ReviewGuardTest.test_audit_must_name_head_and_live_under_validation) [wrong sha]
FAIL: test_audit_must_name_head_and_live_under_validation (test_require_crit_review.ReviewGuardTest.test_audit_must_name_head_and_live_under_validation) [other task]
FAIL: test_audit_must_name_head_and_live_under_validation (test_require_crit_review.ReviewGuardTest.test_audit_must_name_head_and_live_under_validation) [outside validation]
FAIL: test_audit_must_name_head_and_live_under_validation (test_require_crit_review.ReviewGuardTest.test_audit_must_name_head_and_live_under_validation) [bad name]
FAIL: test_base_accepts_a_correct_audit_of_head (test_require_crit_review.ReviewGuardTest.test_base_accepts_a_correct_audit_of_head)
FAIL: test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base (test_require_crit_review.ReviewGuardTest.test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base) (base='HEAD')
FAIL: test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base (test_require_crit_review.ReviewGuardTest.test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base) (base='main')
FAIL: test_base_fails_closed_when_github_metadata_is_unavailable (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_github_metadata_is_unavailable) (metadata='not JSON')
FAIL: test_base_fails_closed_when_github_metadata_is_unavailable (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_github_metadata_is_unavailable) (metadata='{}')
FAIL: test_base_fails_closed_when_github_metadata_is_unavailable (test_require_crit_review.ReviewGuardTest.test_base_fails_closed_when_github_metadata_is_unavailable) (metadata='{"baseRefOid": "-HEAD"}')
FAIL: test_base_rejects_forged_evidence_metadata (test_require_crit_review.ReviewGuardTest.test_base_rejects_forged_evidence_metadata) (field='base_sha', value='HEAD')
FAIL: test_base_rejects_forged_evidence_metadata (test_require_crit_review.ReviewGuardTest.test_base_rejects_forged_evidence_metadata) (field='base_ref', value='feature')
FAIL: test_base_rejects_forged_evidence_metadata (test_require_crit_review.ReviewGuardTest.test_base_rejects_forged_evidence_metadata) (field='base_sha', value=None)
FAIL: test_base_rejects_pr_commits_before_executing_their_collector (test_require_crit_review.ReviewGuardTest.test_base_rejects_pr_commits_before_executing_their_collector) (base='HEAD')
FAIL: test_base_rejects_pr_commits_before_executing_their_collector (test_require_crit_review.ReviewGuardTest.test_base_rejects_pr_commits_before_executing_their_collector) (base='HEAD')
FAIL: test_base_rejects_pr_commits_before_executing_their_collector (test_require_crit_review.ReviewGuardTest.test_base_rejects_pr_commits_before_executing_their_collector) (base='feature')
FAIL: test_base_rejects_side_branch_and_advanced_base_containing_pr_commits (test_require_crit_review.ReviewGuardTest.test_base_rejects_side_branch_and_advanced_base_containing_pr_commits) (base='absorbed')
FAIL: test_base_rejects_side_branch_and_advanced_base_containing_pr_commits (test_require_crit_review.ReviewGuardTest.test_base_rejects_side_branch_and_advanced_base_containing_pr_commits) (base='unrelated')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) (value='')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) (value='.orchestration/validation/test.md')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) (value='.orchestration/acceptance/other.md')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) (value='.orchestration/acceptance/alias.md')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) (value='.orchestration/acceptance/test.md')
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [no block]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [a closing line that is not exactly ---]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [not JSON]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [a list, not an object]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [a non-finite number]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [a duplicate key]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [format]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [task]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [head]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [pr]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [pr of another PR]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [ledger id]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [ledger class]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [searches records]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [searches twice for one class]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [audit_findings entry]
FAIL: test_base_requires_an_acceptance_record_under_acceptance (test_require_crit_review.ReviewGuardTest.test_base_requires_an_acceptance_record_under_acceptance) [S6]
FAIL: test_base_requires_audit_evidence_for_a_reviewed_change (test_require_crit_review.ReviewGuardTest.test_base_requires_audit_evidence_for_a_reviewed_change)
FAIL: test_base_requires_pr_feedback_evidence (test_require_crit_review.ReviewGuardTest.test_base_requires_pr_feedback_evidence)
FAIL: test_base_reviews_committed_branch_changes (test_require_crit_review.ReviewGuardTest.test_base_reviews_committed_branch_changes)
FAIL: test_blocked_or_missing_audit_verdict_fails (test_require_crit_review.ReviewGuardTest.test_blocked_or_missing_audit_verdict_fails) [verdict is blocked]
FAIL: test_blocked_or_missing_audit_verdict_fails (test_require_crit_review.ReviewGuardTest.test_blocked_or_missing_audit_verdict_fails) [verdict is missing]
FAIL: test_broad_orchestration_only_pr_needs_no_audit (test_require_crit_review.ReviewGuardTest.test_broad_orchestration_only_pr_needs_no_audit)
FAIL: test_companion_must_be_this_audits_own_last_message (test_require_crit_review.ReviewGuardTest.test_companion_must_be_this_audits_own_last_message)
FAIL: test_dispositions_of_2026_10_12_without_evidence_are_refused (test_require_crit_review.ReviewGuardTest.test_dispositions_of_2026_10_12_without_evidence_are_refused)
FAIL: test_dispositions_with_an_evidence_command_are_accepted (test_require_crit_review.ReviewGuardTest.test_dispositions_with_an_evidence_command_are_accepted)
FAIL: test_feedback_accepts_absolute_path_through_a_repository_parent_alias (test_require_crit_review.ReviewGuardTest.test_feedback_accepts_absolute_path_through_a_repository_parent_alias)
FAIL: test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent (test_require_crit_review.ReviewGuardTest.test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent)
FAIL: test_github_lookup_ignores_environment_repository_override (test_require_crit_review.ReviewGuardTest.test_github_lookup_ignores_environment_repository_override)
FAIL: test_github_lookup_rejects_evidence_from_another_repository (test_require_crit_review.ReviewGuardTest.test_github_lookup_rejects_evidence_from_another_repository)
FAIL: test_incorrect_audit_needs_audit_findings (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) [no audit_findings]
FAIL: test_incorrect_audit_needs_audit_findings (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) [a fix]
FAIL: test_incorrect_audit_needs_audit_findings (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) [short reason]
FAIL: test_incorrect_audit_needs_audit_findings (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) [no evidence]
FAIL: test_incorrect_audit_needs_audit_findings (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) [empty evidence]
FAIL: test_incorrect_audit_needs_audit_findings (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) [integer n]
FAIL: test_incorrect_audit_needs_audit_findings (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) [zero n]
FAIL: test_incorrect_audit_needs_audit_findings (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) [one missing]
FAIL: test_incorrect_audit_needs_audit_findings (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) [same finding twice]
FAIL: test_incorrect_audit_needs_audit_findings (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) [out of range]
FAIL: test_incorrect_audit_needs_audit_findings (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_needs_audit_findings) [accepted]
FAIL: test_incorrect_audit_without_findings_fails (test_require_crit_review.ReviewGuardTest.test_incorrect_audit_without_findings_fails)
FAIL: test_missing_base_collector_falls_back_only_after_binding (test_require_crit_review.ReviewGuardTest.test_missing_base_collector_falls_back_only_after_binding)
FAIL: test_no_diff_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_no_diff_does_not_require_review)
FAIL: test_older_base_must_not_be_on_the_head_first_parent_chain (test_require_crit_review.ReviewGuardTest.test_older_base_must_not_be_on_the_head_first_parent_chain)
FAIL: test_orchestration_only_pr_needs_no_audit (test_require_crit_review.ReviewGuardTest.test_orchestration_only_pr_needs_no_audit)
FAIL: test_pr_feedback_accepts_complete_evidence_without_a_bot_review (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_evidence_without_a_bot_review)
FAIL: test_pr_feedback_accepts_complete_root_cause_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_accepts_complete_root_cause_dispositions)
FAIL: test_pr_feedback_bodies_are_compared_after_secret_masking (test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) (case='masked with --mask-secrets')
FAIL: test_pr_feedback_bodies_are_compared_after_secret_masking (test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) (case='placeholder on another line, masked')
FAIL: test_pr_feedback_bodies_are_compared_after_secret_masking (test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) (case='quoted assignment, masked')
FAIL: test_pr_feedback_bodies_are_compared_after_secret_masking (test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) (case='verbatim body')
FAIL: test_pr_feedback_bodies_are_compared_after_secret_masking (test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) (case='different body')
FAIL: test_pr_feedback_bodies_are_compared_after_secret_masking (test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) (case='placeholder dropped from a body without a match')
FAIL: test_pr_feedback_bodies_are_compared_after_secret_masking (test_require_crit_review.ReviewGuardTest.test_pr_feedback_bodies_are_compared_after_secret_masking) (case='unmasked assignment with another value')
FAIL: test_pr_feedback_evidence_file_is_not_counted_as_a_change (test_require_crit_review.ReviewGuardTest.test_pr_feedback_evidence_file_is_not_counted_as_a_change)
FAIL: test_pr_feedback_fails_when_the_collector_cannot_run (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fails_when_the_collector_cannot_run)
FAIL: test_pr_feedback_fixed_commit_must_be_in_the_pr_range (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fixed_commit_must_be_in_the_pr_range) (case='predates the base')
FAIL: test_pr_feedback_fixed_commit_must_be_in_the_pr_range (test_require_crit_review.ReviewGuardTest.test_pr_feedback_fixed_commit_must_be_in_the_pr_range) (case='not in HEAD')
FAIL: test_pr_feedback_matches_a_masked_path_but_not_an_edited_one (test_require_crit_review.ReviewGuardTest.test_pr_feedback_matches_a_masked_path_but_not_an_edited_one) (case='path masked with --mask-secrets')
FAIL: test_pr_feedback_must_be_collected_for_the_current_head (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_be_collected_for_the_current_head)
FAIL: test_pr_feedback_must_cover_every_currently_collected_item (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_cover_every_currently_collected_item) (case='one item missing')
FAIL: test_pr_feedback_must_cover_every_currently_collected_item (test_require_crit_review.ReviewGuardTest.test_pr_feedback_must_cover_every_currently_collected_item) (case='hand-written empty list')
FAIL: test_pr_feedback_rejects_evidence_outside_the_repository (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_evidence_outside_the_repository)
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='missing disposition')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='stopgap wording')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='no evidence clause')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='empty evidence command')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='empty reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='a second evidence delimiter as the reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='a second evidence delimiter padding a failure reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='unknown commit')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='short failure reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='short in-progress reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='short cancelled reason')
FAIL: test_pr_feedback_rejects_incomplete_or_invalid_dispositions (test_require_crit_review.ReviewGuardTest.test_pr_feedback_rejects_incomplete_or_invalid_dispositions) (case='not an items document')
FAIL: test_pr_feedback_requires_the_github_head_to_match (test_require_crit_review.ReviewGuardTest.test_pr_feedback_requires_the_github_head_to_match)
FAIL: test_pr_feedback_uses_the_base_collector_not_the_prs_own (test_require_crit_review.ReviewGuardTest.test_pr_feedback_uses_the_base_collector_not_the_prs_own)
FAIL: test_recollection_must_match_the_authenticated_repository (test_require_crit_review.ReviewGuardTest.test_recollection_must_match_the_authenticated_repository)
FAIL: test_retired_audit_dispositions_is_not_read (test_require_crit_review.ReviewGuardTest.test_retired_audit_dispositions_is_not_read)
FAIL: test_s1_class_at_three_with_a_missing_replan_word_is_refused (test_require_crit_review.ReviewGuardTest.test_s1_class_at_three_with_a_missing_replan_word_is_refused) (missing='specification')
FAIL: test_s1_class_at_three_with_a_missing_replan_word_is_refused (test_require_crit_review.ReviewGuardTest.test_s1_class_at_three_with_a_missing_replan_word_is_refused) (missing='design')
FAIL: test_s1_class_at_three_with_a_missing_replan_word_is_refused (test_require_crit_review.ReviewGuardTest.test_s1_class_at_three_with_a_missing_replan_word_is_refused) (missing='implementation')
FAIL: test_s1_class_at_three_with_a_missing_replan_word_is_refused (test_require_crit_review.ReviewGuardTest.test_s1_class_at_three_with_a_missing_replan_word_is_refused) (missing='verification')
FAIL: test_s1_class_at_three_with_all_replan_words_is_accepted (test_require_crit_review.ReviewGuardTest.test_s1_class_at_three_with_all_replan_words_is_accepted) (words='verification, implementation, design, specification.')
FAIL: test_s1_class_at_three_with_all_replan_words_is_accepted (test_require_crit_review.ReviewGuardTest.test_s1_class_at_three_with_all_replan_words_is_accepted) (words='specification desigń implementation verification')
FAIL: test_s1_class_at_three_without_a_replan_line_is_refused (test_require_crit_review.ReviewGuardTest.test_s1_class_at_three_without_a_replan_line_is_refused)
FAIL: test_s1_replan_words_are_ascii_letter_runs (test_require_crit_review.ReviewGuardTest.test_s1_replan_words_are_ascii_letter_runs) (words='specification designᲉ implementation verification')
FAIL: test_s1_replan_words_are_ascii_letter_runs (test_require_crit_review.ReviewGuardTest.test_s1_replan_words_are_ascii_letter_runs) (words='specification designᲉ implementation')
FAIL: test_s6_class_at_three_with_the_matching_searches_entry_is_accepted (test_require_crit_review.ReviewGuardTest.test_s6_class_at_three_with_the_matching_searches_entry_is_accepted)
FAIL: test_s6_class_at_three_without_a_searches_entry_is_refused (test_require_crit_review.ReviewGuardTest.test_s6_class_at_three_without_a_searches_entry_is_refused)
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search (test_require_crit_review.ReviewGuardTest.test_s6_searches_entry_must_equal_the_recomputed_records_search) [the matching set]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search (test_require_crit_review.ReviewGuardTest.test_s6_searches_entry_must_equal_the_recomputed_records_search) [none where nothing matches]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search (test_require_crit_review.ReviewGuardTest.test_s6_searches_entry_must_equal_the_recomputed_records_search) [a record missing]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search (test_require_crit_review.ReviewGuardTest.test_s6_searches_entry_must_equal_the_recomputed_records_search) [a record too many]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search (test_require_crit_review.ReviewGuardTest.test_s6_searches_entry_must_equal_the_recomputed_records_search) [another class's entry]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search (test_require_crit_review.ReviewGuardTest.test_s6_searches_entry_must_equal_the_recomputed_records_search) [a pasted command for its records]
FAIL: test_s6_searches_entry_must_equal_the_recomputed_records_search (test_require_crit_review.ReviewGuardTest.test_s6_searches_entry_must_equal_the_recomputed_records_search)
FAIL: test_small_docs_only_change_does_not_require_review (test_require_crit_review.ReviewGuardTest.test_small_docs_only_change_does_not_require_review)
FAIL: test_swept_ids_come_from_authenticated_authors (test_require_crit_review.ReviewGuardTest.test_swept_ids_come_from_authenticated_authors)
FAIL: test_the_gate_has_no_github_identity_check (test_require_crit_review.ReviewGuardTest.test_the_gate_has_no_github_identity_check)
FAIL: test_verdict_comes_only_from_the_last_message_file (test_require_crit_review.ReviewGuardTest.test_verdict_comes_only_from_the_last_message_file)
FAIL: test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes)
FAIL: test_agmsg_checksum_mismatch_fails_closed (test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed)
FAIL: test_agmsg_fresh_install_populates_skill_and_records_manifest (test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest)
FAIL: test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty)
FAIL: test_agmsg_reports_an_installer_that_leaves_the_wrong_version (test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version)
FAIL: test_agmsg_update_aborts_when_install_corrupts_live_state (test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state)
FAIL: test_installer_cleanup_preserves_failure_status (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_preserves_failure_status) (relative='install/common/sheldon.sh')
FAIL: test_installer_cleanup_survives_mock_function_returns (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) (relative='install/common/mise.sh')
FAIL: test_installer_cleanup_survives_mock_function_returns (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) (relative='install/common/sheldon.sh')
FAIL: test_installer_cleanup_survives_mock_function_returns (test_supply_chain_policy.SupplyChainPolicyTest.test_installer_cleanup_survives_mock_function_returns) (relative='install/ubuntu/server/starship.sh')
FAIL: test_omp_version_check_accepts_the_branded_omp_slash_version_form (test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) (output='other/18.11.3')
FAIL: test_omp_version_check_accepts_the_branded_omp_slash_version_form (test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) (output='omp/omp/18.11.3')
FAIL: test_omp_version_check_accepts_the_branded_omp_slash_version_form (test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) (output='omp/18.11.3-extra')
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Darwin/arm64')
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Darwin/x86_64')
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Linux/x86_64')
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Linux/aarch64')
FAIL: test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin)
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='omp', shadow_version='pin')
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='omp', shadow_version='0.0.0')
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='hcom', shadow_version='pin')
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='hcom', shadow_version='0.0.0')
[exit 2]
```
## 7a. The failing modules of §7 at HEAD against the same modules on a scratch worktree at origin/main (99a4a80f), same sandbox
```console
$ for m in <the nine modules>; do grep -c "^(FAIL|ERROR): test.*(<m>." unit-final.txt; done; cat main-modules.txt
--- HEAD (f6adaea8), FAIL plus ERROR per module:
test_require_crit_review 136
test_herdr_agents 82
test_agent_stop_gate 28
test_ua_symbol_coverage 19
test_update_agent_assets 12
test_runtime_health 8
test_gh_auth 5
test_supply_chain_policy 4
test_aws_cli_acquisition 2
--- every module with a FAIL or ERROR at HEAD:
  28 test_agent_stop_gate
   2 test_aws_cli_acquisition
   5 test_gh_auth
  82 test_herdr_agents
 136 test_require_crit_review
   8 test_runtime_health
   4 test_supply_chain_policy
  19 test_ua_symbol_coverage
  12 test_update_agent_assets
--- origin/main, the unittest summary per module:
test_require_crit_review main: FAILED (failures=136)
test_herdr_agents main: FAILED (failures=1, errors=81)
test_agent_stop_gate main: FAILED (failures=28, skipped=1)
test_ua_symbol_coverage main: FAILED (errors=19)
test_update_agent_assets main: FAILED (failures=12)
test_runtime_health main: FAILED (failures=6, errors=2)
test_gh_auth main: FAILED (errors=5)
test_supply_chain_policy main: FAILED (failures=4)
test_aws_cli_acquisition main: FAILED (failures=2)
[exit 0]
```
## 8. make render-check
```console
$ make render-check
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
[exit 0]
```
## 9. make format: the shfmt step fails on 12 tracked files under .orchestration/tasks/*-input/, the same on origin/main; none is this branch's
```console
$ make format > "$TMPDIR/fmt.txt" 2>&1; echo "make format exit $?"; /usr/bin/grep -E "^diff " "$TMPDIR/fmt.txt" | awk "{print \$3}" | sort -u; echo "--- the same files on origin/main:"; for f in $(/usr/bin/grep -E "^diff " "$TMPDIR/fmt.txt" | awk "{print \$3}" | sort -u); do git show "origin/main:$f" > "$TMPDIR/m.sh"; shfmt --indent 4 --space-redirects -d "$TMPDIR/m.sh" > /dev/null; echo "$f origin/main shfmt exit $?"; done; echo "--- the steps after shfmt, run on their own:"; git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check | tail -n 1; git ls-files -z "*.md" | xargs -0 prettier --check 2>&1 | tail -n 1
make format exit 2
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
--- the same files on origin/main:
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh origin/main shfmt exit 1
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh origin/main shfmt exit 1
home/dot_claude/hooks/executable_project-map-reload.sh origin/main shfmt exit 1
tests/install/macos/common/brew.bats origin/main shfmt exit 1
--- the steps after shfmt, run on their own:
63 files already formatted
All matched files use Prettier code style!
[exit 0]
```
## 10. shellcheck and shfmt -d on the three scripts; ruff on the two tests
```console
$ shellcheck scripts/orchestrator/verdict.sh scripts/orchestrator/audit-pool.sh scripts/orchestrator/orch-audit.sh && echo "shellcheck clean"; shfmt --indent 4 --space-redirects -d scripts/orchestrator/verdict.sh scripts/orchestrator/audit-pool.sh scripts/orchestrator/orch-audit.sh && echo "shfmt clean"; ruff check --config ruff.toml tests/unit/test_verdict.py tests/unit/test_audit_pool.py
shellcheck clean
shfmt clean
All checks passed!
[exit 0]
```
## 11. Caps (Amendment 1): git diff --numstat origin/main...HEAD, summed
```console
$ git diff --numstat origin/main...HEAD; git diff --numstat origin/main...HEAD | awk -F "\t" "{n = \$1 + \$2} \$3 ~ /^tests\\// {t += n; next} \$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^\\.schemas\\// {s += n; next} {o += n} END {printf \"scripts (outside tests/, .orchestration/, .schemas/): %d of 500\ntests/: %d of 500\n.schemas/ (data, outside the count): %d\n\", o, t, s}"
117	0	.orchestration/dotfiles-T133-verdict-audit-pool-a01/task.md
33	0	.schemas/audit.json
140	0	.schemas/classes.yaml
29	0	.schemas/verdict.json
132	0	scripts/orchestrator/audit-pool.sh
102	11	scripts/orchestrator/orch-audit.sh
255	0	scripts/orchestrator/verdict.sh
224	0	tests/unit/test_audit_pool.py
269	0	tests/unit/test_verdict.py
scripts (outside tests/, .orchestration/, .schemas/): 500 of 500
tests/: 493 of 500
.schemas/ (data, outside the count): 202
[exit 0]
```
## 12. The --shadow run on this PR (run outside the sandbox for gh; its output saved, then pasted here)
```console
$ cat "/private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles--claude-worktrees-worker-f/b204c929-0b93-4c40-8b53-fb722279af71/scratchpad/shadow410.txt"
$ scripts/orchestrator/verdict.sh 410 --task dotfiles-T133-verdict-audit-pool-a01 --shadow
verdict: hold: the record .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a01.md is not this task's at the head; PR 410 is not open, non-draft, on main; .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-audit-f6adaea.json is missing or fails .schemas/audit.json; the fresh sweep or .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-pr-feedback.json; the task file .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a01.md or the merge-base diff
verdict: hold .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-verdict-f6adaea.json
[verdict exit 20]
$ jq . <the verdict JSON>; tail -n 1 verdict-shadow.tsv
{
  "verdict": "hold",
  "pr": 410,
  "head": "f6adaea80dea9c170caecac4a264303ee3d27490",
  "task_id": "dotfiles-T133-verdict-audit-pool-a01",
  "conditions": [
    {
      "id": 1,
      "ok": true,
      "evidence": "warning: precheck.json is not bound to the record and the head (PRECHECK_REQUIRED=0)"
    },
    {
      "id": 2,
      "ok": false,
      "evidence": "required checks not SUCCESS: validate, test (ubuntu-24.04, server), test (ubuntu-24.04, client), test (macos-14, client), public-bootstrap (ubuntu-24.04, server), public-bootstrap (ubuntu-24.04, client), public-bootstrap (macos-14, client)"
    },
    {
      "id": 3,
      "ok": false,
      "evidence": "no valid audit .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-audit-f6adaea.json"
    },
    {
      "id": 4,
      "ok": false,
      "evidence": "no fresh sweep or no .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-pr-feedback.json"
    },
    {
      "id": 5,
      "ok": false,
      "evidence": "no readable front matter in .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a01.md or no merge-base diff"
    },
    {
      "id": 6,
      "ok": true,
      "evidence": "revises=0; no S1 line"
    },
    {
      "id": 7,
      "ok": false,
      "evidence": "no valid audit"
    },
    {
      "id": 8,
      "ok": false,
      "evidence": "no front matter, so no security reading"
    },
    {
      "id": 9,
      "ok": false,
      "evidence": "0 sha256 lines; mismatches: none"
    }
  ],
  "inputs_sha256": {
    "fresh-sweep": "c2177d578214fe1be0715809e89075b2b48e2d11d50d0b413010e0688e417c04"
  },
  "generated_at": "2026-10-18T05:38:50Z"
}
410	f6adaea80dea9c170caecac4a264303ee3d27490	hold			2026-10-18T05:38:50Z
[exit 0]
```
