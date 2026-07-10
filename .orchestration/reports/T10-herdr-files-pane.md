# T10 Herdr Files Pane Report

## Status

ready_for_review

`make require-crit-review` confirmed that native agent review is required. The
orchestrator must perform that review because the task does not allow an
additional repo-local Crit JSON/receipt path.

## Changes

- Added the optional auto-refreshing `eza` icon file-list pane.
- Fresh workspaces now split the Claude root pane with ratio `0.8` before starting Codex, producing the verified Claude/Codex/files ordering.
- Existing workspaces missing the files pane split the Codex pane with ratio `0.6`.
- Claude repair excludes panes labeled `files`, preventing the files pane from being reused as an agent pane.
- Added fresh, repair, idempotency, and Ghostty/agmsg call-order coverage with incrementing fake split pane ids.
- Updated the Herdr agents reference summary with the three-pane layout and soft `eza` requirement.

## Scope

- `docs/reference/home/dot_local/bin/common/executable_herdr-session.md` was unchanged because it does not describe a two-pane layout.
- No dependency, CI, hook, permission, or deployed-home changes were made.
- No git, chezmoi, bats, network, LLM, or live Herdr mutation actions were run.
