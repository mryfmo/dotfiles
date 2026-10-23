# Final independent revision review

No remaining substantive finding was identified in the reviewed implementation batch. R1, R2 and the R4 security addendum are verified resolved on the exact bytes below. All preceding reviews and evidence remain historical; this record does not rewrite their findings or extend their hash bindings.

This is independent agent-side process evidence, not reviewer authentication, final-head task audit, CI certification, owner acceptance or merge approval.

## Bound final bytes

| File | SHA-256 |
| --- | --- |
| `scripts/orchestrator/task-consistency-check.py` | `f43de893ab5f7d3d68bac6be5cf8c04c6e33d4303bd38e6eab56dc2726880800` |
| `tests/unit/test_task_consistency_c11_c15.py` | `be102aab7c88dc74f3be5019005992f53485b0a8ed3addcb8abb4decb338dbe1` |
| `tests/unit/test_task_checkers.py` | `20eff6f4cf0cbdb55da3f1265edaec6a3479f238a08a7ef36abfe03a8968e99f` |
| a06 `task.md` | `b9e04cb9b2fdb9d4fea9f8f93eec3a88de55b72d5114797103c98e9784b572af` |

These bindings were recorded before and after the independent tests and remained unchanged.

## Findings verified resolved

- **R1 — cache compatibility, lines 37 and 138–143.** Cache absence no longer fails at import. Launch validates an explicitly supplied cache, preserves an absolute supplied value, and uses its private temporary directory for the child cache when unset. Independent tests verified fallback path absoluteness and cleanup, relative-value refusal, unchanged dispatch invocation, and exact supplied-cache forwarding to the fake-gh child. Executable validation, token environment forwarding and sanitized Git launch controls remain.
- **R2 — resolved-file classification, line 481.** The applied-file predicate uses the already-confined original operand's resolved target. The deterministic fixture forces the NFC alternate's existence/file predicates false, while requiring the one-file wrong-target case to fail without relying on a collision finding. Collision registration still uses enumerated names. Distinct-target and same-target collisions, valid one-file coverage and overlapping-scope controls passed.
- **R4 / `security:b8bf806:1` — canonical approval binding, lines 177–180, 220–223 and 352–358.** The design string retains original Unicode spelling for shared C6/C15 canonical-byte reads. API path validation no longer replaces that spelling with NFC; only POSIX dot/separator cleanup precedes percent encoding. Directory traversal retains raw child paths and uses normalization only for the boundary comparison. The real-CLI fake-API regression rejected an NFD design supplied with the separate NFC file's receipt/hash and omitted assigned invariant, rejected a missing NFD file despite an existing NFC counterpart, and accepted the correct NFD receipt/hash/invariant. The raw-NFD directory-child read also passed.

Read the entire canonical `security-b8bf806.md.last.md` addendum, the revision state in `report.md` and `validation.md`, and the final diff against `b8bf806655496b7a897aea25e1b43319095fac23` with connected checker code and fixtures. Preserved original-path confinement, target identity, collision refusal, raw diagnostics, fixed canonical host/repository/SHA, token forwarding and C14's dispatched-byte authorization. The API fixture now decodes percent-encoded request paths and uses raw Unicode dictionary keys; it models URI transport without equating distinct Git names.

## Independent execution

`revision1-final-independent-commands.json` stores the exact expanded argv arrays, cwd, relevant environment, executable hashes, before/after file bindings, output filenames and actual exits. Each command uses the validated absolute native Python binary with `-I`, inserts only the absolute test root, and runs existing temporary-repository CLI fixtures. The driver exited 0 after both child processes succeeded and all hashes stayed unchanged.

| Runtime | Result | Actual exit | Complete stdout/stderr |
| --- | --- | --- | --- |
| Python 3.15.0 | 16 tests, OK, one native collision subtest skipped | 0 | `revision1-final-independent-3.15.0.log` |
| Python 3.12.15 | 16 tests, OK, one native collision subtest skipped | 0 | `revision1-final-independent-3.12.15.log` |

Methods of `TaskConsistencyC11C15Test`:

- `test_private_cache_when_unset`
- `test_dispatch_env_i_invocation`
- `test_c6_receipt_uses_canonical_design_bytes`
- `test_c15_uses_canonical_main_only`
- `test_canonical_path_pipeline_rejects_normalised_collisions`
- `test_canonical_path_pipeline_preserves_identity`
- `test_checker_rejects_untrusted_bindings_and_git_configuration`
- `test_gh_child_preserves_parent_tokens`
- `test_path_grammar_rejects_escaping_scopes`
- `test_c10_confines_original_unicode_script_paths`
- `test_c12_classifies_backslash_filenames_from_resolved_ancestry`
- `test_path_grammar_separates_directory_and_child_rows`
- `test_security_c12_rejects_internal_directory_alias`
- `test_security_c16_rejects_multi_item_rows`
- `test_reset_scope_rejects_hidden_predecessor_artifacts`
- `test_security_c12_prunes_with_normalised_directory_names`

Only the native two-distinct-file NFC/NFD collision subtest skipped, because this filesystem observed the spellings as aliases. All deterministic absent-alternate, wrong-target, distinct-target and same-target cases ran. These are not native Linux test results.

## Consolidation and complete-cap verification

Directly inspected every fixture consolidation and subsequent raw-API/observer edit. Independently reversed the 29 documented consolidation lines in the current final test text, while retaining subsequent changes, then compared all assertion-call ASTs as multisets: all 104 calls and their multiplicities were identical. The result is saved in `revision1-final-independent-consolidation.json`.

The original consolidation record describes an intermediate snapshot. An initial attempt to reconstruct it by removing only the dispatch observer failed its evidence-association assertion because the later raw-API and directory-child changes also intervened; this was not a checker test failure. The final independent check explicitly uses current `be102aab` bytes and makes no historical-snapshot equivalence claim.

`git diff --numstat 60a6fb2b -- scripts/orchestrator/task-consistency-check.py tests/` exited 0:

```text
419 27 scripts/orchestrator/task-consistency-check.py
6   5  tests/unit/test_regime_ci.py
35  22 tests/unit/test_task_checkers.py
652 0  tests/unit/test_task_consistency_c11_c15.py
```

The complete fixed-base totals are **446 production** and **720 tests**, including the 11 upstream test lines. These fit the task's 450/720 caps without an inherited-line exclusion. The earlier 731-line limitation is resolved on these bytes.

## Remaining process limits

The corrected R3 narrative withdraws the previous misattribution of the six R1 failures. This reviewer does not certify the parent's full-module, historical-red, mutation or complete candidate-minus-base runs. Actual final-head Linux CI, Bot/security/task-audit results, feedback dispositions, owner acceptance and integration gates remain separate requirements. No RESULT or merge readiness is implied before the root's explicit CI-green instruction.

No source/test edits, network, browser, Bats, commit, gate or integration actions were performed. Parent execution, credentials, caller-supplied shared caches and same-UID interference remain documented residual risks.

Verdict: correct
