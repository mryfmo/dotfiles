---
format: 2
task_id: dotfiles-T129-assets-omp-hcom-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/update-agent-assets.sh
  - scripts/lib/installer-pins.sh
  - scripts/check-tools.sh
  - scripts/validate-agent-assets.py
  - tests/unit/test_update_agent_assets.py
  - tests/unit/test_validate_agent_assets.py
  - tests/install/common/check_tools.bats
  - .orchestration/dotfiles-T129-assets-omp-hcom-a01/**
after: []
threat_table:
  - control: "the PR edits home/dot_agents/agent-config.yaml in one place (assets.omp and assets.hcom with the fields item 1 lists; no other section)"
    disposition: "residual: the manifest's assets section is the installer list, not a seat's execution boundary (model_profiles and permissions untouched); the diff review and the audit compare against this row"
  - control: "the PR edits scripts/update-agent-assets.sh in three places (run_pinned_installer passes installer arguments after a -- separator, the tode and terminal-browser calls unchanged; update_omp and update_hcom added; both named in main's list)"
    disposition: "closed: tests/unit/test_update_agent_assets.py::test_update_omp_and_update_hcom_install_at_their_pins_and_refuse_a_drifted_version"
  - control: "the PR edits scripts/lib/installer-pins.sh in one place (the constants OMP_PIN_VERSION, OMP_INSTALLER_SHA256 and HCOM_PIN_VERSION, written by scripts/generate-agent-configs.py from the manifest's render entries as tode's are, never by hand)"
    disposition: "residual: a generated constants file the updater sources; the audit compares its values with the manifest's pin and sha256 fields"
  - control: the PR edits scripts/check-tools.sh in one place (omp and hcom reported with their versions against the pins)
    disposition: "residual: one probe per tool beside the existing ones; the two bats cases cover the lines in CI"
  - control: "the PR edits scripts/validate-agent-assets.py in three places (ASSET_VERIFY_BY_SOURCE gains uv-tool: {pypi-index-sha256}; PINNED_RELEASE_SOURCES and INSTALLING_ASSET_SOURCES gain uv-tool)"
    disposition: "closed: tests/unit/test_validate_agent_assets.py::test_a_uv_tool_asset_needs_an_exact_version_pin_a_reason_an_install_path_and_an_installer"
  - control: "the PR adds tests/unit/test_update_agent_assets.py (the one test of item 5, sourcing the updater with stub curl, uv, omp and hcom on PATH and HOME in a temporary directory)"
    disposition: "residual: stubs written by the test; the audit reads each case against items 2 and 3"
  - control: the PR edits tests/unit/test_validate_agent_assets.py only for the new case
    disposition: "residual: one new test beside the existing ones, which stay byte-identical"
  - control: "the PR edits tests/install/common/check_tools.bats only for the two new cases (omp and hcom lines), which run in CI only (the repository's test policy)"
    disposition: "residual: the cases assert the two check-tools lines on the CI image after the installers ran there"
  - control: "the installers as inputs (omp's install script fetched from the unversioned URL https://omp.sh/install and hashed against the manifest before it runs with --binary --ref v<pin>; hcom from PyPI through uv tool install hcom==<pin>)"
    disposition: "residual: the omp script runs only when its sha256 equals the manifest's (a changed upstream script fails until a reviewed bump); uv verifies every downloaded distribution against the sha256 the PyPI index serves and the exact version makes the file set fixed; both pins are manifest diffs the audit reads; after each install the binary's --version must equal the pin or the installer exits non-zero"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-assets-omp-hcom-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the unit test sources the updater in a bash subprocess (the main guard runs nothing on source) with stub curl, uv, omp and hcom on PATH that record their argv and HOME in a temporary directory, and imports only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; update-agent-assets.sh runs the tools it already runs plus the hashed omp installer and uv tool install, each resolved as the script resolves its tools today; the validator runs under uv with pyyaml as the agent-assets workflow already runs it; a PR checkout as cwd chooses nothing new"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script (two functions in the existing updater, one new test module); any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: the manifest on origin/main has no omp or hcom asset
    command: git show origin/main:home/dot_agents/agent-config.yaml | /usr/bin/grep -cE "^  (omp|hcom):" || true
    output: |-
      0
  - claim: check-tools on origin/main knows neither tool
    command: git show origin/main:scripts/check-tools.sh | /usr/bin/grep -cE "omp|hcom" || true
    output: |-
      0
  - claim: the validator on origin/main has no uv-tool source type, so item 2 adds it
    command: git show origin/main:scripts/validate-agent-assets.py | /usr/bin/grep -c "\"uv-tool\"" || true
    output: |-
      0
  - claim: run_pinned_installer on origin/main passes only environment assignments to the installer (one line), so item 3 adds the argument form omp needs
    command: 'git show origin/main:scripts/update-agent-assets.sh | /usr/bin/grep -cF ''env "$@" bash "${installer}"'' '
    output: |-
      1
  - claim: the bats module for check-tools and the rendered pin constants file exist on origin/main (both are extended, not added)
    command: for f in tests/install/common/check_tools.bats scripts/lib/installer-pins.sh; do git cat-file -e origin/main:$f && printf "%s present\n" "$f"; done
    output: |-
      tests/install/common/check_tools.bats present
      scripts/lib/installer-pins.sh present
---

# AGMSG-TASK dotfiles-T129-assets-omp-hcom-a01 — omp and hcom as pinned assets installed by make update on every machine (plan 023 PR A)

Written 2026-10-17 by the orchestrator seat as plan 023's PR A. The facts read today are in the plan: omp installs by `curl -fsSL https://omp.sh/install | sh` with `--binary --ref v<version>` or `brew install can1357/tap/omp`; hcom by `uv tool install hcom` (PyPI) or `brew install aannoo/hcom/hcom`. The manifest's `assets` section already pins installers of these kinds (`installer-script` for tode and terminal-browser, rendered into `scripts/lib/installer-pins.sh`; `github-release`; `git-commit`). Round 2 of this text applies the Codex half's round 1: the validator has no `uv-tool` source (premise 3), so this PR adds it with its field rules; the omp installer's sha256 is pinned in the manifest like tode's; `run_pinned_installer` passes environment only (premise 4), so it gains an argument form; the check-tools lines get bats cases in the existing module (premise 5).

## Goal

`make update` installs omp and hcom at the manifest's pins on the Mac and on spark, `check-tools` reports both against the pins, a drifted version is refused, and the validator rejects a `uv-tool` asset without an exact version, a reason, an install path and an installer.

## Files

1. `home/dot_agents/agent-config.yaml`: `assets.omp` with `source: installer-script`, `upstream: https://omp.sh/install`, `pin: v<the release the worker reads as current from the GitHub releases of can1357/oh-my-pi at task start>`, `verify: installer-sha256`, `sha256: <the sha256 of the installer text fetched at task start, pasted with its shasum line in the report>`, `note:` what the script does with `--binary --ref` and whether it checks the payload's SHA-256 (the worker quotes the script's lines in the report; the note says "the script checks the payload" or "the ref is the only check"), `reason: the install URL is unversioned and unsigned; the script hash pins the text and the ref pins the binary`, `install_path: ~/.local/bin/omp` (or the path the script installs to, read from the script), `installer: scripts/update-agent-assets.sh#update_omp`, `render: {file: scripts/lib/installer-pins.sh, constants: {OMP_PIN_VERSION: pin, OMP_INSTALLER_SHA256: sha256}}`; `assets.hcom` with `source: uv-tool`, `upstream: https://pypi.org/project/hcom/`, `pin: <the exact version the worker reads as current on PyPI at task start>`, `verify: pypi-index-sha256`, `reason: PyPI publishes a sha256 per file in its index, which uv checks on download; the exact version makes the resolution one fixed file set; no signature or attestation exists to verify independently`, `install_path: ~/.local/bin/hcom`, `installer: scripts/update-agent-assets.sh#update_hcom`, `render: {file: scripts/lib/installer-pins.sh, constants: {HCOM_PIN_VERSION: pin}}`. `scripts/lib/installer-pins.sh` is regenerated by `scripts/generate-agent-configs.py` (the three constants appear; nothing is typed by hand).
2. `scripts/validate-agent-assets.py`: `ASSET_VERIFY_BY_SOURCE["uv-tool"] = {"pypi-index-sha256"}`; `uv-tool` added to `PINNED_RELEASE_SOURCES` (a reason is required) and to `INSTALLING_ASSET_SOURCES` (install_path and installer are required); nothing else.
3. `scripts/update-agent-assets.sh`: `run_pinned_installer` accepts installer arguments after a `--` (everything after it is passed to `bash "${installer}"`; the two existing calls pass none and are unchanged); `update_omp`: when `omp --version` already prints the pin, say so and return; else `run_pinned_installer "${OMP_INSTALLER_URL}" "${OMP_INSTALLER_SHA256}" -- --binary --ref "${OMP_PIN_VERSION}"` (the `OMP_INSTALLER_URL` constant defined beside `TERMINAL_CODE_INSTALLER_URL`; if the fetched script takes its ref from an environment variable instead of arguments, the worker uses that form and names it in the report), then `omp --version` must print the pin, else exit 1 printing both values; `manifest_record` as the other installers call it. `update_hcom`: skip with the script's usual message when `uv` is absent; when `hcom --version` already prints the pin, say so and return; else `uv tool install --force "hcom==${HCOM_PIN_VERSION}"`, then `hcom --version` must print the pin, else exit 1 printing both values; `manifest_record`. Both functions join `main`'s list after `update_terminal_browser`.
4. `scripts/check-tools.sh`: one line each for omp and hcom, the installed version beside the pin from `scripts/lib/installer-pins.sh`.
5. Tests: `tests/unit/test_update_agent_assets.py` (new): `test_update_omp_and_update_hcom_install_at_their_pins_and_refuse_a_drifted_version` (a bash subprocess sources the updater, sets the three constants, and calls the two functions with HOME in a temporary directory and a PATH of stubs: `curl` writes a fixture installer whose sha256 the test computed into the constant and the fixture installer records its arguments and installs a stub `omp` answering the pin; `uv` records its argv and installs a stub `hcom` answering the pin: both functions exit 0, the recorded arguments carry `--binary --ref <pin>` and `hcom==<pin>`; a second call installs nothing (idempotent); a stub answering another version makes each function exit non-zero with both values in its output). `tests/unit/test_validate_agent_assets.py`: `test_a_uv_tool_asset_needs_an_exact_version_pin_a_reason_an_install_path_and_an_installer` (a manifest fixture with the hcom asset of item 1 validates; without `reason`, `install_path` or `installer`, or with `verify: sha256`, the validator fails with its message for that field). `tests/install/common/check_tools.bats`: two cases, the omp and hcom lines show the pinned versions after the installers ran on the CI image (bats runs in CI only).

## Out of scope

omp's configuration, skills providers and the hcom bus (PRs B and C); the operator's logins (`omp login`/`/login openai-codex`, the Anthropic API key, `hcom` setup); spark's relay; pstack (PR G, after this PR).

## Check

`uv run python -m unittest tests/unit/test_update_agent_assets.py tests/unit/test_validate_agent_assets.py -v` green and `uv run --with pyyaml scripts/validate-agent-assets.py` (exit 0) pasted in the validation file, with `shellcheck scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh`, the live run on the worker's machine (`bash -c 'source scripts/update-agent-assets.sh; update_omp; update_hcom'` then `omp --version` and `hcom --version`, pasted), the bats cases green in CI, and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (no other merge is a precondition). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50; every fix round, before or after the first RESULT, counts toward INV-6's cap of two, C-61); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59); a later review's P2 and every P3 are advisory (C-61), as is any other P2, owned by `dotfiles-T129-assets-omp-hcom-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T129-assets-omp-hcom-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md>` and the evidence paths.

## Change (round 2, 2026-10-17T10:18:21Z)

The Codex half's round 1 (one P1, three P2): the `uv-tool` source is added to the validator with its three set edits and a test, both files in allowed_files (item 2, premise 3); the omp installer's sha256 is pinned in the manifest and rendered into `scripts/lib/installer-pins.sh` like tode's (item 1; the file in allowed_files, premise 5); `run_pinned_installer` gains the argument form (item 3, premise 4); the check-tools lines get two cases in the existing `check_tools.bats` instead of a new module (item 5, premise 5); the Checks section carries the pasted pre-send output.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-assets-omp-hcom-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
premise 4: OK
premise 5: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-assets-omp-hcom-a01.md
```
