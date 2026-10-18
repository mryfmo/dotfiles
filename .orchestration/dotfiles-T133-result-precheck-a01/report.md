---
task_id: dotfiles-T133-result-precheck-a01
round: 1
amendment: 1
status: precheck-recorded
---

# Report

Worker `claude-standard-dot-a009` (Claude Code, worker-c), branch `tools/result-precheck-a01` from `origin/main` 99a4a80f, code commit de167fa1. Task copy `.orchestration/dotfiles-T133-result-precheck-a01/task.md` is byte-identical to the amended dispatched file: sha256 `247e7a44f764f3d939f18278c10e380a92909cce38583e28b1cd07d2d7a5a7a8` (Amendment 1's `task_sha256`). Parked PR of item 0: #406 (`tools/omp-config-render`, head 2e978db7c4325f477630234a78a6f7701e45c92e).

## Item 0

Done before item 1: the two parked records of `dotfiles-T129-omp-config-render-a01` committed as 2e978db7 (with three corrections to statements the 08:51 JST STOP had made untrue: the `local-validated` status, a baseline worktree never made, a validation.md never written), pushed, and opened as draft PR #406 with the task's title and body. The classifier denied the item 0 PONG and the branch switch; the orchestrator recorded item 0 from the blocked PONG (message 2090) and re-tasked the switch, which then ran inside the sandbox (sandbox.md).

## What changed

- `scripts/orchestrator/result-precheck.sh` (new, 242 lines): item 1 as amended. Checks `unit-test`, `render-check`, `format` (Amendment 1: CI's `shfmt`, `ruff format` and `prettier` commands in CI's scopes, the three CI lines pasted in the header), `shellcheck`, `secrets` and `local-review` (deferred by default, with the task's shortcut comment), the selector proof, `precheck.json`, `result.txt` and the `precheck=` line. Modes `--secrets <file>` (pre-push) and `--staged` (pre-commit).
- `.githooks/pre-commit` (new, 13 lines): `result-precheck.sh --staged`, so the CI scopes live in one place.
- `.githooks/pre-push` (new, 24 lines): item 2's ranges through `result-precheck.sh --secrets`.
- `scripts/orchestrator/dispatch.sh` (+70/-1): item 3, one block (the `PRECHECK_REQUIRED` read, an embedded Python checker run under the script's allowlisted environment from the root, and `precheck_gate` called on both send paths) and one header paragraph plus the `@env` line.
- `tests/unit/test_result_precheck.py` (new, 284 lines): the seven tests item 4 names.

Caps: 350 changed lines outside `tests/` and `.orchestration/` (cap 350), 284 under `tests/` (cap 450).

## Choices the task text left open

- The precheck refuses (exit 2) a tree with changes outside `.orchestration/<task>/`, so `precheck.json` never attests checks run on uncommitted code.
- A masker failure removes the check logs and writes no record (fail closed: an unmasked log is never left for the commit).
- `--staged` is an added mode of `result-precheck.sh` so the pre-commit hook reuses item 1's `format` and `shellcheck` checks instead of a second copy of CI's scopes.
- The dispatch gate also refuses a `task_id` that is not a task id (it becomes a path and a pathspec), and the evidence-only condition is one `git diff --quiet <field> <head> -- . ':(exclude).orchestration/<task>/'`, so a diff error cannot pass.
- Without an acceptance record dispatch.sh reads no window (premise 1's read happens only in the record path), so an accepted ACCEPTANCE sent without a record counts as missing its RESULT: a warning by default, a refusal under `PRECHECK_REQUIRED=1`.
- The `secrets` count is the masker's own `masked <n> match(es)` figure; the match itself is the byte difference, as item 1 states.
- A selector naming a test that does not exist on the previous head counts as red there (unittest exits 5, "NO TESTS RAN"); the exits are recorded, so the reviewer sees 5 against 1.

## Tests and the controls they close

`uv run python -m unittest tests.unit.test_result_precheck tests.unit.test_orchestrator_tools -v`: 63 tests green (7 new, 56 existing; validation.md). The tests were written after the scripts, so a mutation check (validation.md) stands for the red run: each control disabled in turn made its test fail (the gate call in dispatch.sh: 5 failures; the pre-push refusal; the secrets comparison; the pre-commit hook), and every file was restored and its hash verified.

## The precheck on this head (question of message 2111, default (a))

The Check's command, `scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a01`, exits 1 inside a Claude seat's sandbox: its `unit-test` check runs `make unit-test`, which fails 296 tests there (189 failures, 107 errors, in test_require_crit_review, test_herdr_agents, test_agent_stop_gate, test_ua_symbol_coverage, test_update_agent_assets, test_runtime_health, test_gh_auth, test_supply_chain_policy, test_aws_cli_acquisition). The identical 296 fail on a pristine `origin/main` 99a4a80f worktree in the same sandbox (`cmp` of the sorted names: equal), and none is in this task's modules; every other check of that run passed (`precheck=c9c80f1fde3fb65d0d0e8dd42cc73afc07a92cd6a31b60a5014124b4092fe9b1`, its precheck.json pasted in validation.md). I asked the orchestrator (message 2111) with three options and the default (a), unanswered when this record was written: the committed record is the `--tests` run on this task's two modules, `scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a01 --tests tests/unit/test_result_precheck.py tests/unit/test_orchestrator_tools.py`, exit 0, `precheck=8e6922eb46297b0b5be3c5ec6c8ccc00d27858c119c9220f2ee5f74506f031dc`, with `head` de167fa1. CI's `make unit-test` is the authority for the full suite. Consequence for plan 024: no Claude seat can pass the default `unit-test` check in its sandbox until those tests stop depending on what the sandbox denies.

[memory:failure] In a Claude seat's Bash sandbox `make unit-test` fails 296 tests that pass in CI (the same set on origin/main 99a4a80f), so result-precheck.sh's default `unit-test` check cannot be green there; a seat records a `--tests` run of its own modules and CI decides the full suite.

## Not done yet

The push, the PR, CI, the Bot wait and the RESULT (`parked_pr=406`).

cost: n/a
