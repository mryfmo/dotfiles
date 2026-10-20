---
format: 2
task_id: dotfiles-T132-merge-train-builder-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/train.sh
  - tests/unit/test_train.py
  - .orchestration/dotfiles-T132-merge-train-builder-a01/**
after: []
threat_table:
  - control: "the PR adds scripts/orchestrator/train.sh (the train builder: build, push, wait, merge in order with a tree-prefix check after each merge, split on failure; a train-pr fallback mode)"
    disposition: "closed: tests/unit/test_train.py::test_merge_mode_merges_each_head_in_order_and_main_matches_the_train_prefix"
  - control: the PR adds tests/unit/test_train.py (a fake gh first on PATH and a real git in a temporary origin, main checkout and seed clone)
    disposition: "residual: the fake gh answers from files the case writes and performs a squash merge on the temporary origin where GitHub would; HOME, TMPDIR and PATH point into the TemporaryDirectory; no network and no real gh"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T132-merge-train-builder-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T132-merge-train-builder-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the script touches the main checkout only through git -C <main> fetch and git worktree add/remove of a detached worktree under $TMPDIR (never its index, HEAD or branches); its only remote writes are one push of a new train/<date>-<n> branch and the gh merges it was asked for; the tests run it against a temporary origin, so no test pushes to or merges anything on GitHub"
  - control: "workflow and interpreter or environment inputs"
    disposition: "residual: no workflow file is in allowed_files; the script runs under bash with set -euo pipefail and resolves gh, git and date to absolute paths outside a shims directory under env -i before any fetch or checkout (chain-integrate.sh's pick form, the trusted-root class); its inputs are the mode, the main checkout path and <pr>:<40-hex> heads, each regex-checked, and TRAIN_POLL_SECONDS, TRAIN_WAIT_MAX and TRAIN_DATE, each digit-checked; every gh answer is read through --jq into a compared variable, never eval'd"
  - control: new or renamed scripts
    disposition: "residual: train.sh is the one declared new script; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "closed: tests/unit/test_train.py::test_the_script_text_issues_only_the_plain_pinned_merge_form"
  - control: orchestrator effect update-branch
    disposition: "residual: the script issues no gh pr update-branch: in merge mode strict up-to-date is off and a head is merged as audited; in train-pr mode a base that moved makes gh refuse the merge, the script stops, and the orchestrator runs the step-10 update-branch by hand, after which CI, the sweep and the audit run again"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: neither of this task's files exists on origin/main, nor do the three in-flight scripts this task must not touch (integrate-seat.sh and result-precheck.sh of PR #393, chain-finish.sh of PR #378)
    command: git ls-tree -r --name-only origin/main -- scripts/orchestrator/train.sh tests/unit/test_train.py scripts/orchestrator/integrate-seat.sh scripts/orchestrator/result-precheck.sh scripts/orchestrator/chain-finish.sh | wc -l | tr -d ' '
    output: |-
      0
  - claim: the SKILL's merge rule on origin/main is the plain pinned squash form, which the script reproduces one call per PR
    command: git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c -F 'gh pr merge <pr> --squash --match-head-commit <audited head sha>'
    output: |-
      1
  - claim: the decision this task implements is recorded in the working tree's decisions.tsv (not yet on origin/main; it lands with the next boundary commit, which precedes this dispatch)
    command: a=$(/usr/bin/grep -c '^D-train-strict-off' .orchestration/decisions.tsv); b=$(git show origin/main:.orchestration/decisions.tsv | /usr/bin/grep -c '^D-train-strict-off' || true); echo "$a $b"
    output: |-
      1 0
---

# AGMSG-TASK dotfiles-T132-merge-train-builder-a01 — the merge-train builder: one CI run on the train tip, pinned squash merges in order, a tree-prefix check after each

Written 2026-10-18 by the orchestrator seat from the operator's specification of 08:1x JST and decision `D-train-strict-off` (premise 3): the primary mode is strict up-to-date OFF (the user turns it off as admin once the train is merged and its first real run passes); the train-PR mode exists only while strict is still ON. The integration seat script (`scripts/orchestrator/integrate-seat.sh`, PR #393, unmerged) will call this builder later; this task does not touch it (premise 1): the builder is standalone and takes its inputs as arguments. The gate's train-evidence extension waits for PR #400 and is out of scope. The CI side (the `train/**` trigger) is the sibling task `dotfiles-T132-merge-train-ci-a01`; this script's tests need none of it, a live run does.

## Goal

`scripts/orchestrator/train.sh merge <main> <pr>:<sha> […]` builds `train/<date>-<n>` = `origin/main` plus the given heads squashed in order, pushes it so CI runs once on the tip, waits for that run to be green, then merges each PR in order with the plain pinned squash form and checks after each merge that the new `origin/main` tree equals the train commit at that prefix; on any failure it stops, prints the shorter train (the first half of the remaining heads) and the held heads, and exits nonzero. `train-pr` mode opens the train as a PR and merges that PR instead.

## Files

1. `scripts/orchestrator/train.sh` (new, shdoc header as `chain-integrate.sh`: `@file`, `@brief`, `@description`, one `@arg` per argument, every `@exitcode`, `@example`; `set -euo pipefail`; under 200 lines). Interface: `train.sh <merge|train-pr> <main checkout> <pr>:<sha40> [<pr>:<sha40> …]`; environment `TRAIN_POLL_SECONDS` (default 30), `TRAIN_WAIT_MAX` (default 3600 seconds), `TRAIN_DATE` (default `date -u +%Y%m%d`; tests pin it); all three digit-checked. Steps, each one command under `set -e`, never an `&&` list across steps:
   - (1) arguments: the mode is one of the two words; `<main>` resolves with `cd -- … && pwd -P`; each head matches `^[0-9]+:[0-9a-f]{40}$`, at least one, no PR number twice; `gh`, `git` and `date` resolved as `chain-integrate.sh`'s `pick` does (absolute, outside shims, under `env -i`), before any fetch. Exit 10 on any refusal.
   - (2) fetch: `git -C <main> fetch -q origin main` and, per head, `git -C <main> fetch -q origin "+pull/<pr>/head:refs/remotes/pr/<pr>"`; `git rev-parse refs/remotes/pr/<pr>` must equal the given sha, else exit 10 `head moved: #<pr> is <actual>` (the pin is the audited head; nothing newer is ever built in).
   - (3) name: `n` = 1 + the count of `git ls-remote --heads origin "refs/heads/train/${TRAIN_DATE}-*"`; branch `train/<TRAIN_DATE>-<n>`.
   - (4) build: `git -C <main> worktree add -q --detach <tmp> origin/main` (`<tmp>` under `$TMPDIR`, removed by a trap with `git worktree remove --force`); per head in order `git -c commit.gpgsign=false merge -q --squash <sha>` then `git -c commit.gpgsign=false commit -q -m "train: #<pr> <sha>"` (the same squash GitHub performs: the merge base of main and the head, so the train's commit `i` is the tree main will have after merge `i`); the commit shas go into `prefix[i]`; a conflict exits 20 `conflict at #<pr>` with the split line (below) over the heads from that PR on, and nothing is pushed. An empty squash (a head already on main) exits 20 too.
   - (5) push: `git -C <tmp> push -q origin HEAD:refs/heads/train/<name>`; print `train: <name> <tip>`.
   - (6) wait (merge mode): every `TRAIN_POLL_SECONDS`, `gh run list --branch train/<name> --json headSha,workflowName,status,conclusion --jq '.[] | select(.headSha == "<tip>") | [.workflowName, .status, .conclusion] | @tsv'`; done when each of `Unit test`, `Snippet install` and `Agent assets` (the `name:` of the three required-check workflows) is `completed`; any conclusion other than `success` exits 22 `train CI failed: <workflow> <conclusion>` with the split line; `TRAIN_WAIT_MAX` elapsed exits 21.
   - (7) merge loop (merge mode): per head in order, exactly `gh pr merge <pr> --squash --match-head-commit <sha>` (that argv and nothing else: no `--admin`, `--auto`, `--delete-branch`, `--subject`, `--body`); a nonzero exit stops with exit 24 `merge refused: #<pr>` and the split line over the heads not yet merged (with strict still on, gh refuses here: the message names `train-pr` mode). Then `git -C <main> fetch -q origin main` and the tree-prefix check: `git -C <main> rev-parse origin/main^{tree}` must equal `git -C <tmp> rev-parse <prefix[i]>^{tree}`; a mismatch exits 23 `tree mismatch after #<pr>: main <tree> train <tree>` with the split line over the heads not yet merged (the merged ones are on main and stay; the orchestrator judges main). Print `merged: #<pr> <sha> main <new sha>` per PR and `train: done <n> merged` at the end, exit 0.
   - (8) train-pr mode replaces (6) and (7): `gh pr create --draft --head train/<name> --title "train: <name>" --body "<one line per head: #<pr> <sha>>"` (the body is a `--body-file` under `$TMPDIR` if a shell-safe one-line body is not possible); read the number from gh's URL; `gh pr checks <n> --required --watch` (nonzero: exit 22 with the split line); `gh pr ready <n>`; exactly `gh pr merge <n> --squash --match-head-commit <tip>`; then the tree check of `origin/main^{tree}` against `<tip>^{tree}` (exit 23 on mismatch); print `train-pr: #<n> merged; close each member PR by hand: gh pr close <pr> --comment "merged through train PR #<n>"` for the orchestrator (the script closes nothing). The header's description documents this order and that the mode is for strict ON only: it costs a second CI run (the `train/**` push and the pull_request event) and lands one squash commit for the whole train, so per-PR history is lost.
   - the split line, printed on every nonzero exit after (4): `next train: <first ceil(k/2) remaining heads, space-separated in the input form>` and `held: <the rest>`; the caller re-runs the script with the first list (the bisect), the script re-runs nothing itself.
2. `tests/unit/test_train.py` (new; the fixture form of `tests/unit/test_chain_glue.py`: a bare origin with `main` and `refs/pull/{11,12,13}/head`, a main checkout clone, a seed clone, `GIT_ENV`, `TMPDIR`, `HOME` and `PATH` inside the TemporaryDirectory, `TRAIN_DATE=20261018`, `TRAIN_POLL_SECONDS=0`). The fake `gh` logs every argv to `$CALLS/gh.log` and answers: `run list` prints `$CALLS/runs.tsv` (default: the three workflows `completed success`); `pr merge <n> --squash --match-head-commit <sha>` performs on the seed clone what GitHub does (fetch main and the pull ref, checkout main, `merge --squash <sha>`, commit, push main), writes an extra file into the squash first when `$CALLS/merge-<n>-extra` exists, exits with `$CALLS/merge-<n>-status` when present, and for PR 99 (the train PR) squashes the train tip; `pr create` prints `https://github.com/o/r/pull/99`; `pr checks 99` exits with `$CALLS/checks-status`; `pr ready` logs only. Cases, each asserting on `gh.log`, the exit code, stdout and the temporary origin: (a) `test_merge_mode_merges_each_head_in_order_and_main_matches_the_train_prefix` (three `pr merge` lines in order with the given shas; `origin/main^{tree}` equals the pushed train tip's tree; exit 0); (b) `test_a_tree_mismatch_after_a_merge_stops_and_prints_the_split` (`merge-12-extra`: exit 23, no `pr merge 13`, output names `#12` and `next train: 13:<sha>`); (c) `test_a_red_train_run_splits_the_heads_and_merges_nothing` (`runs.tsv` with `Unit test completed failure`: exit 22, no `pr merge`, `next train: 11:… 12:…` and `held: 13:…`); (d) `test_a_conflicting_head_stops_before_the_push` (head 13 edits the line head 12 edits: exit 20, empty `gh.log`, no `train/` branch on the origin); (e) `test_a_moved_head_is_refused_before_anything_is_built` (a sha that is not the pull ref: exit 10, nothing pushed); (f) `test_the_script_text_issues_only_the_plain_pinned_merge_form` (over the script's text: no `--admin`, `--auto`, `--delete-branch`, `--rebase`, `--merge ` token anywhere; every `gh … pr merge` occurrence is the exact plain form `"${gh}" pr merge "<var>" --squash --match-head-commit "<var>"`, and `pr update-branch` is absent); (g) `test_train_pr_mode_opens_the_train_pr_and_merges_it_pinned_to_the_tip` (`pr create --draft --head train/20261018-1 …`, `pr checks 99 --required --watch`, `pr ready 99`, `pr merge 99 --squash --match-head-commit <tip>` in that order, no per-PR merge, `origin/main^{tree}` equals the tip's tree, the close-by-hand line printed); (h) `test_the_train_name_counts_the_days_existing_trains` (an existing `train/20261018-1` on the origin: the push is `train/20261018-2`). The real `git` is on PATH after the fake `gh` (`/usr/bin:/bin` as `test_chain_glue.py`).

## Out of scope

`scripts/orchestrator/integrate-seat.sh`, `result-precheck.sh` (PR #393), `chain-finish.sh` (PR #378), `chain-integrate.sh` (PR #390), `resolve-threads.sh` (PR #375) and every other existing orchestrator script; the gate (`scripts/require-crit-review.py`, `orch-gate.sh`) and its train-evidence extension (after PR #400); any workflow file (the sibling task); the SKILL and rule texts (the orchestrator's step-10 sentence for the train is a later records or docs task); closing member PRs in train-pr mode; deleting train branches (the repository keeps merged branches).

## Check

Pasted in the validation file: `make render-check` (exit 0; the standing check), `shellcheck -x scripts/orchestrator/train.sh` (CI's form: the `scripts/*.sh` pathspec of `test.yaml`'s "Run ShellCheck" step matches `scripts/orchestrator/` too) and `mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d scripts/orchestrator/train.sh` (CI's form) both clean, `uv run python -m unittest tests/unit/test_train.py -v` green with the eight cases named above, `uv run python -m unittest tests/unit/test_chain_glue.py -v` still green (the fixture form is copied, not shared), `! /usr/bin/grep -E -e '--admin|--auto' scripts/orchestrator/train.sh` (exit 0), and `git diff --numstat origin/main...HEAD`. No live run: the script is never run against GitHub in this task (its first live run is the orchestrator's, after both T132 PRs merge and under the operator's eye). Caps: under 200 changed lines outside `tests/` and `.orchestration/` (plan 021 step 7.2: the script itself; a design that needs more is a `PONG status=question` before writing it, never a cut of a check) and under 1000 added under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main`; under the merge-gate policy the worker opens its PR with the plain draft create form itself (`gh pr create --draft --head <branch>`). No in-flight PR touches either file (premise 1; the NOTES list the five in-flight branches' files). The Completion clause of `.orchestration/tasks/dotfiles-T129-anthropic-auth-runtime-check-a01.md` applies as written, with `dotfiles-T132-merge-train-builder-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears, before the PR's dispositions, C-51) and `task_copy=<sha256 of .orchestration/dotfiles-T132-merge-train-builder-a01/task.md>` in the RESULT, which also pastes the eight test names from the unittest output and the line count of the script.

## VERIFY (the orchestrator closes each before dispatch; a closed item becomes Amendment 1 text, an open one a decided default)

- VERIFY 1: GitHub's squash merge tree equals a local `git merge --squash` of the head onto the current main (same merge base, same rename detection) for the clean merges the train carries; a difference is exactly what the tree-prefix check reports (exit 23), so this is a design fact, not a correctness risk. Default: as item 1 (4) and (7) write; the first live train's output is pasted in the acceptance record.
- VERIFY 2: `gh run list --branch … --json headSha,workflowName,status,conclusion` on the seat's gh (2.102.0 on the orchestrator's Mac prints `-b, --branch` and `-c, --commit` in `gh run list --help`). Default: `--branch` plus the `headSha` filter, as written.
- VERIFY 3: the three workflow `name:` values (`Unit test`, `Snippet install`, `Agent assets`, read from `origin/main` on 2026-10-18) are what `gh run list` reports as `workflowName`. Default: those three literals in the script.
- VERIFY 4: whether PR #400's `gh-merge-gate` PreToolUse hook (it gates `gh pr merge` and `gh pr update-branch` on Claude seats) accepts the script's merge argv when run from the integration seat. Default: the plain form of item 1 (7) is the form the hook is written for; a refusal there is a finding for #400's lineage, not this task.
- VERIFY 5: `gh pr create` needs `--title` and `--body` (or `--fill`) to run non-interactively. Default: `--title` and `--body` as item 1 (8) writes.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T132-merge-train-builder-a01.md: <pending>
premise 1: <pending>
premise 2: <pending>
premise 3: <pending>
masked <n> match(es) in .orchestration/tasks/dotfiles-T132-merge-train-builder-a01.md
```
