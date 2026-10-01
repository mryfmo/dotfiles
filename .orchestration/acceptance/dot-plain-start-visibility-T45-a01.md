# Acceptance record: dot-plain-start-visibility-T45-a01 (IN PROGRESS — paused for pair relaunch)

Orchestrator: claude-remediation-dot, session fc905758 (pane-less, `mosh → zsh
→ claude`, outside Herdr). Worker: claude-standard-dot-a005 (claude, profile
standard = opus-5.5 high), spawn-seated at Herdr wP:p2 by
`herdr-agents --add-worker .claude/worktrees/worker-c`.

## Timeline (UTC, 2026-09-29)

- 23:21 add-worker: first run failed (`HERDR_SOCKET_PATH is unset`, empty
  workspace wP left); second run with the socket exported seated a005; spawn
  readiness timed out (unviewed 18x41 pane defeats poke's input locator).
- 23:21:46 PING via `agmsg-dispatch` read 23:22:00; PONG alive (msg 537).
- 23:22:46 AGMSG-TASK dispatched (msg 538, task_rev sha256 83a1612a…).
- 23:23:32 PONG blocked: 19 zero-byte sandbox stubs in worker-c → orchestrator
  go (msg 540): stubs are sandbox artefacts, explicit-path `git add` only.
- 23:35:18 PONG blocked: deliverable 3 premise wrong — the attach hook is in
  `home/dot_claude/modify_private_settings.json:180` → scope extended (msg
  542); orchestrator grounding failure recorded in the task file.
- 23:48 operator ruling: the current form violates the pair rule (worker not
  visible beside the orchestrator). Pause requested (msg 543): commit WIP on
  `fix/plain-start-visibility`, push, RESULT status=blocked
  note=paused-for-pair-relaunch.

## Decision

**PAUSED — not accepted, not rejected.** Resume in the rule-conformant pair
workspace created by `herdr-agents /home/moriya/Workspace/dotfiles` (full
mode). The next orchestrator (pane p1 of that workspace) resumes T45 by:

1. reading the worker's paused report (path in the RESULT message) and
   `git log origin/fix/plain-start-visibility`;
2. dispatching the same task file (unchanged task_rev
   `83a1612a882fe85edb3ada4dbf0e4151192871a647212e9975d5c3d380fbf4cd`, plus
   the amendment section at its end) to the new pair worker seated in
   worker-c, with `note=resume-from-branch`;
3. then T46 (`dot-orchestrator-linkage-evidence-T46-a01.md`) sequentially in
   the same worktree; T43/T44 headless audits when the operator lifts the Codex
   pause; T40 resume via `--add-worker .claude/worktrees/worker-sec --kind
   codex --profile security`.

## Orchestrator failures this session (for T46's codified checklist)

- Started a pane-less regime with `--add-worker` instead of relaunching the
  pair with full mode from the repo cwd.
- Reported a blocker (trust dialog) from inference; the wake path that always
  worked (`agmsg-dispatch`) reached the worker at once.
- Dispatched with ungrounded `allowed_files` (hook location not grepped).
- Wrote a lesson to Claude auto-memory instead of the repository (deleted).

cost: n/a (worker report pending)
