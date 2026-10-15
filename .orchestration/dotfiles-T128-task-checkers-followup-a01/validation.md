---
task_id: dotfiles-T128-task-checkers-followup-a01
seat: claude-standard-dot-a002
code_commit: d99b6458
---

# Validation: dotfiles-T128-task-checkers-followup-a01

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox. `MAIN` names the main checkout, and `S` a scratch directory under `/tmp/claude-501` that holds the mutation runner. `UV_OFFLINE=1` was set. The output is verbatim, with the main checkout's path removed, and each block ends with the exit status of its command line's last command. §1 to §7 were captured at `d99b6458`, before the PR was marked ready. §8 ran outside the sandbox after the Bot's review of `4cc9d206`.

## 1. Task file and task copy

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
506fa2ce4da29aaa64f67c02b5fbaa92eee40fb0fc0c65070aaf0a3b63a69442  .orchestration/tasks/dotfiles-T128-task-checkers-followup-a01.md
506fa2ce4da29aaa64f67c02b5fbaa92eee40fb0fc0c65070aaf0a3b63a69442  .orchestration/dotfiles-T128-task-checkers-followup-a01/task.md
byte-identical
[exit 0]
```
```console
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T128-task-checkers-followup-a01.md: OK
[exit 0]
```

## 2. Branch and the two premises

```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
d99b6458 fix(orchestrator): the T704 lineage's owned rows: C9's landed checker path, the ledger counts the Codex Bot only, orch-audit.sh trusts only a tracked and unchanged ledger check (T128 task-checkers followup a01)
595997831afcc05b266c9f245456df54725628db
[exit 0]
```
```console
$ git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-task-checkers-a01.md && echo present || echo absent; git cat-file -e origin/main:.orchestration/acceptance/dotfiles-T128-task-checkers-a01.md && echo present || echo absent
present
present
[exit 0]
```

## 3. The owned rows (item 1), read from origin/main

```console
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-task-checkers-a01.md | awk '/^## Owned by dotfiles-T128-task-checkers-followup-a01/ {p = 1; next} /^## / {p = 0} p && /^[^ ]+\t[a-z0-9-]+$/'
local:c1f60f7:3	advisory-p2
audit:c1f60f7:1	ledger-fidelity
audit:c1f60f7:2	trusted-checkout
audit:c1f60f7:3	counter-evidence
[exit 0]
```
```console
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-task-checkers-a01.md | /usr/bin/grep -n '^audit-finding: c1f60f7:3\|^local-finding: c1f60f7:3' | cut -c1-200
94:local-finding: c1f60f7:3 not-applicable:advisory P2 owned by dotfiles-T128-task-checkers-followup-a01 (- [P2] Probe the actual task-consistency checker path — scripts/orchestrator/task-consistency-
122:audit-finding: c1f60f7:3 not-applicable:fixed in this record before the gate (the counters pasted and the threshold dispositioned above); evidence=grep -n 'Threshold disposition' .orchestration/ac
[exit 0]
```

## 4. The script change

```console
$ git diff origin/main...HEAD -- scripts/
diff --git a/scripts/orchestrator/ledger-check.py b/scripts/orchestrator/ledger-check.py
index 26c15b2e..032fd4b0 100644
--- a/scripts/orchestrator/ledger-check.py
+++ b/scripts/orchestrator/ledger-check.py
@@ -1,7 +1,7 @@
 """Read-only: the acceptance record has a ledger row for each Bot finding of the sweep and each audit finding.
 
 `ledger-check.py <record.md> <sweep.json> <audit .last.md>...` (plan 007 T704; orch-audit.sh runs it on every audit):
-a row is a record line `<id><TAB><class>`, the id a Bot review comment or badged Bot review of the sweep, or
+a row is a record line `<id><TAB><class>`, the id a Codex Bot review comment or badged review of the sweep, or
 `audit:<sha7>:<n>` for the n-th `[P0]` to `[P3]` line, bulleted or not, of an audit named `*-audit-<sha7>.md*`. Prints `ledger rows <n>; findings <n>; gaps <n>`
 and one `GAP <id>` line per missing row; exit 1 when a row is missing.
 """
@@ -20,7 +20,8 @@ def main(record, sweep, *audits):
     need = []
     for item in json.loads(Path(sweep).read_text())["items"]:
         url, body = item.get("url") or "", item.get("body") or ""
-        if item["source"] == "review_comment" and item.get("bot") and "discussion_r" in url:
+        # The Codex Bot only, as the gate's swept_finding_ids() counts: another bot's comment is not a finding.
+        if item["source"] == "review_comment" and item.get("author") == BOT and "discussion_r" in url:
             need.append(url.rsplit("discussion_r", 1)[-1])
         elif item["source"] == "review" and item.get("author") == BOT and any(t in body for t in BADGES):
             need.append(url.rpartition("pullrequestreview-")[2])  # a badged review body, as the gate counts it
diff --git a/scripts/orchestrator/orch-audit.sh b/scripts/orchestrator/orch-audit.sh
index f42d0549..45426f2c 100755
--- a/scripts/orchestrator/orch-audit.sh
+++ b/scripts/orchestrator/orch-audit.sh
@@ -5,7 +5,8 @@
 #   Plan 007 T718, the parameterised form of the orchestrator's audit wrapper. The head is always `git -C
 #   <pr-worktree> rev-parse HEAD`. From the checkout this script lives in, never one at the audited head and
 #   only with its tracked, unchanged validator, it refuses a sweep JSON with an item lacking a disposition, runs
-#   the ledger check (ledger-check.py beside it, or the tracked script `--ledger-check` names), then checks the clean
+#   the ledger check (ledger-check.py beside it, or the script `--ledger-check` names; tracked and unchanged from HEAD,
+#   as the validator is), then checks the clean
 #   review worktree `.claude/worktrees/orchestrator-review` out at `origin/main`, copies the task's evidence and
 #   its lineage's records but this head's audit files in, removes those in both checkouts, and runs `codex
 #   --profile audit exec --sandbox read-only -c approval_policy=never -o <out>.last.md` with stdin closed and
@@ -15,7 +16,8 @@
 # @arg $1 string Task id.
 # @arg $2 path The PR's checkout (its HEAD is the audited head).
 # @arg $3 int PR number.
-# @option --ledger-check <script> A ledger check tracked in this repository, run instead of ledger-check.py.
+# @option --ledger-check <script> A ledger check tracked in this repository and unchanged from HEAD, run instead of
+#   ledger-check.py.
 # @exitcode 0 The audit is written; its verdict line is printed.
 # @exitcode 2 Usage error, or a refused precondition.
 # @exitcode 3 The sweep has gaps, the ledger check failed, or codex produced no fresh audit.
@@ -49,7 +51,8 @@ git diff --quiet HEAD -- scripts/validate-agent-assets.py || refuse "the validat
 [[ -z $(git -C "${review}" status --porcelain --untracked-files=all) ]] || refuse "the review worktree is not clean"
 base="$(git merge-base origin/main "${head}")"
 uv run --no-project python -I -c 'import json, sys; gaps = [i for i in json.load(open(sys.argv[1]))["items"] if not i.get("disposition")]; print("sweep gaps", len(gaps)); sys.exit(1 if gaps else 0)' "${v}/${task}-pr-feedback.json" || refuse "the sweep has gaps" 3
-(($# == 3)) || [[ -n $(git ls-files -- "${check}") ]] || refuse "${check} is not a script tracked in this repository"
+[[ -n $(git ls-files -- "${check}") ]] || refuse "${check} is not a script tracked in this repository"
+git diff --quiet HEAD -- "${check}" || refuse "${check} differs from HEAD"
 lineage=("${v}/${family}"-a0*-audit-*.md.last.md)
 uv run --no-project python "${check}" ".orchestration/acceptance/${task}.md" "${v}/${task}-pr-feedback.json" ${lineage[@]+"${lineage[@]}"} || refuse "the ledger is incomplete" 3
 git -C "${review}" checkout -q --detach origin/main
diff --git a/scripts/orchestrator/task-consistency-check.py b/scripts/orchestrator/task-consistency-check.py
index 46541c75..b90616a5 100644
--- a/scripts/orchestrator/task-consistency-check.py
+++ b/scripts/orchestrator/task-consistency-check.py
@@ -33,6 +33,7 @@ C7_NAMES = ROW_UNIT.split("|")
 NONPATH = ("in-process effects", "task metadata", "metadata separators", "workflow and interpreter")
 NONPATH += ("new or renamed scripts", "orchestrator effect")
 C9_NAMES = r"(scripts/[\w./-]+|\b[A-Z][A-Z_]{3,}_EVIDENCE\b|task-consistency-check C\d|\bC\d\b of the task-consistency check|\bclasses:)"
+CHECKER = "scripts/orchestrator/task-consistency-check.py"  # where `task-consistency-check C<n>` lands
 
 
 def front(text):
@@ -113,7 +114,7 @@ def check(p, root):
         if re.search(r"\b(once|until)\b", sent):
             continue
         for n in set(re.findall(C9_NAMES, sent)):
-            probe = n.replace("task-consistency-check ", "scripts/task-consistency-check.py#").split("#")[0]
+            probe = n.replace("task-consistency-check ", f"{CHECKER}#").split("#")[0]
             if probe.startswith("scripts/"):
                 ok = git(root, "cat-file", "-e", f"origin/main:{probe}").returncode == 0
             elif probe.endswith("_EVIDENCE"):
[exit 0]
```

## 5. The Check

```console
$ uv run python -m unittest tests/unit/test_task_checkers.py tests/unit/test_orchestrator_tools.py tests/unit/test_agmsg_orchestration_docs.py -v 2>&1 | /usr/bin/grep -E "c9_probes|counts_what_the_gate|ledger_check_passes|orch_audit|^Ran|^OK|^FAILED"
test_ledger_check_counts_what_the_gate_counts (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_counts_what_the_gate_counts) ... ok
test_ledger_check_passes_a_complete_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_passes_a_complete_record) ... ok
test_task_consistency_check_c9_probes_the_landed_checker_path (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_c9_probes_the_landed_checker_path) ... ok
test_orch_audit_refuses_a_ledger_check_that_differs_from_head (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_refuses_a_ledger_check_that_differs_from_head) ... ok
test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt) ... ok
test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap) ... ok
Ran 103 tests in 37.207s
OK
[exit 0]
```
```console
$ shellcheck scripts/orchestrator/orch-audit.sh && echo shellcheck-clean; shfmt -i 4 -sr -d scripts/orchestrator/orch-audit.sh && echo shfmt-clean; ruff format --check scripts/orchestrator tests/unit/test_task_checkers.py tests/unit/test_orchestrator_tools.py && ruff check scripts/orchestrator/ledger-check.py scripts/orchestrator/task-consistency-check.py tests/unit/test_task_checkers.py tests/unit/test_orchestrator_tools.py
shellcheck-clean
shfmt-clean
7 files already formatted
All checks passed!
[exit 0]
```

## 6. Caps

```console
$ git diff --numstat origin/main...HEAD
3	2	scripts/orchestrator/ledger-check.py
6	3	scripts/orchestrator/orch-audit.sh
2	1	scripts/orchestrator/task-consistency-check.py
36	6	tests/unit/test_orchestrator_tools.py
23	3	tests/unit/test_task_checkers.py
[exit 0]
```
```console
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^(tests|\.orchestration)\// {o += $1 + $2; f++} $3 ~ /^tests\// {t += $1} END {printf "outside tests/ and .orchestration/: %d changed lines (cap 200), %d files; under tests/: %d added lines (cap 1000)\n", o, f, t}'
outside tests/ and .orchestration/: 17 changed lines (cap 200), 3 files; under tests/: 59 added lines (cap 1000)
[exit 0]
```

## 7. Mutation pass

```console
$ uv run --no-project python -I "$S/mutate.py" "$PWD"; git status --short -- scripts
T1 C9 old path: caught
L1 any bot: caught
A1 no HEAD check: caught
A2 default skips tracking: caught
mutations: 4, caught 4
[exit 0]
```

## 8. CI and the Bot on `4cc9d206`

Run outside the sandbox through the permission gate (sandbox record, rows 5 to 7).

```console
$ bash /tmp/claude-501/tcf/bot-wait.sh 365 4cc9d2061f3121952449b1d000edca69c7bb7888 1792040245
elapsed=190s
reviews:
5528296451	4cc9d2061f3121952449b1d000edca69c7bb7888	2026-10-15T05:00:08Z	COMMENTED
comments:
4279174373	4cc9d2061f3121952449b1d000edca69c7bb7888	scripts/orchestrator/orch-audit.sh
[exit 0]
```
```console
$ gh api repos/mryfmo/dotfiles/pulls/365/comments --paginate --jq '[.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .in_reply_to_id==null)]|length'
1
[exit 0]
```

Comment 4279174373, `orch-audit.sh` line 55, is titled `P2 Badge … Isolate imports for the trusted ledger checker`. Review 5528296451's body holds the summary text and no badge.

```console
$ gh pr checks 365 --repo mryfmo/dotfiles --watch --interval 30 > /dev/null 2>&1; echo "checks-watch-exit=$?"; gh pr checks 365 --repo mryfmo/dotfiles
checks-watch-exit=0
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	8s	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/38684185649/job/116255173781	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38684185649/job/116255173710	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38684185649/job/116255173740	
public-bootstrap (macos-14, client)	pass	9m38s	https://github.com/mryfmo/dotfiles/actions/runs/38684185649/job/116255173584	
public-bootstrap (ubuntu-24.04, client)	pass	9m38s	https://github.com/mryfmo/dotfiles/actions/runs/38684185649/job/116255173783	
public-bootstrap (ubuntu-24.04, server)	pass	8m5s	https://github.com/mryfmo/dotfiles/actions/runs/38684185649/job/116255173733	
test (macos-14, client)	pass	6m49s	https://github.com/mryfmo/dotfiles/actions/runs/38684185650/job/116255173596	
test (ubuntu-24.04, client)	pass	8m23s	https://github.com/mryfmo/dotfiles/actions/runs/38684185650/job/116255173560	
test (ubuntu-24.04, server)	pass	5m27s	https://github.com/mryfmo/dotfiles/actions/runs/38684185650/job/116255173243	
test (ubuntu-26.04, client)	pass	8m42s	https://github.com/mryfmo/dotfiles/actions/runs/38684185650/job/116255173619	
validate	pass	1m41s	https://github.com/mryfmo/dotfiles/actions/runs/38684185722/job/116255173773	
[exit 0]
```
