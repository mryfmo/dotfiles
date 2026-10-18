---
format: 2
task_id: dotfiles-T133-regime-ci-a02
kind: code
security: true
allowed_files:
  - .github/workflows/regime.yml
  - scripts/orchestrator/regime-ci.py
  - tests/unit/test_regime_ci.py
  - tests/unit/test_workflow_security.py
  - .orchestration/dotfiles-T133-regime-ci-a02/**
after: []
reset_of: [dotfiles-T133-regime-ci-a01]
threat_table:
  - control: ".github/workflows/regime.yml (pull_request_target, base-sha checkout, pull-ref fetch and base-only verifier execution)"
    disposition: "residual: pull_request_target runs the base's workflow with exactly contents: read and no secret beyond GITHUB_TOKEN's read scope; the fetched head is data, never checked out or executed; test_the_regime_workflow_runs_base_code_only checks the workflow shape and the final-head security review checks the execution boundary."
  - control: "scripts/orchestrator/regime-ci.py (head data read through git show, the base's checker on a temporary task copy, dispatched-text authentication at the base, precheck binding, allowed files, caps and content-based exemption)"
    disposition: "closed: tests/unit/test_regime_ci.py::test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier"
  - control: "tests/unit/test_regime_ci.py (temporary repositories, retained a01 regressions and the four redesign tests)"
    disposition: "residual: fixtures create base and head commits without executing head content; the audit reads the assertions, the red results against 4a921414 and the final-head green results."
  - control: "tests/unit/test_workflow_security.py (amendment 1's single EXPECTED_PERMISSIONS entry for regime.yml)"
    disposition: "residual: the module differs from origin/main by exactly the entry \"regime.yml\": {\"contents\": \"read\"}; the task-level audit compares that diff against amendment 1."
  - control: ".orchestration/dotfiles-T133-regime-ci-a02/** (the reset task's branch artifacts)"
    disposition: "residual: artifacts remain in this task's directory, distinguish historical evidence from redesigned results and carry commands, exit statuses and tested heads for the final-head audit."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-regime-ci-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-regime-ci-a01/task.md)"
    disposition: "residual: the worker deletes the predecessor copy in the first push and adds this dispatched text byte-identically at the a02 path; the TASK and RESULT bind the a02 copy's own SHA256 and the orchestrator verifies the replacement at acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-regime-ci-a02/ (report.md, validation.md, sandbox.md and learning.md)"
    disposition: "residual: records contain prose and pasted command output; sandbox.md lists every refused command and the audit compares the records against the final diff and CI."
  - control: task metadata
    disposition: "residual: the base's dispatched text authenticates the copy and its policy; missing dispatched text produces the explicit unverifiable warning or REGIME_REQUIRE_DISPATCHED failure, and the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance."
  - control: metadata separators
    disposition: "residual: YAML parsing uses the bounded first front-matter document and the dispatched-text byte comparison covers the complete task copy, including its separators."
  - control: in-process effects
    disposition: "residual: the verifier runs git read commands and the base's checker, writes only temporary data files and executes no head content; the first PR's explicitly recorded local bootstrap uses the reviewed candidate verifier with the base's checker."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: the workflow pins checkout and setup-uv to the existing action SHAs, disables persisted credentials and uv caching, passes event values through env and runs uv with --no-config --no-project and Python with -I from the base checkout; production promotion flags remain the operator's decisions."
  - control: new or renamed scripts
    disposition: "residual: regime-ci.py is the only new executable script in this PR; any additional new or renamed script is an undeclared change the audit fails."
  - control: orchestrator effect merge
    disposition: "residual: merge occurs only through gh pr merge --squash --match-head-commit <audited head> after the integration gate in Orchestrator Playbook step 10.5; no local merge or push to main is authorized."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the feedback sweep, the task-level audit and the security review bind the new final head before the gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; herdr-agents --remove-worker refuses a dirty worktree without --force and any forced removal records the uncommitted state it discarded in the acceptance record."
premises:
  - claim: none of the three new files exists on origin/main
    command: git ls-files .github/workflows/regime.yml scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py | wc -l
    output: |-
      0
  - claim: the other workflows pin actions/checkout and astral-sh/setup-uv by sha, the shas regime.yml reuses
    command: "/usr/bin/grep -h 'uses: actions/checkout@\\|uses: astral-sh/setup-uv@' .github/workflows/*.yaml | sed 's/^[- ]*//' | sort -u"
    output: |-
      uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
      uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
  - claim: the task-consistency checker on main documents eleven checks (C1 to C10 and C7b), the unit rules regime-ci runs as a subprocess; C11 to C15 arrive with PR #417 and need no change here
    command: /usr/bin/grep -c '^C[0-9]*b\? ' scripts/orchestrator/task-consistency-check.py
    output: |-
      11
  - claim: the result.txt convention (plan 024 programs (4)) is not on main yet, so the precheck rule applies only when .orchestration/<task>/precheck.json exists in the PR
    command: /usr/bin/grep -c 'result.txt' scripts/orchestrator/result-precheck.sh 2>/dev/null || echo absent-on-main
    output: |-
      absent-on-main
  - claim: the ruleset's seven required contexts do not include regime, so the job starts optional (its promotion is the operator's ruleset step through P1-14's ruleset-request.sh)
    command: gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context]|map(select(.=="regime"))|length'
    output: |-
      0
  - claim: the first PR cannot run its own pull_request_target job because the base has no regime.yml; PR #418 supplies a local run of the job's command line and the job runs on later PRs after it lands
    command: git cat-file -e origin/main:.github/workflows/regime.yml
    output: |-
      (pasted by the worker in validation.md after the command runs, with the resolved base SHA and exit status)
