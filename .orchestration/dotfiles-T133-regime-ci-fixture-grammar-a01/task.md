---
format: 2
task_id: dotfiles-T133-regime-ci-fixture-grammar-a01
kind: code
security: false
allowed_files:
  - tests/unit/test_regime_ci.py
  - .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/**
after: []
threat_table:
  - control: the PR edits tests/unit/test_regime_ci.py only in the five fixture rows named in item 1
    disposition: "residual: the diff is the five `disposition:` strings and nothing else; the task-level audit from main compares the diff against item 1"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
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
  - claim: "tests/unit/test_regime_ci.py builds its fixture rows with a bare `disposition: residual` in five places; the checker on main accepts both the bare form and the `residual: <sentence>` form, while the a05-checker text (PR #417) requires the latter (C13), so the a05 PR's full unit suite is red on this module until the fixtures migrate"
    command: |-
      /usr/bin/grep -nE 'disposition: residual' tests/unit/test_regime_ci.py
    output: |-
      27:    f"  - control: {name}\n    disposition: residual\n"
      127:        rows = "".join(f"  - control: the PR edits {path}\n    disposition: residual\n" for path in scripts)
      276:        no_row = TASK.replace("  - control: the PR edits src/tool.sh\n    disposition: residual\n", "")
      372:        rows = f"  - control: the predecessor copy .orchestration/{T}/task.md\n    disposition: residual\n"
      373:        rows += f"  - control: the task copy .orchestration/{later}/task.md\n    disposition: residual\n"
---

# AGMSG-TASK dotfiles-T133-regime-ci-fixture-grammar-a01 — the regime-ci test fixtures use the disposition grammar

Written 2026-10-20 by the orchestrator seat after worker a012 (PR #417, dotfiles-T133-task-generator-plan-check-a05-checker) blocked on `tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier`, which fails under the a05 checker's C13 rule (`regime-ci-t1-a01-checker-C13-disposition-is-not-closed:-residual:-or-out-of-scope:-and-a-space`) because the module's fixtures write bare `disposition: residual` rows; that file is outside #417's allowed_files and its amendments are spent (INV-6 S2), so the migration is this test-only task. Design 5.14 applies by reference (D-024-30); this task touches no trust boundary.

## Item 1

In `tests/unit/test_regime_ci.py`, each of the five fixture rows in the premise (lines 27, 127, 276, 372, 373) changes from `disposition: residual` to `disposition: "residual: <one sentence naming the control>"` (the task-consistency checker's grammar: a disposition starts with `closed:`, `residual:` or `out-of-scope:` followed by a space). The replacement at line 276 keeps `no_row` removing exactly the `src/tool.sh` row that the `ROWS` constant at line 27 writes, so the assertion it serves still holds. The five rows may share one module-level constant holding that sentence (an f-string at line 276 then), which keeps the module within the cap and ruff-format's 120-column line length; otherwise nothing in the module changes: no test logic, no new test, no renamed test. The migration is forward-compatible: the module stays green on main's checker before and after the change, which is the task's red-and-green evidence (paste the module's run before and after), and PR #417's CI goes green on this module after it takes the new base (the orchestrator update-branches it; this task does not touch #417).

## Check

Run the module directly under the trusted interpreter from the checkout root, before and after the change, and paste both runs into validation.md: `/usr/bin/env -i PATH="$(dirname "$(command -v uv)"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py` (the module ends with `unittest.main()`; no discovery; it shells out to `uv run --with pyyaml python -I` as regime.yml does, so uv's directory stays on PATH, and it creates temporary git repositories, so TMPDIR stays set: measured by a009 on unmodified main inside its sandbox, 16 tests OK, 2026-10-20T04:40Z). Caps: 0 changed lines outside `tests/` and `.orchestration/`; at most 12 changed lines under `tests/`, measured with `git diff --numstat <base40>...<head40>` where `<base40>` is the branch point pasted at dispatch and `<head40>` the RESULT head. Do not run Bats locally; after pushing, verify final-head GitHub Actions and fix in-scope failures before RESULT. This whole task text must remain at or under 90 lines.

## Completion

A fresh branch `tools/regime-ci-fixture-grammar-a01` from `origin/main`; the task copy at `.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md` byte-identical to the dispatched file; report.md names the five rows and both module runs; push with the HTTPS form (`GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push -u https://github.com/mryfmo/dotfiles.git <branch>`); open the PR with `gh pr create --repo mryfmo/dotfiles`; then `AGMSG-RESULT v1 task_id=dotfiles-T133-regime-ci-fixture-grammar-a01 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256 of the task copy>`. Worker Playbook step 4: every command inside the sandbox; any other action is reported as `AGMSG-PONG v1 status=blocked`, never performed.

## Checks (pasted by the orchestrator before each send)

```
pasted 2026-10-20T04:47Z before send 2 (amendment 1, answering a009's question of 04:40:30Z) to a009: the Check command keeps uv's directory on PATH and TMPDIR set (a009 measured 16/16 OK on unmodified main; the orchestrator's own first command was written without execution: C-100 instance, recorded); one shared module constant for the sentence is allowed (11 changed lines measured by a009; the cap of 12 stays); the `src/tool.sh` row comes from line 27's ROWS, not line 127; previous_sha256 2fc20d2392dc7f45df100f314258ecf0ddd9e9f0310e9b2a2f8bac286ce5081d; task-consistency-check.py OK; SECRET_PATTERN 0; home paths 0
branch point for the caps: origin/main 60a6fb2b324d0381c4a6e539b37c650105154a7e at dispatch; task SHA256 in the AGMSG-TASK line; the read marker is recorded in the acceptance record
```
