# Report: dotfiles-T128-gate-evidence-a02

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, branch `regime/gate-evidence`, PR #329, continued from a01's head `5971fffe` (INV-6 reset of `dotfiles-T128-gate-evidence-a01`; reset record `.orchestration/acceptance/dotfiles-T128-gate-evidence-a01-design-reset.md`).
- Task file: sha256 `930f570b…` checked against the TASK (13:17:02Z) and copied byte-identical to `.orchestration/dotfiles-T128-gate-evidence-a02/task.md`. a01's copy (`d1b6fcf3…`) stays unchanged as history (validation §1).
- Commits on the PR: a01's `7f763b7f`, `9a860c95` and `5971fffe` (evidence); a02's `379845f7` (the four round-1 fixes, the two-form search grammar, the a02 task copy), `386a71b3` (evidence), `c81c88a3` (fix round 2), then this evidence.

## What the PR does (task steps 1 to 5)

1. `PR_FEEDBACK_DISPOSITION` is `fixed:<commit>` (unchanged) or `not-applicable:<reason>; evidence=<command>`, both parts non-empty. The reason is greedy up to the last `; evidence=`, so it may contain `;`, as both dispositions of premise 2 do. The 20-character minimum for failure-level items applies to the reason alone. A pr-feedback item without the clause gets `needs a disposition fixed:<commit> or not-applicable:<reason>; evidence=<command>`. An `audit-finding:` line read through `AUDIT_DISPOSITIONS` uses the same regex; its no-match error names the clause, and a `fixed:` there keeps its "a fix moves HEAD" refusal.
2. `ACCEPTANCE_EVIDENCE` is required whenever `BASE` is set and is checked right after the PR-feedback evidence:
   - `orchestration_path_error(..., "acceptance")`;
   - when `PR_FEEDBACK_EVIDENCE` names a task, the record must be `<task>.md` by name and by resolved name, as the audit is bound (thread 4248232964);
   - the file must exist;
   - every `audit-finding:` line that carries a `not-applicable:` must have the evidence clause, whatever the audit verdict (INV-6; thread 4248232988), including a line written as a Markdown list item (`- `, `* `, `+ `, `1. `), as existing records write them (thread 4248697668);
   - ledger rows are the lines that fullmatch `(\d{10,}|audit:[0-9a-f]{7}:\d+)\t(\S+)`. For each class at three or more rows, a stripped line beginning with `search:` must carry a grep in one of a02's two forms, `grep -rl 'classes:…<slug>…' .orchestration/learning/mistakes/` (the SKILL's form, used by the fixture) or `grep -l 'classes:…<slug>…' .orchestration/learning/mistakes/*.md`, and a `contextdb_cli.py memory search …<slug>…`. The class slug must sit inside the grep's quoted `classes:` pattern and inside the memory-search query, each as a whole token (not next to `[\w-]`), so a line naming the class beside a search for another one fails (thread 4248697658). Otherwise the gate prints `S6: class <slug> at <n> without a pasted search`. `grep -l` given the bare directory is refused, because it exits 2 with "Is a directory" and reads no record (thread 4248233012; validation §5);
   - the record is not counted when sizing the diff, like the PR feedback file (thread 4248232998).

   The recipe passes `ACCEPTANCE_EVIDENCE="$(ACCEPTANCE_EVIDENCE)"` and its comment names it; README 427 to 428 and 1101 name it.

3. Eight new tests and new cases in two existing tests (table below). The module runs 79 tests, against 71 on `origin/main` (validation §2, §3). Each new check fails a test when broken: ten one-line mutations (M2 to M11) and the guards of `origin/main` and of the round-2 head `386a71b3` (validation §4).
4. `make require-crit-review` without `BASE` on a records-only tree prints the same line and exit status at `c81c88a3` as at `origin/main` (validation §6).
5. Nothing else changes in the gate. Two message texts carry the new grammar: the audit no-match error and the "leaves audit finding(s) … without a disposition" hint.

## Fixtures and the tests that read them

