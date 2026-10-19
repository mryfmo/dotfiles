---
task_id: dotfiles-T128-chain-review-scripts-followup-a05
seat: claude-standard-dot-a007
---

# Validation: dotfiles-T128-chain-review-scripts-followup-a05

Every command ran from the worktree `.claude/worktrees/worker-c` on the branch `tools/chain-review-scripts-followup-a05` (from origin/main a8a747af), inside the sandbox; `MAIN` names the main checkout and `T` the task id. The output is verbatim, with the home directory replaced by `~`; each block ends with the exit status of the command shown.

## 1. Task file, task copy and the owned row's source

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
b1b9cea0cc5ae47361fb6fef9d9c6f4c6d431e87ab61b85a122121eb736e15b6  $MAIN/.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a05.md
b1b9cea0cc5ae47361fb6fef9d9c6f4c6d431e87ab61b85a122121eb736e15b6  .orchestration/dotfiles-T128-chain-review-scripts-followup-a05/task.md
byte-identical
(exit 0)
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T128-chain-review-scripts-followup-a05.md: OK
(exit 0)
$ git rev-parse origin/main; git log --oneline -1 origin/main
a8a747af06b32ff1d0d1720467892f34d9465ae4
a8a747af fix(claude): render scoped sandbox access per platform (#392)
(exit 0)
$ grep -c "Owned by dotfiles-T128-chain-review-scripts-followup-a05" "$MAIN/.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a04.md"   # the owner section the task names as the source
0
(exit 1)
$ head -1 "$MAIN/.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04-audit-000c5c6.md.last.md"   # the row as the audit receipt states it
[P2] high implementation scripts/orchestrator/local-advisory.sh:62 The guard checks text after the **last** `-local-review-`, so `t-a01-local-review-notes-local-review-aaaaaa1.md` passes as `aaaaaa1`. A matching finding then inherits an unrelated `local:aaaaaa1:1` row’s class and provenance. A read-only probe reproduced this. Strip the exact task prefix before validating the entire suffix, and test this filename.
(exit 0)
```

## 2. The new test against origin/main's script

```console
$ uv run python -m unittest tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_reads_the_whole_suffix_after_the_task_prefix -v   # against origin/main a8a747af's scripts/orchestrator/local-advisory.sh
test_local_advisory_reads_the_whole_suffix_after_the_task_prefix (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_reads_the_whole_suffix_after_the_task_prefix) ... FAIL
AssertionError: Lists differ: ['local:cccccc3:1\tadvisory-p2'] != ['local:cccccc3:1\tunrelated-class']
- ['local:cccccc3:1\tadvisory-p2']
+ ['local:cccccc3:1\tunrelated-class']
Ran 1 test in 0.422s
FAILED (failures=1)
(exit 1)
```

## 3. The new test after the fix

```console
$ uv run python -m unittest tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_reads_the_whole_suffix_after_the_task_prefix -v   # after the fix
test_local_advisory_reads_the_whole_suffix_after_the_task_prefix (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_reads_the_whole_suffix_after_the_task_prefix) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.321s

OK
(exit 0)
```

## 4. The Check: the module

```console
$ uv run python -m unittest tests/unit/test_chain_review_scripts.py -v
test_local_advisory_classes_a_repeat_by_the_earlier_row (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_classes_a_repeat_by_the_earlier_row) ... ok
test_local_advisory_matches_an_earlier_review_id_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_matches_an_earlier_review_id_literally) ... ok
test_local_advisory_matches_the_owner_heading_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_matches_the_owner_heading_literally) ... ok
test_local_advisory_reads_the_whole_suffix_after_the_task_prefix (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_reads_the_whole_suffix_after_the_task_prefix) ... ok
test_local_advisory_records_p2_rows_and_stops_on_p0_p1 (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_records_p2_rows_and_stops_on_p0_p1) ... ok
test_local_advisory_refuses_a_malformed_owner_id (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_refuses_a_malformed_owner_id) ... ok
test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file) ... ok
test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory) ... ok
test_local_review_keeps_env_S_shebang_arguments (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_keeps_env_S_shebang_arguments) ... ok
test_local_review_pins_the_review_binary_interpreter (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_pins_the_review_binary_interpreter) ... ok
test_local_review_refuses_a_quoted_env_S_shebang (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_refuses_a_quoted_env_S_shebang) ... ok
test_local_review_resolves_codex_through_mise_and_refuses_a_shim (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_resolves_codex_through_mise_and_refuses_a_shim) ... ok
test_local_review_resolves_the_review_binary_before_the_checkout (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_resolves_the_review_binary_before_the_checkout) ... ok
test_local_review_reuses_only_a_file_that_records_this_head (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_reuses_only_a_file_that_records_this_head) ... ok
test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file) ... ok
test_local_review_strips_a_worktree_path_holding_sed_syntax_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_strips_a_worktree_path_holding_sed_syntax_literally) ... ok
test_local_review_writes_no_file_when_the_review_binary_fails (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_writes_no_file_when_the_review_binary_fails) ... ok
test_sandbox_scan_prints_the_unsandboxed_mutation_calls (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_sandbox_scan_prints_the_unsandboxed_mutation_calls) ... ok

