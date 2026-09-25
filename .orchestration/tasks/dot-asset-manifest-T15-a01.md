# AGMSG-TASK dot-asset-manifest-T15-a01: single asset manifest and rendered version pins (plan Phase L.1)

Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/remediation-plan-20260925.md` §Phase L, task L.1, principles B-6..B-9, inventory §2.1. Read them first.
Repo: `/home/moriya/Workspace/dotfiles/.claude/worktrees/env-converge-T10`, branch `feat/asset-manifest` from origin/main (after T14 is pushed and the tree is clean). You are `claude-standard-dot-a003`.

## Objective

Give every third-party component ONE declaration (upstream identity, pin, verification, install path, installer step) and render every hard-coded version from it, so that later phases (L.2 pinned-only update, L.3 pin-only upgrade, L.4 Renovate, L.5 doctor drift) have a single source of truth. This task changes no installed behaviour: rendered values must be byte-identical to today's constants.

## Design

1. **Location**: extend `home/dot_agents/agent-config.yaml` with a top-level `assets:` map (reuse the existing manifest; do not add a second YAML file). One entry per component, e.g.:
   ```yaml
   assets:
     mise:            { source: github-release, upstream: jdx/mise, pin: v2026.9.12, verify: release-shasums, install_path: ~/.local/bin/mise, installer: install/common/mise.sh }
     sheldon:         { source: crates, upstream: sheldon, pin: 0.8.5, verify: cargo-locked, installer: install/common/sheldon.sh }
     starship:        { source: github-release, upstream: starship/starship, pin: v1.25.1, verify: release-sha256, installer: install/ubuntu/server/starship.sh }
     aws-cli:         { source: github-release, upstream: aws/aws-cli, pin: 2.35.21, verify: gpg, gpg_fingerprint: <existing>, installer: install/ubuntu/common/aws_cli.sh }
     homebrew-installer: { source: git-commit, upstream: Homebrew/install, pin: <existing commit>, sha256: <existing>, installer: install/macos/... }
     crit:            { source: github-release, upstream: tomasz-tomczyk/crit, pin: v0.20.3, sha256: { linux-amd64: ..., linux-arm64: ... }, install_path: ~/.local/bin/crit, installer: scripts/update-agent-assets.sh#ensure_crit_cli }
     zed:             { ... from installer-pins.sh ... }
     tode:            { source: installer-script, upstream: https://tode.sh/install, pin: v0.3.4, sha256: <installer sha>, note: payload-not-pinned-yet }
     terminal-browser: { ... }
     understand-anything-installer: { source: git-commit, upstream: Egonex-AI/Understand-Anything, pin: 797ce79..., sha256: <existing> }
     compactiondb:    { source: vendored, upstream: <URL or "unknown">, pin: 2.0.0+dotfiles.6, manifest: vendor/compactiondb/MANIFEST.sha256 }
     agmsg:           { source: vendored, upstream: https://github.com/fujibee/agmsg, pin: "snapshot-2026-06-22", note: replaced-by-npm-pin-in-L.7 }
     claude-plugins:  { superpowers: { marketplace: anthropics/claude-plugins-official, pin: 6.4.1 }, crit: {...1.8.10}, ponytail: {...4.10.0}, understand-anything: {...2.9.7} }
     codex-plugins:   { superpowers: {...}, ponytail: { last_revision: <existing>, last_updated: <existing> } }
     gh-extensions:   [ { name: seachicken/gh-poi, pin: v0.18.4 } ]
   ```
   mise-managed tools stay in `home/dot_mise/config.toml` + `mise.lock` (mise is already a manifest); add one `assets.mise-tools: { source: mise, files: [home/dot_mise/config.toml, home/dot_mise/mise.lock] }` pointer so the inventory is complete. Take every current value verbatim from the files listed in §2.1; do not bump anything.
2. **Rendering**: `scripts/generate-agent-configs.py` renders (a) `scripts/lib/installer-pins.sh` from `assets.{crit,zed,tode,terminal-browser}`, (b) a new generated fragment `install/lib/asset-pins.sh` (or per-script `readonly` blocks — choose the one that keeps `install/*.sh` as plain `include`-able scripts under chezmoi; document why) consumed by `install/common/mise.sh`, `install/common/sheldon.sh`, `install/ubuntu/server/starship.sh`, `install/ubuntu/common/aws_cli.sh`, and the Homebrew installer script, replacing their hard-coded `*_VERSION`/commit/sha constants, (c) the `CODEX_UNDERSTAND_ANYTHING_INSTALLER_*` constants and the ponytail `last_revision`/`last_updated` in the Codex config template. `--check` must report clean after regeneration.
3. **Validator**: `scripts/validate-agent-assets.py` checks every `assets` entry has `source`, `upstream`, `pin`, and a verification field appropriate to its source; checks rendered files match the generator output (already the pattern for other templates); fails if any `install/*.sh` still contains a literal `*_VERSION="..."` assignment.
4. **Docs**: README lifecycle section: one paragraph "Asset manifest" describing the single source of truth and that pins change only via the manifest (L.3/L.4 will describe how).

## Tests
- `tests/unit/test_generate_agent_configs.py`: rendering of installer-pins.sh and the install pin fragment from a fixture manifest; `--check` detects drift.
- `tests/unit/test_validate_agent_assets.py`: missing field, literal version left in an installer, rendered drift.
- Byte-identity proof in validation: `git diff --stat` shows generated files with no semantic change; `bash -n` on every touched installer; `shellcheck` clean; `diff <(git show origin/main:scripts/lib/installer-pins.sh) scripts/lib/installer-pins.sh` shows only the generated-header comment (or nothing).
- No local bats; CI runs bootstrap jobs which exercise the installers.

## Validation (verbatim)
`uv run --with pyyaml scripts/generate-agent-configs.py --check`; validator; unit tests; the byte-identity diffs; `gh pr checks` final table.

## Commit / PR
Commits: `feat(agents): declare every third-party asset in one manifest`, `refactor(install): render version pins from the asset manifest`, `test(...)`. Push `feat/asset-manifest`, PR (English), CI green.

## allowed_files
`home/dot_agents/agent-config.yaml`, `scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py`, `scripts/lib/installer-pins.sh` (generated), a new `install/lib/asset-pins.sh` (or equivalent; name it), `install/common/mise.sh`, `install/common/sheldon.sh`, `install/ubuntu/server/starship.sh`, `install/ubuntu/common/aws_cli.sh`, the macOS Homebrew installer script, `home/.chezmoitemplates/codex-config-managed.toml` (generated), `scripts/update-agent-assets.sh` (only to source the rendered constants), `README.md`, tests, and the five artefacts. Anything else → blocked with reason.

## forbidden_actions
bumping any version; `make update`/`make upgrade`/`chezmoi apply`; touching `~/.local/share/chezmoi`; merging; local bats; force-push.

## Artefacts
`.orchestration/<dir>/dot-asset-manifest-T15-a01.md` ×5; `[memory:decision]`: "third-party asset versions live only in agent-config.yaml assets:, rendered by generate-agent-configs.py; installers carry no literal versions". `contextdb_cli.py memory add` from the main checkout; paste.

## Done signal
`AGMSG-RESULT v1 task_id=dot-asset-manifest-T15-a01 status=ready_for_review|blocked pr=<n> ...` via `send.sh dotfiles claude-standard-dot-a003 claude-remediation-dot "<message>"`. max_turns=45.

## Round 3 (orchestrator, 12:07Z) — CodeRabbit final review 5317380626, inline 4104294574

`LITERAL_VERSION_ASSIGNMENT` matches only double-quoted values; unquoted (`readonly TOOL_VERSION=1.2.3`) and single-quoted (`TOOL_VERSION='1.2.3'`) handwritten versions pass validation. Fix at the root: accept `"..."`, `'...'`, and unquoted `[^\s"'$;`()]+` values (still excluding `$` references), respect the assignment boundary, and add both cases to `test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts`. Reply on the CodeRabbit thread with the commit. Push once; no further CodeRabbit trigger (hourly plan) — the thread acknowledgement on the new head is the completion signal for this item.
