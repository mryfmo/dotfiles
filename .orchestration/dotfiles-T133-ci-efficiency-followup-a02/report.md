---
task_id: dotfiles-T133-ci-efficiency-followup-a02
seat: claude-standard-dot-a011
branch: tools/ci-efficiency-followup-a02
base: 740772ef (origin/main)
code_commit: 028af504 (row security:4fe2438:1: 380f86d6 red, 0e42cb06 fix; worker review: 73e59b05 red, 02ff2e1c fix; update-branch 7329f0ee; revise 1: 4dacbd60 red, 67180e37 fix; update-branch b0d957cc; rebase repair 1: bc19b1ea red, 028af504 fix)
task_sha256: 4aa89584da50f4085651d9fd3cddb9e913d7ae0557fa8ba283c2eb89b6146dc3 (amendment 1; previous 50599bfdb250510004525e48155a53b954ba6c19af4a2be5d520c9352a3f2466)
---

# Report: dotfiles-T133-ci-efficiency-followup-a02

- Seat: `claude-standard-dot-a011` in `.claude/worktrees/worker-d`. The branch `tools/ci-efficiency-followup-a02` was created with `--no-track` from `origin/main` `740772ef`, after a single-command `git fetch origin main`. PR #421's and PR #410's branches were left untouched; #421 was marked ready (`gh pr ready 421`) at the orchestrator's request before this task started.
- Task file: `50599bfd…`, copied byte-identical to `.orchestration/dotfiles-T133-ci-efficiency-followup-a02/task.md` (validation §1).
- The owned rows sit under `## Owned by dotfiles-T133-ci-efficiency-followup-a02` in `.orchestration/acceptance/dotfiles-T133-ci-efficiency-a02.md`: `security:4fe2438:1 interpreter-selection`, fixed here, and `security:4fe2438:2 path-filter-quoting`, which the task text assigns to PR #421's `git diff -z` change, so this PR does not touch it.

## Row security:4fe2438:1: ci-rerun.sh pins its tools and interpreter

- **The defect.** `signatures()` ran `uv run --offline --no-project --with pyyaml python …` from the caller's working directory, without `--no-config` or `--python`. Run from a PR checkout, that checkout's `.python-version` or `.venv`, or an inherited `UV_PYTHON` or `VIRTUAL_ENV`, chose the interpreter that read `.github/flakes.yaml`. The reservation's `python3 -I` and the gh, jq and git calls came from whatever PATH the caller had.
- **The fix (`0e42cb06`, then `02ff2e1c` after the worker review).** Right after the usage check, before anything reads a checkout:
  - uv, python3, gh, jq, git and mkdir are resolved as `mise which` answers them under `env -i` from `/`, or else `command -v`.
  - A path under a `shims` directory, a relative path or no path exits 1.
  - All except python3 are linked into a private directory made by `/usr/bin/mktemp -d`, with `/bin/ln`. `PATH` becomes those links, then `/usr/bin:/bin`, and the links are removed on exit.
  - python3 is never linked. It is always started by its own path: the reservation runs `"${py}" -I`, and the PyYAML read runs `uv run --no-config --no-project --python "${py}"` under `env -i` (PATH, HOME and `UV_CACHE_DIR` under HOME only), from the root this script lives in. The offline-first, online-fallback order is unchanged.
  - The result: no checkout's `.python-version`, `.venv` or executable, and no inherited `UV_*` (including `UV_PROJECT_ENVIRONMENT` and `UV_PYTHON`), `VIRTUAL_ENV` or `PYTHON*` variable, picks the interpreter.
  - **Why python3 is not linked.** The worker review of `0e42cb06` (P1, reproduced) found that a link breaks the guarantee. CPython reads a `pyvenv.cfg` beside, and one directory above, the path it was started by, without resolving links. A python3 started as `${TMPDIR}/ci-rerun-bin.XXXXXX/python3` would therefore read `${TMPDIR}/pyvenv.cfg`. In a shared `/tmp` (Linux with TMPDIR unset, or sandbox seats sharing a TMPDIR), another user or seat could plant a standard library there.
  - **Why mktemp and ln use system paths.** Before PATH is pinned, they ran through the inherited PATH, where an empty or `.` entry runs a checkout's own. One exception remains, declared (the second worker review's F1): if the script refuses a tool and exits before PATH is pinned, the EXIT trap's `rm` still resolves through the inherited PATH. The fix is the one word `/bin/rm`, left to the orchestrator because a second worker-side round would count toward INV-6.
  - This follows `scripts/orchestrator/orch-gate.sh` (links resolved under `env -i`, shim refusal) and `dispatch.sh` (`env -i` with an allowlist, `--no-config --no-project --python`, from the root).
  - `mkdir` is in the pinned set because the reservation's parent directory is made with it. The uutils regression case therefore still exercises the mkdir its PATH supplies.
