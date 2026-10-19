---
task_id: dotfiles-T133-verdict-audit-pool-a03
seat: claude-standard-dot-a008
code_head: 8b0b5bb4
revise_1_code_head: cac07914
previous_head: b8998de162afc72d53d07679b8f0a194fcc480ff
revise_1_previous_head: 513e5d0532ec3c21484ab215ef77fea440329749
---

# Validation: dotfiles-T133-verdict-audit-pool-a03

- Every block prints its commands, their verbatim output and the block's last exit status. Each block ran inside the sandbox from this worktree on `tools/verdict-audit-pool-a01` at the code head `8b0b5bb4`. The only later commit adds this directory's records.
  - §11 is the exception: the Check's shadow invocation, which ran outside the sandbox because gh needs the network.
- `MAIN` names the main checkout, `T` the task id, and `OLD` the a02 head `b8998de1`. The scratch worktrees under `$TMPDIR` are removed after their block with `git worktree remove --force`.
- **Historical and final-head evidence:**
  - Historical red results of the retained fixes stay in the a01 and a02 records with their original heads.
  - §4 is this task's own red, against b8998de1.
  - §5, §6a and §8 to §10 are final-head results.
- **Inherited check failures**, each reproduced at the merge-base `3e41e36a` with the same command in the same sandbox:
  - §8a: `make format`.
  - §9a against §9b: `make unit-test`. They are reported as failures, not as passing.

## 1. Task file (sha256 2f049394…) and the branch copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
2f0493944badef8294dc691e87fba7ab6cc84ed2d6e135454a34b1219f724c42  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md
2f0493944badef8294dc691e87fba7ab6cc84ed2d6e135454a34b1219f724c42  .orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T133-verdict-audit-pool-a03.md: OK
[exit 0]
```
## 2. Branch, merge-base and this task's commits on top of the a02 head
```console
$ git branch --show-current; git rev-parse HEAD; git merge-base origin/main HEAD; git log --oneline $OLD..HEAD
tools/verdict-audit-pool-a01
8b0b5bb42b41e3a32344744a362f1c9fc99f2e35
3e41e36abc949acd7e6b4859c1a22df9e665c8d4
8b0b5bb4 test(orchestrator): verdict.sh --validate refuses each rule of the moved schema checker; the usage line names --validate (T133 verdict-audit-pool a03, worker review)
8f22dd9d fix(orchestrator): --apply holds unless the trusted integration gate passes; condition 5 reads each cap from its last declaration; the schema checker moves into verdict.sh from orch-audit.sh (T133 verdict-audit-pool a03)
f8f5da79 test(orchestrator): --apply runs the integration gate before dispatch or merge and holds on its failure; condition 5 honors the latest amended caps; the split's fixtures (T133 verdict-audit-pool a03)
0e16d7eb chore(orchestration): the P1-4a split: the a03 task copy replaces a02's; audit-pool.sh, classes.yaml and test_audit_pool.py leave this branch and orch-audit.sh returns to origin/main (T133 verdict-audit-pool a03)
[exit 0]
```
## 3. The split (item: first push): the a02 copy, the sibling files and orch-audit.sh leave the PR diff; the a03 copy is added
```console
$ git show --stat --format="%h %s" 0e16d7eb | cut -c1-160; for f in .orchestration/dotfiles-T133-verdict-audit-pool-a02/task.md scripts/orchestrator/audit-pool.sh .schemas/classes.yaml tests/unit/test_audit_pool.py; do git cat-file -e "HEAD:$f" 2> /dev/null && echo "present: $f" || echo "absent at HEAD: $f"; done; git diff --quiet origin/main HEAD -- scripts/orchestrator/orch-audit.sh && echo "orch-audit.sh equals origin/main"
0e16d7eb chore(orchestration): the P1-4a split: the a03 task copy replaces a02's; audit-pool.sh, classes.yaml and test_audit_pool.py leave this branch and orch-

 .../dotfiles-T133-verdict-audit-pool-a02/task.md   | 226 ---------------------
 .../dotfiles-T133-verdict-audit-pool-a03/task.md   | 212 +++++++++++++++++++
 .schemas/classes.yaml                              | 140 -------------
 scripts/orchestrator/audit-pool.sh                 | 126 ------------
 scripts/orchestrator/orch-audit.sh                 | 114 +----------
 tests/unit/test_audit_pool.py                      | 219 --------------------
 6 files changed, 223 insertions(+), 814 deletions(-)
