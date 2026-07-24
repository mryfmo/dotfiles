# Plan 005: Make runtime health, recovery, privacy, and verification truthful

> **Executor instructions**: This plan has seven independent phases but one
> shared outcome: success must mean the required behavior actually works. Follow
> phase order because later verification relies on earlier truthful exit codes.
> Add a regression test before each non-trivial behavior change. Do not run Bats
> locally. Regenerate managed agent assets only through the repository generator.
>
> **Drift check**: `git diff --stat e7c2808..HEAD -- .gitignore Makefile scripts/check-tools.sh scripts/upgrade-tools.sh home/dot_local/bin/common/executable_agent-fanout home/dot_local/bin/common/executable_herdr-agents home/dot_ccstatusline/settings.json home/dot_agents tests .github/workflows/test.yaml`

## Status

- **Execution**: DONE — PR #72, merge `11d27f5`
- **Priority**: P1
- **Effort**: L
- **Risk**: MED — stricter failures may expose previously hidden environment debt
- **Depends on**: Plan 002 for meaningful review; Plans 003-004 for stable bootstrap/tool versions
- **Category**: security, correctness, performance, tests, operability
- **Planned at**: commit `e7c2808`, 2026-07-11

## Plan quality self-audit

- [x] Compared with the early-plan standard; L scope has seven phases, measured
      evidence, explicit commands, and phase-specific adversarial checks.
- [x] Required Steps, Commands, Scope, Test plan, Maintenance, STOP, and 安全回帰
      sections are present.
- [x] Current-state `file:line` evidence was measured at `e7c2808`.
- [x] F07, F12, F13, F15, F16, F17, and F19 map to unique task ranges.
- [x] Every phase has positive and adversarial oracles.
- [x] Generated files are changed only through existing generation tooling.
- [x] No daemon, cache service, logging framework, or test framework is added.
- [x] DONE requires a repeated audit plus review/CI acceptance evidence.

## Why this matters

Several runtime surfaces report nominal success while their required behavior is
missing: doctor always succeeds, upgrade swallows required failures, a labeled
Herdr files pane may contain no Yazi, configuration changes are not reloaded,
and placeholder Bats files assert nothing. Meanwhile agent prompts are stored in
an unignored directory and statusline rendering invokes rolling npm packages.

The invariant is operational truth: required failure returns nonzero, sensitive
runtime artifacts are private and uncommittable, a files pane means live Yazi,
and required CI checks contain real assertions.

## Current state

- `.gitignore:9` ignores `.agents/worklog/` but not `.agents/runs/`.
- `home/dot_local/bin/common/executable_agent-fanout:94-101` creates
  `.agents/runs/<timestamp>` and writes the prompt verbatim.
- The same helper writes agent stdout/stderr under that directory without an
  explicit restrictive umask.
- `scripts/check-tools.sh:29` reports missing tools without accumulating a
  failing exit status; `Makefile:62-64` exposes it as `make doctor` only.
- `scripts/check-agent-runtime.py` exists but doctor does not invoke it.
- `scripts/upgrade-tools.sh:172-182` continues after required mise list/tool
  failures; uv and GitHub extension failures are discarded at lines 315 and 327.
- `home/dot_local/bin/common/executable_herdr-agents:151-155` identifies a files
  pane only by `label == "files"`.
- `home/dot_local/bin/common/executable_herdr-agents:240-242` starts Yazi only
  when no labeled pane exists.
- `Makefile:42-53` applies files and updates agent assets without reloading a
  running Herdr server.
- `tests/files/macos.bats` and `tests/files/ubuntu.bats` contain no active file
  assertions; `tests/install/ubuntu/server/empty.bats` is empty.
- `home/dot_ccstatusline/settings.json:9` executes
  `npx -y ccusage@latest statusline` with a long timeout.
- `home/dot_agents/agent-config.yaml:143` declares `npx ccstatusline@latest`;
  generated assets derive from this source.
- `.github/workflows/test.yaml:141-144` runs shfmt but installs/runs no ShellCheck.
- Manual ShellCheck at `e7c2808` reports unquoted HOME expansions in
  `install/ubuntu/server/ssh_server.sh:52,66` plus informational generator findings.

