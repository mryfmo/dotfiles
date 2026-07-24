# Plan 003: Make bootstrap safe, dependency-correct, and testable without secrets

> **Executor instructions**: Complete phases in order. Each atomic task changes
> one behavior and immediately adds or runs its oracle. Do not preserve `--force`
> merely for backward compatibility; preserve user data instead. Do not run Bats
> locally. STOP rather than inventing answers when a supported clean image lacks
> an assumed command.
>
> **Drift check**: `git diff --stat e7c2808..HEAD -- setup.sh README.md install/ubuntu/common/dependencies.sh tests/install/common/setup.bats tests/install/ubuntu/common .github/workflows/remote.yaml home/.chezmoi.yaml.tmpl home/symlink_dot_bashrc.tmpl`

## Status

- **Completion**: DONE — PR #69, merge `69e2338489e22d5279ca3fdf6917f0cbe5950400`; exact-head and post-merge CI passed
- **Priority**: P1
- **Effort**: L
- **Risk**: MED — bootstrap ordering and overwrite semantics affect clean and existing machines
- **Depends on**: Plans 001 and 002; expanded server CI must be safe and later broad changes require a real review gate
- **Category**: correctness, data-loss prevention, CI, DX
- **Planned at**: commit `e7c2808`, 2026-07-11

## Plan quality self-audit

- [x] Compared with the early-plan standard; L scope has measured state, 18
      atomic tasks, explicit commands, and phase-specific oracles.
- [x] Required Steps, Commands, Scope, Test plan, Maintenance, STOP, and 安全回帰
      sections are present.
- [x] Current-state `file:line` evidence was measured at `e7c2808`.
- [x] F03, F08, F09, F11, and F14 are mapped to atomic tasks.
- [x] Clean-machine and existing-machine paths have separate tests.
- [x] Every destructive edge has a sentinel-file adversarial oracle.
- [x] The plan reuses shell, chezmoi, apt/dpkg, and GitHub Actions only.
- [x] DONE requires a repeated audit plus review/CI acceptance evidence.

## Why this matters

The documented public bootstrap is not actually exercised against PR code when
secrets are absent. On minimal Ubuntu it may call curl before installing it,
package detection uses command names instead of Debian package state, and the
apply stage overwrites local modifications without a preview or recovery copy.
An invalid Linux role can also be persisted and break all later renders.

The required invariant is: a supported clean machine can bootstrap from the PR
checkout without private secrets, while an existing machine with local drift is
shown a diff and left byte-identical instead of being force-overwritten.

## Current state

- `install/ubuntu/common/dependencies.sh:35-38` updates APT only while installing
  missing sudo; an existing sudo skips index refresh.
- `install/ubuntu/common/dependencies.sh:50-53` calls `command -v` with package
  names including `iproute2` and `iputils-ping`.
- `README.md:39-50` advertises both curl and wget snippets.
- `setup.sh:153-176` makes Linux initialization a no-op, then unconditionally
  calls curl to install chezmoi.
- `setup.sh:187-217` uses `--force` for init, update, and apply.
- `.github/workflows/remote.yaml:32-37` checks the URL of `main/setup.sh`.
- `.github/workflows/remote.yaml:46-65` runs the full bootstrap only when private
  secrets exist and again fetches `main/setup.sh`.
- `home/.chezmoi.yaml.tmpl:9-15` accepts an existing or prompted system value
  without validating `client|server`.
- `home/symlink_dot_bashrc.tmpl:1-6` is one downstream template that fails only
  after an invalid role has already been saved.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Python tests | `make unit-test` | exit 0 |
| Shell syntax | `bash -n setup.sh install/ubuntu/common/dependencies.sh` | exit 0 |
| Shell format | `shfmt -i 4 -sr -d setup.sh install/ubuntu/common/dependencies.sh` | exit 0 |
| Shell static analysis | `shellcheck -x setup.sh install/ubuntu/common/dependencies.sh` | exit 0 |
| Template render | `CI=true chezmoi execute-template < home/.chezmoi.yaml.tmpl` | valid YAML for supported role |
| CI Bats | `OS=ubuntu-latest SYSTEM=<client|server> ./scripts/run_unit_test.sh` | GitHub only; exit 0 |

## Scope

**In scope**:

- `setup.sh`, `README.md`
- `install/ubuntu/common/dependencies.sh`
- `tests/install/ubuntu/common/dependencies.bats`
- `tests/install/ubuntu/common/dependencies_unit.bats`
- `tests/install/common/setup.bats`
- `.github/workflows/remote.yaml`
- `home/.chezmoi.yaml.tmpl`
- A focused template test under `tests/install/common/` if none can express role validation

