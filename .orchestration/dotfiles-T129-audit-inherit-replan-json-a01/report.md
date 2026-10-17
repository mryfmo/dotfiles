---
task_id: dotfiles-T129-audit-inherit-replan-json-a01
seat: claude-standard-dot-a006
branch: tools/audit-inherit-replan-json
base: 35ab0e95
code_commit: ec4ba99d
fix_commit: f2c3bf9d
revise1_commit: 8bdecb45
task_sha256: 7ea5564f6a3f8e9054a55250ff53a35d72b0445be7841981badfb6cb70021c1d
---

# Report: dotfiles-T129-audit-inherit-replan-json-a01

- Seat: `claude-standard-dot-a006` in `.claude/worktrees/worker-f`, on a fresh branch `tools/audit-inherit-replan-json` from `origin/main`. The branch was cut at `a0e8b8ad` and, before any push, rebased onto `35ab0e95` (#385, `.orchestration` files only), so the PR's base is the current `main`. The PR #378 branch `tools/chain-glue-finish` stays in the worktree, committed and pushed.
- Task file: sha256 `7ea5564f…`, copied byte-identical to `.orchestration/dotfiles-T129-audit-inherit-replan-json-a01/task.md`; the task-consistency check passes (validation §1). Premises 1 to 4 and 6 replay equal; premise 5 prints 3 on the current `origin/main`, 4 at `a0e8b8ad` (§2). No question and no amendment.

## What landed

| File | What it does |
|---|---|
| `scripts/orchestrator/chain-integrate.sh` (+26 −4) | Before the audit step: when the head's first parent has both receipt files (`<task>-audit-<parent sha7>.md` and its `.last.md`), its second parent is an ancestor of `origin/main`, and the PR patch-id is unchanged (`git diff-tree -p $(git merge-base origin/main <rev>) <rev> \| git patch-id --verbatim`, for the parent and the head; `--stable` until the Bot's fix round), both files are copied under the head's sha7 with a first line `inherited-from: <parent sha7>`, the step logs `audit inherited from <parent sha7>` and the verdict line is the inherited summary's last line. Otherwise `orch-audit.sh` and the review-worktree checkout run as before. The refusal of a head that already has its own receipt stays. |
| `scripts/require-crit-review.py` (+20 −13) | `replans` joins `RECORD_KEYS`. A `replans` that is not an object of objects keyed by class slugs is refused as `malformed block: replans must be …`. S1 passes for a class at the limit when `replans[<class>]` holds `specification`, `design`, `implementation` and `verification` as non-empty strings (`replan_complete`), else `S1: <class> at <n> rows without a re-plan (C-59)`; the body-line parse and its tokenizer comment are gone. `swept_finding_ids` keys an audit's findings under the sha7 of a first line `inherited-from: <sha7>` when the summary has one, else under HEAD's. |
| `scripts/orchestrator/acceptance-front-matter.py` (+11 −3) | Keeps a `replans` object through the block rewrite and writes `{}` when there is none. A `replans` that is not an object, or an entry whose key is not a class slug or whose value is not exactly the four keys as non-empty strings, exits 2 (`parser.error`) naming `replans` or `replans.<class>`, before anything is written. |
| `scripts/regime-counters.sh` (+8 −9) | `re-plan=present` when `$rec.rec.replans[<class>]` is an object with the four keys as non-empty strings (jq), else `missing`; the body capture and scan are gone, and the header says so. |
| `tests/fixtures/gate-evidence/acceptance-s6-present.md` (+12 −3) | Its re-plan line moved into the block as `replans`. Prettier then rewrapped the `searches` line, whose trailing comma took it past the width; the content is the same. |
| Tests (+190 −74 in four modules) | The five named tests and the edits item 3 lists, below. |

## The tests, by closed row

