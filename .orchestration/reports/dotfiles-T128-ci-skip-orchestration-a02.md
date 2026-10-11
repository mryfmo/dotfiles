# Report: dotfiles-T128-ci-skip-orchestration-a02

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-f`, branch `feat/ci-skip-orchestration`, PR #320, continuing from `dc4e6c37`. Reset successor of `dotfiles-T128-ci-skip-orchestration-a01` under INV-6 (reset record `.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md`); the implementation on `dc4e6c37` stays.
- Task file sha256 `2c3a5ee2…` checked against TASK 07:35:34Z and copied byte-identical in `406ca746` to `.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md` (the a01 directory stays as it is). Content commit `a35a751e`; then this evidence.

## What changed (`a35a751e`, `tests/unit/test_workflow_orchestration_skip.py` only)

The hand-written workflow reader now fails closed. The test environment has no YAML parser (`make unit-test` runs bare `uv run python`), and no dependency is added. Inside `jobs:`:

- a job name, a job key or a step key must be the plain form `name:` (`[a-z0-9_-]+`, the colon right after, then end of line or a space). Anything else raises `ValueError`: quotes, escapes, a space before the colon, a flow mapping, `<<` merge keys. A job name must carry no value, so `job: {…}` raises too. Comments and blank lines are skipped, and `run: |` script lines are captured as before.
- a job body's first line must sit at four spaces, and a step item's first key must follow `- ` directly. Sibling keys share one indentation, so this pins every job and step key to its column. A body shifted to six spaces, or `-   name:` with its keys at ten, would otherwise hide every key from the reader while GitHub reads them (validation §3, the two positional rows).
- a line at six spaces inside `steps:` that is not a `- ` item, or a step key before any item, raises.

`test_the_reader_fails_closed_on_unsupported_key_forms` replaces `test_structural_tests_see_quoted_keys` (a01's revise check): under the reset, quoted keys raise instead of reading as bare ones, so a01's `revise.yaml` selector no longer resolves. a01 is reset history. The new test has eight subTests: the task's four forms (`if : false`, `"\x69f": false`, `continue-on-error : true`, a step written as `{ if: false }`), a quoted job name, a quoted step key, a shifted job body and a shifted step item. Each must raise.

## Threat table (the completion condition)

| Row | Disposition | Where |
|---|---|---|
| The PR edits the workflow files themselves | residual, as the task states | `tests/unit/test_workflow_security.py` passes unchanged (validation §2) |
| The decision step misclassifies a diff | closed | `DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff`, `…test_the_unit_test_decision_skips_an_orchestration_only_diff`, `…test_the_unit_test_decision_ignores_renames` |
| A required job is skipped | closed | `RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs` and `…test_no_job_is_left_for_a_required_job_to_need`, read by the fail-closed reader: each of the six unsupported-form mutations errors them (validation §3) |
| The decision step itself fails | closed | `DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed`, `…test_every_heavy_step_carries_its_jobs_decision`, read by the same reader |
| The reader misses a valid YAML form | closed | `RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms`. The task's four mutations, and the two positional ones found while checking the reader, each hide a real key from GitHub's YAML parser and fail every structural test that reads the mutated job (validation §3). The lenient reader, and the reader without the indentation check, each fail the test |
| The design is not on `main` at dispatch | closed by the orchestrator, as the task states | the boundary PR `orchestration/boundary-2026-10-11-2` and `gh pr update-branch` before the final audit. The worker runs no `gh pr update-branch` |
| Push and schedule have no PR range | closed | `DecisionTest.test_every_event_but_pull_request_bootstraps` |

The earlier proofs still fail against the new reader at `a35a751e`: 16 of 16 from a01, and 3 of 3 from a01's revise. a01's fourth revise row targeted the removed quoted-key regex and no longer applies; the lenient-reader row replaces it (validation §4).

## Notes

- The full local `make unit-test` fails in the sandbox the same way on `origin/main`: the same failing ids, none only at this head (validation §5). This module passes under it, and CI's `Run Python unit tests` step is the verdict.
- The final head's CI and Bot wait are in the RESULT and the main-checkout copy of this report.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `c62781a9-a65b-4484-925c-383fddb9a114` (validation §6).

cost: n/a

## Final head `fca44b4c` (main-checkout copy)

- Commits: `406ca746` (task copy), `a35a751e` (the fail-closed reader), `fca44b4c` (evidence), pushed together at 07:53:53Z. No `gh pr update-branch` was run here: the orchestrator runs it after the boundary PR merges.
- CI: 13 of 13 pass on `fca44b4c`, the seven required contexts among them; the watcher exited 0 and was joined before the RESULT (validation §7).
- Bot: one round on `fca44b4c`. The code review completed at 07:56:00Z with no review object and no comment, and the Bot reacted 👍 at 07:56:03Z (the security review last ran on `9fcd2b0`). `bot_rounds=1`, no fix round. No thread opened under a02; 4240499289 (a01, `fixed:e872f69f`) is the PR's only Bot thread.
