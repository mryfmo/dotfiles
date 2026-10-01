# Learning: dot-orchestrator-delivery-sandbox-T49-a01

1. **Claude Code exports `CLAUDE_CODE_SESSION_ID` and `CLAUDE_PID` to every subprocess,
   hooks included.** Inside a pane's own hook the composite agmsg instance id is simply
   `${CLAUDE_CODE_SESSION_ID}.${CLAUDE_PID}`. From another process, herdr gives the same two
   values through `agent list` (`agent_session.value`) and `pane process-info --pane`
   (foreground `claude` pid). Applies to any launcher that has to address a claude seat.
   Status: validated (the probe output agrees on both routes).
2. **`AGMSG_SELF_NAME=off`** is upstream's switch for running an agmsg seat command on behalf of
   another pane without renaming the caller's pane. Every launcher-side join or claim should set
   it. Status: observation.
3. **Test helpers that copy `os.environ` must drop the runner's agent session variables**
   (`CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID`). `make unit-test` runs inside a Claude session
   and would otherwise resolve against it, unlike CI. Status: candidate learning.

No rule or skill was promoted beyond the task's own SKILL and rule bullets.

## Revision 2 triage

1. **`excludedCommands` is not a permission grant.** Per the Claude Code settings reference, an
   excluded command runs outside the sandbox but "still goes through permission prompts unless a
   rule allows it". It matches on the first word. A prompt-free unsandboxed command needs both
   `sandbox.excludedCommands` and a `permissions.allow` rule. Status: validated from the
   docs; candidate for the sandbox manifest comment convention.
2. **Hook processes do not inherit the Bash tool's injected variables.** `CLAUDE_CODE_SESSION_ID`
   and `CLAUDE_PID` are set for Bash-tool shells, not on the claude process itself. Hooks must
   read `session_id` from the stdin payload and find the pid by walking the parents. This corrects
   T49 r1 learning 1. Status: observation (orchestrator's `/proc/<pid>/environ` evidence).
3. **Bounded stdin reads in shipped shell must not assume GNU coreutils.** `timeout` is absent on macOS, so a guarded `timeout 2 cat` silently skipped the read there. bash's `read -r -t N -d ''` gives the same bound. Status: validated (macOS CI).
4. **An upstream all-or-nothing multi-team claim needs a per-team repair loop.** One release followed by one retry only covers the first held team. Status: observation.

## Revisions 2-d to 2-f triage

1. **Only a dead pid makes a same-session lock stale.** Parallel `--resume`/`--continue` processes share a session id, so "same sid" never means "our predecessor" without a liveness check. Status: observation.
2. **Check liveness with `ps -p`, not by parsing `kill -0` text.** The message is locale-dependent (this host is Japanese), and `ps -p` also treats another user's process as alive. Status: validated (tests on Linux and macOS CI).

## Revisions 3 and 3-b triage

1. **A bounded read needs an overall deadline, not a per-read timeout.** A byte-wise `read -t` resets the timeout on every byte, so use `SECONDS`-based deadlines for hook stdin. Status: validated (trickle test).
2. **A hook that runs in every pane must check the pane's role before acting on a shared identity.** Status: observation.

## Revision 3-c triage

1. **Liveness for a lock owner means "the expected program is running", not just "the pid exists".** Pids are recycled, so check `ps -o comm=` (basename; macOS prints the path). Status: validated (tests on both OSes).
2. `shutil.copy2` of a macOS system binary fails on its file flags; test fixtures should use `shutil.copyfile` and `chmod`. Status: validated (macOS CI).
