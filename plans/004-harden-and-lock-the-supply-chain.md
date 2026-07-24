# Plan 004: Pin, verify, and continuously test every executable dependency source

> **Executor instructions**: Work by source class in the listed order. Never
> replace one mutable alias with another mutable alias. Record every resolved
> version, full commit SHA, and checksum source. If upstream supplies neither an
> immutable artifact nor an independently published checksum/signature, STOP for
> that dependency and report it; do not add `curl | sh` exceptions.
>
> **Drift check**: `git diff --stat e7c2808..HEAD -- setup.sh install home/dot_mise home/dot_config/sheldon home/.chezmoitemplates/chezmoiexternal.d .github/workflows flake.nix flake.lock docs/plans/nix-first-architecture.md tests`

## Status

- **Execution**: DONE — PR #70, merge `fa76b4a`
- **Priority**: P1
- **Effort**: L
- **Risk**: MED — incorrect platform artifact selection can break clean bootstrap
- **Depends on**: Plans 002 and 003; the review gate must be real and secret-free PR bootstrap must exist
- **Category**: security, dependencies, reproducibility, CI
- **Planned at**: commit `e7c2808`, 2026-07-11

## Plan quality self-audit

- [x] Compared with the early-plan standard; L cross-platform scope has explicit
      source classes, commands, STOP conditions, and per-phase oracles.
- [x] Required Steps, Commands, Scope, Test plan, Maintenance, STOP, and 安全回帰
      sections are present.
- [x] Current-state `file:line` evidence was measured at `e7c2808`.
- [x] F04, F05, F06, F10, and F18 have exclusive task mappings.
- [x] Pinning and integrity verification are separate, testable conditions.
- [x] Four supported OS/architecture combinations are explicit.
- [x] No custom package service or speculative dependency updater is introduced.
- [x] DONE requires a repeated audit plus review/CI acceptance evidence.

## Why this matters

The repository downloads and executes mutable remote code, consumes GitHub
Actions by movable tag, installs most runtime tools as `latest`, resolves shell
plugins without immutable revisions, and evaluates font release APIs during
normal chezmoi operations. A clean machine is therefore neither reproducible nor
fully protected from upstream compromise or availability failures.

Use native controls first: immutable GitHub SHAs, upstream checksum/signature
files, mise lockfiles, Sheldon lock/commit fields, chezmoi external checksums,
and Nix flake locks. GitHub states that a full commit SHA is the only immutable
Action reference: https://docs.github.com/en/actions/reference/security/secure-use

## Current state

- `setup.sh:140-141` executes Homebrew's mutable `HEAD/install.sh`.
- `setup.sh:176` executes `get.chezmoi.io` without integrity verification.
- `install/common/mise.sh:21-24` pipes a versioned but unverified install script.
- `install/common/sheldon.sh:22-23` pipes a remote crate installer.
- `install/ubuntu/server/starship.sh:26-30` uses a mutable installer/latest path.
- `.github/workflows/*.y*ml` uses tag references such as `actions/checkout@v7`,
  `setup-uv@v7`, `mise-action@v4`, and `ssh-agent@v0.10.0`.
- `.github/workflows/ubuntu.yaml:28-31` grants unused Pages and OIDC writes.
- `home/dot_mise/config.toml:2-38` contains 30 `lts`/`latest` requests
  tool requests; no mise lockfile is committed.
- `home/dot_config/sheldon/plugin_sources/*.toml` contains Git sources without a
  consistent immutable commit or committed Sheldon lock.
- `home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl:7-20` calls
  `gitHubLatestReleaseAssetURL` during normal online rendering and specifies no
  archive checksum.
- `flake.nix:5-12` selects NixOS/Home Manager/nix-darwin 25.05; no Nix workflow
  evaluates the flake.

## Authoritative references

- GitHub Action SHA and least privilege:
  https://docs.github.com/en/actions/reference/security/secure-use
- mise lockfiles:
  https://mise.jdx.dev/configuration/settings.html
