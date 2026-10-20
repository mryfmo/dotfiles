---
format: 2
task_id: dotfiles-T133-task-generator-plan-check-a06-checker
kind: code
security: true
design: 5.14 items 2, 3, 8, 9
design_review:
  design: .orchestration/plans/024-design-quality.md
allowed_files:
  - scripts/orchestrator/task-consistency-check.py
  - tests/unit/test_task_consistency_c11_c15.py
  - tests/unit/test_task_checkers.py
  - .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/**
after: []
reset_of: [dotfiles-T133-task-generator-plan-check-a05-checker]
retained_predecessor_directories:
  - .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/
expected_result_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/report.md
expected_validation_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/validation.md
expected_sandbox_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/sandbox.md
expected_learning_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/learning.md
expected_autoskill_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/autoskill.md
expected_measure_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/measure.md
threat_table:
  - {control: "scripts/orchestrator/task-consistency-check.py", disposition: "residual: Checker defenses start after parent execution; fixtures and final-head audit establish checker behavior, not protection against pre-start execution or concurrent same-UID replacement."}
  - {control: "tests/unit/test_task_consistency_c11_c15.py", disposition: "residual: Temporary repositories exercise the real checker; modeled filesystem semantics and fake API responses establish behavior rather than native platform coverage or live GitHub availability."}
  - {control: "tests/unit/test_task_checkers.py", disposition: "residual: Historical fixtures retain their coverage; changed expectations require an identified contract change and cannot conceal unrelated findings."}
  - {control: ".orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/**", disposition: "residual: Commit the byte-identical .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task.md and required evidence before RESULT; artifacts contain no runtime helpers, credentials or approval authority."}
  - {control: "predecessor copy .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/task.md", disposition: "residual: Retain this copy and its artifact directory unchanged from 06ffefbc; reset_of records lineage and permits retention, not edits or inherited approval of the new head."}
  - {control: "checker-side interpreter selection after startup", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_interpreter_resolution_order"}
  - {control: "gh child environment", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_gh_child_preserves_parent_tokens"}
  - {control: "canonical-main design read", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c15_uses_canonical_main_only"}
  - {control: "C6 canonical receipt binding and design hash", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes"}
  - {control: "fixture and evidence symlink exemptions", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_symlink_to_applied_file_is_finding"}
  - {control: "fixture and evidence case-alias exemptions", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_case_alias_to_applied_file_is_finding"}
  - {control: "original Unicode path confinement", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_resolves_original_unicode_path"}
  - {control: "internal directory aliases", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_rejects_internal_directory_alias"}
  - {control: "directory pruning name comparison", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_prunes_with_normalised_directory_names"}
  - {control: "path_entry pipeline identity", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_canonical_path_pipeline_rejects_normalised_collisions"}
  - {control: "path grammar and filesystem identity", disposition: "residual: Each grammar case retains a behavioral fixture; normalized name comparisons never replace confinement of the original path or prevent concurrent same-UID races."}
  - {control: "C16 reference and item coverage", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c16_requires_reference_and_all_item_rows"}
  - {control: "C16 item occurrence counting", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_rejects_multi_item_rows"}
  - {control: "C16 resolved-target applicability", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_uses_resolved_literal_alias"}
  - {control: "task metadata", disposition: "residual: The orchestrator verifies reset lineage, the retained-directory inventory, measured caps, canonical dispatch prerequisite and dispatched-copy identity before sending and accepting."}
  - {control: "metadata separators", disposition: "residual: The complete dispatched-file digest covers YAML separators and body; quoted commands and evidence are data rather than execution authority."}
  - {control: "in-process effects", disposition: "residual: C14 retains its fixed read-only vocabulary and dispatched-byte authorization; no shell, arbitrary Python operand or task-supplied executable is introduced."}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: No caller or workflow edit is authorized; unchanged parent PATH and shared cache remain exposed. Checker compatibility proves no parent sanitization, and token values never enter evidence or argv."}
  - {control: "new or renamed scripts", disposition: "residual: Only the existing checker changes in production; add no resolver, wrapper, dependency, template or runtime code under artifacts."}
  - {control: "orchestrator effect dispatch.sh keeps calling the checker unchanged", disposition: "residual: The dispatch fixture proves checker compatibility only; dotfiles-T133-loop-limits-a01 owns dispatch.sh and dotfiles-T133-trusted-entrypoint-binding-a01 owns executable binding before checker startup."}
  - {control: "orchestrator effect merge", disposition: "residual: The worker never merges; the orchestrator follows Playbook step 10 and binds integration to the audited head."}
  - {control: "orchestrator effect update-branch", disposition: "residual: A changed head requires refreshed applicable CI, feedback and audit evidence; never reuse a preceding head's approval."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: No forced removal is assigned; preserve worker state, PR #440 and withdrawn lineage evidence."}
  - {control: "5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: Item 0 applies by reference; this slice establishes neither separate OS identities nor credential isolation."}
  - {control: "5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: Item 1 applies by reference; this task uses a Codex sandbox and makes no Claude deployment claim."}
  - {control: "5.14 item 2: 無害化した環境を最初に", disposition: "residual: Item 2 applies by reference; PATH-selected mise/uv execute first. dotfiles-T133-loop-limits-a01 owns dispatch.sh, dotfiles-T133-trusted-entrypoint-binding-a01 owns executable binding, and dotfiles-T133-ci-efficiency-followup-a04 owns the resolver and private UV_CACHE_DIR."}
  - {control: "5.14 item 3: 信頼パスの境界検査", disposition: "residual: Item 3 applies by reference; the canonical path pipeline does not establish host isolation or prevent same-UID replacement."}
  - {control: "5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: Item 4 applies by reference; retained consumed-byte and executable-binding checks cannot exclude concurrent same-UID interference."}
  - {control: "5.14 item 5: 出力と予約の同一性", disposition: "residual: Item 5 applies by reference; this read-only checker adds no reservation or integration resource."}
  - {control: "5.14 item 6: 正直な残余", disposition: "residual: Item 6 applies by reference; distinguish fixture observations, inherited evidence, compatibility warnings and unverified deployment."}
  - {control: "5.14 item 7: 検証", disposition: "residual: Item 7 applies by reference; retain negative controls and disclose unavailable platform coverage without claiming it passed."}
  - {control: "5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes"}
  - {control: "5.14 item 9: 私設キャッシュ", disposition: "residual: Item 9 applies by reference; unchanged dispatch selects shared $HOME/.cache/uv, allowing pre-checker poisoning. dotfiles-T133-ci-efficiency-followup-a04 owns the resolver/private cache; dotfiles-T133-loop-limits-a01 and dotfiles-T133-trusted-entrypoint-binding-a01 own parent execution and binding."}
  - {control: "5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: Item 10 applies by reference; D-024-36 records this host's network-disabled Codex seats. Orchestrator transport grants the worker no sandbox escape."}
premises:
  - claim: The fixed measurement base resolves to this commit; local object identity supplies no canonical GitHub design authority.
    command: |-
      git rev-parse 60a6fb2b
    output: |-
      60a6fb2b324d0381c4a6e539b37c650105154a7e
  - claim: The inherited continuation head resolves to this commit; the pipeline draft is not part of this head.
    command: |-
      git rev-parse 06ffefbc
    output: |-
      06ffefbc633fe37bcef107385ea96810b2a9a0c5
---

# AGMSG-TASK dotfiles-T133-task-generator-plan-check-a06-checker

🤖 I read the AGENTS.md for mryfmo/dotfiles.

## Goal and lineage

This text is the reset after INV-6 S2 and C-61 under D-024-39; the a05 findings history is in `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md`.
The a05 text's two amendments and two worker fix rounds are spent; this reset authorizes its measured pipeline round rather than a third a05 repair.

Amendment 1 addresses C-80 round 1's `text-security:4a49ed9:1 input-validation` row; `previous_sha256: 4a49ed9263e025e84f3ec5a51df553cfc83ab71192a4de016770e42a1f80491b`. Read `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-4a49ed9.md.last.md` whole. Only identity-aware coverage and collision rejection, with their regression, change.

Read the a05 task and acceptance record whole, including the carried a04 audit rows and both `re-plan: glob-filter` decisions. Also read both security reviews whole:

- `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-cedc7f5.md.last.md`
- `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-06ffefb.md.last.md`

[memory:failure] PR #417's a01–a04 lineage was withdrawn after the audit of `7a201eab2e77596c9a7bc421162b2f3fde25f6f7`; the a05 record carries its findings and re-plans. Preserve that history; do not revive the withdrawn three-script implementation.

[memory:decision] Plan 024 P1-12 continues only the checker C11–C16 and its tests. Worker a012 (Codex, worker-g) continues PR #440, branch `tools/task-generator-plan-check-a05-checker`, from `06ffefbc633fe37bcef107385ea96810b2a9a0c5`, with fixed measurement base `60a6fb2b324d0381c4a6e539b37c650105154a7e`; do not start a fresh branch or PR.

The held, uncommitted pipeline draft is input to this round, not verified completion. Preserve the existing R4 lint correction. The a05 report records 32 green checker tests on Python 3.15.0 and 3.12.15 and 28/28 killed mutants; rerun against the new head.

`task-from-plan.py`, `plan-check.py`, templates, workflows, dispatch, resolver implementation, deployment and canonical orchestration records remain outside scope.

## Dispatch prerequisite and design

Boundary PR #435's merged state and design publication remain dispatch prerequisites. The orchestrator, which has network access, obtains canonical main with `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`; validate exactly 40 lowercase hexadecimal characters before substituting `<sha40>`.

Read `gh api 'repos/mryfmo/dotfiles/contents/.orchestration/plans/024-design-quality.md?ref=<sha40>' --hostname github.com --jq .content | base64 -d | grep -F 'Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。'`. Require successful exits from every stage and reject missing or malformed content; successful grep alone is insufficient.

Before sending, record #435's merged state from the fixed repository/host API, pinned main SHA, decoded design SHA-256, commands and stage exits in Checks. Local refs, objects, replacement objects, URL rewrites and local digests supply no prerequisite authority. `after: []` does not waive this boundary.

Design 5.14 at `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen under D-024-29 and applies by reference under D-024-30; every item 0–10 has its own threat row above. Do not paraphrase or amend the frozen design.

Premises record local provenance only. Re-run applicable probes before dispatch and paste results in Checks; authoring commands do not extend C14's vocabulary or authorize shell execution.

## Implementation contract

1. Retain interpreter selection: landed `scripts/orchestrator/trusted-interpreter.sh` first, supplied `TRUSTED_PYTHON` second, real `sys.executable` with an explicit stderr fallback warning last. Validate the selected interpreter; resolver failure or invalid supplied input refuses rather than falling through. Add no interpreter PATH discovery.

   Neither `TRUSTED_PYTHON` nor `TRUSTED_BIN_DIR` becomes mandatory. Retain checker-side executable binding when dispatch strips both, and the absolute-cache requirement. No dispatch edit or outer environment prefix repairs this slice.

   Parent PATH-selected mise/uv and shared-cache execution happen before these defenses. Parent hardening belongs to dotfiles-T133-loop-limits-a01, executable binding to dotfiles-T133-trusted-entrypoint-binding-a01, resolver/private UV_CACHE_DIR to dotfiles-T133-ci-efficiency-followup-a04; this slice closes none of those boundaries.

2. C14 consumes `(stdout, exit_status, stderr)`; every nonzero status produces a finding even with matching or empty stdout. Keep dispatched-byte digest authorization, warning without authorization, whitespace comparison and fixed read-only vocabulary. Unsupported commands never reach a shell.

3. Preserve parent `GH_TOKEN` and `GITHUB_TOKEN` exactly for `gh` children, testing each independently, both and neither. Forward through the subprocess environment mapping, never argv or printed values. Retain other sanitization and explicit repository/host binding; dispatch forwarding remains unchanged.

4. C15 accepts referenced designs only from canonical GitHub main, including tasks without invariants. Validate the 40-hex SHA from the fixed repository/host API, then read `gh api repos/mryfmo/dotfiles/contents/<path>?ref=<sha40> --hostname github.com`. Local-only designs fail C15; API failures refuse. Preserve assignment-set and byte-equality checks; hostile `GH_HOST`, local Git configuration and local objects supply no authority.

   C6 uses the same pinned canonical bytes as C15. When `design_review.design_sha256` is present, require its exact SHA-256 over decoded API bytes and a matching `design_review.receipt` against the canonical receipt. When absent, retain legacy canonical receipt comparison and emit a C6 warning naming the missing field. Missing canonical bytes or binding, malformed/mismatched hashes and API failures cannot pass; no local receipt or design supplies authority.

5. Commit one canonical `path_entry` pipeline, consumed by every path-bearing check, explicitly C6/C10/C11/C12/C14 and C16 applicability. Keep the original enumerated path for reporting and filesystem operations, resolve that original to its real target for confinement and applicability, and normalize names to NFC only for comparison. Return the pipeline triple `(original enumerated path, resolved target, comparison key)` together; checks must not independently normalize a pathname before resolving it.

   Matching is identity-aware: a threat row or `allowed_files` entry covers a file only through that file's pipeline triple. The comparison key uses NFC, with case folding where the filesystem folds case. If two enumerated files share a key but have distinct filesystem identities (different resolved paths, or the same path with different byte names on a case- and normalisation-sensitive filesystem), refuse both with `path collision: <a> and <b> normalise to the same key` instead of crediting either.

   Apply it to scopes, threat-row path tokens, design paths, selector paths, applied-file classification and C14 file operands. Git refs remain refs. Preserve the grammar:
   - Repository-relative POSIX literal files, trailing-slash directories and globs; root files need no slash. Remove redundant `./` components consistently.
   - Component-local `*`, `?` and bracket classes; whole-component `**` spans zero or more components. Reject Git pathspec magic, exclusions, escapes and absolute paths after lexical cleanup; never interpret them as scope.
   - Parent traversal, including `../../x/*.py`, and escaping symlinks produce confinement findings, never silent skips. Check symlinked directory prefixes before full-match filtering.
   - Directory and child rows remain separate entries; match normalized path tokens to their own entry. Ancestor substrings do not violate C7b, but a row naming two entries does.
   - Enumerate regular files under fixed scope roots, including ignored and untracked files. Do not follow directory symlinks or scan Git administration. Reject internal directory aliases in literal and glob scopes, even with an explicit row; the index grants no exclusion.
   - Directory pruning compares normalized names against normalized scopes while confining the original directory. A decomposed-Unicode directory must not hide applied files or escaping symlinks.
   - Applied files include root `AGENTS.md`, `Makefile` and `.claude/skills/<name>/SKILL.md`; C12 requires concrete rows for applied wildcard matches, using resolved-target classification.
   - Fixture/evidence exemptions require confinement of the original path, real-target identity beneath the corresponding exempt root, and classification consistent with that exemption. Lexical prefixes or normalized aliases alone grant nothing; retain deterministic case-insensitive checks.

6. Retain C16 under D-024-30: a `security: true` orchestrator-side task explicitly references design 5.14 and has exactly one row for each item 0–10. Determine applicability from canonical scope entries and resolved targets, including covering globs and a literal file symlink into `scripts/orchestrator/`. Match item numbers distinctly, count every occurrence, reject omissions, duplicates and multi-item rows, and preserve non-applicable tasks.

7. Retain only the predecessor directory inventoried above, unchanged from `06ffefbc`; its task.md is historical data. Create this reset's own byte-identical dispatched copy and evidence in its allowed directory. Import or delete no earlier lineage directories. Exercise C2/C3 with the retained predecessor and own-copy rows; hidden predecessor edit scopes using `./` still fail C2. The complete changed-file list and reset lineage must pass regime-ci; no deferred disposition of applicable scope failures.

Retain all other C1–C15 behavior, C11 class selectors, confinement, non-execution and trusted-execution negative controls. Port no dependency on the two deferred scripts.

## Required regression fixtures

Keep the 16 a05 contract fixtures below and their historical behavioral reds at `7a201eab`; rerun every selector green on the final head. Valid controls assert the intended behavior, not an unrelated refusal.

| Behavior | Selector |
| --- | --- |
| Interpreter precedence and invalid-input refusal | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_interpreter_resolution_order` |
| Exact unchanged dispatch invocation without stripped variables | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_dispatch_env_i_invocation` |
| Failed C14 probe with matching stdout | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c14_rejects_failed_probe_with_matching_stdout` |
| Tokens preserved only in the intended child environment | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_gh_child_preserves_parent_tokens` |
| C15 canonical repository, host and SHA without invariants | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c15_uses_canonical_main_only` |
| C6 receipt/hash against the same canonical bytes as C15 | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes` |
| Glob grammar and Git pathspec rejection | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_distinguishes_globs_from_git_pathspecs` |
| Root literals and applied root-file coverage | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_covers_root_files` |
| Separate directory/child rows and combined-row rejection | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_separates_directory_and_child_rows` |
| Equivalent dot spellings | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_normalises_dot_spellings` |
| Traversal, escaping scope and symlink-prefix refusal | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_rejects_escaping_scopes` |
| Exempt symlink cannot hide an applied production file | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_symlink_to_applied_file_is_finding` |
| Deterministic case-alias refusal | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_case_alias_to_applied_file_is_finding` |
| Applied skill instructions, including untracked matches | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c12_covers_applied_skill_instructions` |
| C16 reference, omissions, duplicates and valid control | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c16_requires_reference_and_all_item_rows` |
| Reset-copy coverage and hidden predecessor scope refusal | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_reset_scope_rejects_hidden_predecessor_artifacts` |

One red-then-green regression per finding of the two security reviews is mandatory, with the finding ID bound to its selector:

| Finding or invariant | Selector |
| --- | --- |
| security:cedc7f5:1 — resolve original Unicode pathname | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_resolves_original_unicode_path` |
| security:cedc7f5:2 — reject internal directory aliases | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_rejects_internal_directory_alias` |
| security:cedc7f5:3 — count every item occurrence; reject combined rows | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_rejects_multi_item_rows` |
| security:06ffefb:1 — normalized pruning cannot hide files or escaping symlinks | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_prunes_with_normalised_directory_names` |
| security:06ffefb:2 — resolved literal alias triggers C16 | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_uses_resolved_literal_alias` |
| Enumerated, resolved and matched identities agree across pipeline consumers | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_canonical_path_pipeline_preserves_identity` |
| text-security:4a49ed9:1 input-validation — distinct-file collision refusal and single-file coverage | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_canonical_path_pipeline_rejects_normalised_collisions` |

Preserve the three cedc7f5 reds and their greens at `06ffefbc`; they stay green. The two 06ffefb findings and pipeline-invariant test must fail behaviorally at `06ffefbc` before the pipeline fix and pass after it. Add valid confined controls; preserve raw-path reporting and demonstrate name normalization never changes the target confined.

The collision regression plants both `scripts/café.py` (precomposed) and `scripts/café.py` (`e` followed by U+0301, decomposed) under `scripts/**`, with one concrete threat row. Where the filesystem keeps them distinct, expect the named collision finding and no coverage credit for either file. Probe and state the observed filesystem behavior; skip only the two-file case with a stated reason where name normalisation aliases them, rather than assuming behavior from APFS/HFS+ or the OS. A separate one-file case expects normal coverage and no collision, and runs even where the two-file case skips. Record the collision regression's behavioral red before its fix and green after it.

The dispatch fixture reproduces `env -i`, PATH/HOME/absolute UV_CACHE_DIR, optional LANG/LC_ALL, exported AGMSG_* and the existing pinned offline uv launch followed by `python -I <checker> --root <root> <task>`. Assert real arguments, environment and verdict; this proves checker compatibility only. Model Unicode/case distinctions deterministically on insensitive hosts and disclose unavailable native coverage.

## Commands

Use validated absolute, non-shim interpreter and uv bindings, isolated Python, offline dependencies and temporary absolute caches. Record tool paths, hashes and versions; do not trust a checkout executable, ambient .venv or caller Python startup state. The host-provisioned 3.12 floor is `$HOME/.local/share/mise/installs/python/3.12.15/bin/python3.12`; validate it before use.

Run each complete checker module with both Python 3.12.15 and the current Python 3.15.0 binding, expanding placeholders and recording the exact commands:

```
<absolute uv> run --no-config --no-project --offline --python <absolute interpreter> --with pyyaml python -I -m unittest discover -s tests/unit -p 'test_task_consistency_c11_c15.py' -v
<absolute uv> run --no-config --no-project --offline --python <absolute interpreter> --with pyyaml python -I -m unittest discover -s tests/unit -p 'test_task_checkers.py' -v
```

For individual selectors, use the recorded isolated bootstrap that inserts only the validated absolute test root; do not depend on importing an uninstalled tests namespace through CWD. An unavailable runtime or dependency is a blocked operation, not a red test.

## Check

Write regressions before fixes. Record checker revision/SHA256, regression-source SHA256, actual interpreter/version, expanded commands, complete stdout/stderr and exits for historical reds and final greens. Import errors, absent dependencies, missing tests, unrelated refusals and zero-test runs are not red proofs.

Run `make unit-test`, required formatting, changed-file R4 lint and relevant validators. Compare inherited failures against the unchanged base in the same environment; preserve their exact multiplicities, never label them green or repair outside scope. Do not run Bats locally; the orchestrator reads final-head GitHub Actions and returns the results before RESULT.

Paste mutation totals as `mutations=<observed> killed=<observed> survived=<observed>` with per-mutation outcomes. Retain the 28 prior controls and independently disable each new pipeline behavior; its named fixture must kill the mutant. Commit no mutants or mutation framework; unexplained survivors block completion.

The complete final diff has at most 440 changed lines outside `tests/` and `.orchestration/`, and at most 700 under `tests/`.
Measure with `git diff --numstat 60a6fb2b...<head40>`, substituting the validated full final head.
All production changes are in the one allowed checker. The cap attribution is a05's 396 changed source lines at 06ffefbc plus the pipeline draft's measured +24 = 420, with 20 lines of headroom to 440 under D-024-39; no further cap increase is authorized.

Count additions plus deletions for both source and tests, as regime-ci does. The held draft's tests are +682/-22 = 704 changed lines, so recover at least four lines within the 700 cap while retaining all required controls; 682 additions alone is not a passing total.
Paste the complete numstat, `git diff --name-only 60a6fb2b...<head40>`, per-file arithmetic and both totals in measure.md and RESULT. Do not hide runtime code in artifacts, remove defenses or change a lint baseline to fit.

The whole authored file, including its empty Checks block, is at most 260 lines and has exactly four allowed_files entries. The worker never edits the orchestrator's Checks content; a populated dispatch block is separately identified as appended metadata, never silently excluded from a claimed count.

Run the checker on dispatched bytes and record C14's warning without `--premises-sha`; authorized fixtures use their supplied trusted digest. Never invent dispatch authority from branch bytes or add shell support for authoring probes.

## Completion and evidence

Worker Playbook step 4 applies with this host's measured facts: Codex seats run without network since the daemon restart (D-024-36), so the worker commits locally, PONGs the full head, and the orchestrator transports it to PR #440 and reads CI for the worker; every other command runs inside the sandbox, and any refused command is reported as `AGMSG-PONG v1 status=blocked` with exact command, exit, output and boundary.

Do not retry a refusal through another tool, broader permission or sandbox escape. An orchestrator transport or CI read is not worker permission to leave the sandbox. Record unavailable live API validation honestly and retain local fake-API controls.

Commit report.md, validation.md, sandbox.md, learning.md, autoskill.md (status or not-used), measure.md, the byte-identical task.md and worker review evidence under this task's directory before RESULT. Verify with `git ls-files` that no required evidence remains untracked; this overrides generic untracked-artifact handoff. Codex plan/todo/learn worklogs remain uncommitted.

Use agent-side Crit data and a worker receipt in the allowed directory, with resolved records and the receipt's review_surface/reviewer/review_source/review_outcome binding; no browser, publication or human review request. Run `make require-crit-review` with the required evidence. Retain INV-6/S1 lineage accounting; repeated finding classes require a recorded re-plan, not private patch rounds.

The orchestrator transports every new committed head, checks final-head CI and performs Worker Playbook's bounded Bot procedure for the worker, returning exact observations. Fresh applicable CI follows an evidence-only push too. Keep the existing PR's English title/body current through the orchestrator; the worker never merges or edits canonical acceptance, decision or plan records.

Send `AGMSG-RESULT v1 status=ready_for_review` only after required checks pass. Include full head/base, branch, PR #440, task-copy SHA256, changed-file inventory, retained predecessor directory, final numstat/totals, selectors, historical and new red/green counts, mutation outcomes, CI/Bot observations, proposed feedback dispositions and every artifact path. Report `cost:` with observed figures or `n/a`.

After final-head CI and the required security review, the orchestrator follows Orchestrator Playbook step 10: complete feedback sweep, dispositions, task audit, acceptance record and gate with `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE`. Neither a05 review nor previous CI approves this head.

Deferred checks and changes: generator, plan checker, workflows, dispatch/resolver implementation, deployment and local Bats.
Residual risk: unchanged parent execution, shared cache, credentials and same-UID interference remain; checker fixtures establish no host isolation.

## Checks (pasted by the orchestrator before each send)

```
pasted 2026-10-20T08:09Z before send 1 to a012 (Codex, worker-g): reset of dotfiles-T133-task-generator-plan-check-a05-checker after INV-6 S2 and the cap stop (D-024-39; a05 counters: task=dotfiles-T133-task-generator-plan-check-a05-checker tasks=3 amendments=2 questions=2 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-20T03:20:31Z..none (-) source=liv); C-80 of this text: 4a49ed9 incorrect (1 P2: NFC collision of two distinct files) -> amendment 1 (identity-aware matching, collision refusal) -> 73ac933 correct; task-consistency-check.py OK; SECRET_PATTERN 0; home paths 0; 244 lines (self cap 260)
PR #440 continues on tools/task-generator-plan-check-a05-checker from head 06ffefbc with your uncommitted pipeline draft as this round's content (source cap 440 = 396 at 06ffefbc + the pipeline's measured +24 with headroom; tests 700); the Codex seats have no network (D-024-36): commit locally, PONG the head, the orchestrator transports it and reads CI; the six RegimeCiTest reds stay until #441 merges; task SHA256 in the AGMSG-TASK line, computed over these final bytes
```
