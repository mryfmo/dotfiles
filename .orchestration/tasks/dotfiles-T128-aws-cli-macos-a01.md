---
format: 2
task_id: dotfiles-T128-aws-cli-macos-a01
kind: code
security: false
reset_of: []
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
  - control: the PR edits install/ubuntu/common/aws_cli.sh, a script chezmoi runs on the operator's machine at every apply, which downloads and executes AWS's install.sh on macOS
    disposition: "closed: tests/unit/test_aws_cli_acquisition.py::test_macos_signature_failure_preserves_existing_aws_and_runs_no_installer"
  - control: the downloaded install.sh and the pkg it fetches (network input executed on the host)
    disposition: "residual: install.sh is verified with gpgv against the pinned AWS key (fingerprint FB5DB77F…, the same keyring logic as the Linux archive) before it runs, and install.sh itself refuses a pkg whose Apple signature is not team 94KV3E626L (its lines 461 to 475); a verification failure leaves the installed CLI untouched, which the closed row's test proves"
  - control: the PR adds home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl, a new script wrapper that chezmoi runs on macOS at every apply
    disposition: "residual: the wrapper only includes install/ubuntu/common/aws_cli.sh (the Ubuntu wrapper's form); it runs on a host only after the merge and the operator's make update, and the run_before dirty-source guard refuses an apply from an unmerged tree"
  - control: the PR edits install/macos/common/dependencies.sh, the run_once Homebrew package list
    disposition: "residual: the diff removes one name (awscli) and adds nothing; a fresh machine no longer installs the formula, and an existing machine changes only when the operator runs brew uninstall awscli && brew autoremove"
  - control: the PR edits tests/unit/test_aws_cli_acquisition.py, the oracle of its own change (it already reads BREW_PACKAGES at lines 636 to 637)
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test diff beside the script diff"
  - control: new or renamed scripts (the wrapper home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl is the one new file)
    disposition: "residual: it is named in allowed_files and consists of the include line; any other new or renamed script is an undeclared change the audit fails"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-aws-cli-macos-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance)"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and by the orchestrator at acceptance, never by a hand-written parser; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file, so a second front matter or a moved separator fails acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-aws-cli-macos-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: they are the worker's untrusted claims; acceptance re-checks each claim against the diff, CI and the test output, and the audit reads those sources itself"
  - control: in-process effects
    disposition: "residual: the unit tests run the script under bash with stubbed curl, gpgv and installer commands, as the existing tests do; nothing from the PR is imported into the test process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: none in allowed_files; an undeclared change to such a file is outside the task and fails at the audit (INV-12)"
  - control: orchestrator effects on this PR (merge, update-branch, forced worker removal)
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate; update-branch re-runs CI, the sweep and the audit on the new head; no forced removal is planned"
premises:
  - claim: "awscli is the only installed formula that uses python@3.14, a formula the upgrade script forbids; Homebrew upgrades a dependency with its dependent whatever the forbidden list says (Homebrew FAQ: pinned, outdated formulae that another formula depends on need to be upgraded when required)"
    command: "brew uses --installed python@3.14; brew deps --formula awscli | tr '\\n' ' '"
    output: |-
      awscli
      aws-c-auth aws-c-cal aws-c-common aws-c-compression aws-c-event-stream aws-c-http aws-c-io aws-c-mqtt aws-c-s3 aws-c-sdkutils aws-checksums ca-certificates lz4 mpdecimal openssl@3 python@3.14 readline s2n sqlite xz zstd
  - claim: "AWS signs install.sh (its .sig exists) and does not publish a .sig for the macOS pkg; install.sh verifies the pkg's Apple Developer team instead and installs for the current user under the XDG defaults"
    command: "for u in https://awscli.amazonaws.com/AWSCLIV2.pkg.sig https://awscli.amazonaws.com/v2/install.sh https://awscli.amazonaws.com/v2/install.sh.sig; do printf '%s -> ' \"$u\"; curl -sS -o /dev/null -w '%{http_code}\\n' -I \"$u\"; done; curl -sS https://awscli.amazonaws.com/v2/install.sh | grep -n -E 'AWS_CLI_PKG_TEAM_ID=|pkgutil --check-signature|XDG_DATA_HOME:-|XDG_BIN_HOME:-'"
    output: |-
      https://awscli.amazonaws.com/AWSCLIV2.pkg.sig -> 404
      https://awscli.amazonaws.com/v2/install.sh -> 200
      https://awscli.amazonaws.com/v2/install.sh.sig -> 200
      23:readonly AWS_CLI_PKG_TEAM_ID="94KV3E626L"
      304:    if [ -z "${XDG_DATA_HOME:-}" ] || [ -z "${XDG_BIN_HOME:-}" ]; then
      309:  local data_home="${XDG_DATA_HOME:-$HOME/.local/share}"
      310:  local bin_home="${XDG_BIN_HOME:-$HOME/.local/bin}"
      324:  info "  XDG_DATA_HOME=${XDG_DATA_HOME:-<unset, using default>}"
      325:  info "  XDG_BIN_HOME=${XDG_BIN_HOME:-<unset, using default>}"
      463:  if ! out="$(pkgutil --check-signature "$INSTALLER_PATH" 2>&1)"; then
  - claim: "the Ubuntu installer is Linux-only by its archive URL, and macOS installs awscli from Homebrew"
    command: "grep -n 'awscli-exe-linux' install/ubuntu/common/aws_cli.sh; grep -n -A2 'BREW_PACKAGES=(' install/macos/common/dependencies.sh"
    output: |-
      31:        printf 'https://awscli.amazonaws.com/awscli-exe-linux-%s.zip\n' "${architecture}"
      16:readonly BREW_PACKAGES=(
      17:    awscli
      18:    cmake
  - claim: "gpgv, which the macOS branch runs at every apply, comes from the gpg formula that BREW_PACKAGES keeps and run_once_before_50 installs before any run_after script"
    command: "grep -n -E '^    (gpg|awscli)$' install/macos/common/dependencies.sh"
    output: |-
      17:    awscli
      21:    gpg
---

# AGMSG-TASK dotfiles-T128-aws-cli-macos-a01 — install the AWS CLI on macOS through AWS's official installer, verified, instead of the Homebrew formula (plan 007 T715, option A, operator decision 2026-10-12)

Written 2026-10-12 by the orchestrator seat under plan 007 (Phase 5, T715). Review tier by INV-1 (`kind: code`, no design-tier path). The macOS install becomes what the Ubuntu install already is: AWS's own distribution, signature-verified, under `~/.local/share/aws-cli` with the `~/.local/bin/aws` symlink, updated at every apply when AWS publishes a new release. The manifest `assets.aws-cli` in `home/dot_agents/agent-config.yaml` is not touched: its `installer:` and `render.file:` paths stay, and the generator rewrites only the fingerprint constant. The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C6 pass on this file.

## What to do

1. `install/ubuntu/common/aws_cli.sh`: add a macOS branch keyed on `uname -s` (`Darwin`), keeping the Linux branch as it is.
   - Download `https://awscli.amazonaws.com/v2/install.sh` and `https://awscli.amazonaws.com/v2/install.sh.sig` (exit 3 on a download failure, as the Linux branch does), verify with `gpgv` against the dearmored pinned key exactly as `install_aws_cli` does for the archive, and only then run `bash <install.sh>` with `XDG_DATA_HOME` and `XDG_BIN_HOME` set so the result lands in `AWS_CLI_INSTALL_DIR`'s parent (`~/.local/share`) and `AWS_CLI_BIN_DIR` (`~/.local/bin`); keep `verify_aws_cli_install` as the postcondition.
   - The ETag skip (`aws_cli_archive_etag`, `main`) uses `https://awscli.amazonaws.com/AWSCLIV2.pkg` as the macOS URL; a changed ETag means a new release, as on Linux.
   - `gpgv` is present on a brewed macOS through the `gpg` formula in `BREW_PACKAGES` (line 21), installed by run_once_before_50 before any run_after script; this task keeps that entry.
   - Update the shdoc header: the file installs the current AWS CLI from AWS's official distribution on Linux (archive) and macOS (install.sh and pkg), each verified. Comments in English, shdoc form.
2. `home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl`: the macOS twin of the Ubuntu wrapper, `{{ if eq .chezmoi.os "darwin" }}{{ include "../install/ubuntu/common/aws_cli.sh" }}{{ end }}` in the Ubuntu wrapper's layout.
3. `install/macos/common/dependencies.sh`: remove `awscli` from `BREW_PACKAGES`. Nothing else in the list changes.
4. Tests: in `tests/unit/test_aws_cli_acquisition.py`, the macOS cases in the existing style (stubbed `uname`, `curl`, `gpgv`, `bash`): the URL pair by OS; a `gpgv` failure on install.sh preserves the existing `aws` and runs no installer (the `closed` row's test name, exactly `test_macos_signature_failure_preserves_existing_aws_and_runs_no_installer`); a verified install.sh is invoked with `XDG_DATA_HOME` and `XDG_BIN_HOME` set to the install root and bin dir; the ETag skip uses the pkg URL on macOS. The existing assertion at `tests/unit/test_aws_cli_acquisition.py` lines 636 to 637 (it asserts `awscli` is the first `BREW_PACKAGES` entry) becomes: `awscli` absent and `gpg` present.
5. Report, for the operator's one-time hygiene after the merge and `make update` (not the worker's to run): `brew autoremove --dry-run` after `brew uninstall awscli`, expected to list python@3.14 and the aws-c-* family.

## Validation

- `uv run --no-project python -m unittest tests/unit/test_aws_cli_acquisition.py -v` output in the validation file, with the new tests named.
- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps).
- `shellcheck install/ubuntu/common/aws_cli.sh` output if shellcheck is on PATH (state it if not).

## Completion

The PR is ready for the orchestrator's integration when CI is green (the macOS client job included), the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. Branch `tools/aws-cli-macos`, draft PR from `origin/main`, `kind: code`.
