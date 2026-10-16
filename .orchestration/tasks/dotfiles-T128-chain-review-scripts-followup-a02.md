---
format: 2
task_id: dotfiles-T128-chain-review-scripts-followup-a02
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/local-review.sh
  - tests/unit/test_chain_review_scripts.py
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a02/**
after: [dotfiles-T128-chain-review-scripts-followup-a01]
threat_table:
  - control: the PR edits scripts/orchestrator/local-review.sh only within the owned row (item 1), refusing before the checkout an env -S shebang string the script cannot split as env does (a quote, an escape, an expansion or a comment word)
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_review_refuses_a_quoted_env_S_shebang"
  - control: the PR edits tests/unit/test_chain_review_scripts.py (one new test beside the lineage's, which stay as they are; the stub binaries and the stub mise on PATH answer as in the lineage's tests)
    disposition: "residual: the stubs record and answer, nothing else; the audit reads the case against item 1"
  - control: "the review binary's first line (a shebang the PR head cannot influence, since the binary is resolved in the trusted root before the checkout): an env -S string (the interpreter token and the remainder) that holds a quote, a backslash, a dollar sign or a word starting with # is refused with exit 2 before the checkout, so the script never runs an interpreter with arguments split differently from env on the four -S features that split differently (quoting, escapes, variable expansion, comments)"
    disposition: "residual: plain words are split as the lineage's round-3 fix does; a quoted, escaped, expanding or commented string is refused rather than parsed, so no launcher runs with wrong arguments; the closed row's cases cover a double quote, a single quote, a backslash, a ${X} expansion and a # word"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-review-scripts-followup-a02/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a02/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run local-review.sh as a subprocess with the stub review binary, the stub mise and real git in a temporary repository, and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; local-review.sh resolves the review binary and its env-shebang interpreter in the trusted root before any checkout as the lineage landed (mise which under env -i, a shims path refused), and this row only narrows what it accepts; the test seam is CODEX_BIN and PATH"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the owned rows are in the first owner task''s acceptance record on origin/main at dispatch (absent until boundary (16): the rows were written on 2026-10-15; this task never dispatches before)'
    command: 'git show origin/main:.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a01.md 2>/dev/null | /usr/bin/grep -c "^audit:2e3ff49:1	env-s-quoting" || true'
    output: |-
      0
  - claim: 'local-review.sh on origin/main after PR #364 splits an env -S remainder with read -r -a and refuses nothing about quotes (PR #364 is not merged today, so the count is 0 before and 1 after its merge; the dispatch needs 1)'
    command: 'git show origin/main:scripts/orchestrator/local-review.sh | /usr/bin/grep -c "read -r -a words" || true'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a02 — local-review.sh refuses an `env -S` shebang remainder it cannot split as env does (the second owner task of the chain-review-scripts lineage; the audit of PR #364's 2e3ff49 and its local review)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch; dispatched only after PR #364 merges and boundary (16) puts its record's owner rows on `origin/main` (both premises then read `1`; the outputs above are today's). PR #364's round 3 made `local-review.sh` keep the words after `env -S NAME` as the interpreter's own arguments, split with `read -r -a`; the audit of its update-branch head 2e3ff49 (finding 1, P2, `local-review.sh:96`) and the chain's local review of that head found that `read -r -a` does not follow `env -S`'s quoting: `--require "/opt/review modules/init.js"` becomes three words with literal quotes instead of two, so a valid launcher with a quoted `-S` argument would run with wrong arguments. The rows are `audit:2e3ff49:1` and `local:2e3ff49:1` (class `env-s-quoting`, one defect), both under `## Owned by dotfiles-T128-chain-review-scripts-followup-a02` in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a01.md` (the audit row also appears under its audit heading, as the record's ledger requires); the earlier row `local:850fc54:1` there is closed by PR #364's round 3 (`fixed:afd36bb8`). The codex launcher on this host has no `-S` form, so nothing is wrong today; the row is a correctness gap of the hardening.

## What to do

1. The owned rows: in the shebang branch, when the whole `-S` string (the interpreter token, regex group 2, and the remainder, group 3) holds a double quote, a single quote, a backslash, a dollar sign or a word starting with `#` (the four `env -S` features bash's `read -r -a` splits differently: quoting, escapes, variable expansion and comments, as GNU coreutils documents), `local-review.sh` prints `local-review: the review binary's env -S shebang holds a quote, an escape, an expansion or a comment the script does not split; refused` on stdout (the script's other refusals are stdout lines) and exits 2 before the checkout (nothing written, the worktree untouched); a string of plain words is split as today. The alternative, a faithful `env -S` parser, is out of scope (it is not a few lines, and no launcher this regime runs needs it). Failure mode stated: fail closed on a shebang the script cannot split faithfully.
2. One test, `test_local_review_refuses_a_quoted_env_S_shebang`, in the module's style (`run_tool` returns stdout, which the refusal line is on): five stub binaries whose first lines are `#!/usr/bin/env -S fakeinterp --require "/opt/a b/x.js"`, `#!/usr/bin/env -S fakeinterp 'x'`, `#!/usr/bin/env -S fakeinterp a\ b`, `#!/usr/bin/env -S fakeinterp ${HOMEX}/lib` and `#!/usr/bin/env -S fakeinterp one # two`: each exits 2 with the stdout line, the review worktree stays at `main`, no file is written and the stub interpreter is never run; the round-3 test's plain-word case stays as it is.
3. Nothing else changes: no file outside the two, no behaviour the rows do not name.

## Validation

- `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` in the validation file, with the new test named; `shellcheck scripts/orchestrator/local-review.sh`.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

A fresh branch from `origin/main` after PR #364 merges and boundary (16), one new PR. The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR whose fix stays within these files and is small is fixed in a revise round the orchestrator sends with a `check=` (correction C-50) while INV-6's counts allow it; any other P2 is advisory and recorded under the same heading in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a01.md` for the lineage's next owner task. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test name, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a02/task.md>` and the evidence paths.

## Change (round 2, 2026-10-15 09:0xZ)

The review seat's round 1 (two P2, three P3; the Codex half confirmed round 1): the refused set covers the four `env -S` features that split differently (quote, escape, `$` expansion, `#` comment word), checked over the whole `-S` string; the refusal is a stdout line like the script's others; two test cases added; the record aligned (both rows under the owner heading with their class); the Completion names every P2 thread with the proposed disposition.