### Completion-state evidence at merge `11d27f5`

- `scripts/check-tools.sh:154` returns success only when required failures are zero.
- `scripts/upgrade-tools.sh:448` preserves the same required-failure invariant.
- `tests/unit/test_runtime_health.py:81` begins the private artifact and umask regression coverage.
- `tests/unit/test_herdr_agents.py:479` exercises the full Ghostty/Herdr/agmsg workspace path.
- `tests/files/helpers.bash:16` fails closed unless the isolated chezmoi executable is explicit.
- `scripts/check-statusline-tools.py:20` pins both offline statusline tool versions.
- `tests/unit/test_files_fixture.py:31` protects legacy macOS and Ubuntu fixture initialization.
- `tests/unit/test_statusline_tools.py:16` covers direct pinned statusline execution.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Python tests | `make unit-test` | exit 0 |
| Agent assets | `make validate-agent-assets` | exit 0 |
| Generate assets | `./scripts/update-agent-assets.sh` | exit 0; only expected generated diffs |
| Shell static checks | `git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x` | exit 0 |
| Shell format | `shfmt --indent 4 --space-redirects --diff .` | exit 0 |
| Doctor | `make doctor` | 0 only when all required checks pass |
| Upgrade dry lifecycle | `make -n upgrade` | expected commands, no mutation |
| Herdr status | `herdr status server --json` | top-level status is `running` or `not_running` |
| CI Bats | `./scripts/run_unit_test.sh` with matrix env | GitHub only; exit 0 |
| Plan evidence search | `rg -n 'Positive|Adversarial|Verify' plans/005-make-runtime-health-and-verification-truthful.md` | completion oracles listed |
| Changed-file audit | `git diff --name-only fa76b4a..11d27f5` | only Plan 005 scope and accepted review fixes |
| External plan gate | `uv run python scripts/validate_plan_quality.py /Users/mryfmo/Workspace/dotfiles/plans/005-make-runtime-health-and-verification-truthful.md --acceptance /Users/mryfmo/Workspace/dotfiles/docs/verification/acceptance/005.md --require-acceptance-quality` | exit 0 from the available external gate |

## Scope

**In scope**:

- `.gitignore`
- `home/dot_local/bin/common/executable_agent-fanout`
- `scripts/check-tools.sh`, `scripts/check-agent-runtime.py`, `scripts/upgrade-tools.sh`, `Makefile`
- Their focused tests under `tests/unit/` and `tests/install/common/`
- `home/dot_local/bin/common/executable_herdr-agents` and `tests/unit/test_herdr_agents.py`
- `tests/files/macos.bats`, `tests/files/ubuntu.bats`, and
  `tests/install/ubuntu/server/empty.bats` (rename when adding assertions)
- `home/dot_ccstatusline/settings.json`, `home/dot_agents/agent-config.yaml`, the
  source template/generator that owns generated statusline output, and generated
  outputs produced by `scripts/update-agent-assets.sh`
- `.github/workflows/test.yaml`
- Shell files with actual non-suppressed ShellCheck findings.

**Out of scope**:

- A centralized logging service or encryption-at-rest system.
- Changing agent prompts, model choices, or orchestration protocol.
- Replacing Herdr, Yazi, Zed, ccstatusline, or ccusage.
- Adding retries that turn persistent required failures into success.
- Raising an arbitrary global code-coverage percentage.

## Steps

## Phase 1 — Protect agent run artifacts

### A001 — Add privacy and ignore regression tests

- [x] Add a Python or shell unit test following existing extensionless-helper
      tests that runs agent-fanout in a temporary git worktree/HOME with fake agents.
- [x] Assert the run directory mode is `0700` and prompt/stdout/stderr files are
      not group/other readable.
- [x] Assert `git status --short --ignored` classifies `.agents/runs/**` ignored.

**Verify adversarial**: with the current helper and gitignore, at least the ignore
assertion must fail before production changes.

### A002 — Ignore runtime runs

- [x] Add `.agents/runs/` to `.gitignore` without broadening to all `.agents/`.
- [x] Preserve worklog and orchestration visibility rules already in the repo.