---

# AGMSG-TASK dotfiles-T133-regime-ci-a02 — S1 redesign of dotfiles-T133-regime-ci-a01 (plan 024 P1-11; PR #418)

This text is the independent redesign by a review-profile context other than a01's author. Codex Bot review `5564850518` on `4a921414` produced three P1 findings of class `trust-boundary-pr-input`, recorded as S1 under C-59 in the a01 acceptance record. The root cause was a01's specification of head execution, head-controlled policy authentication and a branch-name exemption.

PR #418 continues on the same branch, `tools/regime-ci-a01`, from `4a921414`. The worker deletes `.orchestration/dotfiles-T133-regime-ci-a01/task.md` in the first push and adds this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-regime-ci-a02/task.md`. The predecessor-copy deletion is the reset bookkeeping named by `reset_of`. The predecessor's other evidence remains unchanged as historical evidence. This reset uses one PR.

The existing Claude standard worker continues implementation. CI YAML and this Python verifier are outside the worker seat's execution boundary. The a01 worker's review fixes and amendment 1 remain part of the implementation, with the head-execution and authentication rules replaced below. The a01 acceptance history retains its stopped status and counters.

The first five premises reproduce a01's write-time observations verbatim. Current observations and premise 6's deferred output are recorded in `validation.md` without changing the dispatched task copy.

## Goal

One GitHub job, `regime`, checks each pull request carrying a task copy against authenticated dispatched policy when that policy exists at the base. It reports one line per violation and passes a records-only pull request without a target with `regime-ci: no target (records-only)`.

The job runs the workflow, verifier and task-consistency checker from the trusted base. The fetched head supplies data only. The task copy, `result.txt`, `precheck.json` and branch name are PR-controlled claims. Missing base-dispatched policy remains visible as a warning while the check is optional and becomes a violation when the operator enables `REGIME_REQUIRE_DISPATCHED=1`.

## Files