| Fixture                                                 | Read by                                                                                                                                                                                                                                     |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tests/fixtures/gate-evidence/pr-feedback-wrong.json`   | `test_dispositions_of_2026_10_12_without_evidence_are_refused` (both items refused with the new text)                                                                                                                                       |
| `tests/fixtures/gate-evidence/pr-feedback-right.json`   | `test_dispositions_with_an_evidence_command_are_accepted`                                                                                                                                                                                   |
| `tests/fixtures/gate-evidence/acceptance-s6-missing.md` | `test_s6_class_at_three_without_a_pasted_search_is_refused`, `test_base_requires_an_acceptance_record_under_acceptance` (content case)                                                                                                      |
| `tests/fixtures/gate-evidence/acceptance-s6-present.md` | `test_s6_class_at_three_with_a_pasted_search_is_accepted` (as written, and with the glob form), `test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict`, and every other `guard_base` run as the default passing record |

The wrong fixture's two dispositions are, byte for byte, the `disposition` fields of items 4244248692 and 4244378809 in `.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-pr-feedback.json` (PR 323, head `3a54d340`, collected 03:21:31Z). The right fixture has the same items, each disposition extended by `; evidence=<command>` with the command that refutes the claim; their outputs are in validation §5. The four fixtures total 26 lines. The present fixture's `search:` commands sit in backticks, because prettier (the formatter hook and CI's `make format`) rewrites a bare `*…*` in Markdown as `_…_`.

New tests without a fixture:

- `test_s6_search_line_names_the_class_token_and_both_commands` refuses eight lines and accepts a control line. The eight are: another class's slug; one command only; a grep outside the mistake records; `grep -l` given the bare directory; the old `grep -rl scope .orchestration`; a grep for another class; a memory search for another class; and a `search:` not at the line start.
- `test_base_requires_an_acceptance_record_under_acceptance`, the threat row's closing test, covers the path (empty, outside `.orchestration/acceptance/`, another task's record, a symlink alias to it, the task's own record missing) and the content (an S6 class at three without a search; an `audit-finding:` not-applicable without evidence, plain and as a list item).
- `test_acceptance_record_not_applicable_needs_evidence_whatever_the_verdict` refuses the clause-less line plain, as a `- ` item and as an indented `1. ` item. It accepts the clause, plain and as a `* ` item, and a fixed finding in prose.
- `test_acceptance_record_is_not_counted_as_a_change`: four docs files plus the record stay under the broad-diff limit.

New cases in existing tests: `no evidence clause`, `empty evidence command` and `empty reason` in `test_pr_feedback_rejects_incomplete_or_invalid_dispositions`, and `no evidence clause` in `test_incorrect_audit_needs_not_applicable_dispositions`.

## Bot round 1 (review 5491066199 on `5971fffe`, 12:55:08Z): five P1, one P2

| Thread     | P   | Class                     | Disposition                                                                                                                                                                                                                           |
| ---------- | --- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4248232955 | P1  | skill-command-sync        | proposed `not-applicable:owned by dotfiles-T128-playbook-rules-a02 item 6, and PR #328 merges before #329; evidence=grep -n 'ACCEPTANCE_EVIDENCE' .orchestration/tasks/dotfiles-T128-playbook-rules-a02.md` (output in validation §5) |
| 4248232964 | P1  | acceptance-record-binding | `fixed:379845f7`                                                                                                                                                                                                                      |
| 4248232976 | P1  | threat-row-missing        | `fixed:379845f7` (the a02 task copy carries the `ACCEPTANCE_EVIDENCE` row, `closed:` by the test above)                                                                                                                               |
| 4248232988 | P1  | acceptance-dispositions   | `fixed:379845f7`                                                                                                                                                                                                                      |
| 4248232998 | P2  | evidence-diff-sizing      | `fixed:379845f7`                                                                                                                                                                                                                      |
| 4248233012 | P1  | search-command-scan       | `fixed:379845f7`                                                                                                                                                                                                                      |

## Bot round 2 (review 5491635781 on `386a71b3`, 13:44:18Z): two P1

| Thread     | P   | Class                                              | Disposition      |
| ---------- | --- | -------------------------------------------------- | ---------------- |
| 4248697658 | P1  | search-command-scan (second, after 4248233012)     | `fixed:c81c88a3` |
| 4248697668 | P1  | acceptance-dispositions (second, after 4248232988) | `fixed:c81c88a3` |

Classes at two on this artifact: search-command-scan and acceptance-dispositions; every other class is at one. Questions: one under a01 (PONG 13:00Z, `status=question`), none under a02. Fix rounds: two (`379845f7` for round 1, `c81c88a3` for round 2), so a Bot P0/P1 on the final head is reported open, not fixed (Worker Playbook step 15). The worker resolves no thread. CI on `5971fffe` and on `386a71b3`: 13 of 13 green (main-checkout validation).

## Declared beyond the letter of the task

- README: besides the input lines 427 to 428 and 1101, two lines in the same section state the disposition grammar, 1094 ("Fill every item's disposition with …") and 1104. Both now show `; evidence=<command>`, because the gate refuses the form they stated. No other README section changes.
- Existing tests: all 17 `not-applicable:` literals gained `; evidence=gh pr checks 1` in one mechanical pass. Without it, the short-reason cases would hit the grammar error before the length rule they test, and the PR-mode passes would fail. The formatter hook (`ruff format`) re-wrapped the lines this pushed past the limit. `guard_base` writes `acceptance-s6-present.md` to `.orchestration/acceptance/test.md` (task `test`, from `test-pr-feedback.json`) and sets `ACCEPTANCE_EVIDENCE` unless the test passes its own.

