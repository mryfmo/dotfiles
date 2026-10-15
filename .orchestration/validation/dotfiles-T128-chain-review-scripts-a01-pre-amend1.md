---
format: 2
task_id: dotfiles-T128-chain-review-scripts-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/local-review.sh
  - scripts/orchestrator/local-advisory.sh
  - scripts/orchestrator/sandbox-scan.sh
  - tests/unit/test_chain_review_scripts.py
  - .orchestration/dotfiles-T128-chain-review-scripts-a01/**
after: [dotfiles-T128-gate-wrapper-path-a01]
threat_table:
  - control: the PR adds scripts/orchestrator/local-review.sh, which checks the review worktree out at a PR head and runs the review binary there read-only, writing one validation file
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file"
  - control: the PR adds scripts/orchestrator/local-advisory.sh, which appends advisory rows and local-finding lines to an acceptance record and stops on a P0 or P1
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_advisory_records_p2_rows_and_stops_on_p0_p1"
  - control: the PR adds scripts/orchestrator/sandbox-scan.sh, which prints the unsandboxed mutation calls of a worker sandbox record
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_sandbox_scan_prints_the_unsandboxed_mutation_calls"
  - control: the PR adds tests/unit/test_chain_review_scripts.py, the oracle of the three rows above (a stub review binary on CODEX_BIN that records argv, cwd and environment and prints a canned transcript; a temporary git repository with a main branch and a head commit as the review worktree; fixture texts the tests write)
    disposition: "residual: the stubs record and print, nothing else; the audit reads each case against the Files items"
  - control: "the review worktree (the path ORCH_REVIEW_WORKTREE names when set, else <root>/.claude/worktrees/orchestrator-review): local-review.sh refuses a dirty one with exit 2, checks the head out detached and restores nothing (the chain's audit wrapper restores it)"
    disposition: "residual: the orchestrator's own worktree, detached at origin/main between runs; the refusal is covered by the first closed row's dirty case; the restore belongs to orch-audit.sh on main"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-chain-review-scripts-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the three scripts as subprocesses with the stub review binary on CODEX_BIN and real git in a temporary repository, and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; local-review.sh runs git, mktemp and the review binary (the value of CODEX_BIN when the environment sets it, the test seam, else codex resolved with command -v in the repository root before the head checkout, its absolute path used afterwards; the profile review is fixed in the script, the model-selection rule); local-review.sh also runs awk, sed, date and cut; local-advisory.sh runs git rev-parse, grep, sed, cut and tr; sandbox-scan.sh runs git rev-parse and grep; the review binary runs with the PR head as its working directory under its own read-only sandbox, so the PR's content (its AGENTS.md, its configuration files) is input to that review and never to the gate: the review's findings are a sample the orchestrator judges (advisory rows or a stop), and the script writes nothing but the validation file"
  - control: new or renamed scripts
    disposition: "residual: three new scripts under scripts/orchestrator/, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'none of the three script names exists under scripts/orchestrator/ on origin/main (the task adds, it does not edit)'
    command: 'git ls-tree --name-only origin/main scripts/orchestrator/ | /usr/bin/grep -c -E "local-review|local-advisory|sandbox-scan" || true'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-a01 — the integration chain's review-side steps become repository scripts with tests (plan 021 step 6.3; the review half of the step's "next tools task")

Drafted 2026-10-14 by the orchestrator seat (the bus time of its TASK line is the dispatch time), in the step-7 short form. Plan 021's step 6.3 inventory names six chain steps whose logic lives only in the orchestrator's scratchpad; the hand-typed-chain class holds fourteen mistake records today, and the structural answer is repository scripts with tests. This task lands the three review-side scripts; its sibling `dotfiles-T128-chain-github-scripts-a01` lands the two GitHub-side scripts (`resolve-threads.sh`, `pr-cost.sh`) with its own test module, so the two run concurrently on disjoint files. The attached inputs under `.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/` of the orchestrator's main checkout (the directory the TASK line's `task_file` is read from, untracked until the next boundary) are the scripts as the chain runs them today, with the repository root resolved by `git rev-parse --show-toplevel`; their sha256 prefixes (`shasum -a 256 <dir>/*.sh | cut -c1-16`): 2e44dabc23ea0397  local-advisory.sh; 2258e370b9ff2575  local-review.sh; 099f6c7534223cb4  sandbox-scan.sh; each item names what changes. The one premise is replayable from any checkout (it reads `origin/main`).

## Goal

The local review of a PR head, the recording of its advisory findings and the scan of a worker's sandbox record run from `scripts/orchestrator/` on `origin/main`, each with one test that closes its row, so the next integration's log names repository scripts for these steps.

## Files

1. `scripts/orchestrator/local-review.sh <task> <head> <pr>`: the input's behaviour (one review per head: an existing `.orchestration/validation/<task>-local-review-<sha7>.md` is reused and re-reported with its finding lines and `local-review: <n> findings (existing <file>)`; otherwise the head must be a local commit, exit 2 if not, and the review worktree clean, exit 2 if not; the worktree is checked out detached at the head; the review binary runs there as `<binary> --profile review -s read-only review --base main` with stdin from `/dev/null`; the transcript's final message after the `codex` marker line is kept with the worktree prefix stripped; the unique lines matching `^- \[P[0-3]\]` are the findings; the file gets the front matter the input writes: task, head, pr, base, started, finished, findings, engine; the findings are printed, then `local-review: <n> findings (<file>)`; a non-zero exit of the review binary prints `local-review: codex exited <n> (see <file>)` and the file is still written from whatever transcript came back; exit 0 with no finding, 3 with findings, 2 on a precondition) with these changes: the repository root is `git rev-parse --show-toplevel`; the review worktree is `$ORCH_REVIEW_WORKTREE` when set, else `<root>/.claude/worktrees/orchestrator-review`; the review binary is `$CODEX_BIN` when set, else `codex` resolved with `command -v` in the repository root before the checkout and used by that absolute path afterwards; the profile `review` stays fixed in the script; an shdoc header; `bash -n` and shellcheck clean.
2. `scripts/orchestrator/local-advisory.sh <task> <head40> <owner-task-id>`: the input's behaviour (reads `.orchestration/validation/<task>-local-review-<sha7>.md`, exit 2 when absent; `findings: 0` prints `local review of <sha7>: no findings` and exits 0; otherwise ensures the heading `## Owned by <owner> (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)` in `.orchestration/acceptance/<task>.md`; then for each unique finding line in order, numbered from 1: a `[P0]` or `[P1]` prints `STOP: local finding <n> of <sha7> is P0/P1: <line>` and makes the exit 3, any other appends the row `local:<sha7>:<n><TAB>advisory-p2` and the line `local-finding: <sha7>:<n> not-applicable:advisory P2 owned by <owner> (<the finding's first 120 characters, backticks removed>); evidence=git show origin/main:.orchestration/tasks/<owner>.md | grep -n 'item 1'`, each only when the record lacks it; last line `local review of <sha7>: <i> finding(s) recorded as advisory under 'Owned by <owner>' in <record>`) with the repository root from `git rev-parse --show-toplevel` and an shdoc header.
3. `scripts/orchestrator/sandbox-scan.sh <task>`: the input's behaviour (over `.orchestration/sandboxes/<task>.md`, where a trailing `-fixtures` of `<task>` is stripped as the input does with `${task%-fixtures}`: the lines matching, case-insensitively as the input's `grep -i` does, `dangerouslyDisableSandbox`, `outside the sandbox` or `unsandboxed` that also match a mutation, `git commit`, `git switch -c`, `git checkout`, `git add`, `git mv`, `git rm`, `cp `, `mv `, `> ` or `tee `, and none of `counts`, `reads`, `lists`, printed with their line numbers followed by `sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit`; with no such line, `sandbox scan: no unsandboxed mutation call in <record>`; a missing record prints nothing; exit 0 in every case) with the repository root from `git rev-parse --show-toplevel` and an shdoc header.
4. `tests/unit/test_chain_review_scripts.py` (new), run by `uv run python -m unittest` without PyYAML, importing only the standard library, each test in a temporary directory holding a git repository with a `main` branch, a head commit and a second worktree for the review:
   - `test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file`: the review worktree is a second worktree of the temporary repository created outside the repository root and named by `ORCH_REVIEW_WORKTREE`; a stub review binary records its argv, its working directory and `PATH` to a log and prints a transcript with a `codex` marker line followed by one `- [P2] …` finding. Case one, `CODEX_BIN` unset: the stub is `codex` in an absolute directory on PATH, PATH also holds the relative entry `./bin` before it, and the head commit (not the root's working tree) contains `bin/codex`, a decoy that logs to a second file; the test asserts the stub's log holds the call with the argv (`--profile review -s read-only review --base main`) and the working directory (the review worktree, whose HEAD is the given head), the decoy's log is empty (the binary was resolved in the repository root before the checkout and run by its absolute path), the repository's main working tree gained no path but the validation file (`git status --porcelain` there lists only it), the file holds the front matter and the finding, the exit is 3 with the finding line and the summary line printed. Case two, `CODEX_BIN` set to the stub: the same assertions on argv and working directory. Then: a second run on the same task and head does not run the stub (its log unchanged) and exits 3 again; a run under a second task name with a transcript of no finding exits 0; a dirty review worktree exits 2 with the stub's log unchanged.
   - `test_local_advisory_records_p2_rows_and_stops_on_p0_p1`: with a local-review file of two P2 findings, the record gains the heading, two rows and two lines once across two runs; with a P1 finding first and a P2 second, the STOP line is printed, the exit is 3, the P2's row and line are appended and the P1 gets none; with `findings: 0` nothing is appended and the exit is 0; with no file the exit is 2.
   - `test_sandbox_scan_prints_the_unsandboxed_mutation_calls`: a sandbox record with one `dangerouslyDisableSandbox … git commit` line and one `unsandboxed … counts` line prints the first with its line number and the judge line; a record with reads only prints the no-hit line; a missing record prints nothing; each exits 0.

## Out of scope

The GitHub-side scripts (the sibling task), the chain glue (`integrate-pr.sh`, `finish-pr.sh`; it stays outside the repository until every step it calls is a repository script, plan 021 step 6.3), `orch-audit.sh`, `orch-gate.sh`, `acceptance-front-matter.py`, `dispatch.sh`, any rule text, the Makefile.

## Check

`uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` green, pasted in the validation file with `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after PR #355, merged 08:27Z as 5ec86052), pairwise-disjoint from the sibling task's files (`scripts/orchestrator/resolve-threads.sh`, `pr-cost.sh`, `tests/unit/test_chain_github_scripts.py`, its evidence directory). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `dotfiles-T128-chain-review-scripts-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the three test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md>` and the evidence paths.

## Change (round 2, 2026-10-14)

The Codex half's round 1: premise 3 counted a phrase across the whole plan file, which the orchestrator's own status line of 08:45Z changed from 8 to 9 within minutes; the premise now counts inside the step 6.3 inventory section only. Item 3 said `<task>.md` where the input reads `${task%-fixtures}.md`; the item now states the input's suffix stripping. The sibling task dropped `review-receipt.sh` (the inventory keeps the receipt as glue), so the sibling file list here names two scripts.

## Change (round 3, 2026-10-14)

The seat's round 1 (on the round-1 hash): premises 1 and 3 read untracked files of the orchestrator's checkout (the inputs, plan 021's inventory) that a worker replaying from its worktree on `origin/main` cannot see, so they are removed and the one premise left reads `origin/main`; the inputs' hashes are stated in the intro as facts. Item 4's first test gains the case that closes the row's resolution claim: `CODEX_BIN` unset, a relative `./bin` on PATH whose `codex` decoy exists only in the head commit, the decoy's log empty; the review worktree sits outside the repository root and the no-new-path assertion is on the main working tree; the no-finding run uses a second task name. Item 1 states the input's continuation on a non-zero review-binary exit; item 3 states the case-insensitive match; row 11 lists the tools each script runs.
