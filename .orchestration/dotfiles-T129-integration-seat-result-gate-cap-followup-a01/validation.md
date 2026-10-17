---
task_id: dotfiles-T129-integration-seat-result-gate-cap-followup-a01
seat: claude-standard-dot-a007
---

# Validation: dotfiles-T129-integration-seat-result-gate-cap-followup-a01

Every command ran from the worktree `.claude/worktrees/worker-c` on the branch `tools/integration-seat-review-body-findings` (stacked on PR #393's head 087516f5), inside the sandbox; `MAIN` names the main checkout and `T` the task id. The output is verbatim, with the home directory replaced by `~`; each block ends with the exit status of the command shown.

## 1. Task file, task copy and the owned row

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
41374b642fbee60caa431e5a73f1d413d4e7744f3941ec71ec775a0b0cde10ad  $MAIN/.orchestration/tasks/dotfiles-T129-integration-seat-result-gate-cap-followup-a01.md
41374b642fbee60caa431e5a73f1d413d4e7744f3941ec71ec775a0b0cde10ad  .orchestration/dotfiles-T129-integration-seat-result-gate-cap-followup-a01/task.md
byte-identical
(exit 0)
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-integration-seat-result-gate-cap-followup-a01.md: OK
(exit 0)
$ git rev-parse HEAD   # PR #393 head, the stacked base
087516f51b8de9ccff42a0a748c34e913af9c8d9
(exit 0)
$ grep -n "^4302959629" the owner section
36:4302959629	review-body-findings
(exit 0)
```

## 2. The diff against 087516f5

```console
$ git diff 087516f51b8de9ccff42a0a748c34e913af9c8d9 -- scripts tests
diff --git a/scripts/orchestrator/result-precheck.sh b/scripts/orchestrator/result-precheck.sh
index b6abc304..0e12554a 100755
--- a/scripts/orchestrator/result-precheck.sh
+++ b/scripts/orchestrator/result-precheck.sh
@@ -4,7 +4,8 @@
 # @description
 #   Plan 023 F4 item 2. `run <task> <pr> <head>` (the worker) writes `.orchestration/<task>/precheck-<sha7>.md`: (a) the
 #   task copy vs the TASK line, (b) files vs allowed_files, (c) the Check's caps, (d) its commands in the validation file,
-#   (e) CI, (f) the Bot's review, (g) each Bot thread as `<id>:<P>:<disposition>` in the report, (h) the local review, (i) the
+#   (e) CI, (f) the Bot's review, (g) each Bot thread as `<id>:<P>:<disposition>` and each Bot review body with a badge as
+#   `review-<id>:<P>:<disposition>` in the report, (h) the local review, (i) the
 #   audit dry run: each `ok`, `missing` or (h, i) `unavailable (<reason>)`; exit 1 on a `missing`. `verify <task> <RESULT>`
 #   finds the receipt by `precheck=` in the tree of `head=` and refuses one without nine statuses, a `missing` or later code.
 # @exitcode 0 Every check ok.
@@ -84,12 +85,17 @@ check_f() {
         /usr/bin/grep -E "bot: none.*${head:0:7}|${head:0:7}.*bot: none" "${d}/report.md"
 }
 check_g() {
-    gh api --paginate "repos/{owner}/{repo}/pulls/${pr}/comments" --jq ".[] | ${bot} | select(.in_reply_to_id == null) | \"\(.id) \(.body | capture(\"(?<p>P[0-3]) Badge\").p // \"P3\")\"" |
+    {
+        gh api --paginate "repos/{owner}/{repo}/pulls/${pr}/comments" --jq ".[] | ${bot} | select(.in_reply_to_id == null) | \"\(.id) \(.body | capture(\"(?<p>P[0-3]) Badge\").p // \"P3\")\""
+        # A review body with a P0 to P3 badge is a finding too (Worker Playbook step 15), named review-<id>, its top badge.
+        gh api --paginate "repos/{owner}/{repo}/pulls/${pr}/reviews" --jq ".[] | ${bot} | {id, p: [.body // \"\" | scan(\"P([0-3]) Badge\") | .[0]]} | select(.p | length > 0) | \"review-\(.id) P\(.p | min)\""
+    } |
         {
             bad=0
             while read -r id p; do # the RESULT's thread token: <id>:P0|P1:fixed:<sha> or open:, <id>:P2|P3:<any>
                 echo "${id} ${p}"
-                /usr/bin/grep -q -E "${id}:${p}:$([[ ${p} == P[01] ]] && echo '(fixed:[0-9a-f]{7}|open:)')" "${d}/report.md" || bad=1
+                # Bounded on the left: a thread id must not match inside review-<id> or a longer number.
+                /usr/bin/grep -q -E "(^|[^0-9-])${id}:${p}:$([[ ${p} == P[01] ]] && echo '(fixed:[0-9a-f]{7}|open:)')" "${d}/report.md" || bad=1
             done
             exit "${bad}"
         }
diff --git a/tests/unit/test_integration_seat.py b/tests/unit/test_integration_seat.py
index 3d8971b2..96fff850 100644
--- a/tests/unit/test_integration_seat.py
+++ b/tests/unit/test_integration_seat.py
@@ -392,6 +392,43 @@ class IntegrationSeatTest(unittest.TestCase):
 
     # Fix round 3 (D-F4-round3): the defects the first use of item 2 found on PR #393.
 
+    def test_result_precheck_reads_the_bot_review_bodies_as_findings(self) -> None:
+        # The Bot's 4302959629: a P0 to P3 badge in a review body is a finding (Worker Playbook step 15), so (g) needs
+        # its review-<id> token in the report; a review body without a badge names none.
+        d = self.precheck_ready()
+        reviews = [
+            {"id": 9, "user": BOT, "commit_id": self.head},
+            {"id": 5550000001, "user": BOT, "commit_id": self.head, "body": "**![P1 Badge](x)** a body finding"},
+            {"id": 5550000002, "user": BOT, "commit_id": self.head, "body": "### 💡 Codex Review\n\nno badge here"},
+            # Two badges in one body: the token carries the top one.
+            {
+                "id": 5550000003,
+                "user": BOT,
+                "commit_id": self.head,
+                "body": "**![P2 Badge](x)** a\n**![P1 Badge](x)** b",
+            },
+        ]
+        (self.calls / "reviews.json").write_text(json.dumps(reviews))
+        inline = "4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory);review-5550000003:P1:open:"
+        collision = "threads=review-4300000001:P1:fixed:abcdef1;4300000002:P2:x;review-5550000001:P1:open:;"
+        collision += "review-5550000003:P1:open:\n"
+        for report, status in (
+            (f"threads={inline}\n", "missing"),
+            (f"threads={inline};review-5550000001:P1:proposed(x)\n", "missing"),
+            (f"threads={inline};review-5550000001:P1:fixed:abcdef1\n", "ok"),
+            (f"threads={inline};review-5550000001:P1:open:\n", "ok"),
+            # A thread id is read whole: review-4300000001 is not the inline thread 4300000001.
+            (collision, "missing"),
+        ):
+            with self.subTest(report=report):
+                (d / "report.md").write_text(report)
+                _, receipt = self.precheck(0 if status == "ok" else 1)
+                self.assertIn(f"- g {status}: ", receipt)
+                self.assertIn("review-5550000001 P1", receipt)
+                self.assertIn("review-5550000003 P1", receipt)
+                self.assertNotIn("review-5550000002", receipt)
+                self.assertNotIn("review-9 ", receipt)
+
     def test_result_precheck_reads_the_task_sha_of_an_amended_task_line(self) -> None:
         # An amended TASK line names previous_task_sha256= before task_sha256=; (a) reads the latter only.
         d = self.precheck_ready()
(exit 0)
```

## 3. The new test against 087516f5's script

```console
$ uv run python -m unittest tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_reads_the_bot_review_bodies_as_findings -v   # against 087516f5's scripts/orchestrator/result-precheck.sh
test_result_precheck_reads_the_bot_review_bodies_as_findings ... 
  test_result_precheck_reads_the_bot_review_bodies_as_findings (report='threads=4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory);review-5550000003:P1:open:\n') ... FAIL
  test_result_precheck_reads_the_bot_review_bodies_as_findings (report='threads=4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory);review-5550000003:P1:open:;review-5550000001:P1:proposed(x)\n') ... FAIL
  test_result_precheck_reads_the_bot_review_bodies_as_findings (report='threads=4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory);review-5550000003:P1:open:;review-5550000001:P1:fixed:abcdef1\n') ... FAIL
  test_result_precheck_reads_the_bot_review_bodies_as_findings (report='threads=4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory);review-5550000003:P1:open:;review-5550000001:P1:open:\n') ... FAIL
  test_result_precheck_reads_the_bot_review_bodies_as_findings (report='threads=review-4300000001:P1:fixed:abcdef1;4300000002:P2:x;review-5550000001:P1:open:;review-5550000003:P1:open:\n') ... FAIL
FAIL: test_result_precheck_reads_the_bot_review_bodies_as_findings (report='threads=4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory);review-5550000003:P1:open:\n')
AssertionError: 1 != 0 : precheck=9d1d4ddda18b904dcf1ac4f7a7624a321092c5cfbea5a33999077a6fab229394 .orchestration/dotfiles-T129-x-a01/precheck-2c653ed.md
FAIL: test_result_precheck_reads_the_bot_review_bodies_as_findings (report='threads=4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory);review-5550000003:P1:open:;review-5550000001:P1:proposed(x)\n')
AssertionError: 1 != 0 : precheck=9d1d4ddda18b904dcf1ac4f7a7624a321092c5cfbea5a33999077a6fab229394 .orchestration/dotfiles-T129-x-a01/precheck-2c653ed.md
FAIL: test_result_precheck_reads_the_bot_review_bodies_as_findings (report='threads=4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory);review-5550000003:P1:open:;review-5550000001:P1:fixed:abcdef1\n')
AssertionError: 'review-5550000001 P1' not found in '---\ntask: dotfiles-T129-x-a01\npr: 7\nhead: 2c653edaeb20e09f8c943f825e1c5e5e8b2c431c\n---\n\n- a ok: `check_a`\n\n```\n96c3021924322650491b480a7cb7215918bc4204e38f48495672ccb481cd8d50  .orchestration/dotfiles-T129-x-a01/task.md\n```\n\n- b ok: `check_b`\n\n```\nyes .orchestration/dotfiles-T129-x-a01/report.md\nyes .orchestration/dotfiles-T129-x-a01/task.md\nyes .orchestration/dotfiles-T129-x-a01/validation.md\nyes scripts/orchestrator/new.sh\n```\n\n- c ok: `check_c`\n\n```\noutside 2 (cap 10), tests 0 (cap 100)\n```\n\n- d ok: `check_d`\n\n```\nuv run python -m unittest tests/unit/test_x.py -v\nshellcheck scripts/orchestrator/new.sh\ngit diff --numstat origin/main...HEAD\n```\n\n- e ok: `check_e`\n\n```\n\n```\n\n- f ok: `check_f`\n\n```\n9\n5550000001\n5550000002\n5550000003\n```\n\n- g ok: `check_g`\n\n```\n4300000001 P1\n4300000002 P2\n```\n\n- h unavailable (no local review of 2c653ed here; a Claude seat cannot run codex review): `check_h`\n\n```\nlocal-review: unavailable (no local review of 2c653ed here; a Claude seat cannot run codex review)\n```\n\n- i unavailable (codex is not on PATH or not reachable from this seat): `check_i`\n\n```\naudit-dry-run: unavailable (codex is not on PATH or not reachable from this seat)\n```\n\n'
FAIL: test_result_precheck_reads_the_bot_review_bodies_as_findings (report='threads=4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory);review-5550000003:P1:open:;review-5550000001:P1:open:\n')
AssertionError: 'review-5550000001 P1' not found in '---\ntask: dotfiles-T129-x-a01\npr: 7\nhead: 2c653edaeb20e09f8c943f825e1c5e5e8b2c431c\n---\n\n- a ok: `check_a`\n\n```\n96c3021924322650491b480a7cb7215918bc4204e38f48495672ccb481cd8d50  .orchestration/dotfiles-T129-x-a01/task.md\n```\n\n- b ok: `check_b`\n\n```\nyes .orchestration/dotfiles-T129-x-a01/report.md\nyes .orchestration/dotfiles-T129-x-a01/task.md\nyes .orchestration/dotfiles-T129-x-a01/validation.md\nyes scripts/orchestrator/new.sh\n```\n\n- c ok: `check_c`\n\n```\noutside 2 (cap 10), tests 0 (cap 100)\n```\n\n- d ok: `check_d`\n\n```\nuv run python -m unittest tests/unit/test_x.py -v\nshellcheck scripts/orchestrator/new.sh\ngit diff --numstat origin/main...HEAD\n```\n\n- e ok: `check_e`\n\n```\n\n```\n\n- f ok: `check_f`\n\n```\n9\n5550000001\n5550000002\n5550000003\n```\n\n- g ok: `check_g`\n\n```\n4300000001 P1\n4300000002 P2\n```\n\n- h unavailable (no local review of 2c653ed here; a Claude seat cannot run codex review): `check_h`\n\n```\nlocal-review: unavailable (no local review of 2c653ed here; a Claude seat cannot run codex review)\n```\n\n- i unavailable (codex is not on PATH or not reachable from this seat): `check_i`\n\n```\naudit-dry-run: unavailable (codex is not on PATH or not reachable from this seat)\n```\n\n'
FAIL: test_result_precheck_reads_the_bot_review_bodies_as_findings (report='threads=review-4300000001:P1:fixed:abcdef1;4300000002:P2:x;review-5550000001:P1:open:;review-5550000003:P1:open:\n')
AssertionError: 1 != 0 : precheck=9d1d4ddda18b904dcf1ac4f7a7624a321092c5cfbea5a33999077a6fab229394 .orchestration/dotfiles-T129-x-a01/precheck-2c653ed.md
Ran 1 test in 3.564s
FAILED (failures=5)
(exit 1)
```

## 4. The new test after the change, and the Check's module

```console
$ uv run python -m unittest tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_reads_the_bot_review_bodies_as_findings -v   # after the change
test_result_precheck_reads_the_bot_review_bodies_as_findings (tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_reads_the_bot_review_bodies_as_findings) ... ok

----------------------------------------------------------------------
Ran 1 test in 3.522s

OK
(exit 0)
```

```console
$ uv run python -m unittest tests/unit/test_integration_seat.py -v
test_integrate_seat_reads_plain_gh_output_under_clicolor_force (tests.unit.test_integration_seat.IntegrationSeatTest.test_integrate_seat_reads_plain_gh_output_under_clicolor_force) ... ok
test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges (tests.unit.test_integration_seat.IntegrationSeatTest.test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges) ... ok
test_result_precheck_and_integrate_seat_read_the_bus_bounded_with_stdin_closed (tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_and_integrate_seat_read_the_bus_bounded_with_stdin_closed) ... ok
test_result_precheck_keeps_the_whole_audit_dry_run_message (tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_keeps_the_whole_audit_dry_run_message) ... ok
test_result_precheck_reads_the_bot_review_bodies_as_findings (tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_reads_the_bot_review_bodies_as_findings) ... ok
test_result_precheck_reads_the_task_sha_of_an_amended_task_line (tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_reads_the_task_sha_of_an_amended_task_line) ... ok
test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt (tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt) ... ok

----------------------------------------------------------------------
Ran 7 tests in 28.130s

OK
(exit 0)
```

## 5. One mutant per part of the change

```python
"""4302959629: one mutant per part of the (g) change, each run against the new test."""
import subprocess
from pathlib import Path
script = Path("scripts/orchestrator/result-precheck.sh")
fixed = script.read_text()
test = "tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_reads_the_bot_review_bodies_as_findings"
lines = fixed.splitlines(keepends=True)
reviews = next(line for line in lines if "/reviews\" --jq" in line and "review-" in line)
def mutate(old, new):
    assert fixed.count(old) == 1, old
    return fixed.replace(old, new)
variants = [
    ("no review bodies read", mutate(reviews, "")),
    ("the first badge, not the top one", mutate("P\\(.p | min)", "P\\(.p[0])")),
    ("no left boundary on the id", mutate('"(^|[^0-9-])${id}:${p}:', '"${id}:${p}:')),
]
try:
    for name, body in variants:
        script.write_text(body)
        r = subprocess.run(["uv", "run", "python", "-m", "unittest", test], capture_output=True, text=True)
        tail = [x for x in r.stderr.splitlines() if x.startswith(("OK", "FAILED"))]
        print(f"{name}: rc={r.returncode} {' | '.join(tail)}")
finally:
    script.write_text(fixed)
print("restored byte-identical:", script.read_text() == fixed)
```

```console
$ uv run --offline --no-project python -I mutants.py   # from the worktree root; the script is pasted in the record
no review bodies read: rc=1 FAILED (failures=5)
the first badge, not the top one: rc=1 FAILED (failures=5)
no left boundary on the id: rc=1 FAILED (failures=1)
restored byte-identical: True
(exit 0)
```

## 6. ShellCheck, shfmt, Ruff and the caps

```console
$ shellcheck scripts/orchestrator/integrate-seat.sh scripts/orchestrator/result-precheck.sh
(exit 0)
$ shfmt -i 4 -sr -d scripts/orchestrator/result-precheck.sh
(exit 0)
$ ruff format --config ruff.toml --check tests/unit/test_integration_seat.py; ruff check --config ruff.toml tests/unit/test_integration_seat.py
1 file already formatted
All checks passed!
(exit 0)
$ git diff --numstat 087516f51b8de9ccff42a0a748c34e913af9c8d9
9	3	scripts/orchestrator/result-precheck.sh
37	0	tests/unit/test_integration_seat.py
(exit 0)
```
