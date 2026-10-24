# O3 omp-first operation: the orchestrator seat is the entry point — kickoff for the orchestrator seat

The operator's direction (2026-10-24T06:3xZ): stop using the Claude Code session as the instruction-giver; start from omp and keep developing. From this kickoff on you are the only coordinator. The operator types instructions into your pane; the Claude Code session no longer sends TASKs or addenda. Everything below is yours to do without asking anyone.

STEP 0, make the seats whole and keep them whole
- `hcom list -v`. Expected seats: `worker-<word>` (U31, PR #488 in flight), `worker-2-<word>` (U30, PR #487 in flight), `audit-<word>`. Launch any missing role yourself with `scripts/orchestrator/hcom-seat <role> [--name <name>]` from this checkout (your policy allows it; `HCOM_DIR` and `HCOM_TEAM` are in your environment). A worker whose seat died keeps its branch in its worktree; relaunch it with the same `--name` and re-send its TASK with `note=resume from your branch`.
- Never spawn an omp subagent (the Task tool): your predecessor died that way on the claude-bridge route (decisions row 2026-10-24T06:1xZ). Read with your own tools.
- When a seat stops answering for 20 minutes while its TASK is open, read its pane (`hcom term <name> --clean`), then relaunch it as above.

STEP 1, resume the loop from the store
Read, never recall: `units.tsv`, `ledger.tsv`, `decisions.tsv`, `gates.md`, `preferences.md` (lines 20 and 21), and the briefs `O2-orchestrator-run-U17-U18-U25d-U30-U28.md`, `O2-addendum-2.md`, `O2-addendum-4.md`, `O2-addendum-5.md`, `O2-resume.md`, and the three addenda inside `U30-seat-text-hygiene.md`. The order stands: lane A U31 → U33 → its pilot in a second repository; lane B U30 → U28 → U32 → U26 → U27; U21 at its gate; U22, U23, U24, U19 after. U34 (deny the `task` tool in the orchestrator and worker overlays) merges into U36 below.

STEP 2, encode omp-first operation as unit U36 (brief `briefs/U36-omp-first-operation.md`, written by the coordinator; dispatch it to the first free worker before U32)
It makes this kickoff the standing mode: the skill's step 0, the `task: deny` rows, the operator's "start here" section, and a supervisor that relaunches you when you die.

STEP 3, the first-pass gate and the merge rule
Apply U30's addenda now, before U30 lands: findings hand-off through `verdicts/U<n>-<head>.md`, the five-point pre-audit gate at RESULT, re-read the PR state after any merge error and never merge one head twice.

REPORT
One `AGMSG-PONG v1 task_id=O3 status=progress note=<unit> landed <sha>` per landed unit on the thread, and the same line in your pane for the operator. The thread is also where the operator's Claude Code session, if it is still open, reads; it will not answer.
