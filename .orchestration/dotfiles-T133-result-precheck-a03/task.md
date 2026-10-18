---
format: 2
task_id: dotfiles-T133-result-precheck-a03
kind: code
security: true
allowed_files:
  - scripts/orchestrator/result-precheck.sh
  - scripts/orchestrator/dispatch.sh
  - .githooks/pre-commit
  - .githooks/pre-push
  - tests/unit/test_result_precheck.py
  - .orchestration/dotfiles-T133-result-precheck-a03/**
after: []
reset_of: [dotfiles-T133-result-precheck-a02]
threat_table:
  - control: "scripts/orchestrator/result-precheck.sh (the pre-RESULT checks, shared per-blob scan, masked logs, selector proof and evidence writer propagate prerequisite and command failures)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_precheck_records_failed_commands_as_not_ok"
  - control: "scripts/orchestrator/dispatch.sh (the acceptance-side precheck binds the newest RESULT, revision ordering, hashes, code head, required checks and requested selectors under PRECHECK_REQUIRED)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise"
  - control: ".githooks/pre-commit (CI's three formatting commands in their staged scopes and shellcheck run against index blobs)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree"
  - control: ".githooks/pre-push (each changed blob reaches the existing detector separately, preserving its file boundary and JSON decoding)"
    disposition: "closed: tests/unit/test_result_precheck.py::test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding"
  - control: "tests/unit/test_result_precheck.py (the retained cases and the new local-review regressions use temporary repositories and recorded fake commands)"
    disposition: "residual: temporary repositories, a temporary HOME, fake bus commands and generated token fixtures isolate the tests; the final-head audit checks that the real detector and assertions exercise the stated controls."
  - control: ".orchestration/dotfiles-T133-result-precheck-a03/** (the redesigned task's branch artifacts)"
    disposition: "residual: artifacts stay in this task's directory, distinguish inherited observations from fresh results, and bind their commands, hashes and tested heads for the final-head audit."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-result-precheck-a03/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-result-precheck-a02/task.md), with .orchestration/dotfiles-T133-result-precheck-a01/task.md also deleted if present"
    disposition: "residual: the worker's first push contains only the named predecessor task-copy deletions as reset bookkeeping and the byte-identical a03 copy; its own SHA256 appears in the TASK and RESULT, and the orchestrator verifies the deletions and byte identity at acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-result-precheck-a03/ (report.md, validation.md, sandbox.md, learning.md, revise.yaml, precheck.json, result.txt and precheck-*.log)"
    disposition: "residual: records and logs are masked before committing, precheck.json binds the last code commit, and the final commit changes only this task's evidence; the audit checks those claims and the hashes."
  - control: "task metadata"
    disposition: "residual: the orchestrator checks the dispatched front matter with task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; the byte comparison covers later metadata changes."
  - control: "metadata separators"
    disposition: "residual: the first document separators bound the YAML front matter and the dispatched-file byte comparison covers the entire task copy and its separators."
  - control: "in-process effects"
    disposition: "residual: subprocesses use temporary repositories and a temporary HOME; temporary scan files and detached proof worktrees are removed, and a failed prerequisite cannot become a successful check."
  - control: "workflow and interpreter or environment inputs"
    disposition: "residual: no workflow or interpreter file changes; Bash scripts retain set -euo pipefail, embedded Python uses -I, and the existing detector and masker run through uv; PRECHECK_REQUIRED defaults to warning, PRECHECK_LOCAL_REVIEW defaults to explicit orchestrator deferral, and invalid values are rejected."
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

# AGMSG-TASK dotfiles-T133-result-precheck-a03 — S1 redesign of dotfiles-T133-result-precheck-a02 (plan 006 INV-6; plan 024 P1-5)

This text is the independent S1 redesign by a review-profile context other than the author of a02. The local review of `4ed1b27a666ba939db76051243143a7d7ed2aaa5` found one P1 and two P2 after a02's revise-1 implementation at `56a734cdc2b03fdda7d386895c104d83ccdba8cd`. The P1 is the third finding of class `secret-scan-bypass`, following the blob-boundary and UTF-16 findings in the local review of `9cd5514a790f6993136f5e74aaf3f3afa31b23d8`. S1 sends the artifact to redesign. The a02 artifact has consumed its one revise round, and no further revise of a02 is authorized.

PR #411 continues on the same branch, `tools/result-precheck-a01`, from `4ed1b27a666ba939db76051243143a7d7ed2aaa5`. The worker's first push deletes `.orchestration/dotfiles-T133-result-precheck-a02/task.md` and adds this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-result-precheck-a03/task.md`. The same push deletes `.orchestration/dotfiles-T133-result-precheck-a01/task.md` if it is still present. The orchestrator owns this reset bookkeeping and directs these exact predecessor task-copy deletions as the only reset deletions outside `allowed_files`. Every other worker edit stays within `allowed_files`. One branch and one implementation PR carry the redesign.

The a01 and a02 records retain their stopped status, historical results and counters. Their report, validation, `revise.yaml` and `precheck.json` remain historical evidence. Fresh results and proof records use `.orchestration/dotfiles-T133-result-precheck-a03/`. The four premises preserve the a02 premises verbatim as write-time observations. The a01 parking work is complete, and its parked draft is PR #406.

The specification replaces aggregate scan input with one unchanged blob per detector invocation. The design uses one shared function that reads `git show <sha>:<path>` into the repository detector's per-file entry point; the pre-push hook loops over pushed blobs, and the precheck reuses that function. The implementation deletes concatenation and synthetic ASCII or NUL-stripped scan views, retains the revise-1 guarantees, and fixes revision ordering and home-path classification. Verification reproduces each finding of both local reviews by an executed assertion failure against the relevant previous production code with the current regression source, then passes on the redesigned code.

## Goal

A seat runs one command before its RESULT to execute the repository's checks on its code head, record their outcomes and stop on a failed check. The orchestrator's accepted ACCEPTANCE verifies that evidence against the newest RESULT and the latest revision request. The pre-commit hook checks staged content. The pre-push hook scans every pushed commit's changed blobs individually with the repository's existing secret detector, preserving JSON and supported UTF-16 decoding and refusing an undecodable blob. Home-path findings remain a separate check confined to paths under `.orchestration/`.

This implements the precheck and hooks in items (4) and (9) of `.orchestration/plans/024-design-programs.md`. The precheck supplies the RESULT hash evidence used by the verdict in `.orchestration/plans/024-design-mechanism.md`; it does not replace the final-head CI, feedback sweep, audit, security review or integration gate.

## Files

1. `scripts/orchestrator/result-precheck.sh <task> [--tests <unittest module>...] [--previous-head <sha40> --check <selector>...] [--secrets <file>]` retains the inherited Bash implementation, `set -euo pipefail` and English shdoc comments. It runs from `git rev-parse --show-toplevel` and refuses uncommitted changes outside `.orchestration/<task>/`, so evidence describes committed code. Its `--staged` mode remains the shared implementation used by the pre-commit hook.

   Each executed check records `{name, ok, exit, output_sha256}`. Its output goes to `.orchestration/<task>/precheck-<name>.log`, masked with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets` before its hash is recorded. A masking failure fails the run, removes unmasked logs and produces no successful evidence record. Evidence masking continues to normalize home paths.

   The default `unit-test` check runs `make unit-test`. `--tests` selects `uv run python -m unittest <modules> -v` instead. The `render-check` check runs `make render-check`. The `format` check runs CI's three formatting commands in CI's scopes: `shfmt --indent 4 --space-redirects --diff` on tracked `install/**/*.sh` and `scripts/**/*.sh`, `ruff format --config ruff.toml --check` on tracked `*.py`, and `prettier --check` on tracked `*.md`. The scopes come from `git ls-files` with CI's pathspecs, and all three commands must exit 0. The script header pastes the corresponding three command lines from `.github/workflows/test.yaml`'s ``Run `shfmt` `` and `Check Python and Markdown formatting` steps. CI's tool selection and repository formatter configuration remain authoritative. The `format` check does not use `make format`'s broader shell scope.

   The `shellcheck` check runs `shellcheck -x` on every existing file changed by `git diff --name-only origin/main...HEAD` that ends in `.sh` or has a Bash or sh shebang. The `secrets` check enumerates the changed blobs in `origin/main...HEAD` and calls the shared one-blob scanning function for each. That function reads the complete blob with `git show <sha>:<path>` and applies the existing detector from `scripts/validate-agent-assets.py` to that file's unchanged bytes. It preserves `read_scannable_text` decoding, `json_strings` decoding of JSON keys and string values, `strip_allowed_secret_placeholders` and `SECRET_PATTERN` matching. Git's binary classification never substitutes a summary for blob content. No concatenated blob stream or aggregate diff is scanned. An unreadable blob, an undecodable blob, or a detector execution failure fails the check. Temporary scan files stay under `$TMPDIR` and are removed by an EXIT trap.

   Secret counts come only from detector matches. The masker's rewrite count and a masked-file byte comparison do not determine whether a blob contains a secret. The original repository-relative blob path governs the separate home-path check in item 7, regardless of the temporary scan file's location. Decoding failures, secret findings and home-path findings have distinct diagnostics that disclose no matched value or raw blob content.

   A failing `git diff`, blob enumeration, blob read, formatter scope listing or prerequisite command explicitly fails its affected check. This includes missing `origin/main`, no merge base, an unavailable check executable and seat-review prerequisites. An empty output file left by a failed command never becomes a successful empty scope or clean scan. The affected check records `ok: false` with a nonzero exit, and the precheck exits 1. Bash's disabled `errexit` inside functions called through `||` is not used as the failure control.

   `PRECHECK_LOCAL_REVIEW=orchestrator` is the default. It records `{name: local-review, ok: null, deferred: orchestrator}` and leaves the local review to the orchestrator on the final head. `PRECHECK_LOCAL_REVIEW=seat` runs `scripts/orchestrator/local-review.sh <task> <head> <pr>`, obtains the PR number through `gh pr view --json number` and requires exit 0. The header retains the line `shortcut: a Claude seat cannot run codex inside its Bash sandbox (local-review.sh's header), so the orchestrator's acceptance runs the local review on the head as today; upgrade to seat when the seats run omp (plan 024 phase 2 B)`. It also retains `shortcut: inside a Claude seat's sandbox the full suite fails on sandbox-denied operations, so a seat runs the precheck with --tests on its task's modules and CI runs the full suite; upgrade when the seats run omp (plan 024 phase 2 B)`.

   `--secrets <file>` applies the same per-file detector to exactly that file and exits 0 for no finding and 1 for a finding, decoding refusal or detector failure. The input remains unchanged. The pre-push caller supplies each blob's commit and original repository-relative path to the shared one-blob entry point in this script. `--staged` runs only the staged formatting and shellcheck checks.

   `--previous-head` with repeated `--check tests/<file>::<name>` selectors creates a detached temporary worktree at that commit and copies the current head's regression module into it before running `uv run python -m unittest tests.unit.<module> -k <name>`. The previous production code remains unchanged. A valid red proof requires exit 1, an executed test count greater than zero and an assertion-failure summary with failures and no errors. A missing test, import failure, runner failure or zero-test run is invalid. The same selector must pass on the current code. Both exit codes and hashes of the masked outputs are recorded in `selectors[]`. The worker records `previous_head` and the complete `check` list in `revise.yaml`. Cleanup uses `git worktree remove --force <dir>` and never `git worktree prune`.

   `precheck.json` contains `{head, tree, generated_at, checks, selectors}`. Its `head` is the last code commit tested by the run and its `tree` is that commit's `HEAD^{tree}`. `result.txt` contains the RESULT template with that code head. The last stdout line is `precheck=<sha256 of precheck.json>`. Exit 0 requires every executed check and every selector proof to succeed; the explicit deferred local review is neither a passing check nor a failure. A failed check exits 1 and usage errors exit 2. The worker commits `precheck.json`, `result.txt` and the masked logs in the final evidence-only commit. Every path changed between the recorded code head and the final head is under `.orchestration/<task>/`. The bus RESULT carries the final head and the unchanged precheck hash; its completed template's other fields remain unchanged. Code changes after a proof require a fresh proof before a new final evidence-only commit.

2. `.githooks/pre-commit` delegates to the shared staged checks. It applies item 1's three CI formatting commands only to staged files in their corresponding CI scopes, and `shellcheck -x` to staged `.sh` and Bash or sh shebang files selected by `git diff --cached --name-only --diff-filter=ACMR`. The checks read index blobs and staged formatter configuration from the exported index snapshot, preserving a valid working-tree copy's inability to hide invalid staged content. A failing command is named and exits 1 to stop the commit.

   `.githooks/pre-push` reads every `<local ref> <local sha> <remote ref> <remote sha>` line from stdin and skips deleted local refs. Its pushed range is `<remote sha>..<local sha>` for an existing remote ref and `<merge-base of origin/main and local sha>..<local sha>` for a new remote ref. It scans every commit in that range, including merge commits, preserving detection of a secret added and removed before the push. It enumerates each commit's changed blobs and invokes item 1's shared function separately for each blob. It never appends blobs to a shared scan input, even with separators.

   A detector match stops the push with exit 1 and reports only the match count and range. An unreadable range, failed enumeration, unreadable blob, undecodable blob or detector failure also stops the push with a distinct failure diagnostic. A home-path finding follows item 7's scope and diagnostic. No matched value or raw content appears in stdout or stderr. Temporary files go under `$TMPDIR` and are removed by a trap. Both hooks retain Bash, `set -euo pipefail` and English shdoc comments. Live `core.hooksPath` configuration belongs to the separate hooks-path task.

3. `scripts/orchestrator/dispatch.sh` retains one acceptance-side precheck block and its header description. It applies only to `AGMSG-ACCEPTANCE v1` with `status=accepted`, before either send path. It uses the pre-send history window already read by the script and selects the newest `AGMSG-RESULT v1` for the same `task_id`. That RESULT must have `status=ready_for_review` and occur after the latest `status=revise` ACCEPTANCE for the task in the same window. A missing window is a missing RESULT; the block adds no second history read.

   The RESULT contains exactly one `head=` of 40 hex digits and one `precheck=` of 64 hex digits. The commit exists in this checkout. The blob at `<head>:.orchestration/<task>/precheck.json` hashes to `precheck=`. Its `head` is that RESULT head or an ancestor whose diff to it contains only this task's evidence paths.

   The six required check names are `unit-test`, `render-check`, `format`, `shellcheck`, `secrets` and `local-review`. Missing names, duplicate names, missing `ok` fields and non-boolean values are invalid. Every executed check requires the JSON boolean `true`. The sole exception is the exact documented `{name: local-review, ok: null, deferred: orchestrator}` record; null on another check and null without that marker are invalid.

   `selectors` is a list of passing proof entries. The latest `status=revise` ACCEPTANCE for this task supplies the requested `check=` selectors after the ordering requirement has been satisfied. Each requested selector has exactly one matching entry with boolean `ok: true`. A missing list, missing requested entry, malformed entry, non-boolean `ok` or failed proof is invalid. The expected set is not inferred from the reported `selectors[]`.

   A missing row, stale RESULT, missing field or object, missing requested selector, malformed record, failed check, checker execution failure or mismatch prints `precheck: <field> <reason>` and refuses the send with exit 1 under `PRECHECK_REQUIRED=1`. With `PRECHECK_REQUIRED` unset or `0`, the same condition prints `precheck: warning <field> <reason>` on stderr and sends. Other values are usage errors. The existing task-id validation, isolated interpreter environment, other refusals and acceptance-record JSON keys remain intact. Enforcement remains staged until the orchestrator enables it after the seats contain the merged implementation.

4. `tests/unit/test_result_precheck.py` retains the existing fixture style from `tests/unit/test_orchestrator_tools.py`: temporary repositories and HOME, recorded command stubs on PATH, fake `history.sh` and `agmsg-dispatch`, and `AGMSG_SCRIPTS` pointing to the fake bus. The secret and push fixtures use the real repository detector with generated token-like values. No fixture contacts a live bus, GitHub or Codex.

   `test_precheck_exits_1_and_records_ok_false_for_each_failing_check` covers each executed check independently, each of the three formatter failures, successful checks, the dirty-code refusal, the recorded code head and the final hash line. `test_precheck_records_the_local_review_as_deferred_by_default` checks the exact deferred record, absence of a seat review call and the shortcut header. `test_precheck_selector_proof_requires_red_on_previous_head_and_green_on_head` covers red then green, refusal of a selector passing on both heads, recorded exits, worktree cleanup and absence of prune. `test_precheck_secrets_mode_counts_and_never_prints_the_match` covers the real detector, count, unchanged input and secret-free stdout and stderr.

   `test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required` retains hash, missing-object, wrong-task, newest-RESULT status, failed-check and evidence-only ancestry cases in required and warning modes. Its successful fixture supplies all six required checks and the exact deferred local-review record. `test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure` and `test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree` retain real temporary commits, CI scope assertions and the index-content regression. `test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern` retains real pushes to a temporary bare remote, clean pushes and the secret-added-then-removed case.

   The a02 regressions `test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit`, `test_precheck_records_failed_commands_as_not_ok` and `test_dispatch_rejects_malformed_checks_and_missing_requested_selectors` remain covered. Their historical red baseline is `a5cb73b489235bb177e346dd00dd9aca28a432e8`, and their green results are rerun on this task's code head. The binary-marked cases retain `-diff`, `binary`, NUL-bearing content, changed history and clean decodable counterparts, and exercise the precheck's per-blob scan. An undecodable clean binary fixture now expects refusal under item 1's fail-closed rule. The malformed-record cases retain empty entries, missing and duplicate names, missing `ok`, string and numeric values, invalid nulls and incomplete requested selector sets in required and warning modes.

   The three revise-1 guarantees fixed at `56a734cd` after the review of `9cd5514` are retained with their tests: blob-boundary isolation in `test_pre_push_scans_each_blob_on_its_own_boundary`, UTF-16 decoding or refusal in `test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan`, and an executed assertion failure for red proof in `test_previous_head_proof_requires_an_executed_failing_test`. Supported UTF-16 files use the existing detector's decoding; unsupported encodings are refused. The retained tests distinguish a decoding refusal from a secret match and preserve the rejection of import, runner and zero-test failures as proof.

   Items 5 to 7 add four named regressions to this module. Those four tests are written before implementation, run red against `4ed1b27a666ba939db76051243143a7d7ed2aaa5` and run green after the fixes. Existing fixture duplication is consolidated as needed without dropping coverage. Fixture lines count against the test cap.

5. The P1 at `.githooks/pre-push:27-31` in `.orchestration/validation/dotfiles-T133-result-precheck-a02-local-review-4ed1b27.md` is fixed by preserving each blob as a separate detector input. Appending another JSON document must never turn a credential-bearing JSON document into raw-text fallback input. The concatenation path is deleted from the hook and the precheck, including the revise-1 newline-separated path and synthetic NUL-normalized views. Both callers reuse the shared one-blob function and the existing detector's JSON and UTF-16 decoding.

   `tests/unit/test_result_precheck.py::test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding` is written first and runs red against `4ed1b27a`. A pushed commit contains a JSON blob whose generated credential has a JSON-escaped prefix such as `\u0067hp_`, followed by a clean JSON blob. The fixture establishes that the first document is detected individually and that concatenating the two documents would hide the decoded credential. The real push is refused, no remote ref is created, and the matched value is absent from stdout and stderr. Clean JSON counterparts pass. The same module verifies that the precheck detects the credential through the shared per-blob scan. The test runs green after the fix, and its commands, outputs, tested heads and exits appear in `validation.md`.

   `tests/unit/test_result_precheck.py::test_pre_push_fails_closed_on_an_undecodable_blob` is written first and runs red against `4ed1b27a`. A pushed blob that the existing detector cannot decode stops the push without creating the remote ref. The diagnostic identifies decoding failure and does not invent a secret match. A supported clean text counterpart passes. The precheck also exits 1 with its `secrets` check recorded as `ok: false` for the undecodable blob. The test runs green after the fix, and both results appear in `validation.md`.

6. The P2 at `scripts/orchestrator/dispatch.sh:174-176` in the local review of `4ed1b27` is fixed by finding the latest `status=revise` ACCEPTANCE across the task's entire existing pre-send window and requiring the newest RESULT to occur after it. A revise line after the last RESULT invalidates that RESULT before its evidence can authorize acceptance. A subsequent ready RESULT must carry the complete requested proofs and valid evidence.

   `tests/unit/test_result_precheck.py::test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise` is written first and runs red against `4ed1b27a`. Its correctly hashed, committed fixtures put a revise line after the last ready RESULT and assert exit 1 with no send under `PRECHECK_REQUIRED=1`. The same history warns and sends when `PRECHECK_REQUIRED` is unset or `0`. A ready RESULT after the latest revise passes when its evidence includes every requested selector. An unrelated task's revise does not invalidate this task's RESULT. The test runs green after the fix, and both results appear in `validation.md`.

7. The P2 at `scripts/orchestrator/result-precheck.sh:98-103` in the local review of `4ed1b27` is fixed by separating credential detection from home-path normalization. A secret finding requires a match from `SECRET_PATTERN` through the existing detector and its decoders. The masker's home-path rewrites are never counted as secret findings. The existing `home_path_pattern` check applies only to original repository-relative paths under `.orchestration/`, including decoded JSON strings as the existing validator does. Public source documentation containing home-path examples passes this separate check. Evidence log masking keeps its existing normalization behavior.

   `tests/unit/test_result_precheck.py::test_pre_push_reports_home_path_rewrites_only_under_orchestration` is written first and runs red against `4ed1b27a`. A public source file containing documentation with home-path examples and no detector secret match pushes successfully. The same text under `.orchestration/` stops the push with a home-path diagnostic and no secret finding. The precheck makes the same scope and classification distinction through the shared scan. The test runs green after the fix, and its commands, outputs and exits appear in `validation.md`.

## Out of scope

`herdr-agents` and live `core.hooksPath` configuration belong to the separate hooks-path task. The record generator and `dispatch.sh --next` remain P1-6, and `verdict.sh` remains P1-4a. Acceptance-record JSON keys, CI workflows, CI's broader shell-formatting coverage, files under `home/` and full-suite sandbox repairs remain outside this task. The worker does not edit the predecessor's canonical task, acceptance records or owner task. The orchestrator performs the reset bookkeeping. Item 0's parking work is already complete.

## Check

`validation.md` contains the commands, verbatim outputs, exit statuses and tested heads for `make unit-test`, `make render-check`, `make format`, `shellcheck -x scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push scripts/orchestrator/dispatch.sh`, `shfmt -d -i 4 -sr scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push scripts/orchestrator/dispatch.sh`, and `uv run python -m unittest tests.unit.test_result_precheck tests.unit.test_orchestrator_tools -v`. The shell checks are clean, CI's three formatting commands in their CI scopes pass and the two unit modules are green.

The default precheck run's exit code and the sorted-names comparison of its unit-test failures with a pristine `origin/main` worktree in the same sandbox are pasted into validation before the final proof run. Inherited `make unit-test` and `make format` failures are recorded as failures with baseline evidence. CI's `make unit-test` on Ubuntu and macOS remains the authority for the full suite.

The final proof command is `scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a03 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools`. It exits 0 and prints its `precheck=` line. The a03 proof adds `--previous-head 4ed1b27a666ba939db76051243143a7d7ed2aaa5` and one `--check` for each of the four named regressions in items 5 to 7. `revise.yaml` records that production baseline and all four selectors. A later authorized revise proof uses its dispatched `--previous-head` and every requested `--check` selector.

The evidence includes one red-then-green regression per finding of both a02 local reviews and the additional undecodable-blob regression. The four new regressions run red against `4ed1b27a666ba939db76051243143a7d7ed2aaa5`. The three retained revise-1 regressions named in item 4 replay their current test source against `9cd5514a790f6993136f5e74aaf3f3afa31b23d8`, where the corresponding defects existed, and run green on this task's code head. Their passing state at `4ed1b27a` is retained rather than represented as a new red result. Each red run executes the current regression test source against the reviewed production implementation in a temporary checkout and records an assertion failure caused by the reviewed behavior. The production commit and copied test-source hash accompany the command, output and exit status. A missing test, missing new helper, import error or unavailable runner is not a red regression proof.

`git diff --numstat origin/main...HEAD` shows at most 420 changed lines outside `tests/` and `.orchestration/`, and at most 520 changed lines under `tests/`. Changed lines are additions plus deletions, including fixtures. The final changed-file inventory and both totals appear in validation and the RESULT. No local Bats tests run; GitHub Actions supplies any required Bats result. The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance.

## Completion

One branch, `tools/result-precheck-a01`, carries this task and continues PR #411 from `4ed1b27a666ba939db76051243143a7d7ed2aaa5`. The worker's first push contains the replacement a03 task copy, the a02 task-copy deletion, the a01 task-copy deletion if still needed, and the redesigned implementation with its tests. No second implementation branch or PR is created.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-result-precheck-followup-a01` as the owner of any advisory P2, `task_copy=<sha256 of .orchestration/dotfiles-T133-result-precheck-a03/task.md>`, `precheck=<sha256 of precheck.json>` and `parked_pr=406` in the RESULT. The three open findings of `4ed1b27` assigned in items 5 to 7 are fixed by this task, including the two P2 previously recorded as advisory. The orchestrator records that superseding ownership outside the worker's edit boundary. Every worker-side fix round counts toward INV-6, including rounds before the first RESULT. The predecessors' stopped history and counters remain recorded.

The report and RESULT name the final head, tested code head, base, branch, changed files, every feedback disposition, test names, caps, task-copy hash and evidence paths. A Codex seat writes evidence at the same relative paths in its own worktree and says so in the RESULT; worker review evidence uses the `-worker-` infix. The orchestrator copies worktree evidence by absolute path before review. The precheck hash also appears in a prose line of the acceptance record, preserving its JSON key set.

This task is `security: true`. The orchestrator runs the local review, task-level audit and separate security-profile review on the final head before the gate. Final-head CI, the feedback sweep, audit dispositions, acceptance record and integration gate follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives fresh required evidence.

The live no-prompt rule governs review requests. No `@codex review` comment is posted. Automatic Bot reviews are observed for the bounded window, and absence after 15 minutes is recorded as `bot: none`. Every `gh` command and every Git write runs individually, without shell chaining or a wrapper combining writes. Permission denials are reported with their command and output; another command or API does not bypass them.

Until P1-14 lands, any string containing the words `gh pr merge` or `gh pr create` is written with the file-edit tool, never in a Bash heredoc or `echo`.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-result-precheck-a03.md: OK
premises: copied from a02 verbatim (write-time outputs of 2026-10-18)
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-result-precheck-a03.md
```

The fixtures do not validate live bus delivery or live hook deployment.
Until `PRECHECK_REQUIRED=1` is enabled, invalid precheck evidence warns and acceptance dispatch continues.