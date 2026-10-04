# Validation: dotfiles-T89-add-worker-same-workspace-a01

- **task_rev:**
  - Dispatched: `sha256:ba6a86a4…0426`.
  - After PONG decision 1: `sha256:1cbabe9557e18a97fe32c473a3226cee661905c200b442223df3a356696a7977`.
  - `sha256sum` of the task file in the main checkout matched each one when it arrived.
- **Branch:** `feat/add-worker-same-workspace` from `origin/main` a575b3cc.
- **PR:** #239, https://github.com/mryfmo/dotfiles/pull/239.
- **Commits:**
  - `55d7e77c`: the change.
  - `37cf5e47`: full-mode repair skips added-worker panes; self-named test fixture.
  - `958468ba`: Codex P2, keep a tab that holds another running agent.
  - `672f720e`: `gh pr update-branch` merge of `main` 523fda06.
- **Final head:** `672f720e8238134000b205181830af445b82f982`.

## Validation commands (verbatim, on the final head)

The unit tests ran in the Claude sandbox. Its pid namespace hides the host's `crit _serve` processes, which otherwise fail two existing regime-boundary tests; see the T64 report.

```
$ git log -1 --format=%H
672f720e8238134000b205181830af445b82f982
$ git diff origin/main --stat
 README.md                                          |  21 ++-
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   2 +-
 home/dot_local/bin/common/executable_herdr-agents  |  67 ++++++-
 scripts/check-regime-boundary.sh                   |  30 ++-
 tests/unit/test_herdr_agents.py                    | 204 +++++++++++++++++++++
 5 files changed, 301 insertions(+), 23 deletions(-)
$ uv run python -m unittest tests.unit.test_herdr_agents 2>&1 | tail -3
Ran 225 tests in 130.840s

OK (skipped=1)
$ make unit-test (tail -3)
Ran 722 tests in 162.976s

OK (skipped=2)
$ mise x shfmt -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_herdr-agents scripts/check-regime-boundary.sh; shellcheck home/dot_local/bin/common/executable_herdr-agents scripts/check-regime-boundary.sh
shfmt exit=0
shellcheck exit=0
$ mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md
Checking formatting...
All matched files use Prettier code style!
$ herdr-agents --help | sed -n '/add-worker/,/remove-worker/p'   (branch copy: bash home/dot_local/bin/common/executable_herdr-agents --help)
       herdr-agents --add-worker <worktree> [--kind codex|claude] [--profile NAME] [--ready-timeout SECONDS] [DIR]
       herdr-agents --remove-worker <worktree> [--force] [DIR]
$ (prose) ... --help | sed -n '/^Add-worker mode/,/unless --force/p'
Add-worker mode seats an extra resident worker for <worktree> (a path under
DIR/.claude/worktrees/, created from origin/main when missing) in its own tab
of the pair workspace for DIR (labeled <team>:<name>; the pair tab is left
untouched), or in its own workspace when DIR has no pair workspace, through
upstream agmsg spawn.sh, with the profile's launch args;
a pane-less caller gets HERDR_SOCKET_PATH derived from the default Herdr server
socket ~/.config/herdr/herdr.sock (the path the Claude sandbox allowlists), a claude worker's workspace-trust dialog is accepted while spawn.sh
waits, and --ready-timeout bounds that wait (spawn.sh default 90 seconds);
remove-worker mode despawns it, turns its delivery off, leaves its team, and
closes that tab (or that workspace), refusing a dirty worktree unless --force.
```

The `--help | sed -n '/add-worker/,/remove-worker/p'` range prints only the two usage lines, because the range ends at the first `remove-worker` match. The prose lines are printed separately above.

## New tests fail against the code they guard

```
$ (launcher and boundary script from origin/main) uv run python -m unittest -k tab_in_the_pair -k tab_of_the_pair -k seat_tab -k its_tab tests.unit.test_herdr_agents
ERROR: test_remove_worker_closes_only_its_tab_in_the_pair_workspace
FAIL: test_add_worker_reuses_a_seat_tab_in_the_pair_workspace
FAIL: test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace
FAIL: test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace
Ran 4 tests in 1.446s
FAILED (failures=3, errors=1)
$ (launcher from 55d7e77c) uv run python -m unittest -k added_worker_pane -k added_claude_worker tests.unit.test_herdr_agents
FAIL: test_full_mode_heal_never_starts_the_worker_in_an_exited_added_worker_pane
FAIL: test_full_mode_heals_the_orchestrator_beside_a_live_added_claude_worker
Ran 2 tests in 0.173s
FAILED (failures=2)
$ (launcher from 37cf5e47) uv run python -m unittest -k another_running_agent tests.unit.test_herdr_agents
FAIL: test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent
Ran 1 test in 0.105s
FAILED (failures=1)
```

