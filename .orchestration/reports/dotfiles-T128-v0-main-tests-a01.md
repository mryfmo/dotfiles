# Report: dotfiles-T128-v0-main-tests-a01

- Seat: `claude-standard-dot-a002` (Claude Code, profile `standard`) in `.claude/worktrees/worker-c` (bring-up PING `bringup-1791667546-81678` answered `alive`, message 267).
- Task file read in full; its sha256 `f16cbd9cecdfc3a0dbe345f376b6f36a8ae7b698c06e3703ab79d956783a41a8` matched the AGMSG-TASK token, and the round-1 amendment's `61554db0d12e73fabd3ba04d078fc29c42a93bbb3fdca3c2ddd129181ff8996f` matches the revise ACCEPTANCE token; the branch copy is recommitted byte-identical at that hash in `c5b7802c`. Design context read from `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` on `origin/main` (INV-12, INV-2 caps, section 6 waves).
- Branch `feat/main-tests` from `origin/main` `b896d9bc` (`git switch -c feat/main-tests --no-track origin/main`). Draft PR #317 (`feat(ci): run main's unit tests against a pull request's scripts`), opened at 00:11Z with the first commit alone. Final head `32fe9a36a6ca67670e54bbcb1c506ca391d9dd32` (revise round 1; round 0 ended at `adcf783b`).
- First commit `efd8b66b`: the task file byte-identical at `.orchestration/dotfiles-T128-v0-main-tests-a01/task.md` (sha256 above, validation §1). The artifacts are at the AGMSG-TASK's `expected_*` paths, which I took as authoritative over the task file's "evidence beside it".

## What changed

1. `scripts/main-tests.sh <base>` (149 lines, shdoc header, mode 755 like its siblings). When `git diff --no-renames $(git merge-base <base> HEAD)..HEAD` touches a script path (`scripts/**`, `home/dot_local/bin/**`, `install/**`, `home/.chezmoiscripts/**`, `setup.sh`), it extracts `git archive HEAD` to a temporary directory and reads the range's single `.orchestration/*/task.md` (more than one fails; none means undeclared mode for everything). Then:
   - (b0) design tier (a missing or unknown `tier:` counts as design): every declared non-data script needs its `tests/unit/test_<name>.py` declared, else `main-tests: design script <path> has no declared contract module <module>`, and each declared module must exist in HEAD, else `main-tests: declared module <module> deleted`;
   - (c) promotion: for a task id not ending in `-contract-a01`, the PR's own copy of each declared module (read before the overlay) must carry no contract decorator, else `main-tests: contract still dormant in <module>`;
   - it then replaces the copy's `tests/unit` with `git archive <base> tests/unit` (`rm -rf` first, so a file the PR adds there, such as a `unittest.py`, cannot shadow main's);
   - (a) undeclared mode: every `tests/unit/test_*.py` on the base runs as it is, except an exempt one (declared in the task.md together with its script). It runs as `uv run --no-config --no-project --python <found from /> python -P -m unittest <names>` from the temporary root with `PYTHONPATH=tests/unit`. Each module's own-path `ROOT` lands on the PR tree; `-P` keeps the PR root off `sys.path`; `--no-config` ignores a `uv.toml` the PR adds; and the explicit interpreter keeps uv from probing a `.venv` the PR plants. A run counts only with unittest's own `Ran <n> tests` (n > 0) and final `OK`;
   - (b) declared mode: for each exempt module, only the `@contract` test methods of main's copy run, with `REGIME_CONTRACT=1`, and the summary's count must equal the number of ids. The ids come from `ast`, so ordinary tests are not selected, and an empty contract class contributes none. A design-tier module whose main copy has no contract, or that main does not have, fails with `main-tests: no contract on main for <module>`.
   - The exit status combines every check. With no script change it prints `main-tests: no script change` and exits 0.