absent at HEAD: .orchestration/dotfiles-T133-verdict-audit-pool-a02/task.md
absent at HEAD: scripts/orchestrator/audit-pool.sh
absent at HEAD: .schemas/classes.yaml
absent at HEAD: tests/unit/test_audit_pool.py
orch-audit.sh equals origin/main
[exit 0]
```
## 3a. The cumulative inventory outside .orchestration/ (origin/main...HEAD) against allowed_files, and the predecessor record directories still in the diff
```console
$ git diff --name-status origin/main...HEAD -- . ":!.orchestration"; git diff --name-only origin/main...HEAD -- .orchestration | cut -d/ -f2 | sort | uniq -c
A	.schemas/audit.json
A	.schemas/verdict.json
A	scripts/orchestrator/verdict.sh
A	tests/unit/test_verdict.py
   9 dotfiles-T133-verdict-audit-pool-a01
   7 dotfiles-T133-verdict-audit-pool-a02
   1 dotfiles-T133-verdict-audit-pool-a03
[exit 0]
```
## 4. RED: the two new regressions at b8998de1 (its verdict.sh and orch-audit.sh), with this head's test file, in a scratch worktree
```console
$ git -C "$R" rev-parse HEAD; git show HEAD:tests/unit/test_verdict.py > "$R/tests/unit/test_verdict.py"; cd "$R" && uv run python -m unittest tests.unit.test_verdict.VerdictTest.test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure tests.unit.test_verdict.VerdictTest.test_verdict_condition_5_honors_the_latest_amended_caps 2>&1 | /usr/bin/grep -E "^(FAIL|ERROR):|^AssertionError|^Ran|^(OK|FAILED)" | sed -E "s/ \(tests\.unit\.test_verdict\.VerdictTest\.[a-z0-9_]+\)//" | cut -c1-220
b8998de162afc72d53d07679b8f0a194fcc480ff
FAIL: test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure (case='zero exit')
AssertionError: Lists differ: ['gate t1-a01 c194569dfe68c8614407c4ed0d4fda[108 chars]128'] != ['gh pr checks 9 --json name,state', 'dispat[86 chars]128']
FAIL: test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure (case='failure')
AssertionError: Regex matched: 'dispatch' matches 'dispatch|pr merge' in 'gh pr view 9 --json headRefOid,isDraft,baseRefName,state,number\ngh pr checks 9 --json name,state\ndispatch dot orch w herdr:s:wJ:p3 /tmp/claude-5
FAIL: test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure (case='refusal')
AssertionError: Regex matched: 'dispatch' matches 'dispatch|pr merge' in 'gh pr view 9 --json headRefOid,isDraft,baseRefName,state,number\ngh pr checks 9 --json name,state\ndispatch dot orch w herdr:s:wJ:p3 /tmp/claude-5
FAIL: test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure (case='missing')
AssertionError: Regex matched: 'dispatch' matches 'dispatch|pr merge' in 'gh pr view 9 --json headRefOid,isDraft,baseRefName,state,number\ngh pr checks 9 --json name,state\ndispatch dot orch w herdr:s:wJ:p3 /tmp/claude-5
FAIL: test_verdict_condition_5_honors_the_latest_amended_caps (case='a later amendment allows 550')
AssertionError: 0 != 10 : verdict: revise .orchestration/validation/t1-a01-verdict-1dfae3d.json
FAIL: test_verdict_condition_5_honors_the_latest_amended_caps (case='the a02 test-only amendment wording')
AssertionError: 0 != 10 : verdict: revise .orchestration/validation/t1-a01-verdict-1dfae3d.json
FAIL: test_verdict_condition_5_honors_the_latest_amended_caps (case='the effective exclusions')
AssertionError: 0 != 10 : verdict: revise .orchestration/validation/t1-a01-verdict-1dfae3d.json
Ran 2 tests in 42.442s
FAILED (failures=7)
[exit 0]
```
## 5. GREEN: the Check command at HEAD, the whole verdict module verbose (the two regressions and every retained case)
```console
$ git rev-parse --short=8 HEAD; uv run python -m unittest tests.unit.test_verdict -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"
8b0b5bb4
test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (tests.unit.test_verdict.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) ... ok
test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto (tests.unit.test_verdict.VerdictTest.test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto) ... ok
test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure (tests.unit.test_verdict.VerdictTest.test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure) ... ok
test_verdict_condition_1_is_a_warning_under_precheck_required_0 (tests.unit.test_verdict.VerdictTest.test_verdict_condition_1_is_a_warning_under_precheck_required_0) ... ok
test_verdict_condition_4_preserves_complete_item_identity_and_multiplicity (tests.unit.test_verdict.VerdictTest.test_verdict_condition_4_preserves_complete_item_identity_and_multiplicity) ... ok
test_verdict_condition_4_rejects_an_undispositioned_status_with_a_null_url (tests.unit.test_verdict.VerdictTest.test_verdict_condition_4_rejects_an_undispositioned_status_with_a_null_url) ... ok
test_verdict_condition_4_requires_saved_and_fresh_heads_to_equal_the_accepted_head (tests.unit.test_verdict.VerdictTest.test_verdict_condition_4_requires_saved_and_fresh_heads_to_equal_the_accepted_head) ... ok
test_verdict_condition_4_uses_the_existing_disposition_and_commit_validators (tests.unit.test_verdict.VerdictTest.test_verdict_condition_4_uses_the_existing_disposition_and_commit_validators) ... ok
test_verdict_condition_5_honors_the_latest_amended_caps (tests.unit.test_verdict.VerdictTest.test_verdict_condition_5_honors_the_latest_amended_caps) ... ok
test_verdict_counts_open_p0_p1_findings_even_when_the_id_is_empty (tests.unit.test_verdict.VerdictTest.test_verdict_counts_open_p0_p1_findings_even_when_the_id_is_empty) ... ok
test_verdict_holds_on_a_missing_or_schema_failing_input (tests.unit.test_verdict.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input) ... ok
test_verdict_loop_refreshes_the_trusted_checkout_after_a_merge (tests.unit.test_verdict.VerdictTest.test_verdict_loop_refreshes_the_trusted_checkout_after_a_merge) ... ok
test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold (tests.unit.test_verdict.VerdictTest.test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold) ... ok
test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout (tests.unit.test_verdict.VerdictTest.test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout) ... ok
test_verdict_reads_the_record_front_matter_offline_and_holds_when_pyyaml_is_unavailable (tests.unit.test_verdict.VerdictTest.test_verdict_reads_the_record_front_matter_offline_and_holds_when_pyyaml_is_unavailable) ... ok
test_verdict_shadow_appends_the_machine_column_only (tests.unit.test_verdict.VerdictTest.test_verdict_shadow_appends_the_machine_column_only) ... ok
test_verdict_validate_refuses_each_rule_the_moved_schema_checker_holds (tests.unit.test_verdict.VerdictTest.test_verdict_validate_refuses_each_rule_the_moved_schema_checker_holds) ... ok
Ran 17 tests in 260.962s
OK
[exit 0]
```
## 6. The schema checker moved from b8998de1 orch-audit.sh into verdict.sh: both agree, exit status and message, on 35 cases (the comparison script, then its run)
```console
$ cat "$TMPDIR/chk-equiv.py"; uv run --no-project python -I "$TMPDIR/chk-equiv.py"
# The inherited checker (b8998de1 orch-audit.sh, 2-argument mode) and verdict.sh's must agree on every case.
import itertools, json, os, re, subprocess, sys, tempfile
def body(text, start):
    return text.split(start, 1)[1].split("\nPY\n", 1)[0]
