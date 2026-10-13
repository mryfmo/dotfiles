---
format: 2
task_id: dotfiles-T128-orchestrator-tools-followup-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/boundary.sh
  - scripts/orchestrator/ff-main.sh
  - scripts/orchestrator/orch-audit.sh
  - scripts/orchestrator/orch-gate.sh
  - scripts/orchestrator/fill_sweep.py
  - scripts/orchestrator/acceptance-front-matter.py
  - scripts/orchestrator/codex-review.sh
  - scripts/orchestrator/design-keydiff.py
  - scripts/orchestrator/replay.sh
  - scripts/orchestrator/dispatch.sh
  - scripts/orchestrator/bus-read.sh
  - scripts/orchestrator/three-repeat.sh
  - scripts/regime-counters.sh
  - tests/unit/test_regime_counters.py
  - tests/unit/test_orchestrator_tools.py
  - .orchestration/dotfiles-T128-orchestrator-tools-followup-a01/**
after: [dotfiles-T128-orchestrator-tools-a02]
threat_table:
  - control: the PR edits scripts/orchestrator/boundary.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/ff-main.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/orch-audit.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/orch-gate.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/fill_sweep.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/acceptance-front-matter.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/codex-review.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/design-keydiff.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/replay.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/dispatch.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/bus-read.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/three-repeat.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/regime-counters.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits tests/unit/test_regime_counters.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits tests/unit/test_orchestrator_tools.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-orchestrator-tools-followup-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance); the pair's receipts name this file's hash"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: the branch evidence records under .orchestration/dotfiles-T128-orchestrator-tools-followup-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: the worker's untrusted claims; acceptance re-checks each against the diff, CI and the test output"
  - control: in-process effects
    disposition: "residual: acceptance-front-matter.py imports scripts/require-crit-review.py's record validator into its process, and the tests import fill_sweep.py, acceptance-front-matter.py and design-keydiff.py; each is the declared change or the gate module on main, read line by line by the orchestrator and the audit"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts resolve exactly these host binaries, a closed list the tests stub or the audit replays from the diff: git, gh, make, codex, uv and the interpreter it resolves as `python` under `uv run --no-project` (the attached inputs' form; the first slice's `python3 -I` is the other accepted form, and the implementation uses one of the two, never a bare `python` outside uv), shasum, jq (regime-counters.sh's ledger parsing), env, bash, agmsg-dispatch, the agmsg history.sh, and the coreutils awk, cat, cp, cut, date, dirname, find, grep, head, ls, mkdir, mktemp, mv, rm, rmdir, sed, sort, tail, tee, tr, wc, xargs; a script that needs another binary adds it to this row by amendment before it is written as the SKILL's own commands do; fill_sweep.py and acceptance-front-matter.py read and write the acceptance record's JSON block with the standard library's json module, as amendment 1 of dotfiles-T128-gate-evidence-a03 defines it (plan 013 A′); two scripts use PyYAML through uv run --no-project --with pyyaml (the uv cache; a network fetch only when the cache is empty): design-keydiff.py for the design file's front matter, and boundary.sh for scripts/validate-agent-assets.py --mask-secrets and make validate-agent-assets, the repository's own masker and validator; neither is the gate (PR #329 thread 4250238721 is about the gate); replay.sh runs the given command with env -i PATH=/usr/bin:/bin bash -c; the tests stub every host binary on PATH"
  - control: new or renamed scripts
    disposition: "residual: every new script is under scripts/orchestrator/, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: "the lineage's last task file is on origin/main (this task runs after it)"
    command: "git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md && echo present"
    output: "present"
  - claim: "the lineage's acceptance record is on origin/main (the owned section is appended to it by the daily boundary after the PR's merge, before this task dispatches)"
    command: "git cat-file -e origin/main:.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md && echo present"
    output: "present"

---

# AGMSG-TASK dotfiles-T128-orchestrator-tools-followup-a01 — the residual findings of the tools PRs (#346 and the PR after it) (the owner task of the T718 tools lineage; plan 020 step 1, C-32's owner-first pattern)

Written 2026-10-13 13:37Z by the orchestrator seat, pair-reviewed before dispatch. Under plan 020 a P2 finding (Codex Bot, the orchestrator's local review, or the audit) on a head of the tools PRs (#346 and the PR after it) is advisory: it is dispositioned on the PR as `not-applicable:advisory P2 owned by dotfiles-T128-orchestrator-tools-followup-a01` and recorded as a row of `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md` under the heading `## Owned by dotfiles-T128-orchestrator-tools-followup-a01`; only P0/P1 findings get the PR's one fix round. This task fixes exactly those rows after the PR merges; it exists on `main` before the findings do, so no boundary commit is needed between a PR's final head and its merge. Review tier by INV-1 (the same files and kind as `dotfiles-T128-orchestrator-tools-a02`). The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C10 and C7b pass on this file.

## What to do

1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-orchestrator-tools-followup-a01` in `.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a02.md` as read from `origin/main` (advisory P2 findings on the lineage's PR heads, each dispositioned on the PR as `not-applicable:advisory P2 owned by dotfiles-T128-orchestrator-tools-followup-a01; evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a01.md | grep -n 'item 1'` (the gate's full form once PR #329 lands)). That section is this item's whole definition, closed at the lineage's acceptance and landed by the daily boundary after the merge; this task dispatches only after that boundary (the dispatch line names the record's hash); a finding outside the section is not owned here, and a missing or empty section at dispatch makes this task a no-op that report.md states (the section is created at the lineage's acceptance, so it does not exist before that). For each row: the defect the thread or finding names is fixed at root cause in the file it names, with one test per fix in the lineage's test module (and a fixture when the test reads one); the RESULT lists each row with `fixed:<sha>`.
2. Nothing else changes: no file outside the owned rows' files, no behaviour the rows do not name.

## Validation

- The lineage's test command output in the validation file (the module `allowed_files` names), with the new tests named.
- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`).

## Completion

The PR is ready for the orchestrator's integration when CI is green, the Bot's single review (on PR open) is in, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread as advisory. A fresh branch from `origin/main` after the lineage's PR merges, a new PR; the orchestrator runs the local review once on the final head; one fix round at most; a surviving P0/P1 stops the PR.
