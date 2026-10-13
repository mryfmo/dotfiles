# Report: dotfiles-T128-gate-evidence-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, branch `regime/gate-evidence` from `origin/main` `683384ea`, draft PR #329.
- Task file: sha256 `73514492…` checked against the TASK (11:58:43Z); amendment 1 (12:35:57Z) at `d1b6fcf3…`, recommitted byte-identical to `.orchestration/dotfiles-T128-gate-evidence-a01/task.md` (validation §1).
- Commits: `7f763b7f` (the change, the four fixtures, the task copy at `73514492…`), `9a860c95` (amendment 1: the `search:` grammar, the present fixture, the task copy at `d1b6fcf3…`), then this evidence.

## What changed (task steps 1 to 5)

1. `PR_FEEDBACK_DISPOSITION` is `fixed:<commit>` (unchanged) or `not-applicable:<reason>; evidence=<command>`, both parts non-empty. The reason group is greedy up to the last `; evidence=`, so a reason may contain `;` (both dispositions of premise 2 do). The 20-character minimum for failure-level items applies to the reason alone. A pr-feedback item without the clause gets `needs a disposition fixed:<commit> or not-applicable:<reason>; evidence=<command>`. An `audit-finding:` line read through `AUDIT_DISPOSITIONS` uses the same regex; its no-match error names the clause (`line needs \`not-applicable:<reason>; evidence=<command>\``), and a `fixed:` there keeps its own "a fix moves HEAD" refusal, so the audit error never offers `fixed:`.
2. `ACCEPTANCE_EVIDENCE` is required whenever `BASE` is set, checked right after the PR-feedback evidence with `orchestration_path_error(..., "acceptance")` and an existence check; when set without `BASE` it is checked the same way and is otherwise optional. Ledger rows are the lines that fullmatch `(\d{10,}|audit:[0-9a-f]{7}:\d+)\t(\S+)`. For each class at three or more rows, a stripped line beginning with `search:` must name the class as a whole token (not next to `[\w-]`, so `scope` is not named by a line about `class-count-scope`) and contain `grep -l 'classes:`, `.orchestration/learning/mistakes` and `contextdb_cli.py memory search` (amendment 1); otherwise `S6: class <slug> at <n> without a pasted search`. The recipe passes `ACCEPTANCE_EVIDENCE="$(ACCEPTANCE_EVIDENCE)"` and its comment names it; README 427 to 428 and 1101 name it.
3. Six new tests and new cases in two existing tests (table below); the module runs 77 tests, 71 on `origin/main` (validation §2, §3). Every new check fails its test when broken (validation §4).
4. `make require-crit-review` without `BASE` on a records-only tree prints the same line and exit status at `9a860c95` as at `origin/main` (validation §6).
5. Nothing else changes in the gate. Two message texts carry the new grammar: the audit no-match error and the "leaves audit finding(s) … without a disposition" hint.

## Fixtures and the tests that read them

| Fixture | Read by |
|---|---|
| `tests/fixtures/gate-evidence/pr-feedback-wrong.json` | `test_dispositions_of_2026_10_12_without_evidence_are_refused` (both items refused with the new text) |
| `tests/fixtures/gate-evidence/pr-feedback-right.json` | `test_dispositions_with_an_evidence_command_are_accepted` |
| `tests/fixtures/gate-evidence/acceptance-s6-missing.md` | `test_s6_class_at_three_without_a_pasted_search_is_refused` |
| `tests/fixtures/gate-evidence/acceptance-s6-present.md` | `test_s6_class_at_three_with_a_pasted_search_is_accepted`, and every other `guard_base` run as the default passing record |

The wrong fixture's two dispositions are the `disposition` fields of items 4244248692 and 4244378809 in `.orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-pr-feedback.json` (PR 323, head `3a54d340`, collected 03:21:31Z), byte for byte. The right fixture has the same items, with each disposition extended by `; evidence=<command>`. The commands are the ones that refute each claim: the managed settings' `defaultMode`/`ask` lines for "human-only permission gate", and `scripts/regime-counters.sh:114` (the first RESULT's head) for the head binding. Their outputs are in validation §5. The four fixtures total 26 lines.

New tests without a fixture: `test_s6_search_line_names_the_class_token_and_both_commands` (another class's slug, one command only, a grep outside the mistake records, the pre-amendment `grep -rl`, a `search:` not at the line start) and `test_base_requires_an_acceptance_record_under_acceptance` (empty, outside `.orchestration/acceptance/`, missing file). New cases in existing tests: `no evidence clause`, `empty evidence command` and `empty reason` in `test_pr_feedback_rejects_incomplete_or_invalid_dispositions`, and `no evidence clause` in `test_incorrect_audit_needs_not_applicable_dispositions`.

## Declared beyond the letter of the task

- README: besides the input lines 427 to 428 and 1101, the same section has two lines that tell the reader the disposition grammar: 1094 (the sweep code block's "Fill every item's disposition with …") and 1104 ("any item without a `fixed:<commit>` or `not-applicable:<reason>` disposition"). Both now show `; evidence=<command>`, because the gate refuses the form they stated. No other README section changes. The threat-table row names "the two lines"; these two more are in the same section and are declared here.
- Existing tests: all 17 `not-applicable:` literals gained `; evidence=gh pr checks 1` in one mechanical pass. Without it, the short-reason cases would hit the grammar error before the length rule they test, and the PR-mode passes would fail. The repository's formatter hook (`ruff format`) re-wrapped the lines that this pushed past the line limit. `guard_base` writes `acceptance-s6-present.md` to `.orchestration/acceptance/test.md` and sets `ACCEPTANCE_EVIDENCE` unless the test passes its own. The file is an untracked `.md`, so the docs-only and "Review not required" outcomes are unchanged (77 OK).

## Not changed, for the owners

- `home/dot_agents/skills/agmsg-orchestration/SKILL.md` step 10.4 (the gate command without `ACCEPTANCE_EVIDENCE`), and the old `not-applicable:<reason>` form in SKILL lines 167, 171 and 210, `home/dot_config/claude/rules/pr-integration.md:4`, the `scripts/pr-feedback.py` docstring (line 10) and `tests/fixtures/regime/worker-step-15.md`. They are outside `allowed_files`; the SKILL text is `dotfiles-T128-playbook-rules-a01`'s. Integration order: once this PR merges and until that task lands, step 10.4's command run verbatim is refused for the missing `ACCEPTANCE_EVIDENCE`, and every `not-applicable:` without the clause is refused.
- INV-6's sentence says the gate refuses an acceptance record that "carries a not-applicable disposition without an evidence= clause". The gate reads `audit-finding:` lines only through `AUDIT_DISPOSITIONS`, as before, and only for an `incorrect` verdict. The record named by `ACCEPTANCE_EVIDENCE` is read for the S6 ledger only. So a record whose `audit-finding:` lines lack the clause under a `correct` verdict passes, which follows step 5 ("not the gate's other checks"). Whether the S6 reader should also check those lines is the orchestrator's decision.
- A ledger row with a longer audit sha (`audit:<sha8+>:<n>`) is not a row: the regex follows the task's `audit:<sha7>:<n>` literally.

## Notes

- Understand-Anything hook: did not fire. plan-mode-used: no.
- The main-checkout copy of this report adds CI, the Bot wait, the final head and the CompactionDB `memory add`.

cost: n/a
