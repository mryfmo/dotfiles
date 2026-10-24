# U44 The program's done predicate, measured on the real artifact; the clean-up table refreshed — brief

GOAL
The program's frame (decisions 2026-10-23T01:05:00Z, row 2) names a countable done predicate: twelve units verified; the final check on the real artifact: three omp seats on hcom, one TASK to RESULT to verdict round trip, a claude-bridge turn and an openai-siwc turn, pstack listed, zero Claude Code or Codex seats. This unit measures each clause on this host today, writes the result into `overview.md` with the evidence lines, and refreshes the operator's clean-up table (`handouts/cleanup-table.md`) with everything the day added, so the operator's G8 run is one pass.

SCOPE
One branch `records/program-close-out` from `origin/main` (3da0e299 or later). May write: `.orchestration/orchestrate/regime-cutover/overview.md` (a "Done predicate, measured" section), `.orchestration/orchestrate/regime-cutover/handouts/cleanup-table.md` (rows added, none removed), `.orchestration/orchestrate/regime-cutover/handouts/U1-operator-steps.md` only to mark steps now obsolete. Records only: the PR is records-only (every path under `.orchestration/`), so the regime check passes without a Program-Unit line, and the CI test jobs skip.

CHANGE
1. Measure each clause with one command and paste its output: `HCOM_DIR=~/.local/state/hcom-regime hcom list -v` (seats, their tool and directory), `bus-history.sh regime --kind TASK --limit 1`, `--kind RESULT --limit 1`, `--kind VERDICT --limit 1` (or the `AGMSG-` forms where older rows are the latest), the model routes of the three profiles (`grep -n model ~/.agents/omp/profiles/{orchestrator,worker,audit}.yml`), `pstack` presence (`command -v pstack` or the manifest entry), and the Claude Code and Codex seat count from `hcom list -v` (`tool:` field). The twelve-units count comes from `units.tsv` `state=landed` rows (`awk -F'\t' '$3=="landed"' units.tsv | wc -l`).
2. For each clause write `met` or `not met` with the pasted line; a `not met` names the unit that closes it or the operator step.
3. Clean-up table: add PR #500 (superseded by #501, close), the `~/.local/state/hcom/kit-pilot` store and `~/.local/state/omp-seats/kit-pilot/` seats root (the U33 pilot's scratch artefacts; their checkout under `$TMPDIR` is gone), the stopped seat worktrees that no longer have a branch to keep (`git worktree list` against open PR branches), and the `handouts/U1-operator-steps.md` steps now obsolete; each row with the exact command and the reason, none executed by you.
4. Residuals index: one list in `overview.md` of the residual rows the day left open with their owners (U41's `uninstall_*` functions with no caller; U38b's inherited rows; the `.ua` index refresh; the one-time store move of README "Run a program in another repository"; the operator's Ubuntu handout steps 2 to 9).

ACCEPTANCE
1. Every clause has a pasted measurement line from this host; nothing is asserted from memory.
2. The clean-up table's new rows carry commands the operator can run as written; the table says what each removes and why it is safe.
3. CI green (the records-only path: regime `no target (records-only)`), PR body `Program-Unit: regime-cutover/U44` is not needed but harmless; pre-RESULT five-point self-check (threat table: records only, say so); orchestrator verdict.

TIMEBOX
45 minutes.

FORBIDDEN
No command that changes host state (no kill, no rm, no close, no launch); measurements only; no omp subagent; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 24).