old = body(subprocess.run(["git", "show", "b8998de1:scripts/orchestrator/orch-audit.sh"], capture_output=True, text=True).stdout, "read -r -d '' checker << 'PY' || true\n")
new = body(open("scripts/orchestrator/verdict.sh").read(), "read -r -d '' checker << 'PY' || true # <schema> <json>: the stdlib subset of JSON Schema 2020-12 .schemas/ uses\n")
d = tempfile.mkdtemp()
def run(code, schema, doc):
    sp, dp = os.path.join(d, "s.json"), os.path.join(d, "d.json")
    json.dump(schema, open(sp, "w")); open(dp, "w").write(doc if isinstance(doc, str) else json.dumps(doc))
    r = subprocess.run([sys.executable, "-I", "-c", code, sp, dp], capture_output=True, text=True)
    return r.returncode, r.stderr.strip()
audit, verdict = (json.load(open(f".schemas/{n}.json")) for n in ("audit", "verdict"))
H, A = "a" * 40, "2026-10-18T05:00:00Z"
good = {"head": H, "task_id": "t1-a01", "auditor": "c", "generated_at": A, "verdict": "correct", "findings": []}
f = {"id": "1", "priority": "P2", "confidence": "high", "file": "x", "line": 1, "class": "records-form", "scope": "code", "rationale": "r"}
cases = [(audit, good), (audit, good | {"findings": [f]}), (audit, good | {"findings": [f | {"status": "fixed"}]})]
for k, bad in [("head", "A" * 40), ("head", H + "\n"), ("head", 1), ("task_id", "-x"), ("generated_at", "2026-10-18"), ("generated_at", "2026-10-18T05:00:00"),
               ("generated_at", "2026-02-30T05:00:00Z"), ("generated_at", "2026-10-18T05:00:00.123+09:00"), ("verdict", "ok"), ("findings", {}), ("extra", 1)]:
    cases.append((audit, good | {k: bad}))
