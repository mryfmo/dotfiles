---
format: 2
task_id: dotfiles-T133-regime-ci-fixture-grammar-a02
kind: code
security: false
reset_of: [dotfiles-T133-regime-ci-fixture-grammar-a01]
allowed_files:
  - tests/unit/test_regime_ci.py
  - .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/**
after: []
threat_table:
  - control: the PR edits tests/unit/test_regime_ci.py only in the five fixture rows named in item 1 and their shared constant
    disposition: "residual: the inherited replacements and RESIDUAL constant stay unchanged from 15bc046e; the task-level audit compares the implementation against that commit"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/task.md)
    disposition: "residual: byte-identical to the dispatched file whose sha256 is in the TASK line; the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; sandbox.md lists each command as inside or excluded and records refusals; the audit reads them"
  - control: predecessor copy .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md
    disposition: "residual: retained unchanged on the branch from cd47e1b0; the orchestrator compares its bytes at acceptance"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the test module runs the base's verifier and checker on fixtures in temporary directories; nothing live changes"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the module runs as today under the trusted interpreter"
  - control: new or renamed scripts
    disposition: "residual: none; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: |-
      PR #441's inherited head cd47e1b0 has 11 changed lines under tests/ against branch point 60a6fb2b; the reset preserves this implementation.
    command: |-
      git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2 -- tests/unit/test_regime_ci.py
    output: |-
      6	5	tests/unit/test_regime_ci.py
---

# AGMSG-TASK dotfiles-T133-regime-ci-fixture-grammar-a02 — reset the fixture-grammar task

This text is the reset after INV-6 S2 (two orchestrator-text amendments and two questions), written by a review-profile context other than the a01 author; the a01 findings history lives in `.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md`. Design 5.14 applies by reference (D-024-30); this remains test-only and touches no trust boundary.

## Item 1

Continue PR #441 (`https://github.com/mryfmo/dotfiles/pull/441`) on its existing branch `tools/regime-ci-fixture-grammar-a01`, from head `cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2`, in a009's worker-c checkout. Keep the implementation from `15bc046ef0bc50476879e92cfaa42e5952f6878b` unchanged: the five fixture rows originally at lines 27, 127, 276, 372 and 373 of `tests/unit/test_regime_ci.py` read the module-level `RESIDUAL` constant containing the quoted `residual: <sentence>` disposition; `no_row` still removes exactly the `src/tool.sh` row written by `ROWS`. No test logic, tests or test names change.

The worker only adds `.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/task.md` and its `report.md`, `validation.md`, `sandbox.md`, and `learning.md`. The task copy is byte-identical to the dispatched text, including the orchestrator's pasted Checks. Preserve all a01 files unchanged, including its task copy; do not recreate the branch, open another PR, or edit the implementation.

## Check

Keep the a01 before-and-after evidence (16/16 OK), and run this measured module command once more on the final head from the checkout root, pasting the command and full output into validation.md: `/usr/bin/env -i PATH="$(dirname "$(command -v uv)"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py`. The module ends with `unittest.main()`; no discovery. Its subprocess needs uv's directory on PATH, TMPDIR for temporary repositories, and the three proxy variables for the pyyaml fetch. This form measured 16 tests OK inside the sandbox for a009 at 04:48Z and for the orchestrator at 04:51:17Z on 2026-10-20 (`Ran 16 tests in 50.784s`, `OK`).

Caps: 0 changed lines outside `tests/` and `.orchestration/`; at most 12 changed lines under `tests/` (already met: 11). Measure and paste `git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...<head40>`, replacing `<head40>` with the RESULT head. Also paste the comparison proving no implementation or a01 record changed from cd47e1b0. Do not run Bats locally. After pushing, verify GitHub Actions on the final head and record their results before RESULT; a failure requiring implementation changes is a blocked PONG.

## Completion

report.md names the five inherited fixture rows, unchanged implementation, prior before-and-after evidence, final module run, caps, final-head CI, and task-copy sha256. validation.md contains the pasted checks; sandbox.md lists each command individually with `inside` or `excluded`, including refused commands and their boundary; learning.md records reusable learning or explicitly states none. Record the cost if exposed, otherwise `cost: n/a`.

Commit only the five a02 additions and push with `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles.git HEAD:tools/regime-ci-fixture-grammar-a01`; the shared Git configuration is read-only for the seat, so do not set upstream configuration.

Worker Playbook step 4 for this task: every command runs inside the sandbox except the agmsg delivery send (`send.sh`/the Stop-hook delivery), which the current Claude worker configuration routes through the documented exclusion until P1-15 (`dotfiles-T133-worker-write-boundary-a03`) lands; any other action outside the sandbox is reported as `AGMSG-PONG v1 status=blocked` with the exact command and boundary, never performed.

Send `AGMSG-RESULT v1 task_id=dotfiles-T133-regime-ci-fixture-grammar-a02 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` with PR #441's URL, the pushed final head, and the sha256 of the a02 task copy.

## Checks (pasted by the orchestrator before each send)

```
pasted 2026-10-20T06:40Z before send 1 to a009 (Claude, worker-c): reset of dotfiles-T133-regime-ci-fixture-grammar-a01 after INV-6 S2 by two orchestrator-text amendments (a01 counters: task=dotfiles-T133-regime-ci-fixture-grammar-a01 tasks=3 amendments=2 questions=2 results=2 withdrawn=0 revises=1 first_result_head=e51fee5b29ad97e4f2c5ed20ba3bffcc1ffd9c38 bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-20T04); audit cd47e1b: no code finding, P2 orchestration (S2), P2 conformance (the agmsg send exclusion unstated), P3 (push -u); text by the review profile; task-consistency-check.py OK; SECRET_PATTERN 0; home paths 0; 74 lines
PR #441 continues on tools/regime-ci-fixture-grammar-a01 from head cd47e1b0 with the implementation 15bc046e unchanged; the worker adds the a02 task copy and records only; the a01 copy stays; push without -u; CI read by the orchestrator; task SHA256 in the AGMSG-TASK line, computed over these final bytes
```
