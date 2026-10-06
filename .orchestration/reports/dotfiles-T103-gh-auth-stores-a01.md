# Report: dotfiles-T103-gh-auth-stores-a01

- **PR:** #288, branch `feat/gh-auth-stores` on base `origin/main` `2d0ef943`.
- **Final head:** `c4fa1c14d447d99ca3de999bd4c47df3407ecc2b`, built in six commits: `bb9e92ed`, `5a5a9ab7`, `0ec58c80`, `0a28eb74`, `a41a56bd` (revise round 1) and `c4fa1c14` (revise round 2).
- **task_rev:** `sha256:81602cc1…d1bcbd299` verified at dispatch, and `sha256:3f7c52c2…a976d1a80c7ba86` after PONG decision 1.
- **Kind:** Claude seat. The change touches no permission, sandbox or hook boundary source.

## What changed

1. **One store per account.**
   - **Manifest:** `home/dot_agents/agent-config.yaml` declares `owner_gh_config_dir: ~/.config/gh` and `work_gh_config_dir: ~/.config/gh-work`, next to the existing `worker_gh_config_dir: ~/.config/gh-worker`. These are directories only. The comment says the owner directory must equal gh's default, because the orchestrator uses gh without `GH_CONFIG_DIR`.
   - **Renderer:** `scripts/generate-agent-configs.py` (`GH_CONFIG_DIRS`, `gh_config_dirs`) validates each path the way the worker path was validated. It rejects two stores that name the same directory, and renders `OWNER_GH_CONFIG_DIR`, `WORK_GH_CONFIG_DIR` and `WORKER_GH_CONFIG_DIR` into `home/dot_agents/model-profiles.env`.
   - **Existing consumers:** `WORKER_GH_CONFIG_DIR` keeps its name, value and quoting. herdr-agents, codex-orchestrate and check-tools.sh all source the file, so the two extra variables do nothing there.
2. **The login step.**
   - **`scripts/gh-auth-stores.sh` (new, shdoc):** it reads the three variables from `~/.agents/model-profiles.env`, unsets `GH_TOKEN`, `GITHUB_TOKEN` and the enterprise variants, and sets `umask 077`. For each store:
     - if `GH_CONFIG_DIR=<dir> gh auth status --hostname github.com` succeeds, the store is skipped;
     - if there is no terminal, it prints the `make gh-auth` hint and never prompts;
     - otherwise it runs `gh auth login --hostname github.com --git-protocol https --insecure-storage` and then `chmod 600 <dir>/hosts.yml`.

     It never reads or prints a credential. It needs only bash 3.2: `${!var}` and explicit label pairs, no `${var^^}`.
   - **Dropping `gh auth setup-git` (PONG decision 1):** the managed `~/.config/git/config` (from `home/dot_config/git/config.tmpl`) already sets `helper = !gh auth git-credential`. That helper reads `GH_CONFIG_DIR`, so it serves every store. On this host there is no `~/.gitconfig`, so `setup-git`'s `--global` writes would rewrite that managed file and leave chezmoi drift.
   - **`make gh-auth` (new):** runs the script.
   - **`setup.sh`:** `authenticate_github` runs at the end of `main`. It is skipped in CI, without a terminal, or without `gh`, and points at `make gh-auth`.
   - **`make update`:** unchanged; nothing on its path logs in. The literal `gh auth login` appears only in `scripts/gh-auth-stores.sh`.
3. **Doctor.** `scripts/check-agent-runtime.py` adds `gh_credential_store_findings`. For each store declared in the source `model-profiles.env`:
   - It prints `found: GitHub <label> credential store <dir> (hosts.yml 0600, one user: <login>)` when `hosts.yml` is a user-owned regular file with mode 0600 and `gh auth status --json hosts` shows exactly one working login.
   - Otherwise it prints a `WARN:` with the `make gh-auth` hint: missing, bad mode, a store holding 0 or 2+ logins, a failed status, or `gh` absent.
   - `found:` lines are a new `is_info` class. They are printed but are neither errors nor repair targets, so a present store cannot make doctor exit non-zero.
   - The token variables are stripped from gh's environment, and doctor never prompts.
   - `scripts/check-tools.sh`'s missing-worker hint now says `run make gh-auth` (allowed by PONG decision 1).
