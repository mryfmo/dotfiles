# T29 result report

- Task: `T29-agmsg-regime-default-on`
- Worktree: `/Users/mryfmo/Workspace/dotfiles-t29`
- Branch: `docs/agmsg-regime-default-on`
- Commit: `ee39911 docs(rules): make agmsg orchestration default-on`
- Changed only `home/dot_config/claude/rules/agmsg-orchestration.md`, first bullet only.
- The bullet makes the regime default-on when the bus and resident worker exist, declares agmsg always-on, preserves the orchestrator role, and limits direct mutation to an explicit current-task opt-out.
- Acceptance revision applied: replaced the comma-spliced `, and act only as orchestrator:` seam with `; act only as orchestrator:`.
- PR #98 revision applied: restored the explicit operator-request trigger alongside the default-on availability trigger.
- Initial commit `3314a97` and revisions `ab1c000`/`ee39911` were made without pushing. The orchestrator then authorized the push of `ab1c000`, followed by an authorized `--force-with-lease` push of `ee39911` for the PR-review fix.
- No chezmoi apply, live Herdr mutation, dependency/CI change, local Bats, or LLM call was performed.

Acceptance review and the final Crit gate remain orchestrator-side under the configured role split.