1. `.github/workflows/regime.yml` uses `pull_request_target` with types `opened`, `synchronize`, `reopened` and `ready_for_review`. Its top-level `permissions:` block contains exactly `contents: read`, with no job-level override and no secret input. It retains concurrency group `regime-pr-${{ github.event.pull_request.number }}` with `cancel-in-progress: true`, one job named `regime` on `ubuntu-24.04` and `timeout-minutes: 10`.

   `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1` uses `fetch-depth: 0`, `ref: ${{ github.event.pull_request.base.sha }}` and `persist-credentials: false`. `astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7` retains `enable-cache: false`.

   The workflow passes the PR number, base SHA and head SHA through step environment variables. A fetch step runs `git fetch --no-tags origin "refs/pull/${PR_NUMBER}/head:refs/regime/pr-head"` and verifies that the fetched commit equals the event's head SHA. The destination is a detached ref and the working tree remains at the base SHA. A disagreement fails the run.

   The verifier step runs `uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "${BASE_SHA}" --head "${HEAD_SHA}"`. The workflow checks out no head or merge commit, invokes no head script or action, and imports, sources or executes no fetched file. All event expressions reach shell commands through `env`.

2. `scripts/orchestrator/regime-ci.py --base <ref> --head <sha> [--root <checkout>]` remains Python with PyYAML through `uv run --no-config --no-project --with pyyaml`, the standard library otherwise and an English shdoc-style module docstring. It resolves the arguments to commit SHAs and uses the base checkout as `--root`, defaulting to the current Git toplevel. The checkout check binds `HEAD` to the resolved base rather than the head.

   The script lists the complete `git diff --name-only --no-renames -z <base>...<head>` and corresponding NUL-delimited numstat. Its targets are task directories touched by that diff that carry `.orchestration/<t>/task.md` at the head. Historical task directories untouched by the PR are not targets. Every head file is read through `git show <head sha>:<path>` into bytes or temporary data files. No read depends on a head working tree.

   The copy passes the base checkout's tracked checker, invoked as `uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <base checkout> <temporary copy>`. Temporary task data does not replace tracked base files. The checker's lines are reported verbatim with `regime-ci: <t>: checker:`. Its verdict counts only when its verdict line agrees with its exit status; a crash, missing verdict or contradictory exit status is a violation. The explicit `task-id` check compares the copy's front-matter `task_id` with `<t>`. The retained C1 adaptation suppresses only the checker's filename mismatch caused by naming a temporary copy `task.md`; other checker findings remain violations.

   The dispatched text is read only from `<base sha>:.orchestration/tasks/<t>.md`. When it exists, the head copy must be byte-identical. The base text supplies the policy for `allowed_files`, caps and `reset_of`; a head edit to either the copy or a dispatched-text file cannot replace that policy. A byte mismatch is a `task-copy` violation.

   When the base lacks dispatched text, the copy remains unverifiable even if the head contains `.orchestration/tasks/<t>.md` or a matching `result.txt` token. The script prints `regime-ci: warning: <t>: task copy unverifiable (no dispatched text at base)` while `REGIME_REQUIRE_DISPATCHED` is unset. With `REGIME_REQUIRE_DISPATCHED=1`, the same condition is a `task-copy` violation and the run exits 1. Checks against the claimed copy still run during this transition, and their results do not authenticate its policy.

   A present `result.txt` retains the `task_copy=` consistency check against the copy's SHA256. A mismatching or missing token is a violation when that result file supplies the binding. A matching token is self-attested and cannot remove the unverifiable warning or satisfy the promotion flag. Matching `precheck=` and `task_copy=` tokens establish consistency among PR-controlled records, not independent authorization.

   A present `.orchestration/<t>/precheck.json` retains the worker's corrected binding rule. Its `head` is a 40-hex commit ID equal to the checked head, or an ancestor whose complete difference to the head contains only this task's evidence paths and its declared reset predecessor's evidence paths. The comparison uses the full ancestor-to-head diff, including changes reverted relative to the PR base. Its bytes' SHA256 equals `result.txt`'s `precheck=` token. Invalid JSON, an invalid head, an unrelated commit, code drift or a hash mismatch is a violation. An absent precheck prints `regime-ci: warning: <t>: precheck absent`; the later `PRECHECK_REQUIRED` transition remains outside this task.

   Every changed path matches an `allowed_files` entry of the applicable policy. Plain entries match exactly, `/**` matches the directory prefix, and `*` and `?` stay within a path segment. Each stray path is a violation. The cap parser reads the policy's `## Check` section, accepts the retained parenthetical wording such as `changed lines (added plus deleted) outside`, and compares additions plus deletions with the outside and tests caps. Backticked paths remain accepted and the default exclusions remain `tests/` and `.orchestration/`. Each exceeded cap is a violation and each missing cap produces a warning. Numstat paths containing tabs remain intact. Binary files retain the documented zero-line count. The checker supplies C4 and C7b without a second implementation.

   Amendment 1's lineage rule remains. A later copy whose `reset_of` names a predecessor is the checked copy for that lineage, and each retained predecessor copy produces `regime-ci: warning: <t>: predecessor copy <path> (reset_of of <later task>)`. A copy that no later copy names remains its own target. The applicable policy's reset predecessor directories remain lineage evidence for allowed-files and evidence-only precheck comparisons after the predecessor task copy is deleted. Base-dispatched metadata controls this exemption whenever available; provisional head metadata never removes the unverifiable warning or failure.

   A diff with no target passes only when every changed path is under `.orchestration/`. A path outside that directory with no task copy is a violation. Neither `GITHUB_HEAD_REF` nor any other branch-name input grants an exemption.

   The verifier retains one finding per line on stdout as `regime-ci: <t>: <rule>: <detail>`, warnings prefixed `regime-ci: warning:`, exit 1 for violations and the final `regime-ci: ok <n> task(s)` with exit 0 otherwise. Failed Git listings retain exit 2 and cannot become empty successful diffs. A head edit to the workflow or verifier scripts retains an audit warning whose wording identifies the base versions as the executing versions.