**Out of scope**:

- Private dotfiles contents or private deploy-key behavior.
- Version/checksum pinning; Plan 004 owns it.
- A new installer framework, container orchestrator, or rollback daemon.
- Removing macOS/Ubuntu platform support.

## Steps

## Phase 1 — Correct Ubuntu dependency installation

### A001 — Write package-state tests

- [ ] Replace command-name mocks in the dependency unit test with a mock of
      `dpkg-query -W -f=${Status}`.
- [ ] Cover installed, absent, and partially installed package states.
- [ ] Assert `iproute2` and `iputils-ping` are not repeatedly classified missing
      when dpkg reports `install ok installed`.

**Verify adversarial**: before production changes, CI Bats must fail because the
current script never calls `dpkg-query`.

### A002 — Use Debian package state as the single oracle

- [ ] In `install_apt_packages`, classify a package installed only when
      `dpkg-query` returns the exact installed status.
- [ ] Keep the existing `PACKAGES` array and install batching.
- [ ] Do not introduce a package-to-command mapping.

**Verify**: mock tests show only absent/partial packages in the apt install arguments.

### A003 — Refresh APT before any non-empty install

- [ ] Make `run_apt_get update` occur once after determining at least one package
      is missing and before `install -y`.
- [ ] Preserve proxy environment forwarding.
- [ ] Avoid a second update when sudo itself must first be installed as root.

**Verify**: the mocked call log is ordered `update` then `install`; an empty
missing set produces neither call.

### A004 — Close the dependency phase

- [ ] Run syntax, format, ShellCheck, and Python tests.
- [ ] Obtain Ubuntu client/server Bats proof in CI.

## Phase 2 — Support both documented fetchers

### A005 — Add fetcher-selection regression cases

- [ ] Extend `tests/install/common/setup.bats` with isolated PATH cases:
      curl-only, wget-only, neither, and both.
- [ ] Each fake fetcher must log which URL it received.
- [ ] Neither-present must exit nonzero with one deterministic error.

### A006 — Add one minimal stdout fetch function

- [ ] Add one function in `setup.sh` that accepts exactly one URL.
- [ ] Prefer curl when available; otherwise use wget; otherwise return nonzero.
- [ ] Route every bootstrap text download through it, including Homebrew and
      chezmoi installation paths until Plan 004 replaces remote execution.

**Verify**: `rg -n 'curl .*https?://|wget .*https?://' setup.sh` finds only the
fetch function implementation, documented comments, or explicitly justified
non-body requests.

### A007 — Prove wget-only Linux bootstrap

- [ ] Run the existing isolated setup test with fake wget and no curl.
- [ ] Assert the fake chezmoi reaches `init`, preview, and apply phases.
- [ ] Keep curl and wget README snippets accurate.

## Phase 3 — Replace forced overwrite with preview and recovery

### A008 — Characterize clean and locally modified target behavior

- [ ] Add isolated tests using fake chezmoi that log `init`, `status`, `diff`, and
      `apply` operations.
- [ ] Clean target: apply proceeds without an overwrite prompt.
- [ ] Target with a non-space first `chezmoi status` column: diff is printed,
      apply is not invoked, existing bytes/modes remain unchanged, and bootstrap
      returns nonzero.
- [ ] Failed status, diff, or apply returns nonzero. Status/diff failures occur
      before target mutation; an apply failure may retain target operations
      that chezmoi completed before reporting the error.

### A009 — Implement the shortest safe sequence

- [ ] Remove unconditional `--force` from the normal apply path.
- [ ] Run `chezmoi status --path-style absolute --exclude=scripts` before apply.
- [ ] Per chezmoi's documented status format, treat any line whose first column
      is not a space as local drift since the last write.
- [ ] When local drift exists, run `chezmoi diff`, print a message that no
      destination targets were changed, and return nonzero without invoking
      apply. Source-state or config changes made by init/update may remain.
- [ ] When no local drift exists, run `chezmoi diff` then `chezmoi apply` without
      `--force`.
- [ ] In non-interactive CI, allow apply only inside the isolated test HOME.
- [ ] Return nonzero on status, diff, or apply failure. Do not claim
      transaction/rollback semantics that chezmoi does not provide.

**Verify adversarial**: plant an unmanaged sentinel and a locally modified
managed target. Bootstrap returns nonzero, apply is never called, and both files
are byte-identical after the attempt.

### A010 — Document recovery

