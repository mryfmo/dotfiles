# AGMSG-TASK dot-mise-symlink-T3-a01 — stop `make upgrade` and mise from writing into the main checkout through the live symlink

## Root cause (established)

- `home/dot_config/mise/symlink_config.toml.tmpl` and `symlink_mise.lock.tmpl` make `~/.config/mise/{config.toml,mise.lock}` symlinks into `{{ .chezmoi.sourceDir }}/dot_mise/*`, i.e. the MAIN checkout.
- `scripts/upgrade-tools.sh:186` resolves `mise_config_dir` to `~/.config/mise` by default. So `make upgrade` run in ANY worktree (and any ad-hoc `mise upgrade`, e.g. `home/dot_zshrc:51`) follows the symlink and mutates main's `home/dot_mise` pair. This is what left main dirty across sessions (the 2026-09-22 autostash conflict) and what spilled T2's output into main today.

## Required outcome

1. `make upgrade` operates ONLY on the checkout it runs from: in `scripts/upgrade-tools.sh` default `mise_config_dir` to `"${repo_root}/home/dot_mise"` (repo_root already computed the same way elsewhere in the file; keep the `MISE_CONFIG_DIR` env override for tests). Update the two grep assertions in `tests/install/common/lifecycle.bats:271-272` to the new literal and add a bats/unit case proving that a worktree run with a symlinked `~/.config/mise` does not touch the symlink target (fixture: fake HOME with symlinks into a separate "main" dir; run the upgrade path with fake `mise`; assert main dir unchanged and worktree pair changed).
2. `~/.config/mise/*` must stop being a live write path into the source tree: replace the two `symlink_*.tmpl` with chezmoi-managed regular files that render the committed content (e.g. `home/dot_config/mise/config.toml.tmpl` / `mise.lock.tmpl` using `{{ include "../../dot_mise/config.toml" }}` style include, or whatever chezmoi idiom the repo already uses for included sources — check `home/.chezmoitemplates` and existing `include` usage). Keep `home/dot_mise/*` as the single source of truth. Update `tests/unit/test_supply_chain_policy.py:187` (currently asserts the symlink template exists) to assert the new managed-file form and that the rendered content equals `home/dot_mise/*`.
3. `home/dot_zshrc:51` (`mise upgrade "npm:@anthropic-ai/claude-code"`) — after (2) this writes to `~/.config/mise` only; leave it, but add one comment line noting pins are committed only via `make upgrade`.
4. README `make upgrade` paragraph (around L428) and `scripts/upgrade-tools.sh` @description: one sentence each stating that upgrade edits the current checkout's `home/dot_mise` and `~/.config/mise` is an applied copy.

Ponytail: smallest diff that achieves 1–2; no new abstractions; no new deps.

## Worktree / branch

New worktree `.claude/worktrees/mise-symlink` from `origin/main`, branch `fix/mise-config-not-live-symlink`. Do NOT rebase onto PR #170 or the upgrade-pins branch.

## allowed_files

`scripts/upgrade-tools.sh`, `home/dot_config/mise/**`, `home/dot_zshrc`, `README.md`, `tests/**`, `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-mise-symlink-T3-a01.md` (write artifacts under the MAIN repo `.orchestration/` — your registered project now includes the main path).

## forbidden_actions

no git commit; no push; no PR; no local bats; NO `chezmoi apply`/`make update` on the operator HOME (prove with fixtures only); no mise config/lock content changes; no touching PR #170 / upgrade-pins worktrees.

## Validation (verbatim outputs)

- `make unit-test`; `shellcheck scripts/upgrade-tools.sh`; `shfmt -i 4 -sr -d scripts/upgrade-tools.sh`; `git diff --check`.
- `chezmoi execute-template` (or `chezmoi cat` against a temp destDir/config with `--source` pointing to the worktree `home/`) showing `~/.config/mise/config.toml` renders as a regular file byte-identical to `home/dot_mise/config.toml`.
- The new spill-proof fixture test red-first then green.
- `uv run --with pyyaml python scripts/validate-agent-assets.py`.

## Durable facts

- [memory:decision] `~/.config/mise` is an applied copy of `home/dot_mise`; `make upgrade` mutates only the checkout it runs from. Record via `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "..."` and paste the ID.

max_turns=30. Reply with `AGMSG-RESULT v1`.