### A003 — Set restrictive creation modes

- [x] Set `umask 077` before creating the run directory/files.
- [x] Ensure the parent `.agents/runs` and per-run directory are private.
- [x] Do not log prompt content to terminal beyond current explicitly requested output.

### A004 — Verify no secret-like artifact is tracked

- [x] Run the new mode/ignore test.
- [x] Run `git ls-files '.agents/runs/**'` and require no output.
- [x] Run `make validate-agent-assets`.

## Phase 2 — Make doctor and upgrade exit codes truthful

### A005 — Define required versus optional checks once

- [x] Encode this exact required doctor set in existing script control flow:
      `git`, `chezmoi`, `mise`, `uv`, `gh`, their version commands, `chezmoi
      doctor`, `mise doctor`, `mise ls --current`, and
      `scripts/check-agent-runtime.py` when its source/deployed roots exist.
- [x] Treat Homebrew as required on Darwin and not applicable on Linux.
- [x] Treat private chezmoi source/config and installed GitHub CLI extensions as
      optional warnings because public lifecycle does not require them.
- [x] Do not create a new config format.

### A006 — Add failing doctor tests

- [x] Fake one missing required tool and assert nonzero.
- [x] Fake one missing optional tool and assert zero with warning.
- [x] Fake agent runtime drift and assert nonzero.
- [x] Healthy environment asserts zero.

### A007 — Accumulate doctor failures

- [x] Make `check-tools.sh` accumulate required failures and return nonzero at end.
- [x] Have `make doctor` invoke existing `scripts/check-agent-runtime.py` after
      tool checks, preserving the first/nonzero aggregate result.
- [x] Print one final required/optional summary.

### A008 — Add failing upgrade tests

- [x] Cover failures in these required executed phases: Homebrew on Darwin, mise
      self, mise inventory/tool install/tool upgrade, Codex/Claude CLI upgrade,
      agent asset regeneration, uv tool upgrade, and apt when `--system` requests it.
- [x] Cover GitHub extension upgrade as the one optional phase.
- [x] Assert final status and summary, not only log text.

### A009 — Return partial failure

- [x] Continue independent updates to maximize useful work.
- [x] Track required failures and return nonzero after the summary.
- [x] Keep only GitHub extension upgrade failure as warning-only.
- [x] Remove `|| true` only where it masks a required failure.

### A010 — Verify lifecycle truth

- [x] Run focused Python tests, `make unit-test`, and `make doctor` in healthy state.
- [x] Run isolated fake-tool failure cases and record exact nonzero codes.
- [x] Do not run a real upgrade as part of tests.

## Phase 3 — Restart Yazi when the files pane is stale

### A011 — Add files-pane liveness fixtures

- [x] Extend `tests/unit/test_herdr_agents.py` with: live Yazi, labeled empty pane,
      labeled pane running a different process, and missing pane.
- [x] Assert live Yazi is untouched.
- [x] Assert stale labeled pane is reused and starts Yazi without an extra split.

### A012 — Use Herdr's foreground-process data

- [x] Inspect the actual `herdr pane list --json` field exposed by the pinned
      Herdr version from Plan 004.
- [x] Replace label-only success with label plus live Yazi process check.
- [x] Keep one helper; do not duplicate JSON parsing across callers.

### A013 — Repair in place

- [x] If the labeled files pane exists but Yazi is absent, run Yazi in that pane.
- [x] Split a new pane only when no files pane exists.
- [x] Preserve current Claude/Codex pane placement and focus behavior.

### A014 — Verify Herdr layout regressions

- [x] Run all `test_herdr_agents.py` tests.
- [x] Confirm stale repair produces one Yazi run and zero split calls.
- [x] Confirm live Yazi produces neither run nor split.

## Phase 4 — Reload Herdr config after managed updates

### A015 — Add running/not-running Make behavior tests

- [x] Extend `tests/install/common/lifecycle.bats` with fake `chezmoi`, asset
      updater, and `herdr` commands under a temporary HOME/PATH.
- [x] Running server: reload called once after apply/assets succeed.
- [x] JSON status `not_running`: update succeeds and prints a concise skip message.
- [x] Status command failure, malformed or multiple JSON documents,
      non-string/unknown/missing status, and reload failure each make update return nonzero.

