# Report: dotfiles-T128-gate-evidence-a04

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, branch `regime/gate-evidence`, PR #329. a04 is a03's INV-6 reset under plan 014 option A (reset record `.orchestration/acceptance/dotfiles-T128-gate-evidence-a03-design-reset.md`), continued from a03's amendment-1 head `82e86e50`.
- Task file: sha256 `03a5253d…` checked against the TASK (03:13:46Z) and copied byte-identical to `.orchestration/dotfiles-T128-gate-evidence-a04/task.md`. a01's, a02's and a03's copies stay unchanged as history (validation §1).
- Commits:
  - a01: `7f763b7f`, `9a860c95`, `5971fffe`;
  - a02: `379845f7`, `386a71b3`, `c81c88a3`, `d5d6c9b1`, `c6cf0548`, `61d90302`;
  - a03: `b2b3db45`, `c36fcd35`, `7581d590`, `3c20b0ca`, `f5f980f9`, `82e86e50`;
  - a04: `9db7ed3c` (the coverage rule, `dispatch`, unknown keys, three fixtures, the task copy), then this evidence.

## What a04 adds to a03 amendment 1 (task item 2's new sentence, items 3 and 5)

- **Ledger coverage** (thread 4254092805). The gate computes the set of swept finding ids:
  - every item of `PR_FEEDBACK_EVIDENCE` with `author` `chatgpt-codex-connector[bot]` and `source` `review_comment` (its id is the text after the last `_r` of its `url`);
  - every item with that author and `source` `review` whose `body` contains one of the four exact strings `![P0 Badge]`, `![P1 Badge]`, `![P2 Badge]`, `![P3 Badge]` (the text after `pullrequestreview-`);
  - `audit:<HEAD[:7]>:<n>` for each `[P0]`–`[P3]` line of `AUDIT_EVIDENCE`'s `.last.md` summary, counted with the gate's existing `AUDIT_FINDING` pattern, the one that numbers an `incorrect` audit's findings.

  It refuses a record whose ledger ids, as strings, do not include all of them, with `S6: ledger lacks <the missing ids, sorted>`. That is a set difference on exact strings: apart from the four badge tokens, no text of a body is read. The summary is required whenever `AUDIT_EVIDENCE` is set. A missing summary is refused with the text the audit check already uses (`… must exist with codex's final message`), because the coverage check runs before the audit check. Coverage is judged after the identity triple and the field checks, and before the S6 class count, so the class count reads a covered ledger.