| Closed row | Test |
|---|---|
| chain-integrate.sh | `test_integrate_inherits_the_audit_across_an_update_branch_only_head`. Real git in the module's temporary repositories. P is the PR head with stub receipt files; M moves main. The positive head merges M into P with no other change: the two patch-ids are equal, the stub `orch-audit.sh` records no call, both files exist under the head's sha7 with the marker first, the log holds `audit rc=0: audit inherited from <P7>`, and the last line carries the inherited verdict. The negative head has the same two parents and also edits `b.txt` in the merge: the patch-ids differ, the stub records one call, and no file exists under its sha7. Since the fix round, a merge with the same parents that only indents `b.txt` also runs the audit (the patch-ids differ under `--verbatim`). A last head merges a newer main into the positive head: it inherits again and keeps `inherited-from: <P7>`, one marker only. |
| require-crit-review.py | `test_s1_replan_is_read_from_the_record_block_json`: three rows of one class with the object passes; a body line alone and a blank part refuse with the S1 message; a list and an entry that is text are malformed blocks. `test_s6_reads_an_inherited_audit_s_ids_under_the_parent_sha7`: a summary whose first line is the marker and whose body has two findings passes S6 with ledger rows `audit:<parent sha7>:1` and `:2`; rows under the head's sha7 alone are refused as `S6: ledger lacks audit:<parent sha7>:1, audit:<parent sha7>:2`, exactly two, so the marker is not a finding. |
| regime-counters.sh | `test_s1_replan_token_comes_from_the_record_block_json`: present with the object, missing without it, and missing with a body line alone. |
| acceptance-front-matter.py | `test_front_matter_keeps_and_validates_the_replans_object`: written `{}` when absent, kept through a rewrite, exit 2 naming the key for a list, a missing part, an extra part, a blank part and a key that is no slug, the record unchanged each time. |

The existing tests changed exactly as item 3 lists. In `tests/unit/test_require_crit_review.py`, `write_record` writes `replans` for each class at three rows (an explicit `replans` field, or `None`, wins), and a helper `rewrite_replans` sets the block's `replans` for the migrated tests. `test_s1_class_at_three_without_a_replan_line_is_refused`, `…_with_all_replan_words_is_accepted` and `…_with_a_missing_replan_word_is_refused` became `test_s1_class_at_three_without_a_replans_object_is_refused`, `…_with_the_four_keys_is_accepted` and `…_with_a_missing_key_is_refused`; `test_s1_replan_words_are_ascii_letter_runs` is removed. In `tests/unit/test_regime_counters.py`, `s1_record_lines` takes `replans`, `test_s1_reports_replan_present_for_the_class` and `test_s1_reports_replan_missing_without_the_four_keys` (renamed) read the object, `test_s1_replan_words_are_ascii_letter_runs` is removed, and `test_s1_excludes_advisory_p2_at_three_rows` passes the object instead of the empty body. Each module also gained a `REPLAN` constant.

Red and mutants: the five new tests fail on `origin/main`'s four scripts (validation §4: five failures, one error). Nine mutants, each caught by its test, then a passing baseline (§6): the patch-id comparison dropped, a parent's marker not kept, the marker ignored by S6, S1 taking any entry, the malformed-block check dropped, the counters reading no `replans`, the counters taking any part, the writer taking extra parts, the writer writing no `replans`. The fix round adds a tenth, `--verbatim` back to `--stable` (§8).

## CI and the Bot

- **CI on `c1011dfa`:** the 12 check runs passed, with CodeRabbit and GitGuardian.
- **The Bot's first review** (`5557556989` on `c1011dfa`, 11:25:10Z, after `gh pr ready` at 11:23:18Z; its security review found nothing) left two threads:
  - **P1 `4302490292`** (`chain-integrate.sh:180`), "Use a whitespace-sensitive comparison before inheriting audits": `fixed:f2c3bf9d`, the one fix round. `git patch-id --stable` strips whitespace, so a merge whose conflict resolution only re-indented a line kept the parent's id and inherited its audit. `--verbatim` keeps whitespace in the id, and the inheritance test gains an indentation-only merge, which now runs the audit (validation §8: red on `ec4ba99d`'s script, a tenth mutant).
  - **P2 `4302490297`** (`require-crit-review.py:803`), "Reject every malformed replan entry in the gate": proposed for the orchestrator, not changed here. The gate checks only that each entry is an object, as the reading below explains, so an incomplete entry below the threshold or an entry with extra keys passes it while the writer refuses both. A small fix within `allowed_files` makes the gate's shape check the writer's (exactly the four keys, each a non-empty string), which moves an incomplete entry at the threshold from the S1 refusal to the malformed-block refusal and changes one assertion of `test_s1_class_at_three_with_a_missing_key_is_refused`; that is a C-50 revise round if the orchestrator sends one, otherwise advisory, owned by `dotfiles-T129-audit-inherit-replan-json-followup-a01`.
