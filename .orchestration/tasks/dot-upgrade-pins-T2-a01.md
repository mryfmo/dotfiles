# AGMSG-TASK dot-upgrade-pins-T2-a01 — regenerate tool pins via make upgrade

## Objective

The operator's machine already runs newer tools than the committed pins (mise `ls --current`: dotenvx 2.28.0, gh 2.101.0, herdr 0.9.1, node 26.9.0, bash-language-server 5.8.0, uv 0.12.15; Crit v0.20.3 live). The previous uncommitted `make upgrade` output was discarded during git recovery (evidence: `.agents/worklog/claude/2026-09-25-autostash-recovery/*.patch`). Regenerate it cleanly on top of current `origin/main` so the pins are committed in one chore commit, never left dirty.

## Steps

1. In the `update-convergence` worktree (or a new `upgrade-pins` worktree from origin/main if B is not merged yet — use `git worktree add .claude/worktrees/upgrade-pins -b chore/upgrade-pins origin/main`), run `make upgrade` (no `SYSTEM=1`).
2. Review the resulting diff of `home/dot_mise/config.toml`, `home/dot_mise/mise.lock`, `scripts/lib/installer-pins.sh`. Expected: the versions listed above plus crit v0.20.3 with its two Linux SHA256 values. Report any other change (e.g. tode/terminal-browser bumps) explicitly.
3. Verify the crit checksums independently: download both release assets for the pinned tag and `shasum -a 256`; paste output.
4. `mise install --locked` succeeds in the worktree; `uv run pytest tests/unit -q -k 'upgrade or mise or pins'`.

## allowed_files

- `home/dot_mise/config.toml`, `home/dot_mise/mise.lock`, `scripts/lib/installer-pins.sh` (only via `make upgrade`; no hand edits)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-upgrade-pins-T2-a01.md` under the herdr-sheldon worktree

## forbidden_actions

no git commit; no push; no PR; no local bats; no `make update`/`chezmoi apply`; no edits outside allowed_files; no ad-hoc version edits.

## Durable facts

- [memory:decision] Tool pin bumps are produced only by `make upgrade` on a clean main-based branch and committed as a single `chore(mise)` commit in the same session.

Record with `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "..."` and paste the command + ID into the report.

max_turns=20. Reply with `AGMSG-RESULT v1`.
