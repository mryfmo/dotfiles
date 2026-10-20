---
task_id: dotfiles-T133-trusted-exec-contract-tests-a01
seat: claude-standard-dot-a011
branch: tools/trusted-exec-contract-tests-a01
base: ba318e53 (origin/main at the branch point)
code_head: f4eed1cc (e603ac51 task copy; 755d9002 tests, red; 4729b83c helper; f4eed1cc the worker review's fix round)
task_sha256: dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c
---

# Report: dotfiles-T133-trusted-exec-contract-tests-a01

- **Seat and branch.** Seat `claude-standard-dot-a011` in `.claude/worktrees/worker-d`. The branch `tools/trusted-exec-contract-tests-a01` was created with `--no-track` from `origin/main` `ba318e53`. The task copy is byte-identical to the dispatched text `dd754911…` (validation §1).
- **Premises.** Re-run at worker start: Python 3.15.0, Darwin, `dscl` present and `getent` absent, the helper absent from `origin/main`, `origin/main` at `ba318e53` (validation §2). The absolute interpreter is the observed `python3`'s real path, `…/mise/installs/python/3.15.0/bin/python3.15`.
- **Design.** Section 5.14 items 2, 3, 7 and 9 apply by reference (D-024-30). This record names the items and does not restate them.
- **Interruption.** Between the helper and its records, the orchestrator's amendment 1 to `dotfiles-T128-chain-review-scripts-followup-a06` was handled on PR #434 (`af862335`, its own RESULT), and this branch was untouched meanwhile.

## What the helper provides

`tests/unit/trusted_exec_contract.py` uses the standard library only. It exposes plain functions and one mixin.

- **The fixture factories** `shim_path(env=None)`, `hostile_git()`, `worker_root()` and `swapped_file()` are `functools.partial` objects over one context manager. It makes a temporary directory, builds the probe there, and removes it on exit, an exception included.
- **The mixin** `TrustedExecContractMixin` gives `enter()`, a `TestCase.enterContext` that also works on Python 3.10, and `shim_probe()`, `hostile_git_probe()`, `worker_root_probe()` and `swapped_file_probe()`.
- **Standalone functions:** `parse_env`, `assert_sanitized_env`, `repository_root`, `passwd_home`, `run_under_trusted_parent` and `TrustedExecRefused`.

The six requirements:

1. **Shim on PATH.** `ShimProbe` puts failing shims of `uv`, `python3`, `gh`, `git` and `bash` first on the offered PATH. Each records its name and complete argv as a JSON line through an absolute interpreter, and exits 97. `assert_none_ran()` raises with each recorded run.
2. **Hostile Git.** `HostileGit` makes a legitimate and an attacker repository, with distinguishable `probe.txt` contents. `attack(kind)` offers three attacks, each exercised separately:
   - `environment` exports the six named `GIT_*` variables.
   - `local-worktree` plants `core.worktree` in the fixture repository's own `.git/config`, removed on exit.
   - `local-include` plants an `include.path` whose file sets `core.fsmonitor` to an attacker program.

   `assert_unaffected(root, content)` reports an attacker root, attacker content or an attacker program that ran. The measurements behind the payloads are in learning item 1: `-c core.worktree` does not undo a local `core.worktree` but `--work-tree` does, and an included `core.worktree` is inert while an included `core.fsmonitor` runs.
3. **Worker root.** `WorkerRoot` provides an input, an output and a not-yet-created output under `<root>/.claude/worktrees/probe-seat/`.
   - A read shows as the input's access time leaving 0. When it starts, the probe measures on a scratch file that a read moves a zeroed access time, and refuses to run where it does not.
   - A write, append, replacement or removal of either file shows as a changed inode, size or mtime, or a missing file. Creating the new output shows as its directory existing.
4. **Swapped file.** `SwappedFile.swap()` is the deterministic barrier, with no sleep and no loop. It makes the checked name a link to attacker content.
   - `assert_not_consumed(data)` refuses attacker bytes. It also refuses a consumer that never reached the barrier ("never swapped"), so a skipped barrier cannot pass vacuously.
   - The case-alias subcase uses the case-flipped name when `samefile` measures it to be the same file. Otherwise `alias` is None, with the measured reason, and the test reports the subcase as skipped, never passed.
5. **Sanitized environment.** `assert_sanitized_env(observed, declared=())` requires the name set to equal `PATH`, `HOME`, `LANG` and the declared names, with `PATH=/usr/bin:/bin`.
6. **Trusted parent.** `run_under_trusted_parent(script, *args)` runs the following, with `env={}` and stdin closed:

   ```text
   /usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <realpath of script> [args...]
   ```

   - `passwd_home()` asks the directory service for the real UID's account, never `HOME` or PATH: `/usr/bin/dscl . -read /Users/<name> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux.
   - `repository_root()` comes from the module's own path.
   - Before anything runs, it refuses a relative path, a script that resolves outside the root (traversal, sibling prefix, symlink) and a non-regular file.

## Tests and the selectors

`tests/unit/test_trusted_exec_contract.py` (`TrustedExecContractTest`) was written first and was red at `755d9002`: the module did not exist (validation §4). Each `case_*` function runs a deliberately noncompliant consumer stub, which must make the probe assertion fail for the intended reason, then a compliant stub, which must pass. It returns the observed failure text (validation §6).

The selectors:

- `test_each_probe_detects_condition` runs the six cases as subtests.
- `test_shim_probe`, `test_hostile_git_probe`, `test_worker_root_probe`, `test_swapped_file_probe`, `test_sanitized_environment_probe` and `test_trusted_parent_probe` are the threat row's six selectors.
- `test_passwd_home_reads_the_directory_service_of_each_platform` covers both lookup branches and their refusals with standard-library mocks.
- `test_probes_clean_up_after_an_exception` covers cleanup.

What the individual tests add:

- **Hostile Git:**
  - each of the six `GIT_*` names, alone, changes what git does in the legitimate repository;
  - the local attack changes only the fixture's `.git/config`, and this repository's Git configuration hashes the same before and after.
- **Worker root:** reads, writes, creation, a shell append, a shell replacement and an unlink.
- **Trusted parent:**
  - the real `repository_root()` under hostile `GIT_*` names;
  - argv preserved, including `a b`, an empty string, `$(echo injected)`, `*` and a newline;
  - a word-split launch rejected;
  - the six refusals, each by its message, with the execution marker absent;
  - the exact parent argv and `env={}`, observed by a spy that still executes.
- **The red reasons** of the hostile-Git cases are required in full (root, content and hook), so no part of an attack can go inert unnoticed.

## The Check

- The focused suite ran with a temporary `HOME` and `UV_CACHE_DIR`, exit 0, 9 tests OK at `f4eed1cc` (validation §5). The fixture directories were 0 before and 0 after, the temporary `HOME` was empty after the run, and the Git configuration hash was unchanged. The command:

  ```text
  uv run --no-project --offline --python <observed absolute Python> python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py -v
  ```

- The same suite under the default `uv` interpreter (Python 3.10, which `make unit-test` uses on this seat): 9 tests OK.
- **Wrong implementations** (validation §7): the worker review's eight surviving mutants and four no-op assertions are each red. Most fail the aggregate selector too. M05, M18 and M25 fail their individual tests.
- **Formatting:** `ruff format --check` and `ruff check` are clean on both files. `make format` exits 2 on inherited shfmt diffs in files this PR does not change (validation §8).
- **Caps** (validation §8): the helper has 242 added lines (cap 250) and its tests 324 (cap 350). The task text is 198 lines with three allowed_files entries. Validation §8 has the final line counts. No local Bats ran.

## Limitations and observations

- **The worker sandbox and `dscl`.** The worker review measured that `dscl . -read` fails inside the worker sandbox with exit 70. An unmocked `run_under_trusted_parent` therefore raises on macOS under the worker sandbox, and consumer tests substitute `_directory_service`, as these tests do. The real directory-service output was not exercised here.
- **The worker-root read detection** depends on the filesystem moving a zeroed access time on a read. APFS here and Linux `relatime` do, and the probe refuses to run where a read does not.
- **The case-alias subcase** ran on this case-insensitive APFS. On a case-sensitive filesystem, such as Linux CI, it is reported as skipped with the measured reason, and remains unproved there.
- **Not run here:** Python 3.11 to 3.14 and Linux. CI runs Linux and macOS.
- **The validation record** elides the seat's inherited variable names and PATH value from two red reasons, keeping their count.

## Evidence, review, cost

- **Evidence:** `.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/`: `task.md`, this report, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md`, `result.txt`, and the worker review JSON and receipt.
- **Worker review:** one read-only round on `4729b83c`, `Verdict: incorrect`, with five P2 and five P3. They were fixed in one worker-side round (`f4eed1cc`), except the P3 noted in the review JSON as declared.
- **precheck:** pending-411 (`scripts/orchestrator/result-precheck.sh` is not on main).
- **cost:** n/a (the runtime exposes no token or cost figure to the seat).
