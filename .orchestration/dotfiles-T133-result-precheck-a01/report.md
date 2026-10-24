---
task_id: dotfiles-T133-result-precheck-a01
round: 1
revise: 1
amendment: 2
status: precheck-recorded
---

# Report

Worker `claude-standard-dot-a009` (Claude Code, worker-c), branch `tools/result-precheck-a01` from `origin/main` 99a4a80f, code commits de167fa1, 105e42cf (Amendment 2's header line), a7b0da2f (the Bot fix round) and bdd8ab81 (revise round 1), PR #411. Task copy `.orchestration/dotfiles-T133-result-precheck-a01/task.md` is byte-identical to the twice-amended dispatched file: sha256 `05caa77f064b809185138817d869ae0b4fc52ef76863715d1e6d998134ac011f` (Amendment 2's `task_sha256`). Parked PR of item 0: #406 (`tools/omp-config-render`, head 2e978db7c4325f477630234a78a6f7701e45c92e).

## Item 0

Done before item 1: the two parked records of `dotfiles-T129-omp-config-render-a01` committed as 2e978db7 (with three corrections to statements the 08:51 JST STOP had made untrue: the `local-validated` status, a baseline worktree never made, a validation.md never written), pushed, and opened as draft PR #406 with the task's title and body. The classifier denied the item 0 PONG and the branch switch; the orchestrator recorded item 0 from the blocked PONG (message 2090) and re-tasked the switch, which then ran inside the sandbox (sandbox.md).

## What changed

- `scripts/orchestrator/result-precheck.sh` (new, 245 lines): item 1 as amended. Checks `unit-test`, `render-check`, `format` (Amendment 1: CI's `shfmt`, `ruff format` and `prettier` commands in CI's scopes, the three CI lines pasted in the header), `shellcheck`, `secrets` and `local-review` (deferred by default, with the task's two shortcut comments), the selector proof, `precheck.json`, `result.txt` and the `precheck=` line. Modes `--secrets <file>` (pre-push) and `--staged` (pre-commit, on the staged blobs since revise round 1).
- `.githooks/pre-commit` (new, 13 lines): `result-precheck.sh --staged`, so the CI scopes live in one place.
- `.githooks/pre-push` (new, 24 lines): item 2's ranges through `result-precheck.sh --secrets`, as the patch of every commit in the range (`git log -p --cc`, the fix round) rather than the net diff.
- `scripts/orchestrator/dispatch.sh` (+67/-1): item 3, one block (the `PRECHECK_REQUIRED` read, an embedded Python checker run under the script's allowlisted environment from the root, and `precheck_gate` called on both send paths) and one header paragraph plus the `@env` line; since the fix round the checker also requires `status=ready_for_review` and a record with no failed check or selector.
- `tests/unit/test_result_precheck.py` (new, 318 lines): the seven tests item 4 names, two of them extended in the fix round, and revise round 1's `test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree`.

Caps on the final code head bdd8ab81: 350 changed lines outside `tests/` and `.orchestration/` (cap 350), 318 under `tests/` (cap 450).

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

## The precheck on this head (question of message 2111, decided as (a) by Amendment 2)

The Check's command, `scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a01`, exits 1 inside a Claude seat's sandbox: its `unit-test` check runs `make unit-test`, which fails 296 tests there (189 failures, 107 errors, in test_require_crit_review, test_herdr_agents, test_agent_stop_gate, test_ua_symbol_coverage, test_update_agent_assets, test_runtime_health, test_gh_auth, test_supply_chain_policy, test_aws_cli_acquisition). The identical 296 fail on a pristine `origin/main` 99a4a80f worktree in the same sandbox (`cmp` of the sorted names: equal), and none is in this task's modules; every other check of that run passed (`precheck=c9c80f1fde3fb65d0d0e8dd42cc73afc07a92cd6a31b60a5014124b4092fe9b1`, its precheck.json pasted in validation.md). I asked the orchestrator (message 2111) with three options; Amendment 2 decided (a) and added the header's second `shortcut:` line (105e42cf, which also drops one redundant comment line so the cap holds). Amendment 2's form ran on 105e42cf, `scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a01 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools`: exit 0, 63 tests OK, `precheck=862c3566250a09767c00e329a4f47c7bee1f992cb128c6400a57a0c79f476f14`; the fix round's head a7b0da2f gave `precheck=24beae719509c95f0ce01317ab24675b7e6db1152b9cb1d44d3cf5095a282f32`, and the committed record is revise round 1's run on bdd8ab81 with the `check=` selector: exit 0, `precheck=c7aaf1cf96b9a25dbed4b583ba3e2c74ef2227ebfe05d84444c9e7861ede2ad4`. An earlier `--tests` run with file paths on de167fa1 (`precheck=8e6922eb…`, commit 50b265d8) is superseded. CI's `make unit-test` is the authority for the full suite. Consequence for plan 024: no Claude seat can pass the default `unit-test` check in its sandbox until those tests stop depending on what the sandbox denies.

[memory:failure] In a Claude seat's Bash sandbox `make unit-test` fails 296 tests that pass in CI (the same set on origin/main 99a4a80f), so result-precheck.sh's default `unit-test` check cannot be green there; a seat records a `--tests` run of its own modules and CI decides the full suite.

## The Bot's review of 1763da66 (06:01:15Z, at `gh pr ready`), and the fix round a7b0da2f

- 4305945403 (P1, `.githooks/pre-push`: the net diff of two endpoints misses a token added and removed again before the push): fixed:a7b0da2f. The hook scans `git log -p --cc --format= <remote>..<local>`, every commit's patch; the pre-push test gains that branch and fails on the pre-fix hook (validation.md).
- 4305945407 (P1, `dispatch.sh`: a record with a failed check, or a `status=blocked` RESULT, passed the gate): fixed:a7b0da2f. The gate requires the newest RESULT's `status=ready_for_review`, a non-empty `checks` list with no `ok: false`, and every selector `ok: true`; the dispatch test gains both cases and fails on the pre-fix script on exactly those two.
- 4305945406 (P2, `result-precheck.sh --staged` reads the working tree, not the index): fixed:bdd8ab81 in revise round 1 (ACCEPTANCE of 06:26:12Z, C-50). `--staged` exports the whole index with `git checkout-index -a` into its work directory and runs the checks there with `GIT_DIR`, `GIT_WORK_TREE` and an absolute `GIT_INDEX_FILE` (a hook's own may be relative), so every tracked config applies as in CI; `test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree` fails on 3f5177a9's script and passes on bdd8ab81 (validation.md).

Under the no-prompt rule of 05:07Z no `@codex review` was posted, so the fix round's head has no Bot review (`bot_rounds=1`).

Observation for plan 024 (no code change; item 1 states it this way): the selector proof runs each selector from the previous head's own checkout, so a test the revise round modified runs in its old form there and passes, and a test the round added does not exist there (unittest exit 5 counts as red). A proof of a modified test would run the current test file against the previous head's code.

## Not done yet

CI on the final head and the RESULT (`parked_pr=406`).

cost: n/a
