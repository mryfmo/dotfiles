---
format: 2
task_id: dotfiles-T128-update-bootstrap-canonical-a01
kind: code
security: false
reset_of: []
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - Makefile
  - tests/unit/test_supply_chain_policy.py
  - .orchestration/dotfiles-T128-update-bootstrap-canonical-a01/**
after: []
threat_table:
  - control: the PR edits Makefile, whose update target runs on the operator's machine in the canonical clone
    disposition: "closed: tests/unit/test_supply_chain_policy.py::test_update_skips_agmsg_bootstrap_in_the_canonical_clone"
  - control: the PR edits tests/unit/test_supply_chain_policy.py, the oracle of its own change
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test beside the Makefile diff"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-update-bootstrap-canonical-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared at acceptance)"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: the branch evidence records under .orchestration/dotfiles-T128-update-bootstrap-canonical-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: the worker's untrusted claims; acceptance re-checks each against the diff, CI and the test output"
  - control: in-process effects
    disposition: "residual: the test reads the Makefile text or runs make -n in a temporary copy; nothing from the PR is imported into the test process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: none in allowed_files; an undeclared change to such a file fails at the audit (INV-12)"
  - control: new or renamed scripts
    disposition: "residual: none; a new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: "make update ends by running agmsg-bootstrap in whatever checkout it runs in, and herdr-agents prints a join.sh instruction when that checkout has no identity"
    command: "grep -n 'agmsg-bootstrap' Makefile | head -3; grep -n 'No agmsg %s identity' home/dot_local/bin/common/executable_herdr-agents"
    output: |-
      124:	$(MAKE) agmsg-bootstrap
      157:.PHONY: agmsg-bootstrap
      158:agmsg-bootstrap:
      1402:                printf 'No agmsg %s identity for %s; run: AGMSG_RESOLVE_PROJECT=0 %s/join.sh <team> <agent-name> %s "%s"\n' \
  - claim: "on 2026-10-12 the operator's make update in the canonical clone printed that instruction for ~/.local/share/chezmoi (the operator's pasted terminal output)"
    command: "git -C ~/.local/share/chezmoi pull && make -C ~/.local/share/chezmoi update   (operator's terminal, 2026-10-12 10:0xZ; last lines)"
    output: |-
      /Library/Developer/CommandLineTools/usr/bin/make agmsg-bootstrap
      No agmsg Claude Code identity for ~/.local/share/chezmoi; run: AGMSG_RESOLVE_PROJECT=0 ~/.agents/skills/agmsg/scripts/join.sh <team> <agent-name> claude-code "~/.local/share/chezmoi"
  - claim: "the existing supply-chain policy tests already name the bootstrap target"
    command: "grep -n -c 'agmsg-bootstrap\\|bootstrap-agmsg' tests/unit/test_supply_chain_policy.py"
    output: "1"
---

# AGMSG-TASK dotfiles-T128-update-bootstrap-canonical-a01 — `make update` stops inviting a seat into the canonical clone (plan 007 T716)

Written 2026-10-12 by the orchestrator seat under plan 007 (Phase 5, T716; approval pending at drafting time). Review tier by INV-1 (`kind: code`). The canonical chezmoi clone is pull and apply only (SKILL "Review and integration invariants": no seat edits it, one orchestrator identity per repository at the working clone), yet `make update` there ends with an instruction to register an identity at it (premise 2). The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C6 pass on this file.

## What to do

1. In `Makefile`'s `update` target, run `$(MAKE) agmsg-bootstrap` only when `$(CURDIR)` is not the chezmoi source directory (compare against `$(HOME)/.local/share/chezmoi`, or `chezmoi source-path` when `chezmoi` is on PATH; pick the one that needs no new dependency and say which); in the canonical clone print one line instead: `agmsg bootstrap skipped: the canonical chezmoi clone is pull and apply only; seats register at the working clone.` Keep every other step of `update` as it is.
2. `tests/unit/test_supply_chain_policy.py`: one test named exactly `test_update_skips_agmsg_bootstrap_in_the_canonical_clone` that runs `make -n update` (or reads the target) with `CURDIR` set to the canonical path and asserts the bootstrap is not invoked and the skip line is, and that in another directory the bootstrap is invoked as before. Follow the module's existing style for Makefile checks.
3. Nothing else changes: not `herdr-agents`, not the `agmsg-bootstrap` target itself.

## Validation

- `uv run --no-project python -m unittest tests/unit/test_supply_chain_policy.py -v` output in the validation file (the new test named).
- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps).

## Completion

The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. Branch `tools/update-bootstrap-canonical`, draft PR from `origin/main`. After the merge the operator's next `make update` in the canonical clone prints the skip line (the measurement).
