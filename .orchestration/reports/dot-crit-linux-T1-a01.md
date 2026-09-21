# dot-crit-linux-T1-a01 report

cost: n/a

## Result

- F1: pinned stable Crit `v0.20.2` Linux amd64/arm64 binaries to their upstream-matching SHA-256 values. Linux now downloads to a temporary file, verifies checksum and version, stages beside the destination, then atomically replaces `~/.local/bin/crit`; macOS keeps the Homebrew path.
- F1: the correct pinned Linux version is a download-free no-op, and a checksum/version failure leaves an existing binary unchanged. `make upgrade` refreshes the Crit tag and both binary hashes with the existing pin rewrite.
- F1: `ensure_crit_cli` records `~/.local/bin/crit` in the installed-asset manifest. Scoped reverse mapping: `rm ~/.local/bin/crit`.
- F2: `make update` runs `git pull --ff-only` only on clean `main` tracking `origin/main`. Every ineligible state prints one actionable Notice and continues; pull failure warns and continues.
- F2: README lifecycle and agent-asset documentation now describes both behaviors.

## Validation

- Official GitHub latest-release metadata reports `v0.20.2`, `draft=false`, `prerelease=false`.
- Both downloaded Linux binary hashes match the upstream `checksums.txt` entries.
- Bash syntax, production ShellCheck, Bats ShellCheck with repository-existing SC2314/SC2016 exclusions, shfmt, ruff, and `git diff --check` pass.
- The related Python unit suites pass all 36 tests. Local bats was not run, as required.
- Hermetic `make update` traces prove pull-before-apply on clean main and no pull plus the exact Notice on dirty main.
- The actual `ensure_crit_cli` function installed and ran `crit v0.20.2` in a credential-free `adh-test` scratch user, wrote the manifest path, and removed the user/home afterward.
- Codex completed a Crit data review with one resolved review-scope approval record and passed `make require-crit-review` using the repo-local receipt.

Full command outputs are in `.orchestration/validation/dot-crit-linux-T1-a01.md`.

## Durable decision

[memory:decision] Linux Crit installs use stable, pinned amd64/arm64 release binaries with verified SHA-256 and atomic replacement, while `make update` pulls only clean `main` tracking `origin/main` and otherwise continues with an actionable notice.

CompactionDB command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-crit-linux-T1-a01: Linux Crit installs pin stable v0.20.2 amd64/arm64 release binaries with verified SHA-256 and atomic replacement, while make update pulls only clean main tracking origin/main and otherwise continues with an actionable notice.'
```

Memory ID: `7520a322-d63d-403a-9837-70af16f3b871`

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
