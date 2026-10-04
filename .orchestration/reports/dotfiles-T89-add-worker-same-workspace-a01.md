# Report: dotfiles-T89-add-worker-same-workspace-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `feat/add-worker-same-workspace` from `origin/main` a575b3cc.
- **task_rev:** both dispatched revs matched: `ba6a86a4…`, and `1cbabe95…` after PONG decision 1.
- **PR:** #239, https://github.com/mryfmo/dotfiles/pull/239.
- **Commits:**
  - `55d7e77c`: the change.
  - `37cf5e47`: full-mode guard and test fixture.
  - `958468ba`: Codex P2.
  - `672f720e`: `gh pr update-branch` with `main` 523fda06.
- **Final head:** `672f720e`.
  - **CI:** green; 13 pass including CodeRabbit, and `nix` is skipped.
  - **Branch:** up to date with `main` 523fda06 (behind_by=0).
  - **Codex:** 👍.
  - **`mergeable_state`:** `blocked`, only by the one unresolved Codex P2 thread 4175474967 (fixed in `958468ba`), which is left for the orchestrator.

## 1. What changed (PONG decision 1: q1=A, q2=a separate tab per worker)

- **`--add-worker`:**
  - The setup now also resolves the pair workspace with `load_seat_labels` and `single_managed_workspace "<repo> agents" DIR`. That is the lookup restart, audit and full mode use, and it finds an attach-mode pair through its self-named orchestrator label (the live wT is labelled `dotfiles`).
  - With a pair workspace, the worker is seated through the unchanged upstream path `spawn.sh … --terminal-driver herdr --window` with `HERDR_WORKSPACE_ID=<pair>`. The driver runs `herdr tab create --workspace <pair> --label <team>:<name> --cwd <worktree>` and renames the pane to the same label. The placement record and the `linkage=` line are unchanged, and the pair tab is never touched.
  - "Already seated" now also means a pane labelled `<team>:<name>` with an agent in the pair workspace.
  - Without a pair workspace (the pane-less bring-up, q1=A), it still creates or reuses `<repo> worker <name>`, and no exit 2 is added.
- **`--remove-worker`:**
  - After despawn, delivery off and leave, a new `close_worker_tab` closes the worker's tab in the pair workspace.
  - It closes only a tab whose panes all carry that `<team>:<name>` label, or are unlabelled and agentless (after the Codex P2).
  - It still closes the worker's own legacy workspace when one exists, which is what the live migration of wY and wZ needs.
- **Beyond the PONG premise of "zero pair-tab guard changes" (commit `37cf5e47`):**
  - The attach, restart and layout repairs are filtered to the pair tab and need no change.
  - Full mode's `has_claude_pane` and `empty_pane_id`, however, scan the whole workspace. A live added claude worker in its tab would count as the orchestrator, so a missing orchestrator would not be healed. An exited added worker's pane would be picked as an empty pane and the pair worker started in the added worker's tab.
  - Both helpers now skip a pane with a self-named `<team>:<name>` label whose cwd is a linked worktree under DIR (`added_worker_pane_filter`). The pair seats are normalized to `claude-orchestrator`/`<kind>-worker` first, and the orchestrator's cwd is DIR itself, so neither is skipped.
  - Two tests cover this, and both fail against `55d7e77c`.
- **`check-regime-boundary.sh` (item 2): changed, not dropped.** The seat-identity checks do not cover added workers, which are registered at their own worktrees.
  - The legacy "additional worker workspace still open" check stays, for the own-workspace case.
  - A new check reports "additional worker tab still open in <pair label>: <pane label>" for any pane in the pair workspace whose cwd is a linked worktree other than the manifest `worker_worktree`. The pair workspace is the one with a pane at the main checkout itself, which also catches attach-mode labels.
- **Docs:**
  - The usage text and `@option`.
  - README: the parallel-worker paragraph, the add-worker list, the re-run note and the remove-worker paragraph.
  - SKILL "Parallel workers": one sentence each for add and remove.
  - The README codex spawn-options line also gains the T64 flags (`--ask-for-approval never`, the `network_access=true` `--config` line), which T64 had missed.
- **Tests:** seven new tests (six on the first two commits, one for the P2):
  - pair tab seating, with the linkage PING going to the new pane;
  - reuse of a seated tab;
  - removal closes only its tab;
  - a tab holding another running agent is kept;
  - the boundary tab report;
  - the two full-mode repair cases.
  - Each fails against the code it guards. Totals: 225 herdr-agents tests, `make unit-test` 722 OK.

