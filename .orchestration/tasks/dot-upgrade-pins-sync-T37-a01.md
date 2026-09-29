# AGMSG-TASK dot-upgrade-pins-sync-T37-a01

## Objective

`make upgrade` ran on this host (canonical clone `~/.local/share/chezmoi`, base
09a7777) and left these pending, uncommitted pin changes there (read-only for
you; the orchestrator does not commit them because the ccusage bump breaks a
test until the expected versions move with it):

- `home/dot_mise/config.toml` + `home/dot_mise/mise.lock`: node 26.9.0→26.10.0,
  dotenvx 2.28.2→2.29.0, `npm:@anthropic-ai/claude-code` 2.1.283→2.1.284,
  `npm:@openai/codex` 0.157.1→0.158.0, `npm:ccusage` 20.0.23→20.0.24,
  `npm:pnpm` 12.4.1→12.5.1 (7-day window applied by mise `--before 7d`).
- Release-asset pins (`bump_release_asset_pins`): `home/dot_agents/agent-config.yaml`
  aws-cli 2.36.49→2.36.50 and crit v0.20.3→v0.21.0 with four new per-arch
  sha256; `install/ubuntu/common/aws_cli.sh` and `scripts/lib/installer-pins.sh`
  re-rendered accordingly.

`tests/unit/test_statusline_tools.py::test_mise_config_and_lock_pin_exact_npm_versions`
fails against that config because the ccusage expectation is still 20.0.23 in
`scripts/check-statusline-tools.py:20`, `tests/unit/test_statusline_tools.py:24,104`
and `.github/workflows/test.yaml:204,215` (the T25 lesson: the four locations
move together).

Deliver:

1. Carry the pending pins exactly (PR #178 precedent): on a clean branch run
   `git -C ~/.local/share/chezmoi diff origin/main -- home/dot_mise/config.toml home/dot_mise/mise.lock home/dot_agents/agent-config.yaml install/ubuntu/common/aws_cli.sh scripts/lib/installer-pins.sh | git apply --index`
   and prove blob identity: for each of the five files `git hash-object <file>`
   in your worktree must equal `git -C ~/.local/share/chezmoi hash-object <file>`.
   Paste both columns. Never edit those files by hand.
2. Sync ccusage 20.0.24 in the four locations above (and any other occurrence
   `grep -rn '20\.0\.23' scripts tests .github` finds). If `ccstatusline`
   stayed at 2.2.30, leave it.
3. Independently verify the two new release-asset pins against upstream
   (read-only network): `gh api repos/aws/aws-cli/git/refs/tags/2.36.50`
   exists; `crit` v0.21.0 release assets' sha256 equal the four values in the
   manifest (`gh release download tomasz-tomczyk/crit --pattern … -O - | sha256sum`
   or the checksums file). Paste the evidence; if any digest differs, STOP and
   PONG (supply-chain).
4. Tests: `make unit-test` green (the statusline test now expects 20.0.24);
   `make validate-agent-assets` ok; the render check
   (`scripts/generate-agent-configs.py --check`) ok.

[memory:decision] T37: the 2026-09-29 `make upgrade` pins (node 26.10.0,
dotenvx 2.29.0, claude-code 2.1.284, codex 0.158.0, ccusage 20.0.24, pnpm
12.5.1, aws-cli 2.36.50, crit v0.21.0) land together with the ccusage
expected-version sync in check-statusline-tools.py, its test, and test.yaml,
carried from the canonical clone with blob-identity proof (operator 2026-09-29).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c chore/upgrade-pins-20260929 origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `home/dot_mise/config.toml`, `home/dot_mise/mise.lock`, `home/dot_agents/agent-config.yaml`, `install/ubuntu/common/aws_cli.sh`, `scripts/lib/installer-pins.sh` (applied from the canonical diff only)
- `scripts/check-statusline-tools.py`, `tests/unit/test_statusline_tools.py`, `.github/workflows/test.yaml` (ccusage version strings only)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-upgrade-pins-sync-T37-a01.md` (main checkout)

## Forbidden actions

- Any write into `~/.local/share/chezmoi`; `make update`/`make upgrade`/`mise install`/`chezmoi apply`; hand-editing the five pin files; changing versions other than the ones listed; merging; force push; local bats; writes outside the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
for f in home/dot_mise/config.toml home/dot_mise/mise.lock home/dot_agents/agent-config.yaml install/ubuntu/common/aws_cli.sh scripts/lib/installer-pins.sh; do printf '%s %s %s\n' "$f" "$(git hash-object "$f")" "$(git -C ~/.local/share/chezmoi hash-object "$f")"; done
make validate-agent-assets
make unit-test
git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main` titled `chore(pins): make upgrade 2026-09-29 - node 26.10.0, codex 0.158.0, claude-code 2.1.284, ccusage 20.0.24 (+sync), pnpm 12.5.1, aws-cli 2.36.50, crit v0.21.0`, English description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs and the PR number/head SHA.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `send.sh --body-file` for replies (turn delivery reaches you).
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
