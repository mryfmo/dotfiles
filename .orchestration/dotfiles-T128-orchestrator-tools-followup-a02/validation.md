---
task_id: dotfiles-T128-orchestrator-tools-followup-a02
seat: claude-standard-dot-a002
code_commit: bf0fe7ab
---

# Validation: dotfiles-T128-orchestrator-tools-followup-a02

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox; `MAIN` names the main checkout and `T` the task id. `UV_OFFLINE=1` was set for every uv call. The output is verbatim, with the main checkout's path replaced by `$MAIN`, and each block ends with the exit status of the command shown (the capture script's `PIPESTATUS`; §6's block shows the script and its output, and each mutant line carries its own `rc`). Captured at `bf0fe7ab`.

## 1. Task file and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
5fab7eb8076bb83f23f094cbbcd3be5e8881dd3b6ece707a4db14a96c119b3bb  $MAIN/.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02.md
5fab7eb8076bb83f23f094cbbcd3be5e8881dd3b6ece707a4db14a96c119b3bb  .orchestration/dotfiles-T128-orchestrator-tools-followup-a02/task.md
byte-identical
[exit 0]
```
```console
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T128-orchestrator-tools-followup-a02.md: OK
[exit 0]
```
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T-input/"*
b8e90801c5a20fbdd97f9b06a298e320e1bbabf3288cff6881a5b5dfdc5e6f43  $MAIN/.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02-input/a05-record.md
9b4f109878ee1dd912a2cd18cb9ef2fd9725d02a786b9c131d3d75061161b747  $MAIN/.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02-input/dotfiles-T128-chain-github-scripts-followup-a01-audit-e9404a6.last.md
fc57b78efdda6ae5fde3816cfb403f3b866bacf7cd19c819747f84fc88cda6be  $MAIN/.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02-input/dotfiles-T128-orchestrator-tools-followup-a01-audit-2e77a33.last.md
80939ee041f3e28891945efcf81f660891a033e6adfbc6a1fb6d1264c995784f  $MAIN/.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a02-input/dotfiles-T128-validator-offline-a01-audit-39c186a.last.md
[exit 0]
```
## 2. Branch and the three premises
```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
bf0fe7ab fix(orchestrator): boundary.sh deletes each name literally, fill_sweep.py sees collisions on its lookup keys and selects a null-url status by source and check (T128 orchestrator-tools followup a02)
907522c2ac89c2096a91e70d9effb512886df681
[exit 0]
```
```console
$ git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a01.md && echo present
present
[exit 0]
```
```console
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md | /usr/bin/grep -c '^## Owned by dotfiles-T128-orchestrator-tools-followup-a01'
1
[exit 0]
```
```console
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md | /usr/bin/grep -c '^audit:f48593d:'
6
[exit 0]
```
## 3. The owned rows (the attached copy of the record)
```console
$ /usr/bin/grep -n -E '^audit:(2e77a33|e9404a6|39c186a):' "$MAIN/.orchestration/tasks/$T-input/a05-record.md"
183:audit:2e77a33:1	pathspec-globbing
184:audit:2e77a33:2	collision-key-order
356:audit:e9404a6:2	evidence-command-null-url
357:audit:39c186a:2	evidence-command-null-url
[exit 0]
```
## 4. The diff outside tests and the evidence
```console
$ git diff origin/main...HEAD -- scripts/
diff --git a/scripts/orchestrator/boundary.sh b/scripts/orchestrator/boundary.sh
index ba92b8c2..26e367d7 100755
--- a/scripts/orchestrator/boundary.sh
+++ b/scripts/orchestrator/boundary.sh
@@ -51,7 +51,7 @@ for f in "${files[@]}"; do
         cp -- "${f}" "${tree}/${f}"
         copied+=("${f}")
     else
-        git -C "${tree}" rm -q --ignore-unmatch -- "${f}"
+        git -C "${tree}" rm -q --ignore-unmatch -- ":(literal)${f}"
     fi
 done
 cd -- "${tree}"
diff --git a/scripts/orchestrator/fill_sweep.py b/scripts/orchestrator/fill_sweep.py
index affb6302..261a0fb7 100644
--- a/scripts/orchestrator/fill_sweep.py
+++ b/scripts/orchestrator/fill_sweep.py
@@ -60,10 +60,11 @@ def main(argv):
             reply[str(c["in_reply_to_id"])] = m.group(1)  # the latest reply wins
     gaps = []
     keys = [(item.get("url") or "").rsplit("#", 1)[-1] for item in sweep["items"]]
-    shared = {k for k, n in collections.Counter(keys).items() if n > 1}
-    for n, (item, key) in enumerate(zip(sweep["items"], keys, strict=True)):
-        cid, source, body = key.replace("discussion_r", ""), item["source"], item.get("body") or ""
-        if key in shared:
+    cids = [key.replace("discussion_r", "") for key in keys]  # the lookup keys, so a collision is seen after the strip
+    shared = {k for k, n in collections.Counter(cids).items() if n > 1}
+    for n, (item, key, cid) in enumerate(zip(sweep["items"], keys, cids, strict=True)):
+        source, body = item["source"], item.get("body") or ""
+        if cid in shared:
             if cid in extra:
                 print("shared-key", cid, f"item#{n}")
             key, cid = f"item#{n}", None
@@ -72,6 +73,11 @@ def main(argv):
         elif source == "review" and "Codex Review" in body:
             source = "codex_review"
         show = f"{EVIDENCE}jq '.items[] | select(.url == \"{item.get('url')}\")' {sweep_path}"
+        if item.get("url") is None:  # a JSON null url (a status without a target): select by source and check
+            check = json.dumps(item.get("check"))
+            show = (
+                f"{EVIDENCE}jq '.items[] | select(.source == {json.dumps(source)} and .check == {check})' {sweep_path}"
+            )
         if cid is None:
             show = f"{EVIDENCE}jq '.items[{n}]' {sweep_path}"
         level = item.get("level")
[exit 0]
```
## 5. The Check
```console
$ uv run python -m unittest tests/unit/test_orchestrator_tools.py -v
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
test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history) ... ok
test_dispatch_records_the_sent_line_with_its_read_marker (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_records_the_sent_line_with_its_read_marker) ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file) ... ok
test_dispatch_refuses_a_line_without_a_task_id (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_line_without_a_task_id) ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_malformed_record_block_before_sending) ... ok
test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields) ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line) ... ok
test_dispatch_refuses_an_unwritable_record_before_sending (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_an_unwritable_record_before_sending) ... ok
test_dispatch_refuses_malformed_lines (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_malformed_lines) ... ok
test_ff_main_keeps_a_local_deletion_across_the_fast_forward (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_ff_main_keeps_a_local_deletion_across_the_fast_forward) ... ok
test_ff_main_keeps_local_edits_across_the_fast_forward (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_ff_main_keeps_local_edits_across_the_fast_forward) ... ok
test_fill_sweep_fills_only_a_commented_review (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_fills_only_a_commented_review) ... ok
test_fill_sweep_fills_only_notice_annotations_and_success_statuses (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_fills_only_notice_annotations_and_success_statuses) ... ok
test_fill_sweep_ignores_a_disposition_reply_from_another_login (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_ignores_a_disposition_reply_from_another_login) ... ok
test_fill_sweep_leaves_a_badged_review_body_a_gap (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_leaves_a_badged_review_body_a_gap) ... ok
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
Ran 51 tests in 33.344s

OK
[exit 0]
```
```console
$ shellcheck scripts/orchestrator/boundary.sh && echo clean
clean
[exit 0]
```
```console
$ ruff check scripts/orchestrator/fill_sweep.py tests/unit/test_orchestrator_tools.py && ruff format --check scripts/orchestrator/fill_sweep.py tests/unit/test_orchestrator_tools.py
All checks passed!
2 files already formatted
[exit 0]
```
## 6. Mutation check (each fix reverted alone, its test run, the file restored with git checkout)
```console
$ the three mutants below, run by a loop: sed the line, run the one test, git checkout the file
T=tests/unit/test_orchestrator_tools.py
run() { # label file sed-expression test
    sed -i '' "$3" "$2"
    git diff -U0 -- "$2" | /usr/bin/grep '^[-+] '
    UV_OFFLINE=1 uv run python -m unittest "$T" -k "$4" >"$TMPDIR/tf2/m.log" 2>&1
    echo "mutant=$1 test=$4 rc=$? $(tail -1 "$TMPDIR/tf2/m.log")"
    git checkout -- "$2"
}
run literal-off scripts/orchestrator/boundary.sh 's|":(literal)${f}"|"${f}"|' test_boundary_deletes_a_name_with_glob_characters_literally
run raw-keys scripts/orchestrator/fill_sweep.py 's|Counter(cids)|Counter(keys)|' test_fill_sweep_sees_a_collision_after_the_discussion_r_strip
run null-url-off scripts/orchestrator/fill_sweep.py 's|if item.get("url") is None:|if False:|' test_fill_sweep_selects_a_null_url_status_by_source_and_check
git status --short -- scripts/
--- output
-        git -C "${tree}" rm -q --ignore-unmatch -- ":(literal)${f}"
+        git -C "${tree}" rm -q --ignore-unmatch -- "${f}"
mutant=literal-off test=test_boundary_deletes_a_name_with_glob_characters_literally rc=1 FAILED (failures=1)
-    shared = {k for k, n in collections.Counter(cids).items() if n > 1}
+    shared = {k for k, n in collections.Counter(keys).items() if n > 1}
mutant=raw-keys test=test_fill_sweep_sees_a_collision_after_the_discussion_r_strip rc=1 FAILED (failures=1)
-        if item.get("url") is None:  # a JSON null url (a status without a target): select by source and check
+        if False:  # a JSON null url (a status without a target): select by source and check
mutant=null-url-off test=test_fill_sweep_selects_a_null_url_status_by_source_and_check rc=1 FAILED (failures=1)
[exit 0]
```
## 7. Caps
```console
$ git diff --numstat origin/main...HEAD
1	1	scripts/orchestrator/boundary.sh
10	4	scripts/orchestrator/fill_sweep.py
67	0	tests/unit/test_orchestrator_tools.py
[exit 0]
```
