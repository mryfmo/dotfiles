---
task_id: dotfiles-T133-trusted-exec-contract-tests-a01
seat: claude-standard-dot-a011
branch: tools/trusted-exec-contract-tests-a01
base: ba318e53 (origin/main at the branch point)
previous_head: 9545e59f4a91aae36cd850c4645d29c366845844 (the audited head; the orchestrator's update-branch merge)
code_head: 7d3ecd4f (e603ac51 task copy; 755d9002 tests, red; 4729b83c helper; f4eed1cc the worker review's fix round; bb539aa7 revise 1 tests, red; 65c81c98 revise 1 fix; eda9b5ee the non-absolute home case; 7d3ecd4f the revise review's P3 fixes)
task_sha256: dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c
---

# Report: dotfiles-T133-trusted-exec-contract-tests-a01

- **Seat and branch.** Seat `claude-standard-dot-a011` in `.claude/worktrees/worker-d`. The branch `tools/trusted-exec-contract-tests-a01` was created with `--no-track` from `origin/main` `ba318e53`, and the orchestrator update-branched it to `9545e59f`. The task copy is byte-identical to the dispatched text `dd754911…` (validation §1).
- **Premises.** Re-run for this round (validation §2): Python 3.15.0, Darwin, `dscl` present and `getent` absent, the helper absent from `origin/main`. The absolute interpreters are mise's 3.15.0 and uv's 3.10.22. Without `--python`, uv picks 3.10 under this seat's HOME and 3.15 under a temporary one, so every suite run names its interpreter.
- **Design.** Section 5.14 items 2, 3, 7 and 9 apply by reference (D-024-30). This record names the items and does not restate them.
- **Authority for the passwd change.** The task text names `dscl` or `getent` as the source of the home. Revise 1's check (4), in the orchestrator's ACCEPTANCE of round 1, moved the source to `pwd.getpwuid` and kept those two as a cross-check.

## Revise 1

The task-level audit of `9545e59f` returned two P2 and two P3, and the orchestrator added a measured finding. This round answers each one:

| Finding | What changed | Where it shows |
| --- | --- | --- |
| P2: a same-length overwrite keeps the inode, size and a coarse mtime, so `assert_untouched()` missed it | The probe sets both files' mtime to a fixed past instant and compares the whole content as well as the inode and mtime | `test_worker_root_probe_detects_a_same_length_overwrite`, red at `bb539aa7` (validation §4), green at `7d3ecd4f` (§5); the content-compare mutant is red (§7) |
| P2: mutation M16 never ran, because its replacement matched twice | M16 is anchored on the runner's own `check=False` call. Every block now truncates its output, asserts one match and prints `mutated:` | 17 blocks in §7, each with `mutated:` and a red run |
| P3: the Python 3.10 claim cited a run that was 3.15 | The 3.10 suite runs uv's 3.10 by absolute path and prints its version | §5: `3.10.22`, 10 tests OK |
| P3: the report claimed macOS CI coverage | macOS CI skips the unit suite for this diff, so the macOS evidence is this seat's local runs | §9: the workflow rule and the macOS job's skipped steps |
| Orchestrator: `dscl` fails in both seat sandboxes | `passwd_home()` reads `pwd.getpwuid(os.getuid()).pw_dir` and uses `dscl` or `getent` only as a cross-check when it runs | `test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check`, red at `bb539aa7` (§4), green at `7d3ecd4f` (§5); live on this seat, `dscl` exits 70 and the home still resolves (§6); three mutants red (§7) |

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

   `assert_unaffected(root, content)` reports an attacker root, attacker content or an attacker program that ran. The measurements behind the payloads are in learning item 1.
3. **Worker root.** `WorkerRoot` provides an input, an output and a not-yet-created output under `<root>/.claude/worktrees/probe-seat/`. Both files start with access time 0 and a fixed past mtime (2001).
   - A read shows as the input's access time leaving 0. When it starts, the probe measures on a scratch file that a read moves a zeroed access time, and refuses to run where it does not.
   - A write shows as a changed inode, an mtime off the fixed instant, or content other than the original bytes. The content is compared because a write in place can keep the inode, the size and a coarse clock's mtime. It is read only from the same regular file (the inode and mode recorded at the start), and the probe puts that read's access time back.
   - A removal shows as a missing file, and creating the new output as its directory existing.
4. **Swapped file.** `SwappedFile.swap()` is the deterministic barrier, with no sleep and no loop. It makes the checked name a link to attacker content.
   - `assert_not_consumed(data)` refuses attacker bytes. It also refuses a consumer that never reached the barrier ("never swapped"), so a skipped barrier cannot pass vacuously.
   - The case-alias subcase uses the case-flipped name when `samefile` measures it to be the same file. Otherwise `alias` is None, with the measured reason, and the test reports the subcase as skipped, never passed.
5. **Sanitized environment.** `assert_sanitized_env(observed, declared=())` requires the name set to equal `PATH`, `HOME`, `LANG` and the declared names, with `PATH=/usr/bin:/bin`.
6. **Trusted parent.** `run_under_trusted_parent(script, *args)` runs the following, with `env={}` and stdin closed:

   ```text
   /usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <realpath of script> [args...]
   ```

   - `passwd_home()` reads the real UID's passwd entry, never `HOME` or PATH. Where the directory service runs (`/usr/bin/dscl . -read /Users/<name> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), its answer must agree with the entry. A failed lookup leaves the entry standing alone, and a disagreeing or malformed answer, or a non-absolute home, is refused.
   - `repository_root()` comes from the module's own path.
   - Before anything runs, it refuses a relative path, a script that resolves outside the root (traversal, sibling prefix, symlink) and a non-regular file.

## Tests and the selectors

`tests/unit/test_trusted_exec_contract.py` (`TrustedExecContractTest`) was written first. It was red at `755d9002`, where the module did not exist, and revise 1's two tests were red at `bb539aa7` against the audited helper (validation §4). Each `case_*` function runs a deliberately noncompliant consumer stub, which must make the probe assertion fail for the intended reason, then a compliant stub, which must pass. It returns the observed failure text (validation §6).

The selectors:

- `test_each_probe_detects_condition` runs the six cases as subtests.
- `test_shim_probe`, `test_hostile_git_probe`, `test_worker_root_probe`, `test_swapped_file_probe`, `test_sanitized_environment_probe` and `test_trusted_parent_probe` are the threat row's six selectors.
- `test_worker_root_probe_detects_a_same_length_overwrite` and `test_passwd_home_uses_getpwuid_and_treats_dscl_or_getent_as_an_optional_cross_check` are revise 1's selectors.
- `test_probes_clean_up_after_an_exception` covers cleanup.

What the individual tests add:

- **Hostile Git:**
  - each of the six `GIT_*` names, alone, changes what git does in the legitimate repository;
  - the local attack changes only the fixture's `.git/config`, and this repository's Git configuration hashes the same before and after.
- **Worker root:** reads, writes, creation, a shell append, a shell replacement, an unlink, and an in-place same-length overwrite of either file with its mtime put back.
- **The passwd lookup:** on macOS and Linux, an agreeing answer, a lookup that fails as `dscl` does in the seat sandboxes, a disagreeing answer and a malformed one; a platform with no directory service, with an absolute and with a relative passwd home; each with the exact lookup argv.
- **Trusted parent:**
  - the real `repository_root()` under hostile `GIT_*` names;
  - argv preserved, including `a b`, an empty string, `$(echo injected)`, `*` and a newline;
  - a word-split launch rejected;
  - the six refusals, each by its message, with the execution marker absent;
  - the exact parent argv and `env={}`, observed by a spy that still executes.
- **The red reasons** of the hostile-Git cases are required in full (root, content and hook), so no part of an attack can go inert unnoticed.

## The Check

- **Python 3.15.0**, with a temporary `HOME` and `UV_CACHE_DIR`: exit 0, 10 tests OK at `7d3ecd4f` (validation §5). The fixture directories were 0 before and 0 after, the temporary `HOME` was empty after the run, and the Git configuration hash was unchanged. The command:

  ```text
  uv run --no-project --offline --python <absolute Python> python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py -v
  ```

- **Python 3.10.22**, by absolute path, the same way: 10 tests OK (validation §5).
- **Wrong implementations** (validation §7): 17 replacements, each matching exactly once and each making the suite exit 1:
  - the worker review's eight survivors (M33, M04, M05, M14, M15, M16, M18, M25);
  - a no-op of each probe assertion (worker-root read, worker-root write, shim, swap barrier);
  - the worker-root content compare dropped;
  - the worker-root access time not put back after the probe's own read;
  - the passwd cross-check dropped;
  - a failed lookup no longer tolerated;
  - a non-absolute home accepted.
- **Formatting:** `ruff format --check` and `ruff check` are clean on both files. `make format` exits 2 on inherited shfmt diffs in files this PR does not change (validation §8).
- **Caps** (validation §8): the helper has 247 changed lines (cap 250) and its tests 350 (cap 350, reached exactly). The task text is 198 lines with three allowed_files entries. No local Bats ran.

## Limitations and observations

- **macOS CI does not run this module.** `.github/workflows/test.yaml` skips the macOS unit suite for a pull request whose relevant paths are all Python, docs or records, as this one's are. The macOS job's test steps were skipped on the earlier head `25dd01e5` (validation §9). The macOS evidence is this seat's local runs, and Linux CI is the only CI that runs the module.
- **The directory service.** `dscl` exits 70 inside this sandbox (validation §6), so here the passwd entry stands alone. The cross-check's parsing of real `dscl` and `getent` output is tested with standard-library mocks only.
- **The worker-root probe** depends on the filesystem moving a zeroed access time on a read, which APFS here and Linux `relatime` do. The probe refuses to run where a read does not.
- **The case-alias subcase** ran on this case-insensitive APFS. On a case-sensitive filesystem, such as Linux CI, it is reported as skipped with the measured reason, and remains unproved there.
- **Known gaps of the worker-root probe**, older than revise 1 and measured by its review, with no line left under the caps for their tests. The probe does not see:
  - a new file beside the two named ones, such as an atomic writer's leftover temporary file;
  - a read of the output;
  - a rename away and back;
  - identical bytes written with the mtime put back.

  A seat-directory listing and the access-time check on both files would close the first two. Proposed as a follow-up.
- **Untested by construction.** The probe reads content only from a file whose inode and mode match the ones recorded at the start, so a recycled inode number on a symlink or FIFO cannot hang the read. No test forces inode reuse, which APFS does not do. The newline half of the passwd home check has no row either. The home is passed as one `HOME=` argument, so a newline cannot split it.
- **One unexplained failure.** The revise review saw `test_worker_root_probe` fail once, without a subtest label, during a mutant run whose mutation cannot reach that test, and not again in 52 later unmutated runs. Its guess, unverified: an outside reader, such as an indexer, touched the input's access time.
- **Not run here:** Python 3.11 to 3.14.
- **The validation record** elides the seat's inherited variable names and PATH value from two red reasons, keeping their count.

## Evidence, review, cost

- **Evidence:** `.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/`: `task.md`, this report, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md`, `result.txt`, `revise.yaml`, and the worker review JSON and receipt.
- **Worker review:** one read-only round on `4729b83c`, `Verdict: incorrect`, five P2 and five P3, fixed in `f4eed1cc` except the P3 declared in the review JSON. Revise 1 had a second read-only round on `9545e59f..65c81c98`, `Verdict: correct`, with no P0 to P2 and five P3:
  - the access-time put-back was untested;
  - the non-absolute home refusal was untested, and two subtests shared a label;
  - the older worker-root gaps listed above;
  - a recycled inode;
  - one unexplained failure.

  `eda9b5ee` and `7d3ecd4f` fixed the first two and the recycled inode. The rest are declared above. The review also noted that the task text names `dscl` or `getent`, which the authority bullet at the top answers.
- **precheck:** pending-411 (`scripts/orchestrator/result-precheck.sh` is not on main).
- **cost:** n/a (the runtime exposes no token or cost figure to the seat).