for k, bad in [("line", 0), ("line", True), ("line", 1.5), ("class", "no-such"), ("scope", "x"), ("rationale", "r" * 401), ("status", "open"), ("x", 1)]:
    cases.append((audit, good | {"findings": [f | {k: bad}]}))
cases += [(audit, {k: v for k, v in good.items() if k != "auditor"}), (audit, "not json"), (audit, "[]"), (audit, "null")]
vg = {"verdict": "accept", "pr": 1, "head": H, "task_id": "t", "conditions": [{"id": 1, "ok": True, "evidence": "e"}], "inputs_sha256": {"a": "0" * 64}, "generated_at": A}
cases += [(verdict, vg), (verdict, vg | {"pr": 0}), (verdict, vg | {"conditions": [{"id": 10, "ok": True, "evidence": "e"}]}), (verdict, vg | {"inputs_sha256": {"a": "x"}}),
          (verdict, vg | {"revise_line": "AGMSG-ACCEPTANCE v1 x"}), (verdict, vg | {"revise_line": "x"}), (verdict, vg | {"conditions": [{"id": 1, "ok": 1, "evidence": "e"}]})]
cases += [({"format": "date-time"}, 5), ({"format": "date-time"}, "x")]  # format without a type: non-strings skip it
bad = [(s, d_, run(old, s, d_), run(new, s, d_)) for s, d_ in cases if run(old, s, d_) != run(new, s, d_)]
print(f"{len(cases)} cases, {len(bad)} disagreements")
for s, d_, o, n in bad: print(json.dumps(d_)[:100], o, n)
35 cases, 0 disagreements
[exit 0]
```
## 6a. The worker review P2: each one-rule mutant of the moved checker (and a --validate that exits 0) fails test_verdict_validate_refuses_each_rule_the_moved_schema_checker_holds, in a scratch worktree at HEAD (the mutant script, then its run)
```console
$ cat "$TMPDIR/mut-v03.py"; uv run --no-project python -I "$TMPDIR/mut-v03.py" "$Q"
# Each mutant deletes one rule of verdict.sh's schema checker (or the --validate entry); the per-rule test must fail.
import shutil, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); src = (root / "scripts/orchestrator/verdict.sh").read_text()
M = {
    "date-time": ('s.get("format") != "date-time" or', 'True or'),
    "additionalProperties": ('if sub is False or isinstance', 'if isinstance'),
    "required": ('return f"{at} lacks {k}"', 'pass'),
    "anchoring": ('p[:-1] + r"\\Z" if p.endswith("$") else p', 'p'),
    "min/max": ('return f"{at} is out of range"', 'pass'),
    "enum": ('return f"{at} {v!r} is not in the enum"', 'pass'),
    "type": ('return f"{at} is not {t}"', 'pass'),
    "maxLength": ('return f"{at} is longer than {s[\'maxLength\']}"', 'pass'),
    "bool-as-integer": (' or isinstance(v, bool) and t == "integer"', ''),
    "--validate exit 0": ('exec "${VERDICT_BIN}/python3" -I -c "${checker}" "$2" "$3"; fi', 'exit 0; fi'),
}
test = "tests.unit.test_verdict.VerdictTest.test_verdict_validate_refuses_each_rule_the_moved_schema_checker_holds"
for name, (a, b) in M.items():
    assert src.count(a) == 1, name
    (root / "scripts/orchestrator/verdict.sh").write_text(src.replace(a, b))
    r = subprocess.run(["uv", "run", "python", "-m", "unittest", test], cwd=root, capture_output=True, text=True)
    print(f"{name}: {'killed' if r.returncode else 'SURVIVED'}")
(root / "scripts/orchestrator/verdict.sh").write_text(src)
date-time: killed
additionalProperties: killed
required: killed
anchoring: killed
min/max: killed
enum: killed
type: killed
maxLength: killed
bool-as-integer: killed
--validate exit 0: killed
[exit 0]
```
## 7. The schemas: parsed content equal to b8998de1 (whitespace-only reformatting), and their line counts
```console
$ for n in audit verdict; do git show "$OLD:.schemas/$n.json" > "$TMPDIR/old-$n.json"; uv run --no-project python -I -c "import json, sys; print(sys.argv[3], json.load(open(sys.argv[1])) == json.load(open(sys.argv[2])))" "$TMPDIR/old-$n.json" ".schemas/$n.json" "$n parsed-equal:"; done; wc -l .schemas/audit.json .schemas/verdict.json scripts/orchestrator/verdict.sh
audit parsed-equal: True
verdict parsed-equal: True
      13 .schemas/audit.json
      12 .schemas/verdict.json
     273 scripts/orchestrator/verdict.sh
     298 total