- **Test (`380f86d6`).** `tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment`.
  - The helper runs from a fixture checkout. Its `.python-version` names a working fake python (it execs the real one) that writes a marker. A `.venv` holds that fake, and `UV_PYTHON` and `VIRTUAL_ENV` point at it.
  - The helper must still rerun the run (exit 0, one `gh run rerun`), and the marker must stay absent.
  - Red on `380f86d6`: the marker is written. Green at the head (validation §3).
  - From the worker review (`73e59b05`): the same test also plants `mktemp` and `ln` in the checkout and puts an empty entry first on PATH, and these must never run. A new test, `…::test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path`, puts a logging python3 wrapper first on PATH and asserts that every start uses the wrapper's own path, never a link. Both are red on `73e59b05` (0e42cb06's script): the wrapper was started as `…/ci-rerun-bin.*/python3`, and the planted `mktemp` ran. Both are green at the head.
  - `setUp` adds a failing fake `mise`, so every tool resolves through PATH, the stub `gh` first, and no test reaches a real gh.

## The Check

Validation sections are cited as §. Everything ran at `02ff2e1c`, inside the sandbox.

- `uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security tests.unit.test_ci_rerun -v`: 35 tests pass at the head (§3). Red results (§3):
  - On `380f86d6` (the original script), the pinning test fails: the planted interpreter's marker was written.
  - On `73e59b05` (0e42cb06's script), both worker-review cases fail. The interpreter was started as `$TMPDIR/ci-rerun-bin.*/python3`, and the checkout's `mktemp` ran.
- `shellcheck` on `ci-rerun.sh`: clean. `shfmt -i 4 -sr -d` (the repository form): clean. A bare `shfmt -d` asks for tabs on every tracked script. `ruff format --check`: clean (§4).
- `make format`: exit 2 (§5). Its whole-tree shfmt step flags 12 files, all unchanged from `740772ef`. ruff and prettier are clean.
- `make unit-test`, with the sandbox's commit-signing and `mktemp` limits neutralized identically on both sides (§6): 1218 tests at the head and 1216 at the base `740772ef`. Both have the same 44 failures and 10 errors, in `test_agent_stop_gate` (4), `test_gh_auth` (5), `test_herdr_agents` (37) and `test_runtime_health` (8). No test fails at the head that does not also fail at the base. These are inherited failures, not passing.
- Caps (§7): 34 changed lines outside `tests/` and `.orchestration/` (cap 250); 40 under `tests/` (cap 350).
- After the push, `gh run list --branch tools/ci-efficiency-followup-a02 --json name,event,conclusion`, the seven required contexts, the absence of a `private-bootstrap` run on the PR, and the Bot window go in the RESULT, because a record cannot hold its own commit's CI.

## Revise 1 (the chain's P1 on the update-branch head 7329f0ee)

The chain's local review found a P1 at `scripts/orchestrator/ci-rerun.sh:42`. The EXIT trap ran `rm` through the caller's PATH, and the refusal path exits before PATH is pinned, so an `rm` planted first on PATH ran at exit. This was round 2's declared P3, which I had left to the orchestrator. The revise item covers every command the script runs before its PATH pin. Besides the trap's `rm`, that includes the `env` around `mise which`, which runs in every pass of the tool loop, on every run.

- **Fix (`67180e37`).**
  - The trap runs `/bin/rm`, and the loop runs `/usr/bin/env`, as `mktemp` (`/usr/bin/mktemp`) and `ln` (`/bin/ln`) already did.
  - The description now says so. It also names `mise` as the one program found through PATH. `mise` is the resolver that row `security:4fe2438:1` prescribes, and it has no fixed system path. A caller who controls PATH also controls the `command -v` fallback, which round 2 declared as P3 (a).
  - Nothing else changed.
- **Test.** `tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_never_runs_a_path_resolved_command_before_the_pin` puts an `rm` and an `env` that log their names first on PATH. It runs the script on the refusal path (a `jq` under a `shims/` directory, exit 1) and as a full run (exit 0), and requires that neither logged anything.
  - Red on `4dacbd60`, the test on `7329f0ee`'s script (validation §8). The refusal run logged `env` four times and then `rm`; the full run logged `env` six times.
  - Green at `67180e37`: the module's 10 tests pass. shellcheck, `shfmt -i 4 -sr -d` and ruff are clean.
- **Caps** against the new merge base (§8): 35 changed lines outside `tests/` and `.orchestration/` (cap 250), and 60 under `tests/` (cap 350).
- **No worker-side review round.** C-61 counts the pre-push round and this revise as the cap, so the revise's evidence is the red-then-green test and the chain's next run.

## Rebase repair 1 (the comparison lint of main 205fe85c on the update-branch head b0d957cc)

The orchestrator dispatched this repair under D-024-24 as amendment 1, not as a fix round. The dispatched text is `4aa89584…` (previous `50599bfd…`), and the task copy here was swapped to it byte-identical. The amendment adds `scripts/lint-comparisons-baseline.tsv` to `allowed_files`, for baseline rows of pre-existing comparisons only. The 06:05:35Z TASK line named amendment 1 while the text still had the old sha, and the orchestrator corrected it at 06:09:06Z.

PR #415 added `scripts/lint-comparisons.py`. With `main` merged in (`b0d957cc`), the lint's `test_the_changed_files_are_clean_against_the_baseline` fails on `scripts/orchestrator/ci-rerun.sh:46`: `[[ ${found} == /* && ${found} != */shims/* ]]` compares a path by its string form (R1). This branch introduced that line in `0e42cb06`; `main` has no shims check. So the repair normalises the line rather than adding a baseline row, and `scripts/lint-comparisons-baseline.tsv` is unchanged.

- **Fix (`028af504`).** The tool's directory is resolved physically on the same line, `where="$(cd -P -- "${found%/*}" 2> /dev/null && pwd -P)"`. The shims test reads `${where}/`.
  - A relative path, or a directory that cannot be resolved, is still refused.
  - A bare `realpath` of the tool would not do, because a shim link resolves to mise itself.
  - The repair also refuses a PATH entry that is a link to a shims directory. The string check let that through. This follows from normalising the line, and the test case below pins it. Nothing else changed.
- **Test (red `bc19b1ea`, green `028af504`).** `test_ci_rerun_never_runs_a_path_resolved_command_before_the_pin` gains the case `refused through a link`, and every case now checks that a refusal names the shims directory. On `bc19b1ea`, the old check let the link through and the run failed only later, at the stub `jq`.
- **The lint** (validation §9): `uv run --no-project python -I scripts/lint-comparisons.py --changed scripts/orchestrator/ci-rerun.sh`.
  - At `b0d957cc`: exit 1 with the R1 hit, and `test_lint_comparisons` fails `test_the_changed_files_are_clean_against_the_baseline`.
  - At `028af504`: exit 0. Its only output is the five warnings for `regime-ci.py`, an unchanged file. `test_lint_comparisons`: 14 tests OK. `test_ci_rerun`: 10 tests OK. shellcheck, `shfmt -i 4 -sr -d` and ruff are clean.
- **Caps** (§9): 36 changed lines outside `tests/` and `.orchestration/` (cap 250), and 68 under `tests/` (cap 350).

## Changed files

`scripts/orchestrator/ci-rerun.sh`, `tests/unit/test_ci_rerun.py` and `.orchestration/dotfiles-T133-ci-efficiency-followup-a02/**`.

## Evidence, review, cost

- Evidence in `.orchestration/dotfiles-T133-ci-efficiency-followup-a02/`: `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `dotfiles-T133-ci-efficiency-followup-a02-worker-crit.json` and `dotfiles-T133-ci-efficiency-followup-a02-worker-review-receipt.md`.
- Worker-side independent review: two rounds.
  - Round 1, on `0e42cb06`: `Verdict: incorrect`. Its P1 (the link under a shared TMPDIR, so `pyvenv.cfg` chose the standard library) and two P3 were fixed in one worker-side round (red `73e59b05`, fix `02ff2e1c`).
  - Round 2, on `02ff2e1c`: `Verdict: correct`, with five P3, all declared in `dotfiles-T133-ci-efficiency-followup-a02-worker-crit.json`. One of them is the EXIT trap's `rm` on the refusal path. Its fix is the one word `/bin/rm`; it was not applied, because a second worker-side round would count toward INV-6, so the orchestrator decides.
  - Receipt: `dotfiles-T133-ci-efficiency-followup-a02-worker-review-receipt.md`.
- No Understand-Anything hook prompt fired, and no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