4. **README.** The operator-phase block is now:
   - the three-store table (account, store, rendered variable, user);
   - the `make gh-auth` / `setup.sh` step and its skip rule;
   - the chezmoi-private `encrypted_private_hosts.yml` note (such a store prompts for nothing);
   - the managed-helper sentence, "`make update` never prompts and never logs in", the owner-directory and offline notes, and a short command block.

   The later sentence that credited `gh auth setup-git` with the HTTPS helper now names the managed helper. Prettier passes.
5. **Tests.**
   - `test_gh_credential_stores_render_one_directory_per_account`: defaults, shell-safe custom paths, invalid paths, and the shared-directory rejection.
   - Two doctor tests with fake HOMEs and a fake `gh` that fails if a token variable leaks. They cover found, bad mode, missing, two logins, a failed login state and `gh` absent, plus no repair for `found:`.
   - `test_gh_auth_stores.py`:
     - without a terminal, no login call and exit 1;
     - on a pty, only the empty stores are logged in, with `GH_TOKEN` unset in every call, `hosts.yml` 0600 and a 0700 directory;
     - `setup.sh` under `CI=true` with no terminal skips and never calls `gh`.
   - The existing tests that pinned old behaviour were updated: one invalid-manifest doctor test stubs the new check, and `test_runtime_health` follows the new hint.
   - On `origin/main` the five new tests fail; the validation file has the output verbatim.

## Review

An independent read-only subagent reviewed `bb9e92ed` and reported 7 findings: 1 P1, 1 P2 and 5 P3. The evidence is in `-worker-crit.json` and `-worker-review-receipt.md` (`review_outcome: addressed`).
- **P1, `setup-git` drift:** sent to the orchestrator as a PONG, then fixed in `0ec58c80`.
- **P2, owner-dir contract:** documented in `5a5a9ab7`.
- **P3 items fixed:**
  - the check-tools hint (`0ec58c80`, with `0a28eb74` for its test);
  - the unset-variable hint, the setup.sh CI test and the offline note (`5a5a9ab7`).
- **P3, doctor tokenSource:** `not-applicable`. check-tools already requires file storage for the worker, and the owner and work stores may use the keyring.

## Validation and CI

- **Tests:** `make unit-test`: 915 tests, OK (skipped=1) on `0a28eb74`, and 916 on the final head `a41a56bd`.
- **Other checks:** `make render-check`, the validator (rc=0), `bash -n` and shellcheck on `setup.sh`, `scripts/gh-auth-stores.sh` and `scripts/check-tools.sh`, ruff format and prettier all pass. `ruff check`: the repository has existing findings, and CI does not run it. The pasted scan, with its script, shows 0 findings on lines this branch adds, in every changed Python file.
- **The task's `grep -n 'gh auth login' … home/.chezmoiscripts`:** it returns rc=2, because `home/.chezmoiscripts` is a directory and plain `grep -n` reports that as an error. The recursive form finds no match (rc=1). Both are pasted.
- **CI:** pasted for the first head `bb9e92ed` and for `0a28eb74`, both green on the first run. The final head `a41a56bd` is in the revise-round-1 section. `main` is unchanged.
- **Bot wait on `0a28eb74`:** 15 minutes, no review, inline comment or quota notice for that head.
- **The Bot P1 on the first head:** the Codex security review on `bb9e92ed` (thread on `scripts/gh-auth-stores.sh:45`) says `--insecure-storage` puts the owner token in a file that worker seats can read.
  - My final-head loop counted only items on `0a28eb74` and missed it. The unresolved thread showed up through `mergeable_state: blocked`.
  - I reported it by PONG with a keyring proposal for the owner and work stores.
  - **PONG decision 2:** file storage for every store stands, by operator decision (design report §12). The orchestrator replies `not-applicable` and resolves the thread, so this seat leaves it untouched.
- **Lesson for the bot step:** sweep every Bot item on the PR, not only those on the final head.

## Follow-ups (not done here)

- check-tools.sh's `check_github_identities` and the new runtime report both look at the worker store, so `make doctor` reports it twice, at different severities. Merging them is out of this task's scope.

[memory:decision] dotfiles-T103 (operator 2026-10-05): GitHub credentials are one store per account, prompted for only in the interactive operator phase (`setup.sh`, `make gh-auth`); `make update` never prompts; chezmoi-private encrypted `hosts.yml` files make the prompt a no-op.

CompactionDB: recorded as `ba9aa377-1bb6-4a41-898a-5fe622684558`; the command and readback are in the validation file.

