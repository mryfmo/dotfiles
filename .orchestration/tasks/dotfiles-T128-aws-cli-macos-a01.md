---
format: 2
task_id: dotfiles-T128-aws-cli-macos-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - install/ubuntu/common/aws_cli.sh
  - home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl
  - install/macos/common/dependencies.sh
  - tests/unit/test_aws_cli_acquisition.py
  - .orchestration/dotfiles-T128-aws-cli-macos-a01/**
after: []
threat_table:
  - control: the PR edits install/ubuntu/common/aws_cli.sh, which gains a macOS branch keyed on uname -s Darwin that downloads AWS's install.sh and its .sig, verifies the signature with gpgv against the dearmored pinned key before anything runs, and only then runs the installer under XDG_DATA_HOME and XDG_BIN_HOME; the Linux branch is unchanged
    disposition: "closed: tests/unit/test_aws_cli_acquisition.py::test_macos_signature_failure_preserves_existing_aws_and_runs_no_installer"
  - control: the PR adds home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl, the macOS twin of the Ubuntu wrapper, one include guarded by the darwin os check
    disposition: "residual: the file is the include line and its guard, nothing else; the audit reads it against item 2; chezmoi runs it at every apply, as it runs the Ubuntu twin"
  - control: the PR edits install/macos/common/dependencies.sh, removing awscli from BREW_PACKAGES and nothing else
    disposition: "residual: one list entry removed; the existing test test_platform_package_managers_and_wrapper_own_aws_cli is changed to assert awscli absent and gpg present (item 4), so a second change to the list fails that test"
  - control: the PR edits tests/unit/test_aws_cli_acquisition.py, the oracle of the rows above (uname, curl, gpgv, gpg and bash overridden as shell functions in the sourced prelude record their argv and answer from files the test writes; nothing downloads, nothing installs)
    disposition: "residual: the stubs record and answer, nothing else; the audit reads each case against item 4"
  - control: "the macOS install path at apply time: curl to awscli.amazonaws.com for install.sh, install.sh.sig, version.txt and the AWSCLIV2.pkg ETag, gpgv against the pinned key, then bash install.sh, which downloads the pkg, verifies its Apple Developer team id and runs Apple's installer and pkgutil before the files land under the XDG roots"
    disposition: "residual: install.sh runs only after its signature verified against the key already pinned for the Linux archive (the closed row's test); a download failure returns 3 from install_aws_cli before any verification and main then keeps a working installed CLI (fail open, as on Linux) or fails when none runs; install.sh's own pkg check (AWS_CLI_PKG_TEAM_ID) is AWS's control, outside this repository; verify_aws_cli_install is the postcondition on both OSes"
  - control: the ETag skip (aws_cli_archive_etag in main) with https://awscli.amazonaws.com/AWSCLIV2.pkg as the macOS URL
    disposition: "residual: a changed ETag means a new release and a re-install, an unchanged one skips, as on Linux; the test test_macos_etag_skip_uses_the_pkg_url covers the URL by OS"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-aws-cli-macos-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-aws-cli-macos-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests source install/ubuntu/common/aws_cli.sh in a bash subprocess whose prelude overrides uname, curl, gpgv, gpg and bash as shell functions, and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the script runs uname, curl, gpg, gpgv, bash, mktemp, awk, date, mkdir, rm, dirname, cat, unzip and the archive's own aws/install on Linux, and the installed aws binary (printf and read are bash builtins; curl's --head is a flag, not a command), each resolved on the user's PATH at apply time (gpgv from the gpg formula of BREW_PACKAGES, installed by run_once_before_50 before any run_after script); install.sh itself runs Apple's installer and pkgutil and fetches version.txt and the pkg; the tests override the commands as shell functions in the sourced prelude; nothing the downloaded content contains chooses an executable: install.sh runs only after gpgv accepted it"
  - control: new or renamed scripts
    disposition: "residual: one new script, home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the Homebrew awscli formula is the only installed formula that uses python@3.14, a formula scripts/upgrade-tools.sh forbids (python@*), and its dependency list carries python@3.14, so brew upgrade of awscli pulls the forbidden dependency at every make update (the operator-reported error; replayed by the orchestrator outside the sandbox, the seats read the paste)'
    command: 'brew uses --installed python@3.14; brew deps --formula awscli | tr "\n" " "'
    output: |-
      awscli
      aws-c-auth aws-c-cal aws-c-common aws-c-compression aws-c-event-stream aws-c-http aws-c-io aws-c-mqtt aws-c-s3 aws-c-sdkutils aws-checksums ca-certificates lz4 mpdecimal openssl@3 python@3.14 readline s2n sqlite xz zstd 
  - claim: 'AWS signs install.sh (its .sig exists) and publishes no .sig for the macOS pkg, so the signature check applies to install.sh and the pkg is verified by install.sh itself (replayed by the orchestrator outside the sandbox, the seats read the paste)'
    command: 'for u in https://awscli.amazonaws.com/AWSCLIV2.pkg.sig https://awscli.amazonaws.com/v2/install.sh https://awscli.amazonaws.com/v2/install.sh.sig; do printf "%s -> " "$u"; curl -sS -o /dev/null -w "%{http_code}\n" -I "$u"; done'
    output: |-
      https://awscli.amazonaws.com/AWSCLIV2.pkg.sig -> 404
      https://awscli.amazonaws.com/v2/install.sh -> 200
      https://awscli.amazonaws.com/v2/install.sh.sig -> 200
  - claim: 'on origin/main the macOS Homebrew list installs awscli (line 17) and gpg (line 21), so removing awscli leaves gpgv available for the signature check'
    command: 'git show origin/main:install/macos/common/dependencies.sh | /usr/bin/grep -nE "^\s+(awscli|gpg)$"'
    output: |-
      17:    awscli
      21:    gpg
  - claim: 'the test module on origin/main holds sixteen tests, the Linux cases this task keeps and extends'
    command: 'git show origin/main:tests/unit/test_aws_cli_acquisition.py | /usr/bin/grep -c "def test_"'
    output: |-
      16
---

# AGMSG-TASK dotfiles-T128-aws-cli-macos-a01 — the AWS CLI on macOS from AWS's official installer, verified, instead of the Homebrew formula (plan 007 T715, operator decision option A of 2026-10-12; rewritten in the plan 021 step 7 short form on 2026-10-15 after the operator asked why make update still fails on awscli)

Written 2026-10-12 by the orchestrator seat as plan 007 T715 and pair-reviewed once in `dotfiles-T128-task-review-phase1-a01` (both halves `revise`, one revision applied), never dispatched; rewritten 2026-10-15 in the short form with the same items, pair-reviewed before dispatch. The symptom: every `make update` runs `scripts/upgrade-tools.sh`, which skips the forbidden `python@3.14` yet upgrades the Homebrew `awscli` formula that depends on it, so the Homebrew step fails or warns on this machine at each update (premise 1). The fix is the one the Ubuntu install already has: AWS's own distribution, signature-verified, under `~/.local/share/aws-cli` with the `~/.local/bin/aws` symlink, updated at every apply when AWS publishes a new release. The manifest `assets.aws-cli` in `home/dot_agents/agent-config.yaml` is not touched. A Claude seat: no file is Claude's boundary.

## Goal

On macOS, `chezmoi apply` installs and updates the AWS CLI through AWS's signed `install.sh` under the XDG roots, Homebrew no longer installs `awscli`, and `make update` stops tripping on `python@3.14`.

## Files

1. `install/ubuntu/common/aws_cli.sh`: a macOS branch keyed on `uname -s` (`Darwin`), the Linux branch unchanged. The branch downloads `https://awscli.amazonaws.com/v2/install.sh` and `https://awscli.amazonaws.com/v2/install.sh.sig` (exit 3 on a download failure, as the Linux branch does), verifies with `gpgv` against the dearmored pinned key exactly as `install_aws_cli` does for the archive, and only then runs `bash <install.sh>` with `XDG_DATA_HOME` set to the parent of `AWS_CLI_INSTALL_DIR` (`~/.local/share`) and `XDG_BIN_HOME` to `AWS_CLI_BIN_DIR` (`~/.local/bin`). The branch has no staged archive to read a version from, so before install.sh runs it fetches `https://awscli.amazonaws.com/v2/version.txt` (a download failure returns 3, like the other downloads) and passes that version to `verify_aws_cli_install`, which stays the postcondition: the installed `aws --version` must report AWS's current release, as the Linux branch checks against the staged archive's version. `aws_cli_url` gains a Darwin case before its architecture switch, returning the pkg URL for any architecture (today the switch rejects `arm64` with "Unsupported AWS CLI architecture", and both `aws_cli_archive_etag` and `install_aws_cli` call it, so without this the macOS ETag probe would read as offline). The ETag skip (`aws_cli_archive_etag`, `main`) uses `https://awscli.amazonaws.com/AWSCLIV2.pkg` as the macOS URL. The shdoc header says the file installs the current AWS CLI from AWS's official distribution on Linux (archive) and macOS (install.sh and pkg), each verified; comments in English, shdoc form. Failure modes stated, the Linux branch's: a download failure makes `install_aws_cli` return 3 before any verification, and `main` then keeps a working installed `aws` and returns 0 with a warning (fail open on purpose: the installed CLI stays, the ETag stays unrecorded so the next apply retries) and returns 3, the download status, when no working `aws` exists (the Linux test's "download fails, no CLI" case pins 3; the path that returns 1 is the ETag probe failing with no working `aws`, unchanged); the version read from version.txt is trimmed of whitespace before use (the file has no trailing newline today); a `gpgv` failure leaves the existing `aws` untouched and runs no installer (fail closed, `main` returns the status); a failure to read or dearmor the pinned key (the key file missing, its fingerprint or expiry wrong, `gpg --dearmor` failing) stops before any `gpgv` call and runs no installer (fail closed, the Linux branch's `test_key_metadata_failures_stop_before_dearmor_and_gpgv` form); a non-zero exit of install.sh returns that status from `install_aws_cli`, so `main` returns it and records no ETag (fail closed); an installer exit 0 without a working `aws` fails the postcondition (fail closed), as on Linux.
2. `home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl` (new): the macOS twin of the Ubuntu wrapper, `{{ if eq .chezmoi.os "darwin" -}}` … `{{ include "../install/ubuntu/common/aws_cli.sh" }}` … `{{- end }}` in the Ubuntu wrapper's layout, nothing else.
3. `install/macos/common/dependencies.sh`: remove `awscli` from `BREW_PACKAGES`; nothing else in the list changes (`gpg` stays, it provides `gpgv`).
4. `tests/unit/test_aws_cli_acquisition.py`: the macOS cases in the existing style, `bash -c 'source "$1"; …'` with `uname()`, `curl()`, `gpgv()`, `gpg()` and `bash()` overridden as shell functions in the sourced prelude as the Linux cases do (`bash()` intercepts the installer call and records its argv and environment; no PATH stub named `bash`, which the harness's own `bash -c` would resolve), named verbatim: `test_macos_signature_failure_preserves_existing_aws_and_runs_no_installer` (a `gpgv` failure on install.sh: the existing `aws` untouched, the stub `bash` never called, exit non-zero), `test_macos_verified_install_runs_install_sh_with_xdg_roots` (a verified install.sh is run by `bash` with `XDG_DATA_HOME` and `XDG_BIN_HOME` set to the install root's parent and the bin dir, and the postcondition compares the stub `aws --version` with the fetched version.txt), `test_macos_etag_skip_uses_the_pkg_url` (the ETag probe on macOS reads the pkg URL, on Linux the archive URL; the `uname` override answers `Darwin` for `-s` and `arm64` for `-m`, so the Darwin case of `aws_cli_url` is what passes), `test_macos_download_failure_keeps_a_working_aws_and_runs_no_gpgv` (a failing `curl` for install.sh: `install_aws_cli` returns 3 with no `gpgv` and no `bash` call, and `main` returns 0 with the warning when the stub `aws` runs, 3 when it does not, as the Linux case pins). The existing `test_platform_package_managers_and_wrapper_own_aws_cli` changes its first assertion: `awscli` absent from `BREW_PACKAGES` and `gpg` present; its other assertions stay. The Linux tests stay as they are.

The report names, for the operator's one-time hygiene after the merge and `make update` (not the worker's to run): `brew uninstall awscli` then `brew autoremove --dry-run`, expected to list `python@3.14` and the `aws-c-*` family.

## Out of scope

`scripts/upgrade-tools.sh` and its forbidden list (T714 owns the Homebrew attestation failure); `home/dot_agents/agent-config.yaml` and `assets.aws-cli`; the Linux branch's behaviour; the Ubuntu wrapper template; any other `BREW_PACKAGES` entry; `docs/history` (frozen by convention: its two sentences that Homebrew owned the macOS install stay as history, and the kept assertions of `test_platform_package_managers_and_wrapper_own_aws_cli` on them keep passing).

## Check

`uv run python -m unittest tests/unit/test_aws_cli_acquisition.py -v` green (the sixteen existing tests, one changed, plus the four macOS tests), pasted in the validation file with `shellcheck install/ubuntu/common/aws_cli.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (`tools/aws-cli-macos`). The PR is ready for the orchestrator's integration when the ruleset's required checks are green (the macOS client job included), the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `dotfiles-T128-aws-cli-macos-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by dotfiles-T128-aws-cli-macos-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-aws-cli-macos-a01/task.md>` and the evidence paths. After the merge the operator runs `make update`; the applied `~/.local/bin/aws` then comes from AWS's installer and `brew list awscli` is the operator's hygiene step above.