## For the orchestrator

- This PR's own integration is the gate's first run under the new grammar: at its head, `make require-crit-review` is this PR's script. It requires `ACCEPTANCE_EVIDENCE=.orchestration/acceptance/dotfiles-T128-gate-evidence-a02.md` (the name the binding demands, from `dotfiles-T128-gate-evidence-a02-pr-feedback.json`). It also requires `; evidence=<command>` on every `not-applicable` in #329's sweep JSON and on the record's `audit-finding:` lines, and the S6 search line for any class at three.
- Outside `allowed_files`, the old `not-applicable:<reason>` form remains in the SKILL (step 10.4's command and lines 167, 171, 210), `home/dot_config/claude/rules/pr-integration.md:4`, the `scripts/pr-feedback.py` docstring (line 10) and `tests/fixtures/regime/worker-step-15.md`. The SKILL text is `dotfiles-T128-playbook-rules-a02`'s, and PR #328 merges first.
- `origin/main` moved to `7cbe5405` (boundary commits #330 and #331). They touch none of this PR's files, and `git merge-tree` merges cleanly (validation §9). `gh pr update-branch` is the orchestrator's effect.
- A ledger row with a longer audit sha (`audit:<sha8+>:<n>`) is not a row: the regex follows the task's `audit:<sha7>:<n>` literally.

## Notes

- Understand-Anything hook: did not fire. plan-mode-used: no. No worker-side review receipt: the tree is clean, and the task asks for none (a02 of A7 had none either).
- CompactionDB (main checkout): `memory add` printed `7f2f0c0b-6d20-42af-97ac-c5cfcfe62ea7` (decision) and `f939c61c-9822-407c-9928-d67bec0531c6` (failure) under a01; a02 adds the round-1 decision `43f0ce26-7095-45a2-a86c-d8bfbe197b1d` (validation §10), whose search grammar supersedes the one in `7f2f0c0b…`.
- The main-checkout copy adds the final head, CI, the Bot wait and the memory ids.

## Final head, CI and Bot round 3 (main-checkout copy)

- Final head `d5d6c9b1b22c32e483f76ed2d313571a487aa16a` (the diff head; `d5d6c9b1` is the evidence commit for the code head `c81c88a3`). CI: 13 of 13 green on it, as on `5971fffe` and `386a71b3` (validation §11). Bot reviews: one per head, on `5971fffe`, `386a71b3` and `d5d6c9b1` (validation §12). Bot rounds 3, fix rounds 2.
- Bot round 3 (review 5491920865, 14:07:25Z) is not fixed (Worker Playbook step 15). Both threads stay open for the orchestrator:

| Thread     | P   | Class                                                                                          | State and proposal                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------- | --- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4248934816 | P1  | disposition-delimiter (new, at 1)                                                              | `open:4248934816`. Real: the greedy reason splits at the last `; evidence=`, so `not-applicable:; evidence=echo proof; evidence=true` passes with the reason `; evidence=echo proof`. The greedy split was this worker's design choice. Proposed revise: the reason may not contain `; evidence=` (a second delimiter is refused), `check=tests/unit/test_require_crit_review.py::test_pr_feedback_rejects_incomplete_or_invalid_dispositions` (a new `second evidence delimiter` case).                                                                                                                                                                                                    |
| 4248934830 | P1  | search-command-scan (third on this artifact, after 4248233012 and 4248697658: an S1 candidate) | `open:4248934830`. The substring match accepts `echo grep …` and `xgrep …`. The two options are the orchestrator's. Option A, a revise: `grep` and `contextdb_cli.py` must each begin a command segment (after the class label, `;`, `&&`, `\|` or a backtick), `check=tests/unit/test_require_crit_review.py::test_s6_search_line_names_the_class_token_and_both_commands`. Option B, `not-applicable:a search: line is process evidence, not proof of execution; a well-formed command can be pasted unrun as easily as echo grep, so segment boundaries do not close the bypass; evidence=grep -n 'process evidence, not reviewer authentication' AGENTS.md` (output in validation §13). |

- Questions: one under a01 (PONG 13:00Z), none under a02. No RESULT before this one, for a01 or a02.

## RESULT

`AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-a02 status=ready_for_review pr=329 head=d5d6c9b1b22c32e483f76ed2d313571a487aa16a bot_rounds=3 fix_rounds=2 open:4248934816 open:4248934830 …` (the dispatched line names the five main-checkout paths, the dispositions above and the memory ids).

cost: n/a