[exit 0]
```
## 8. The Check script commands: shellcheck and shfmt on verdict.sh, make format, make render-check
```console
$ shellcheck scripts/orchestrator/verdict.sh && echo "shellcheck clean"; shfmt -i 4 -sr -d scripts/orchestrator/verdict.sh && echo "shfmt clean"; make format > "$TMPDIR/v03-format.txt" 2>&1; echo "make format exit $?"; tail -n 3 "$TMPDIR/v03-format.txt"; make render-check 2>&1 | tail -n 3; echo "make render-check exit ${PIPESTATUS[0]}"
shellcheck clean
shfmt clean
make format exit 2
     }
 
make: *** [format] Error 1
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
make render-check exit 0
[exit 0]
```
## 8a. make format flags the same files at the merge-base 3e41e36a (scratch worktree) as at HEAD, and none of this PR's; shfmt v3.14.1
```console
$ for each checkout: make format; echo exit; the files its diff names
8b0b5bb4: make format exit 2; flagged: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh home/dot_claude/hooks/executable_project-map-reload.sh tests/install/macos/common/brew.bats 
3e41e36a: make format exit 2; flagged: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh home/dot_claude/hooks/executable_project-map-reload.sh tests/install/macos/common/brew.bats 
[exit 0]
```
## 9a. make unit-test on a scratch worktree at the merge-base 3e41e36a (the unchanged base), same sandbox
```console
$ cd "$B" && make unit-test > "$TMPDIR/v03-unit-base.txt" 2>&1; summary
make exit 2
Ran 1207 tests in 2300.771s
FAILED (failures=195, errors=111, skipped=2)
  28 test_agent_stop_gate
   2 test_aws_cli_acquisition
   5 test_gh_auth
  87 test_herdr_agents
 136 test_require_crit_review
   8 test_runtime_health
   4 test_supply_chain_policy
  19 test_ua_symbol_coverage
  17 test_update_agent_assets
[exit 0]
```
## 9b. make unit-test at the code head 8b0b5bb4, same sandbox
```console
$ make unit-test > "$TMPDIR/v03-unit-head.txt" 2>&1; summary
make exit 2
Ran 1224 tests in 1216.156s
FAILED (failures=195, errors=111, skipped=2)
  28 test_agent_stop_gate
   1 test_agmsg_dispatch
   2 test_aws_cli_acquisition
   5 test_gh_auth
  86 test_herdr_agents
 136 test_require_crit_review
   8 test_runtime_health
   4 test_supply_chain_policy
  19 test_ua_symbol_coverage
  17 test_update_agent_assets
[exit 0]
```
## 9c. make unit-test at the code head with commit signing off and init.defaultBranch=main (git config environment variables)
```console
$ GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false GIT_CONFIG_KEY_1=init.defaultBranch GIT_CONFIG_VALUE_1=main make unit-test > "$TMPDIR/v03-unit-head-env.txt" 2>&1; summary
make exit 2
Ran 1224 tests in 963.567s
FAILED (failures=91, errors=10, skipped=2)
  28 test_agent_stop_gate
   2 test_aws_cli_acquisition
   5 test_gh_auth
  37 test_herdr_agents
   8 test_runtime_health
   4 test_supply_chain_policy
  17 test_update_agent_assets