----------------------------------------------------------------------
Ran 18 tests in 10.669s

OK
(exit 0)
```

## 5. ShellCheck, shfmt, Ruff, the caps and the diff

```console
$ shellcheck scripts/orchestrator/local-advisory.sh
(exit 0)
$ shfmt -i 4 -sr -d scripts/orchestrator/local-advisory.sh
(exit 0)
$ ruff format --config ruff.toml --check tests/unit/test_chain_review_scripts.py; ruff check --config ruff.toml tests/unit/test_chain_review_scripts.py
1 file already formatted
All checks passed!
(exit 0)
$ git diff --numstat origin/main -- scripts tests
3	1	scripts/orchestrator/local-advisory.sh
23	0	tests/unit/test_chain_review_scripts.py
(exit 0)
$ git diff origin/main -- scripts tests
diff --git a/scripts/orchestrator/local-advisory.sh b/scripts/orchestrator/local-advisory.sh
index 76ad6f41..70d63269 100755
--- a/scripts/orchestrator/local-advisory.sh
+++ b/scripts/orchestrator/local-advisory.sh
@@ -57,7 +57,9 @@ token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BA
 earlier=""
 for f in .orchestration/validation/"$task"-local-review-*.md; do
     [[ -f $f && $f != "$LR" ]] || continue
-    e=${f%.md} && e=${e##*-local-review-} && k=0
+    # The exact prefix is stripped, so the whole rest of the name must be the head: a name with a second
+    # `-local-review-` cannot pass as its last part (the audit of 000c5c6, finding 1).
+    e=${f%.md} && e=${e#.orchestration/validation/"$task"-local-review-} && k=0
     # Only a seven-hex suffix names a reviewed head; any other file is skipped (the audit of d3e8acf, finding 1).
     [[ $e =~ ^[0-9a-f]{7}$ ]] || continue
     while IFS= read -r l; do
diff --git a/tests/unit/test_chain_review_scripts.py b/tests/unit/test_chain_review_scripts.py
index 82c1e351..8d0fdd4f 100644
--- a/tests/unit/test_chain_review_scripts.py
+++ b/tests/unit/test_chain_review_scripts.py
@@ -496,6 +496,29 @@ class ChainReviewScriptsTest(unittest.TestCase):
         [line] = [line for line in text.splitlines() if line.startswith("local-finding: cccccc3:")]
         self.assertNotIn("repeat of", line)
 
+    def test_local_advisory_reads_the_whole_suffix_after_the_task_prefix(self):
+        # The audit of 000c5c6, finding 1: the guard read the text after the last `-local-review-`, so a file named
+        # t-a01-local-review-notes-local-review-aaaaaa1.md passed as aaaaaa1 and a repeat took that unrelated row's class.
+        owner, v = "t-followup-a01", ".orchestration/validation"
+        self.write(f".orchestration/tasks/{owner}.md", "owner\n")
+        self.write(
+            f"{v}/t-a01-local-review-notes-local-review-aaaaaa1.md",
+            "---\nfindings: 1\n---\n\n- [P2] scripts/x.sh:12 quoting\n",
+        )
+        record = self.write(".orchestration/acceptance/t-a01.md", "# record\nlocal:aaaaaa1:1\tunrelated-class\n")
+        head = "cccccc3" + "1" * 33
+        self.write(f"{v}/t-a01-local-review-cccccc3.md", "---\nfindings: 1\n---\n\n- [P2] scripts/x.sh:12 again\n")
+        self.run_tool("local-advisory.sh", "t-a01", head, owner)
+        text = record.read_text()
+        self.assertEqual(["local:cccccc3:1\tadvisory-p2"], re.findall(r"^local:cccccc3:\d\t.*$", text, re.MULTILINE))
+        [line] = [line for line in text.splitlines() if line.startswith("local-finding: cccccc3:")]
+        self.assertNotIn("repeat of", line)
+        # A real earlier review of the same task still classes the repeat.
+        self.write(f"{v}/t-a01-local-review-aaaaaa1.md", "---\nfindings: 1\n---\n\n- [P2] scripts/x.sh:12 quoting\n")
+        record.write_text("# record\nlocal:aaaaaa1:1\tquoting\n")
+        self.run_tool("local-advisory.sh", "t-a01", head, owner)
+        self.assertIn("local:cccccc3:1\tquoting\n", record.read_text())
+
     def test_sandbox_scan_prints_the_unsandboxed_mutation_calls(self):
         sandboxes = ".orchestration/sandboxes"
         hit = "| 2 | dangerouslyDisableSandbox: git commit -m wip |"
(exit 0)
```