### A016 — Add the reload recipe directly to `Makefile`

- [x] After `scripts/update-agent-assets.sh`, add one recipe block; do not create
      a new helper file.
- [x] If `herdr` is absent, print one skip line and succeed.
- [x] Otherwise capture `herdr status server --json`; command failure returns nonzero.
- [x] Use `jq -er` to require a top-level object whose `status` is a string;
      malformed, multiple-document, missing, and non-string results fail closed.
- [x] For exact value `running`, call `herdr server reload-config` and propagate
      its status. For exact value `not_running`, print skip and succeed. Any other or
      missing value is an error.
- [x] Do not start Herdr automatically.

### A017 — Wire `make update`

- [x] Invoke the helper after `scripts/update-agent-assets.sh`.
- [x] Keep `make apply` as the existing alias.
- [x] Document automatic reload and the manual recovery command.

### A018 — Verify failure propagation

- [x] Confirm apply failure prevents reload.
- [x] Confirm asset generation failure prevents reload.
- [x] Confirm reload failure makes `make update` fail.

## Phase 5 — Replace placeholder platform tests with assertions

### A019 — Delete the empty-test illusion

- [x] Remove `tests/install/ubuntu/server/empty.bats` or rename it to a behavior it
      actually verifies.
- [x] Do not leave empty test files to preserve test count.

### A020 — Define minimal platform manifests

- [x] macOS client: assert representative managed shell config, Ghostty config,
      Yazi config, executable helper mode, and absent server-only file.
- [x] Ubuntu client: assert the equivalent Linux client set.
- [x] Ubuntu server: assert server shell config and absent GUI/client-only files.
- [x] Use chezmoi render/apply in isolated HOME, not the developer HOME.

### A021 — Implement file assertions

- [x] Add existence, target/content, and executable-mode assertions where relevant.
- [x] Add at least one negative assertion per platform/role.
- [x] Do not duplicate the full repository manifest; choose critical boundaries.

### A022 — Add rerun/idempotency assertion

- [x] Apply twice in isolated HOME.
- [x] Confirm the second apply yields no unexpected diff and sentinels survive.

### A023 — Obtain CI-only Bats evidence

- [x] Confirm every matrix cell executes nonzero test count.
- [x] In each isolated Bats fixture, remove one required target, invoke the same
      assertion helper under `run`, and assert its status is nonzero. This is the
      adversarial oracle; do not push a deliberately broken branch.

## Phase 6 — Remove rolling npm from the statusline hot path

### A024 — Add generated-config tests

- [x] Assert ccusage and ccstatusline commands contain no `npx`, `@latest`, or
      network installer flag.
- [x] Assert commands resolve through mise shims/PATH configured by agent assets.

### A025 — Add tools to the locked mise source

- [x] Declare exact/locked ccusage and ccstatusline package versions in the same
      `home/dot_mise/config.toml` policy established by Plan 004.
- [x] Regenerate the mise lockfile through mise.
- [x] Do not add a second npm global-install path.

### A026 — Change the source of generated commands

- [x] Replace statusline command paths with direct `ccusage`/`ccstatusline` binaries.
- [x] Edit `home/dot_agents/agent-config.yaml` or its authoritative template, not
      generated outputs by hand.
- [x] Run `scripts/update-agent-assets.sh` once.

### A027 — Verify offline and latency behavior

- [x] With network disabled and tools preinstalled, invoke each command and require
      exit 0 within its configured timeout.
- [x] Confirm a missing binary fails immediately with a clear error, not a 50-second wait.
- [x] Run agent asset generation and validation twice; second generation has no diff.

## Phase 7 — Enforce ShellCheck in CI

### A028 — Establish a clean ShellCheck baseline

- [x] Run the tracked-shell command from Commands you will need.
- [x] Fix real quoting/path findings, including HOME expansions in
      `install/ubuntu/server/ssh_server.sh`.
- [x] Add narrowly scoped `# shellcheck disable=` only for proven intentional
      generator literals; include the rule ID and reason.

### A029 — Add the CI tool

