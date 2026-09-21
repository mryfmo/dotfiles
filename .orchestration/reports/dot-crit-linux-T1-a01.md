# dot-crit-linux-T1-a01 report

cost: n/a

## Result

- F1: pinned stable Crit `v0.20.2` Linux amd64/arm64 binaries to their upstream-matching SHA-256 values. Linux now downloads to a temporary file, verifies checksum and version, stages beside the destination, then atomically replaces `~/.local/bin/crit`; macOS keeps the Homebrew path.
- F1: the correct pinned Linux version is a download-free no-op, and a checksum/version failure leaves an existing binary unchanged. `make upgrade` refreshes the Crit tag and both binary hashes with the existing pin rewrite.
- F1: `ensure_crit_cli` records `~/.local/bin/crit` in the installed-asset manifest. Scoped reverse mapping: `rm ~/.local/bin/crit`.
- F2: `make update` runs `git pull --ff-only` only on clean `main` tracking `origin/main`. Every ineligible state prints one actionable Notice and continues; pull failure warns and continues.
- F2: README lifecycle and agent-asset documentation now describes both behaviors.

## Revision

- Replaced the function-scoped `RETURN` cleanup trap with `install_pinned_linux_crit`, a subshell helper using an `EXIT` trap. Cleanup variables now remain alive for the full trap lifetime, matching `_install_mise_binary`.
- Restored the README validator's literal single-line token `version-matched Claude release artifact`.
- Added a trap-leak regression and passed the requested full runtime-health suite plus `scripts/validate-agent-assets.py`.
- Resolved the Bats Notice assertion through `pwd -P` fixture resolution. The product remains unchanged: macOS CI exposed `/var` versus `/private/var`, while both Ubuntu jobs passed the original assertion.

## Validation

- Official GitHub latest-release metadata reports `v0.20.2`, `draft=false`, `prerelease=false`.
- Both downloaded Linux binary hashes match the upstream `checksums.txt` entries.
- Bash syntax, production ShellCheck, Bats ShellCheck with repository-existing SC2314/SC2016 exclusions, shfmt, ruff, and `git diff --check` pass.
- The related Python unit suites pass all 36 tests. Local bats was not run, as required.
- Hermetic `make update` traces prove pull-before-apply on clean main and no pull plus the exact Notice on dirty main.
- The actual `ensure_crit_cli` function installed and ran `crit v0.20.2` in a credential-free `adh-test` scratch user, wrote the manifest path, and removed the user/home afterward.
- Codex completed initial and revision Crit data reviews with three resolved review-scope approval records and passed `make require-crit-review` using the repo-local receipt.
- Revise validation passed 26 runtime-health tests and the full agent-asset validator.

Full command outputs are in `.orchestration/validation/dot-crit-linux-T1-a01.md`.

## Durable decision

[memory:decision] Linux Crit installs use stable, pinned amd64/arm64 release binaries with verified SHA-256 and atomic replacement, while `make update` pulls only clean `main` tracking `origin/main` and otherwise continues with an actionable notice.

CompactionDB command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-crit-linux-T1-a01: Linux Crit installs pin stable v0.20.2 amd64/arm64 release binaries with verified SHA-256 and atomic replacement, while make update pulls only clean main tracking origin/main and otherwise continues with an actionable notice.'
```

Memory ID: `7520a322-d63d-403a-9837-70af16f3b871`

Revision failure memory command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content 'dot-crit-linux-T1-a01 revise: a RETURN trap created inside ensure_crit_cli can outlive its local cleanup variables and fail later function returns under set -u; isolate download staging in a subshell helper and use an EXIT trap, following _install_mise_binary.'
```

Failure memory ID: `1639ae38-a92b-4f5a-a0c4-b7659a9b257e`

Path-resolution failure memory ID: `b62160c1-001b-444f-afac-f3c18347527f`

## Side effects and reverse mapping

- The final VM validation left no scratch user, home, or Crit binary behind.
- Runtime installation by `make update` is recorded as manifest step `ensure_crit_cli`; this task's documented reverse operation is `rm ~/.local/bin/crit`.
- Full `remove-agent-asset` support for this path was explicitly kept outside task scope.

## Constraints honored

- No git commit or push.
- No local bats execution.
- No mise config or lock changes.
- VM work used only `limactl shell adh-test`; no credentials were copied.
- Scratch users were removed and cleanup was verified.