- [ ] Update README with `status -> preview -> apply -> verify` behavior.
- [ ] Document that local drift stops before destination-target mutation, while
      source-state or config changes made by init/update may remain; include
      exact commands for `chezmoi diff`, resolving/adding the local change, and
      rerunning setup.
- [ ] Remove statements claiming forced overwrite is expected behavior.

## Phase 4 — Test the PR's public bootstrap without secrets

### A011 — Check out the PR source

- [ ] Add `actions/checkout` to `remote.yaml`.
- [ ] Stop fetching `raw.githubusercontent.com/.../main/setup.sh` for PR
      correctness checks.
- [ ] Execute `${GITHUB_WORKSPACE}/setup.sh` or its file contents from checkout.

### A012 — Separate public and private bootstrap jobs

- [ ] Create a required public job/matrix for Ubuntu client, Ubuntu server, and
      macOS client that uses temporary HOME and no private secret.
- [ ] Keep private-dotfiles restoration in a separate optional secret-gated job.
- [ ] Public job must run for fork PRs and Dependabot.

### A013 — Add destructive sentinels to the public job

- [ ] Before bootstrap, create unrelated sentinels under `.local/bin`, `.ssh`,
      and one unmanaged home path.
- [ ] After bootstrap, compare hashes and modes.
- [ ] Assert the selected role and core managed files exist.

### A014 — Prove branch locality

- [ ] Add a temporary test-only marker in a PR run and confirm the workflow sees
      it from checkout; remove marker before final commit.
- [ ] Confirm workflow logs contain the PR HEAD SHA and not `main` content SHA.

## Phase 5 — Validate role before persistence

### A015 — Add accepted-role render tests

- [ ] Render config for Linux `client`, Linux `server`, and macOS default.
- [ ] Assert exact resulting `data.system` values.

### A016 — Add invalid-role tests

- [ ] Cover typo, empty, whitespace, and a previously persisted invalid value.
- [ ] Assert rendering fails immediately with `client or server` in the message.

### A017 — Validate at the input boundary

- [ ] Validate `$system` in `.chezmoi.yaml.tmpl` before emitting YAML.
- [ ] Accept only exact `client` and `server`; macOS still defaults to `client`.
- [ ] Do not scatter role checks into downstream templates.

### A018 — Run complete plan gates

- [ ] Run all local commands in Commands you will need except Bats.
- [ ] Push after authorization and require all public matrix cells to pass.
- [ ] Confirm no secret-gated job is required for the PR to be green.

## Test plan

- APT: installed/absent/partial packages, sudo present/absent, ordered update/install.
- Fetch: curl-only, wget-only, both, neither.
- Apply: clean, locally modified, failed status, failed diff, failed apply,
  unmanaged sentinel.
- Public CI: three supported platform/system pairs from PR checkout.
- Role: client, server, macOS default, typo, empty, persisted invalid value.

## Done criteria

- [ ] `dpkg-query`, not `command -v`, determines Debian package state.
- [ ] Every non-empty apt install is preceded by one successful update.
- [ ] wget-only documented bootstrap reaches chezmoi without curl.
- [ ] Normal bootstrap contains no unconditional `chezmoi apply --force`.
- [ ] Locally modified managed targets are previewed and left byte-identical.
- [ ] Public CI executes PR checkout code without secrets on all supported pairs.
- [ ] Invalid roles fail before config persistence or downstream rendering.
- [ ] Local syntax, format, ShellCheck, and Python tests pass.
- [ ] GitHub Bats and required checks pass.
- [ ] `plans/README.md` status is updated after merge.
- [ ] Before implementation and again before DONE, repeat this self-audit and
      attach its result to the PR/CI acceptance evidence.

## STOP conditions

- The installed chezmoi version's status first-column semantics differ from the
  official documented format; report the exact output before writing a parser.
- Public macOS CI cannot be isolated from the runner user's real HOME.
- A clean supported image requires a network credential for public bootstrap.
- Role validation requires duplicating the allowed set in more than the config
  input boundary and tests.
- Plan 001 is not merged before Ubuntu Server CI expansion.

## Maintenance notes

- Keep public bootstrap independent from private restoration.
- Test new Debian dependencies by package state, never executable name.
- Add future roles only through a deliberate allowlist and matrix design change.

## 安全回帰

- An unrelated file is never deleted or overwritten.
- Local drift and failures before apply return nonzero without target mutation.
- An apply failure returns nonzero and is documented as potentially retaining
  target operations completed before the failure; the operator must inspect
  `chezmoi status`/`diff`, resolve the error, and rerun.
- Fork PRs receive a meaningful required bootstrap result without secrets.
- Invalid trust-boundary input fails before state is written.
