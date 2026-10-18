---
format: 2
task_id: dotfiles-T133-result-precheck-a02
kind: code
security: true
allowed_files:
  - scripts/orchestrator/result-precheck.sh
  - scripts/orchestrator/dispatch.sh
  - .githooks/pre-commit
  - .githooks/pre-push
  - tests/unit/test_result_precheck.py
  - .orchestration/dotfiles-T133-result-precheck-a02/**
after: []
reset_of: [dotfiles-T133-result-precheck-a01]
threat_table:
  - control: "scripts/orchestrator/result-precheck.sh (the pre-RESULT checks, masked logs, selector proof and evidence writer propagate prerequisite and command failures)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_precheck_records_failed_commands_as_not_ok"
  - control: "scripts/orchestrator/dispatch.sh (the acceptance-side precheck binds the newest ready RESULT, hashes, code head, required checks and requested selectors under PRECHECK_REQUIRED)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_dispatch_rejects_malformed_checks_and_missing_requested_selectors"
  - control: ".githooks/pre-commit (CI's three formatting commands in their staged scopes and shellcheck run against index blobs)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree"
  - control: ".githooks/pre-push (every pushed commit's changed blob content is scanned despite binary attributes and NUL bytes, without printing matches)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit"
  - control: "tests/unit/test_result_precheck.py (the retained cases and the three local-review regressions use temporary repositories and recorded fake commands)"
    disposition: "residual: temporary repositories, a temporary HOME, fake bus commands and generated token fixtures isolate the tests; the final-head audit checks that the real masker and assertions exercise the stated controls."
  - control: ".orchestration/dotfiles-T133-result-precheck-a02/** (the reset task's branch artifacts)"
    disposition: "residual: artifacts stay in this task's directory, distinguish inherited observations from fresh results, and bind their commands, hashes and tested heads for the final-head audit."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-result-precheck-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-result-precheck-a01/task.md)"
    disposition: "residual: the a02 copy is byte-identical to the dispatched text and its own SHA256 appears in the TASK and RESULT; the orchestrator verifies replacement and byte identity at acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-result-precheck-a02/ (report.md, validation.md, sandbox.md, learning.md, revise.yaml, precheck.json, result.txt and precheck-*.log)"
    disposition: "residual: records and logs are masked before committing, precheck.json binds the last code commit, and the final commit changes only this task's evidence; the audit checks those claims and the hashes."
  - control: "task metadata"
    disposition: "residual: the orchestrator checks the dispatched front matter with task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; the byte comparison covers later metadata changes."
  - control: "metadata separators"
    disposition: "residual: the first document separators bound the YAML front matter and the dispatched-file byte comparison covers the entire task copy and its separators."
  - control: "in-process effects"
    disposition: "residual: subprocesses use temporary repositories and a temporary HOME; temporary scan files and detached proof worktrees are removed, and a failed prerequisite cannot become a successful check."
  - control: "workflow and interpreter or environment inputs"
    disposition: "residual: no workflow or interpreter file changes; Bash scripts retain set -euo pipefail, embedded Python uses -I, and the existing masker runs through uv; PRECHECK_REQUIRED defaults to warning, PRECHECK_LOCAL_REVIEW defaults to explicit orchestrator deferral, and invalid values are rejected."
  - control: "new or renamed scripts"
    disposition: "residual: the inherited precheck script and two hooks remain the only new executables, all named in allowed_files and the RESULT; the final-head audit compares the full inventory."
  - control: "orchestrator effect merge"
    disposition: "residual: the orchestrator merges only with gh pr merge --squash --match-head-commit <audited head> after the integration gate; no local merge or push to main is authorized."
  - control: "orchestrator effect update-branch"
    disposition: "residual: gh pr update-branch changes the head, so CI, the feedback sweep, task-level audit and security review bind the resulting final head before the gate."
  - control: "orchestrator effect forced worker removal"
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state in the acceptance record."
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

# AGMSG-TASK dotfiles-T133-result-precheck-a02 — INV-6 reset of dotfiles-T133-result-precheck-a01 (plan 006 S2; plan 024 P1-5)

This text is the independent redesign by a review-profile context other than the author of a01. Plan 006 INV-6 stopped a01 at S2 after two amendments. The chain stopped at the local review of `a5cb73b489235bb177e346dd00dd9aca28a432e8` in `.orchestration/validation/dotfiles-T133-result-precheck-a01-local-review-a5cb73b.md`. No task-level audit ran on that head.

PR #411 continues under this task on the same branch, `tools/result-precheck-a01`. The reviewed implementation is the starting point. The next push replaces `.orchestration/dotfiles-T133-result-precheck-a01/task.md` with this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-result-precheck-a02/task.md`. The orchestrator removes the predecessor task copy as reset bookkeeping; worker edits stay within `allowed_files`. The a01 records retain their stopped status and historical counters. Its item 0 is complete and its parked draft is PR #406.

The four premises preserve a01's write-time observations verbatim. The worker's a01 report, `revise.yaml` and `precheck.json` remain historical evidence. Fresh validation and proof records use this task's own evidence directory.

## Goal

A seat runs one command before its RESULT to execute the repository's checks on its code head, record their outcomes and stop on a failed check. The orchestrator's accepted ACCEPTANCE verifies that evidence against the newest RESULT. The pre-commit hook checks staged content and the pre-push hook scans the content of every pushed commit's changed blobs, including content Git marks as binary.

## Files

1. `scripts/orchestrator/result-precheck.sh <task> [--tests <unittest module>...] [--previous-head <sha40> --check <selector>...] [--secrets <diff-file>]` retains the inherited Bash implementation, `set -euo pipefail` and English shdoc comments. It runs from `git rev-parse --show-toplevel` and refuses uncommitted changes outside `.orchestration/<task>/`, so evidence describes committed code. Its `--staged` mode remains the shared implementation used by the pre-commit hook.

   Each executed check records `{name, ok, exit, output_sha256}`. Its output goes to `.orchestration/<task>/precheck-<name>.log`, masked with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets` before its hash is recorded. A masking failure fails the run, removes unmasked logs and produces no successful evidence record.

   The default `unit-test` check runs `make unit-test`. `--tests` selects `uv run python -m unittest <modules> -v` instead. The `render-check` check runs `make render-check`. The `format` check runs CI's three formatting commands in CI's scopes: `shfmt --indent 4 --space-redirects --diff` on tracked `install/**/*.sh` and `scripts/**/*.sh`, `ruff format --config ruff.toml --check` on tracked `*.py`, and `prettier --check` on tracked `*.md`. The scopes come from `git ls-files` with CI's pathspecs, and all three commands must exit 0. The script header pastes the corresponding three command lines from `.github/workflows/test.yaml`'s ``Run `shfmt` `` and `Check Python and Markdown formatting` steps. CI's tool selection and repository formatter configuration remain authoritative. The `format` check does not use `make format`'s broader shell scope.

   The `shellcheck` check runs `shellcheck -x` on every existing file changed by `git diff --name-only origin/main...HEAD` that ends in `.sh` or has a Bash or sh shebang. The `secrets` check writes `git diff --text origin/main...HEAD` to a temporary file under `$TMPDIR`, masks a copy and compares the two byte for byte. A difference fails the check and reports only the match count. Temporary scan files are removed by an EXIT trap. Item 6 governs every command failure in these checks.

   `PRECHECK_LOCAL_REVIEW=orchestrator` is the default. It records `{name: local-review, ok: null, deferred: orchestrator}` and leaves the local review to the orchestrator on the final head. `PRECHECK_LOCAL_REVIEW=seat` runs `scripts/orchestrator/local-review.sh <task> <head> <pr>`, obtains the PR number through `gh pr view --json number` and requires exit 0. The header retains the line `shortcut: a Claude seat cannot run codex inside its Bash sandbox (local-review.sh's header), so the orchestrator's acceptance runs the local review on the head as today; upgrade to seat when the seats run omp (plan 024 phase 2 B)`. It also retains `shortcut: inside a Claude seat's sandbox the full suite fails on sandbox-denied operations, so a seat runs the precheck with --tests on its task's modules and CI runs the full suite; upgrade when the seats run omp (plan 024 phase 2 B)`.

   `--secrets <diff-file>` runs only the secrets detector on that file and exits 0 for no match and 1 for a match or detector failure. `--staged` runs only the staged formatting and shellcheck checks. `--previous-head` with repeated `--check tests/<file>::<name>` selectors creates a detached temporary worktree at that commit, runs each selector there with `uv run python -m unittest tests.unit.<module> -k <name>` and requires red there and green in the current tree. Both exit codes and hashes of their masked outputs are recorded in `selectors[]`. The worker records the revise request's `previous_head` and complete `check` list in `revise.yaml`. Cleanup uses `git worktree remove --force <dir>` and never `git worktree prune`.

   `precheck.json` contains `{head, tree, generated_at, checks, selectors}`. Its `head` is the last code commit tested by the run and its `tree` is that commit's `HEAD^{tree}`. `result.txt` contains the RESULT template with that code head. The last stdout line is `precheck=<sha256 of precheck.json>`. Exit 0 requires every executed check and every selector proof to succeed; the explicit deferred local review is neither a passing check nor a failure. A failed check exits 1 and usage errors exit 2. The worker commits `precheck.json`, `result.txt` and the masked logs in the final evidence-only commit. Every path changed between the recorded code head and the final head is under `.orchestration/<task>/`. The bus RESULT carries the final head and the unchanged precheck hash; its completed template's other fields remain unchanged. Code changes after a proof require a fresh proof before a new final evidence-only commit.

2. `.githooks/pre-commit` delegates to the shared staged checks. It applies item 1's three CI formatting commands only to staged files in their corresponding CI scopes, and `shellcheck -x` to staged `.sh` and Bash or sh shebang files selected by `git diff --cached --name-only --diff-filter=ACMR`. The checks read index blobs and staged formatter configuration from the exported index snapshot, preserving a valid working-tree copy's inability to hide invalid staged content. A failing command is named and exits 1 to stop the commit.

   `.githooks/pre-push` reads every `<local ref> <local sha> <remote ref> <remote sha>` line from stdin and skips deleted local refs. Its pushed range is `<remote sha>..<local sha>` for an existing remote ref and `<merge-base of origin/main and local sha>..<local sha>` for a new remote ref. It scans every commit in that range, preserving detection of a secret added and removed before the push. Item 5 defines the content scan. Temporary files go under `$TMPDIR` and are removed by a trap. A match prints only its count and the range and exits 1; an unreadable range also stops the push. Both hooks retain Bash, `set -euo pipefail` and English shdoc comments. Live `core.hooksPath` configuration belongs to the separate hooks-path task.

3. `scripts/orchestrator/dispatch.sh` retains one acceptance-side precheck block and its header description. It applies only to `AGMSG-ACCEPTANCE v1` with `status=accepted`, before either send path. It uses the pre-send history window already read by the script, selects the newest `AGMSG-RESULT v1` for the same `task_id` and requires `status=ready_for_review`. A missing window is a missing RESULT; the block adds no second history read.

   The RESULT contains exactly one `head=` of 40 hex digits and one `precheck=` of 64 hex digits. The commit exists in this checkout. The blob at `<head>:.orchestration/<task>/precheck.json` hashes to `precheck=`. Its `head` is that RESULT head or an ancestor whose diff to it contains only this task's evidence paths. The JSON's executed checks and required selector proofs must succeed under item 7's schema rules. The newest preceding `status=revise` ACCEPTANCE for this task in that same history window supplies the requested `check=` selectors; their expected set is not inferred from the reported `selectors[]`.

   A missing row, field, object, requested selector, malformed record, failed check, checker execution failure or mismatch prints `precheck: <field> <reason>` and refuses the send with exit 1 under `PRECHECK_REQUIRED=1`. With `PRECHECK_REQUIRED` unset or `0`, the same condition prints `precheck: warning <field> <reason>` on stderr and sends. Other values are usage errors. The existing task-id validation, isolated interpreter environment, other refusals and acceptance-record JSON keys remain intact. Enforcement remains staged until the orchestrator enables it after the seats contain the merged implementation.

4. `tests/unit/test_result_precheck.py` retains the existing fixture style from `tests/unit/test_orchestrator_tools.py`: temporary repositories and HOME, recorded command stubs on PATH, fake `history.sh` and `agmsg-dispatch`, and `AGMSG_SCRIPTS` pointing to the fake bus. The secrets and push fixtures use the real repository masker with generated token-like values. No fixture contacts a live bus, GitHub or Codex.

   `test_precheck_exits_1_and_records_ok_false_for_each_failing_check` covers each executed check independently, each of the three formatter failures, successful checks, the dirty-code refusal, the recorded code head and the final hash line. `test_precheck_records_the_local_review_as_deferred_by_default` checks the exact deferred record, absence of a seat review call and the shortcut header. `test_precheck_selector_proof_requires_red_on_previous_head_and_green_on_head` covers red then green, refusal of a selector passing on both heads, recorded exits, worktree cleanup and absence of prune. `test_precheck_secrets_mode_counts_and_never_prints_the_match` covers the real masker, count, unchanged input and secret-free stdout and stderr.

   `test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required` retains hash, missing-object, wrong-task, newest-RESULT status, failed-check and evidence-only ancestry cases in required and warning modes. Its successful fixture supplies all six required checks and the exact deferred local-review record. `test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure` and `test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree` retain real temporary commits, CI scope assertions and the index-content regression. `test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern` retains real pushes to a temporary bare remote, clean pushes and the secret-added-then-removed case. Items 5 to 7 add their named regressions to this same module. Fixture lines count against the test cap.

5. The local review's P1 at `.githooks/pre-push:19-20` is fixed by scanning the text content of every changed blob in every pushed commit with `git show <sha>:<path>`, including merge commits. Git's binary classification never substitutes a summary for the scanned content. A blob containing a NUL byte cannot hide a secret. The precheck's own secrets diff uses item 1's forced-text form for the same reason.

   `tests/unit/test_result_precheck.py::test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit` is written first and runs red against `a5cb73b4`. Its cases include `-diff` and `binary` attributes, a NUL-bearing file containing a generated secret, a secret added and removed in the pushed history, and clean counterparts. It asserts refusal of every secret-bearing push, successful clean pushes, no remote ref created on refusal and no matched value in stdout or stderr. It also exercises the precheck's forced-text secrets input. The same test runs green after the fix; both commands, exits and outputs go in `validation.md`.

6. The local review's P2 at `scripts/orchestrator/result-precheck.sh:173-174` is fixed by explicitly propagating a failing `git diff` and every check command that fails to run. An empty output file left by a failed command never becomes a successful empty scope or clean scan. This includes the shellcheck file list, formatter scopes, secrets input and seat-review prerequisites. The failing check records `ok: false` with a nonzero exit and the precheck exits 1. Bash's disabled `errexit` inside functions called through `||` is not used as the failure control.

   `tests/unit/test_result_precheck.py::test_precheck_records_failed_commands_as_not_ok` is written first and runs red against `a5cb73b4`. Cases cover missing `origin/main`, no merge base, an injected failing diff or file-list command and an unavailable check executable. They assert a nonzero precheck exit, `ok: false` for every affected check and preserved command-failure evidence. The corresponding healthy cases pass. The same test runs green after the fix; both commands, exits and outputs go in `validation.md`.

7. The local review's P2 at `scripts/orchestrator/dispatch.sh:188-190` is fixed by validating the complete expected check set and the type and value of every `ok` field. The six required names are `unit-test`, `render-check`, `format`, `shellcheck`, `secrets` and `local-review`. Missing names, duplicate names, missing `ok` fields and non-boolean values are invalid. Each executed check requires the JSON boolean `true`. The sole exception is the exact documented `{name: local-review, ok: null, deferred: orchestrator}` record; null on another check and null without that marker are invalid.

   `selectors` is a list. Each requested `--check` selector from the revise message has exactly one matching entry with boolean `ok: true`. A missing list, missing requested entry, malformed entry, non-boolean `ok` or failed proof is invalid. Invalid evidence refuses dispatch under `PRECHECK_REQUIRED=1` and warns under its unset or `0` default, using the same diagnostics as other precheck failures.

   `tests/unit/test_result_precheck.py::test_dispatch_rejects_malformed_checks_and_missing_requested_selectors` is written first and runs red against `a5cb73b4`. Correctly hashed and committed fixtures cover `checks=[{}]`, missing required checks, an unrelated successful check, duplicate names, missing `ok`, string and numeric values, invalid nulls and missing selectors when the preceding revise message names `check=`. A two-selector request with one omitted entry is refused. Valid boolean successes with complete proofs and the exact deferred review record pass. Every malformed case refuses without sending under `PRECHECK_REQUIRED=1` and warns and sends when unset or `0`. The same test runs green after the fix; both commands, exits and outputs go in `validation.md`.

## Out of scope

`herdr-agents` and live `core.hooksPath` configuration belong to the separate hooks-path task. The record generator and `dispatch.sh --next` remain P1-6, and `verdict.sh` remains P1-4a. Acceptance-record JSON keys, CI workflows, CI's broader shell-formatting coverage, files under `home/` and full-suite sandbox repairs remain outside this task. The worker does not edit the predecessor's canonical task, acceptance records or owner task. The orchestrator performs the reset bookkeeping. Item 0's parking work is already complete.

## Check

`validation.md` contains the commands, verbatim outputs, exit statuses and tested heads for `make unit-test`, `make render-check`, `make format`, `shellcheck -x scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push scripts/orchestrator/dispatch.sh`, `shfmt -d -i 4 -sr scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push scripts/orchestrator/dispatch.sh`, and `uv run python -m unittest tests.unit.test_result_precheck tests.unit.test_orchestrator_tools -v`. The shell checks are clean, CI's three formatting commands in their CI scopes pass and the two unit modules are green.

The default precheck run's exit code and the sorted-names comparison of its unit-test failures with a pristine `origin/main` worktree in the same sandbox are pasted into validation before the final proof run. Inherited `make unit-test` and `make format` failures are recorded as failures with baseline evidence. CI's `make unit-test` on Ubuntu and macOS remains the authority for the full suite.

The final proof command is `scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a02 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools`. It exits 0 and prints its `precheck=` line. A revise proof adds the dispatched `--previous-head` and every requested `--check` selector. The evidence includes items 5 to 7's red-then-green runs. Each red run executes the current regression test source against the reviewed production implementation in a temporary checkout and records an assertion failure; a missing test, import error or unavailable runner is not a red regression proof.

`git diff --numstat origin/main...HEAD` shows at most 420 changed lines outside `tests/` and `.orchestration/`, and at most 520 changed lines under `tests/`. Changed lines are additions plus deletions, including fixtures. The final changed-file inventory and both totals appear in validation and the RESULT. No local Bats tests run; GitHub Actions supplies any required Bats result. The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance.

## Completion

One branch, `tools/result-precheck-a01`, carries this task and continues PR #411. The next push contains the replacement a02 task copy and the three fixes. No second implementation branch or PR is created.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-result-precheck-followup-a01` as the owner of any advisory P2, `task_copy=<sha256 of .orchestration/dotfiles-T133-result-precheck-a02/task.md>`, `precheck=<sha256 of precheck.json>` and `parked_pr=406` in the RESULT. The three findings explicitly assigned in items 5 to 7 are fixed by this task. Every worker-side fix round counts toward INV-6, including rounds before the first RESULT. The predecessor's stopped history and counters remain recorded.

The report and RESULT name the final head, tested code head, base, branch, changed files, every feedback disposition, test names, caps, task-copy hash and evidence paths. A Codex seat writes evidence at the same relative paths in its own worktree and says so in the RESULT; worker review evidence uses the `-worker-` infix. The orchestrator copies worktree evidence by absolute path before review. The precheck hash also appears in a prose line of the acceptance record, preserving its JSON key set.

This task is `security: true`. The orchestrator runs the local review, task-level audit and separate security-profile review on the final head before the gate. Final-head CI, the feedback sweep, audit dispositions, acceptance record and integration gate follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives fresh required evidence.

The live no-prompt rule governs review requests. No `@codex review` comment is posted. Automatic Bot reviews are observed for the bounded window, and absence after 15 minutes is recorded as `bot: none`. Every `gh` command and every Git write runs individually, without shell chaining or a wrapper combining writes. Permission denials are reported with their command and output; another command or API does not bypass them.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-result-precheck-a02.md: OK
premises 1 to 4: the a01's, re-run by the orchestrator at dispatch (2026-10-18 16:2x JST), outputs equal
redesigned by the codex review profile (headless, read-only) at 2026-10-18T07:2xZ as the INV-6 reset of a01 with the local review of a5cb73b4 folded in; checked and dispatched by the orchestrator
```

The fixtures do not validate live bus delivery or live hook deployment.
Until `PRECHECK_REQUIRED=1` is enabled, invalid precheck evidence warns and acceptance dispatch continues.
