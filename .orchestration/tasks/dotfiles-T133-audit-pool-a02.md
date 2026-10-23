---
format: 2
task_id: dotfiles-T133-audit-pool-a02
kind: code
security: true
allowed_files:
  - scripts/orchestrator/audit-pool.sh
  - scripts/orchestrator/orch-audit.sh
  - .schemas/classes.yaml
  - tests/unit/test_audit_pool.py
  - .orchestration/dotfiles-T133-audit-pool-a02/**
  - tests/unit/trusted_exec_contract.py
after: [dotfiles-T133-worker-write-boundary-slice4-a01]
reset_of: [dotfiles-T133-audit-pool-a01]
threat_table:
  - control: "scripts/orchestrator/audit-pool.sh (trusted execution, frozen requests, queue ownership, physical-slot locks, full-head identities, validated outputs and bounded retries)"
    disposition: "residual: tests/unit/test_audit_pool.py exercises the ten C-80 findings and concurrent subprocess outcomes; the host write boundary mitigates same-user replacement, and killed-pool reservations remain held until explicit trusted cleanup."
  - control: "scripts/orchestrator/orch-audit.sh (verified executable realpaths, pinned Git operations, frozen evidence, differential accounting, extraction and masking)"
    disposition: "residual: tests/unit/test_audit_pool.py::test_orch_audit_executes_only_the_realpaths_verified_against_origin_main and the retained differential and masking regressions exercise consumption boundaries; processes outside every seat sandbox remain a host-level residual."
  - control: ".schemas/classes.yaml (complete controlled vocabulary from JSON and prose ledgers, remedy sentences and blast_radius globs)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius"
  - control: "tests/unit/test_audit_pool.py (retained behavior cases, source-pinned schema shape, complete vocabulary fixture and red-then-green regressions)"
    disposition: "residual: temporary trusted-host fixtures and fake services exercise executable selection, filesystem identity, queue concurrency and evidence binding without live audits or retry delays."
  - control: ".orchestration/dotfiles-T133-audit-pool-a02/** (this reset task's branch artifacts)"
    disposition: "residual: artifacts identify source commits, tested heads, executable realpaths, snapshot hashes, all ten C-80 dispositions and final-head results; inherited evidence never substitutes for this task's validation."
  - control: "tests/unit/trusted_exec_contract.py (shared trusted-host contract fixture helper, created here if absent)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_audit_pool_never_executes_a_shim_first_on_path; tests/unit/test_audit_pool.py::test_audit_pool_ignores_planted_git_environment_and_config; tests/unit/test_audit_pool.py::test_audit_pool_refuses_trusted_paths_under_a_worker_root; tests/unit/test_audit_pool.py::test_audit_pool_never_consumes_a_file_swapped_after_verification"
  - control: "the task-file copies (.orchestration/dotfiles-T133-audit-pool-a02/task.md and .orchestration/dotfiles-T133-audit-pool-a01/task.md)"
    disposition: "residual: the a02 copy is byte-identical to the dispatched text and its own SHA256 is bound by TASK and RESULT; a01 never started or pushed, so the worker creates no a01 copy and deletes no predecessor material."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-audit-pool-a02/ (report.md, validation.md, sandbox.md, learning.md and revise.yaml)"
    disposition: "residual: records distinguish source history, actual red and green executions, refused commands, inherited failures, complete changed-line counts and final-head review evidence."
  - control: task metadata
    disposition: "residual: the orchestrator checks task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; dispatch also requires the exact a02 text to pass C-80."
  - control: metadata separators
    disposition: "residual: the first document separators bound the YAML front matter and byte comparison covers the complete dispatched task copy."
  - control: in-process effects
    disposition: "residual: selection consumes frozen request values under the queue and physical-slot locks; publication and cleanup require unchanged path, inode and content identities."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: sanitized startup, verified absolute executables, Python isolation and pinned Git configuration prevent inherited discovery inputs from selecting code; no workflow or seat-policy change is authorized."
  - control: new or renamed scripts
    disposition: "residual: the pool is the only new production executable, the existing audit wrapper is modified and the shared helper is test-only; the final inventory contains no undeclared production helper."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges only after the integration gate with gh pr merge --squash --match-head-commit <audited head>; no local merge or push to main is authorized."
  - control: orchestrator effect update-branch
    disposition: "residual: an updated head receives the required fresh CI, feedback sweep, task-level audit and security review before the integration gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state in acceptance."
  - control: "5.14 item 1 (write boundary, premise 6)"
    disposition: "residual: the unchanged manifest-rendered seat sandbox supplies the write boundary and make render-check supplies rendered-deny evidence before dispatch; D-024-17 owns absolute binding of unsandboxed gh, and this task changes no sandbox policy."
  - control: "5.14 item 2 (sanitized environment first)"
    disposition: "residual: the pool enters env -i before interpreter startup, discovery or child execution and uses verified absolute binaries and pinned Git configuration; tests/unit/test_audit_pool.py::test_audit_pool_never_executes_a_shim_first_on_path and tests/unit/test_audit_pool.py::test_audit_pool_ignores_planted_git_environment_and_config exercise this control."
  - control: "5.14 item 3 (trusted-path boundary checks)"
    disposition: "residual: all trusted paths are realpath-resolved and rejected under worker roots, with case-insensitive identity comparison where required; tests/unit/test_audit_pool.py::test_audit_pool_refuses_trusted_paths_under_a_worker_root exercises direct and symlinked paths."
  - control: "5.14 item 4 (execute verified realpaths and consume verified contents)"
    disposition: "residual: verified executable realpaths are used directly, consumed files have unique 0600 trusted snapshots, recorded SHA256 values are checked before reuse and shadow rows bind compared outputs; tests/unit/test_audit_pool.py::test_audit_pool_never_consumes_a_file_swapped_after_verification exercises replacement between verification and consumption."
  - control: "5.14 item 5 (output and reservation identity)"
    disposition: "residual: full 40-hex heads name requests and outputs, each physical slot has one persistent inode-bound lock created with O_EXCL, and overlapping queues are refused; tests/unit/test_audit_pool.py::test_pool_detects_replaced_lock_inodes_and_frozen_request_changes, tests/unit/test_audit_pool.py::test_pool_refuses_queues_sharing_a_physical_slot_range and tests/unit/test_audit_pool.py::test_pool_uses_full_heads_and_refuses_case_alias_output_collisions exercise these controls."
  - control: "5.14 item 6 (honest residual)"
    disposition: "residual: the final section states the host-boundary residual in one line; fixture success does not claim protection against an unsandboxed same-UID writer or completion of D-024-17."
  - control: "5.14 item 7 (shared verification)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_audit_pool_never_executes_a_shim_first_on_path; tests/unit/test_audit_pool.py::test_audit_pool_ignores_planted_git_environment_and_config; tests/unit/test_audit_pool.py::test_audit_pool_refuses_trusted_paths_under_a_worker_root; tests/unit/test_audit_pool.py::test_audit_pool_never_consumes_a_file_swapped_after_verification"
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
  - claim: |-
      すべての worker 席は manifest から描画した sandbox の下で動き、書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
    command: make render-check
    output: |-
      (pasted at dispatch)
---

# AGMSG-TASK dotfiles-T133-audit-pool-a02 — C-80 reset of dotfiles-T133-audit-pool-a01 under D-024-18 (plan 024 P1-4a; seat=a008, worker-f; tools/audit-pool-a02 from origin/main; one PR)

This task resets the audit-pool half split from PR #410. The a01 text failed C-80 with six P1 and four P2 in `.orchestration/validation/dotfiles-T133-audit-pool-a01-text-security.md.last.md`. Every finding is an implementation requirement and regression below.

Design section 5.14 of `.orchestration/plans/024-design-quality.md` applies in full by reference under D-024-18. Its seven items and premise 6 are authoritative. Programs items (2) and (3) of `.orchestration/plans/024-design-programs.md` supply the pool and vocabulary design. Programs item (16), `audit-pool.sh --second-opinion`, remains outside this task.

The worker creates `tools/audit-pool-a02` from `origin/main` and re-runs the three inherited premises before cherry-picking. The first premise's a02 branch denotes the stopped combined `dotfiles-T133-verdict-audit-pool-a02` lineage at `b8998de162afc72d53d07679b8f0a194fcc480ff`. The orchestrator supplies premise 6's rendered-deny evidence before dispatch. An unavailable write boundary holds dispatch.

The source commits introducing and modifying `scripts/orchestrator/audit-pool.sh`, `scripts/orchestrator/orch-audit.sh`, `.schemas/classes.yaml` and `tests/unit/test_audit_pool.py` contribute changes to those four paths only. Mixed-path commits contribute only their relevant changes. The report lists each source SHA, its resulting commit and any conflict resolution.

The a03 acceptance context is `.orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md`. Commit `0e16d7eb` removed the pool files from PR #410 and restored its audit wrapper to `origin/main`. PR #410 remains the verdict sibling's PR. The audit-pool a01 never started on a seat and never pushed, so this worker deletes nothing from that lineage.

This branch contains the inherited pool behavior, this reset's fixes, the shared test helper and its own artifacts. Predecessor task copies and evidence do not enter its cumulative diff. This task has one new PR and its own reviews, audit and acceptance.

## Goal

Queued audits run with bounded concurrency in separate trusted pool worktrees and retain only schema-valid, masked audit JSON. Differential results account for every previous finding with status verified against the previous-to-current diff.

Executable selection, repository selection, file consumption, reservations and publication follow 5.14. Decoded diagnostics expose no secret values. One validated task and full head has one reserved or running audit across concurrent pool processes.

## Files

1. `scripts/orchestrator/audit-pool.sh [--once|--loop] [--max 2] [--queue <dir>]` remains Bash with English shdoc documentation. The default queue is `.orchestration/validation/audit-queue/`. Requests are `<task>-<head40>.request` files containing `key=value` lines for `pr`, `head`, `base`, `task` and optional `previous_head`. The basename and contents agree on the validated task and full 40-hex head. Values are validated before forming arguments or paths.

   The entry enters `env -i` before interpreter startup files, executable discovery, repository discovery or child execution. Startup uses trusted absolute interpreter and bootstrap paths. The pool resolves `python3`, `uv`, `codex`, `gh` and `git` to verified absolute real binaries in the trusted root. Mise shims and worker-controlled tool configuration never select their targets. Other external utilities also use verified absolute executables. The private PATH contains only links to verified targets and supplies no executable discovery. Python runs with `-I`. The report records the trusted root and executable realpaths.

   Queue, worktree, output, snapshot and lock paths are realpath-resolved before use. Trusted paths under `.claude/worktrees/` or a manifest worker root are refused. Symlink components are resolved before comparison, and physical identity comparisons are case-insensitive on case-insensitive filesystems. Parent directories receive the same checks before creating a missing leaf.

   Each slot uses a detached `origin/main` worktree under the anchored trusted root, outside all worker roots, selected through `ORCH_REVIEW_WORKTREE`. Slot 1 has its own pool worktree. The integration worktree and another slot's physical directory are never reused. The report records this replacement of the inherited `.claude/worktrees/orchestrator-audit-<n>` placement.

   Each request invokes the verified audit wrapper as `<verified-wrapper-realpath> <task> --head <head40> <pr> --json .orchestration/validation/<task>-audit-<head40>.json`. Differential arguments name the full previous head and its full-head output.

   Differential execution remains disabled until `.orchestration/validation/audit-shadow.tsv` supplies two distinct completed comparisons with zero finding difference. Every shadow row that can enable differential execution or downstream `--apply` identifies both compared audit outputs by sha256, task and full head. The pool validates and freezes those outputs, recomputes their finding comparison and rechecks their recorded hashes before using the row. Fabricated rows, duplicate comparisons, missing outputs and changed outputs do not enable execution.

   Before enablement, a request with `previous_head` receives a full audit and a differential prompt at `<out>.differential-prompt.txt`. That prompt names the frozen previous findings and actual previous-to-current diff.

   A zero audit exit and output passing the verified wrapper's `--validate .schemas/audit.json <out>` retain the masked JSON and rename the request to `.done`. Other outcomes remove only this request's verified unusable output, write a masked rejection reason and mark the request `.blocked`.

   A failed Codex run reporting 429 is retried after 60, 120 and 240 seconds, then blocked. Logs and rejection records retain the retry marker and masked diagnostics without an unmasked transcript. `--loop` repeats every 30 seconds until the verified queue's `.stop` exists.

   `tests/unit/test_audit_pool.py::test_pool_saves_only_schema_valid_audit_json_and_blocks_a_rejected_request` retains its behavior. The red-then-green selectors for these controls are `tests/unit/test_audit_pool.py::test_audit_pool_never_executes_a_shim_first_on_path`, `tests/unit/test_audit_pool.py::test_audit_pool_refuses_trusted_paths_under_a_worker_root` and `tests/unit/test_audit_pool.py::test_pool_requires_hash_bound_completed_shadow_comparisons_for_apply`.

2. Queue selection retains portable `fcntl.flock` locking because macOS has no `flock` command. `--max` remains a positive single-digit slot count with default 2. The slot range remains 1 through `--max`.

   Selection freezes the validated request into a unique 0600 snapshot under the trusted root. The child consumes those exact bytes and values after a sha256 recheck. It never reparses a mutable queue pathname. Request transitions compare the original file identity before renaming it. Replacement causes refusal and never redirects publication or cleanup.

   Queue selection and each physical slot use trusted persistent locks. Initial lock creation uses `O_EXCL`. Each physical slot has exactly one lock, independent of queue naming. The pool retains its open descriptor and compares its inode with the lock pathname after acquisition and before consumption or publication. Lock files are never unlinked or replaced to release ownership. A replaced inode refuses work rather than creating a second lock domain.

   Trusted queue-to-slot ownership refuses queues sharing any physical slot in their range. Separate `--queue` directories never authorize simultaneous checkout or cleanup of the same slot.

   Reservations, running markers and all output names use the full 40-hex head. Task-name aliases on case-insensitive filesystems are refused before opening, replacing or removing an output. Distinct heads sharing their first seven characters retain distinct reservations and outputs.

   Under the queue lock, malformed basenames are blocked unread with a rejection reason. Only the anchored `<task-id>-<head40>.request` form reaches processing. Decoded slots are validated as positive single-digit integers before use. Filename text never enters Bash arithmetic.

   Killed-pool running markers retain their slot and audit-key reservations until explicit trusted cleanup. `--once` names held slots when requests wait. Marker replacement is detected before its contents authorize any operation.

   The retained malformed-name test keeps its command-substitution-shaped filename, absent marker, absent Codex call, blocked result and rejection reason. The retained slot test proves the physical slot is separate from integration and outside worker roots, beyond checking Codex's textual `-C`.

   The red-then-green selectors are `tests/unit/test_audit_pool.py::test_pool_detects_replaced_lock_inodes_and_frozen_request_changes`, `tests/unit/test_audit_pool.py::test_pool_refuses_queues_sharing_a_physical_slot_range`, `tests/unit/test_audit_pool.py::test_pool_uses_full_heads_and_refuses_case_alias_output_collisions`, `tests/unit/test_audit_pool.py::test_pool_rejects_a_malformed_request_name_and_never_evaluates_it` and `tests/unit/test_audit_pool.py::test_pool_slots_never_use_the_integration_worktree`.

3. `scripts/orchestrator/orch-audit.sh` accepts `--head <sha40>` in place of the existing `<pr-worktree>` positional and requires that head to exist as a commit in the verified checkout. `ORCH_REVIEW_WORKTREE` selects a verified trusted slot. The standalone default also resides under the anchored trusted root outside worker roots.

   Direct wrapper execution follows the same sanitized startup and absolute-executable controls as pool execution. Every Git invocation uses the verified absolute Git binary, explicit `-C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `-c core.hooksPath=/dev/null`, `-c core.fsmonitor=false` and `-c protocol.allow=never`. Inherited `GIT_*` values are discarded. Replacement objects are disabled. Repository redirects and planted configuration cannot change repository discovery, checkout or the diff.

   The validator and ledger checker are realpath-resolved, checked against the trusted `origin/main` content and executed by those exact verified realpaths. Their executable targets receive the check. An unchanged tracked symlink alone authenticates no target. Content hashes are rechecked immediately before execution. The existing tracked ledger-check override remains constrained by these checks.

   Evidence read by validation, ledger checking and the auditor comes from the same unique 0600 trusted snapshots. Snapshot sha256 values are checked before consumption and recorded beside the output. Copying evidence into the review worktree preserves those verified bytes. Sidecar digest records preserve the unchanged audit JSON schema.

   `--json <out>` asks for one fenced JSON audit block immediately before the final `Verdict:` line. The verdict remains the last non-blank line for the existing integration gate. The JSON contains `head`, `task_id`, `auditor`, `generated_at`, `verdict` and findings with `id`, `priority`, `confidence`, `file`, `line`, `class`, `scope`, `rationale` and `status`.

   Extraction validates against the real `.schemas/audit.json` and binds head, task and verdict to this audit and its final verdict line. Missing or invalid JSON produces exit 3 and leaves no usable stale JSON. `--validate <schema> <json>` runs the same stdlib checker without launching an audit. Required keys, types, enums, bounds, SHA patterns, additional-property restrictions and date-time format remain enforced.

   `generated_at` is an RFC 3339 date-time with `Z` or an explicit offset. Date-only values, naive timestamps and invalid calendar dates fail. The offset regression retains its positive and negative controls.

   Every existing refusal remains. The trusted checkout cannot be at the audited head, the sweep has no gaps and the ledger check passes. Only a zero Codex exit with a fresh, non-empty final message supplies evidence. Failed transcripts expose only the 429 retry marker. Review-worktree cleanup removes copied schema data and operates only on verified slot paths.

   After a successful audit exit, the extracted document receives the existing JSON-aware masking and schema revalidation before retention. Masker failure makes the audit unusable even when cleanup fails. The extracted-document test retains its Unicode-escaped token fixture and decoded-token absence assertion.

   The red-then-green selectors are `tests/unit/test_audit_pool.py::test_audit_pool_ignores_planted_git_environment_and_config`, `tests/unit/test_audit_pool.py::test_orch_audit_executes_only_the_realpaths_verified_against_origin_main`, `tests/unit/test_audit_pool.py::test_audit_pool_never_consumes_a_file_swapped_after_verification`, `tests/unit/test_audit_pool.py::test_orch_audit_json_mode_rejects_a_generated_at_without_an_offset` and `tests/unit/test_audit_pool.py::test_orch_audit_json_mode_masks_the_extracted_document_before_retaining_it`.

4. `.schemas/classes.yaml` contains one entry per controlled class as `<slug>: {remedy: <sentence>, blast_radius: [<globs>]}`. It retains every ledger class in the cited acceptance records and includes `unbound-evidence`, `fail-open-on-error`, `argv-text-mismatch`, `json-interpolation`, `string-form-comparison`, `ps-output-parsing`, `records-form` and `advisory-p2`. The validation file contains the seeding command and output.

   Vocabulary closure reads both the JSON-front-matter `ledger` and prose ledger rows containing `<id>\t<class>`. It includes standalone rows and the tab-separated rows embedded in prose in `.orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a01.md`, `.orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a02.md` and `.orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md`, together with the other cited acceptance records. An empty JSON ledger never suppresses prose rows. `local:85a4722:1` with class `interpreter-selection` is a required regression fixture.

   PR #410 owns the real audit JSON schema. The standalone pool tests embed its source-pinned structural contract from `b8998de162afc72d53d07679b8f0a194fcc480ff` inside the allowed test module and instantiate it only in temporary repositories. The fixture enum includes the complete controlled vocabulary. The report records the source SHA and explicit enum additions required by prose-ledger closure.

   The schema-class test compares the fixture enum and vocabulary, rejects an unknown class and checks the real checkout schema when present. A real schema mismatch fails visibly and is reported to the verdict sibling; this worker changes no runtime schema. Standalone tests require neither an unmerged sibling worktree nor a Git object fetched during CI. Runtime auditing requires the real schema and refuses its absence or incompatible vocabulary.

   The red-then-green selectors are `tests/unit/test_audit_pool.py::test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius` and `tests/unit/test_audit_pool.py::test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class`. The closure regression fails on the inherited JSON-only reader even when its JSON ledger is empty.

5. The b8998de differential-audit P1 is fixed. `--previous-head <sha40> --previous-findings <json>` binds the previous document to this task and previous head and supplies the actual previous-to-current Git diff.

   Previous evidence has its sha256 recorded when its validated, masked output is retained. Reuse requires that existing trusted digest record and rechecks it before creating the previous-evidence snapshot and immediately before consumption. Computing a fresh hash of an already rewritten file never establishes prior validation. Missing digest records, changed bytes and disagreement between ledger-checked and auditor-consumed bytes refuse reuse.

   The auditor verifies each previous finding's `fixed` or `still-open` status against the diff and records its supporting explanation within the existing finding record. New findings concern new hunks.

   Before retaining a differential result, extraction verifies that every previous finding appears exactly once with its original identity and an explicit `fixed` or `still-open` status. Omission, duplicate accounting, invalid status, mismatched task or head, unreadable previous evidence and unreadable diffs refuse the result with exit 3 and leave no usable JSON. A schema-valid empty findings array cannot erase a previous finding. A fixed claim requires diff support.

   `tests/unit/test_audit_pool.py::test_orch_audit_differential_result_verifies_every_previous_finding_against_the_diff` is written first. Its previous audit contains a P1 outside the new hunks and its otherwise valid current response omits it. The inherited implementation retains the empty result. The correction refuses it and removes stale output. Subcases cover missing status and unsupported fixed claims. Positive controls retain an unchanged finding as still-open and account for a genuinely fixed finding with diff support.

   `tests/unit/test_audit_pool.py::test_orch_audit_refuses_changed_previous_evidence_at_reuse` is written first. It rewrites a previously validated audit to `findings: []` without updating its trusted validation digest and proves that neither differential execution nor ledger checking consumes the replacement. Both selectors have red and green results.

6. The b8998de decoded-diagnostic P2 is fixed. Decoded values are masked before schema errors are constructed or printed. Raw decoded enum values, object keys and secret-bearing exception details never reach stdout, stderr, pool logs or rejection records. Both JSON extraction and standalone validation enforce this boundary. Masker failure refuses without an unmasked diagnostic fallback.

   `tests/unit/test_audit_pool.py::test_orch_audit_masks_decoded_values_before_printing_schema_errors` is written first. Its invalid enum contains a Unicode-escaped fake token that the Markdown masker misses before decoding. The inherited checker prints the decoded token. The correction rejects the record, omits the token from every diagnostic surface and leaves no usable JSON. Standalone validation and a valid masked-document control retain their expected results. The selector has red and green results.

7. The b8998de duplicate-reservation P2 is fixed. Selection refuses an audit key already reserved or running while holding the queue lock and the relevant physical-slot lock. The key binds the validated task and full head to the frozen request and output identity.

   A reserved `.running-<slot>` marker covers both the interval before child startup and execution. A duplicate becomes blocked with a masked reason without taking another slot, replacing the original marker or modifying its outputs. A distinct key can use another free slot. Killed-pool markers continue reserving their keys until explicit trusted cleanup.

   `tests/unit/test_audit_pool.py::test_pool_refuses_an_audit_key_already_reserved_or_running_under_the_lock` is written first. A barrier holds the first fake audit active while the same task and head are enqueued again and another pool process selects work. The inherited implementation reserves another slot. The correction starts exactly one audit, blocks the duplicate and preserves the original result. A distinct-key control uses the other slot. The selector also covers a reserved request whose child has not started and has red and green results.

8. `tests/unit/test_audit_pool.py` retains every existing behavior case and assertion. It retains `test_pool_saves_only_schema_valid_audit_json_and_blocks_a_rejected_request`, `test_pool_runs_at_most_max_audits_and_the_third_request_waits`, `test_pool_retries_a_429_three_times_then_blocks`, `test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree`, `test_orch_audit_json_mode_extracts_the_final_json_block_and_keeps_every_refusal`, `test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class`, `test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius` and `test_orch_audit_json_mode_rejects_a_generated_at_without_an_offset`.

   It also retains `test_pool_rejects_a_malformed_request_name_and_never_evaluates_it`, `test_pool_slots_never_use_the_integration_worktree` and `test_orch_audit_json_mode_masks_the_extracted_document_before_retaining_it`. Their setup and expectations adopt full-head names and trusted slot placement without dropping their original assertions.

   Refusal cases retain changed and untracked validators, ledger-check failure, masker failure, head refusal, unavailable commits, sweep gaps, missing JSON, unknown classes and mismatched audit identity or verdict. Fixtures use temporary repositories, isolated trusted roots, fake Codex and fake sleep. The extracted-document test uses the real masker. Fake binaries reside in the fixture's trusted binary root; an attacker-controlled PATH directory is a separate negative input.

   The module uses `tests/unit/trusted_exec_contract.py`, creating that shared helper here if absent. The helper supplies the minimum reusable trusted-host fixtures without a production bypass or a new runtime configuration option. Its four contract tests are `tests/unit/test_audit_pool.py::test_audit_pool_never_executes_a_shim_first_on_path`, `tests/unit/test_audit_pool.py::test_audit_pool_ignores_planted_git_environment_and_config`, `tests/unit/test_audit_pool.py::test_audit_pool_refuses_trusted_paths_under_a_worker_root` and `tests/unit/test_audit_pool.py::test_audit_pool_never_consumes_a_file_swapped_after_verification`.

   The shim test plants executable markers and worker tool configuration. The Git test plants repository redirects, injected configuration, hooks and replacement-object inputs. The path test covers worktree, output, queue, executable, ledger, evidence and lock paths through direct and symlinked worker roots. The swap test places barriers between verification and consumption for executable targets, requests, previous evidence and copied audit inputs, and proves replacement bytes never reach their consumer.

   All four selectors have red and green results. Fixture setup supplies the helper, trusted binaries and schema data on the red baseline, so an import error, missing sibling file or missing executable never substitutes for the intended behavioral failure. All fixture data and shared-helper changes count against the test cap.

## Out of scope

The verdict sibling owns `verdict.sh`, `.schemas/verdict.json`, `.schemas/audit.json` and `test_verdict.py`, which PR #410 carries. This task changes none of those files.

`dispatch.sh`, the record generator, gate and validator implementations, Makefile targets, CI changes, `integrate-seat.sh`, `dispositions.py`, `hold-playbook.sh` and programs item (16)'s `--second-opinion` remain outside this task.

Seat sandbox policies and the absolute execution binding of unsandboxed worker commands belong to D-024-17. This task relies on their stated boundary, records its residual and changes no policy.

The three inherited b8998de findings and all ten C-80 findings assigned above are fixed here. They are never reassigned as advisory P2.

## Check

The validation file contains commands, verbatim output, exit statuses and tested heads for the three re-run source premises, premise 6's rendered-deny evidence, the source cherry-pick inventory, `make unit-test`, `make render-check`, `make format`, `shellcheck scripts/orchestrator/audit-pool.sh scripts/orchestrator/orch-audit.sh`, `shfmt -i 4 -sr -d scripts/orchestrator/audit-pool.sh scripts/orchestrator/orch-audit.sh` and `uv run python -m unittest tests.unit.test_audit_pool -v`. The script checks are clean and the pool module is green.

Each selector named in Files receives its own red result against the inherited behavior at `b8998de162afc72d53d07679b8f0a194fcc480ff` and green result after its fix. A retained regression already fixed at that head retains its historical failing head and receives a fresh final-head green result. The validation file distinguishes those historical results from the new regressions.

The `tests/unit/test_audit_pool.py::<method>` selectors identify methods in `AuditPoolTest`. Individual executions use `uv run python -m unittest tests.unit.test_audit_pool.AuditPoolTest.<method> -v`. Every new regression is written before its implementation change.

Red-baseline fixtures provide the source-pinned schema shape, complete vocabulary fixture, shared helper and trusted executable setup. Missing sibling files never cause an unrelated red result. Historical combined-task evidence never substitutes for this reset's validation.

`git diff --numstat origin/main...HEAD` shows at most 600 changed lines outside `tests/` and `.orchestration/` and at most 800 under `tests/`. Changed lines are additions plus deletions over the complete PR diff. `.schemas/classes.yaml` counts within the 600-line cap and is also reported separately. The shared test helper and every fixture count within the 800-line cap. Meeting a cap removes no required behavior, validation, assertion or trust-boundary control.

An inherited check failure is reproduced against the unchanged base with the same command and environment and reported as a failure with that evidence. It is never labelled passing or repaired outside `allowed_files`. Local Bats tests remain unrun and GitHub Actions supplies their required results.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task-copy byte comparison and SHA256 cover this task's complete text. The cumulative changed-file inventory contains only this task's allowed files.

## Completion

One fresh branch, `tools/audit-pool-a02`, starts from `origin/main` and carries one new PR with an English title and description. The worker records source SHAs, resulting commits and conflict resolutions in `.orchestration/dotfiles-T133-audit-pool-a02/report.md`. Its PR receives its own reviews, final-head task-level audit, security review and acceptance record. Neither sibling's review evidence substitutes for the other's.

Dispatch occurs only after this exact a02 text has passed its C-80 pre-dispatch security review. The orchestrator records the reviewed text's sha256 and `Verdict: correct` evidence before sending it. The review of a01 supplies findings, never approval of a02.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with the live overrides below, `dotfiles-T133-verdict-audit-pool-followup-a01` as the owner of every advisory P2, `task_copy=<sha256 of .orchestration/dotfiles-T133-audit-pool-a02/task.md>` and `parked_pr=407` in the RESULT. The orchestrator verifies the owner task exists before assigning an advisory disposition. PR #407 stays parked and no parking operation is repeated.

The a02 task copy is byte-identical to the dispatched text. The TASK's `task_sha256` and RESULT's `task_copy` bind that same copy. The worker creates no predecessor copy and deletes no predecessor artifact.

There is at most one worker-side pre-push review round. Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. This reset preserves the stopped combined task's history and a01's pre-dispatch rejection. A surviving P0/P1 is sent in the RESULT as `open:<finding id>` with its evidence and stops the PR for the operator's decision. The worker never starts another review loop to hide a surviving finding.

The report and RESULT identify the new PR, head, base, branch, changed files, source SHAs, every feedback disposition, test names, red and green heads, code and test totals, vocabulary count, trusted executable realpaths, evidence digests, task-copy hash and evidence paths. They distinguish inherited behavior, the three inherited fixes, all ten C-80 fixes, historical evidence and final-head results.

Evidence records use `.orchestration/dotfiles-T133-audit-pool-a02/report.md`, `validation.md`, `sandbox.md`, `learning.md` and `revise.yaml` when applicable. A Codex seat writes evidence at those same relative paths in its own worktree and states that placement in the RESULT. Worker review evidence uses the required `-worker-` infix. The orchestrator copies worktree evidence by absolute path before review.

This task is `security: true`. The orchestrator runs its own task-level audit and separate security-profile review on the final head before the gate. Final-head CI, the complete feedback sweep, finding dispositions, acceptance record, integration gate and merge follow Orchestrator Playbook step 10 in its prescribed order. Changed heads receive fresh required evidence. The orchestrator merges with `gh pr merge --squash --match-head-commit <audited head>` after the gate.

No `@codex review` comment is posted. Automatic review is observed for the bounded window and absence after 15 minutes is recorded as `bot: none`. The RESULT states the actual observed review count. Commands matching a live ask rule are not issued and no API or browser path bypasses that rule.

Each `gh` command, Git write and `git fetch` runs individually without shell chaining or a wrapper combining commands. Refused commands retain their command, exit status and output while independent authorized work continues.

Until plan 024 P1-14 lands, every string containing the words `gh pr merge` or `gh pr create` is written with the file-edit tool. Shell commands, heredocs and shell wrappers never write those strings. This writing rule supplies no authorization to execute a command refused by the live permission boundary.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```

Live audit-service calls and local Bats remain unexercised; runtime audits require the real schema, and killed-pool reservations require explicit trusted cleanup.
Residual: same-UID processes outside every seat sandbox and the unsandboxed-gh exemption owned by D-024-17 remain host-boundary risks.