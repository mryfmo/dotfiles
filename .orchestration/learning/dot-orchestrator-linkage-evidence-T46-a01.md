# Learning: dot-orchestrator-linkage-evidence-T46-a01

1. **Look before removing a worktree.** A cleanup instruction written from a branch's PR state
   ("closed, superseded") can miss uncommitted work in the worktree. `git status` plus a
   byte-compare against main before `git worktree remove` caught 59 lines of unique WIP here.
   Status: observation (now part of the report's evidence pattern).
2. **A WIP commit on a branch whose remote moved on cannot be pushed without force.** Push it
   to a new branch name instead and leave the original remote branch untouched. Status:
   observation (operator-approved resolution).
3. **When two accepted rules conflict, ask before writing.** The T46 Start checklist draft
   contradicted the merged T45 bullet; one PONG turned it into a reconciled checklist that
   cross-references T45. Status: observation.
4. **A check that imports another script's function** (`spec_from_file_location`) keeps one
   implementation. Set `sys.dont_write_bytecode` so it leaves no `__pycache__` behind. Status:
   observation.

No rule or skill was promoted beyond the task's own SKILL and rule changes.
5. **`team.sh --json` is not a passive lookup for Codex members.** In agmsg 1.5.0 it observes
   them through `terminal_peek` → `herdr pane read`. Read the spawn placement record
   (`run/spawn.<team>__<name>`) instead. **Follow-up candidate:** the merged T45 plain-start
   summary (`print_plain_start_summary`) still calls `team.sh --json` for the seated worker's
   placement and should switch to the record too. It is out of T46's scope (the r2 amendment says
   so) and noted here for a task. Status: candidate.
6. **Correlate replies by message id, not by body pattern alone.** A `task_id=bringup` PONG from an
   earlier session matched the first implementation. Status: validated (test).

## Revisions 3 and 3-b triage

7. **Resolve upstream state through upstream resolvers, and keep their refusals.** A legacy fallback that swallows the resolver's refusal reintroduces the ambiguity the resolver exists to stop. Fall back only when the resolver itself is unavailable. Status: validated (tests).
8. **`if ! cmd; then rc=$?` captures the negated status (0).** Capture with `cmd || rc=$?` and then test rc; the new test caught this before commit. Status: validated.

## Revisions 4 and 4-b triage

9. **Validate before using in shell arithmetic, and force base 10.** Under `set -u`, a non-numeric value aborts the shell, and a leading zero is octal (`08` errors). Here the error even escaped the add-worker block into the full-mode path. Use `^[0-9]+$` and then `10#${value}`. Status: validated (tests).
10. **Where an identity is required, require exactly one; never take `head -n 1`.** Status: observation.

## Revision 5 triage

11. **Make every probe message unique per invocation** (a nonce task_id) and match replies on it. A row-id order alone cannot reject a late reply to an earlier probe. Status: validated (test).
12. **A cached locator (placement record) must be checked against the current context (workspace) before use.** Status: validated (test).
13. **A boundary check over checkouts must cover every worktree, and must tell seats (must be non-empty) from tooling worktrees (exempt).** Status: validated (tests).

## Revision 6 triage

14. **A name or label is not an identity.** Match Herdr workspaces by label *and* the location of their panes (cwd under the checkout), as `find_managed_workspaces` already does. Status: validated (test).

## Revision 7 triage

15. **A seat holds one identity, not one per runtime.** Count names across every runtime type at an active seat. Per-type counts let a claude-code + codex pair pass. Status: validated (test).
16. **A record is a claim; the live list is the fact.** Check a retained placement record's pane against the current `pane list` before dispatching to it. Status: validated (test).
17. **The script's checkout is not the repository's main checkout.** Pass the main checkout to every repo-scoped probe, and use the script's own root only to locate code. Status: validated (test).

## Revision 8 triage

18. **"Present" is not "mine".** A retained record's pane must be both live and new to this invocation (absent from the pre-spawn list). On failure, print the exact command, its exit code and the query that would verify delivery, and never swallow the tool's own stderr. Status: validated (test).

## Revision 9 triage

19. **A documented command must run as written.** Copy a recovery command's argument list from the tool's usage, including the required message argument, and drop a documented call when the code dropped it for a stated reason. Status: validated (auditor reproduction; doc fixed).
