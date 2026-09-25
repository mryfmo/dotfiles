# AGMSG-TASK dot-herdr-sheldon-T1-a02 — rebase and finish the two revised tasks in worktree herdr-sheldon

Both dot-herdr-sheldon-T1-a01 and dot-docs-align-T1-a01 got `status=revise` (see `.orchestration/acceptance/dot-herdr-sheldon-T1-a01.md` and `.orchestration/acceptance/dot-docs-align-T1-a01.md` in the main repo). Their uncommitted diffs still sit in `.claude/worktrees/herdr-sheldon` (branch `fix/herdr-reload-and-sheldon-client`, based on 788ba3b; main is now far ahead).

## Steps

1. In that worktree: save the current diff (`git diff > .agents/worklog/codex/herdr-sheldon-pre-rebase.patch`), then `git reset --hard` and `git reset --hard origin/main` (branch stays the same name), then re-apply the patch by hand where it still makes sense:
   - KEEP: Makefile herdr reload `protocol_mismatch` tolerance + `tests/install/common/lifecycle.bats` cases + README lifecycle paragraph; Dockerfile ubuntu 24.04 / no apt bats / UID-1000 reuse; `scripts/update-agent-assets.sh` header comment; `home/dot_agents/README.md` numbering fix.
   - DROP: `home/dot_config/sheldon/plugin_sources/client/ubuntu.toml` change and its `setup.bats` case (superseded by 82d4961 on main).
   - RE-MERGE against current text: README herdr-agents section (pane split / agent start / worker_kind wording from d004ddb + 4d4767b must be preserved).
   Note main's Makefile `update` target changed in #170 (unmerged-index check first); keep that.
2. Validation (verbatim): `make unit-test`; `uv run --with pyyaml python scripts/validate-agent-assets.py`; the reload fixture trace for both branches (as in the original validation); `git diff --check`; `rg` stale-text check from dot-docs-align-T1-a01.
3. Artifacts: `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-herdr-sheldon-T1-a02.md` under the MAIN repo `.orchestration/`. Move the a01 artifacts that only exist under the worktree `.orchestration/` into the main repo `.orchestration/` unchanged (they are history).

## allowed_files

`Makefile`, `README.md`, `Dockerfile`, `scripts/update-agent-assets.sh` (header comment only), `home/dot_agents/README.md`, `tests/**`, `.orchestration/**` artifacts named above, `.agents/worklog/codex/**`.

## forbidden_actions

no git commit; no push; no PR; no local bats; no VM/docker (already proven in a01); no mise changes; no logic changes beyond the a01 scope.

max_turns=25. Reply with `AGMSG-RESULT v1`.