[exit 0]
```
## 9d. The two runs differ only in two timing tests (one each, same totals); each passes alone at the head
```console
$ comm -3 of the failing test lists of 9a and 9b; then each differing test alone at HEAD
base only: FAIL: test_session_start_attach_bounds_a_trickling_hook_payload (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_bounds_a_trickling_hook_payload)
head only: FAIL: test_timeout_is_one_shared_budget (test_agmsg_dispatch.AgmsgDispatchTest.test_timeout_is_one_shared_budget)
OK
OK
[exit 0]
```
## 10. Caps over origin/main...HEAD (git diff --numstat; additions plus deletions)
```console
$ B=$(git merge-base origin/main HEAD); echo "merge-base ${B:0:8}"; git diff --numstat "$B...HEAD" -- . ":!.orchestration"; git diff --numstat "$B...HEAD" | awk -F "\t" "\$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^tests\\// {t += \$1 + \$2; next} {o += \$1 + \$2} END {printf \"outside tests/ and .orchestration/: %d of 300\nunder tests/: %d of 400\n\", o, t}"; echo "verdict.sh alone: $(wc -l < scripts/orchestrator/verdict.sh) of 300 lines"
merge-base 3e41e36a
13	0	.schemas/audit.json
12	0	.schemas/verdict.json
273	0	scripts/orchestrator/verdict.sh
393	0	tests/unit/test_verdict.py
outside tests/ and .orchestration/: 298 of 300
under tests/: 393 of 400
verdict.sh alone:      273 of 300 lines
[exit 0]
```
## 11. The Check's shadow invocation at 8b0b5bb4, PR #410's head then (outside the sandbox: its re-exec reaches gh)
```console
$ git rev-parse HEAD; gh pr view 410 --json headRefOid --jq .headRefOid
8b0b5bb42b41e3a32344744a362f1c9fc99f2e35
8b0b5bb42b41e3a32344744a362f1c9fc99f2e35
$ scripts/orchestrator/verdict.sh --shadow 410 --task dotfiles-T133-verdict-audit-pool-a03; echo "exit $?"
verdict: hold: the record .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md is not this task's at the head; .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-audit-8b0b5bb.json is missing or fails .schemas/audit.json; the fresh sweep, .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-pr-feedback.json or the merge base; the task file .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md or the merge-base diff
verdict: hold .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-verdict-8b0b5bb.json
exit 20
$ jq . .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-verdict-8b0b5bb.json; tail -n 1 .orchestration/validation/verdict-shadow.tsv
{
  "verdict": "hold",
  "pr": 410,
  "head": "8b0b5bb42b41e3a32344744a362f1c9fc99f2e35",
  "task_id": "dotfiles-T133-verdict-audit-pool-a03",
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
      "evidence": "no valid audit .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-audit-8b0b5bb.json"
    },
    {
      "id": 4,
      "ok": false,
      "evidence": "no fresh sweep, no .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-pr-feedback.json or no merge base"
    },
    {
      "id": 5,
      "ok": false,
      "evidence": "no readable front matter in .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md or no merge-base diff"
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
  "inputs_sha256": {},
  "generated_at": "2026-10-19T02:12:02Z"
}
410	8b0b5bb42b41e3a32344744a362f1c9fc99f2e35	hold			2026-10-19T02:12:02Z
[exit 0]
```

# Revise 1 (AGMSG-ACCEPTANCE status=revise, 2026-10-19T05:34:59Z; previous head 513e5d05, the orchestrator's update-branch head)

- Every block below ran inside the sandbox from this worktree at the revise's code head `cac07914`. The only later commit is this records commit.
- Red runs at `513e5d05` with this head's test file (R2). Green, the mutants, the lint, the inventory and the caps run at the code head (R3 to R7).
- §1 to §11 above stay as the reset round's evidence at `8b0b5bb4`.

## R1. Revise 1: the branch, origin/main and this round's commits on the update-branch head 513e5d05
```console
$ git branch --show-current; git rev-parse HEAD origin/main; git log --oneline $PREV..HEAD
tools/verdict-audit-pool-a01
cac0791494cd7765187ba3c99f12ff377f9adffb
205fe85c19c03750fe3551bb96e084e9f0a676b6
cac07914 chore(orchestration): the a01 and a02 record directories leave PR 410's tree; the orchestrator keeps the records (T133 verdict-audit-pool a03, revise 1)
32e4d2fb fix(orchestrator): verdict unsets inherited functions, honours a pinned state only as it builds one and never resolves through a caller's VERDICT_BIN; condition 4 holds while scripts/__pycache__ exists (T133 verdict-audit-pool a03, revise 1)
a19a0eba test(orchestrator): a caller's bin holding a copied, not linked, tool is not a pinned state (T133 verdict-audit-pool a03, revise 1)
51abdb1c test(orchestrator): verdict ignores a caller's bin and PATH overrides and never imports cached bytecode; the module compacted to its cap with every case kept (T133 verdict-audit-pool a03, revise 1)
[exit 0]
```
## R2. RED at 513e5d05 (its verdict.sh), with this head's test file, in a scratch worktree: the two checks of the revise
```console
$ git -C "$R" rev-parse --short=8 HEAD; git show HEAD:tests/unit/test_verdict.py > "$R/tests/unit/test_verdict.py"; cd "$R" && uv run python -m unittest $REV 2>&1 | /usr/bin/grep -E "^(FAIL|ERROR):|^AssertionError|^Ran|^(OK|FAILED)" | sed -E "s/ \(tests\.unit\.test_verdict\.VerdictTest\.[a-z0-9_]+\)//" | cut -c1-200
513e5d05
FAIL: test_verdict_ignores_caller_bin_and_path_overrides (case='function')
AssertionError: Tuples differ: (0, False) != (20, True)
FAIL: test_verdict_ignores_caller_bin_and_path_overrides (case='variable')
AssertionError: Tuples differ: (20, False) != (0, True)
FAIL: test_verdict_ignores_caller_bin_and_path_overrides (case='copy')
AssertionError: Tuples differ: (20, False) != (0, True)
FAIL: test_verdict_never_imports_cached_bytecode
AssertionError: Tuples differ: (20, False) != (20, True)
Ran 2 tests in 6.765s
FAILED (failures=4)
[exit 0]
```
## R3. GREEN at the code head: the whole verdict module, verbose (the 17 tests of the reset, every one kept through the compaction, and the two checks)
```console
$ git rev-parse --short=8 HEAD; uv run python -m unittest tests.unit.test_verdict -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"
cac07914
test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds (tests.unit.test_verdict.VerdictTest.test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds) ... ok
test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto (tests.unit.test_verdict.VerdictTest.test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto) ... ok
test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure (tests.unit.test_verdict.VerdictTest.test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure) ... ok
test_verdict_condition_1_is_a_warning_under_precheck_required_0 (tests.unit.test_verdict.VerdictTest.test_verdict_condition_1_is_a_warning_under_precheck_required_0) ... ok
test_verdict_condition_4_preserves_complete_item_identity_and_multiplicity (tests.unit.test_verdict.VerdictTest.test_verdict_condition_4_preserves_complete_item_identity_and_multiplicity) ... ok
test_verdict_condition_4_rejects_an_undispositioned_status_with_a_null_url (tests.unit.test_verdict.VerdictTest.test_verdict_condition_4_rejects_an_undispositioned_status_with_a_null_url) ... ok
test_verdict_condition_4_requires_saved_and_fresh_heads_to_equal_the_accepted_head (tests.unit.test_verdict.VerdictTest.test_verdict_condition_4_requires_saved_and_fresh_heads_to_equal_the_accepted_head) ... ok
test_verdict_condition_4_uses_the_existing_disposition_and_commit_validators (tests.unit.test_verdict.VerdictTest.test_verdict_condition_4_uses_the_existing_disposition_and_commit_validators) ... ok
test_verdict_condition_5_honors_the_latest_amended_caps (tests.unit.test_verdict.VerdictTest.test_verdict_condition_5_honors_the_latest_amended_caps) ... ok
test_verdict_counts_open_p0_p1_findings_even_when_the_id_is_empty (tests.unit.test_verdict.VerdictTest.test_verdict_counts_open_p0_p1_findings_even_when_the_id_is_empty) ... ok
test_verdict_holds_on_a_missing_or_schema_failing_input (tests.unit.test_verdict.VerdictTest.test_verdict_holds_on_a_missing_or_schema_failing_input) ... ok
test_verdict_ignores_caller_bin_and_path_overrides (tests.unit.test_verdict.VerdictTest.test_verdict_ignores_caller_bin_and_path_overrides) ... ok
test_verdict_loop_refreshes_the_trusted_checkout_after_a_merge (tests.unit.test_verdict.VerdictTest.test_verdict_loop_refreshes_the_trusted_checkout_after_a_merge) ... ok
test_verdict_never_imports_cached_bytecode (tests.unit.test_verdict.VerdictTest.test_verdict_never_imports_cached_bytecode) ... ok
test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold (tests.unit.test_verdict.VerdictTest.test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold) ... ok
test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout (tests.unit.test_verdict.VerdictTest.test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout) ... ok
test_verdict_reads_the_record_front_matter_offline_and_holds_when_pyyaml_is_unavailable (tests.unit.test_verdict.VerdictTest.test_verdict_reads_the_record_front_matter_offline_and_holds_when_pyyaml_is_unavailable) ... ok
test_verdict_shadow_appends_the_machine_column_only (tests.unit.test_verdict.VerdictTest.test_verdict_shadow_appends_the_machine_column_only) ... ok
test_verdict_validate_refuses_each_rule_the_moved_schema_checker_holds (tests.unit.test_verdict.VerdictTest.test_verdict_validate_refuses_each_rule_the_moved_schema_checker_holds) ... ok
Ran 19 tests in 148.263s
OK
[exit 0]
```
## R4. Each control of the revise is load-bearing: one mutant per control fails a check, in a scratch worktree at HEAD (the mutant script, then its run)
```console
$ cat "$TMPDIR/mut-v03r.py"; uv run --no-project python -I "$TMPDIR/mut-v03r.py" "$Q"
# Each mutant removes one control of the revise; one of the two revise tests must fail on every one.
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); f = root / "scripts/orchestrator/verdict.sh"; src = f.read_text()
M = {
    "inherited functions kept": ('for f in $(compgen -A function); do unset -f "${f}"; done', ':'),
    "any exported name accepted": ('|| pinned=no; done\nfor t in', '|| :; done\nfor t in'),
    "a tool that is no link accepted": ('/shims/ ]] || pinned=no; done', '/shims/ ]] || :; done'),
    "the caller's bin searched": ('|| search+="${search:+:}${d}"; done', '|| :; done; search=${PATH}'),
    "scripts/__pycache__ allowed": (' && ! -e scripts/__pycache__ ]]', ' ]]'),
}
tests = ["tests.unit.test_verdict.VerdictTest.test_verdict_ignores_caller_bin_and_path_overrides",
         "tests.unit.test_verdict.VerdictTest.test_verdict_never_imports_cached_bytecode"]
