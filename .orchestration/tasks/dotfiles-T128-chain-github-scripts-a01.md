---
format: 2
task_id: dotfiles-T128-chain-github-scripts-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/resolve-threads.sh
  - scripts/orchestrator/pr-cost.sh
  - tests/unit/test_chain_github_scripts.py
  - .orchestration/dotfiles-T128-chain-github-scripts-a01/**
after: [dotfiles-T128-gate-wrapper-path-a01]
threat_table:
  - control: the PR adds scripts/orchestrator/resolve-threads.sh, which replies to a PR's unresolved review threads with the orchestrator's dispositions and resolves them through the GitHub API with the orchestrator's gh credentials
    disposition: "closed: tests/unit/test_chain_github_scripts.py::test_resolve_threads_replies_with_the_table_row_and_resolves_only_threads_with_rows"
  - control: the PR adds scripts/orchestrator/pr-cost.sh, which appends one ledger line per PR to .orchestration/metrics/pr-cost.tsv from the GitHub API
    disposition: "closed: tests/unit/test_chain_github_scripts.py::test_pr_cost_appends_one_ledger_line_from_the_api"
  - control: the PR adds tests/unit/test_chain_github_scripts.py, the oracle of the two rows above (a stub gh on PATH that records every call and answers canned JSON per endpoint; fixture tables and sweep files the tests write)
    disposition: "residual: the stub records and answers, nothing else; the audit reads each case against the Files items"
  - control: "the GitHub writes (reply comments and thread resolutions on the PR, with the orchestrator's gh credentials): the body of a reply is built only from the disposition table row or the sweep JSON's disposition field, both orchestrator-authored, in the two fixed sentences; --dry-run writes nothing"
    disposition: "residual: covered by the first closed row's dry-run and missing-row cases; a thread without a row is left open and makes the exit 3, never guessed"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-github-scripts-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-chain-github-scripts-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the two scripts as subprocesses with the stub gh first on PATH and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts run gh, jq, awk and uv run --no-project python, each resolved on the orchestrator's PATH (the tests put the stub gh first); the repository name mryfmo/dotfiles stays literal as in the inputs; nothing the PR under integration contains chooses any of them"
  - control: new or renamed scripts
    disposition: "residual: two new scripts under scripts/orchestrator/, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'neither script name exists under scripts/orchestrator/ on origin/main (the task adds, it does not edit)'
    command: 'git ls-tree --name-only origin/main scripts/orchestrator/ | /usr/bin/grep -c -E "resolve-threads|pr-cost" || true'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-chain-github-scripts-a01 — the integration chain's GitHub-side steps become repository scripts with tests (plan 021 step 6.3; the GitHub half of the step's "next tools task")

Drafted 2026-10-14 by the orchestrator seat (the bus time of its TASK line is the dispatch time), in the step-7 short form. Plan 021's step 6.3 inventory names six chain steps whose logic lives only in the orchestrator's scratchpad; the hand-typed-chain class holds fourteen mistake records today, and the structural answer is repository scripts with tests. This task lands the two GitHub-side scripts (the receipt stays glue, as the inventory says); its sibling `dotfiles-T128-chain-review-scripts-a01` lands the three review-side scripts (`local-review.sh`, `local-advisory.sh`, `sandbox-scan.sh`) with its own test module, so the two run concurrently on disjoint files. The attached inputs under `.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/` of the orchestrator's main checkout (the directory the TASK line's `task_file` is read from, untracked until the next boundary) are the scripts as the chain runs them today, with the repository root resolved by `git rev-parse --show-toplevel`; their sha256 prefixes (`shasum -a 256 <dir>/*.sh | cut -c1-16`): 235d84b15ede9cb8  pr-cost.sh; 118108254c8f8adb  resolve-threads.sh; each item names what changes. The one premise is replayable from any checkout (it reads `origin/main`).

## Goal

The thread resolution and the cost ledger line of a PR run from `scripts/orchestrator/` on `origin/main`, each with one test that closes its row, so the next integration's log names repository scripts for these steps.

## Files

1. `scripts/orchestrator/resolve-threads.sh <pr> <extra.tsv> [<mode>] [<sweep.json>]`: the input's behaviour (the arguments are positional as in the input: the third is `--dry-run` or any placeholder such as `-`, the fourth the sweep JSON; the table must exist; the PR's unresolved review threads come from one GraphQL query over the first 100 threads, each as its first comment's database id and the thread id; for each: the disposition is the table row whose first column is that comment id, else, when a sweep JSON is given, the `disposition` of the sweep item whose `url` ends with `_r<comment id>`; no disposition prints `no disposition row for thread <id> (table or sweep); left open` and makes the exit 3; a `fixed:` row's reply body is `Disposition (orchestrator): <row>. Fixed at root cause in that commit on this branch; verified by the task's tests and CI on the final head. Resolving.`, a `not-applicable:` row's is `Disposition (orchestrator): <row>. Resolving; the owning task on main carries it.`, any other form is reported and makes the exit 3; `--dry-run` prints `would reply+resolve <id>: <row's first 90 characters>` and writes nothing; otherwise one reply is posted on the comment and one `resolveReviewThread` mutation sent for the thread, `resolved <id> (<row's first 60 characters>)` printed; last line `resolved <n> thread(s); missing rows: <0|1>`) with an shdoc header; `gh` is called by name as the input does.
2. `scripts/orchestrator/pr-cost.sh <pr>`: the input's behaviour (creates `.orchestration/metrics/pr-cost.tsv` with its header once; reads the PR, its reviews, its top-level comments and its commits from the API; the line's fields in order: pr, branch, created, merged or `open`, wall hours from creation to merge or now with one decimal, commits, the Codex Bot's reviews, its top-level comments with a `P[01] Badge`, those with a `P[23] Badge`, the local-review files whose `pr:` line names the PR, the update-branch merge commits, the recording time; appends the line and prints it) with the repository root from `git rev-parse --show-toplevel` and an shdoc header.
3. `tests/unit/test_chain_github_scripts.py` (new), run by `uv run python -m unittest` without PyYAML, importing only the standard library, each test in a temporary directory holding a git repository (the scripts' root) with the stub `gh` first on PATH; the stub appends each call's argv and stdin to a log and answers from canned files the test writes, keyed on the API path together with the `--jq` expression when one is given (the input calls `pulls/<pr>/comments` twice with different filters, and a filtered call consumes the filter's output, so each canned file holds that call's post-filter output), and on `graphql` for the query (the `--jq` output, one `<comment id> <thread id>` line per unresolved thread); a `pr view --json headRefOid` form is not needed here:
   - `test_resolve_threads_replies_with_the_table_row_and_resolves_only_threads_with_rows`: a GraphQL answer with two unresolved threads; a table with a `fixed:` row for the first; a sweep JSON with a `not-applicable:` disposition for neither: the first thread gets one reply with the `fixed:` sentence and one resolve mutation naming its thread id, the second is reported left open, the exit is 3; with a placeholder third argument and the sweep JSON as the fourth carrying the second thread's `not-applicable:` disposition, both are resolved, the second with the `not-applicable:` sentence, and the exit is 0; `--dry-run` as the third argument logs no reply and no mutation and prints the `would reply+resolve` line.
   - `test_pr_cost_appends_one_ledger_line_from_the_api`: canned PR, reviews, comments (one Bot `P1 Badge` top-level comment, one Bot `P2 Badge` reply that does not count, one other user's comment) and commits (one update-branch merge message): the TSV gets the header and one line with the fields the item names; a second run appends a second line and no second header.

## Out of scope

The review-side scripts (the sibling task), the chain glue (`integrate-pr.sh`, `finish-pr.sh`; it stays outside the repository until every step it calls is a repository script, plan 021 step 6.3), `fill_sweep.py`, `acceptance-front-matter.py`, `orch-audit.sh`, `orch-gate.sh`, `dispatch.sh`, any rule text, the Makefile.

## Check

`uv run python -m unittest tests/unit/test_chain_github_scripts.py -v` green, pasted in the validation file with `shellcheck scripts/orchestrator/resolve-threads.sh scripts/orchestrator/pr-cost.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after PR #355, merged 08:27Z as 5ec86052), pairwise-disjoint from the sibling task's files (`scripts/orchestrator/local-review.sh`, `local-advisory.sh`, `sandbox-scan.sh`, `tests/unit/test_chain_review_scripts.py`, its evidence directory). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `dotfiles-T128-chain-github-scripts-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-chain-github-scripts-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the two test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-github-scripts-a01/task.md>` and the evidence paths.

## Change (round 2, 2026-10-14)

The Codex half's round 1: item 3 added `review-receipt.sh` where plan 021's step 6.3 inventory keeps the receipt as glue (one `printf`); the script, its row, its test, its input and every mention are removed, and the task lands two scripts. Premise 3 counted a phrase across the whole plan file, which the orchestrator's own status line of 08:45Z changed within minutes; it now counts inside the step 6.3 inventory section only.

## Change (round 3, 2026-10-14)

The seat's round 1 on the sibling task applies here too: premises 1 and 3 read untracked files of the orchestrator's checkout (the inputs, plan 021's inventory) that a worker replaying from its worktree on `origin/main` cannot see, so they are removed and the one premise left reads `origin/main`; the inputs' hashes are stated in the intro as facts.

## Change (round 4, 2026-10-14)

The seat's round 3: P2 the stub gh keyed on the API path alone could not serve pr-cost.sh's two differently filtered calls on one path, and the filtered calls consume the filter's output; item 3 now keys the stub on the path plus the `--jq` expression with post-filter canned output, and on `graphql` for the query. P3 item 1 states the positional arguments (the third `--dry-run` or a placeholder, the fourth the sweep), the first-100-threads query and the 90- and 60-character truncations of the printed row; the test's sweep case passes the placeholder.