- **The re-review** after the fix round: `@codex review` at 11:45:16Z; the Bot answered with issue comment `6233545017` on `199afeaa` at 11:50:41Z, "Didn't find any major issues", an issue comment rather than a review object. CI on `199afeaa`: 11 check runs passed, with CodeRabbit and GitGuardian.
- **Revise round 1** (ACCEPTANCE `status=revise`, bus 2026-10-17T12:13:03Z, C-50, the second fix round of INV-6) took the P2 `4302490297`: `fixed:8bdecb45`. The gate's malformed-block check holds every `replans` entry to the writer's rule, exactly the four keys, each a non-empty string, whatever the class's row count, so an incomplete entry below the threshold and an entry with extra keys are refused as a malformed block. An incomplete entry at the threshold is now that refusal too, not S1's, so two assertions moved: the one of `test_s1_class_at_three_with_a_missing_key_is_refused` the ACCEPTANCE names, and the blank-part case of this PR's own `test_s1_replan_is_read_from_the_record_block_json`, which asserted the S1 message. New: `test_a_malformed_replans_entry_is_refused_at_any_threshold` (an incomplete, a keyless, a non-string and an extra-key entry for the class with one ledger row, and an extra-key entry at three rows: each a malformed block; both entries complete: accepted), red on `199afeaa`'s gate (validation §9). Twelve mutants, each caught. The writer is unchanged. The Bot's review of the new head and CI are in the RESULT.

## Readings, declared

- **Which refusal for an incomplete entry.** Item 2 gives the S1 refusal for a class whose entry lacks a key and `malformed block` for a `replans` that is not an object of objects. Round 1 read that as a shape-only malformed check in the gate, with the four keys in S1; the Bot's P2 `4302490297` and the orchestrator's revise round replaced it: since `8bdecb45` the gate holds every entry to the writer's rule, so S1's own refusal is left for a class at the threshold with no entry.
- **A chain of inheritances.** When main moves again after an inherited head, the next update-branch head's first parent is the inherited head, whose receipt starts with the marker. The copy keeps that marker instead of prepending its own, so the ids stay those of the head the audit ran on, which the ledger rows carry. Without this, the gate would ask for `audit:<inherited head>:<n>` rows that do not exist.
- **The patch-id fails closed to a fresh audit.** Both ids are computed outside the `if` condition, where errexit is suspended, and a failure is an empty id; an empty id never matches, so an empty PR diff or a failed computation runs the audit. The detection runs git in the main checkout, which holds `refs/remotes/pr/<pr>` and the fresh `origin/main`.
- **The marker is read from the summary's first line**, as item 1 specifies. An auditor's own final message could also begin with such a line; the effect is limited to which sha7 the ledger rows must carry, the verdict and the `audit_findings` count are read as before, and the copy is written only by `chain-integrate.sh`. Recorded as a residual, not changed.
- **The test environment.** This host's global git config signs commits with a key that is absent and sets no `init.defaultBranch`, so the gate suite's `setUp` commit fails and 132 of its tests fail on an unmodified `origin/main` too; the Check ran with `GIT_CONFIG_*` equal to CI's settings (validation §7). The whole suite has 68 failures and 10 errors in six modules this task does not touch, identical on `origin/main`.
- **Lint.** `ruff check` reports I001, FURB167 and UP022 in `scripts/require-crit-review.py` and I001 and UP022 in its test module; `origin/main` reports the same, and CI runs `ruff format --check`, which passes.

## Known gaps, named

- **Three records on `main` carry a `re-plan:` body line** (premise 5 now counts 3: `dotfiles-T128-project-map-pane-open-a01-followup-a01.md`, `dotfiles-T128-s1-replan-gate-a01.md`, `dotfiles-T128-seat-launch-args-a01.md`). Until the orchestrator moves each line into its block's `replans` object at the boundary after this merge (Out of scope), the counters print `re-plan=missing` and the gate refuses S1 for those classes.
- **`scripts/orchestrator/chain-finish.sh` (PR #378) keys `audit-finding:` lines on the head's sha7.** On an inherited head the record's lines name the parent's sha7, so the finish chain would exit 12. It is outside `allowed_files`; the orchestrator owns the follow-up.

## Not done, or outside scope

- The hcom counters, the lints, the AGENTS.md Audit section, `orch-audit.sh`, `chain-finish.sh` and the record migration are untouched (Out of scope).
- The project-map subagent was not run: `.project-map/` is outside `allowed_files`.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- CompactionDB: `memory add` in the worktree's own database, entry `e0e1d43c-9ac6-4cd0-a64c-935ab3ef7871` (validation §7, the command and a search showing it).
- cost: n/a (the runtime exposes no session figures to the seat).
