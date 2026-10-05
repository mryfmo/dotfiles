# E2E leg: macOS installers and unattended `make update` (operator-run)

Evidence pasted by the operator into the orchestrator session on 2026-10-05 (macOS host `a0004262`, Intel x64: `Skipping mise upgrade for fd: newer releases lack a macOS x64 asset`). Recorded by the orchestrator seat; the operator's own shell transcript is the source.

Command: `git -C ~/.local/share/chezmoi pull && make -C ~/.local/share/chezmoi update && make -C ~/.local/share/chezmoi upgrade`

- `git pull`: fast-forward 62d0771f..413e3f37 with `Created autostash` / `Applied autostash` (the Mac clone carries local tracked changes; `make update` then printed `Notice: local source not pulled (tracked files have staged or unstaged changes)`).
- `make update`: ran to completion without a password or other prompt; `chezmoi apply --verbose` deployed `.agents/agent-config.yaml` (orchestrator_kind, Codex `command_hooks`, CompactionDB pin 2.0.0+dotfiles.9), `.agents/model-profiles.env` (`HERDR_AGENTS_ORCHESTRATOR_KIND="claude"`), the SKILL and rule changes, `.codex/config.toml` with the three CompactionDB hook tables, `codex-orchestrate`, `contextdb-codex-notify` and `herdr-agents`; Claude Code plugins Crit 1.8.11→1.8.12 and Ponytail 4.10.3→4.12.0 ("Restart to apply"); Codex plugins and Understand-Anything skills refreshed; herdr integrations installed (`config_reload` applied).
- Warnings during `make update`: `hook trust divergence` for the three ponytail hooks (same as Linux; resolved by dotfiles-T82b), `GitHub CLI is not authenticated. Run setup-gh` (Mac `gh` not logged in: extensions skipped), `private chezmoi source/config not found` (expected on this host), `No agmsg Claude Code identity for ~/.local/share/chezmoi` (the chezmoi clone is not an agmsg project; informational).
- `make upgrade`: Homebrew no upgrades after forbidden-formula filtering; `mise` tools current except `npm:pnpm 12.7.0 → 12.8.0` (new pin diff left in the Mac clone); agent CLIs `npm:@openai/codex@0.160.0`, `npm:@anthropic-ai/claude-code@2.1.289`; terminal tool pins, release asset pins and gh extensions skipped for lack of `gh` auth; `Upgrade summary: required failures: 0; optional warnings: 3`.
- Not yet pasted for this leg: `make doctor` output and `bats tests/install/macos` (operator to run after `gh auth login`).

Follow-ups: the Mac pin diff (pnpm 12.8.0 and the autostashed local changes) travels as a branch `pins/macos-2026-10-05` pushed by the operator; the orchestrator opens the PR and the worker task syncs the version assertions in `tests/**`.
