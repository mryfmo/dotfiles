---
format: 2
task_id: dotfiles-T133-dispositions-a02
kind: code
security: true
allowed_files:
  - scripts/orchestrator/dispositions.py
  - scripts/orchestrator/orch-gate.sh
  - tests/unit/test_dispositions.py
  - tests/unit/test_orch_gate_path.py
  - .orchestration/dotfiles-T133-dispositions-a02/**
after: [dotfiles-T133-permission-guard-gate-a05]
reset_of: [dotfiles-T133-dispositions-a01]
threat_table:
  - control: "scripts/orchestrator/dispositions.py (disposition proposals, the three refutation forms, static selector verification against the head tree and parsing of prefetched required-check data)"
    disposition: "closed: tests/unit/test_dispositions.py::DispositionsTest::test_dispositions_verifies_test_refutations_from_head_tree_and_required_checks"
  - control: "scripts/orchestrator/orch-gate.sh (re-validation immediately before the gate, enforcement only under DISPOSITIONS_REQUIRE_REFUTATION=1 and reporting otherwise)"
    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_revalidates_the_dispositions_before_the_gate"
  - control: "tests/unit/test_dispositions.py (temporary Git repositories, sweep fixtures, prefetched API fixtures and file URLs for source verification)"
    disposition: "residual: fixtures use temporary repositories and files, perform no live GitHub writes and leave markers that detect importing or executing a named head test; the final-head audit reads their assertions."
  - control: "tests/unit/test_orch_gate_path.py (fake binaries, fixture main, inherited-environment cases, verifier authentication and sweep-copy identity)"
    disposition: "residual: fake binaries record arguments, environments, working directories and execution order; fixture main supplies authenticated verifier bytes, and the final-head audit reads refusal and restoration assertions."
  - control: ".orchestration/dotfiles-T133-dispositions-a02/** (this reset task's branch artifacts)"
    disposition: "residual: evidence identifies tested revisions, preserves predecessor failures and separates worker fixtures from the orchestrator's API reads; the audit compares its claims with the diff and CI."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-dispositions-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-dispositions-a01/task.md)"
    disposition: "residual: the first push deletes the a01 copy and adds the byte-identical dispatched a02 copy as specified reset bookkeeping; TASK and RESULT name the a02 copy's SHA256, and the orchestrator verifies the replacement at acceptance."
  - control: task metadata
    disposition: "residual: the orchestrator checks format, task identity, reset_of, allowed_files, threat_table and premises with task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; whole-file byte identity protects the dispatched policy."
  - control: metadata separators
    disposition: "residual: the first document separators bound structured metadata, and the task-copy comparison covers the complete file."
  - control: in-process effects
    disposition: "residual: the verifier performs Git data reads and the source URL fetch, parses API JSON inside the sandbox and writes only its requested output; it never imports head modules, discovers tests or executes a selector."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter configuration changes; execution uses isolated Python, a constructed env -i environment and a private PATH of absolute binaries resolved in the trusted root."
  - control: new or renamed scripts
    disposition: "residual: dispositions.py is the only new script relative to main; RESULT lists it, and any other new or renamed script fails the audit."
  - control: the environment before Git discovery
    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_sanitizes_the_environment_before_git_discovery"
  - control: the executed verifier's identity
    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_runs_dispositions_only_when_it_matches_main"
  - control: the validated sweep's identity
    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_validates_the_copy_it_reads"
  - control: the prefetched required-check data
    disposition: "residual: the orchestrator records its own ruleset and exact-head check-runs reads in protected evidence, and the verifier parses their raw JSON again rather than accepting saved verification booleans."
  - control: the strength of a test refutation
    disposition: "residual: selector presence and successful required checks provide evidence of the head's CI strength only; P0/P1 remain unrefuted claims until programs item (16), P1-10 part 2, confirms them."
  - control: the outside-sandbox gh exception
    disposition: "residual: decision D-024-17 assigns closure to plan 024 P1-15, whose worker exclusions execute an absolute trusted binary; this task retains today's individual gh reads and does not change worker exclusions."
  - control: the worker-seat write boundary
    disposition: "residual: every worker seat's sandbox denies writes outside its worktree and listed scratch paths, protecting the trusted checkout, review worktree and orchestrator evidence; a same-UID process outside every seat sandbox remains outside this protection."
  - control: orchestrator effect merge
    disposition: "residual: merge uses only gh pr merge --squash --match-head-commit <audited head> after the integration gate; local merges and pushes to main remain forbidden."
  - control: orchestrator effect update-branch
    disposition: "residual: a rebase or gh pr update-branch changes the head, so required CI, feedback collection, task-level audit and security review bind the resulting final head before integration."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; the existing dirty-worktree rule applies, and the acceptance record identifies any discarded uncommitted state."
premises:
  - claim: neither new file exists on origin/main
    command: git ls-files scripts/orchestrator/dispositions.py tests/unit/test_dispositions.py | wc -l
    output: |-
      0
  - claim: a sweep item of pr-feedback.py carries source, author, bot, level, path, line, body, url, the source's extra state and disposition, so the thread's commit comes from gh when the item lacks it
    command: sed -n '133,143p' scripts/pr-feedback.py | /usr/bin/grep -o '"[a-z]*"' | tr '\n' ' '
    output: |-
      "source" "author" "login" "slug" "" "bot" "level" "path" "line" "body" "" "url" "disposition" "" 
  - claim: orch-gate.sh invokes the gate once with PR_FEEDBACK_EVIDENCE, the point before which the re-validation runs
    command: /usr/bin/grep -c 'PR_FEEDBACK_EVIDENCE="${sweep}"' scripts/orchestrator/orch-gate.sh
    output: |-
      1
  - claim: the orch-gate tests live in tests/unit/test_orch_gate_path.py and use fake binaries on a private PATH
    command: /usr/bin/grep -c 'def test_orch_gate_' tests/unit/test_orch_gate_path.py
    output: |-
      3
  - claim: audit-pool.sh is not on origin/main at the predecessor's write time, so the --second-opinion mode of programs item (16) is a later task
    command: git ls-files scripts/orchestrator/audit-pool.sh | wc -l
    output: |-
      0
  - claim: the gate already holds the disposition and commit validators dispositions.py reuses
    command: /usr/bin/grep -n 'def commit_in_range\|def parse_disposition' scripts/require-crit-review.py | cut -c1-24
    output: |-
      389:def commit_in_range(
      397:def parse_disposition(
---

# AGMSG-TASK dotfiles-T133-dispositions-a02 — INV-6 reset of dotfiles-T133-dispositions-a01 (plan 006 S2; plan 024 P1-10 part 1, programs item (5))

This reset incorporates the independent review-profile redesign and the orchestrator's decisions after C-80 returned `Verdict: incorrect` with eight P1 and one P2 in `.orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md.last.md`.

The local review of revise-1 head `bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3` stopped the chain at `2026-10-18T22:1xZ`. It found one P1 in the CI-log verifier and two P2 concerning interleaved diagnostic output and loss of the full selector. A second revise would reach INV-6 S2, and the operator forbids a third round. The unsound CI-log design came from the orchestrator's amendment 1.

PR #419 continues on `tools/dispositions-a01` from `bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3`. The merged P1-11 baseline is `origin/main` at `0e496ce7449e9286aeac3b2770cbff374c7dc5cf`. The worker rebases onto main containing that baseline and merged PR #421 before its first push. One branch and one PR carry the reset. The orchestrator names the worker seat in the TASK line.

The worker's first push deletes `.orchestration/dotfiles-T133-dispositions-a01/task.md` and adds this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-dispositions-a02/task.md`. That predecessor-copy deletion is the specified reset bookkeeping exception to `allowed_files`. The predecessor's other artifacts, canonical task text and acceptance history remain unchanged.

The six command-output premises retain a01's write-time observations as historical evidence. New report, validation, sandbox and learning records use the a02 directory. The a01 acceptance record retains its audit, amendment, revise, advisory rows and S2 withdrawal.

The design sources are `.orchestration/plans/024-design-programs.md` items (5) and (16), and `.orchestration/plans/024-design-quality.md` section 5.13. The additional inputs are the a01 task and acceptance records, `.orchestration/validation/dotfiles-T133-dispositions-a01-local-review-bdbbbf9.md`, the C-80 verdict, the branch diff through `bdbbbf91`, `scripts/orchestrator/orch-gate.sh` at `origin/main` and the checker docstring in `scripts/orchestrator/task-consistency-check.py`.

The audit decision at `fa47987` established that a `test:` refutation never executes head code on the orchestrator's host. Running a test in the trusted checkout tests pre-regression code. The merged regime workflow executes base code and inspects the PR as data. It has no head-test execution responsibility.

The CI results-artifact design is withdrawn. A head-authored test produces its own result, so an artifact, runner, workflow step or download cannot establish producer trust. The Linux keyring restriction also prevents an in-sandbox helper from implementing the proposed authenticated gh fetch. This task adds no results runner, results artifact, artifact download or workflow change.

The write-boundary premise is that every worker seat's sandbox denies writes outside its worktree and listed scratch paths. The trusted checkout, review worktree and orchestrator's evidence are protected by that boundary. The threat table states its residual once. Decision D-024-17 owns the separate outside-sandbox executable-selection defect; this task retains today's single-command gh reads.

## Goal

For a PR head, every review-comment item of the sweep gets a machine proposal: `fixed:<commit>` when an eligible branch commit between the thread's commit and the head touches the thread's hunk, otherwise a demand for `not-applicable:` with one of the three refutation forms. The gate wrapper re-validates the saved dispositions before the gate runs.

A `test:` refutation holds only when its selector names a test function present at the stated path in the head tree, the required unit-test check runs concluded success for that exact head, and the finding is P2 or P3. A P0/P1 `test:` refutation is a claim that programs item (16)'s second opinion must confirm. `--require-refutation` treats that claim as not yet refuted.

This evidence has the strength of the head's CI. It supplies no proof against a head-authored test and establishes no per-selector execution outcome.

## Files

1. `scripts/orchestrator/dispositions.py <pr> <head> --feedback <sweep.json> [--out <json>] [--require-refutation] [--commits <json>] [--checks <json>]` is a Python CLI run with `python -I`, using the standard library only and an English shdoc-style module docstring.

   The tool processes each `review_comment` item and each badged `review` finding. The location comes from the item's path and line, with the existing review-body blob-link handling retained. A finding without a location gets the not-applicable demand and still requires a refutation when its disposition is not-applicable.

   The thread's commit comes from `original_commit_id`, the existing `commit` field, the `--commits` map from URL to commit, or the existing gh read, in that order. A required commit that cannot be obtained or read produces a hold with the reason. Item 6 defines the proposal path that needs no thread-commit lookup.

   The proposal uses the PR diff and `git diff <thread commit>..<head> -- <path>`. A covering hunk uses its old-side and new-side ranges. The tool walks eligible branch commits newest first and proposes `fixed:<commit>` only for a commit whose own diff against its parent touches that range. Base commits and base-merge-only changes supply no branch fix. An unchanged hunk, an upstream-only change or the absence of an eligible fixing commit produces the not-applicable demand. Paths remain literal Git pathspecs, and sweep text is never evaluated.

   The output is the sweep with `proposal` added per processed item and the existing `disposition` untouched. A checked not-applicable disposition also receives its verification record. `--out` selects the output file, and stdout is the default. Diagnostic lines go to stderr.

   The three refutation forms remain `test:<selector>`, `source:{url, fetched_at, quote}` and `diff:<range>`. The existing `; evidence=<form>` disposition representation remains. The CI-log parser and `--ci-log` input are removed.

   The `test:` form reads the named file with `git show <head>:<path>` and parses it as Python syntax data with the standard-library AST. The full selector identifies the file and function, including its module and class components when present. A full dotted selector maps deterministically to its repository path. The existing path spelling remains supported, and a classless function name must identify one function unambiguously at that path. Missing paths, missing functions, mismatched classes, ambiguous selectors and malformed syntax fail verification with a reason.

   The head file is never imported, sourced, evaluated or executed. Decorators and test bodies remain data. The verifier performs no unittest discovery and launches no selector.

   `--checks` supplies prefetched API data. Its JSON contains the repository, exact head, raw ruleset response and raw check-runs response pages. The orchestrator obtains the ruleset with an individual gh read and obtains the head's check runs with one individual `gh api --paginate --slurp` command against `repos/{owner}/{repo}/commits/<head>/check-runs?filter=latest&per_page=100`. The repository comes from the trusted checkout. The check-runs endpoint names the exact audited head.

   Each gh read runs outside the sandbox as the individual command permitted today. Its output is parsed inside the sandbox and recorded as data. The Python helper, JSON construction and JSON parsing do not run outside the sandbox. The worker uses fixtures for tests and prefetched inputs for authenticated reads; it never attempts to escape the sandbox through a Python gh subprocess.

   The required unit-test contexts come from the orchestrator's ruleset read. Their current names are `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)` and `test (macos-14, client)`. The sweep and head-authored workflow text cannot choose the required names. Missing or malformed ruleset data and an empty required unit-test set fail verification.

   Every required unit-test context must have its latest check run on the exact head with `status: completed` and `conclusion: success`. Pagination is consumed completely. Selection never searches older runs for a preferred success. A missing context, wrong head, pending run, skipped run, neutral conclusion, failure or malformed response fails verification with a reason.

   The verification record preserves the original selector, resolved path and function, head, required context names and selected check-run identities and conclusions. It states that selector presence and successful CI were checked. It never states that the named function ran.

   A P2/P3 finding with both checks satisfied receives a verified `test:` record. A P0/P1 finding receives `claim-recorded` and `refutation.ok: false` until programs item (16), P1-10 part 2, confirms it. Missing or ambiguous priority receives no P2/P3 acceptance. A P0/P1 marker always selects the stricter handling.

   The `source:` form fetches the named URL read-only, verifies that the quote occurs in the fetched page text and records the page's SHA256. The existing `file://` fixtures remain accepted for tests. A malformed form, failed fetch or absent quote fails verification with the reason. This check establishes quote occurrence and page identity; semantic refutation remains subject to the design's judgment rules.

   The `diff:` form uses the tool-fixed `<thread commit>..<audited head>` range. A caller-supplied range is accepted only when its endpoints equal those fixed commits, the thread's hunk is unchanged over that range and the disposition names why the path is unreachable. The reason retains the existing minimum of 20 characters. The result is recorded as `claim-recorded`. A range such as `<head>..<head>` is refused. Until programs item (16)'s second opinion confirms it, `--require-refutation` refuses a P0/P1 not-applicable resting on `diff:` alone.

   `--require-refutation` prints one line per not-applicable disposition with a missing, failed or not-yet-confirmed form and exits 1. The legacy `evidence=<command>` form is reported as `legacy-evidence` and fails only under `--require-refutation`. Exit 0 means the selected mode completed, exit 1 means a required refutation failed, and exit 2 means usage failure or a hold such as an unreadable sweep or a required missing thread commit. Missing check data fails the refutation and never authorizes local head-code execution.

2. `scripts/orchestrator/orch-gate.sh` enters a constructed `env -i` environment before any Git discovery or checkout.

   The trusted root is established from the wrapper's physical source location. Absolute tools are resolved in that root, and the existing private links directory supplies the private PATH. The interpreter is resolved in the trusted root before the review worktree is entered and is invoked directly with isolated Python options.

   The environment sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`. Every Git call carries `-c core.hooksPath=/dev/null` and `-c core.fsmonitor=false`, including discovery, authentication, data reads, checkout, cleanup and restoration. Inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_GLOBAL` and other caller Git overrides do not reach discovery. The existing removal and worktree-restoration trap remains effective on failure.

   The wrapper authenticates `scripts/orchestrator/dispositions.py` as it authenticates the gate and validator. The executed file is the trusted checkout's regular tracked file, and its SHA256 equals the SHA256 of `git show origin/main:scripts/orchestrator/dispositions.py`. Missing, changed, untracked or substituted verifier bytes refuse before execution. No verifier is loaded from the PR head or review checkout.

   Until PR #419 merges, the new verifier is absent from trusted main. The new gate step is exercised only by worker tests with a fixture main containing its authenticated verifier. Integration of PR #419 uses the existing trusted main gate. The candidate wrapper and verifier are never run on the orchestrator's host to bootstrap their own integration.

   After checkout and evidence preparation, the wrapper retains one dispositions re-validation step immediately before the gate. It validates the review-worktree sweep at the same path and working directory passed to `scripts/require-crit-review.py` through `PR_FEEDBACK_EVIDENCE`. It records that file's SHA256 in its output. It never validates the trusted-root source copy while the gate reads another copy.

   The orchestrator's prefetched checks are recorded at `.orchestration/<task>/checks.json` and supplied through `--checks` when a `test:` form needs them. Production evidence comes from the orchestrator's own API reads. Worker-authored check fixtures do not become production evidence. The wrapper passes the protected data to the authenticated verifier and does not accept cached `refutation.ok` values as authority.

   Under `DISPOSITIONS_REQUIRE_REFUTATION=1`, re-validation adds `--require-refutation`, and failure refuses with wrapper exit 2 and the tool's diagnostic lines. Without the variable, the same step reports verification failures without enforcing them. A usage failure, hold or verifier-authentication failure remains a wrapper refusal. The PR number and head come from the wrapper's existing arguments.

   The step executes no head code and no test selector.

3. `tests/unit/test_dispositions.py` retains temporary-repository coverage for changed-hunk proposals, untouched-line demands, all three refutation forms, legacy evidence and holds.

   `test_dispositions_proposes_fixed_for_a_changed_hunk_and_demands_not_applicable_otherwise` checks the actual fixing commit, an untouched line and unchanged existing dispositions. The review-body finding and literal-pathspec regressions remain.

   `test_require_refutation_fails_without_a_form_and_accepts_each_of_the_three` uses head-tree and prefetched-check fixtures for `test:`, a `file://` page for present and absent source quotes, and fixed-range diff fixtures for accepted and refused claims. It checks the recorded source hash, reporting mode and enforcement mode.

   `test_dispositions_holds_on_an_unreadable_sweep_or_a_missing_commit` retains exit-2 coverage for malformed input and an unavailable commit needed by a located in-diff thread.

   `test_diff_refutation_range_is_fixed_to_thread_commit_and_head_and_is_a_claim` retains arbitrary-range refusal, the unreachable-path reason and the P0/P1 second-opinion restriction.

   `test_dispositions_verifies_test_refutations_from_head_tree_and_required_checks` checks an exact present function with successful required checks for P2 and P3. It separately checks missing paths, absent functions, wrong classes, malformed check data, missing required contexts, incomplete pagination, wrong heads and pending or unsuccessful latest runs. An older successful run never overrides a newer failed or pending run. P0/P1 produce claims and fail `--require-refutation`. Missing priority does not acquire P2/P3 treatment.

   Head-test fixtures contain import and execution markers. Verification creates neither marker. The test forbids log reads, artifact commands and selector execution. Assertions describe static presence and CI conclusions without claiming a per-selector result.

4. `tests/unit/test_orch_gate_path.py` retains its existing fake-binary style and private-PATH, shim-refusal, cleanup and restoration coverage.

   `test_orch_gate_revalidates_the_dispositions_before_the_gate` checks that enforcement refuses before the fake gate runs when current verification fails, including when saved verification claims success. Reporting mode prints the failed verification and permits the fake gate. The audited head reaches the verifier, and no local head-test marker is created.

   `test_orch_gate_sanitizes_the_environment_before_git_discovery` supplies inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_GLOBAL` and Git configuration overrides pointing to a decoy repository. The gate selects the intended trusted root and PR worktree. The recorded first Git invocation already has the sanitized environment and required configuration arguments. Checkout and restoration retain those controls.

   `test_orch_gate_runs_dispositions_only_when_it_matches_main` supplies verifier bytes in fixture main. Matching trusted-checkout bytes execute. Modified bytes, a missing main version and a substituted file refuse before verifier or gate execution. A matching file in the head tree cannot authorize different trusted-checkout bytes.

   `test_orch_gate_validates_the_copy_it_reads` makes the source sweep and copied review sweep differ. The verifier and fake gate record the same sweep path and bytes, and the wrapper's reported SHA256 matches those bytes. A valid source copy cannot authorize an invalid review copy. Enforcement refuses before the fake gate runs.

   Fixture main is used for every case exercising the new step before merge. Fixture lines count against the test cap.

5. The inherited row `local:fa47987:1` remains the skipped-only rejection item.

   `tests/unit/test_dispositions.py::DispositionsTest::test_test_refutation_rejects_skipped_required_checks` checks that `skipped`, `neutral`, absent and incomplete required checks cannot satisfy `test:`, even when their output contains fabricated passing-test text. Exit 0 from a selector or helper supplies no evidence because verification executes no selector or helper from the head.

   Check-runs data does not distinguish a successful suite that skipped the named function. The report states that limitation when recording this row's absorption. This task makes no claim that static presence plus suite success proves execution of a non-skipped test.

6. The inherited row `local:fa47987:2` remains the not-applicable demand for upstream-only threads.

   A thread whose path and line are outside the audited base-to-head PR diff gets the not-applicable demand. Proposal generation checks PR-diff membership before a thread-commit lookup that the proposal does not need. An absent path, an uncovered line and an upstream-only change supply no branch fixing commit.

   The proposal is `not-applicable:` rather than a hold or an unrelated `fixed:` candidate. A separately requested `diff:` refutation still needs the thread commit required by fixed-range verification.

   `tests/unit/test_dispositions.py::DispositionsTest::test_dispositions_demands_not_applicable_for_a_thread_outside_the_diff` covers an absent path and an uncovered line without a readable thread commit and forbids an unnecessary gh lookup. `test_upstream_only_hunk_changes_demand_not_applicable` retains proof that a base merge supplies no branch fix.

7. The inherited row `local:bdbbbf9:3` remains the full-selector preservation item.

   `tests/unit/test_dispositions.py::DispositionsTest::test_test_refutation_preserves_the_full_selector` checks the original selector in the verification record and matches its complete file, module, class and function identity against the head tree. A similarly named function in another module or class cannot satisfy it. Selector parsing never discards module or class components to obtain a match.

8. The inherited row `local:bdbbbf9:2` remains the interleaved-output item and is moot under this design.

   Verification consumes no human-readable test output. Interleaved diagnostics and fabricated `... ok` lines have no authority. The old CI-log parser is deleted. The head-tree and check-runs regressions assert that no log request is made and that unrelated output text cannot change the result.

9. `.orchestration/dotfiles-T133-dispositions-a02/report.md` states the proposal rule, the three forms, static selector verification, required-check selection, the priority restriction and the legacy-evidence transition.

   The report pastes the output of `grep -l "evidence=" .orchestration/validation/*-pr-feedback.json | wc -l` and identifies it as a count of matching records. It names programs item (16), `audit-pool.sh --second-opinion`, as P1-10 part 2 after PR #410.

   The report maps the four inherited rows to items 5 through 8 and their final-head evidence. They belong to this reset and receive no new advisory deferral. The report distinguishes predecessor results from new red-then-green evidence.

   The report records withdrawal of the artifact design, the strength and skipped-test limitation of the replacement evidence, D-024-17's ownership of the outside-sandbox exception, the environment controls, verifier authentication and the validated sweep's SHA256.

## Out of scope

`audit-pool.sh --second-opinion` is programs item (16) and P1-10 part 2, after PR #410. This task adds no second-opinion mode and accepts no saved consensus boolean as a substitute.

`scripts/require-crit-review.py` remains unchanged. Its existing disposition and commit validators are reused or re-implemented read-only. `fill_sweep.py`, `pr-feedback.py` and the sweep format remain unchanged. The chain scripts continue calling the gate wrapper.

Flipping `DISPOSITIONS_REQUIRE_REFUTATION` remains a decision row. This task changes no enforcement default.

All workflows remain unchanged, including `.github/workflows/test.yaml` and `.github/workflows/regime.yml`. `scripts/orchestrator/regime-ci.py` and the Makefile remain unchanged. `scripts/ci/unittest-results.py` and `tests/unit/test_unittest_results.py` are excluded. The regime job receives no head-test execution or selector-result responsibility.

CI-log parsing, results-artifact production, artifact downloads and head-test execution during refutation verification are excluded.

The worker-exclusion change owned by D-024-17 and plan 024 P1-15 is outside this task. This task changes no sandbox permissions, exclusion configuration or executable-selection policy for worker seats.

## Check

`make format` completes, and `uv run python -m unittest tests.unit.test_dispositions tests.unit.test_orch_gate_path -v` is green. `shellcheck scripts/orchestrator/orch-gate.sh` and `shfmt -d scripts/orchestrator/orch-gate.sh` are clean.

The new head-tree and required-check regression, the skipped-check regression, the outside-diff regression, the full-selector regression and the three named gate-boundary regressions have recorded red runs against `bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3` and green runs against the final head. Each record names its tested revision, exact selector, command, exit status and output. Unsupported predecessor inputs are recorded as unsupported inputs and are never presented as exploit reproductions.

The interleaved-output item records deletion of the log parser and the final-head assertions that log commands and free-text outcomes have no authority. Historical green runs do not replace final-head evidence.

The real-sweep check retains PR #409 and head `4fe243803971bd5ba8ab45f8ede5cfb4dd37f719`. Required thread commits are read with individual gh commands and saved as `.orchestration/dotfiles-T133-dispositions-a02/thread-commits.json`. The helper runs inside the sandbox as `uv run --no-project python -I scripts/orchestrator/dispositions.py 409 4fe243803971bd5ba8ab45f8ede5cfb4dd37f719 --feedback .orchestration/validation/dotfiles-T133-ci-efficiency-a02-pr-feedback.json --commits .orchestration/dotfiles-T133-dispositions-a02/thread-commits.json`. Its output is pasted once.

A real `test:` verification uses the orchestrator's own prefetched ruleset and exact-head check-runs data through `--checks`. The validation record includes the individual gh commands, repository, requested head, exit statuses and raw-response hashes. A missing real input remains a failed verification and is never replaced by a worker fixture.

All command output is pasted in `.orchestration/dotfiles-T133-dispositions-a02/validation.md`. Sandbox records identify each individual outside-sandbox gh command and the in-sandbox helper and parser. The record identifies fixture-main tests separately from production gate execution.

At `bdbbbf91`, the measured diff contains 284 changed lines outside `tests/` and `.orchestration/`, and 279 under `tests/`. `git diff --numstat origin/main...HEAD` records the final totals: at most 420 changed lines outside `tests/` and `.orchestration/`, and at most 480 under `tests/`. Changed lines are additions plus deletions, including fixtures.

No local Bats tests run. Required Bats results come from GitHub Actions. The orchestrator runs task-consistency-check C1 to C10 and C7b before dispatch and at acceptance.

## Completion

PR #419 continues on `tools/dispositions-a01` from `bdbbbf91765a8f9c2f94565096c8bcbf2fca47b3`, rebased onto main containing `0e496ce7` and merged PR #421 before the first push. The first push deletes the a01 task copy and adds the byte-identical dispatched a02 copy. This reset creates no fresh implementation branch or second implementation PR.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's branch, dependency and review requirements, `dotfiles-T133-dispositions-followup-a01` as the owner of any new advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-dispositions-a02/task.md>` in RESULT. The orchestrator writes that owner task before assigning its first advisory row. The four inherited rows remain completion requirements of a02.

RESULT also carries `precheck=<sha256 of .orchestration/dotfiles-T133-dispositions-a02/precheck.json>` when `scripts/orchestrator/result-precheck.sh` has merged through PR #411, and otherwise carries `precheck=pending-411`.

Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. The predecessor's pre-RESULT fix round, amendment, revise and S2 stop remain recorded. This reset does not recast predecessor findings or failed verification as approvals.

The worker's own pre-push review is one round at most. A P0/P1 surviving that round is sent in RESULT as open and stops integration. The worker starts no further private correction-and-review cycle to avoid reporting it. Any later permitted round remains subject to INV-6 and the inherited completion rule.

No `@codex review` comment is posted. Automatic final-head Bot reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required CI passes before a completion RESULT. RESULT identifies every inline and review-body finding, its proposed disposition and every surviving P0/P1 as `open:<thread id>` or `open:review-<review id>`.

A Codex seat writes evidence at the same relative paths in its worktree and says so in RESULT. Worker-side review evidence carries the required `-worker-` infix. RESULT names the head, base, branch, changed files, Bot findings and dispositions, open P0/P1 findings, exact test selectors, red-then-green evidence, caps, the one new script, task-copy hash and artifact paths. The orchestrator copies worktree evidence by absolute path before review.

This task is `security: true`. Under C-80, a separate security-profile context reviews this complete revised text before dispatch. That review is a dispatch prerequisite and is not claimed as completed by this text. The orchestrator also runs the task-level audit and a separate security-profile review on the final implementation head.

Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. A changed head receives fresh required evidence. Integration of this PR uses the existing trusted main gate; the new step remains confined to fixture-main tests until merge. Merge uses `gh pr merge --squash --match-head-commit <audited head>`.

Commands for gh and Git writes run individually, without shell chaining or a wrapper combining writes. A classifier denial produces a blocked PONG naming the command and reason. Until P1-14 lands, strings containing `gh pr merge` or `gh pr create` are written with the file-edit tool rather than a Bash heredoc or `echo`.

## Sequencing note (orchestrator, 2026-10-19T03:0xZ)

This task edits `scripts/orchestrator/orch-gate.sh`, which `dotfiles-T133-permission-guard-gate-a05` also edits (the sanitized environment of design 5.14 item 2 and the private uv cache of item 9). The a05 change lands first; this task starts after PR #420 merges, rebases onto that main, and its orch-gate.sh item builds on the sanitized environment a05 provides instead of adding a second one. Design 5.14 applies to this task by reference (D-024-18); the threat table's environment, trusted-path and committed-ledger rows are read against it.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```

Local Bats tests, live enforcement changes and head-code execution during refutation verification are not performed.
A `test:` refutation has the strength of the head's CI and supplies no proof against a head-authored test; P0/P1 claims remain unrefuted until the item-16 second opinion confirms them.