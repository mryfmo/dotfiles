---
task_id: dotfiles-T130-sandbox-portability-a01
seat: claude-review-dot-a005
code_commit: 005e6c91
---

# Validation: dotfiles-T130-sandbox-portability-a01

Every command ran from the worktree `.claude/worktrees/worker-d` on the branch `portability/sandbox-a01` at `005e6c91`, inside the sandbox; `MAIN` names the main checkout and `T` the task id. uv ran offline. The output is verbatim, with the main checkout's and the home directory's paths replaced by `$MAIN` and `$HOME`, and each block ends with the exit status of the command shown.

## 1. Task file (Amendment 2's text, sha256 53eb1abb…) and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
53eb1abbaa839795a41abd9540a5e08bd312e95a4b9274bbdf272721f3a967bc  $MAIN/.orchestration/tasks/dotfiles-T130-sandbox-portability-a01.md
53eb1abbaa839795a41abd9540a5e08bd312e95a4b9274bbdf272721f3a967bc  .orchestration/dotfiles-T130-sandbox-portability-a01/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T130-sandbox-portability-a01.md: OK
[exit 0]
```
## 2. Branch and base
```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
005e6c91 test(portability): guard the tracked scripts against diff with a process-substitution argument and hard-coded /tmp (T130 sandbox-portability a01, items 1 and 2)
e9bc99d2fe02b8e35b33350d1fd0a0cdc1185dbd
[exit 0]
```
## 2a. Premise 1 (no diff with process substitution in tracked scripts)
```console
$ git grep -cE 'diff[^|]*<\(' origin/main -- scripts home install | wc -l | tr -d " "
0
[exit 0]
```
## 2b. Premise 2 (no ps parsing through a pipe)
```console
$ git grep -cE '\bps (-|a)[^|]*\|' origin/main -- scripts home install | wc -l | tr -d " "
0
[exit 0]
```
## 2c. Premise 3 (the store base lines of paths.py; item 3 withdrawn by Amendment 2, the premise still replays)
```console
$ git show origin/main:.claude/contextdb/contextdb/paths.py | /usr/bin/grep -nF .claude | cut -d: -f1 | paste -sd, -
44,54,68,114
[exit 0]
```
## 3. The sandbox measurement behind Amendment 1 (the four process-substitution forms, run inside the sandbox)
```console
$ bash -c "... done < <(...)"; bash -c "comm -23 <(...) <(...)"; bash -c "cat <(...)"; bash -c "diff <(...) <(...)"
process-substitution forms inside the sandbox (bash 3.2.57(1)-release):
done < <(...): lines=3 rc=0
comm <(..) <(..): rc=0
cat <(..): rc=0
diff: /dev/fd/63: Operation not permitted
diff <(..) <(..): rc=2
```
## 4. The Check: the guard tests (both green; item 2's guard was red on the two probe literals before they moved)
```console
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_sandbox_portability.py -v
test_no_hard_coded_tmp_in_tracked_scripts (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_no_hard_coded_tmp_in_tracked_scripts) ... ok
test_no_process_substitution_in_tracked_scripts (tests.unit.test_sandbox_portability.SandboxPortabilityTest.test_no_process_substitution_in_tracked_scripts) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.646s

OK
[exit 0]
```
## 4a. The two literals that moved off /tmp (item 2, Amendment 1)
```console
$ git diff origin/main...HEAD -- scripts/check-statusline-tools.py
diff --git a/scripts/check-statusline-tools.py b/scripts/check-statusline-tools.py
index ef9bff90..b289bb39 100644
--- a/scripts/check-statusline-tools.py
+++ b/scripts/check-statusline-tools.py
@@ -13,9 +13,9 @@ from pathlib import Path
 
 CLAUDE_STATUS = {
     "model": {"display_name": "Claude"},
-    "workspace": {"current_dir": "/private/tmp"},
+    "workspace": {"current_dir": "/nonexistent/statusline"},
     "session_id": "offline-test",
-    "transcript_path": "/private/tmp/nonexistent.jsonl",
+    "transcript_path": "/nonexistent/statusline/transcript.jsonl",
 }
 
 
[exit 0]
```
## 5. Caps: git diff --numstat origin/main...HEAD
```console
$ git diff --numstat origin/main...HEAD
2	2	scripts/check-statusline-tools.py
102	0	tests/unit/test_sandbox_portability.py
[exit 0]
```
## 5a. Caps summed (Amendment 2's Check: at most 20 changed lines outside tests/ and .orchestration/, 200 added under tests/)
```console
$ git diff --numstat origin/main...HEAD | awk '…'
outside tests/ and .orchestration/: 4 changed lines (cap 20); under tests/: 102 added lines (cap 200)
[exit 0]
```
## 6. CompactionDB memory add (Message Contract: before completion)
```console
$ UV_OFFLINE=1 uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] T130 sandbox-portability: measured inside the Claude sandbox … name that base."
a913dfb6-9917-4a58-baf1-d516cdcec6aa
[exit 0]
```