3. `tests/unit/test_regime_ci.py` retains the a01 rule regressions, amendment 1's lineage test and the worker's review coverage. Fixtures now hold the verifier and checker at the base and run from a base checkout against fetched head data. The old head-checkout assertion becomes a base-checkout assertion. Expected result-binding warnings and workflow expectations follow item 2 rather than the withdrawn head-execution design.

   `test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr` retains the consistent case and one subtest per rule branch, each asserting the violation's rule, detail and exit status. Coverage retains checker crashes and verdict/exit disagreement, directory/task-ID mismatch, both caps and parenthetical wording, precheck hash and 40-hex validation, non-ancestor and evidence-only ancestry, reverted prechecked changes, Git listing failure, missing-cap warnings, result-token mismatch and uv configuration isolation.

   `test_the_regime_workflow_runs_base_code_only` is written first and is red against `4a921414`. It asserts the `pull_request_target` trigger and event types, permissions exactly `contents: read`, no job permission override, the pinned actions, base-SHA checkout, `fetch-depth: 0`, disabled credential persistence, pull-ref fetch and fetched-head binding. It asserts that no step checks out the head or executes a path populated from head content. It retains the concurrency, job-name, `--no-config`, isolated-Python and environment-transport assertions.

   `test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier` is written first and is red against `4a921414`. Its fixture head changes both `scripts/orchestrator/regime-ci.py` and `scripts/orchestrator/task-consistency-check.py` to programs that would falsely pass and leave execution markers. The base policy allows those two script paths so their edits alone do not explain a failure. The compliant case passes, the violating case is rejected by the base verifier and base checker, and no head-program marker appears. A forged dispatched file at the head and a recomputed result token cannot replace base policy or authorize an otherwise forbidden path. The checkout remains at the base throughout.

   `test_regime_ci_exempts_records_only_heads_by_content_not_branch_name` is written first and is red against `4a921414`. A branch named `orchestration/x`, with `GITHUB_HEAD_REF` set to the same name, carries a code change and receives the normal checks or the missing-target violation. A feature branch whose changed paths are only under `.orchestration/` and which has no target receives the records-only line and exit 0.

   `test_regime_ci_unverifiable_copy_is_a_warning_until_the_flag` is written first and is red against `4a921414`. The base lacks dispatched text while the head carries a well-formed copy and a matching self-attested `task_copy=` token. A head-dispatched file does not change the outcome. Without the flag the test asserts the unverifiable warning and exit 0; with `REGIME_REQUIRE_DISPATCHED=1` it asserts a `task-copy` violation and exit 1.

   Fixture lines count against the test cap. Historical red evidence remains labelled with its original commit, and the four redesign tests have their own red evidence against `4a921414` before implementation.

