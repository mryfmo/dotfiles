---
format: 2
task_id: dotfiles-T128-homebrew-attestation-token-a01
kind: code
security: false
reset_of: []
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/upgrade-tools.sh
  - tests/unit/test_upgrade_tools.py
  - .orchestration/dotfiles-T128-homebrew-attestation-token-a01/**
after: []
threat_table:
  - control: the PR edits scripts/upgrade-tools.sh, which make update runs on the operator's machine with the operator's gh login
    disposition: "closed: tests/unit/test_upgrade_tools.py::test_attestation_token_comes_from_the_environment_or_gh_and_never_prints"
  - control: the gh token placed in HOMEBREW_GITHUB_API_TOKEN for the brew process (a credential crossing into a child process)
    disposition: "residual: the variable is a function-local export (local -x) around the brew calls only, never echoed, never written to a file; Homebrew documents HOMEBREW_GITHUB_API_TOKEN as its token input and needs no scope, so a dedicated no-scope token in the private chezmoi domain (operator, optional) replaces the gh token without a code change"
  - control: the PR adds tests/unit/test_upgrade_tools.py, the oracle of its own change
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test beside the script; the test stubs gh and brew and asserts the environment the brew stub sees"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-homebrew-attestation-token-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared at acceptance)"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: the branch evidence records under .orchestration/dotfiles-T128-homebrew-attestation-token-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: the worker's untrusted claims; acceptance re-checks each against the diff, CI and the test output"
  - control: in-process effects
    disposition: "residual: the unit test runs the script's function under bash with stubbed gh and brew; nothing from the PR is imported into the test process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: none in allowed_files; an undeclared change to such a file fails at the audit (INV-12)"
  - control: new or renamed scripts
    disposition: "residual: the new file is the test module only; a new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: "the script turns attestation verification on whenever gh is on PATH and supplies no token"
    command: "sed -n '123,126p' scripts/upgrade-tools.sh"
    output: |-
      if has_command gh; then
              # Homebrew verifies bottle build-provenance attestations through gh (HOMEBREW_VERIFY_ATTESTATIONS).
              local -x HOMEBREW_VERIFY_ATTESTATIONS=1
          else
  - claim: "Homebrew 7.0.9 resets PATH to the system directories, looks the token up as HOMEBREW_GITHUB_API_TOKEN, then gh auth token on that PATH plus /opt/homebrew/opt/gh/bin, then the keychain, and refuses to verify with no token; on this machine gh is mise-installed, so the lookup finds nothing"
    command: "grep -n 'PATH=\"/usr/bin' /opt/homebrew/bin/brew; sed -n '130,131p' /opt/homebrew/Library/Homebrew/utils/attestation.rb; sed -n '219,221p' /opt/homebrew/Library/Homebrew/utils/github/api.rb; brew ruby -e 'require \"utils/github/api\"; puts(GitHub::API.github_cli_token.nil? ? \"github_cli_token=nil\" : \"github_cli_token=present\")' 2>&1 | tail -1"
    output: |-
      301:PATH="/usr/bin:/bin:/usr/sbin:/sbin"
            credentials = GitHub::API.credentials
            raise GhAuthNeeded, "missing credentials" if credentials.blank?
            @credentials ||= Homebrew::EnvConfig.github_api_token.presence
            @credentials ||= github_cli_token
            @credentials ||= keychain_username_password
      github_cli_token=nil
  - claim: "the operator's make update of 2026-10-12 10:0xZ aborted the Homebrew batch on the first bottle to reach verification, and 14 formulae stay outdated"
    command: "brew outdated --formula --quiet | wc -l"
    output: "      14"
---

# AGMSG-TASK dotfiles-T128-homebrew-attestation-token-a01 — hand Homebrew the token it needs for bottle attestation (plan 007 T714)

Written 2026-10-12 by the orchestrator seat under plan 007 (Phase 5, T714; approval pending at drafting time). Review tier by INV-1 (`kind: code`; `scripts/upgrade-tools.sh` is on no design-tier list). The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C6 pass on this file.

## Why

`make update` turns Homebrew's bottle attestation on (premise 1) but Homebrew cannot find a token through the mise-installed gh (premise 2: "The bottle for aws-c-s3 could not be verified. This typically indicates a missing GitHub API token"), so every run aborts the Homebrew section (premise 3). Dropping the check is not an option (supply-chain verification stays); the fix supplies the token the way Homebrew documents (`HOMEBREW_GITHUB_API_TOKEN`; the Manpage says Homebrew needs no scopes for it).

## What to do

1. In `upgrade_homebrew()` of `scripts/upgrade-tools.sh`, inside the `has_command gh` branch: export, function-local (`local -x`), the variable `HOMEBREW_GITHUB_API_TOKEN`: keep the caller's value when the environment already sets it, otherwise take the output of `gh auth token 2> /dev/null || true`. (Write the assignment so that the repository masker leaves it alone: the masker redacts a literal of the form NAME="…" when NAME ends in TOKEN, which is why this sentence names no literal.) When the result is empty, print `gh has no token; Homebrew bottle attestation verification is skipped.` and do not set `HOMEBREW_VERIFY_ATTESTATIONS` (the same policy the script already applies when gh is absent). Never print the token. Update the shdoc comment of the function (English, shdoc form).
2. `tests/unit/test_upgrade_tools.py` (new): in the style of `tests/unit/test_aws_cli_acquisition.py` (run the function under bash with stub commands on PATH), three tests: with a `gh` stub printing a token, the `brew` stub sees `HOMEBREW_VERIFY_ATTESTATIONS=1` and `HOMEBREW_GITHUB_API_TOKEN` equal to the stub's token and the script's stdout never contains the token (`test_attestation_token_comes_from_the_environment_or_gh_and_never_prints`); with `HOMEBREW_GITHUB_API_TOKEN` already set, `gh auth token` is not called and the environment value wins; with a `gh` stub printing nothing, verification is off and the skip message is printed.
3. Nothing else changes in the script: the forbidden-formula list, the dependents check, the mise and uv sections.

## Validation

- `uv run --no-project python -m unittest tests/unit/test_upgrade_tools.py -v` output in the validation file.
- `shellcheck scripts/upgrade-tools.sh` output if shellcheck is on PATH (state it if not).
- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps).

## Completion

The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. Branch `tools/homebrew-attestation-token`, draft PR from `origin/main`. After the merge the operator's next `make update` is the measurement: the Homebrew section ends with 0 optional warnings.
