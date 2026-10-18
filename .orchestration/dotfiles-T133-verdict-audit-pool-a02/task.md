---
format: 2
task_id: dotfiles-T133-verdict-audit-pool-a02
kind: code
security: true
allowed_files:
  - scripts/orchestrator/verdict.sh
  - scripts/orchestrator/audit-pool.sh
  - scripts/orchestrator/orch-audit.sh
  - .schemas/audit.json
  - .schemas/verdict.json
  - .schemas/classes.yaml
  - tests/unit/test_verdict.py
  - tests/unit/test_audit_pool.py
  - .orchestration/dotfiles-T133-verdict-audit-pool-a02/**
after: []
reset_of: [dotfiles-T133-verdict-audit-pool-a01]
threat_table:
  - control: "scripts/orchestrator/verdict.sh (the nine conditions, trusted execution context, complete feedback matching, disposition validation, shadow gate and accept-only application)"
    disposition: "residual: the retained tests and the six regression tests in items 6 to 11 exercise the decision and application boundaries; the final-head task-level audit and security review assess their combined coverage."
  - control: "scripts/orchestrator/audit-pool.sh (the exclusively locked queue, bounded concurrency, isolated review slots, schema validation, differential gate and bounded 429 retries)"
    disposition: "residual: the pool tests exercise the queue and subprocess outcomes in temporary repositories; killed-pool running files retain their slots until explicit cleanup and are reported when requests wait."
  - control: "scripts/orchestrator/orch-audit.sh (head selection, JSON extraction, schema validation, differential inputs, review-worktree selection, existing refusals and masking)"
    disposition: "residual: the retained JSON-mode test exercises every existing refusal, and the offset regression exercises date-time validation; the final-head audit checks that no refusal or masking step was removed."
  - control: ".schemas/audit.json (the audit record, controlled class enum and JSON Schema 2020-12 constraints)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class"
  - control: ".schemas/verdict.json (the accept, revise and hold record)"
    disposition: "closed: tests/unit/test_verdict.py::test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold"
  - control: ".schemas/classes.yaml (the controlled finding classes, remedy sentences and blast_radius globs)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius"
  - control: "tests/unit/test_verdict.py (the retained verdict fixtures and the six red-then-green regressions)"
    disposition: "residual: temporary repositories and fake external tools record arguments and effects; each regression keeps unrelated conditions green and refreshes evidence hashes so its result demonstrates the named defect."
  - control: "tests/unit/test_audit_pool.py (the pool, schema, timestamp and audit-refusal fixtures)"
    disposition: "residual: fake codex and sleep exercise concurrency and retry behavior without live audits or retry delays; temporary review worktrees isolate fixture mutations."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a02/** (this reset task's branch artifacts)"
    disposition: "residual: artifacts stay within this task's directory, distinguish historical results from final-head results, and carry command, exit-status and head provenance for acceptance."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-verdict-audit-pool-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-verdict-audit-pool-a01/task.md)"
    disposition: "residual: the a02 copy is byte-identical to the dispatched text and its own SHA256 appears in the TASK and RESULT; the orchestrator verifies replacement and byte identity before acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-verdict-audit-pool-a02/ (report.md, validation.md, sandbox.md, learning.md and revise.yaml)"
    disposition: "residual: records preserve the provenance of inherited a01 evidence, report the six new regression results separately, and disclose refused commands, remaining limits and the final changed-file inventory."
  - control: task metadata
    disposition: "residual: the orchestrator checks the dispatched front matter with task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; byte identity covers subsequent metadata changes."
  - control: metadata separators
    disposition: "residual: the first document separators bound the YAML front matter and the dispatched-file byte comparison covers the complete task copy."
  - control: in-process effects
    disposition: "residual: normal verdict evaluation writes validation artifacts and temporary files; application sends through dispatch.sh and merges through gh only after accept, the shadow gate and the integration procedure."
  - control: workflow and interpreter or environment inputs
    disposition: "closed: tests/unit/test_verdict.py::test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout"
  - control: new or renamed scripts
    disposition: "residual: the two new orchestrator scripts and three schema data files are the declared additions; no additional executable script or renamed helper is introduced, and the final inventory is checked against allowed_files."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges only with gh pr merge --squash --match-head-commit <audited head> after the integration gate; this PR is integrated manually and supplies no authorization to exercise live --apply."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch changes the head, so CI, the feedback sweep, task-level audit and security review bind the resulting final head before the gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records the discarded uncommitted state in the acceptance record."
premises:
  - claim: orch-audit.sh takes the audited head from a PR worktree positional today, so item 3 adds --head as the alternative the pool needs
    command: "/usr/bin/grep -c 'usage: orch-audit.sh <task> <pr-worktree> <pr>' scripts/orchestrator/orch-audit.sh"
    output: |-
      1
  - claim: pr-feedback.py writes its document with --json <out>, the form verdict.sh calls for the final head's sweep
    command: uv run --no-project python scripts/pr-feedback.py --help | /usr/bin/grep -c -- '--json JSON'
    output: |-
      2
  - claim: regime-counters.sh has the --history-only mode verdict.sh reads for condition 6
    command: /usr/bin/grep -c -- '--history-only) history_only=true' scripts/regime-counters.sh
    output: |-
      1
  - claim: none of the new files exists on origin/main
    command: git ls-files .schemas scripts/orchestrator/verdict.sh scripts/orchestrator/audit-pool.sh | wc -l
    output: |-
      0
---

# AGMSG-TASK dotfiles-T133-verdict-audit-pool-a02 — INV-6 reset of dotfiles-T133-verdict-audit-pool-a01 (PR #410; plan 024 P1-4a)

This text is the independent redesign by a review-profile context other than the author of a01. The orchestrator's local review of revise-1 head `85a472294d0c10835bd7235e3c76d045846a6ed9` found two P1 and four P2 in `scripts/orchestrator/verdict.sh`. The operator's directive of 2026-10-18 forbids a third round. Another a01 revise would reach two revises under plan 006 INV-6 S2, so a01 remains stopped and this task returns the work to design.

PR #410 continues under this task on the same branch, `tools/verdict-audit-pool-a01`, starting from `85a472294d0c10835bd7235e3c76d045846a6ed9`. The next push replaces `.orchestration/dotfiles-T133-verdict-audit-pool-a01/task.md` with this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-verdict-audit-pool-a02/task.md`. The orchestrator handles predecessor-copy removal and relocation of inherited branch evidence as reset bookkeeping. Worker edits remain within `allowed_files`, and the final cumulative changed-file inventory remains within that boundary. Historical evidence retains its original task identifiers and tested heads. The a01 acceptance history and counters remain unchanged.

The a01 item 0 is complete. PR C stage 1 is parked as draft PR #407 at `dfa9001b858431751faeab3b779b71eb0da01c2f`. This task repeats no parking, branch creation or PR creation.

The four premises preserve a01's write-time observations verbatim. The implementation and validation requirements below incorporate amendment 1, the retained worker fixes, the revise-1 fixes and all six findings of the local review. The design remains `.orchestration/plans/024-design-programs.md` items (1), (2) and (3), with the nine verdict conditions in `.orchestration/plans/024-design-mechanism.md`. The class vocabulary remains at `.schemas/classes.yaml` because checker C2 excludes another task directory from `allowed_files`.

## Goal

The orchestrator's acceptance of a PR becomes one script's nine positively checked conditions with a schema-valid JSON verdict. Audits run from a queue two at a time with structured findings whose classes come from one controlled vocabulary.

PR-controlled interpreter selectors, empty finding identifiers, stale feedback documents, null feedback URLs, shared feedback URLs and invalid dispositions cannot produce acceptance. The six local-review findings are fixed in this reset.

## Files

1. `scripts/orchestrator/verdict.sh <pr> [--apply] [--loop] [--shadow]` is Bash with `set -Eeuo pipefail`, English shdoc documentation and `jq` for JSON. Python checks run under the pinned execution context of item 6, with isolated Python and offline dependency resolution. Every condition is `{id, ok, evidence}` and becomes true only from a positive check of parsed, validated input.

   The inputs are `gh pr view <pr> --json headRefOid,isDraft,baseRefName,state,number`, `gh pr checks <pr> --json name,state`, the acceptance record whose JSON block `pr` equals `<pr>` and its `head`, the task selected by that record or `--task <id>`, the record's prose `precheck: <sha256>`, `.orchestration/validation/<task>-audit-<sha7>.json`, a fresh `scripts/pr-feedback.py <pr> --json <mktemp>` sweep, `.orchestration/validation/<task>-pr-feedback.json` for saved dispositions, `.orchestration/tasks/<task>.md` for `allowed_files`, `security` and Check caps, the regime counters, the merge-base diff and numstat, and the head-specific security review when required. The acceptance record names this task, PR and current head and contains a ledger array. The PR is open, non-draft and based on `main`. A missing head is fetched from `pull/<pr>/head` and must resolve locally before evaluation continues.

   Condition 1 verifies that `git show <head>:.orchestration/<task>/precheck.json` hashes to the record's `precheck:` value and names `<head>` or an ancestor whose diff to `<head>` contains only `.orchestration/<task>/` paths. An unset or zero `PRECHECK_REQUIRED` makes failure of this condition a warning.

   Condition 2 requires every one of the seven required checks named below to be present with state `SUCCESS` for the head. Empty or unreadable checks hold. Multiple entries for a required name all have to be `SUCCESS`.

   Condition 3 requires an audit that validates against `.schemas/audit.json`, names this task and head, contains zero open P0/P1 findings as counted in item 7, and has verdict `correct` or a non-empty set of remaining findings whose scopes are all `records`. A blocked audit holds. An incorrect audit with no remaining findings does not pass through an empty records-only comparison.

   Condition 4 requires the saved document and fresh sweep to name the accepted head, complete feedback identity matching with multiplicity, and a valid disposition for every fresh item. Items 8 to 11 define these checks. Diagnostic URLs never determine whether this condition passes.

   Condition 5 requires every path in `git diff --name-only <base> <head>` to match an `allowed_files` entry and the additions-plus-deletions totals from `git diff --numstat --no-renames <base> <head>` to remain within the Check caps. The base is `git merge-base origin/main <head>`. Failure to resolve the base or read the diff holds. The cap parser recognizes `at most <n> changed lines outside` and `<n> under tests/`, including backticked paths. Every backticked exclusion named after `outside` in the Check sentence leaves the outside count. The default exclusions are `tests/` and `.orchestration/`.

   Condition 6 reads `scripts/regime-counters.sh <task> --pr <pr>` so the S1 check has its ledger source. It requires no `S1:` line and a parsed `revises` value below 2. A missing ledger, failed counters command or unreadable count holds.

   Condition 7 requires the numeric count of open P0/P1 audit findings to be zero, as item 7 defines.

   Condition 8 requires `.orchestration/validation/<task>-security-<sha7>.md.last.md` to end with the last non-blank line `Verdict: correct` when the task's `security` is true. Unreadable task front matter cannot select the non-security path.

   Condition 9 requires at least one `sha256:<hex> <path>` line in the acceptance record's prose and verifies every such line against its file.

   The verdict is `accept` when all nine conditions pass. It is `hold` when condition 6 or 7 fails, an input is missing, unreadable or schema-invalid, or evaluation encounters an internal error. Other failed conditions produce `revise`. The revise line is `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise previous_head=<head> reason=<failed ids> next_action=<the first failed condition's evidence, shell-safe>`. The orchestrator supplies the `check=` selectors.

   The output is `.orchestration/validation/<task>-verdict-<sha7>.json`, validated against `.schemas/verdict.json`, with `verdict`, `pr`, `head`, `task_id`, `conditions[]`, `inputs_sha256{}`, `generated_at` and optional `revise_line`. Exit codes remain 0 for accept, 10 for revise, 20 for hold and 2 for usage or internal error, with internal error treated as hold. A refusal before a usable task or head exists reports hold without inventing an output identity.

   `--apply` requires the trusted execution context of item 6, tracked scripts, schemas and task files equal to `origin/main`, and no untracked executable helper substituted in those code directories. It remains disabled until the last four rows of `.orchestration/validation/verdict-shadow.tsv` agree between machine and human and represent four distinct PRs. Four rows for one PR do not unlock application. After accept only, it writes `AGMSG-ACCEPTANCE v1 task_id=<task> status=accepted reason=verdict-<sha7> next_action=merge` to a temporary file, sends it through `scripts/orchestrator/dispatch.sh <team> <from> <to> <pane> <file> <record>`, then invokes `gh pr merge <pr> --squash --match-head-commit <head>`. The team, sender, recipient and placement come from `--team`, `--from`, `--to` and `--pane`. Arguments containing `--admin` or `--auto` anywhere are refused at parse time with exit 2 before any read or tool invocation.

   `--shadow` writes the verdict JSON and appends `<pr>\t<head>\t<verdict>\t\t\t<generated_at>` to `.orchestration/validation/verdict-shadow.tsv`, whose columns are `pr`, `head`, `machine`, `human`, `agree` and `at`. The orchestrator supplies the human and agreement columns. Shadow mode sends nothing and merges nothing.

   `--loop` processes open, non-draft PRs on `main` in PR-number order when an acceptance record exists and its head equals the PR's current head. It fetches origin between PRs and retains the same pinned execution context.

2. `scripts/orchestrator/audit-pool.sh [--once|--loop] [--max 2] [--queue <dir>]` is Bash with English shdoc documentation. Its default queue is `.orchestration/validation/audit-queue/`. Requests are `<task>-<sha7>.request` files containing `key=value` lines for `pr`, `head`, `base`, `task` and optional `previous_head`. The request values are validated before they form command arguments or output paths.

   An exclusive `fcntl.flock` on `<queue>/.lock` serializes selection and slot reservation. This retains the portable implementation because macOS has no `flock` command. At most `--max` audits run concurrently. Slot 1 uses `.claude/worktrees/orchestrator-review`; slot 2 uses `.claude/worktrees/orchestrator-review-2`, created detached at `origin/main` when missing. Each slot is passed through `ORCH_REVIEW_WORKTREE`.

   Each request runs `scripts/orchestrator/orch-audit.sh <task> --head <head> <pr> --json .orchestration/validation/<task>-audit-<sha7>.json`. Differential arguments are `--previous-head <sha> --previous-findings .orchestration/validation/<task>-audit-<prev7>.json`. Differential execution stays disabled until `.orchestration/validation/audit-shadow.tsv` contains two comparisons with zero finding difference. Before then, a request with `previous_head` receives a full audit and a differential prompt beside its output at `<out>.differential-prompt.txt`.

   A zero exit and output passing `orch-audit.sh --validate .schemas/audit.json <out>` retain the JSON and rename the request to `.done`. Every other outcome removes unusable JSON, writes a reason to `<request>.rejected` and renames the request to `.blocked`. A failed Codex run reporting 429 is retried after 60, 120 and 240 seconds, then blocked. Queue logs and rejection files contain the retry marker and masked diagnostics without copying an unmasked transcript. Running files left by a killed pool retain their slots until explicit cleanup, and `--once` names held slots when requests wait. `--loop` repeats every 30 seconds until `<queue>/.stop` exists.

3. `scripts/orchestrator/orch-audit.sh` accepts `--head <sha40>` in place of the existing `<pr-worktree>` positional. The supplied head exists as a commit in this checkout. `ORCH_REVIEW_WORKTREE` selects the review slot and otherwise retains the current default.

   `--json <out>` asks for one fenced JSON block describing `.schemas/audit.json` immediately before the final `Verdict:` line. The final verdict remains the last non-blank line because the existing integration gate reads that line. The record contains `head`, `task_id`, `auditor`, `generated_at`, `verdict` and findings with `id`, `priority`, `confidence`, `file`, `line`, `class`, `scope`, `rationale` and `status`. The extractor checks the block against the schema and checks its head, task and verdict against this audit and its final verdict line. A missing or invalid block produces exit 3 and leaves no usable stale JSON.

   `--validate <schema> <json>` runs the same stdlib checker without launching an audit. The checker enforces the schemas' required keys, types, enums, bounds, SHA pattern, additional-property restrictions and date-time format. `generated_at` is a valid RFC 3339 date-time with `Z` or an explicit offset. Date-only values, naive timestamps and invalid calendar dates fail. This retains the revise-1 fix and its regression test.

   `--previous-head <sha> --previous-findings <json>` gives the auditor the previous findings and `git diff <prev>..<head>`, asks for each previous finding's `fixed` or `still-open` status, and asks for new findings on the new hunks. The pool controls when differential execution becomes enabled.

   Every existing refusal remains: this checkout cannot be at the audited head, the validator must be tracked and unchanged, the sweep cannot have gaps, and the ledger check must pass. The tracked ledger-check override retains its existing constraints. Only a zero Codex exit with a fresh, non-empty final message supplies audit evidence. Masking remains mandatory after that exit, and masker failure makes the audit unusable. Review-worktree cleanup also removes copied schema data. A failed transcript exposes only the 429 retry marker.

4. `.schemas/audit.json` and `.schemas/verdict.json` remain JSON Schema 2020-12 documents with `additionalProperties: false` at the top level and in the defined item objects. Their fields follow plan 024 programs item (3) and the verdict output in item 1. The audit finding class enum is generated from `.schemas/classes.yaml`, and a test keeps them equal.

   `.schemas/classes.yaml` has one entry per class in the form `<slug>: {remedy: <sentence>, blast_radius: [<globs>]}`. It contains every ledger class in the acceptance records plus `unbound-evidence`, `fail-open-on-error`, `argv-text-mismatch`, `json-interpolation`, `string-form-comparison`, `ps-output-parsing`, `records-form` and `advisory-p2`. The validation file contains the seeding command and its output. The three `.schemas/` files are data outside the 500-line code cap, and their line counts are reported separately.

5. `tests/unit/test_verdict.py` retains `test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds`, `test_verdict_holds_on_a_missing_or_schema_failing_input`, `test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto`, `test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold`, `test_verdict_condition_1_is_a_warning_under_precheck_required_0`, `test_verdict_shadow_appends_the_machine_column_only` and `test_verdict_reads_the_record_front_matter_offline_and_holds_when_pyyaml_is_unavailable`.

   The green fixture accepts. Variants breaking conditions 1 to 5, 8 and 9 revise, while failures of conditions 6 and 7 hold. The JSON identifies each failed condition. Retained cases cover an empty checks response, duplicate required-check entries with a failure, a blocked audit, an incorrect audit without findings, a missing ledger, a missing record, an unavailable head, a failed merge-base read, cap parsing with backticks, absent evidence hashes and a checkout at the PR's code commit. Apply tests record arguments and prove that revise and hold never dispatch or merge. They retain refusal of forbidden flags before fake tools run, refusal before four distinct agreeing PRs, and dispatch-before-merge ordering with `--match-head-commit`.

   The task front matter is read offline only. A cached PyYAML environment permits the green path. An unavailable offline PyYAML environment produces hold with exit 20, and no online fallback runs. This retains the revise-1 fix while item 6 pins the environment and interpreter used for that read.

   `tests/unit/test_audit_pool.py` retains `test_pool_saves_only_schema_valid_audit_json_and_blocks_a_rejected_request`, `test_pool_runs_at_most_max_audits_and_the_third_request_waits`, `test_pool_retries_a_429_three_times_then_blocks`, `test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree`, `test_orch_audit_json_mode_extracts_the_final_json_block_and_keeps_every_refusal`, `test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class`, `test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius` and `test_orch_audit_json_mode_rejects_a_generated_at_without_an_offset`. The refusal test exercises the validator's changed and untracked states, the ledger-check failure and masker failure as well as the existing head and sweep refusals.

   Fixtures use temporary repositories and fake external tools. They include valid head metadata and complete feedback identities for the stronger checks. Fixture lines count against the test cap. Refactoring to meet the caps retains every existing case and assertion of behavior.

6. The interpreter-selection P1 is fixed in `scripts/orchestrator/verdict.sh`. The script resolves `uv`, Python, `gh`, `git` and `jq` to absolute executables in the trusted root before it reads any PR checkout. It uses the private PATH of links established by `scripts/orchestrator/orch-gate.sh`, with shim refusal and trusted-root resolution. Required shell utilities are resolved there as well. The execution environment is explicitly constructed, and a PR checkout or inherited tool-selection environment cannot participate in interpreter discovery.

   Python runs through a pinned absolute interpreter with isolation. Any required offline PyYAML environment is resolved and pinned in the trusted root before PR input processing. Subsequent `uv` calls and helper subprocesses retain that interpreter and explicit environment. A checkout's `.python-version`, `.venv`, executable files, uv configuration or mise configuration cannot select another interpreter or tool. The schema check, feedback collector and task-front-matter read obey the same boundary. Missing trusted tools or an unavailable offline dependency environment hold before dispatch or merge.

   `tests/unit/test_verdict.py::test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout` is written first. Its fixture reproduces the old tracked-code guard passing while a checkout contains a `.python-version` naming a marker-writing fake Python outside the guarded code directories. It also covers checkout-local environment and executable selection. The fake delegates as needed so the old path reaches the interpreter-selection defect rather than failing on an unrelated fixture. The test proves that ordinary pinned-tool evaluation still works and that the planted executable never writes its marker. It is red against `85a472294d0c10835bd7235e3c76d045846a6ed9` and green after the fix.

7. The open-finding P1 is fixed in conditions 3 and 7. Both use the numeric count of P0/P1 findings whose status is `new`, `still-open` or absent. Missing status retains the existing `new` default. The count is independent of diagnostic identifiers. Empty identifiers cannot make an open finding disappear, and records scope cannot exempt an open P0/P1 finding. Condition 3 includes the zero-count requirement alongside its audit-verdict and scope checks. Condition 7 fails when the count is nonzero, producing hold.

   `tests/unit/test_verdict.py::test_verdict_counts_open_p0_p1_findings_even_when_the_id_is_empty` is written first. An otherwise green fixture has an incorrect audit with one unfixed records-scope P1 whose `id` is empty. The record's audit hash is refreshed. The old implementation accepts, and the corrected implementation fails conditions 3 and 7 and holds. Subcases retain the same result for P0 and `still-open`, while a fixed finding does not count as open. The test is red against `85a472294d0c10835bd7235e3c76d045846a6ed9` and green after the fix.

8. The feedback-head P2 is fixed in condition 4. The saved feedback document's `head_sha` and the fresh sweep's `head_sha` both equal the head being accepted. A missing or unequal head fails condition 4 even when item URLs and dispositions remain identical.

   `tests/unit/test_verdict.py::test_verdict_condition_4_requires_saved_and_fresh_heads_to_equal_the_accepted_head` is written first. Its green control binds both documents to the accepted head. Separate subcases change only the saved head, only the fresh head, and remove each head field. Each rejects acceptance and identifies condition 4. The stale-head cases are red against `85a472294d0c10835bd7235e3c76d045846a6ed9` and green after the fix.

9. The null-URL P2 is fixed in condition 4. Undispositioned or invalidly dispositioned items are counted before their diagnostic URLs are formatted. A null or empty URL changes only the diagnostic text.

   `tests/unit/test_verdict.py::test_verdict_condition_4_rejects_an_undispositioned_status_with_a_null_url` is written first. An otherwise green fresh sweep and saved document contain a commit status whose `target_url` yields a null item URL and whose disposition is absent. Condition 4 fails and acceptance is refused. A valid disposition for that same identity supplies the green control. The regression is red against `85a472294d0c10835bd7235e3c76d045846a6ed9` and green after the fix.

10. The shared-URL P2 is fixed in condition 4. Feedback matching uses complete item identity and preserves multiplicity through the existing `feedback_key()` and `missing_feedback()` behavior in the trusted root's `scripts/require-crit-review.py`. Source, URL, level, path, line, body and author participate in identity, with only the existing exact masked-body and masked-path equivalence accepted. Each saved item covers at most one fresh item. A URL-indexed map cannot collapse annotations or reuse one disposition for several items.

    `tests/unit/test_verdict.py::test_verdict_condition_4_preserves_complete_item_identity_and_multiplicity` is written first. Two annotations share a check-run URL but differ in their full identities. A disposition on only the last annotation leaves the first uncovered and fails condition 4. A second subcase presents duplicate fresh identities with fewer saved dispositioned occurrences and also fails. Supplying one valid saved occurrence for every fresh occurrence passes. The shared-URL regression is red against `85a472294d0c10835bd7235e3c76d045846a6ed9` and green after the fix.

11. The disposition-validation P2 is fixed in condition 4. The script reuses the existing disposition and commit validators from the trusted root's `scripts/require-crit-review.py`, including `parse_disposition()` and `commit_in_range()`, without modifying that module. A `fixed:<sha>` disposition names an existing commit inside the authenticated base-to-head range. A `not-applicable:<reason>; evidence=<command>` disposition has a non-empty reason and evidence command and satisfies the existing level-specific reason requirements. Prefix checks alone cannot approve a disposition. Evidence commands remain data and are never executed by verdict evaluation.

    `tests/unit/test_verdict.py::test_verdict_condition_4_uses_the_existing_disposition_and_commit_validators` is written first. Its negative cases include `not-applicable:; evidence=`, a whitespace-only reason, an empty evidence command, a repeated evidence delimiter, an unknown hexadecimal fix commit, a commit at or before the base and a commit outside the head's ancestry. Each fails condition 4 and refuses acceptance. A real fix commit inside base..head and a complete not-applicable disposition supply positive controls. The bypass cases are red against `85a472294d0c10835bd7235e3c76d045846a6ed9` and green after the fix.

The seven required check names from a01 are `validate`, `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)`, `test (macos-14, client)`, `public-bootstrap (ubuntu-24.04, server)`, `public-bootstrap (ubuntu-24.04, client)` and `public-bootstrap (macos-14, client)`.

## Out of scope

`dispatch.sh` (P1-5 owns it; verdict.sh is its client), the record generator (P1-6), `dispositions.py` and `--second-opinion` (P1-10), `hold-playbook.sh` (P1-13), the gate `scripts/require-crit-review.py` and `validate-agent-assets.py` (in flight in #390, #389, #396), any `make` target or CI step (the schema check runs as a unit test), `integrate-seat.sh` (P1-4).

## Check

`make unit-test`, `make render-check`, `make format`, `shellcheck` and `shfmt -d` on the three scripts clean, `uv run python -m unittest tests.unit.test_verdict tests.unit.test_audit_pool -v` green, `scripts/orchestrator/verdict.sh --shadow <this PR>` run once on your own PR with its JSON pasted (hold is the expected verdict before the audit exists), all pasted in `.orchestration/dotfiles-T133-verdict-audit-pool-a02/validation.md`, with `git diff --numstat origin/main...HEAD`: at most 500 changed lines outside `tests/`, `.orchestration/` and `.schemas/` (the three files under `.schemas/` are data in the D-cap-F2 form and leave the count; paste their line counts separately), 500 under `tests/`.

The concrete shadow invocation is `scripts/orchestrator/verdict.sh --shadow 410 --task dotfiles-T133-verdict-audit-pool-a02`. Its JSON and exit status are recorded with the tested head. This task exercises no live `--apply`.

The validation file contains commands, verbatim output, exit statuses and tested heads for all checks. Each of items 6 to 11 has its own red result against `85a472294d0c10835bd7235e3c76d045846a6ed9` and green result after its fix. The revised fixtures first establish their green controls, retain unrelated valid conditions and refresh hashes of changed evidence. Historical a01 red results retain their original references and are identified as historical. The retained tests, including both revise-1 regressions, run again on the final implementation.

Changed lines are additions plus deletions. The code and test caps apply to the complete PR diff against `origin/main`. Schema data is counted separately. Meeting a cap removes no required behavior, regression case, validation or trust-boundary control.

An inherited check failure is reproduced against the unchanged base with the same command and environment and is reported as a failure with that evidence. It is not labelled passing and is not repaired outside `allowed_files`. No local Bats tests run. GitHub Actions supplies required Bats results.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task-copy byte comparison and its SHA256 cover this a02 text.

## Completion

One branch, `tools/verdict-audit-pool-a01`, carries this reset and continues PR #410. The next push contains the replacement a02 task copy and this task's evidence. No new implementation branch or PR is created, and the completed parking step is not repeated.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written with the live no-prompt rule below, `dotfiles-T133-verdict-audit-pool-followup-a01` as the owner of any advisory P2, `task_copy=<sha256 of .orchestration/dotfiles-T133-verdict-audit-pool-a02/task.md>` and `parked_pr=407` in the RESULT. The orchestrator writes that owner task before assigning an advisory disposition. The six findings in items 6 to 11 belong to this reset and are fixed here. Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. The stopped a01 history is not rewritten to exclude earlier rounds.

The report and RESULT name the head, base, branch, changed files, every feedback disposition, test names, code and test totals, separate schema-data counts, task-copy hash and evidence paths. The report distinguishes retained behavior, the six fixes, historical evidence and final-head results. A Codex seat writes evidence at the same relative paths in its own worktree and says so in the RESULT. Worker-side review evidence uses the required `-worker-` infix. The orchestrator copies worktree evidence by absolute path before review.

This task is `security: true`. The orchestrator runs the task-level audit and a separate security-profile review on the final head before the gate. Final-head CI, the feedback sweep, finding dispositions, acceptance record, integration gate and merge follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives fresh required evidence. The orchestrator merges with `gh pr merge --squash --match-head-commit <audited head>`. The four-distinct-PR shadow requirement remains enforced in code, and this PR itself is integrated manually after the gate.

The live no-prompt rule governs the inherited Bot workflow. No `@codex review` comment is posted. Automatic review is observed for the bounded window, and absence after 15 minutes is recorded as `bot: none`. Commands matching a live ask rule are not issued, and no alternate API or browser path bypasses that rule. Each `gh` command and each Git write runs individually without shell chaining or a wrapper combining commands. `git fetch` also runs individually. A refused command is recorded with its command, exit status and output while independent authorized work continues.

Live dispatch, merge and audit-service behavior are not exercised by the fixtures, and local Bats remain unrun. A killed audit pool can leave running-slot files that block those slots until explicit cleanup.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```