4. `.orchestration/dotfiles-T133-regime-ci-a02/report.md` states the replacement of head execution by base execution, the head's role as data and the base-dispatched authentication rule. It records the precheck ancestor correction, the two transition warnings, the self-attested nature of result bindings and the condition under which each warning becomes a failure. It explains that dispatched records currently land on main at boundaries and that promotion requires enforcing dispatch-before-PR order. It records the operator's separate decision rows for required-check promotion and `REGIME_REQUIRE_DISPATCHED=1`, with `ruleset-request.sh` owning the ruleset step after P1-14.

   `tests/unit/test_workflow_security.py` retains amendment 1's exact one-line addition to `EXPECTED_PERMISSIONS`, `"regime.yml": {"contents": "read"}`. No other line in that module changes.

5. Bot P1 thread `4308651010` is fixed by the base-selected workflow, explicit base-SHA checkout, pull-ref data fetch and base-only verifier and checker execution in items 1 and 2. Editing either verifier at the head changes data reviewed by the audit and cannot change this run's verdict logic.

6. Bot P1 thread `4308651011` is fixed by authenticating the copy against dispatched text at the base and deriving policy from that trusted text. Head-dispatched files and `result.txt` hashes remain claims. Missing base-dispatched text produces the explicit warning until the operator enables `REGIME_REQUIRE_DISPATCHED=1`, when it becomes a failure.

7. Bot P1 thread `4308651013` is fixed by deriving the records-only exemption solely from the complete changed-path list. A branch name beginning with `orchestration/` supplies no authority.

8. The first PR adding `regime.yml` cannot run its own `pull_request_target` job because its base has no workflow. PR #418 supplies a local run of the job's command line against its final head, pasted in `validation.md` with the base SHA, head SHA, command, output and exit status. The local bootstrap uses an isolated base checkout with the reviewed candidate `regime-ci.py` installed for that run, since the script is also absent at the base. The checker remains the base copy and the fetched head remains data. This bootstrap is recorded as local development evidence, and the workflow gains no head-execution fallback. Earlier a01 `regime` runs remain historical evidence. Every later PR runs the landed base workflow.

## Out of scope

Making `regime` a required check and setting `REGIME_REQUIRE_DISPATCHED=1` in production are the operator's separate decision rows. This task implements and tests the flag while leaving it unset in the workflow. Promotion follows the decision that dispatched task text reaches the base before the PR.

`scripts/orchestrator/task-consistency-check.py` remains owned by P1-12, PR #417. `result-precheck.sh` and `result.txt` remain owned by P1-5, PR #411. `dispatch.sh` remains owned by P1-5 and P1-6, and `verdict.sh` remains owned by P1-4a. Other workflow files remain owned by F5, PR #409, and the private-bootstrap workflow remains outside this task.

The worker leaves canonical predecessor task text, acceptance records and operator decision records unchanged. The orchestrator owns reset records, promotion decisions and advisory-finding owner tasks.

## Check

`make format`, `uv run python -m unittest tests.unit.test_regime_ci -v` and `uv run python -m unittest tests.unit.test_workflow_security -v` have their commands, verbatim output, exit statuses and tested heads pasted in `.orchestration/dotfiles-T133-regime-ci-a02/validation.md`. The unit modules are green. An inherited formatting failure is reproduced on the unchanged base and recorded as a failure with that evidence; it is never labelled green or repaired outside `allowed_files`.

The four redesign tests are written before implementation and each has a red result against `4a921414`, followed by a green result on the redesigned final head. The retained worker-review and amendment 1 regressions remain green. No local Bats tests run.

The local bootstrap reproduces the job's command line, `uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "${BASE_SHA}" --head "${HEAD_SHA}"`, once against the worker's final PR head. The validation records the isolated base checkout, candidate verifier source, base checker source, fetched head and the complete output. The a02 task copy is its target. Missing base-dispatched text and an absent precheck are expected warnings during their documented transitions; other violations remain findings to fix.

