# Report: dotfiles-T128-gate-evidence-a02

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, branch `regime/gate-evidence`, PR #329, continued from a01's head `5971fffe` (INV-6 reset of `dotfiles-T128-gate-evidence-a01`; reset record `.orchestration/acceptance/dotfiles-T128-gate-evidence-a01-design-reset.md`).
- Task file: amendment 1 (TASK 14:28:26Z) at sha256 `241aec12…`, recommitted byte-identical to `.orchestration/dotfiles-T128-gate-evidence-a02/task.md`; the first a02 copy was `930f570b…`, and a01's copy (`d1b6fcf3…`) stays unchanged as history (validation §1).
- Commits on the PR:
  - a01: `7f763b7f`, `9a860c95`, `5971fffe` (evidence);
  - a02: `379845f7` (the four round-1 fixes, the a02 task copy), `386a71b3` (evidence), `c81c88a3` (fix round 2), `d5d6c9b1` (evidence, the first RESULT's head);
  - amendment 1: `c6cf0548` (the recomputed S6 search, the first-delimiter grammar, the task copy), then this evidence.

## What the PR does (task steps 1 to 5)

1. `PR_FEEDBACK_DISPOSITION` is `fixed:<commit>` (unchanged) or `not-applicable:<reason>; evidence=<command>`, both parts non-empty. Neither part may hold a `; evidence=`, so a full match splits at the first delimiter and refuses a second one (amendment 1; thread 4248934816). A reason may still contain an ordinary `;`, as both dispositions of premise 2 do. The 20-character minimum for failure-level items applies to the reason alone and can no longer be padded through a second delimiter. The rule applies in three places:
   - a pr-feedback item without the clause gets `needs a disposition fixed:<commit> or not-applicable:<reason>; evidence=<command>`;
   - an `audit-finding:` line read through `AUDIT_DISPOSITIONS` is matched from its `not-applicable:` to the end of the line, and its error names the clause, while a `fixed:` there keeps its "a fix moves HEAD" refusal;
   - the acceptance record's own `audit-finding:` lines follow the same rule (item 2).
2. `ACCEPTANCE_EVIDENCE` is required whenever `BASE` is set and is checked right after the PR-feedback evidence:
   - `orchestration_path_error(..., "acceptance")`;
   - when `PR_FEEDBACK_EVIDENCE` names a task, the record must be `<task>.md` by name and by resolved name, as the audit is bound (thread 4248232964);
   - the file must exist;
   - every `audit-finding:` line that carries a `not-applicable:` must have the clause, whatever the audit verdict (INV-6; thread 4248232988). That includes a line written as a Markdown list item (`- `, `* `, `+ `, `1. `), as existing records write them (thread 4248697668);
   - S6, as of amendment 1. Ledger rows are the lines that fullmatch `(\d{10,}|audit:[0-9a-f]{7}:\d+)\t(\S+)`. For each class at three or more rows, a class outside `[a-z0-9-]` is refused. Otherwise the gate runs `grep -rl 'classes:.*<slug>' .orchestration/learning/mistakes/` itself, from the repository root and without a shell (an argument list). It refuses an exit status other than 0 or 1 (grep exit 2: the directory is missing or unreadable). It then requires a stripped line `search: <slug> -> <basenames, space-separated, or none>` whose set equals the basenames grep found, or prints `S6: class <slug> at <n> without a matching records search`. The gate reads no pasted command text. The `contextdb: <slug> -> <n> lines` line is the orchestrator's and is not read (threads 4248233012, 4248697658, 4248934830; the S1 record `plan-006-s1-gate-evidence-search-command-scan-2026-10-12.md`);
   - the record is not counted when sizing the diff, like the PR feedback file (thread 4248232998).

   The recipe passes `ACCEPTANCE_EVIDENCE="$(ACCEPTANCE_EVIDENCE)"` and its comment names it; README 427 to 428 and 1101 name it.

3. Eight new tests and new cases in two existing tests (below). The module runs 79 tests, against 71 on `origin/main` (validation §2, §3). Each new check fails a test when broken: twelve one-line mutations (M2 to M13) and the guards of `origin/main` and of the first RESULT's head `d5d6c9b1` (validation §4).
4. `make require-crit-review` without `BASE` on a records-only tree prints the same line and exit status at `c6cf0548` as at `origin/main` (validation §6).
5. Nothing else changes in the gate. Two message texts carry the new grammar: the audit no-match error and the "leaves audit finding(s) … without a disposition" hint.

## Fixtures and the tests that read them

| Fixture                                                 | Read by                                                                                                                                                                                                         |
| ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tests/fixtures/gate-evidence/pr-feedback-wrong.json`   | `test_dispositions_of_2026_10_12_without_evidence_are_refused` (both items refused with the new text)                                                                                                           |
| `tests/fixtures/gate-evidence/pr-feedback-right.json`   | `test_dispositions_with_an_evidence_command_are_accepted`                                                                                                                                                       |
| `tests/fixtures/gate-evidence/acceptance-s6-missing.md` | `test_s6_class_at_three_without_a_search_line_is_refused`, `test_base_requires_an_acceptance_record_under_acceptance` (content cases)                                                                           |
| `tests/fixtures/gate-evidence/acceptance-s6-present.md` | `test_s6_class_at_three_with_the_matching_search_line_is_accepted`, `test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict`, and every other `guard_base` run as the default passing record |

The wrong fixture's two dispositions are, byte for byte, the `disposition` fields of items 4244248692 and 4244378809 in `.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-pr-feedback.json` (PR 323, head `3a54d340`, collected 03:21:31Z). The right fixture has the same items, each disposition extended by `; evidence=<command>` with the command that refutes the claim; their outputs are in validation §5. The present fixture states `search: class-count-scope -> M-20261012-3.md`, which is what the real tree's search returns (validation §5). The test repositories' base commit carries a mistake record of that name with `classes: [evidence, class-count-scope]`. The four fixtures total 27 lines.

New tests without a fixture:

- `test_s6_search_line_must_equal_the_recomputed_records_search` accepts the matching set, and `none` where nothing matches. It refuses:
  - a record missing from the line;
  - a record too many;
  - another class's line;
  - pasted command text instead of the template;
  - a `search:` not at the line start;
  - a class outside `[a-z0-9-]` (`Scope;touch-pwned`, refused before any search runs; no file appears);
  - grep exit 2 once the records directory is gone.
- `test_base_requires_an_acceptance_record_under_acceptance`, the threat row's closing test. It covers the path (empty, outside `.orchestration/acceptance/`, another task's record, a symlink alias to it, the task's own record missing) and the content: an S6 class at three without a search line or with the wrong set, and an `audit-finding:` not-applicable without evidence, as a list item, or with a second delimiter.
- `test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict` refuses the clause-less line plain, as a `- ` item and as an indented `1. ` item, and a line with a second delimiter. It accepts the clause, plain and as a `* ` item, and a fixed finding in prose.
- `test_acceptance_record_is_not_counted_as_a_change`: four docs files plus the record stay under the broad-diff limit.

New cases in existing tests:

- `test_pr_feedback_rejects_incomplete_or_invalid_dispositions`: `no evidence clause`, `empty evidence command`, `empty reason`, `a second evidence delimiter as the reason` (the Bot's example) and `a second evidence delimiter padding a failure reason`;
- `test_incorrect_audit_needs_not_applicable_dispositions`: `no evidence clause` and `a second evidence delimiter`.

## Bot threads

| Round (review, head)       | Thread     | P   | Class                     | Disposition                                                                                                                                                                                                                 |
| -------------------------- | ---------- | --- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 (5491066199, `5971fffe`) | 4248232955 | P1  | skill-command-sync        | proposed `not-applicable:owned by dotfiles-T128-playbook-rules-a02 item 6, and PR #328 merges before #329; evidence=grep -n 'ACCEPTANCE_EVIDENCE' .orchestration/tasks/dotfiles-T128-playbook-rules-a02.md` (validation §5) |
| 1                          | 4248232964 | P1  | acceptance-record-binding | `fixed:379845f7`                                                                                                                                                                                                            |
| 1                          | 4248232976 | P1  | threat-row-missing        | `fixed:379845f7` (the a02 task copy carries the `ACCEPTANCE_EVIDENCE` row, closed by the test above)                                                                                                                        |
| 1                          | 4248232988 | P1  | acceptance-dispositions   | `fixed:379845f7`                                                                                                                                                                                                            |
| 1                          | 4248232998 | P2  | evidence-diff-sizing      | `fixed:379845f7`                                                                                                                                                                                                            |
| 1                          | 4248233012 | P1  | search-command-scan       | `fixed:c6cf0548` (amendment 1: the recomputed search replaces the pasted-command check of `379845f7`)                                                                                                                       |
| 2 (5491635781, `386a71b3`) | 4248697658 | P1  | search-command-scan       | `fixed:c6cf0548` (as above; `c81c88a3` first bound the pasted grep to the class)                                                                                                                                            |
| 2                          | 4248697668 | P1  | acceptance-dispositions   | `fixed:c81c88a3`                                                                                                                                                                                                            |
| 3 (5491920865, `d5d6c9b1`) | 4248934816 | P1  | disposition-delimiter     | `fixed:c6cf0548` (amendment 1 item 1)                                                                                                                                                                                       |
| 3                          | 4248934830 | P1  | search-command-scan       | `fixed:c6cf0548` (amendment 1 item 2; S1 on this class)                                                                                                                                                                     |

Questions: one under a01 (PONG 13:00Z), none under a02. RESULTs: one under a02 so far (14:16:46Z, head `d5d6c9b1`), so a Bot P0/P1 on this head is the first INV-6 head after a RESULT. The worker resolves no thread. CI on `5971fffe`, `386a71b3` and `d5d6c9b1`: 13 of 13 green each (main-checkout validation).

## Declared beyond the letter of the task

- README: besides the input lines 427 to 428 and 1101, two lines in the same section state the disposition grammar, 1094 ("Fill every item's disposition with …") and 1104. Both now show `; evidence=<command>`, because the gate refuses the form they stated. No other README section changes.
- Existing tests: all 17 `not-applicable:` literals gained `; evidence=gh pr checks 1` in one mechanical pass. Without it, the short-reason cases would hit the grammar error before the length rule they test, and the PR-mode passes would fail. The formatter hook (`ruff format`) re-wrapped the lines this pushed past the limit.
- `guard_base` writes `acceptance-s6-present.md` to `.orchestration/acceptance/test.md` (task `test`, from `test-pr-feedback.json`) and sets `ACCEPTANCE_EVIDENCE` unless the test passes its own. `setUp` commits one mistake record into each test repository's base, so it is never a change.

## For the orchestrator

- This PR's own integration is the gate's first run under the new grammar: at its head, `make require-crit-review` is this PR's script. It requires `ACCEPTANCE_EVIDENCE=.orchestration/acceptance/dotfiles-T128-gate-evidence-a02.md` (the name the binding demands, from `dotfiles-T128-gate-evidence-a02-pr-feedback.json`). It also requires `; evidence=<command>`, once, on every `not-applicable` in #329's sweep JSON and on the record's `audit-finding:` lines. For any class at three in the record's ledger, it requires `search: <slug> -> <set>` equal to the gate's own `grep -rl` from the review worktree's root.
- Outside `allowed_files`, the old `not-applicable:<reason>` form remains in the SKILL (step 10.4's command and lines 167, 171, 210), `home/dot_config/claude/rules/pr-integration.md:4`, the `scripts/pr-feedback.py` docstring (line 10) and `tests/fixtures/regime/worker-step-15.md`. The SKILL text is `dotfiles-T128-playbook-rules-a02`'s, and PR #328 merges first.
- `origin/main` moved to `e0e2fe62` (boundary commits #330, #331 and the next). They touch none of this PR's files, and `git merge-tree` merges cleanly (validation §9). `gh pr update-branch` is the orchestrator's effect.
- A ledger row with a longer audit sha (`audit:<sha8+>:<n>`) is not a row: the regex follows the task's `audit:<sha7>:<n>` literally.

## Notes

- Understand-Anything hook: did not fire. plan-mode-used: no. No worker-side review receipt: the tree is clean, and the task asks for none.
- CompactionDB (main checkout): `7f2f0c0b-6d20-42af-97ac-c5cfcfe62ea7` (a01 decision), `f939c61c-9822-407c-9928-d67bec0531c6` (failure), `43f0ce26-7095-45a2-a86c-d8bfbe197b1d` (a02 decision) and `e74368c4-1073-4761-b26f-a4c9c735f0e3` (amendment 1 decision) (validation §10); each later decision supersedes the search grammar of the earlier ones.
- The main-checkout copy adds the final head, CI and the Bot wait.

## Final head, CI and Bot round 4 (main-checkout copy)

- The diff head is `61d90302` (the evidence commit for the code head `c6cf0548`). The orchestrator's `gh pr update-branch` made the merge head `4e2266aae7cddb692a9d56d8a8d2c83e48cc8303` (parents `61d90302` and `origin/main` `e0e2fe62`).
- CI (validation §11):
  - `61d90302`: 12 of 12 check runs green.
  - `4e2266aa`, first attempt: `public-bootstrap (macos-14, client)` failed in `50-install-dependencies.sh`, because Homebrew's download returned `HTTP status: 503`. Fail-fast then cancelled the two Ubuntu `public-bootstrap` jobs.
  - `gh run rerun 38266004570 --failed` (15:02:05Z): attempt 2 passed, so all 12 check runs are green.
  - CodeRabbit is skipped on every head (automatic reviews are off).
- Bot (validation §12): no review of `61d90302` arrived within 15 minutes, and `@codex review` was posted at 617 s, so the diff head records `bot: none`. That manual request's review ran on the merge head: review 5492641317 (15:10:21Z) on `4e2266aa`, with two P1 and one P2. This is the fourth Bot round; fix rounds are already two, so it is not fixed (Worker Playbook step 15).
- INV-6: the first RESULT went out at 14:16:46Z on `d5d6c9b1`. `4e2266aa` is the first later head with a Bot P1, so the count is one of two.

| Thread     | P   | Class                                                                             | Verified (validation §13) and proposal                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ---------- | --- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 4249544748 | P1  | acceptance-dispositions (third, after 4248232988 and 4248697668: an S1 candidate) | `open:4249544748`. Real: `audit-finding: 1 parser accepts not-applicable: without evidence -> fixed:abcdef0` is refused, because the check judges the first `not-applicable:` on the line, not the line's disposition. Proposed revise: judge the last `fixed:`/`not-applicable:` token on the line, `check=tests/unit/test_require_crit_review.py::test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict` (a new `a fixed finding that quotes the grammar` case).                                   |
| 4249544762 | P1  | acceptance-record-binding (second, after 4248232964)                              | `open:4249544762`. Real in principle: the feedback JSON (`head_sha`) and the audit (its name) are bound to HEAD, and the record is bound only to the task. A stale record of the same name passes after a new head. A head line is a record-format decision (the orchestrator writes the record and the SKILL's step 10.3 sentence), so it is yours: for example a `head: <full sha>` line compared with HEAD, `check=tests/unit/test_require_crit_review.py::test_base_requires_an_acceptance_record_under_acceptance`. |
| 4249544794 | P2  | regex-backtracking (new; the disposition-delimiter regex of amendment 1)          | `open:4249544794`. Real: a malformed 5,000-character disposition takes about 0.2 s on this host, and 2,000 characters about 0.03 s (quadratic). Proposed revise: split once on the first `; evidence=` with `str.partition`, refuse a second with `in`, and check each part linearly; `check=tests/unit/test_require_crit_review.py::test_pr_feedback_rejects_incomplete_or_invalid_dispositions` (a long malformed case under a time bound).                                                                            |

## RESULT

`AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-a02 status=ready_for_review pr=329 head=61d90302acb180efc5e99146256ac94764c49d51 merge_head=4e2266aae7cddb692a9d56d8a8d2c83e48cc8303 bot_rounds=4 fix_rounds=2 open:4249544748 open:4249544762 open:4249544794 …` (the dispatched line names the five main-checkout paths and the memory ids).

cost: n/a
