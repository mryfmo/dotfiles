# Acceptance: dot-mise-symlink-T3-a01

status: accepted
date: 2026-09-25
reviewer: claude-deep-dot (orchestrator, adversarial review)
cost: n/a

## Independent re-derivation

- Templates `home/dot_config/mise/{config.toml,mise.lock}.tmpl` render byte-identical to `home/dot_mise/*` (`chezmoi execute-template | cmp`, orchestrator-run).
- upgrade-tools.sh: `MISE_CONFIG_DIR` defaults to `<checkout>/home/dot_mise`, override preserved; `MISE_CEILING_PATHS=<checkout>`; worker's native `mise config ls` probe lists only the checkout config.
- Fake-mise spill fixture (default + override) and chezmoi render/apply fixtures are red-first per validation.
- `make unit-test`: one non-reproducible failure on first run while T4's suite ran concurrently; second run 393 OK. CI is the arbiter.
- shellcheck, shfmt, asset validator, diff check, review guard: OK.

## Live verification pending (operator)

Next `make update` on the operator machine must replace `~/.config/mise/{config.toml,mise.lock}` symlinks with regular files (`ls -la ~/.config/mise`), and a subsequent `make update` must show no chezmoi diff.

## Integration

Committed on `fix/mise-config-not-live-symlink`, PR #172.

## Revision 1 (PR #172 Codex bot review, commit 124c089)

- home/dot_zshrc:51 — `@description` inside a function body is not shdoc-attachable; make it a plain inline comment. Valid.
- scripts/upgrade-tools.sh:15 — after `make upgrade`, `~/.config/mise` (now an applied copy) still carries the old pins until `make update`, so shells resolve old versions meanwhile. Valid. Fix: when the executing checkout is the chezmoi source tree, end the upgrade by applying just the two managed files (`chezmoi apply ~/.config/mise/config.toml ~/.config/mise/mise.lock`); otherwise print one line saying the live copy follows after merge + `make update`. Test both branches with a fake chezmoi in the existing upgrade fixture.

## Revision 1 result

status: accepted — `apply_upgraded_mise_config` applies only the two managed files when `chezmoi source-path` toplevel == repo_root and no required phase failed; otherwise prints the follow-after-merge note. Four-case fixture (canonical/non-canonical × failure phases). Orchestrator reran unit suite OK, shellcheck, shfmt, diff check. Pushed to PR #172.
