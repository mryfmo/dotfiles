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
  - tests/unit/test_update_agent_assets.py
  - tests/install/common/check_tools.bats
  - tests/unit/test_runtime_health.py
  - tests/unit/test_asset_manifest.py
  - .orchestration/dotfiles-T129-assets-omp-hcom-a01/**
after: []
threat_table:
  - control: "the PR edits home/dot_agents/agent-config.yaml in one place (assets.omp and assets.hcom, both source https-download with pin, verify sha256, the recorded hashes and URLs, reason, install_path, installer and render; no other section)"
    disposition: "residual: the manifest's assets section is the installer list, not a seat's execution boundary (model_profiles and permissions untouched); the diff review and the audit compare the recorded values with the sources pasted in the task text"
  - control: "the PR edits scripts/update-agent-assets.sh in two places (update_omp and update_hcom, each download, sha256 comparison, install from the verified file, --version check; both named in main's list after update_terminal_browser)"
    disposition: "closed: tests/unit/test_update_agent_assets.py::test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin and ::test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin"
  - control: "the PR edits scripts/lib/installer-pins.sh in one place (the constants OMP_PIN_VERSION, OMP_TARBALL_SHA256, HCOM_PIN_VERSION and the four HCOM_<PLATFORM>_SHA256 and HCOM_<PLATFORM>_URL pairs, written by scripts/generate-agent-configs.py from the two render entries as crit's are, never by hand)"
    disposition: "residual: a generated constants file the updater sources; the audit compares its values with the manifest's fields and with the sources in the task text"
  - control: the PR edits scripts/check-tools.sh in one place (omp and hcom reported with their versions against the pins, in the crit line's form)
    disposition: "residual: one probe per tool beside the existing ones; the two bats cases cover the lines in CI"
  - control: "the PR adds tests/unit/test_update_agent_assets.py (the two tests of item 5, sourcing the updater with stub curl, npm, uv, omp and hcom on PATH and HOME in a temporary directory)"
    disposition: "residual: stubs and fixture downloads written by the test; the audit reads each case against item 3"
  - control: "the PR edits tests/unit/test_runtime_health.py only for the optional-warning count and its fixture (the two new absence warnings of check-tools raise the expected count from 1 to 3; Amendment 3) and for the three updater main-caller fixtures, which gain stubs for update_omp and update_hcom so their isolation and curl-failure assumptions hold (Amendment 4)"
    disposition: "residual: the count, the fixture and the three stubs change, no assertion is removed; the audit's diff review checks the module against this row"
  - control: "the PR edits tests/unit/test_asset_manifest.py only for the install-step fixture of test_updater_has_one_recording_call_for_each_install_step (the two new manifest_record calls, 15 to 17; Amendment 5)"
    disposition: "residual: the step list grows by the two new steps, no assertion is removed; the audit's diff review checks the module against this row"
  - control: "the PR edits tests/install/common/check_tools.bats only for the two new cases (omp and hcom lines), which run in CI only (the repository's test policy)"
    disposition: "residual: the cases run check-tools with a stub binary at the pin and without it, as the check_crit_cli cases do"
  - control: "the downloads as inputs (the omp tarball https://registry.npmjs.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-18.11.3.tgz and the hcom wheel of the host's platform from files.pythonhosted.org)"
    disposition: "residual: each download is compared with the rendered sha256 before anything runs (the install_crit_release pattern, premise 4); npm installs the verified tarball file and uv installs the verified wheel file, never a name a registry resolves at install time; a changed upstream file fails until a reviewed pin bump; after each install the binary's --version must equal the pin or the installer exits non-zero; nothing is installed in any seat's sandbox and no sandbox permission changes: the install runs where the operator runs make update after the merge"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-assets-omp-hcom-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the unit tests source the updater in a bash subprocess (the main guard runs nothing on source) with stub curl, npm, uv, omp and hcom on PATH that record their argv, HOME in a temporary directory and the constants set by the test, and import only the standard library; nothing is imported into another process and nothing reaches the network"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; update-agent-assets.sh runs curl, shasum, npm (mise's node) and uv as it resolves its tools today, under make update as today (premise 6); the validator runs under uv with pyyaml as the agent-assets workflow already runs it; a PR checkout as cwd chooses nothing new"
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
  - claim: the validator accepts verify sha256 on an https-download asset (one line), so no validator change is needed
    command: 'git show origin/main:scripts/validate-agent-assets.py | /usr/bin/grep -cF "\"https-download\": {\"sha256\", \"gpg\"}"'
    output: |-
      1
  - claim: 'the crit installer is the pattern: one function downloads, compares the sha256 with the rendered constant and installs the verified file, and four platform lines pick the constant'
    command: a=$(git show origin/main:scripts/update-agent-assets.sh | /usr/bin/grep -c "^function install_crit_release"); b=$(git show origin/main:scripts/update-agent-assets.sh | /usr/bin/grep -cE "checksum=.*CRIT_(LINUX|DARWIN)_(AMD64|ARM64)_SHA256"); echo "$a $b"
    output: |-
      1 4
  - claim: the bats module for check-tools and the rendered pin constants file exist on origin/main (both are extended, not added)
    command: for f in tests/install/common/check_tools.bats scripts/lib/installer-pins.sh; do git cat-file -e origin/main:$f && printf "%s present\n" "$f"; done
    output: |-
      tests/install/common/check_tools.bats present
      scripts/lib/installer-pins.sh present
  - claim: make update already runs the updater (the lines naming it in the Makefile), so the two functions run on every machine with no Makefile change
    command: git show origin/main:Makefile | /usr/bin/grep -c "update-agent-assets.sh"
    output: |-
      3
---

# AGMSG-TASK dotfiles-T129-assets-omp-hcom-a01 — omp and hcom as pinned assets installed by make update on every machine (plan 023 PR A)

Written 2026-10-17 by the orchestrator seat as plan 023's PR A. Amendment 2 (2026-10-17T10:46:55Z) follows the operator's instruction of 19:4x JST: nothing is installed in a sandbox; PR A pins version, URL and sha256 in `agent-config.yaml`, puts the install into `update-agent-assets.sh` (which `make update` runs, premise 6), and tests it with fake binaries, a reproduced download and a hash comparison; the real install is the operator's `make update` after the merge; the sandbox's permission scope stays as it is. Both tools are `https-download` assets with `verify: sha256` (premise 3), installed the way `install_crit_release` installs crit (premise 4): download, compare the sha256 with the rendered constant, install from the verified file, check `--version`.

Pinned values and their sources (read by the orchestrator, outside any seat's task):

- omp: `https://registry.npmjs.org/@oh-my-pi%2Fpi-coding-agent` (read 2026-10-17T10:33Z): `dist-tags.latest` = `18.11.3`, published 2026-10-16T21:52:39.004Z, `bin` omp → `dist/cli.js`, `dist.tarball` = `https://registry.npmjs.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-18.11.3.tgz`, `dist.integrity` = `sha512-7MdQBaj/zGHG7uV0mJSrYGHsjX3xthYgXUxTxLeJeFFL15UAnyE99kAfDE66c8LdXU0dN34eTyw6lfM7K5ouCg==`, `dist.shasum` = `a187bd1b0ef31c17e18b456846309f64fe92cf87`. The tarball fetched 2026-10-17T10:44:00Z: 14684952 bytes, sha256 `b4a4eaf8057a7591f4ca83be293780489fd72b174e6a629d4704320165177f09`; its sha512 equals the registry's integrity.
- hcom: `https://pypi.org/pypi/hcom/json` (read 2026-10-17T10:33Z): `info.version` = `0.7.30`; the platform wheels (no sdist, no universal wheel), `filename`, sha256, URL:
  - darwin-arm64 `hcom-0.7.30-py3-none-macosx_11_0_arm64.whl` `764b6469ce4fe470094d2fb821285ea5e7e002726c68c634752663abe2410ea4` `https://files.pythonhosted.org/packages/f5/ed/5e951b0e6fcadef1a2598e82b969b3eaa387a3e202f8987102d0e84cddfc/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl`
  - darwin-amd64 `hcom-0.7.30-py3-none-macosx_10_12_x86_64.whl` `bb32f2e0357e067c03827fc3c8e1319d67874b7bc49977c5e69b95a11a2a9bfb` `https://files.pythonhosted.org/packages/ba/c3/04dd3c68d87620fa347372b5e9450c3bb3518aa096abdf08169e6d2ce37f/hcom-0.7.30-py3-none-macosx_10_12_x86_64.whl`
  - linux-amd64 `hcom-0.7.30-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` `38b4424fb335cd6faa70010823682e53a4a2e29e31a36a977874a13f11ad0992` `https://files.pythonhosted.org/packages/21/fb/0a48f19a1c39b4ff59412f1fe34130c14acbc55da69097018d729191c6d2/hcom-0.7.30-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`
  - linux-arm64 `hcom-0.7.30-py3-none-manylinux_2_28_aarch64.whl` `278202e8eedce8a838785be8153b26b36fee0662640fc838fc7048da01aaba81` `https://files.pythonhosted.org/packages/f0/23/e746ce90643a1286ed3c6410c66eaae7134fbd2267d002814e6a932a2b60/hcom-0.7.30-py3-none-manylinux_2_28_aarch64.whl`

## Goal

`make update` installs omp 18.11.3 and hcom 0.7.30 from downloads whose sha256 equals the manifest's, refuses a drifted download or a drifted installed version, and `check-tools` reports both against the pins; the unit tests prove it with stubs and no network.

## Files

1. `home/dot_agents/agent-config.yaml`: `assets.omp` with `source: https-download`, `upstream: https://registry.npmjs.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-18.11.3.tgz`, `pin: "18.11.3"`, `verify: sha256`, `sha256: b4a4eaf8057a7591f4ca83be293780489fd72b174e6a629d4704320165177f09`, `note:` the registry facts above (integrity, shasum, published, bin, the fetch time), `reason: the npm registry serves an integrity hash from the same registry and no signature or attestation; the reviewed sha256 of the exact tarball is the check`, `install_path: ~/.local/bin/omp`, `installer: scripts/update-agent-assets.sh#update_omp`, `render: {file: scripts/lib/installer-pins.sh, constants: {OMP_PIN_VERSION: pin, OMP_TARBALL_SHA256: sha256}}`; `assets.hcom` with `source: https-download`, `upstream: https://pypi.org/project/hcom/0.7.30/#files`, `pin: "0.7.30"`, `verify: sha256`, `sha256:` the four-platform map above (keys `darwin-arm64`, `darwin-amd64`, `linux-amd64`, `linux-arm64`, as crit's), `files:` the four URLs above under the same keys, `note:` the PyPI read time and that no sdist exists, `reason: PyPI serves a sha256 per file from the same index and no signature or attestation; the reviewed sha256 of the exact wheel is the check`, `install_path: ~/.local/bin/hcom`, `installer: scripts/update-agent-assets.sh#update_hcom`, `render: {file: scripts/lib/installer-pins.sh, constants: {HCOM_PIN_VERSION: pin, HCOM_DARWIN_ARM64_SHA256: sha256.darwin-arm64, HCOM_DARWIN_AMD64_SHA256: sha256.darwin-amd64, HCOM_LINUX_AMD64_SHA256: sha256.linux-amd64, HCOM_LINUX_ARM64_SHA256: sha256.linux-arm64, HCOM_DARWIN_ARM64_URL: files.darwin-arm64, HCOM_DARWIN_AMD64_URL: files.darwin-amd64, HCOM_LINUX_AMD64_URL: files.linux-amd64, HCOM_LINUX_ARM64_URL: files.linux-arm64}}`. If the generator cannot render a `files.<key>` path, the four URLs become constants beside `TERMINAL_CODE_INSTALLER_URL` in the updater instead and the report says so; the manifest keeps them under `files:` as the record either way.
2. `scripts/lib/installer-pins.sh`: regenerated by `scripts/generate-agent-configs.py` as the Makefile runs it (the constants of item 1 appear; nothing is typed by hand).
3. `scripts/update-agent-assets.sh`: `update_omp`: skip with the script's usual message when `npm` is absent; when `omp --version` already prints the pin, say so and return; else download `OMP_TARBALL_URL` (`https://registry.npmjs.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-${OMP_PIN_VERSION}.tgz`, defined beside `TERMINAL_CODE_INSTALLER_URL`) to a temporary file, compare `shasum -a 256` with `OMP_TARBALL_SHA256` (mismatch: exit 1 printing both, nothing installed), `npm_config_min_release_age=0 npm install -g --prefix "${HOME}/.local" "<the verified tarball file>"` (the cooldown set to zero for this one command only, as `ensure_mise_npm_agent_cli` already does for the harness CLIs: the reviewed sha256 of the tarball is this install's review; decision D-omp-cooldown, Amendment 5; a test asserts the assignment is on that command and nowhere else), then `omp --version` must print the pin, else exit 1 printing both; `manifest_record` as the other installers call it. `update_hcom`: `case "$(uname -s)/$(uname -m)"` picks the platform's `HCOM_<PLATFORM>_URL` and `HCOM_<PLATFORM>_SHA256` (the four crit lines' form; an unsupported platform skips with the usual message); skip when `uv` is absent; when `hcom --version` already prints the pin, say so and return; else download the wheel to a temporary file, compare its sha256 (mismatch: exit 1 printing both, nothing installed), `uv tool install --force "<the verified wheel file>"`, then `hcom --version` must print the pin, else exit 1 printing both; `manifest_record`. Both functions join `main`'s list after `update_terminal_browser`; temporary files are removed on return as `run_pinned_installer` removes its own.
4. `scripts/check-tools.sh`: one line each for omp and hcom, the installed `--version` beside `OMP_PIN_VERSION` and `HCOM_PIN_VERSION` from `scripts/lib/installer-pins.sh`, in the form the crit line uses (absent: a warning, not a failure).
5. Tests: `tests/unit/test_update_agent_assets.py` (new): `test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin` (a bash subprocess sources the updater with HOME in a temporary directory, a PATH of stubs and the constants set by the test: stub `curl` writes a fixture tarball (any bytes) to the `-o` path and records the URL, `OMP_TARBALL_SHA256` is that fixture's sha256; stub `npm` records its argv and writes a stub `omp` answering the pin: exit 0, the recorded URL names the pin, the recorded argv is `install -g --prefix <HOME>/.local <tarball path>`; a second run installs nothing (idempotent); with `OMP_TARBALL_SHA256` set to another value the function exits non-zero printing both hashes and npm records no call; with a stub `omp` answering another version after the install the function exits non-zero printing both versions) and `test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin` (the same shape with stub `uv` recording `tool install --force <wheel path>`, the test host's platform constants set from the fixture, and the two drift cases). `tests/install/common/check_tools.bats`: two cases, the omp and hcom lines with a stub binary at the pin reported, and absent reported as a warning, as the check_crit_cli cases are written (bats runs in CI only).

## Out of scope

Installing anything on any machine (the operator runs `make update` after the merge); omp's configuration, skills providers and the hcom bus (PRs B and C); the operator's logins; spark's relay; pstack (PR G, after this PR); any change to a sandbox's permission scope.

## Check

`uv run python -m unittest tests/unit/test_update_agent_assets.py -v` green and `uv run --offline --with pyyaml scripts/validate-agent-assets.py` (exit 0) pasted in the validation file, with `shellcheck scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh`, the bats cases green in CI, and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (no other merge is a precondition). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50; every fix round, before or after the first RESULT, counts toward INV-6's cap of two, C-61); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59); a later review's P2 and every P3 are advisory (C-61), as is any other P2, owned by `dotfiles-T129-assets-omp-hcom-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T129-assets-omp-hcom-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md>` and the evidence paths.

## Change (round 2, 2026-10-17T10:18:21Z)

The Codex half's round 1 (one P1, three P2): the `uv-tool` source is added to the validator with its three set edits and a test, both files in allowed_files (item 2, premise 3); the omp installer's sha256 is pinned in the manifest and rendered into `scripts/lib/installer-pins.sh` like tode's (item 1; the file in allowed_files, premise 5); `run_pinned_installer` gains the argument form (item 3, premise 4); the check-tools lines get two cases in the existing `check_tools.bats` instead of a new module (item 5, premise 5); the Checks section carries the pasted pre-send output.

## Amendment 1 (round 2, 2026-10-17T10:4xZ)

a004's PONGs of 10:25Z and 10:27Z (status=blocked): its permission gate refused `gh release view --repo can1357/oh-my-pi` (releases are the operator's; read-only or not, the gate decides by policy), and the live install writes `~/.local/bin` and uv's tool state outside the Codex writable roots. The orchestrator's own gate refused the same release read and the installer fetch. Changes: omp is a mise npm tool at `18.11.3` (item 1, premise 4), no installer script, no `assets.omp`, no `run_pinned_installer` change; hcom keeps the `uv-tool` asset at `0.7.30`; the live install is the orchestrator's at acceptance (`mise install "npm:@oh-my-pi/pi-coding-agent"` and `uv tool install hcom==0.7.30` on this host under the tool-manager exemption, `omp --version` and `hcom --version` pasted in the acceptance record), so the worker's checks are the unit tests, the validator and shellcheck; the facts the worker would have read are pasted above. The worker's saved untracked records in worker-e stay; the branch starts from `origin/main` at 35ab0e95 or later.

## Amendment 2 (round 2, 2026-10-17T10:46:55Z)

The operator's instruction (19:4x JST): no install in a sandbox; PR A pins version, URL and sha256 in `agent-config.yaml`, puts the install into `update-agent-assets.sh` under `make update`, tests with fake binaries, a reproduced download and a hash comparison; the latest versions come from the registries when `gh release view` is unusable; the sandbox permission scope is unchanged; the real install is the operator's `make update` after the merge. Changes from Amendment 1: omp returns to the manifest as an `https-download` asset pinned by the tarball's sha256 (no mise line, no `home/dot_mise/config.toml`), hcom becomes an `https-download` asset pinned per platform wheel (no `uv-tool` source, so `scripts/validate-agent-assets.py` and its test leave allowed_files), both installed from the verified file; the orchestrator's acceptance-time install of Amendment 1 is withdrawn; the registry facts and the tarball hash are pasted above with their sources and fetch times.

## Amendment 3 (round 2, 2026-10-17T11:08:23Z)

a004's question (PONG 11:07Z): check-tools' two new absence warnings (omp, hcom not installed) raise the optional-warning count `tests/unit/test_runtime_health.py` asserts from 1 to 3. Decided by default: `tests/unit/test_runtime_health.py` joins allowed_files for that count and its fixture only (the real warning count stays, nothing is suppressed); the import of the pins into check-tools stays source-time as a004 proposed. Nothing else changes.

## Amendment 4 (round 2, 2026-10-17T11:11:16Z)

a004's addendum (PONGs 11:08Z and 11:10Z): the three updater main-caller fixtures in `tests/unit/test_runtime_health.py` need stubs for `update_omp` and `update_hcom` (their curl-failure fixtures otherwise stop `main` at the new download). Decided by default: the threat row covers those three fixtures' stubs too; no assertion is removed; nothing else changes.

## Amendment 5 (round 2, 2026-10-17T11:37:48Z)

a004's question (PONG 11:36Z) on PR #388 head f9c5e1a5: CI fails in `tests/unit/test_asset_manifest.py::test_updater_has_one_recording_call_for_each_install_step` (15 vs 17 steps; the module was outside allowed_files) and in public-bootstrap, where the real npm registry answers ETARGET for `@oh-my-pi/omp-stats@18.11.3` under the inherited `min-release-age` of 72 hours (omp 18.11.3 was published 2026-10-16T21:52Z). Decided by default: `tests/unit/test_asset_manifest.py` joins allowed_files for the step fixture only; `npm_config_min_release_age=0` is set on the omp install command only (the existing harness-CLI pattern; the pinned tarball hash is the review), with an env-assertion test, no global policy change and no CI suppression (decision D-omp-cooldown). This is fix round 2 of INV-6's two; a further fix is the operator's decision.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-assets-omp-hcom-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
premise 4: OK
premise 5: OK
premise 6: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-assets-omp-hcom-a01.md
```
