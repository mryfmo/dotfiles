---
format: 2
task_id: dotfiles-T133-audit-pool-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/audit-pool.sh
  - scripts/orchestrator/orch-audit.sh
  - .schemas/classes.yaml
  - tests/unit/test_audit_pool.py
  - .orchestration/dotfiles-T133-audit-pool-a01/**
after: []
threat_table:
  - control: "scripts/orchestrator/audit-pool.sh (the exclusively locked queue, unique audit-key reservations, bounded concurrency, isolated slots, validated results and bounded retries)"
    disposition: "residual: pool fixtures exercise concurrent selection and subprocess outcomes in temporary repositories; killed-pool running files retain their reservations until explicit cleanup and are reported when requests wait."
  - control: "scripts/orchestrator/orch-audit.sh (head selection, differential finding verification, JSON extraction, schema validation, existing refusals and masking before diagnostics)"
    disposition: "residual: retained refusal and masking cases and the two new audit regressions exercise extraction and disclosure boundaries; the final-head audit and separate security review assess their combined coverage."
  - control: ".schemas/classes.yaml (the controlled finding vocabulary, remedy sentences and blast_radius globs)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius"
  - control: "tests/unit/test_audit_pool.py (the retained pool and audit cases, pinned schema fixture and three new regressions)"
    disposition: "residual: fake codex and sleep exercise queue, retry, differential and masking behavior without live audits or retry delays; temporary repositories and worktrees isolate fixture effects."
  - control: ".orchestration/dotfiles-T133-audit-pool-a01/** (this sibling task's branch artifacts)"
    disposition: "residual: artifacts remain within this task's directory, identify source cherry-picks and tested heads, and distinguish inherited material from this PR's validation."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-audit-pool-a01/task.md)"
    disposition: "residual: the copy is byte-identical to the dispatched text and its own SHA256 appears in the TASK and RESULT; the orchestrator checks byte identity at acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-audit-pool-a01/ (report.md, validation.md, sandbox.md, learning.md and revise.yaml)"
    disposition: "residual: records list the cherry-picked source SHAs and resulting commits, retained fixes, three new regressions, refused commands, final inventory, caps and final-head results."
  - control: task metadata
    disposition: "residual: the orchestrator checks the dispatched front matter with task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; byte identity covers subsequent metadata changes."
  - control: metadata separators
    disposition: "residual: the first document separators bound the YAML front matter and the dispatched-file byte comparison covers the complete task copy."
  - control: in-process effects
    disposition: "residual: queue selection and reservation occur under one exclusive lock, audit subprocesses use pool-specific worktrees, and only validated and masked results become usable evidence."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter configuration changes; Python checker subprocesses run isolated, request and slot values are validated before use, and ORCH_REVIEW_WORKTREE selects a pool-specific slot without weakening existing audit refusals."
  - control: new or renamed scripts
    disposition: "residual: the only new executable is the declared pool script, the existing audit wrapper is modified and the declared vocabulary is data; the final inventory contains no verdict implementation, JSON schema addition or undeclared helper."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges only with gh pr merge --squash --match-head-commit <audited head> after the integration gate; no local merge or push to main is authorized."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch changes the head, so required CI, the feedback sweep, task-level audit and security review bind the resulting final head before the gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records the discarded uncommitted state in the acceptance record."
premises:
  - claim: the a02 branch holds the three implementation and vocabulary files inherited by this sibling
    command: git ls-tree --name-only b8998de162afc72d53d07679b8f0a194fcc480ff scripts/orchestrator/audit-pool.sh scripts/orchestrator/orch-audit.sh .schemas/classes.yaml | wc -l
    output: |-
      3
  - claim: audit-pool.sh and classes.yaml are absent from a clean origin/main checkout before cherry-picking
    command: git ls-files scripts/orchestrator/audit-pool.sh .schemas/classes.yaml | wc -l
    output: |-
      0
  - claim: orch-audit.sh is already tracked on origin/main
    command: git ls-files scripts/orchestrator/orch-audit.sh | wc -l
    output: |-
      1
---

# AGMSG-TASK dotfiles-T133-audit-pool-a01 — audit-pool sibling on tools/audit-pool-a01 from origin/main (plan 024 P1-4a; own PR)

This task is the new sibling lineage created by the independent review-profile redesign of `dotfiles-T133-verdict-audit-pool-a02`. The combined task stopped under plan 006 INV-6 S2 after the local review of `b8998de162afc72d53d07679b8f0a194fcc480ff` found two P1 and three P2. The stopped acceptance history and its counters remain unchanged.

The worker creates `tools/audit-pool-a01` from `origin/main` and re-runs all three premises before cherry-picking. The a02 branch's commits introducing and modifying `scripts/orchestrator/audit-pool.sh`, `scripts/orchestrator/orch-audit.sh`, `.schemas/classes.yaml` and `tests/unit/test_audit_pool.py` are cherry-picked for those four paths only. Mixed-path source commits contribute only their changes to these paths. The report lists every cherry-picked source SHA, its resulting commit and any conflict resolution.

This branch contains the four inherited files at the b8998de behavior baseline, this task's fixes and its own artifacts. Verdict code, JSON schema additions, predecessor task copies and predecessor evidence do not enter its cumulative diff. This task has its own PR, reviews, audit and acceptance record. PR #410 remains the verdict sibling's PR.

The design is `.orchestration/plans/024-design-programs.md` items (2) and (3). Item (16)'s second-opinion mechanism remains outside this task. `.schemas/classes.yaml` remains the vocabulary path because checker C2 excludes another task's `.orchestration/` directory from `allowed_files`.

## Goal

Queued audits run with bounded concurrency in separate pool worktrees and retain only schema-valid, masked audit JSON. Differential results account for every previous finding with a status verified against the previous-to-current diff.

Decoded schema errors expose no secret values. One audit key has only one reserved or running audit across concurrent pool processes.

## Files

1. `scripts/orchestrator/audit-pool.sh [--once|--loop] [--max 2] [--queue <dir>]` remains Bash with English shdoc documentation. The default queue is `.orchestration/validation/audit-queue/`. Requests are `<task>-<sha7>.request` files containing `key=value` lines for `pr`, `head`, `base`, `task` and optional `previous_head`. Request values are validated before they form command arguments or output paths.

   An exclusive `fcntl.flock` on `<queue>/.lock` serializes selection and slot reservation across pool processes. This retains the portable implementation because macOS has no `flock` command. `--max` is a positive single-digit slot count and defaults to 2.

   Every slot uses its own `.claude/worktrees/orchestrator-audit-<n>` worktree, created detached at `origin/main` when missing and selected through `ORCH_REVIEW_WORKTREE`. Slot 1 also uses this pool-specific naming. Neither the integration worktree nor another active slot is reused.

   Each request runs `scripts/orchestrator/orch-audit.sh <task> --head <head> <pr> --json .orchestration/validation/<task>-audit-<sha7>.json`. Differential arguments are `--previous-head <sha> --previous-findings .orchestration/validation/<task>-audit-<prev7>.json`.

   Differential execution remains disabled until `.orchestration/validation/audit-shadow.tsv` contains two comparisons with zero finding difference. Before then, a request with `previous_head` receives a full audit and a differential prompt beside its output at `<out>.differential-prompt.txt`. The prompt names the previous findings and previous-to-current diff.

   A zero audit exit and output passing `orch-audit.sh --validate .schemas/audit.json <out>` retain the JSON and rename the request to `.done`. Other outcomes remove unusable JSON, write a masked reason to `<request>.rejected` and rename the request to `.blocked`.

   A failed Codex run reporting 429 is retried after 60, 120 and 240 seconds, then blocked. Queue logs and rejection records contain the retry marker and masked diagnostics without copying an unmasked transcript. Running files left by a killed pool retain their slots and audit-key reservations until explicit cleanup. `--once` names held slots when requests wait. `--loop` repeats every 30 seconds until `<queue>/.stop` exists.

2. The request-name and slot fixes from revise 1 remain enforced. Under the queue lock, malformed basenames are blocked unread and receive a rejection reason. Only the anchored `<task-id>-<sha7>.request` form reaches request processing. Decoded slots are validated as positive single-digit integers before use, and filename text never enters Bash arithmetic.

   `test_pool_rejects_a_malformed_request_name_and_never_evaluates_it` retains its command-substitution-shaped filename, absence of its marker, absence of a Codex call, blocked result and rejection reason. `test_pool_slots_never_use_the_integration_worktree` retains the assertion that slot 1 invokes Codex in `orchestrator-audit-1`. Historical red results remain identified by their original heads and both tests run green on this task's final implementation.

3. `scripts/orchestrator/orch-audit.sh` accepts `--head <sha40>` in place of the existing `<pr-worktree>` positional and requires that head to exist as a commit in the checkout. `ORCH_REVIEW_WORKTREE` selects the review slot and otherwise retains the current default.

   `--json <out>` asks for one fenced JSON audit block immediately before the final `Verdict:` line. The final verdict remains the last non-blank line for the existing integration gate. The record contains `head`, `task_id`, `auditor`, `generated_at`, `verdict` and findings with `id`, `priority`, `confidence`, `file`, `line`, `class`, `scope`, `rationale` and `status`.

   Extraction validates the block against `.schemas/audit.json` and binds its head, task and verdict to this audit and its final verdict line. Missing or invalid JSON produces exit 3 and leaves no usable stale JSON. `--validate <schema> <json>` runs the same stdlib checker without launching an audit. It enforces required keys, types, enums, bounds, SHA patterns, additional-property restrictions and date-time format.

   `generated_at` is a valid RFC 3339 date-time with `Z` or an explicit offset. Date-only values, naive timestamps and invalid calendar dates fail. `test_orch_audit_json_mode_rejects_a_generated_at_without_an_offset` retains its positive offset and negative controls.

   Every existing refusal remains. The checkout cannot be at the audited head, the validator is tracked and unchanged, the sweep has no gaps and the ledger check passes. The tracked ledger-check override retains its existing constraints. Only a zero Codex exit with a fresh, non-empty final message supplies evidence. Failed transcripts expose only the 429 retry marker. Review-worktree cleanup also removes copied schema data.

   Masking remains mandatory after the successful audit exit. The extracted document receives the existing JSON-aware masking and schema revalidation before becoming usable. Masker failure removes unusable JSON and produces refusal even when cleanup itself fails. `test_orch_audit_json_mode_masks_the_extracted_document_before_retaining_it` retains its Unicode-escaped token fixture and assertion that the decoded token does not remain in the retained document.

4. `.schemas/classes.yaml` contains one entry per controlled class in the form `<slug>: {remedy: <sentence>, blast_radius: [<globs>]}`. It retains every ledger class in the acceptance records and includes `unbound-evidence`, `fail-open-on-error`, `argv-text-mismatch`, `json-interpolation`, `string-form-comparison`, `ps-output-parsing`, `records-form` and `advisory-p2`. The validation file includes the seeding command and its output.

   The audit JSON contract belongs to the verdict sibling and retains its b8998de class enum. This task introduces no tracked JSON schema. The pool tests embed that pinned audit-schema contract as fixture data inside the allowed test module and write it only into temporary repositories. The report identifies the contract's source SHA.

   `test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class` compares the vocabulary with the pinned contract, exercises unknown-class rejection and also checks the checkout's audit schema when it is present. The standalone sibling tests require neither an unmerged sibling worktree nor a Git object fetched during CI. Runtime audit processing still requires the real schema and refuses its absence rather than skipping validation.

5. The b8998de differential-audit P1 is fixed. `--previous-head <sha> --previous-findings <json>` binds the previous document to this task and previous head and supplies `git diff <prev>..<head>` to the auditor. The auditor verifies every previous finding's `fixed` or `still-open` status against that diff and records the supporting explanation within the existing finding record. New findings concern the new hunks.

   Before retaining a differential result, extraction verifies that every previous finding appears exactly once with its original identity and an explicit `fixed` or `still-open` status. Omitted findings, duplicate accounting, invalid statuses, mismatched previous task or head, unreadable previous evidence and unreadable diffs refuse the result with exit 3 and leave no usable JSON. A schema-valid empty findings array cannot erase an earlier finding. An unchanged finding outside the new hunks remains explicitly accounted for as still-open. A fixed claim requires support from the diff rather than a status label alone.

   `test_orch_audit_differential_result_verifies_every_previous_finding_against_the_diff` is written first. Its previous audit contains a P1 outside the new hunks and its otherwise valid current response omits that finding. The inherited implementation retains the empty result, giving the red result against `b8998de162afc72d53d07679b8f0a194fcc480ff`. The corrected implementation refuses it and removes stale output. Subcases reject a missing status and a fixed claim unsupported by the diff. Positive controls carry the unchanged finding as still-open and account for a genuinely fixed finding with diff support. The fixture proves that the previous findings and the actual diff reach the differential audit.

6. The b8998de decoded-diagnostic P2 is fixed. Decoded values are masked before schema errors are constructed or printed. Raw decoded enum values, object keys and exception details containing secrets do not reach stdout, stderr, pool logs or rejection records. Both `--json` extraction and standalone `--validate` obey this boundary. Masker failure produces refusal without an unmasked diagnostic fallback.

   `test_orch_audit_masks_decoded_values_before_printing_schema_errors` is written first. Its invalid enum contains a Unicode-escaped fake token that the Markdown masker does not recognize before decoding. The inherited checker prints the decoded token, giving the red result against `b8998de162afc72d53d07679b8f0a194fcc480ff`. The corrected implementation rejects the schema-invalid record while omitting the token from stdout, stderr, the pool log and the rejection record, and leaves no usable JSON. Standalone validation and a valid masked-document control retain their expected results.

7. The b8998de duplicate-reservation P2 is fixed. Selection refuses an audit key already reserved or running while holding the same exclusive queue lock used for slot reservation. The key is the validated task and full head, with the request basename bound to those values. A reserved `.running-<slot>` marker covers the interval before the child starts as well as its execution.

   A duplicate becomes blocked with a masked reason without taking another slot, replacing the original running marker or modifying the original audit's outputs. Another distinct key can use a free slot. Killed-pool markers continue to reserve their keys until explicit cleanup.

   `test_pool_refuses_an_audit_key_already_reserved_or_running_under_the_lock` is written first. A barrier holds the first fake audit active while the same task and head are enqueued again and a concurrent pool process selects work. The inherited implementation reserves the second slot for that key, giving the red result against `b8998de162afc72d53d07679b8f0a194fcc480ff`. The corrected implementation starts exactly one audit for the key, blocks the duplicate and preserves the original result. A distinct-key control still uses the other slot. The test also covers a reservation whose child has not started.

8. `tests/unit/test_audit_pool.py` retains every existing behavior case and these test names:

   `test_pool_saves_only_schema_valid_audit_json_and_blocks_a_rejected_request`, `test_pool_runs_at_most_max_audits_and_the_third_request_waits`, `test_pool_retries_a_429_three_times_then_blocks`, `test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree`, `test_orch_audit_json_mode_extracts_the_final_json_block_and_keeps_every_refusal`, `test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class`, `test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius` and `test_orch_audit_json_mode_rejects_a_generated_at_without_an_offset` remain present.

   `test_pool_rejects_a_malformed_request_name_and_never_evaluates_it`, `test_pool_slots_never_use_the_integration_worktree` and `test_orch_audit_json_mode_masks_the_extracted_document_before_retaining_it` remain present.

   Refusal cases retain changed and untracked validators, ledger-check failure, masker failure, head refusal, unavailable commits, sweep gaps, missing JSON, unknown classes and mismatched audit identity or verdict. Fixtures use temporary repositories, pool-specific worktrees, fake Codex and fake sleep. The extracted-document test uses the real masker. Refactoring retains every behavior case and assertion, and all fixture data counts against the test cap.

## Out of scope

The verdict sibling owns `verdict.sh`, `.schemas/verdict.json`, `.schemas/audit.json` and `test_verdict.py`. `dispatch.sh`, the record generator, gate and validator changes, Makefile targets, CI changes, `integrate-seat.sh`, `dispositions.py`, `hold-playbook.sh` and programs item (16)'s `--second-opinion` remain outside this task. The three b8998de findings assigned above are fixed here rather than assigned to an advisory owner.

## Check

The validation file contains commands, verbatim output, exit statuses and tested heads for all three re-run premises, the source cherry-pick inventory, `make unit-test`, `make render-check`, `make format`, `shellcheck scripts/orchestrator/audit-pool.sh scripts/orchestrator/orch-audit.sh`, `shfmt -i 4 -sr -d scripts/orchestrator/audit-pool.sh scripts/orchestrator/orch-audit.sh` and `uv run python -m unittest tests.unit.test_audit_pool -v`. The script checks are clean and the pool module is green.

Each new regression has its own red result against `b8998de162afc72d53d07679b8f0a194fcc480ff` and green result after the fix. Split fixtures provide the pinned schema contract before those red runs so missing sibling files cannot cause an unrelated failure. Retained tests run again on the final implementation. Historical a02 red results retain their original heads and do not substitute for this task's validation.

`git diff --numstat origin/main...HEAD` shows at most 300 changed lines outside `tests/`, `.orchestration/` and `.schemas/`, and 400 under `tests/`. Changed lines are additions plus deletions over the complete PR diff. `.schemas/classes.yaml` is data and its line count is reported separately. Meeting a cap removes no required behavior, validation, regression case or trust-boundary control.

An inherited check failure is reproduced against the unchanged base with the same command and environment and reported as a failure with that evidence. It is never labelled passing or repaired outside `allowed_files`. Local Bats tests remain unrun and GitHub Actions supplies their required results.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task-copy byte comparison and SHA256 cover this task's text. The cumulative changed-file inventory contains only this task's allowed files.

## Completion

One fresh branch, `tools/audit-pool-a01`, starts from `origin/main` and carries one new PR with an English title and description. The worker lists the cherry-picked source SHAs and resulting commits in `.orchestration/dotfiles-T133-audit-pool-a01/report.md`. Its PR receives its own reviews, task-level audit, security review and acceptance record. Neither sibling's review evidence substitutes for the other's.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with the live rules below, `dotfiles-T133-audit-pool-followup-a01` as the owner of advisory P2, `task_copy=<sha256 of .orchestration/dotfiles-T133-audit-pool-a01/task.md>` and `parked_pr=407` in the RESULT. The orchestrator writes the owner task before assigning an advisory disposition. PR #407 stays parked and no parking operation is repeated. The three b8998de findings in items 5 to 7 belong to this task.

There is at most one worker-side pre-push review round. Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. This task starts a new lineage and does not rewrite the stopped combined task's history. A surviving P0/P1 stops the PR for the operator's decision under the inherited Completion rule.

The report and RESULT identify the new PR, head, base, branch, changed files, cherry-picked SHAs, every feedback disposition, test names, code and test totals, separate vocabulary-data count, task-copy hash and evidence paths. They distinguish inherited behavior, the three fixes, historical evidence and final-head results. A Codex seat writes evidence at the same relative paths in its own worktree and states that placement in the RESULT. Worker review evidence uses the required `-worker-` infix and the orchestrator copies worktree evidence by absolute path before review.

This task is `security: true`. The orchestrator runs its own final-head task-level audit and separate security-profile review before the gate. Final-head CI, the feedback sweep, finding dispositions, acceptance record, integration gate and merge follow Orchestrator Playbook step 10 in its prescribed order. Changed heads receive fresh required evidence. The orchestrator merges with `gh pr merge --squash --match-head-commit <audited head>` after the gate.

No `@codex review` comment is posted. Automatic review is observed for the bounded window and absence after 15 minutes is recorded as `bot: none`. Commands matching a live ask rule are not issued and no API or browser path bypasses that rule. Each `gh` command, Git write and `git fetch` runs individually without shell chaining or a wrapper combining commands. Refused commands retain their command, exit status and output while independent authorized work continues.

Until plan 024 P1-14 lands, every string containing the words `gh pr merge` or `gh pr create` is written with the file-edit tool. Shell commands, heredocs and shell wrappers do not write those strings. This writing rule supplies no authorization to execute a command refused by the live permission boundary.

Live audit-service calls and local Bats are not exercised. Runtime JSON audits require the real audit schema, and killed-pool reservations remain held until explicit cleanup.

## Checks

```
dotfiles-T133-audit-pool-a01.md: OK
premises: three, re-run by the worker at start (the a02 branch holds the files; audit-pool.sh and classes.yaml absent on main; orch-audit.sh tracked)
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-audit-pool-a01.md
```
