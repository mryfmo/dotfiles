# AGMSG-TASK dot-macos-crit-pinned-install-T17-a01: install Crit on macOS from the pinned release, stop swallowing install failures (plan Phase G.2)

Evidence: every `public-bootstrap (macos-14, client)` run on PRs #178 and #180 carries a failure-level annotation `crit: no bottle available!` (brew, Tier 3) plus "taps are not trusted: aws/tap azure/bicep hashicorp/tap", while the job succeeds because `scripts/update-agent-assets.sh:252` runs `brew install crit || true` and `.github/workflows/test.yaml:125` runs `brew trust ... || true`. Release `tomasz-tomczyk/crit v0.20.3` ships `crit-darwin-amd64`, `crit-darwin-arm64` and `checksums.txt`.

Repo: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-b` (your own worktree, detached at origin/main; `git switch -c fix/macos-crit-pinned-install origin/main`). You are `claude-standard-dot-a004` (herdr pane wE:p4). T15 (asset manifest) is merged: put the darwin sha256 pins in `assets.crit.sha256.{darwin-amd64,darwin-arm64}` and regenerate; do not edit installer-pins.sh by hand.

## Required changes
1. `ensure_crit_cli` in `scripts/update-agent-assets.sh`: use the same pinned-release path on Darwin as on Linux: download `crit-darwin-<arch>` for `CRIT_PIN_VERSION`, verify against pinned sha256, install to `~/.local/bin/crit`. Remove the `brew install crit || true` branch. Keep `--version` verification.
2. Pins: add `CRIT_DARWIN_AMD64_SHA256` / `CRIT_DARWIN_ARM64_SHA256` (from the release `checksums.txt`, verify against the downloaded binaries) — if T15 (asset manifest) has landed, add them to the manifest and regenerate; otherwise to `scripts/lib/installer-pins.sh` and extend `fetch_crit_pin` in `scripts/upgrade-tools.sh` to compute darwin hashes too.
3. Doctor: report crit version and origin (pinned release) on both OSes.
4. CI (`.github/workflows/test.yaml`): the macOS bootstrap step must fail on installer failure — remove `|| true` on `brew trust` and decide explicitly: either trust the taps with a documented reason or drop the untrusted taps from the install list. Any remaining tolerated failure must be an explicit, commented `continue-on-error` at step level, never a shell `|| true`.
5. Tests: unit test for the Darwin branch (fake `uname`, fake `curl`, sha mismatch → fail), bats for the CI-facing behaviour if a bats file covers update-agent-assets; validator passes.

## Validation (verbatim)
Unit tests; validator; `gh pr checks` with `public-bootstrap (macos-14, client)` annotations count = 0 failure-level (paste `gh api check-runs/<id>/annotations`); `pr-feedback.py <n>` output with dispositions (rule from T16).

## allowed_files
`scripts/update-agent-assets.sh`, `scripts/lib/installer-pins.sh` or the asset manifest + generated files, `scripts/upgrade-tools.sh`, `scripts/check-tools.sh`, `.github/workflows/test.yaml`, tests, README (crit install section), artefacts.

## forbidden_actions
merging; `make update`/`make upgrade`/`chezmoi apply`; local bats; force-push; shell-level `|| true` on install steps.

## Artefacts / Done signal
Standard five + pr-feedback JSON. `[memory:decision]`: "Crit is installed from the pinned GitHub release with per-platform sha256 on every OS; install failures fail the run". RESULT via send.sh. max_turns=30.
