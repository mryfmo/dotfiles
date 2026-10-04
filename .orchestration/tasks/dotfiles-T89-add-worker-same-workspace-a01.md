# AGMSG-TASK dotfiles-T89-add-worker-same-workspace-a01

Drafted 2026-10-04 by the orchestrator seat from the operator instruction 「並列化は同じ spaces 内で行うべき」: parallel workers are seated as panes inside the pair's Herdr workspace, not as one workspace per worker. Dispatch condition: dotfiles-T64 merged (same file `executable_herdr-agents`); before T67 if the operator keeps this priority.

## Objective

Today `herdr-agents --add-worker <worktree>` seats each extra worker in its own Herdr workspace (upstream `spawn.sh --project <worktree> --terminal-driver herdr` opened wY and wZ for worker-d/worker-e while the pair lives in wT). Change the launcher so that an added worker becomes a new pane in the pair workspace of DIR (the workspace that holds the orchestrator pane and the pair worker pane, found the way `--attach`/`--restart-worker` find it), labelled `<team>:<identity>` like the pair panes, arranged with the existing panes; `--remove-worker` closes that pane (not a workspace) after despawn/delivery-off/leave; the audit tab stays as is.

1. `home/dot_local/bin/common/executable_herdr-agents`: `--add-worker` resolves the managed pair workspace for DIR (exit 2 with the full-mode hint when none exists, as other pair modes do); seats the worker through the upstream spawn path with the herdr terminal driver targeting that workspace/pane (read `~/.agents/skills/agmsg/scripts/spawn.sh --help` and `drivers/terminals/herdr/README.md` for the supported placement options; if the driver can only open a window, create the pane with the launcher's existing pane-creation helper and pass the pane to the driver, the way the pair worker pane is created; never call raw `herdr` topology commands outside the launcher's helpers); writes the placement record so `poke.sh`/`despawn.sh` keep working; prints the same `linkage=` line. `--remove-worker` closes the pane it created and leaves the workspace open. Keep `--add-worker` for the pane-less on-demand case unchanged in behaviour where no workspace exists (it must still exit 2 with the hint, per the SKILL).
2. `scripts/check-regime-boundary.sh`: the "additional worker workspace still open" check (~101-114) becomes "additional worker pane still open in the pair workspace" (or is dropped if the pane check is already covered by the seat-identity checks; say which).
3. Tests: `tests/unit/test_herdr_agents.py` add-worker/remove-worker cases (fake herdr records the pane creation in the pair workspace and the close), `tests/unit/test_regime_boundary*.py` if the check changes.
4. Docs: README `--add-worker`/`--remove-worker` paragraphs and `SKILL.md` "Parallel workers" section (one sentence each: panes in the pair workspace). Do not touch rule files (T88).
5. Live migration note for the operator (report only): the two workers currently in wY/wZ (a006, a007) are re-seated by `herdr-agents --remove-worker <worktree>` then `--add-worker <worktree>` after `make update`, at a task boundary.

[memory:decision] dotfiles-T89 (operator 2026-10-04): parallel workers are seated as panes inside the pair's Herdr workspace; `herdr-agents --add-worker` creates a labelled pane there and `--remove-worker` closes it; one workspace per repository.

## Repo / branch

- Work ONLY in your own worktree (worker-c for a005). `git fetch origin`; `git switch -c feat/add-worker-same-workspace origin/main` (a575b3cc or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`, `scripts/check-regime-boundary.sh`
- `tests/unit/test_herdr_agents.py`, `tests/unit/test_regime_boundary*.py`
- `README.md` (the add/remove-worker paragraphs), `home/dot_agents/skills/agmsg-orchestration/SKILL.md` ("Parallel workers" section)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T89-add-worker-same-workspace-a01.md` (main checkout)

## Forbidden actions

- Raw `herdr` topology commands against the live workspace (the live migration is the operator's, after merge); changes to upstream agmsg scripts under `~/.agents`; rule files; the audit lane; `make update`/`make apply`; local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
uv run python -m unittest tests.unit.test_herdr_agents 2>&1 | tail -3
make unit-test
make validate-agent-assets
mise x shfmt -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_herdr-agents scripts/check-regime-boundary.sh; shellcheck home/dot_local/bin/common/executable_herdr-agents scripts/check-regime-boundary.sh
mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md
herdr-agents --help | sed -n '/add-worker/,/remove-worker/p'
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

Live acceptance (orchestrator, after merge and the operator's `make update`): `herdr-agents --add-worker .claude/worktrees/worker-d` seats a006's replacement as a pane in wT with `linkage=ok … pong=yes`; `team.sh dotfiles` shows its placement in wT; `herdr-agents --remove-worker` closes only that pane.

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot review of that head; fix P0/P1 inline findings and repeat; close your crit server if Plan Mode opened one; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=40.

## PONG decision 1 (2026-10-03T23:42Z)

- q1: **(A)**. With no pair workspace for DIR, `--add-worker` keeps today's behaviour (its own workspace; the pane-less bring-up in SKILL.md:22 stays valid). With a pair workspace present, the worker is seated inside it. Item 1's "exit 2 with the full-mode hint" is withdrawn.
- q2: **separate tab per worker inside the pair workspace** (`spawn.sh --window` with `HERDR_WORKSPACE_ID=<pair>`), not a split under the pair worker pane. Reason: it satisfies the operator's "same workspace" with zero changes to the pair-tab guards (`--restart-worker`, attach/full repair, `has_claude_pane`/`empty_pane_id`), so the pair seats stay unambiguous. Label the tab/pane `<team>:<name>`; keep the placement record; `--remove-worker` closes that tab. If the herdr driver cannot target a workspace for `--window`, report what it supports before falling back to the split design.
