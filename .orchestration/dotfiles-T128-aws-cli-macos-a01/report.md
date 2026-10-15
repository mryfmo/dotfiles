---
task_id: dotfiles-T128-aws-cli-macos-a01
seat: claude-standard-dot-a002
branch: tools/aws-cli-macos
base: 04590ae9
code_commit: fe392450
pr: 363
task_sha256: b51b8bfba2d259b710917f5ea0cb333b83768c129da66c38bc3cdddbfd48a585
---

# Report: dotfiles-T128-aws-cli-macos-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/aws-cli-macos` from `origin/main` `04590ae9`, PR #363. The PR #360 branch stays as it was for its integration.
- Task file: sha256 `b51b8bfb…`, copied byte-identical to `.orchestration/dotfiles-T128-aws-cli-macos-a01/task.md`; the task-consistency check passes on the dispatched file (validation §1).
- Dispatched 01:13:34Z. Premises 3 and 4 replay equal (validation §2). Premises 1 and 2 need the network: read from the orchestrator's paste, not replayed. No question and no amendment. An alive PONG at 01:22:11Z named the candidates below before the Bot saw the PR.
- AWS's `install.sh` was read with WebFetch, as reference data, to confirm what item 1 relies on:
  - its install root is `${XDG_DATA_HOME:-$HOME/.local/share}/aws-cli`;
  - `${XDG_BIN_HOME:-$HOME/.local/bin}/aws` links to `aws-cli/aws`, the macOS pkg's flat layout;
  - it fetches `v2/version.txt`, trims the whitespace, and exits 0 when that version is already installed;
  - it checks the pkg with `pkgutil --check-signature` for the team id `94KV3E626L` before `installer -pkg … -target CurrentUserHomeDirectory`;
  - it exits 2 on a downgrade and 1 on its other errors, and accepts `--version`, `--system`, `--quiet`.

## What landed

| Item | File | What it does |
|---|---|---|
| 1 | `install/ubuntu/common/aws_cli.sh` | **The shdoc header** names both distributions, each verified. **`aws_cli_url`** answers `https://awscli.amazonaws.com/AWSCLIV2.pkg` on `Darwin` before its architecture switch, so `aws_cli_archive_etag` and `main`'s ETag skip read the pkg on macOS. **`install_aws_cli`** takes a macOS path on `Darwin`:<br>1. It downloads `v2/install.sh` and `v2/install.sh.sig`, then `v2/version.txt`, trimmed of whitespace; each download returns 3 on failure, before any verification.<br>2. It runs the existing key checks and dearmor, unchanged, then `gpgv` on `install.sh`.<br>3. Only then does it run `XDG_DATA_HOME=<parent of AWS_CLI_INSTALL_DIR> XDG_BIN_HOME=<AWS_CLI_BIN_DIR> bash <install.sh>`, whose non-zero exit it returns.<br>4. It calls `verify_aws_cli_install <version.txt's version>`.<br>The Linux path keeps every line. The only Linux-visible difference is that `aws_cli_url` now calls `uname -s` first, and `aws_cli_url` sits in the `else` branch of the new `Darwin` test. |
| 2 | `home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl` (new) | The `darwin` guard, the include of `../install/ubuntu/common/aws_cli.sh`, `end`. This is the layout of the macOS wrappers, such as `run_once_04-install-ghostty.sh.tmpl`. |
| 3 | `install/macos/common/dependencies.sh` | `awscli` removed from `BREW_PACKAGES`; nothing else (`gpg` stays). |
| 4 | `tests/unit/test_aws_cli_acquisition.py` | The four macOS tests and the changed first assertion; see below. |

The failure modes item 1 lists, each pinned by a test:
- a download failure returns 3, and `main` keeps a working `aws` with exit 0 or returns 3 without one;
- a `gpgv` failure runs no installer;
- a key failure stops before `gpgv` (the existing checks, shared);
- an installer failure returns its status through `main`, which records no ETag;
- an exit-0 installer that leaves another version active fails the postcondition.

## Tests

The four macOS tests share one prelude, `MACOS_PRELUDE`. It overrides `uname` (`Darwin` for `-s`, `arm64` for `-m`), `curl`, `gpg`, `gpgv` and `bash` as shell functions, as item 4 asks. A helper, `run_macos`, gives each run a fresh `HOME`, a call log, a temporary directory and the existing `mktemp` shim.

- **`test_macos_signature_failure_preserves_existing_aws_and_runs_no_installer`:** a failing `gpgv`, which was called on `install.sh.sig` and `install.sh`. The exit is non-zero, the existing `aws` is untouched, the stub `bash` never runs and no temporary file is left.
- **`test_macos_verified_install_runs_install_sh_with_xdg_roots`:**
  - The stub `bash` runs the downloaded `install.sh` with `XDG_DATA_HOME=<HOME>/.local/share` and `XDG_BIN_HOME=<HOME>/.local/bin` and no other argument.
  - The URLs are `install.sh`, its `.sig` and `version.txt`, in that order.
  - `Installed aws-cli/2.37.6.` is printed.
  - The postcondition fails when the installer leaves `2.35.20` active against version.txt's `2.37.6`.
  - Beyond item 4's text: `main` with an installer that exits 2 returns 2 and records no ETag (item 1's installer failure mode).
- **`test_macos_etag_skip_uses_the_pkg_url`:**
  - The probe reads `AWSCLIV2.pkg` under `Darwin`/`arm64`, so `aws_cli_url`'s Darwin case passes, and the archive URL under the Linux `uname`.
  - Beyond the text: `main` with the pkg's ETag recorded and a working CLI makes the HEAD request alone.
- **`test_macos_download_failure_keeps_a_working_aws_and_runs_no_gpgv`:**
  - A failing `install.sh` download, and beyond the text a failing `.sig` and `version.txt` too: `install_aws_cli` returns 3 with no `gpgv` and no `bash`.
  - `main` returns 0 with the warning when a working `aws` exists, and records no ETag; it returns 3 when none exists.
- **`test_platform_package_managers_and_wrapper_own_aws_cli`:** its first assertion now reads the `BREW_PACKAGES` list: `awscli` absent, `gpg` present. Its other assertions stay.

The Check (validation §4) shows 20 tests in the Claude sandbox: 18 pass. The other two are Linux tests this task does not touch: `test_gpgv_failure_preserves_existing_aws_and_skips_unzip` and `test_verified_archive_runs_installer_with_user_local_update_arguments`. They fail identically on `origin/main` there (§5), because they call macOS `mktemp -d` without the shim, which writes under `/var/folders/…`, and the sandbox denies that. CI runs the module outside any sandbox.

Mutation pass on the macOS branch: 12 mutations, 12 caught (validation §8). They cover:
- the Darwin URL;
- the `install.sh` URL and path;
- version.txt's exit 3 and its trim;
- `gpgv` skipped on macOS;
- each XDG root;
- the installer's status;
- the postcondition;
- the macOS path falling through to the Linux one;
- Darwin detection.

## Caps

Validation §7:

- outside `tests/` and `.orchestration/`: 3 files, 35 added + 6 deleted = 41 changed lines (cap 200);
- under `tests/`: 147 added lines (cap 1000);
- 4 files outside `.orchestration/`.

## CI and the Bot

- **The Bot:**
  - PR #363 was opened as a draft and marked ready (01:23:38Z) after the evidence commit `c2638b32`. The Bot's Security Review of `c2638b3` completed at 01:28:01Z, with no finding.
  - The host slept during the Bot wait. The wait's next poll came at 2741 seconds, after one failed `gh` call ("error connecting to api.github.com"). It posted `@codex review` then (02:12:59Z, issue comment 6182834286) and stopped at its 15-minute bound.
  - The Bot answered with issue comment 6182875026 at 02:16:04Z: `Codex Review: Didn't find any major issues`, `**Reviewed commit:** c2638b3292`, the head.
  - There is no review object and no inline thread, so there is nothing to disposition (validation §9).