## 2. Findings and caveats for acceptance

1. **Environment never reached spawn-seated workers.**
   - The running a006 and a007 agents in wY and wZ (`/proc/<pid>/environ`) have none of `AGMSG_RESOLVE_PROJECT`, `AGMSG_CC_MONITOR_KEEP_ALIVE` or `HERDR_AGENTS_LAYOUT`. The `workspace create --env` of the old path set them only for the workspace's root pane, never for the `--window` tab that spawn.sh opened.
   - So tabs in the pair workspace behave the same as before. It also means SKILL's claim that "`spawn.sh --project` sets `AGMSG_RESOLVE_PROJECT=0` for agmsg-spawned seats" covers only spawn's own `join.sh`, not the seated agent's environment.
   - Proposed follow-up: carry these through the spawn path. This is outside the allowed SKILL section.
2. **Untested against live Herdr** (the live acceptance will show):
   - **Empty tab left behind:** I assume Herdr drops a tab when `despawn.sh` closes its only pane. If it does not, `close_worker_tab` finds no labelled pane and an empty tab remains, which the boundary check cannot see because it has no cwd in a worktree.
   - **Concurrent tab creation:** an `--audit` tab created at the same moment as an `--add-worker` could be taken for the new pane by the linkage and trust-dialog pane diff. The placement record path is preferred when the record exists.
3. **Behaviour changes:**
   - `--remove-worker` now exits 2 when `single_managed_workspace` finds duplicate pair workspaces, which it did not consult before.
   - Re-adding after an exited worker opens a second tab, because a stale tab whose agent has exited does not count as seated. This is the same as the old own-workspace flow, but more visible now.
4. **Help output:** the task's `--help | sed -n '/add-worker/,/remove-worker/p'` prints only the two usage lines; the prose is pasted separately in the validation file.
5. **README pane-less paragraph (~555):** it still says the worker's placement is confirmed from `team.sh --json` and the PING is sent with `poke.sh`, while SKILL:22 says the placement record and `agmsg-dispatch`. This is outside the add/remove-worker paragraphs, so it is a proposed follow-up.

## 3. Live migration (item 5, operator, after merge and `make update`, at a task boundary)

For each of `worker-d` (a006, wY) and `worker-e` (a007, wZ):

1. `herdr-agents --remove-worker .claude/worktrees/<worktree>` despawns, turns delivery off and leaves, then closes the legacy workspace through the label lookup. It finds no tab in wT.
2. `herdr-agents --add-worker .claude/worktrees/<worktree>` seats the worker in a new tab of wT labelled `dotfiles:<identity>` and prints `linkage=…`.

Running `--add-worker` first only reports "already seated in workspace wY", because the legacy seat is still live. `make check-regime-boundary` currently reports the two legacy workspaces; after the migration, any added-worker tab still open in wT is reported instead.

## 4. Codex bot

| Head | Result |
|---|---|
| `55d7e77c` | Pushed before the PR existed, so it had no review of its own. |
| `37cf5e47` | P2 "Preserve nonempty unlabeled panes before closing a worker tab", fixed in `958468ba`. The task requires only P0/P1; I fixed this one because the guard prevents destroying a running agent. |
| `958468ba` | 👍 00:15:19Z |
| `672f720e` (final) | 👍 00:22:24Z |

I did not reply to or resolve any thread.

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T89 (operator 2026-10-04): parallel workers are seated as panes inside the pair'"'"'s Herdr workspace; `herdr-agents --add-worker` creates a labelled pane there and `--remove-worker` closes it; one workspace per repository.'
9c11dc0f-9fff-4d47-9018-f870a5398948
```

[memory:decision] dotfiles-T89 (operator 2026-10-04): parallel workers are seated as panes inside the pair's Herdr workspace; `herdr-agents --add-worker` creates a labelled pane there and `--remove-worker` closes it; one workspace per repository.

The decision text is the task's verbatim, so it says "panes". As implemented per PONG decision 1, each pane sits in its own tab of the pair workspace, and `--remove-worker` closes that tab.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T89-add-worker-same-workspace-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T89-add-worker-same-workspace-a01.md`
- learning: `.orchestration/learning/dotfiles-T89-add-worker-same-workspace-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T89-add-worker-same-workspace-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).