`git diff --numstat origin/main...HEAD` shows at most 330 changed lines outside `tests/` and `.orchestration/`, 480 under `tests/`. Changed lines are additions plus deletions and fixtures count against the test cap. The validation includes the totals and changed-file inventory.

The first PR's absent base workflow is recorded with premise 6's command and output. Its local run replaces the a01 requirement to paste this new job's own GitHub run. Other GitHub Actions checks on the final head still pass. After the workflow lands, validation for later PRs includes the actual final-head `regime` conclusion from `gh run view`.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The a02 task copy remains byte-identical to the dispatched file.

## Completion

One branch, `tools/regime-ci-a01`, continues PR #418 from `4a921414`. The first push deletes the a01 task copy and adds the byte-identical a02 copy. This reset creates no second implementation PR.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's existing-PR continuation, first-PR evidence rule and prohibition on `@codex review` comments taking precedence. `dotfiles-T133-regime-ci-followup-a01` owns any advisory P2, and the orchestrator writes its task file before recording ownership. Every worker-side fix round counts toward INV-6 under C-61. The stopped a01 history remains intact.

The RESULT carries `task_copy=<sha256 of .orchestration/dotfiles-T133-regime-ci-a02/task.md>`. It also carries `precheck=` when `scripts/orchestrator/result-precheck.sh` has merged, otherwise `precheck=pending-411`. The report and RESULT identify the final head, base, branch, changed files, test names, caps, evidence paths and every Bot thread's disposition, including threads `4308651010`, `4308651011` and `4308651013`. Worker-side review evidence uses the required `-worker-` infix.

This task is `security: true`. The orchestrator runs the task-level audit and a separate security-profile review on the final head. Final-head CI, the feedback sweep, audit dispositions, acceptance record and gate follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives fresh evidence.

No `@codex review` comment is issued. Commands for every `gh` and Git write run individually, without shell chaining or a wrapper combining writes. A classifier denial produces a blocked PONG with the command and refusal. Until P1-14 lands, any string containing the words gh pr merge or gh pr create is written with the file-edit tool, never in a Bash heredoc or echo.

Local Bats and production promotion are outside this task. Unverifiable policy remains a warning until the operator enables `REGIME_REQUIRE_DISPATCHED=1`.

## Amendment 1 (round 1, 2026-10-18T21:4xZ): the checker never reads a pull request's text

a008's review of 4a921414..bcbd6949 (21:37:56Z) found a P0 of the class trust-boundary-pr-input in this text: item 2's sentence that the checks against the claimed copy still run feeds the head's task copy to the base checker, whose C10 runs `git grep -qF <backticked literal>` unquoted, so a literal `--open-files-in-pager=CMD` in a PR's copy runs CMD inside the pull_request_target job. That sentence is withdrawn. The base checker (`task-consistency-check.py` from the base commit) reads only the dispatched text at the base (`.orchestration/tasks/<t>.md` on the base sha) and never a byte of the head's copy; when the base lacks the dispatched text the copy is unverifiable, the checker is skipped with the warning line, and only the pure-Python reads of the copy (yaml.safe_load for allowed_files and the Check sentence, with no subprocess given any string from it) still run; an authenticated predecessor copy is superseded only by an authenticated successor (a reset_of chain is honoured only when both copies verify against the base); the precheck diff uses `--no-renames`. The checker's own hardening (`git grep -e` for literals, C6 path containment) belongs to P1-12 (`dotfiles-T133-task-generator-plan-check-a02`) and lands before `regime` is promoted. Regression tests: a head copy whose backticked literal is `--open-files-in-pager=<marker command>` runs nothing (the marker is never written) and the copy is reported unverifiable; a verified copy reaches the checker from base bytes only. This is INV-6's first amendment (C-61); the counters are pasted below.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-regime-ci-a02.md: OK
premises 1 to 5: copied from a01 verbatim (write-time outputs of 2026-10-18 22:0x JST); premise 6: the first PR cannot run its own pull_request_target job (the base has no regime.yml)
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-regime-ci-a02.md
```