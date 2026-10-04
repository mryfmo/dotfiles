# Report: dotfiles-T93-gate-masked-feedback-bodies-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `fix/gate-masked-feedback-bodies` from `origin/main` 65915b93.
- **task_rev:** `sha256:366944e4…1e81`, matched.
- **PR:** #251, https://github.com/mryfmo/dotfiles/pull/251.
- **Commits:**
  - `7d7a9777`: the change.
  - `935399c0`: placeholder handling, from my own equivalence check.
  - `4db6083a`: Codex P2 4176779660.
  - `63e8fd90`: Codex P2s 4176797732 and 4176797738. This moved the fix to the masker side.
  - `10c03df2`: `gh pr update-branch` (main f2b5c115).
  - `dd155f2b`: Codex P2 4176920525.
  - Revise round 1:
    - `56546541`: audit items 1-3.
    - `c70878d4`: merge of main febd0cb7.
    - `62cf4aa9`: Codex P2 4177133524.
    - `ba920163`: merge of main 6de95167.
    - `09784303`: Codex P2 4177181654.
    - `aa5b061e`: merge of main c6b348ba.
  - Revise round 2:
    - `254d9ebf`: audit items 1-2.
- **Final head (revise round 2):** `254d9ebf`. Round 0 ended at `dd155f2b` and round 1 at `aa5b061e`. CI, branch and bot state are in the validation file's revise sections.
- **Status:** ready_for_review.

## 1. What changed (as of the final head)

- **`scripts/require-crit-review.py`:**
  - `validator()` loads `validate-agent-assets.py` by path from the guard's own directory (cached).
  - `feedback_key(item, masked=False)` identifies an item by source, url, level, path, line and body. With `masked=True`, only the body and the path are masked with `mask_secret_matches`; source, url, level and line stay byte-exact.
  - `missing_feedback()` matches each collected item against a saved item whose key equals the verbatim key or the masked key, consuming the saved items as a multiset. Saved items are never normalized, so only redactions the masker actually applies are ignored.
  - The docstring says why a masked body or path is accepted.