- Sheldon lock/update and commit/tag configuration:
  https://sheldon.cli.rs/Command-line-interface.html and
  https://sheldon.cli.rs/Configuration.html
- chezmoi external validation/checksums:
  https://www.chezmoi.io/user-guide/include-files-from-elsewhere/ and
  https://www.chezmoi.io/reference/special-files/chezmoiexternal-format/
- Current NixOS release/support statement:
  https://nixos.org/blog/announcements/2026/nixos-2605/

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Mutable Action scan | `rg -nP 'uses:\s+(?!\./)(?!docker://)\S+@(?![0-9a-f]{40}(?:\s*#|$))\S+' .github/workflows` | no matches |
| Rolling mise scan | `rg -n '= "(latest|lts)"|version = "latest"' home/dot_mise/config.toml` | no matches after lock policy |
| Remote execution scan | `rg -n 'curl.*\|.*(sh|bash)|bash -c.*curl|sh -c.*curl' setup.sh install` | no unverified execution path |
| Python tests | `make unit-test` | exit 0 |
| Asset validation | `make validate-agent-assets` | exit 0 |
| Shell static checks | `git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x` | exit 0 |
| Nix lock/check | `nix flake lock --update-input <name>` then `nix flake check --no-build` | exit 0; lock committed |
| CI-only bootstrap | public matrix from Plan 003 | all cells pass |

## Scope

**In scope**:

- Download/install paths in `setup.sh` and `install/**/*.sh`.
- Tests directly covering those installers.
- `tests/unit/test_workflow_security.py` (new, Python stdlib only) for immutable
  Action refs and exact top-level permission maps.
- All external `uses:` entries and workflow `permissions`.
- `home/dot_mise/config.toml` plus the mise lockfile at the path required by the
  installed mise version.
- Sheldon plugin source files and its native lockfile if supported by the
  deployed configuration layout.
- chezmoi external templates and checksum metadata.
- `flake.nix`, `flake.lock`, Nix migration docs, and one Nix CI job added to the
  existing `.github/workflows/test.yaml`; do not create a seventh workflow.

**Out of scope**:

- Building a private artifact mirror, package registry, or updater service.
- Upgrading application behavior unrelated to compatibility with pinned versions.
- Pinning operating-system APT/Homebrew repository snapshots.
- Promoting the opt-in Nix path to the default dotfiles implementation.

## Steps

## Phase 1 — Verify executable downloads

### A001 — Inventory every executable network source

- [ ] Produce a table in the PR description/evidence with caller, URL, version,
      supported platforms, upstream checksum/signature URL, and current test.
- [ ] Include Homebrew, chezmoi, mise, Sheldon, Starship, and any additional
      matches from the remote execution scan.
- [ ] Classify non-executable archives separately.

**Verify**: every match from the scan appears exactly once in the inventory.

### A002 — Add checksum-failure test helpers

- [ ] Extend existing installer Bats tests with fake download bodies and known
      SHA-256 values.
- [ ] Add a corrupted-body case that must fail before shell/binary execution.
- [ ] Add a missing-checksum case that must fail closed.

**Verify adversarial**: fake executable writes a marker when run; corrupted
download returns nonzero and marker does not exist.

### A003 — Pin and verify chezmoi

- [ ] Select one explicit chezmoi release that has upstream checksums for every
      supported bootstrap platform.
- [ ] Download the platform archive and upstream checksum file, verify SHA-256,
      then install only the verified binary at the existing destination.

**Verify positive/adversarial**: correct fixture installs; one-byte corruption
returns nonzero before the fake binary marker is written.

### A004 — Pin and verify mise

- [ ] Keep one explicit mise release and select its platform artifact directly.
- [ ] Verify against the upstream release checksum before installing to
      `${HOME}/.local/bin/mise`; stop piping `install.sh` to a shell.

**Verify positive/adversarial**: cover a correct checksum and a correct artifact
paired with another platform's checksum.

### A005 — Pin and verify Sheldon

