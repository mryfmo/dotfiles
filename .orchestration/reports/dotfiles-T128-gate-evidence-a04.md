# Report: dotfiles-T128-gate-evidence-a04

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, branch `regime/gate-evidence`, PR #329. a04 is a03's INV-6 reset under plan 014 option A (reset record `.orchestration/acceptance/dotfiles-T128-gate-evidence-a03-design-reset.md`), continued from a03's amendment-1 head `82e86e50`.
- Task file: amendment 1 (03:37:55Z; wording only, the `dispatch` entry's ` read_at=read|unread` suffix) at sha256 `be659392…`, recommitted byte-identical to `.orchestration/dotfiles-T128-gate-evidence-a04/task.md`; the first a04 copy was `03a5253d…`. `acceptance-dispatch-key.md`'s example entries now end in `read_at=read` and `read_at=unread`; the gate still validates the list only as strings. a01's, a02's and a03's copies stay unchanged as history (validation §1).
- Commits:
  - a01: `7f763b7f`, `9a860c95`, `5971fffe`;
  - a02: `379845f7`, `386a71b3`, `c81c88a3`, `d5d6c9b1`, `c6cf0548`, `61d90302`;
  - a03: `b2b3db45`, `c36fcd35`, `7581d590`, `3c20b0ca`, `f5f980f9`, `82e86e50`;
  - a04: `9db7ed3c` (the coverage rule, `dispatch`, unknown keys, three fixtures, the task copy), `863ae465` (evidence), `ca7dcd73` (amendment 1's task copy and fixture wording), `8d54fd76` (fix round 1), `8c0c015b` (the fixtures moved to PR #340), then this evidence.
- **The INV-2 split** (the orchestrator's answer of 03:47Z: a cap is a split, never a disposition). The thirteen files under `tests/fixtures/gate-evidence/` (twelve fixtures and `.prettierrc`, 164 lines) are on PR #340, branch `regime/gate-evidence-fixtures` from `origin/main` `4470b0c8`, head `27e8a0ea`. PR #329 keeps four files outside `.orchestration/`: the gate, its test module, the Makefile and the README. Outside `.orchestration`, the tested content `8d54fd76` equals `8c0c015b` plus #340's fixtures (validation §9). #329's CI fails until #340 merges and #329 takes the new base, because its test module reads the fixtures.

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

The module runs 92 tests on the combined content (#329 with #340's fixtures), against 71 on `origin/main`: 21 more, where the task asks for at least 13 (validation §2, §3). Each rule fails a test when broken: one-line mutations M2 to M29, plus the guards of `origin/main`, of a02's head `61d90302`, of a03's code head `f5f980f9` and of a04's `9db7ed3c` (validation §4).

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

The twelve fixtures, now on PR #340, total 163 lines, under the 170 cap; with `.prettierrc`, 164 (validation §5).

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

## a04 Bot round 1 (review 5498584052 on `ca7dcd73`, 03:50:47Z): two P1, fix round 1 (`8d54fd76`)

| Thread | P | Class | Disposition |
|---|---|---|---|
| 4254525594 | P1 | front-matter-delimiter (new) | `fixed:8d54fd76`: both delimiters are whole lines that are exactly `---` (a prefix search let `---junk` close the block); the closing test's `a closing line that is not exactly ---` case |
| 4254525603 | P1 | coverage-source-authentication (new) | `fixed:8d54fd76`: `feedback_key` compares `author` with the live collection too, so a saved sweep cannot change a Codex item's author to keep it out of the ledger's required ids (`test_swept_ids_come_from_authenticated_authors`) |

CI on `ca7dcd73`: 12 of 12 check runs green. Questions under a04: none (PONG 03:47Z was the orchestrator's answer to a flag). Fix rounds: one.

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
- INV-2: answered by the split above. PR #329 has 4 files outside `.orchestration/` and PR #340 has 13; each PR is within the 500-line and 1000-line caps (validation §9).
- `origin/main` (`948d1f38`) merges cleanly, and `update-branch` is yours (validation §9).

## Notes

- Understand-Anything hook: did not fire. plan-mode-used: no. No worker-side review receipt.
- CompactionDB (main checkout): the a04 decision (validation §10), which adds the coverage rule to `4ea2924d…`.
- The main-checkout copy adds the final head, CI and the Bot wait.


## Final heads, CI and the Bot (main-checkout copy)

- PR #329: final head `ffe7d872f39491dbb539399b4aa5482a85c91ce2` (the evidence commit over the code head `8c0c015b`; outside `.orchestration/` the two are identical, validation §15). `origin/main` (`1da9594c`) merges cleanly.
- PR #340: the worker's head `27e8a0ea376cbaeb73b976ed77ffa0d8d166e6c2`. GitHub's `update-branch` merge `20d776d4` (04:33:39Z, parents `27e8a0ea` and `1da9594c`) is not a worker commit. `1da9594c` touches no file of either PR (validation §15).
- CI (validation §11):
  - `863ae465` and `ca7dcd73`: 12 of 12 check runs green.
  - `27e8a0ea` (#340): 12 of 12 green. `20d776d4`: 12 of 12 green.
  - `ffe7d872` (#329): eight green, `test (ubuntu-24.04, server)` failed, and the other three test jobs were cancelled by fail-fast. The failed job ran 1017 tests with 82 errors, all in `test_require_crit_review` and all `FileNotFoundError` on `tests/fixtures/gate-evidence/*`. That is the split's expected red: it lasts until #340 merges and #329 takes the new base.
- Bot (validation §12):
  - a04 round 1: review 5498584052 on `ca7dcd73`, two P1, fixed in `8d54fd76` (the table above).
  - a04 round 2: review 5498822030 on `ffe7d872` (04:27:57Z), one P1 (below).
  - #340: the security review completed on `27e8a0e` with no comment. The code review on `27e8a0e` was a manual `@codex review` and answered "Didn't find any major issues" in an issue comment (6138208548, 04:25:33Z). The code review on `20d776d` completed at 04:35:27Z with no comment.
  - The Bot wait on #340 printed `bot: none` because it read only the Bot's reviews, not its issue comments; the listing in validation §12 shows the issue comment.
- Bot rounds under a04: two on #329 and one on #340. Fix rounds: one (`8d54fd76`). Questions: none. Amendments: one (`be659392`).
- This is a04's first RESULT, so no INV-6 count for Bot P1s on heads after the first RESULT applies yet. `863ae465` was GitHub's head from 03:41:59Z until `ca7dcd73`'s push at 03:45:31Z, and the unfiltered listing in validation §12 shows no Codex review on it.
- History (validation §16): two AGMSG-TASKs, the first and amendment 1, so one amendment. The four worker PONGs are all `status=alive`, so there are no questions. The orchestrator's 03:47:03Z PONG is `status=answer`, to the INV-2 flag carried in the worker's 03:45:49Z PONG.
- The branch report's "For the orchestrator" names `origin/main` as `948d1f38`. That sha predates the fetch at 04:10Z; §9 (`4470b0c8`) and §15 (`1da9594c`) are authoritative.

| Thread | P | Class | State and proposal |
|---|---|---|---|
| 4254731145 (review 5498822030 on `ffe7d872`) | P1 | split-fixture-order (new) | proposed `not-applicable:the fixtures are on PR #340 by the orchestrator's INV-2 split (PONG 03:47Z), which integrates first, and #329 takes them through update-branch before its gate; evidence=git ls-tree -r --name-only origin/main tests/fixtures/gate-evidence`. The finding is accurate for #329 alone: the test module reads 13 files that #329 does not carry. Adding them back would undo the split that the cap requires. Validation §11 shows that the red job's 82 errors are all `FileNotFoundError` on paths under `tests/fixtures/gate-evidence/`; ten of the 13 names appear, because each test stops at its first missing read. After #340 merges, the evidence command lists the 13 paths. If you prefer `fixed:`, the update-branch merge that brings #340's fixtures into #329 also passes the gate's range check: an ancestor of HEAD and not of the base (`scripts/require-crit-review.py:385-386`). |

## Precision notes (main-checkout copy)

- The gate imports only standard-library modules. The precise check at `ffe7d872` finds no PyYAML import, no `"uv"` argument and no `["grep"` subprocess (validation §13).
- The recipe passes `ACCEPTANCE_EVIDENCE` to the gate (validation §14).

## RESULT

`AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-a04 status=ready_for_review pr=329 head=ffe7d872f39491dbb539399b4aa5482a85c91ce2 fixtures_pr=340 fixtures_head=27e8a0ea376cbaeb73b976ed77ffa0d8d166e6c2 …` (the dispatched line names the five main-checkout paths, the CI state, the dispositions and the memory ids).

cost: n/a

