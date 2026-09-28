# AGMSG-TASK dot-ua-core-build-shim-T33g-a01

## Objective

T33f's live verification failed on this host (acceptance record
`.orchestration/acceptance/dot-ua-core-build-T33f-a01.md`, "Live verification"):
`build_understand_anything_core` chose `pnpm` because `has_command pnpm` saw
the mise shim, but the newly pinned `npm:pnpm 12.4.1` was not installed, so the
shim failed with `mise ERROR No version is set for shim: pnpm` and the build
WARNed. `make update` installs pinned mise tools only from an explicit list
(`Makefile`: `mise install --locked node` and `mise install --locked
npm:ccstatusline npm:ccusage`); there is no mise onchange script; new pins are
installed only by `make upgrade` or on-demand `mise exec`. Verified on this
host: `mise exec npm:pnpm -- pnpm --version` auto-installed 12.4.1 in 2 s, after
which the shim works.

Deliver:

1. `scripts/update-agent-assets.sh` `build_understand_anything_core`: when
   `mise` is available, ALWAYS run pnpm as `mise exec npm:pnpm -- pnpm …` (it
   installs the pinned version on demand and never depends on shim state);
   use a bare `pnpm` from PATH only when `mise` is absent; keep WARN-never-fail.
2. `Makefile` `update` target: add `npm:pnpm` to the explicit
   `mise install --locked npm:ccstatusline npm:ccusage` line so the shim is
   backed after every `make update` (same pattern, no new mechanism).
3. Tests (`tests/unit/test_update_agent_assets_ua_core.py`, mutation baseline
   against the unmodified origin/main script): (a) with a fake `mise` and a fake
   `pnpm` shim that exits 1 printing `mise ERROR No version is set for shim: pnpm`,
   the build goes through `mise exec npm:pnpm -- pnpm` and succeeds; (b) without
   `mise`, PATH pnpm is used; (c) a Makefile test (existing pattern in
   `tests/unit/`, e.g. the test that asserts the `update` recipe lines, or a new
   small one) that the `update` recipe installs `npm:pnpm`.
4. README: adjust the one sentence if it names the mechanism.

[memory:decision] T33g: the Understand-Anything core build always invokes pnpm
through `mise exec npm:pnpm` when mise exists (shim presence is not tool
presence), and `make update` installs `npm:pnpm` explicitly, so a fresh pin is
usable on the same run (operator 2026-09-28, from the T33f live-verification
failure).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c fix/ua-core-build-shim origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `scripts/update-agent-assets.sh`
- `Makefile` (the `update` recipe's mise install line only)
- `tests/unit/test_update_agent_assets_ua_core.py` and one Makefile-recipe test file if needed
- `README.md`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ua-core-build-shim-T33g-a01.md` (main checkout)

## Forbidden actions

- Running the real `update-agent-assets.sh`, `make update`, `make upgrade`,
  `mise install`/`mise exec`, `pnpm`, or any network install on the host (fake
  CLIs only); touching the Claude plugin cache, mise pins, model_profiles,
  permgate, hooks configs, `reviews/ADH_Integrated_Plan/`; merging; force push;
  local bats; `make apply`/`chezmoi apply`; writes outside the worktree except
  the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
shellcheck -x scripts/update-agent-assets.sh
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
   Live verification (`make update` on this host with the pin uninstalled and
   dist moved aside) is orchestrator-side at acceptance.