- [x] Install ShellCheck on Ubuntu and macOS using the existing package steps.
- [x] Do not install through another package manager or `latest` network command.

### A030 — Add one CI ShellCheck step

- [x] Use the same tracked-file selection command locally and in CI.
- [x] Run after checkout/tool install and before Bats.
- [x] Fail the job on any non-suppressed finding.

### A031 — Prove the oracle is non-empty

- [x] Temporarily add an unquoted variable in an in-scope shell file.
- [x] Confirm the CI/local ShellCheck step fails with the expected rule.
- [x] Revert the deliberate defect and confirm the step passes.

## Test plan

- Agent artifacts: ignored, private modes, no tracked run files.
- Doctor: healthy, missing required, missing optional, runtime drift.
- Upgrade: required partial failure, optional failure, continued independent work.
- Herdr: live/stale/missing files pane and unchanged agent layout.
- Reload: `running`, `not_running`, malformed/multiple JSON, apply failure,
  asset failure, status failure, and reload failure.
- Platform manifests: positive and negative files plus second-apply idempotency.
- Statusline: generated direct commands, offline invocation, missing binary fast fail.
- ShellCheck: clean baseline and one deliberate-failure proof.
- Regression: `make unit-test`, asset generation/validation, shfmt, CI Bats matrix.

**Verify**

- Positive: private artifacts, truthful health exits, and independent upgrade phases pass their focused tests.
- Adversarial: symlink artifacts, missing required tools, and failed upgrade phases return nonzero without hiding independent work.

**Verify**

- Positive: a live Yazi pane is reused and a stale files pane is repaired in place.
- Adversarial: duplicate panes, pane-inspection failures, and failed restarts never report a healthy layout.

**Verify**

- Positive: macOS client plus Ubuntu client/server public bootstrap and manifest matrices pass from the exact PR and merge heads.
- Adversarial: missing fixture paths, role leakage, target drift, and a second non-idempotent apply fail the matrix.

**Verify**

- Positive: exact locked statusline tools execute offline and tracked shell files pass ShellCheck.
- Adversarial: wrong versions, shim routing, network access, and deliberate shell defects fail their respective gates.

## Done criteria

- [x] `.agents/runs/**` is ignored and created with private permissions.
- [x] `make doctor` is nonzero for any required tool/runtime failure.
- [x] `make upgrade` is nonzero after any required partial failure.
- [x] A labeled stale files pane restarts Yazi in place.
- [x] `make update` reloads a running Herdr server and propagates reload failure.
- [x] No placeholder/empty Bats file remains; each platform matrix cell asserts behavior.
- [x] Statusline commands contain no `npx` or `@latest` and work offline when installed.
- [x] ShellCheck runs as a required CI step and the tracked shell baseline is clean.
- [x] All local commands and required GitHub checks pass.
- [x] All generated asset diffs originate from the generator and a second run is clean.
- [x] `plans/README.md` status is updated after merge.
- [x] Before implementation and again before DONE, repeat this self-audit and
      attach its result to the PR/CI acceptance evidence.

## STOP conditions

- Herdr's pinned JSON output exposes no reliable foreground-process/liveness field.
- `make update` cannot distinguish “server stopped” from a permission/protocol error.
- Required/optional tool classification conflicts with documented core workflows.
- Agent asset generation changes unrelated settings or secrets.
- A platform file assertion requires applying to the real HOME.
- Plan 004 did not leave a working committed mise lockfile/policy that Plan 005
  can extend with ccusage and ccstatusline.

## Maintenance notes

- Return runtime status according to the required/optional classification below.
- Declare generated agent commands once in the authoritative source and regenerate.
- Add new shell files to the same ShellCheck selector; update Herdr process fixtures
  deliberately when its schema changes.

## 安全回帰

- Sensitive prompts and logs are private and excluded from version control.
- Required failures cannot be downgraded to warnings or zero exit.
- Self-healing reuses existing panes and never duplicates a live Yazi process.
- Generated files are never edited independently of their source.
- Verification contains at least one demonstrated failing adversarial case per phase.
- Platform acquisition boundaries remain explicit: AWS CLI uses Homebrew on macOS and the signed official AWS v2 installer on Linux, never mise.
