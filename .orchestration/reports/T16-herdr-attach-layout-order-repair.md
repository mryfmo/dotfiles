# T16 worker report

## Status

Ready for review on branch `feat/herdr-attach-order-repair`.

## Revision

Addressed `AGMSG-ACCEPTANCE status=revise` for workspace-vs-tab scope:

- Derive the current `tab_id` from `HERDR_PANE_ID` in workspace pane-list JSON.
- Filter pane accounting to that tab before Codex lookup, ambiguity checks,
  files-pane ensure, and order repair.
- Preserve whole-refusal semantics for unmanaged panes on the current tab while
  ignoring unrelated panes on other tabs.
- Added a regression test proving a second-tab extra pane does not block rename,
  Yazi ensure, or the expected swaps on the Claude tab and is never touched.

Addressed the follow-up `AGMSG-ACCEPTANCE status=revise` for real Herdr stdout:

- Updated the fake `pane rename` command to emit realistic `pane_info` JSON.
- Reproduced command-substitution pollution in the existing restarted-Codex
  regression test before the fix.
- Silenced only `start_codex_agent`'s rename stdout so the function returns
  exactly one pane id. This fixes attach mode and the pre-existing full-mode
  existing-workspace capture path at the shared root.

## Changes

- Added a tab-scoped attach-mode ambiguity guard before any pane mutation.
  Unknown same-tab panes, duplicate same-tab `files` panes, and pane identities
  that cannot be mapped to the current Claude pane plus the registered Codex
  pane now print a clear stderr warning and exit 0.
- Added attach-mode order repair after the existing files/Codex ensure steps.
  It refreshes the pane list, reads `result.layout.panes[].rect.x`, and performs
  at most two source/target swaps to reach `claude | codex | files`.
- Added unit tests for `files | claude | codex`, already-correct order, and
  duplicate-files ambiguity.
- Kept the early attach no-op paths and full mode unchanged.

## Read-only Herdr evidence

`herdr pane layout` exposed the required x-order fields:

```json
{"id":"cli:pane:layout","result":{"layout":{"area":{"height":44,"width":172,"x":26,"y":1},"focused_pane_id":"w13:p2","panes":[{"focused":false,"pane_id":"w13:p8","rect":{"height":44,"width":86,"x":26,"y":1}},{"focused":false,"pane_id":"w13:pA","rect":{"height":44,"width":43,"x":112,"y":1}},{"focused":true,"pane_id":"w13:p2","rect":{"height":44,"width":43,"x":155,"y":1}}],"splits":[{"direction":"right","id":"split_0_root","ratio":0.5,"rect":{"height":44,"width":172,"x":26,"y":1}},{"direction":"right","id":"split_1_1","ratio":0.5,"rect":{"height":44,"width":86,"x":112,"y":1}}],"tab_id":"w13:t1","workspace_id":"w13","zoomed":false},"type":"pane_layout"}}
```

`herdr pane` advertised the deterministic swap form:

```text
herdr pane swap --source-pane ID --target-pane ID
```

## Deliberate scope

Ratio repair was skipped. The observed layout describes nested split ratios,
while `pane resize` accepts only a pane, direction, and amount. There is not
enough documented correspondence to compute a safe 40/40/20 mutation without
experimenting against the live session, which this task forbids.

No live Herdr mutation, chezmoi apply, dependency/CI change, LLM call, commit,
or push was performed.

`make require-crit-review` was run and correctly requested review, but its
scope included the pre-existing dirty worktree (80 files / 6373 lines), not
only T16. This worker cannot create Crit evidence outside `allowed_files`; the
handoff status is therefore `ready_for_review` for the orchestrator.