- [ ] Pin Sheldon `0.8.5` from crates.io; reject its mutable GitHub release
      binaries because they publish no independent checksum/signature or
      attestation, as recorded in `.orchestration/reports/plan-004-stop.md`.
- [ ] Use crates.io's registry checksum and the crate's packaged `Cargo.lock` to
      build from source with locked dependencies on supported platforms.
- [ ] Prefer the existing mise cargo backend only if official behavior proves it
      invokes the equivalent of `cargo install --locked`; otherwise use the
      shortest existing shared-installer path that explicitly does so.
- [ ] Remove the mutable `crate.sh | bash` execution path and preserve the
      existing install/uninstall command boundary.

**Verify positive/adversarial**: checksum mismatch produces no Sheldon binary.

### A006 — Pin and verify Starship

- [ ] Select one explicit Starship release and platform artifact.
- [ ] Verify its upstream checksum before replacing `${BIN_DIR}/starship`.
- [ ] Preserve Plan 001's file-only uninstall boundary.

**Verify positive/adversarial**: existing Starship and sibling sentinel survive
a failed checksum; verified install replaces only Starship.

### A007 — Pin the Homebrew installer source

- [ ] Review one Homebrew/install commit and record its full commit SHA.
- [ ] Obtain `install.sh` from a local clone checked out at that verified commit,
      compute SHA-256 from the checked-out file, and store it beside the pinned
      raw commit URL. Do not derive the expected digest from bootstrap's download.
- [ ] Verify downloaded bytes before executing with `NONINTERACTIVE=1`.

**Verify adversarial**: a fake raw response with the right URL but altered bytes
returns nonzero before the Homebrew installer marker runs.

### A008 — Remove unverified fallbacks

- [ ] Remove or reject any fallback that executes content after download failure,
      checksum absence, checksum mismatch, or unknown platform.
- [ ] Do not silently switch back to a mutable installer.

### A009 — Close installer verification

- [ ] Run installer unit tests, syntax, ShellCheck, and the Plan 003 public matrix.
- [ ] Confirm every supported platform selects exactly one expected artifact.

## Phase 2 — Make GitHub Actions immutable and least-privileged

### A010 — Enumerate all external Actions

- [ ] Parse every workflow `uses:` entry.
- [ ] Exclude local `./` Actions and Docker image references only.
- [ ] Record current tag and upstream repository.

### A011 — Pin `actions/checkout`

- [ ] Resolve the current reviewed tag in `actions/checkout`, peel it to its
      upstream 40-character commit SHA, and replace every checkout reference.
- [ ] Retain the readable version tag as a trailing YAML comment.

**Verify**: all checkout refs use the same 40-hex SHA; temporarily restoring one
tag makes the immutable-ref scan fail.

### A012 — Pin `astral-sh/setup-uv`

- [ ] Resolve, verify upstream ownership, and replace every setup-uv tag with its
      40-character commit SHA plus version comment.

**Verify**: no `astral-sh/setup-uv@v` match remains.

### A013 — Pin `jdx/mise-action`

- [ ] Resolve, verify upstream ownership, and replace every mise-action tag with
      its 40-character commit SHA plus version comment.

**Verify**: no `jdx/mise-action@v` match remains.

### A014 — Pin `webfactory/ssh-agent`

- [ ] Resolve, verify upstream ownership, and replace every ssh-agent tag with
      its 40-character commit SHA plus version comment.

**Verify**: no `webfactory/ssh-agent@v` match remains.

### A015 — Pin `benchmark-action/github-action-benchmark`

- [ ] Resolve, verify upstream ownership, and replace its tag with a 40-character
      commit SHA plus version comment.

**Verify**: no benchmark Action tag match remains.

### A016 — Pin `codecov/codecov-action`

- [ ] Resolve, verify upstream ownership, and replace its tag with a 40-character
      commit SHA plus version comment.

**Verify**: no Codecov Action tag match remains.

### A017 — Minimize workflow permissions