- **Not run:** `make update`, `make apply`, `make gh-auth`, `gh auth login`.

## Revise round 1 (task_rev `sha256:a7f207f0…c03fa70`)

The audit of `0a28eb74` returned `incorrect`: 2 P2 and 3 P3. All are fixed in `a41a56bd`, or in the artifacts.

1. **A fresh bootstrap couldn't find `gh` (P2): fixed.**
   - **Cause:** on a fresh machine `gh` exists only as a mise shim, and the bootstrap shell's PATH didn't include the shims, so the login step was skipped on the very run it exists for.
   - **Fix:** `setup.sh` (`authenticate_github`) and `scripts/gh-auth-stores.sh` now put `$HOME/.local/share/mise/shims` on PATH before looking for `gh`. That is the same line the agent-asset updater command uses.
   - **Test:** with PATH set to `/usr/bin:/bin` and `gh` present only as a shim under the fake HOME, `setup.sh`'s step on a pty runs the two logins.
2. **The duplicate-store check ignored `~` (P2): fixed.** The renderer now compares `normpath(expanduser(path))`, so `~/.config/gh` and its absolute spelling under `$HOME` count as one store. Test: with `HOME` set to a fixture directory, that directory's absolute `.config/gh` path as the work store is rejected.
3. **Hint on the mode/ownership warning (P3): fixed.**
   - The warning now ends with `run make gh-auth`.
   - For that hint to actually fix the mode, the script sets an existing `hosts.yml` to 0600 even for a store it skips.
   - Tests: the doctor wording, and a skipped store's `hosts.yml` going from 0644 to 0600.
4. **Artifacts (P3 ×2): fixed.**
   - The sandbox record now states the PONG-decision-1 authorization and the one `check-tools.sh` edit.
   - The CI claim names only heads whose check output is pasted.
   - The `ruff check` claim now has its pasted scan and script.

On `0a28eb74`, all four round-1 tests fail; the output is in the validation file.

- **Re-run on `a41a56bd`:**
  - `make unit-test`: 916 tests, OK (skipped=1).
  - `bash -n` and shellcheck on `setup.sh`, `scripts/gh-auth-stores.sh` and `scripts/check-tools.sh`, `make render-check`, the validator (rc=0), ruff format and prettier all pass.
  - The ruff added-line scan finds nothing.
  - CI and the Bot wait are in the validation file.
- **Not run:** `make update`.

## Revise round 2 (task_rev `sha256:2043ad50…b7310816`)

The audit of `a41a56bd` returned `incorrect`: 1 P2 and 1 P3. Both are fixed.

1. **A failed `chmod 600` was swallowed (P2): fixed in `c4fa1c14`.**
   - **Cause:** `ensure_store` runs in an `||` list, where errexit is off. A `chmod` that failed, for example on a `hosts.yml` another user owns, was ignored. On the skip path the store still counted as skipped, and `make gh-auth` could exit 0 with the file exposed.
   - **Fix:** both chmod calls now go through `secure_hosts_file`. It prints `gh-auth: <label> store <dir>: cannot set hosts.yml to mode 0600; make it yours, then run "make gh-auth"` and returns 1, so the store counts as failed. A failed `mkdir -p` now fails the store too.
   - **Test:** a `chmod` on PATH that always fails. Both the owner store (skip path) and the work store (after its login) fail with the message, the script exits 1, and the owner store is not reported as skipped.
   - **Test fake:** the fake `gh` now calls `/bin/chmod`, so the failing fake doesn't block its simulated login.
   - **Previous head:** on `a41a56bd` the test fails, with test exit 1. The owner store is reported as skipped and the message is missing.
2. **Round-1 negative-test transcript (P3): fixed in the validation file.** Its `exit=0` was the status of a `grep` that filtered the test output. That block now holds the verbatim wrapper that was run, plus a re-run without the filter, which shows `FAILED (failures=4)` and `test exit=1`. The round-2 transcript records the test process's own status.

- **Re-run on `c4fa1c14`:**
  - `make unit-test`: 917 tests, OK (skipped=1).
  - `bash -n` and shellcheck, `make render-check`, the validator (rc=0), ruff format and prettier all pass.
  - The ruff added-line scan finds nothing.
  - CI and the Bot wait are in the validation file.
- **Not run:** `make update`.

cost: n/a
