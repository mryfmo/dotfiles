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
workspace created by `herdr-agents ~/Workspace/dotfiles` (full
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

## Resume review (2026-10-01, RESULT msg 606, head 9eb3e43 after merging main)

Re-dispatched 09:12Z (msg 602, `note=resume-from-branch`, same task file plus
its amendments). Worker merged origin/main (T47/T49 herdr-agents changes) and
pushed 0a35010 (XDG isolation for socket tests, composite-id wording),
dfdfbe8 (trust-dialog watcher `return 0` — the audit of e6f350b found the
`set -e` exit before `wait`; orchestrator confirmed in the code and noted it
matches the 2026-09-29 "did not signal ready" shape), 9eb3e43 (macOS AF_UNIX
path-length test fix). Full PR read from git objects: `print_plain_start_summary`
(one line, worker placement via `team.sh --json`), hook redirects only stderr
so stdout reaches the SessionStart context, `--add-worker` derives
`HERDR_SOCKET_PATH`, accepts the spawned worker's trust dialog during the
readiness wait, takes `--ready-timeout`, and reports spawn.sh's exit code.
Audits: e6f350b incorrect (stdout→log fixed by 89e95e4; watcher status fixed
by dfdfbe8), 89e95e4, 0a35010, dfdfbe8, 9eb3e43 correct. 660 tests OK; CI
green Linux+macOS; CLEAN. PR #216 sweep (16 items): one valid Codex P2 — the
derived socket honours `XDG_CONFIG_HOME` while the sandbox allowlists only
`~/.config/herdr/herdr.sock` → **REVISE** (allowlisted path only; test uses a
short fake HOME). Remaining 15 items not-applicable.

## Resume round 2 and acceptance (2026-10-01, RESULT msg 608, head 51f8bc7)

51f8bc7 read from git objects: `--add-worker` derives only
`${HOME}/.config/herdr/herdr.sock` (herdr's default and the one socket the
managed Claude sandbox allowlists; `XDG_CONFIG_HOME` no longer honoured, with
the reason in a comment), README/SKILL/usage name the allowlisted path, the
macOS AF_UNIX test uses a short fake HOME. Audit of 51f8bc7: **correct**. CI
green Linux+macOS; CLEAN. PR #216 sweep on 51f8bc7 (16 items): the Codex P2 →
fixed:51f8bc7; 15 non-review items not-applicable.

Audit ledger (6 non-merge commits): e6f350b incorrect (stdout→log fixed by
89e95e4; trust-dialog watcher status fixed by dfdfbe8); 89e95e4, 0a35010,
dfdfbe8, 9eb3e43, 51f8bc7 correct.

Behaviour accepted: a plain-shell Claude start never exits the SessionStart
hook silently (one-line state + on-demand commands + seated worker); the hook's
stdout reaches the session context; `--add-worker` works from a pane-less
caller (socket derivation, trust-dialog acceptance during the readiness wait,
`--ready-timeout`, spawn.sh exit code reported). Residual, documented: a
sandboxed pane-less session has no Monitor watch; RESULTs arrive by turn
delivery (T49 composite-lock rule applies to the pane-less claim too).

Orchestrator failures of the original 2026-09-29 session stay recorded above
and are codified by T46 (next task). CompactionDB: the worker's T45 decision
stands.

cost: worker ~? (original session) + resume rounds (session counters; no per-task figure)

**Decision: ACCEPTED.** Merge PR #216 (squash, no `--delete-branch`); T46 is
dispatched next.
