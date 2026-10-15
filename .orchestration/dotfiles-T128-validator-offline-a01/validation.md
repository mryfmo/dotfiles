---
task_id: dotfiles-T128-validator-offline-a01
seat: claude-standard-dot-a002
code_commit: 4730fb1c
---

# Validation: dotfiles-T128-validator-offline-a01

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox; `MAIN` names the main checkout. `UV_OFFLINE=1` was set for the commands that call uv directly. The output is verbatim, with the main checkout's path removed, and each block ends with the exit status of its command line's last command. Captured at `4730fb1c`.

## 1. Task file and task copy

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
52a5f2099551f2b434c23b0ccefcb426bf5c5b87288ebc3e2b43430d699c779e  .orchestration/tasks/dotfiles-T128-validator-offline-a01.md
52a5f2099551f2b434c23b0ccefcb426bf5c5b87288ebc3e2b43430d699c779e  .orchestration/dotfiles-T128-validator-offline-a01/task.md
byte-identical
[exit 0]
```
```console
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T128-validator-offline-a01.md: OK
[exit 0]
```

## 2. Branch and the three premises

```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
4730fb1c fix(make): the two validator recipes run from the uv cache when it holds PyYAML, through the index only when it does not (T128 validator-offline a01)
595997831afcc05b266c9f245456df54725628db
[exit 0]
```
```console
$ git show origin/main:Makefile | /usr/bin/grep -c "uv run --with pyyaml scripts/validate-agent-assets.py\|uv run --with pyyaml scripts/generate-agent-configs.py --check"
2
[exit 0]
```
```console
$ git cat-file -e origin/main:tests/unit/test_makefile_offline.py 2>/dev/null && echo present || echo absent
absent
[exit 0]
```
```console
$ git show origin/main:tests/install/common/lifecycle.bats | /usr/bin/grep -c "make validate-agent-assets\|make render-check"
0
[exit 1]
```

## 3. The change

```console
$ git diff origin/main...HEAD -- Makefile
diff --git a/Makefile b/Makefile
index 16678885..d50194bb 100644
--- a/Makefile
+++ b/Makefile
@@ -184,9 +184,12 @@ format:
 unit-test:
 	uv run python -m unittest discover -s tests/unit -v
 
+# The index form fails inside the Claude sandbox even while the uv cache holds PyYAML, so a probe picks the cache first.
+UV_PYYAML = $(if $(shell uv run --offline --with pyyaml python -c 'import yaml' 2> /dev/null && echo y),uv run --offline --with pyyaml,uv run --with pyyaml)
+
 .PHONY: validate-agent-assets
 validate-agent-assets:
-	uv run --with pyyaml scripts/validate-agent-assets.py
+	$(UV_PYYAML) scripts/validate-agent-assets.py
 
 .PHONY: check-regime-boundary
 check-regime-boundary:
@@ -200,7 +203,7 @@ codex-hook-trust:
 
 .PHONY: render-check
 render-check:
-	uv run --with pyyaml scripts/generate-agent-configs.py --check
+	$(UV_PYYAML) scripts/generate-agent-configs.py --check
 
 .PHONY: require-crit-review
 # BASE=<ref> adds the committed <ref>...HEAD changes and requires PR_FEEDBACK_EVIDENCE and
[exit 0]
```

## 4. The Check

```console
$ uv run python -m unittest tests/unit/test_makefile_offline.py -v
test_the_recipe_falls_back_only_when_the_cache_is_cold (tests.unit.test_makefile_offline.MakefileOfflineTest.test_the_recipe_falls_back_only_when_the_cache_is_cold) ... ok
test_validator_targets_try_the_offline_form_first (tests.unit.test_makefile_offline.MakefileOfflineTest.test_validator_targets_try_the_offline_form_first) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.504s

OK
[exit 0]
```
```console
$ make -n render-check; make -n validate-agent-assets
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
uv run --offline --with pyyaml scripts/validate-agent-assets.py
[exit 0]
```
```console
$ ruff format --check tests/unit/test_makefile_offline.py && ruff check tests/unit/test_makefile_offline.py
1 file already formatted
All checks passed!
[exit 0]
```

## 5. Both targets run for real inside the sandbox (D10 from this seat)

```console
$ make validate-agent-assets > /tmp/claude-501/vo-va.txt 2>&1; echo "validate-agent-assets rc=$?"; tail -1 /tmp/claude-501/vo-va.txt; make render-check 2>&1 | tail -1; echo "render-check rc=${PIPESTATUS[0]}"
validate-agent-assets rc=0
agent asset validation ok
generated agent configs are up to date
render-check rc=0
[exit 0]
```

## 6. Caps

```console
$ git diff --numstat origin/main...HEAD
5	2	Makefile
61	0	tests/unit/test_makefile_offline.py
[exit 0]
```
```console
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^(tests|\.orchestration)\// {o += $1 + $2; f++} $3 ~ /^tests\// {t += $1} END {printf "outside tests/ and .orchestration/: %d changed lines (cap 200), %d files; under tests/: %d added lines (cap 1000)\n", o, f, t}'
outside tests/ and .orchestration/: 7 changed lines (cap 200), 1 files; under tests/: 61 added lines (cap 1000)
[exit 0]
```