- **`scripts/validate-agent-assets.py`:**
  - **`--mask-secrets` (a deviation beyond the task's four items, forced by Codex P2 4176797738):**
    - A `.json` file that parses is masked per key and string value through `mask_members` and `mask_json_strings`, then rewritten as `json.dumps(indent=2, ensure_ascii=False)`, the `pr-feedback.py` layout. Members are masked as they are parsed, so an earlier duplicate member is counted before `json.loads` drops it.
    - Two distinct keys that mask to one name fail with the path and both original keys, exit 1, and leave the file unchanged.
    - Any other file is masked as text, as before; `herdr-agents --audit` passes only Markdown. No CLI flag was added.
  - **Secret scan:** a file that parses as JSON is scanned per object key and string value (`json_strings`, duplicate keys included), and any other file as whole text.
  - **`read_scannable_text()`:** under `.orchestration/`, a NUL byte fails first with the path and its offset, and a UTF-16 file fails as non-UTF-8 evidence, both before any decode. Other files are unchanged: UTF-16 BOM text is decoded, and NUL binaries are skipped.
  - Before the change, no `.orchestration` file held a NUL (0 of 1852 committed, 0 on disk) or was UTF-16 (0 of 2195 on disk). These are Python scans with a positive control, and the commands are in the validation file.
- **Rules:** one sentence each in `pr-integration.md` and the Codex `PR 統合` gate bullet. The evidence JSON may be masked with `--mask-secrets`, which masks its keys and string values. The guard identifies an item by its source, url, level, path, line and body, and accepts a body or path that is verbatim or exactly that masked form.
- **Tests:**
  - **Gate:** `test_pr_feedback_bodies_are_compared_after_secret_masking` and `test_pr_feedback_matches_a_masked_path_but_not_an_edited_one`. A masked path is accepted; an edited path and a masked url are rejected.
  - **Validator, secret scan:**
    - `test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries`;
    - `test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset`;
    - `test_secret_scan_reads_json_per_key_and_string_value`.
  - **Validator, masking:**
    - `test_masks_json_string_values_and_keeps_the_document_parseable`;
    - `test_masks_an_earlier_duplicate_member_so_the_scan_passes`;
    - `test_a_masked_key_collision_fails_and_leaves_the_file_unchanged`.
  - Each round's new tests fail against the previous head; the runs are in the validation file. On the final head, `make unit-test` passes with 783 tests, and `make validate-agent-assets` passes.

## 2. Why the design moved to the masker

The first design masked decoded bodies on both sides with the validator's masker, as the task text asked. But `--mask-secrets` masked the serialized JSON text, and `pr-feedback.py` writes each body as one escaped JSON line. Masking the file and masking the decoded body then disagree:

- **Placeholders:** the file masker strips them from a whole body line, but only when that line matches. I found this myself (fixed in `935399c0`); `4db6083a` then answered P2 4176779660.
- **Escaped quotes:** a quoted assignment is never masked in the file, while the gate masked the decoded body, so a different value passed. This is P2 4176797732.
- **Broken JSON:** a body ending in an assignment prefix let the text pattern consume the closing quote and the next field. This is P2 4176797738, and it means the workflow the PR's own rule sentence advertises corrupted the evidence.

Masking the decoded string values makes a saved body exactly `mask_secret_matches(live body)` by construction. The gate then needs no emulation, and the earlier normalization was removed. The scratch equivalence check (verbatim in the validation file) covers seven bodies, including both P2 bodies. The gate accepts every saved item and rejects an unmasked assignment with another value.

**Former ceiling, fixed in revise round 1 (`56546541`):** a string value that ends in an assignment prefix, followed by the next JSON field, still matches the scan across the serialized text. The scratch check shows the only match starting in that body and spanning a newline. The repository scan then fails on that file, so it fails closed and needs a hand edit. It is never a bypass.

## 3. Trust boundary

The gate still runs the GitHub base SHA's `pr-feedback.py`, so the PR cannot swap the collector. The masker comes from the local `validate-agent-assets.py`, which is the same trust level as `require-crit-review.py` itself (both run from the local checkout). A PR that could weaken the masker could equally edit `feedback_key`, so no new boundary is introduced.

## 4. Codex bot and threads

| Head | Result |
|---|---|
| `7d7a9777` | 👍 at 08:28:26Z, seen by my poll. The reaction list now shows only the later 👍, so the bot seems to replace its reaction per head. |
| `935399c0` | P2 4176779660, "Preserve placeholder-only text in evidence comparisons": `fixed:4db6083a`. That commit strips placeholders only from a body that holds a match. `63e8fd90` then dropped body normalization entirely, and the case stays rejected by test. |
| `4db6083a` | P2 4176797732, "Match the file masker's serialized-body semantics": `fixed:63e8fd90`. Saved bodies are no longer normalized, and only verbatim or exactly-masked bodies match. |
| `4db6083a` | P2 4176797738, "Keep masked PR-feedback JSON parseable": `fixed:63e8fd90`. `--mask-secrets` masks JSON per string value and keeps the document parseable. |
| `63e8fd90` | No review of its own; `gh pr update-branch` superseded it about 5 minutes after the push. |
| `10c03df2` | P2 4176920525, "Match redacted feedback paths as well as bodies": `fixed:dd155f2b`. At `dd155f2b` the masked key masked every string field; revise round 1 narrowed it to body and path. |
| `10c03df2` | P2 4176920521, "Keep harmless assignment suffixes from blocking masked evidence": `fixed:56546541` in revise round 1. The secret scan reads JSON per key and string value. The round-0 proposal below is withdrawn. |
| `dd155f2b` (final) | 👍 at 09:39:44Z, with no review comment. |

*(Withdrawn in revise round 1; the audit rejected it, and `56546541` fixes the thread.)* Proposed `not-applicable` for 4176920521. This is the known ceiling in section 2 and is fail-closed. A JSON string value ending in an assignment prefix, followed by the next field, matches the repository scan across JSON syntax, so CI rejects the evidence file. It never lets a secret or an altered item through. Fixing it would make the repository-wide `validate_no_obvious_secrets` JSON-aware. That changes what the scan sees for every committed JSON file, which is beyond T93's masking and NUL items. The orchestrator can hand-edit that body, or open a follow-up task for a JSON-aware scan.

I did not reply to or resolve any thread.


## 5. Notes

- **Test variable renamed.** The test's first draft assigned the key-shaped literal to a variable named `token`, and the assignment tripped the token-assignment pattern. It was renamed to `key_shaped` before the first push.
- **`ruff check`.** It reports the same 15 existing findings in these four files, both on `origin/main` and on `4db6083a`; I did not re-count on the final head. CI runs only `ruff format --check`, which passes.
- **T71 artifact correction.** validation:125 was narrowed to lexical path validation, and the T71 ACCEPTANCE acknowledged it at 08:08:21Z. Per that note, I'll report future corrections inside the next RESULT or a PONG.
- **Restored a script after a failed capture.** A zsh `$ref:scripts` history-modifier expansion aborted one comparison capture after it had overwritten `scripts/require-crit-review.py` with the base version. I restored it from the saved copy, checked it with `git diff --quiet HEAD -- scripts`, then repeated the capture with `${ref}`.

## Revise round 1 (task-level audit of `dd155f2b`: incorrect)

The commits are `56546541` (items 1-3 with tests) and `62cf4aa9` (Codex P2 on `c70878d4`). Two `gh pr update-branch` merges followed, `c70878d4` (main febd0cb7) and `ba920163` (main 6de95167, #252). `09784303` then answers the Codex P2 on `ba920163`, and `aa5b061e` merges main c6b348ba (#254).

1. **Identity fields:** `feedback_key(masked=True)` masks only `path` and `body`; source, url, level and line stay byte-exact. The masked-path test gains "url masked with `--mask-secrets`", which the gate rejects (rc 1).
2. **JSON-aware repository scan:**
   - `validate_no_obvious_secrets()` scans a file that parses as JSON per object key and string value, via `json_strings()`. That reads `object_pairs_hook=tuple`, so a duplicate key's earlier value is scanned too; any other file keeps the whole-text scan.
   - A body ending in an assignment prefix no longer matches across JSON syntax, so thread 4176920521 is `fixed:56546541`.
   - The per-string scan is also stricter in one way: it now sees a quoted assignment that JSON escaping used to hide.
   - All 85 committed `.orchestration` JSON files pass. One untracked file in the main checkout is flagged: the orchestrator's `dotfiles-T93-gate-masked-feedback-bodies-a01-pr-feedback.json`, whose bot bodies quote assignments. Run `--mask-secrets` on it before the boundary commit (the documented workflow); the gate still accepts the masked body.
3. **Object keys:** `mask_json_strings` masks dictionary keys. A ponytail comment notes the known ceiling: two key-shaped keys masked to one name keep the last value.
4. **NUL evidence:** the validation file now has the pre-change count and the positive-control run. That is the T93 base `65915b93` (1852 committed `.orchestration` files, 0 with NUL) plus the main checkout on disk (0 with NUL). It also shows the discarded `grep -P` probe, which misses the control (rc 1).

**Codex P2 4177133524 on `c70878d4`** ("Preserve duplicate JSON members while masking"): `fixed:62cf4aa9`. `--mask-secrets` now masks every member as it is parsed (`object_pairs_hook`), so a secret in an earlier duplicate member is counted and is gone from the rewritten file. The earlier duplicate is dropped, as `json.loads`, and so the gate, reads the file. `test_masks_an_earlier_duplicate_member_so_the_scan_passes` checks this.

**Codex P2 4177181654 on `ba920163`** ("Compare all unmasked feedback fields"): `fixed:09784303`. The cause was my rule wording in `62cf4aa9`, "every other field must match exactly", which overclaimed. The guard has always identified an item by source, url, level, path, line and body; that predates this PR, and the task kept it. The sentences now name that identity.

Widening the identity to `author`, `bot`, `check`, `resolved` and `outdated` would change the gate's evidence logic, which the task forbids. Thread state such as `resolved` and `outdated` also legitimately changes between collection and the gate run. If the orchestrator wants those fields bound, that is a follow-up task.

**Tests:**
- New: `test_secret_scan_reads_json_per_key_and_string_value` covers the across-fields body passing, a key-shaped key, a duplicate key's earlier value, an escaped quoted assignment, and a non-JSON file keeping the text scan. The mask test gains a key-shaped key; the masked-path test gains the url case; and the duplicate-member mask test is new.
- These fail against `dd155f2b` (3 failures, 1 error) and against `c70878d4` (the duplicate case).
- `make unit-test` on `aa5b061e` passes with 781 tests, and `make validate-agent-assets` passes.

**Threads on the final head:**
- 4176779660: `fixed:4db6083a`
- 4176797732: `fixed:63e8fd90`
- 4176797738: `fixed:63e8fd90`
- 4176920525: `fixed:dd155f2b`
- 4176920521: `fixed:56546541`
- 4177133524: `fixed:62cf4aa9`
- 4177181654: `fixed:09784303` (wording; widening the identity is out of scope)
- 4177248224 (on `aa5b061e`, "Support masked feedback URLs"): proposed `not-applicable`. It asks the gate to accept a masked `url`, which revise item 1 of the task-level audit explicitly rejects ("source, url and level stay byte-exact"); `dd155f2b` did exactly that. The case fails closed: a check-run or status url holding a key-shaped token makes either the scan or the gate reject the evidence, never accept an altered item. The orchestrator can hand-mask such an item or re-task if it decides urls may be masked.

The orchestrator's own replies (41769973xx/41769974xx/41769975xx/41769976xx) are not mine to answer. I did not reply to or resolve any thread.

## Revise round 2 (task-level audit of `aa5b061e`: incorrect)

The fix is commit `254d9ebf`. `main` had not moved, so no update-branch was needed.

1. **NUL before the UTF-16 decode:**
   - `read_scannable_text()` used to decode a UTF-16 BOM file before the NUL check, so a BOM-prefixed `.orchestration` artifact bypassed the scan.
   - Under `.orchestration/`, a NUL byte now fails first, with its offset, and a UTF-16 file fails even with no NUL byte; evidence is UTF-8 text. Other files are unchanged.
   - Test: `test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset`. A BOM-prefixed fixture holding a key-shaped string fails with offset 3, and a NUL-free UTF-16 fixture fails as UTF-16.
   - Read-only check: 0 of 2195 files in the main checkout's `.orchestration` start with a UTF-16 BOM.
2. **Masked key collision:**
   - `mask_members()` now raises `MaskedKeyCollision` when two distinct original keys mask to one name. `--mask-secrets` prints the path and both original keys, exits 1 and leaves the file unchanged. A repeated identical key still keeps its last value, as `json.loads` reads it.
   - Test: `test_a_masked_key_collision_fails_and_leaves_the_file_unchanged`.
   - Note: as the directive asks, the error message prints both original (key-shaped) keys to stderr. That exposes them on the terminal of whoever runs the masker on their own file.
3. **Report:** section 1 and the header now describe the final state: only body and path are masked, and the test count is 783.

Both new tests fail against the `aa5b061e` validator (2 failures). On `254d9ebf`, `make unit-test` passes with 783 tests and `make validate-agent-assets` passes.

**Threads:** unchanged from round 1. 4177248224 remains proposed `not-applicable`, because a masked url contradicts round-1 item 1. Any new bot finding on the final head is listed in the validation file.

## CompactionDB

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T93 (orchestrator 2026-10-04): the integration gate compares PR-feedback bodies after the validator'"'"'s secret masking, so saved evidence may be masked; the secret scan fails, rather than skips, an `.orchestration` text file that contains a NUL byte.'
2c104580-db1d-4867-9777-cb115fb37676
[exit 0]
```

[memory:decision] dotfiles-T93 (orchestrator 2026-10-04): the integration gate compares PR-feedback bodies after the validator's secret masking, so saved evidence may be masked; the secret scan fails, rather than skips, an `.orchestration` text file that contains a NUL byte.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T93-gate-masked-feedback-bodies-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T93-gate-masked-feedback-bodies-a01.md`
- learning: `.orchestration/learning/dotfiles-T93-gate-masked-feedback-bodies-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T93-gate-masked-feedback-bodies-a01.md`

cost: n/a (no subagents, no model-driven runs; two advisor consultations; the runtime does not expose session totals).