(Each run swapped only the named file, then restored it. All pass on the final head.)

## Live, read-only evidence

The upstream herdr driver placement for `--window` (from `~/.agents/skills/agmsg/scripts/drivers/terminals/herdr/ops.sh`, `terminal_spawn`) is `herdr tab create --workspace "$HERDR_WORKSPACE_ID" --label "$label" --cwd "$project"`, followed by `pane rename "$pane" "$label"`. The label is `_herdr_label "$AGMSG_SPAWN_TEAM" "$name"`, that is `<team>:<name>`. spawn.sh `launch_in_herdr` downgrades `--window` to a split only when `HERDR_WORKSPACE_ID` is unset.

Live workspaces (`herdr workspace list`, read-only). The live pair keeps its own label, so the pair is found by its orchestrator seat label, not by `<repo> agents`:

```
wT	dotfiles
wY	dotfiles worker worker-d
wZ	dotfiles worker worker-e
```

The environment of today's spawn-seated workers (`/proc/<pid>/environ`, read-only). `workspace create --env` never reached their `--window` tab, so a pair-workspace tab behaves the same:

```
4127157 /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-d claude | HERDR_PANE_ID=wY:p2 HERDR_WORKSPACE_ID=wY
4144333 /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-e claude | HERDR_PANE_ID=wZ:p2 HERDR_WORKSPACE_ID=wZ
(no AGMSG_RESOLVE_PROJECT, AGMSG_CC_MONITOR_KEEP_ALIVE or HERDR_AGENTS_LAYOUT in either)
```

The branch's `scripts/check-regime-boundary.sh --report` against the live state, filtered to the Herdr lines. It reports the two legacy workspaces and no false positive for the pair wT, whose worker runs in the manifest worktree:

```
regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
regime-boundary: additional worker workspace still open: dotfiles worker worker-e (herdr-agents --remove-worker)
```

## Codex review

| Head | Result |
|---|---|
| `37cf5e47` | 1 P2 "Preserve nonempty unlabeled panes before closing a worker tab" (comment 4175474967), fixed in `958468ba` |
| `958468ba` | 👍 2026-10-04T00:15:19Z, no inline finding |
| `672f720e` (final, the merge of main) | 👍 2026-10-04T00:22:24Z, no inline finding |

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T89 (operator 2026-10-04): parallel workers are seated as panes inside the pair'"'"'s Herdr workspace; `herdr-agents --add-worker` creates a labelled pane there and `--remove-worker` closes it; one workspace per repository.'
9c11dc0f-9fff-4d47-9018-f870a5398948
```

## CI, mergeable_state and branch (final head `672f720e`)

```
$ gh pr checks 239
nix	skipping
test (ubuntu-24.04, server)	pass
test (macos-14, client)	pass
test (ubuntu-24.04, client)	pass
public-bootstrap (macos-14, client)	pass
CodeRabbit	pass
changes	pass
public-bootstrap (ubuntu-24.04, client)	pass
private-bootstrap (macos-14, client)	pass
private-bootstrap (ubuntu-24.04, client)	pass
public-bootstrap (ubuntu-24.04, server)	pass
private-bootstrap (ubuntu-24.04, server)	pass
test (ubuntu-26.04, client)	pass
validate	pass
$ gh api repos/mryfmo/dotfiles/pulls/239 --jq '.mergeable_state'
blocked
$ gh api repos/mryfmo/dotfiles/compare/main...feat/add-worker-same-workspace
behind_by=0 ahead_by=4
```

`blocked` is only the one unresolved Codex P2 thread (4175474967, fixed in `958468ba`), which is left for the orchestrator to resolve.

## make validate-agent-assets (run in the main checkout, which is on main, not the PR head)

```
$ make validate-agent-assets; echo exit=$?
exit=0
uv run --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: crit review server still running (pgrep -f 'crit _serve')
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-e (herdr-agents --remove-worker)
agent asset validation ok
(untracked .orchestration WARN lines omitted; the boundary commit is the orchestrator's)
```
