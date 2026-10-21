---
format: 2
task_id: dotfiles-T130-sandbox-portability-a01
kind: code
security: false
allowed_files:
  - scripts/check-statusline-tools.py
  - tests/unit/test_sandbox_portability.py
  - .orchestration/dotfiles-T130-sandbox-portability-a01/**
after: []
threat_table:
  - control: "the PR edits scripts/check-statusline-tools.py in two literals (the probe's cwd and transcript path move off /tmp to a path that does not exist; Amendment 1)"
    disposition: "residual: two string literals of a probe that needs only a cwd string and a missing transcript path; the guard test of item 2 then accepts the file; the audit reads the diff"
  - control: "the PR adds tests/unit/test_sandbox_portability.py (the guard tests of items 1 and 2 over the tracked tree)"
    disposition: "residual: the tests read git ls-files and the checkout; fixtures written into a temporary directory; the audit reads each case against its item"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T130-sandbox-portability-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T130-sandbox-portability-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run git ls-files and read the checkout, and write fixtures into a temporary directory; nothing else runs"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the tests run under make unit-test as today"
  - control: new or renamed scripts
    disposition: "residual: none; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: no tracked script under scripts/, home/ or install/ on origin/main uses diff with process substitution, so item 1 is a guard, not a rewrite
    command: git grep -cE 'diff[^|]*<\(' origin/main -- scripts home install | wc -l | tr -d " "
    output: |-
      0
  - claim: no tracked script under scripts/, home/ or install/ on origin/main parses ps output through a pipe, so item 2 (d) is a guard the lint's R5 rule already carries
    command: git grep -cE '\bps (-|a)[^|]*\|' origin/main -- scripts home install | wc -l | tr -d " "
    output: |-
      0
  - claim: the contextdb store base on origin/main is the .claude/contextdb directory of the repository root (the two lines item 3 changes)
    command: 'git show origin/main:.claude/contextdb/contextdb/paths.py | /usr/bin/grep -nF .claude | cut -d: -f1 | paste -sd, -'
    output: |-
      44,54,68,114
---

# AGMSG-TASK dotfiles-T130-sandbox-portability-a01 — the sandbox portability follow-up (the operator's 20:59 JST approval; the monitor's 22:40 JST item 1)

Written 2026-10-17 by the orchestrator seat from the overnight monitor's consolidated correction of 22:40 JST (item 1, under the operator's 21:49 JST directive) and the operator's 20:59 JST approval ("code and rule fixes go in a follow-up PR"). The grounding on origin/main (premises 1 to 3): no `diff <(...)` and no `ps` parsing exist in tracked scripts, and `/tmp` appears only inside test fixture strings, so items 1 and 2 are guards that keep it so, and item 3 is the one real move. Item (e) of the approval, a sandbox exclusion for the codex local-review command, is Claude's permission boundary and travels as `dotfiles-T130-codex-local-review-exclusion-a01` to a Codex seat (Orchestrator Playbook step 3). Worker: claude-review-dot-a005 (worker-d; its #387 is accepted pending integration). It does not need PR #392 merged.

## Goal

The repository's own scripts work inside the Claude sandbox on both OSes: no `diff` over process substitution, no hard-coded `/tmp`, no `ps` parsing (the CompactionDB store stays under `.claude/`: Amendment 2).

## Files

1. `tests/unit/test_sandbox_portability.py` (new), `test_no_process_substitution_in_tracked_scripts`: over `git ls-files -- scripts home install` filtered to shell files (names ending `.sh`, `.bash`, `.zsh` or a `sh`/`bash`/`zsh` shebang), no line outside a comment contains `<(` or `>(`; the fixture is a temporary repository with one offending script, refused, and the checkout, accepted.
2. Same file, `test_no_hard_coded_tmp_in_tracked_scripts`: over the same files plus `.py` files under the same roots, no line outside a comment contains `/tmp/` or a bare `/tmp` path literal unless the line also reads `TMPDIR` (the sandbox's writable temporary directory is `$TMPDIR`, never `/tmp`); fixture as above. (d) `ps` parsing: none on origin/main (premise 2); the lint of PR #387 carries rule R5 for it, so no second guard; the report says so.
3. Withdrawn (Amendment 2): the CompactionDB store stays under `.claude/`; the relocation is an upstream design task of its own (D-portability-store).

## Out of scope

The agmsg skill's `storage.sh` (upstream, not in this repository); `tests/unit/test_herdr_agents.py` (in flight in PR F4); the sandbox exclusion for the codex local-review command (`dotfiles-T130-codex-local-review-exclusion-a01`); any lint change (`scripts/lint-comparisons.py` is PR #387's).

## Check

`uv run python -m unittest tests/unit/test_sandbox_portability.py -v` green pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 20 changed lines outside `tests/` and `.orchestration/` (the two literals), 200 under `tests/` (Amendment 2: item 3 withdrawn).

## Completion

One PR from a fresh branch off `origin/main`. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T130-sandbox-portability-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T130-sandbox-portability-a01/task.md>` in the RESULT.

## Amendment 1 (round 1, 2026-10-17T14:4xZ)

a005's question (PONG 14:38:09Z), measured inside the sandbox: `done < <(…)`, `comm <(…) <(…)` and `cat <(…)` work; only `diff <(…) <(…)` fails (`diff: /dev/fd/63: Operation not permitted`). So item 1's guard is premise 1's own predicate and no wider: `test_no_process_substitution_in_tracked_scripts` refuses a `diff` invocation with a `<(` or `>(` argument (the fixture `diff <(a) <(b)` refused, the checkout accepted); the 30 `done < <(…)` loops and the one `comm` form stay. Item 2's guard refuses two lines of `scripts/check-statusline-tools.py` (lines 16 and 18, the probe's `/private/tmp` payload literals): option A, the file joins `allowed_files` with its row and the two literals move to a path that does not exist (the probe needs only a cwd string and a missing transcript path). Item 3 proceeds as written. Nothing else changes.

## Amendment 2 (round 1, 2026-10-17T14:4xZ)

a005's blocked PONG (14:40:40Z) on item 3: the store move needs edits outside this task and across a trust boundary: `home/dot_local/bin/common/executable_contextdb-codex-notify` (lines 49 to 69) resolves the project by the `.claude/contextdb` directory, refuses symlinks under it and requires its state and spool children before running the trusted CLI from `~/.agents/compactiondb/`, with `tests/unit/test_contextdb_codex_notify.py` asserting that boundary; the trusted CLI's `paths.py` is byte-identical to this repository's copy (synced from `vendor/compactiondb/`, never edited), so moving only the repository's package base would split the ledger into two stores; `compactiondb-install` rewrites the package copy and the ignore entries on reinstall; upstream has no store-base option. Decision (default, D-portability-store): item 3 is withdrawn from this task; the store stays under `.claude/` (the sandbox reaches it today: this seat's own `memory add` wrote there). A relocation, if the operator still wants it, is a design task of its own on `vendor/compactiondb` (a store-base option), then the receiver, its tests and the installer. `allowed_files` loses `.claude/contextdb/**`, `.gitignore` and `CLAUDE.md` with their rows; the Goal, item 3 and the Check below read accordingly; items 1 and 2 stand as Amendment 1 says.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T130-sandbox-portability-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T130-sandbox-portability-a01.md
```