for name, (a, b) in M.items():
    assert src.count(a) == 1, name
    f.write_text(src.replace(a, b))
    r = subprocess.run(["uv", "run", "python", "-m", "unittest", *tests], cwd=root, capture_output=True, text=True)
    print(f"{name}: {'killed' if r.returncode else 'SURVIVED'}")
f.write_text(src)
inherited functions kept: killed
any exported name accepted: killed
a tool that is no link accepted: killed
the caller's bin searched: killed
scripts/__pycache__ allowed: killed
[exit 0]
```
## R5. shellcheck and shfmt on verdict.sh; ruff format on the test; the schemas parsed-equal to b8998de1
```console
$ shellcheck scripts/orchestrator/verdict.sh && echo "shellcheck clean"; shfmt -i 4 -sr -d scripts/orchestrator/verdict.sh && echo "shfmt clean"; ruff format --config ruff.toml --check tests/unit/test_verdict.py; for n in audit verdict; do git show "b8998de1:.schemas/$n.json" > "$TMPDIR/old-$n.json"; uv run --no-project python -I -c "import json, sys; print(sys.argv[3], json.load(open(sys.argv[1])) == json.load(open(sys.argv[2])))" "$TMPDIR/old-$n.json" ".schemas/$n.json" "$n parsed-equal:"; done
shellcheck clean
shfmt clean
1 file already formatted
audit parsed-equal: True
verdict parsed-equal: True
[exit 0]
```
## R6. Item 3: the cumulative inventory is this task's allowed files and its own records; the a01 and a02 directories are gone
```console
$ git diff --name-only origin/main...HEAD; for d in a01 a02; do [ -z "$(git ls-files .orchestration/dotfiles-T133-verdict-audit-pool-$d)" ] && echo "absent at HEAD: .orchestration/dotfiles-T133-verdict-audit-pool-$d/"; done
.orchestration/dotfiles-T133-verdict-audit-pool-a03/dotfiles-T133-verdict-audit-pool-a03-worker-crit.json
.orchestration/dotfiles-T133-verdict-audit-pool-a03/dotfiles-T133-verdict-audit-pool-a03-worker-review-receipt.md
.orchestration/dotfiles-T133-verdict-audit-pool-a03/learning.md
.orchestration/dotfiles-T133-verdict-audit-pool-a03/report.md
.orchestration/dotfiles-T133-verdict-audit-pool-a03/revise.yaml
.orchestration/dotfiles-T133-verdict-audit-pool-a03/sandbox.md
.orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md
.orchestration/dotfiles-T133-verdict-audit-pool-a03/validation.md
.schemas/audit.json
.schemas/verdict.json
scripts/orchestrator/verdict.sh
tests/unit/test_verdict.py
absent at HEAD: .orchestration/dotfiles-T133-verdict-audit-pool-a01/
absent at HEAD: .orchestration/dotfiles-T133-verdict-audit-pool-a02/
[exit 0]
```
## R7. Caps over origin/main...HEAD (additions plus deletions)
```console
$ B=$(git merge-base origin/main HEAD); echo "merge-base ${B:0:8}"; git diff --numstat "$B...HEAD" -- . ":!.orchestration"; git diff --numstat "$B...HEAD" | awk -F "\t" "\$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^tests\\// {t += \$1 + \$2; next} {o += \$1 + \$2} END {printf \"outside tests/ and .orchestration/: %d of 300\nunder tests/: %d of 400\n\", o, t}"; echo "verdict.sh alone: $(wc -l < scripts/orchestrator/verdict.sh) of 300 lines"; wc -l .schemas/audit.json .schemas/verdict.json
merge-base b22a5580
11	0	.schemas/audit.json
10	0	.schemas/verdict.json
278	0	scripts/orchestrator/verdict.sh
399	0	tests/unit/test_verdict.py
outside tests/ and .orchestration/: 299 of 300
under tests/: 399 of 400
verdict.sh alone:      278 of 300 lines
      11 .schemas/audit.json
      10 .schemas/verdict.json
      21 total
[exit 0]
```