- [ ] Add explicit top-level permissions to all six workflows.
- [ ] Encode this exact allowed map in `tests/unit/test_workflow_security.py`:
      `docs.yml -> {contents: write}`; `agent-assets.yml`, `macos.yaml`,
      `remote.yaml`, `test.yaml`, and `ubuntu.yaml -> {contents: read}`.
- [ ] Reject missing permissions, extra permission keys, job-level overrides, and
      values outside the exact map. The macOS benchmark uses its separate PAT;
      it does not require `GITHUB_TOKEN` write permission.
- [ ] Remove Ubuntu `pages: write` and `id-token: write`.
- [ ] Parse only the repository's top-level two-space permission block with
      Python stdlib; do not add a YAML dependency for this fixed policy.

**Verify Positive**: `uv run python -m unittest tests.unit.test_workflow_security -v`
passes with the exact six-file map.

**Verify Adversarial**: temporarily change only Ubuntu to `contents: write`; the
focused test fails naming `ubuntu.yaml` and the expected/read versus actual/write
values. Revert the mutation and rerun to green.

### A018 — Add automated update ownership

- [ ] Configure existing Dependabot support for `github-actions` if absent.
- [ ] Do not add a second bot or custom updater.
- [ ] Require the same CI matrix for SHA update PRs.

### A019 — Verify Action hardening

- [ ] Run workflow syntax validation available in the repo/CI.
- [ ] Run the immutable-ref scan and inspect effective permissions in job logs.
- [ ] Require the scan to reject any external `uses:` ref not matching
      `@[0-9a-f]{40}` before an optional trailing version comment.
- [ ] Run `uv run python -m unittest tests.unit.test_workflow_security -v` and
      require both immutable-ref and permission-map cases to pass.

## Phase 3 — Lock mise and Sheldon runtime inputs

### A020 — Define the version policy in config comments/docs

- [ ] Fixed/locked: all tools required by bootstrap, tests, agents, and statusline.
- [ ] Rolling updates occur only through `make upgrade` plus reviewed lock diff.
- [ ] Do not retain `latest` merely because a lockfile later resolves it unless
      mise documents that exact combination as reproducible.

### A021 — Generate and commit the mise lockfile

- [ ] Use the installed mise version's documented lockfile support.
- [ ] Include all supported platforms that mise can lock.
- [ ] Confirm two clean resolutions without network metadata changes produce an
      identical lockfile.

**Verify adversarial**: temporarily restore one `latest` entry; the rolling mise
scan fails. Revert it and require an identical second lock generation.

### A022 — Pin Sheldon sources natively

- [ ] Use Sheldon commit fields and/or its native lockfile for every Git source.
- [ ] Keep explicit update via `sheldon lock --update` or the documented command.
- [ ] Assert a second lock generation is byte-identical.

**Verify adversarial**: temporarily remove one plugin commit/lock entry; the
source-to-lock completeness check fails. Revert it.

### A023 — Test locked installs

- [ ] Update installer tests to assert locked resolution is invoked.
- [ ] Public bootstrap must fail when a required locked artifact is unavailable,
      not silently install another version.

## Phase 4 — Remove live API dependence from chezmoi externals

### A024 — Add offline-render regression tests

- [ ] Render externals with network/DNS unavailable and no special offline flag.
- [ ] Assert template evaluation succeeds from fixed metadata.
- [ ] Assert font URLs and checksums are deterministic.

### A025 — Replace latest-release template calls

- [ ] Remove `gitHubLatestReleaseAssetURL` from normal render paths.
- [ ] Use the already declared fixed Nerd Fonts release version for both URLs.
- [ ] Store SHA-256 checksums in the external entries using chezmoi's native
      checksum field.

### A026 — Separate update discovery from normal operation

- [ ] If automatic discovery is retained, place it only in explicit maintenance
      tooling such as `make upgrade`, never in template evaluation.
- [ ] A discovery failure must leave existing pinned metadata unchanged.

### A027 — Verify archive integrity failure

