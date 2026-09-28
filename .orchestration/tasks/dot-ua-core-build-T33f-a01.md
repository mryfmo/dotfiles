# AGMSG-TASK dot-ua-core-build-T33f-a01

## Objective

The managed asset lifecycle installs Understand-Anything (Claude plugin via the
marketplace; Codex-side clone at `~/.understand-anything/repo` with the
`~/.understand-anything-plugin` symlink) but never builds
`packages/core`, so `skills/understand/prepare-incremental.mjs` (which imports
`packages/core/dist/index.js`) cannot run and every `.ua/` incremental update
request from the SessionStart/PostToolUse hooks fails. Evidence:
`.orchestration/learning/rule_candidates/understand-anything-core-build.md`
(T33c blocked PONG, 2026-09-28). The orchestrator built it once by hand with
`mise exec pnpm@12.4.1 -- pnpm install --frozen-lockfile && mise exec pnpm@12.4.1 -- pnpm --filter @understand-anything/core build`
because `pnpm` has no mise global default on this host.

Verified facts (orchestrator, read-only, 2026-09-28): `provision_codex_understand_anything_runtime`
copies `packages/core/dist`, `packages/core/node_modules` and `node_modules` FROM the
Claude plugin cache release artifact (`~/.claude/plugins/cache/understand-anything/understand-anything/<ver>`)
INTO the Codex clone, silently skipping absent sources. The cache artifact 2.9.7
contains neither `dist` nor `node_modules` (marketplace checkouts are git
content; `dist` is a build output), so the copy loop provisions nothing and no
warning is printed. Upstream's own `skills/understand/SKILL.md` (lines 117–119)
builds in place wherever `$PLUGIN_ROOT` resolves — `if [ ! -f
"$PLUGIN_ROOT/packages/core/dist/index.js" ]; then cd "$PLUGIN_ROOT" && (pnpm
install --frozen-lockfile 2>/dev/null || pnpm install) && pnpm --filter
@understand-anything/core build; fi` — i.e. upstream expects the build to happen
inside the Claude plugin cache for Claude sessions (`$CLAUDE_PLUGIN_ROOT`) and
inside `~/.understand-anything-plugin` for Codex. `packages/core/package.json`
has `"build": "tsc"`; the root `package.json` declares no `packageManager`.

Deliver:

1. `scripts/update-agent-assets.sh` — in `provision_codex_understand_anything_runtime`,
   before the copy loop: when the release artifact lacks
   `packages/core/dist/index.js`, run upstream's exact guard+build in the release
   artifact directory (this mirrors what the plugin's own skill does in a Claude
   session, so writing `dist`/`node_modules` there is sanctioned by upstream);
   then let the existing loop copy `dist`/`node_modules` into the Codex clone as
   today. If there is no release artifact at all, build directly in the clone
   with the same guard. Idempotent (the `index.js` guard); on a build failure
   print a WARN naming the manual command and continue (never fail `make
   update` for this). Resolve `pnpm` without a global default: the mise-pinned
   tool (item 2) via the mise shim, else `mise exec pnpm@<pin> -- pnpm`, else
   WARN and skip. shdoc comments in English.
2. Pin `pnpm` in the mise manifest `home/dot_mise/config.toml` (+ lock) at the
   version the plugin's `packageManager`/lockfile expects (check
   `~/.understand-anything-plugin/package.json`; 12.4.1 was used successfully),
   following the existing tool-pin pattern and the 7-day window rule for new
   pins (`scripts/upgrade-tools.sh` conventions) — if the pin would violate the
   window, PONG with the candidate versions instead of pinning.
3. `scripts/check-agent-runtime.py` (doctor) — WARN when the Codex-side clone
   exists but `packages/core/dist/index.js` is missing or older than `src`,
   naming the make target that fixes it (`make update`).
4. Tests: `tests/unit/` cases with fake `pnpm`/`mise` for (a) build runs when
   dist is missing, (b) build is skipped when dist is fresh, (c) WARN path when
   no pnpm is resolvable, (d) doctor WARN/ok for the two dist states. Mutation
   baseline against the unmodified scripts.
5. README: one sentence in the Understand-Anything section about the core
   build being part of `make update`.

[memory:decision] T33f: `update-agent-assets.sh` builds Understand-Anything
`packages/core` idempotently after provisioning the Codex-side clone using a
mise-pinned pnpm, and `make doctor` warns when `dist` is missing or stale, so
`.ua/` incremental updates never depend on a manual build (operator 2026-09-28).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c fix/ua-core-build origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `scripts/update-agent-assets.sh`
- `scripts/check-agent-runtime.py`
- `home/dot_mise/config.toml`, `home/dot_mise/mise.lock` (pnpm pin only)
- `tests/unit/test_update_agent_assets*.py`, `tests/unit/test_check_agent_runtime*.py` (existing or new)
- `README.md`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ua-core-build-T33f-a01.md` (main checkout)

## Forbidden actions

- Running the real `update-agent-assets.sh`, `make update`, `make upgrade`,
  `mise install`, `pnpm`, or any network install on the host (fake CLIs only);
  touching the Claude plugin cache, model_profiles, permgate, hooks configs,
  `reviews/ADH_Integrated_Plan/`; merging; force push; local bats;
  `make apply`/`chezmoi apply`; writes outside the worktree except the listed
  `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
shellcheck scripts/update-agent-assets.sh
shfmt --indent 4 --space-redirects --diff scripts/update-agent-assets.sh
git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs
   (including the mutation baseline) and the PR number/head SHA.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `inbox.sh dotfiles claude-standard-dot-a005` at each milestone.
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
   Live verification (`make update` on this host after merge) is
   orchestrator-side at acceptance.
