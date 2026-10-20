---
format: 2
task_id: dotfiles-T133-result-precheck-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/result-precheck.sh
  - scripts/orchestrator/dispatch.sh
  - .githooks/pre-commit
  - .githooks/pre-push
  - tests/unit/test_result_precheck.py
  - .orchestration/dotfiles-T133-result-precheck-a01/**
after: []
threat_table:
  - control: "the PR adds scripts/orchestrator/result-precheck.sh (the pre-RESULT gate of plan 024 P1-5, programs (4): it runs the checks of item 1 from the seat's own worktree, writes precheck.json and result.txt under the task's evidence directory, prints the sha256 of precheck.json, and exits 1 when any check it ran is not ok)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_precheck_exits_1_and_records_ok_false_for_each_failing_check"
  - control: "the PR edits scripts/orchestrator/dispatch.sh in one place (item 3: an AGMSG-ACCEPTANCE line with status=accepted is checked against the newest AGMSG-RESULT of its task in the history window the script already reads: head= and precheck= present, the precheck.json of that head hashes to precheck=, its head field is the RESULT head or an ancestor whose diff to it is evidence-only; PRECHECK_REQUIRED=1 refuses, unset or 0 warns; every existing refusal stays)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required"
  - control: "the PR adds .githooks/pre-commit (the CI formatting commands on the staged files in their scopes and shellcheck on the staged shell files; exit 1 stops the commit)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure"
  - control: "the PR adds .githooks/pre-push (the secret detector of item 1 applied to the diff of every pushed range read from the hook's stdin; exit 1 stops the push and never prints the matched text)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern"
  - control: "the PR adds tests/unit/test_result_precheck.py (the fixtures of item 4: stub make, shellcheck, uv, codex-free local review, history.sh and agmsg-dispatch on PATH in a temporary directory; temporary git repositories for the hooks and the selector worktree)"
    disposition: "residual: fakes record every argv; nothing reaches a live bus, GitHub or codex; the audit reads each case"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-result-precheck-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: "the branch evidence records under .orchestration/dotfiles-T133-result-precheck-a01/ (report.md, validation.md, sandbox.md, learning.md, precheck.json, result.txt)"
    disposition: "residual: prose, pasted command output and the two JSON or line records item 1 defines; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the scripts as subprocesses under a fake PATH and a temporary HOME; the detector reads a copy of the diff in $TMPDIR and the copy is removed; nothing writes outside the worktree, the evidence directory and $TMPDIR"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts run under bash with set -euo pipefail and python -I through uv run --offline, as dispatch.sh already does; PRECHECK_REQUIRED and PRECHECK_LOCAL_REVIEW are the only environment inputs, both read once and both with a failing-closed default under PRECHECK_REQUIRED=1"
  - control: new or renamed scripts
    disposition: "residual: 1 new script under scripts/orchestrator and 2 new hooks under .githooks, all named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: dispatch.sh already reads the team history through history.sh with an empty agent argument and a bounded window, so item 3 reads the RESULT from that window and adds no second read
    command: /usr/bin/grep -c -E 'history.sh" "\$\{team\}" "" "\$\{limit\}"' scripts/orchestrator/dispatch.sh
    output: |-
      1
  - claim: local-review.sh documents that codex fails inside the Bash sandbox, so a Claude seat cannot run the local review itself and item 1 records that check as deferred to the orchestrator by default
    command: /usr/bin/grep -c 'Run outside the Bash sandbox' scripts/orchestrator/local-review.sh
    output: |-
      1
  - claim: the gate's acceptance-record block has a fixed key set without precheck, so the precheck sha travels in the RESULT line and in a prose line of the record, never as a new JSON key
    command: /usr/bin/grep -n '^RECORD_KEYS = ' scripts/require-crit-review.py
    output: |-
      42:RECORD_KEYS = {"format", "task", "head", "pr", "ledger", "searches", "audit_findings", "dispatch"}
  - claim: none of the new files exists on origin/main
    command: git ls-files .githooks scripts/orchestrator/result-precheck.sh tests/unit/test_result_precheck.py | wc -l
    output: |-
      0
---

# AGMSG-TASK dotfiles-T133-result-precheck-a01 — the pre-RESULT gate (plan 024 P1-5: `result-precheck.sh`, the acceptance-side refusal in `dispatch.sh`, the `.githooks` pre-commit and pre-push)

Written 2026-10-18 by the orchestrator seat from plan 024 (`.orchestration/plans/024-omp-cutover-and-corrective-order.md` wave P-W0, `024-todo.md` row P1-5, `024-design-programs.md` items (4) and (9), `024-design-quality.md` 5.11 Q-A to Q-F). Seat: claude-standard-dot-a009 (worker-c). The precheck lets a seat stop itself before a RESULT, so revise rounds (34 of 98 so far) fall; the hooks stop format failures and secrets before a commit or push. Harness-independent: bash, git, make, uv; nothing under `home/`.

## Item 0 (first, about 15 minutes): park PR B stage 1 as a draft

Your worktree holds `tools/omp-config-render` at 41da91ce with two untracked evidence files under `.orchestration/dotfiles-T129-omp-config-render-a01/`. Commit them on that branch (`git -c commit.gpgsign=false commit`), `git push origin tools/omp-config-render`, open the PR as a draft (`gh pr create --draft --head tools/omp-config-render --title "feat(agents): render omp's default model role from the manifest (T129 omp-config-render a01)" --body "Plan 024 phase 2 B stage 1, parked as a draft under plan 024 0b; resumed in D-W0."`), and send one line on the bus for that task: `AGMSG-PONG v1 task_id=dotfiles-T129-omp-config-render-a01 status=alive note=parked-draft-pr-<n>-head-<sha40>`. No report, validation or RESULT for that task now; it resumes in phase 2. Then `git switch -c tools/result-precheck-a01 --no-track origin/main` and start item 1. A `.git/config.lock` left by an earlier attempt is the orchestrator's to remove: send `AGMSG-PONG v1 status=blocked` naming it.

## Goal

A seat runs one command before its RESULT that performs the repository's own checks on its head, records the outcome as evidence in the PR tree, and refuses to let a RESULT through with a failed check; the orchestrator's dispatch of an accepted ACCEPTANCE verifies that evidence against the RESULT; two git hooks stop format and secret failures before CI sees them.

## Files

1. `scripts/orchestrator/result-precheck.sh <task> [--tests <unittest module>...] [--previous-head <sha40> --check <selector>...] [--secrets <diff-file>]` (new, bash, `set -euo pipefail`, shdoc comments; run from the root of the seat's worktree, `git rev-parse --show-toplevel`). Checks, each recorded as `{name, ok, exit, output_sha256}` (the output itself goes to `.orchestration/<task>/precheck-<name>.log`, masked with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets`): `unit-test` = `make unit-test`, or with `--tests` `uv run python -m unittest <modules> -v`; `render-check` = `make render-check`; `format` = the three formatting commands of CI's test job in their exact scope (Amendment 1: `shfmt --indent 4 --space-redirects --diff` on `git ls-files 'install/**/*.sh' 'scripts/**/*.sh'`, `ruff format --config ruff.toml --check` on `git ls-files '*.py'`, `prettier --check` on `git ls-files '*.md'`; each read from `.github/workflows/test.yaml`'s `Run \`shfmt\`` and `Check Python and Markdown formatting` steps and pasted in the script's header comment, so a scope change in CI is a one-line change here), exit 0 for all three being the zero-difference condition; `shellcheck` = `shellcheck` on every file of `git diff --name-only origin/main...HEAD` that ends in `.sh` or whose first line is a bash or sh shebang; `secrets` = the diff `git diff origin/main...HEAD` written to a `mktemp` file under `$TMPDIR`, the masker run on that copy, and the copy compared byte for byte with the original: a difference is a match, recorded as a count only, never the text (the copy is removed by a trap); `local-review` = under `PRECHECK_LOCAL_REVIEW=seat` runs `scripts/orchestrator/local-review.sh <task> <head> <pr>` (the PR number from `gh pr view --json number`) and requires exit 0; under the default `PRECHECK_LOCAL_REVIEW=orchestrator` it is recorded as `{name: local-review, ok: null, deferred: orchestrator}` and does not fail the precheck, with the header comment `shortcut: a Claude seat cannot run codex inside its Bash sandbox (local-review.sh's header), so the orchestrator's acceptance runs the local review on the head as today; upgrade to seat when the seats run omp (plan 024 phase 2 B)`. `--secrets <diff-file>` runs only the secrets check on the named file and exits 0 or 1 (the pre-push hook's entry). With `--previous-head` and one or more `--check tests/<file>::<name>` selectors (the `check=` form of a `status=revise` ACCEPTANCE): `git worktree add --detach <mktemp dir> <previous-head>`, each selector run there as `uv run python -m unittest tests.unit.<module> -k <name>` and required to fail, then run in the current tree and required to pass, both exit codes and output sha256 recorded under `selectors[]`; the worktree is removed with `git worktree remove --force <dir>` (never `git worktree prune`). Output: `.orchestration/<task>/precheck.json` = `{head: <git rev-parse HEAD at run time>, tree: <HEAD^{tree}>, generated_at, checks: [...], selectors: [...]}`, and `.orchestration/<task>/result.txt` = the RESULT line to be sent with `head=` set to that same head (the final head includes these two files, so the bus RESULT replaces `head=` with the final head and keeps every other field). The last stdout line is `precheck=<sha256 of precheck.json>`; exit 0 when every check that ran is ok (a deferred check is neither), exit 1 otherwise, exit 2 on usage. The worker commits precheck.json, result.txt and the logs as the last commit, whose diff from `precheck.json`'s `head` is only under `.orchestration/<task>/`, and writes `precheck=<sha256>` into the RESULT.
2. `.githooks/pre-commit` (new): from `git rev-parse --show-toplevel`, the three formatting commands of item 1's `format` check restricted to the staged files in their scopes (Amendment 1) and `shellcheck` on the staged files (`git diff --cached --name-only --diff-filter=ACMR`) that end in `.sh` or carry a bash or sh shebang; any failure prints the failing command and exits 1. `.githooks/pre-push` (new): reads the `<local ref> <local sha> <remote ref> <remote sha>` lines from stdin; for each line with a non-deleted local sha, the diff is `git diff <remote sha>..<local sha>` when the remote sha is not all zeros, else `git diff $(git merge-base origin/main <local sha>)..<local sha>`; each diff goes to a `mktemp` file under `$TMPDIR` and through `scripts/orchestrator/result-precheck.sh --secrets <file>`; a match exits 1 with the count and the range, never the text. Both hooks are bash with shdoc comments and run under `set -euo pipefail`. Setting `core.hooksPath` in the seats' worktrees is P1-7's (`herdr-agents`), not this task's.
3. `scripts/orchestrator/dispatch.sh`: one new block, for a line `AGMSG-ACCEPTANCE v1 ... status=accepted` only. From the pre-send history window the script already reads (premise 1), take the newest row whose body starts `AGMSG-RESULT v1` and carries this line's `task_id=`; read its `head=` (40 hex) and `precheck=` (64 hex); `git cat-file -e <head>^{commit}` in this checkout; `git show <head>:.orchestration/<task>/precheck.json` must hash (sha256) to `precheck=`, its `head` field must be `<head>` or an ancestor of it (`git merge-base --is-ancestor`) such that `git diff --name-only <field> <head>` lists only paths under `.orchestration/<task>/`. Any missing row, field, object or mismatch: with `PRECHECK_REQUIRED=1` exit 1 naming the field (`precheck: <field> <reason>`), nothing sent; otherwise print `precheck: warning <field> <reason>` on stderr and continue (plan 024 0d: staged enforcement, `PRECHECK_REQUIRED` unset or `0` until the orchestrator flips it after the four seats' branches contain this task's merge). No other behaviour of the script changes; the header's description gains one paragraph.
4. `tests/unit/test_result_precheck.py` (new; the pattern of `tests/unit/test_orchestrator_tools.py`: stubs on PATH in a temporary directory recording argv to a calls file, `history.sh` and `agmsg-dispatch` stubbed, `AGMSG_SCRIPTS` pointed at the stub directory, dispatch.sh copied beside a stub checker): `test_precheck_exits_1_and_records_ok_false_for_each_failing_check` (one case per check: make unit-test, make render-check, make format, shellcheck, a diff the stub masker changes, local review under `PRECHECK_LOCAL_REVIEW=seat` exiting 3; each alone makes exit 1 and `ok: false` for that name and `ok: true` for the others; all green makes exit 0 and the last line `precheck=<sha256 of the file>`); `test_precheck_records_the_local_review_as_deferred_by_default` (no codex on PATH, `ok: null`, exit 0, the shortcut comment present in the script); `test_precheck_selector_proof_requires_red_on_previous_head_and_green_on_head` (a temporary repository with two commits; a selector passing on both fails the precheck; red then green passes; the temporary worktree is removed; `git worktree prune` is never called, asserted from the stub git log or by running real git and listing worktrees); `test_precheck_secrets_mode_counts_and_never_prints_the_match` (`--secrets` on a file holding a value the real masker masks: exit 1, stdout and stderr free of that value); `test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required` (history holds a RESULT with `head=` and `precheck=`; a temporary repository provides the head with a precheck.json: equal hash and an evidence-only ancestor diff passes; a missing `precheck=`, a hash mismatch, a `head` field whose diff touches a path outside the evidence directory, and a missing object each exit 1 under `PRECHECK_REQUIRED=1` with nothing sent, and each warns and sends under `PRECHECK_REQUIRED=0`); `test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure` and `test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern` (a temporary repository with `core.hooksPath` pointing at the repository's `.githooks`, stub make and shellcheck on PATH; a real push to a bare temporary remote with a secret-like line fails, a clean one passes). Fixture lines count against the test cap.

## Out of scope

`herdr-agents` and `core.hooksPath` (P1-7); the record generator and `dispatch.sh --next` (P1-6); `verdict.sh` (P1-4a, which reads precheck.json through the same rule); any key in the acceptance record's JSON block (premise 3); CI (P1-3 and P1-11); any file under `home/`.

## Check

`make unit-test`, `make render-check`, `make format`, `shellcheck` and `shfmt -d` on the three new scripts clean, `uv run python -m unittest tests.unit.test_result_precheck tests.unit.test_orchestrator_tools -v` green, and the precheck run on your own head with the task's test selection (Amendment 2: `scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a01 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools`) with exit 0 and its `precheck=` line, plus the default run's exit code and the sorted-names comparison of its failures with a pristine origin/main worktree in the same sandbox, all pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 350 changed lines outside `tests/` and `.orchestration/`, 450 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main` after item 0. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-result-precheck-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears), `task_copy=<sha256 of .orchestration/dotfiles-T133-result-precheck-a01/task.md>`, `precheck=<sha256 of precheck.json>` and `parked_pr=<the item 0 PR number>` in the RESULT. This task is `security: true`: the orchestrator runs the task-level audit and a second review on the `security` profile on the final head before the gate (plan 024 5.11 Q-A).

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-result-precheck-a01.md: OK
premises 1 to 4: outputs pasted at write time (2026-10-18 13:3x JST)
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-result-precheck-a01.md
```

## Amendment 1 (round 1, 2026-10-18T04:34Z)

a009's question PONG (04:33:12Z): `make format` exits 2 on origin/main 99a4a80f itself, because its `shfmt --diff .` covers twelve tracked files CI's shfmt step never formats (ten under `.orchestration/tasks/*-input/`, `home/dot_claude/hooks/executable_project-map-reload.sh`, `tests/install/macos/common/brew.bats`), while CI runs shfmt on `install/**/*.sh` and `scripts/**/*.sh` only. Decided by the orchestrator by default: option (b). The precheck mirrors CI, so the `format` check and the pre-commit hook run CI's three formatting commands in CI's scopes (item 1 and item 2 read accordingly, the threat row of the hook likewise); the twelve files are out of scope here (CI's blind spot is a separate task, if any). The Check's "precheck exit 0 on your own head" holds under (b).

## Amendment 2 (round 1, 2026-10-18T05:29Z)

a009's question PONG (05:20:02Z): `make unit-test` fails 296 tests inside a Claude seat's Bash sandbox (test_require_crit_review 136, test_herdr_agents 82, test_agent_stop_gate 28, …), identically on a pristine origin/main 99a4a80f worktree in the same sandbox and none in this task's modules, so the Check's "precheck exit 0 on your own head" cannot hold with the default `unit-test` check. Decided by the orchestrator by default: option (a). The Check's proof run uses `--tests` with the task's two modules (the form item 1 already defines), and the validation file pastes the default run's exit and the baseline comparison; CI's `make unit-test` on ubuntu and macOS stays the authority for the full suite. The script's header gains `shortcut: inside a Claude seat's sandbox the full suite fails on sandbox-denied operations, so a seat runs the precheck with --tests on its task's modules and CI runs the full suite; upgrade when the seats run omp (plan 024 phase 2 B)`. No other change. INV-6: amendments 2 (both answer the sandbox reality the task text assumed away: format scope, full-suite runs); the orchestrator records the pattern for the P1-12 task generator (a Check command is run in a seat before dispatch). No further amendment on this task; a third need is a hold and a re-plan.