- **CI on `c2638b32`:** 15 of 15 checks pass. The `--watch` exited 1 on the same network drop, and the listing it printed afterwards shows every check passing (validation §9).
- **The real macOS install ran on GitHub's runner.** `public-bootstrap (macos-14, client)` runs `setup.sh`, so `chezmoi apply` ran the new `run_after_04` wrapper (rendered as `.chezmoiscripts/macos/04-install-aws-cli.sh`):
  - `gpgv` reported a good signature from the AWS CLI Team key `FB5DB77F…` on `install.sh`;
  - `install.sh` installed AWS CLI 2.38.1 from the pkg into `$HOME/.local/share/aws-cli`;
  - the postcondition printed `Installed aws-cli/2.38.1.` (validation §9, the log excerpt).

  The `MacOS` workflow's `build` job passed in 4 seconds: its steps run only when the private-dotfiles secrets are configured, so it applied nothing.
- **CI on the final head (this commit, the evidence update):** in the RESULT.

## For the operator, after the merge and `make update`

`brew uninstall awscli`, then `brew autoremove --dry-run`, which is expected to list `python@3.14` and the `aws-c-*` family. These are not the worker's to run.

## Not done, or outside scope

Beyond item 1, not changed, and named in the 01:22:11Z PONG:

1. The script fetches version.txt, and `install.sh` fetches it again. A release published between the two fails the postcondition (fail closed; the next apply retries). `install.sh --version <X.Y.Z>` would pin it, but item 1 runs `install.sh` without arguments.
2. `install.sh` exits 2 when the installed CLI is newer than version.txt (it refuses a downgrade), and `main` then returns 2 (fail closed).
3. The new macOS wrapper has no test (row 2 is residual: the audit reads it).

- `ruff check` reports I001 on the module's import block. It is unchanged from `origin/main`, which reports it too (validation §6), so it is left as it is. `ruff format --check` passes.
- The macOS branch's `mkdir -p` of the two roots is not pinned by a test (`install.sh` creates its own directories).
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