- **`dispatch`**: an optional list of strings, validated only as such. Any key outside `format`, `task`, `head`, `pr`, `ledger`, `searches`, `audit_findings` and `dispatch` is refused with `acceptance record: unknown key <k>`, after the identity triple.
- Everything else is a03 amendment 1, unchanged:
  - the single-split disposition grammar;
  - the JSON block read with `json.loads(object_pairs_hook, parse_constant)` and nothing outside the standard library;
  - the identity triple `task`, `head` and `pr`;
  - the `pathlib` records search;
  - `audit_findings`;
  - the retired `AUDIT_DISPOSITIONS`;
  - the binding of the record to the task and its exclusion from diff sizing (a03's report).

## Tests and fixtures

The module runs 91 tests, against 71 on `origin/main`: 20 more, where the task asks for at least 13 (validation §2, §3). Each rule fails a test when broken: one-line mutations M2 to M27, plus the guards of `origin/main`, of a02's head `61d90302` and of a03's code head `f5f980f9` (validation §4).

| Fixture (`tests/fixtures/gate-evidence/`) | Read by |
|---|---|
| `pr-feedback-wrong.json` | `test_dispositions_of_2026_10_12_without_evidence_are_refused` |
| `pr-feedback-right.json` | `test_dispositions_with_an_evidence_command_are_accepted`, `test_acceptance_record_ledger_must_cover_swept_findings`, and the review-body tests (as the base of `right_items_with_reviews`) |
| `acceptance-stale-head.md` | `test_acceptance_record_head_must_be_head`, `test_base_requires_an_acceptance_record_under_acceptance` |
| `acceptance-s6-missing.md` | `test_s6_class_at_three_without_a_searches_entry_is_refused`, `test_base_requires_an_acceptance_record_under_acceptance` |
| `acceptance-s6-present.md` | `test_s6_class_at_three_with_the_matching_searches_entry_is_accepted`, `test_acceptance_record_prose_is_not_read`, and every other `guard_base` run as the default passing record |
| `acceptance-finding-quotes-grammar.md` | `test_audit_finding_reason_may_quote_the_grammar` |
| `acceptance-wrong-pr.md` | `test_acceptance_record_pr_must_be_the_swept_pr`, `test_base_requires_an_acceptance_record_under_acceptance` |
| `acceptance-duplicate-key.md` | `test_acceptance_record_refuses_a_duplicate_key`, `test_base_requires_an_acceptance_record_under_acceptance` |
| `acceptance-nan.md` | `test_acceptance_record_refuses_a_non_finite_number`, `test_base_requires_an_acceptance_record_under_acceptance` |
| `acceptance-ledger-incomplete.md` | `test_acceptance_record_ledger_must_cover_swept_findings` |
| `acceptance-dispatch-key.md` | `test_acceptance_record_accepts_a_dispatch_list` |
| `acceptance-ledger-review-body.md` | `test_acceptance_record_ledger_must_cover_a_badged_review_body` |

The twelve fixtures total 163 lines, under the 170 cap (validation §5).

New tests:

- `test_acceptance_record_ledger_must_cover_swept_findings` covers both halves of the coverage rule. First, a ledger without review comment 4244378809 is refused (`S6: ledger lacks 4244378809`). Then a covering record is run against a test-written audit summary with two findings and one `audit:` row, and refused (`S6: ledger lacks audit:<head7>:2`).
- `test_acceptance_record_ledger_must_cover_a_badged_review_body` uses a sweep of the two review comments plus three Codex review bodies: badged (`![P1 Badge](…)`), plain summary text, and a near match (`P1 Badge` and `[P1]` without the markup). The record lacking the badged body is refused. The same sweep passes with the badged body as a row, while the plain and near-match bodies need none.
- `test_swept_ids_are_exactly_the_review_comments_and_the_badged_review_body` calls `swept_finding_ids` directly. It checks that the set is exactly the two review comments and the badged body, and that a summary's two numbered findings become `audit:<sha7>:1` and `:2`.
- `test_acceptance_record_accepts_a_dispatch_list` accepts the two-entry fixture and refuses a non-string entry.
- `test_acceptance_record_refuses_an_unknown_key` writes its record in the test, with no fixture file.

## Bot threads

All earlier threads keep their a03 dispositions (`.orchestration/dotfiles-T128-gate-evidence-a03/report.md`, "Bot threads").

| Thread | P | Class | Disposition |
|---|---|---|---|
| 4254092805 (a03 round 2, review 5498081103 on `82e86e50`) | P1 | ledger-completeness | `fixed:9db7ed3c` (the coverage sentence) |
| 4248232955 | P1 | skill-command-sync | proposed `not-applicable:owned by dotfiles-T128-playbook-rules-a04 item 6, and PR #328 merges before #329; evidence=grep -n 'ACCEPTANCE_EVIDENCE' .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md` |

The main-checkout copy names the sha and adds the Bot round on the a04 head. The worker resolves no thread.

## Declared beyond the letter of the task

- `pr-feedback-wrong.json` and `pr-feedback-right.json`: each of their two items gains `"author": "chatgpt-codex-connector[bot]"`, the real author of threads 4244248692 and 4244378809 in the a02 sweep (validation §5). Their dispositions stay byte-for-byte, and the wrong and right fixtures keep the same items. So `pr-feedback-right.json` already has the Codex `review_comment` with a `_r<digits>` url that item 3 asks for, and gains no third item.
- `write_record` replaces `"audit:HEAD7:` with the test repository's `HEAD[:7]`, next to the `"head": "HEAD"` placeholder, because an audit row's sha cannot be fixed in a fixture.
- `audit_guard` now writes a record whose ledger covers each `[P0]`–`[P3]` line of its audit text, as coverage requires. `acceptance-finding-quotes-grammar.md` carries one `audit:HEAD7:1` row.
- `tests/fixtures/gate-evidence/.prettierrc` (`trailingComma: none`), carried over from a03 amendment 1: prettier formats the block as YAML front matter.

## For the orchestrator

- This PR's own integration is the gate's first run under the contract. `.orchestration/acceptance/dotfiles-T128-gate-evidence-a04.md` starts with a JSON block containing:
  - `"task": "dotfiles-T128-gate-evidence-a04"`, `"head": "<the audited head>"` and `"pr": 329`;
  - a `ledger` whose ids cover every Codex review comment of #329's sweep (all of them, whatever their disposition), every Codex review body with a badge, and `audit:<head7>:<n>` for each finding of the task-level audit of that head;
  - a `searches` entry for every class at three;
  - `audit_findings` if the audit is `incorrect`;
  - optionally `dispatch`.

  It also needs `; evidence=<command>`, once, on every `not-applicable` in the sweep JSON.
- The threat row for the audit summary (`.last.md`) is residual. The gate counts its `[P0]`–`[P3]` lines and reads nothing else, so a shortened summary shrinks the required set.
- **INV-2's file cap cannot be met as the task is written.** The Validation section allows at most 15 changed files outside `.orchestration/`. Item 3 alone requires twelve fixtures, and items 2 and 3 require the gate, its test module, the Makefile and the README: 16 files. `tests/fixtures/gate-evidence/.prettierrc` makes 17 (validation §9). The other two caps hold: 331 added lines outside `tests/` (cap 500) and 701 under `tests/` (cap 1000). I did not drop a required fixture or the `.prettierrc` to fit the cap; without the `.prettierrc`, prettier rewrites the JSON fixtures into invalid JSON and CI's format check fails. The fix is task text, and yours: raise the cap, move a fixture into its test (as the unknown-key case already is), or waive INV-2 for this PR.
- `origin/main` (`948d1f38`) merges cleanly, and `update-branch` is yours (validation §9).

## Notes

- Understand-Anything hook: did not fire. plan-mode-used: no. No worker-side review receipt.
- CompactionDB (main checkout): the a04 decision (validation §10), which adds the coverage rule to `4ea2924d…`.
- The main-checkout copy adds the final head, CI and the Bot wait.

cost: n/a