- [ ] Provide a wrong checksum in an isolated fixture.
- [ ] Confirm chezmoi rejects it before extraction and does not alter target fonts.

### A028 — Close external availability work

- [ ] Run offline render, checksum failure, `chezmoi diff`, and public bootstrap.

## Phase 5 — Update and evaluate the opt-in Nix path

### A029 — Confirm current supported release branches

- [ ] From official NixOS, Home Manager, and nix-darwin sources, record the
      supported compatible release branches as of execution date.
- [ ] Use NixOS 26.05 unless upstream compatibility evidence requires another
      currently supported branch; STOP on incompatibility rather than mixing eras.

### A030 — Update inputs and lock

- [ ] Change all three input branches as one atomic compatibility unit.
- [ ] Regenerate `flake.lock` with Nix, not manual JSON edits.
- [ ] Review the lock diff for expected upstream owners and revisions.

**Verify adversarial**: temporarily restore one `25.05` input; the release-policy
scan must fail before evaluation. Revert it.

### A031 — Evaluate every declared output

- [ ] Evaluate Linux and Darwin home configurations.
- [ ] Evaluate the Darwin system configuration on a compatible runner.
- [ ] Run formatter/check output evaluation without activating the configuration.

### A032 — Add Nix CI

- [ ] In existing `.github/workflows/test.yaml`, extend the changes job with a
      `should_nix` output true only for `flake.nix`, `flake.lock`, or `nix/**`.
- [ ] Add a secret-free `nix` job with `ubuntu-latest` and `macos-14` matrix,
      gated by `should_nix`; do not create a new workflow file.
- [ ] Cache only immutable Nix store paths; do not require a private cache secret.
- [ ] Require evaluation on Linux and macOS.

**Verify Adversarial**: a docs-only diff reports `should_nix=false`; a temporary
`nix/**` fixture diff reports `should_nix=true` and schedules both matrix cells.

### A033 — Update Nix documentation

- [ ] Replace 25.05 commands with the selected supported release.
- [ ] Document evaluation/canary commands and keep Nix opt-in.

## Test plan

- Downloads: correct checksum, corrupt body, missing checksum, unknown platform.
- Actions: full SHA only, least permissions, Dependabot update path.
- mise/Sheldon: first lock, identical second lock, unavailable locked artifact.
- externals: default offline render, correct checksum, wrong checksum.
- Nix: all declared outputs evaluate on appropriate OS runners.
- Regression: Python, agent assets, ShellCheck, shfmt, public bootstrap matrix.

## Done criteria

- [ ] No executable network content runs before integrity verification.
- [ ] Every external Action is pinned to a verified 40-character upstream SHA.
- [ ] Workflow token permissions are job-minimal.
- [ ] Required mise tools and Sheldon plugins resolve reproducibly from committed locks/pins.
- [ ] Normal chezmoi diff/apply does not call a latest-release API.
- [ ] Every external archive has a checksum.
- [ ] Nix uses a currently supported compatible release and has Linux/macOS CI.
- [ ] All local gates and Plan 003 public bootstrap checks pass.
- [ ] `plans/README.md` status is updated after merge.
- [ ] Before implementation and again before DONE, repeat this self-audit and
      attach its result to the PR/CI acceptance evidence.

## STOP conditions

- Upstream offers no immutable artifact and no trustworthy checksum/signature.
- A pinned version lacks a supported platform artifact.
- mise lock semantics cannot cover the declared backend/platform.
- Home Manager, nix-darwin, and nixpkgs have no mutually supported release set.
- Any fix requires committing a secret or private artifact URL.

## Maintenance notes

- Update pin, checksum/lock, tests, and provenance comment together.
- Reviewers must reject mutable fallbacks and unknown-schema acceptance.
- Keep update automation native to Dependabot, mise, Sheldon, and Nix.

## 安全回帰

- Unknown bytes never execute.
- Unavailable metadata never mutates existing pins.
- Lock regeneration is deterministic and reviewable.
- Security hardening does not require private credentials for public CI.