2. `scripts/lib/contract_markers.py` (118 lines): `task` (PyYAML front matter: id, normalised tier, declared modules, exempt modules, uncovered design scripts; malformed front matter exits non-zero), `scripts` (the script-path filter, the one place the list is written), `contracts` (unittest ids of contract-decorated test methods, a decorated class contributing its own) and `dormant`. The decorator forms it resolves are `from regime_contract import contract [as X]` (and `*`), `import regime_contract [as Y]` with `@Y.contract`, and an inline `skipUnless(...)` whose arguments contain `'REGIME_CONTRACT'`. A nested contract counts as dormant too.
3. `tests/unit/regime_contract.py`: `contract = unittest.skipUnless(os.environ.get("REGIME_CONTRACT") == "1", "dormant contract")` and the contract-PR and promotion note.
4. `.github/workflows/test.yaml`: job `main-tests` (ubuntu-24.04, `needs: changes`, no job-level `if`, checkout `fetch-depth: 0` without persisted credentials, setup-uv at the pinned SHA the test job uses). Its first step runs `git fetch --no-tags origin main` and copies `origin/main:scripts/lib/github-release.sh`, `origin/main:scripts/main-tests.sh` and `origin/main:scripts/lib/contract_markers.py` into `$RUNNER_TEMP/scripts/`. The install step sources main's `github-release.sh` from there, and the last step runs `bash "$RUNNER_TEMP/scripts/main-tests.sh" origin/main`. When main has no copy (this PR only), it prints `main has no <path>; running this PR's copy` and copies the PR's file. **The acceptance record should say this PR ran the PR's own harness.**
5. SKILL: Worker Playbook step 16 (the two-mode protocol in one paragraph), and one sentence in Orchestrator Playbook step 3 naming the harness files and the job as an operator-routed gate source "as `scripts/require-crit-review.py` is". That second edit is my reading of item 2's "join the operator-routed gate sources": no list of them exists in the repository, and step 3 is where routing lives.
6. `tests/unit/test_contract_markers.py` (10 tests) and `tests/unit/test_main_tests.py` (20 tests over scratch repositories whose `main` holds a module with an ordinary and a contract test, each resolving `ROOT` from its own path). Decorator samples live in strings, so this PR's own modules carry no real contract decorator for the promotion check to find.

## Decisions the task's step list did not name

- **Declared modules are `tests/unit/test_*.py` entries only.** `tests/unit/regime_contract.py` is a helper, not a test module. Counting it would make every design-tier task fail "no contract on main" for it.
- **The deleted-module check is design tier only**, read from its place inside (b0). A review-tier deletion is left to the audit (INV-12's "a deleted ... fails-when-removed test is a conformance finding").
- **More than one task.md in the range fails the run**, because the task says "the single `.orchestration/*/task.md`".
- **Tools the job installs.** `jq` and `zsh` (as the test job's Python step), and chezmoi through the test job's verified path: release tag from `scripts/lib/github-release.sh`, checksum, and `github_release_attestation` (exits 1 when it fails), without the fixture checks. The first run on `3e715ef5` errored five modules on a missing `chezmoi`.
- **Temporary directory.** `mktemp -d "${TMPDIR:-/tmp}/main-tests.XXXXXX"`: macOS `mktemp -d` ignores `$TMPDIR`, and the Claude sandbox denies its default.
- **Bash 3.2.** The declared list is a newline string read with `while read`. macOS bash 3.2 cannot expand an empty array under `set -u`, and the macOS test job runs the harness through `test_main_tests.py`.
- **`9b8a62a2` → `9e841365`.** The uncovered-script scenario left the PR's contract dormant, so removing the uncovered-script rule kept it green. The scenario now promotes.
- **`9e841365` → `56d887dd`, runner isolation.** Undeclared mode ran `python -m unittest` from the PR tree with `tests/unit` on `PYTHONPATH`, and the overlay kept files the PR added there. A PR-added `tests/unit/unittest.py` or root `unittest.py` containing `raise SystemExit(0)` replaced the standard library's runner, so the harness exited 0 without running main's tests (reproduced in a scratch directory before the fix). The overlay now replaces `tests/unit` wholesale, Python runs with `-P`, and every uv call takes `--no-config`. Two scenarios cover it.
- **`56d887dd` → `adcf783b`, a failing helper fails the run.** The script-change check read the helper inside `[ -z "$(...)" ]`, where `set -e` does not apply, so a helper that failed (uv unable to fetch PyYAML, for one) printed nothing and the harness reported `no script change` and exited 0. The mutation run exposed it when removing `--no-config` left its test green. The helper's output, and main's module list, are now assigned before use; `test_a_helper_failure_fails_the_run` points `UV_INDEX_URL` at a dead index. All 18 rule removals failed their test at that head.
- **PR size.** 334 added lines outside `tests/` and `.orchestration/` (cap 500), 438 under `tests/` (cap 1000), 7 changed files outside `.orchestration/` (cap 15) (validation §1 numstat).

## Revise round 1

The audit of `adcf783b` (`Verdict: incorrect`) and the task's "Revise round 1" section. Each check below failed on the `adcf783b` code and passes at the final head (validation §R); `.orchestration/dotfiles-T128-v0-main-tests-a01/revise.yaml` records them with `previous_head: adcf783b06d9081280991a3727f8a21c3c61ac85`. Fix commit `c5b7802c`, plus `32fe9a36` for one extra check.

1. (P1, `test.yaml:108`) A new first step, "Fetch main's harness and helpers", runs `git fetch` and writes `origin/main:scripts/lib/github-release.sh` and the harness pair to `$RUNNER_TEMP/scripts/`. The install step sources `"${RUNNER_TEMP}/scripts/lib/github-release.sh"`, and only the harness pair falls back to the PR's copy (the comment says so). Check `test_nothing_from_the_pr_runs_before_mains_harness`: in the job, every `source`/`.`/`bash`/`sh` target is under `${RUNNER_TEMP}/`, the fetch precedes the first `source`, and there is exactly one `cp "${path}"` fallback, the one over the harness pair.
2. (P1, `main-tests.sh:32`) **`--isolated` does not prevent it, so I did not use it.** A scratch `.venv/bin/python` that writes a marker ran under `uv run --no-config --no-project`, under `--with pyyaml`, and under `--isolated`: uv's discovery executes it while probing interpreters. It did not run with an explicit `--python <path>`. The harness now resolves `python="$(cd / && uv python find --no-config)"` once, from `/`, and passes `--python "${python}"` to every uv call (validation §R pastes the probe). This also keeps a PR's `.python-version` from choosing the interpreter. Check `test_a_planted_venv_is_not_used`: a planted `.venv/bin/python` and `python3` that `touch` a marker, and the marker must not exist after a passing run.
3. (P1, `main-tests.sh:119`) `run_unittest` tees unittest's output and requires its own summary: a last `Ran <n> tests` with `n > 0` (and `n` equal to the contract-id count in declared mode), and a final `OK` or `OK (...)` line. Otherwise it prints `main-tests: no complete unittest summary (...)` and fails. Check `test_a_zero_exit_without_a_summary_fails`: main's module runs a PR script that calls `os._exit(0)` at import. I also added `test_a_short_contract_summary_fails` (`32fe9a36`) for the count: a PR script prints a forged one-test `OK` summary and exits while two contracts are selected.
4. (P1, orchestration) The helper prints `exempt` for a declared module only when the task.md declares its script too (`module_for`). Only exempt modules leave undeclared mode and get contract-only runs. Declared modules still get the promotion and deleted-module checks. Check `test_a_declared_module_without_its_script_stays_undeclared`. Step 16 of the SKILL says the same.
5. (P2, `main-tests.sh:36`) Both `git diff` calls take `--no-renames`. Check `test_a_renamed_script_still_triggers` (`scripts/foo.sh` moved to `elsewhere/foo.sh`).
6. (P2, `contract_markers.py:88`) `contracts` lists test methods only: a decorated class contributes its own `test*` methods, so an empty one contributes nothing and reads as `no contract on main`. The declared-mode count check (item 3) backs it. Check `test_an_empty_contract_class_is_no_contract`.
7. (P2, evidence) The orchestrator's; no worker action.

All 25 rule removals (the round-0 rules and these seven) fail their test at the final head (validation §2).

**Residual risks:**
- Code that main's tests import from the PR runs inside the unittest process, so it can still print a forged summary with the right count and exit 0. Item 3 catches early exits and short counts, not a forgery that knows the count; in undeclared mode any count above zero is accepted.
- The job's YAML still comes from the PR's own workflow file (unchanged from round 0's note).

## main-tests on this PR fails by design

The design-tier rule applies to this PR itself. The task.md has no `tier:` stamp, so it counts as design, and main holds no contract for `tests/unit/test_main_tests.py` or `tests/unit/test_contract_markers.py`. Both the local run and the CI job print those two `no contract on main` lines and exit 1. Undeclared mode passes: CI ran all 925 of main's tests `OK` (validation §5). V0 is the wave that "ships its script and its test together", and `main-tests` is not a required check until the operator lists it. Proposed sweep disposition for the job's failure: `not-applicable: V0 bootstrap - main-tests fails only on "no contract on main" for this PR's own two modules, which main cannot hold before V0 merges; all 925 main tests pass in the same run (contract-first starts at V1 per the task file)`.

## Invariants

- invariant: INV-12 → tests/unit/test_main_tests.py::test_an_undeclared_script_change_meets_mains_ordinary_tests, scripts/main-tests.sh:143
- invariant: INV-12 → tests/unit/test_main_tests.py::test_a_declared_script_meets_mains_contract_only, scripts/main-tests.sh:147
- invariant: INV-12 → tests/unit/test_main_tests.py::test_a_design_tier_module_needs_a_contract_on_main, scripts/main-tests.sh:117
- invariant: INV-12 → tests/unit/test_main_tests.py::test_an_implementation_must_promote_its_contracts, scripts/main-tests.sh:91
- invariant: INV-12 → tests/unit/test_main_tests.py::test_aliased_and_inline_contracts_are_still_dormant, scripts/lib/contract_markers.py:56
- invariant: INV-12 → tests/unit/test_main_tests.py::test_a_deleted_module_still_runs_from_main, scripts/main-tests.sh:98
- invariant: INV-12 → tests/unit/test_main_tests.py::test_files_the_pr_plants_cannot_replace_mains_runner, scripts/main-tests.sh:97
- invariant: INV-12 → tests/unit/test_main_tests.py::test_a_uv_config_the_pr_plants_is_ignored, scripts/main-tests.sh:36
- invariant: INV-12 → tests/unit/test_main_tests.py::test_a_helper_failure_fails_the_run, scripts/main-tests.sh:43
- invariant: INV-12 → tests/unit/test_main_tests.py::test_design_scripts_need_declared_modules_that_exist, scripts/main-tests.sh:74
- invariant: INV-12 → tests/unit/test_main_tests.py::test_an_install_change_triggers_the_run, scripts/lib/contract_markers.py:16
- invariant: INV-12 → tests/unit/test_main_tests.py::test_no_script_change_skips, scripts/main-tests.sh:45
- invariant: INV-12 → tests/unit/test_main_tests.py::test_more_than_one_task_file_fails, scripts/main-tests.sh:62
- invariant: INV-12 → tests/unit/test_main_tests.py::test_nothing_from_the_pr_runs_before_mains_harness, .github/workflows/test.yaml:125
- invariant: INV-12 → tests/unit/test_main_tests.py::test_a_planted_venv_is_not_used, scripts/main-tests.sh:30
- invariant: INV-12 → tests/unit/test_main_tests.py::test_a_zero_exit_without_a_summary_fails, scripts/main-tests.sh:132
- invariant: INV-12 → tests/unit/test_main_tests.py::test_a_short_contract_summary_fails, scripts/main-tests.sh:133
- invariant: INV-12 → tests/unit/test_main_tests.py::test_a_declared_module_without_its_script_stays_undeclared, scripts/lib/contract_markers.py:46
- invariant: INV-12 → tests/unit/test_main_tests.py::test_a_renamed_script_still_triggers, scripts/main-tests.sh:41
- invariant: INV-12 → tests/unit/test_main_tests.py::test_an_empty_contract_class_is_no_contract, scripts/lib/contract_markers.py:95
- invariant: INV-12 → tests/unit/test_contract_markers.py::test_every_form_is_found_on_its_method, scripts/lib/contract_markers.py:70
- invariant: INV-12 → .github/workflows/test.yaml:79 (the main-tests job runs main's copy of the harness; validation §5)

## Notes for the orchestrator

- **Sequencing:** list `main-tests` as a required check only after #317 merges. It is red on #317 by design, so requiring it first would block this PR.
- uv still reads a `.python-version` the PR adds (`--no-config` covers `uv.toml` and `pyproject.toml`). The file can only pick a CPython version from uv's default source; one without `-P` (older than 3.11) or one that cannot be fetched fails the run rather than passing it. The `test` job's `make unit-test` honours a PR-planted `uv.toml` as it always has; that is outside this wave.
- The job's YAML runs from the PR's own workflow file, so a PR could still rewrite the job. The routing sentence plus V1's refusal of workflow changes outside a design-tier task.md are what close that. This wave adds no check for it.
- The fallback to the PR's harness copy stays in the job after merge but is taken only while `origin/main` lacks the file. A PR that deletes the harness is still judged by main's copy, and main's `test_main_tests.py` would fail it in undeclared mode.
- Local suite: in this sandbox `make unit-test` on unchanged main fails 114 tests and errors in 103 (host-access tests). The harness's undeclared mode at the final head fails exactly the same 223 ids (validation §4). `test_statusline_tools` timed out once on its 1-second `ccstatusline` launch, then passed on rerun (validation §1, both runs pasted).
- `public-bootstrap` on `9b8a62a2` failed once on a snapcraft API timeout (`HTTP 408` fetching the `mesa-2404` assertion during `chezmoi apply`); the other two jobs were cancelled by fail-fast. I reran the failed jobs (validation §5).
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

The task file carries no `[memory:...]` marker, so the decision recorded is this wave's outcome. Command (main checkout, outside the sandbox through the permission gate; validation §6 pastes it with its output):

```
cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128 wave V0 (worker claude-standard-dot-a002, 2026-10-11, PR 317): scripts/main-tests.sh overlays main tests/unit on a git-archive copy of the PR tree … on PR 317 itself it fails by design on two no-contract-on-main lines (V0 bootstrap) while all 925 main tests pass.'
```

Printed id: `c64e9528-04e1-4075-900a-34e53f044946`. Round 1 adds a second decision (validation §6): uv executes a planted `.venv` interpreter even with `--isolated`, so the harness passes `--python` resolved from `/`, plus the summary, exemption, rename and contract-id rules. Printed id: `6f5e1dc2-27b4-4a10-8e09-5d0e7c0c12d7`.

## CI and Bot

- CI at the final head `32fe9a36`: 14 of 15 checks pass, including the four `test` jobs (each runs `test_main_tests.py`; my local runs used macOS `/bin/bash` 3.2.57), three `public-bootstrap`, `validate` and `changes`. `main-tests` fails by design (above) after `Ran 925 tests ... OK` (validation §5).
- Bot: the step-15 loop on `32fe9a36` ran from 02:03:04Z to 02:18:05Z and found no Bot review or top-level comment: `bot: none` (validation §7). No Codex Bot activity exists on the PR at any head. The PR is a draft, as the task asked, and every recent task PR the connector reviewed (#312, #314, #315) was opened ready. If you want a Bot review before integration, the PR needs `gh pr ready 317` (I left it draft). CodeRabbit posted only its "Review skipped: Auto reviews are disabled" notice.
- Threads: none. Nothing to fix or disposition; I resolved nothing.
- Sweep items I expect: the `main-tests` check failure and its `Process completed with exit code 1` annotation (proposed disposition above), and the CodeRabbit notice (an issue comment with no finding).

cost: n/a
