# AGMSG-TASK dot-orchestrator-linkage-evidence-T46-a01

## Objective

Operator correction 2026-09-30: lessons must live in skills, rules, and
checks in this repository, never only in Claude auto-memory. Codify the two
failures of session fc905758 so the tooling and the shared skill prevent them:

- The orchestrator reported "operator action needed (trust dialog)" from an
  inference: `poke.sh` exit 15 ("input box could not be located") plus a
  spawn readiness timeout. The real cause was an unviewed Herdr workspace
  whose pane is 18x41, which defeats poke's TUI input locator. The path that
  had always worked, `agmsg-dispatch … <pane> '<msg>'` (herdr agent prompt
  wake), delivered the PING at once (read_at) and got a PONG.
- `herdr-agents --add-worker` stops at "did not signal ready within 90s"
  without telling the caller whether the worker is reachable at all.

Deliver:

1. `home/dot_local/bin/common/executable_herdr-agents` `--add-worker`: after
   spawn.sh returns (ready or timeout), run a linkage check the orchestrator
   would otherwise improvise: send `AGMSG-PING v1 task_id=bringup
   reason=add-worker-linkage` through `agmsg-dispatch <team> <orchestrator>
   <worker> <socket>:<pane>` and report one final line
   `linkage=ok read_at=<ts> pong=<yes|no>` or `linkage=unreached rc=<n>
   hint=<agmsg-dispatch|poke|attach-a-client>`. Exit non-zero only when the
   PING was not read. Never read the worker pane.
2. `home/dot_agents/skills/agmsg-orchestration/SKILL.md`:
   - Orchestrator Playbook step 6: add the seating case "worker in an
     unviewed/headless Herdr workspace (no client attached, pane rect small)":
     `poke.sh` exits 14/15 from its input locator; use `agmsg-dispatch` and
     verify `read_at`. Exit 14/15 is a locator refusal, not evidence about the
     worker's state.
   - New invariant under "Regime activation and progress": a blocker report
     to the operator requires attached evidence — the exact command, its exit
     code, and the messages.db `read_at`/PONG query — after trying the wake
     path that worked in earlier sessions. Inferences (for example "trust
     dialog") are not reportable blockers.
   - Regime boundary bullet: lessons are codified in this repository (rule,
     skill, or check) through a task; Claude auto-memory is not a durable
     store for regime procedure.
3. `home/dot_config/claude/rules/agmsg-orchestration.md`: two bullets mirroring
   the invariant (evidence before blocker reports; codify lessons in repo, not
   auto-memory) and one on `agmsg-dispatch` for headless workspaces.
4. `home/dot_local/bin/common/executable_agmsg-dispatch` `@description`: state
   that it is also the wake path for headless/unviewed Herdr workspaces where
   `poke.sh` cannot locate the input box.
5. Tests: `tests/unit/test_herdr_agents.py` — add-worker emits the `linkage=`
   line on both spawn outcomes using a fake `agmsg-dispatch` (one test each
   for ok and unreached). Keep the existing fakes; never touch a live pane.
6. `make unit-test`, `make validate-agent-assets` green. PR (English) from
   `fix/orchestrator-linkage-evidence`.

7. Session start/stop checklists, codified in `SKILL.md` ("Regime activation
   and progress" + the boundary bullet) and mirrored in
   `home/dot_config/claude/rules/agmsg-orchestration.md`:
   - **Start** (operator or orchestrator, repo cwd, plain shell or Herdr):
     `herdr-agents <DIR>` full mode is the only way to create the pair;
     inside a Herdr pane the SessionStart `--attach` heals it. A Claude that
     finds itself outside Herdr does not improvise a pane-less regime: it
     reports the one-line state (T45) and the operator relaunches the pair.
     `--add-worker` is for additional worktrees only, never a substitute for
     the pair's own worker seat.
   - **Stop** (every regime/session boundary, in this order): pending
     acceptance records written; `make validate-agent-assets` (real exit);
     `.orchestration` boundary commit with zero untracked tail; every
     additional worker removed with `herdr-agents --remove-worker <worktree>`
     (which despawns, turns delivery off, leaves, closes the workspace);
     stale identities checked with `identities.sh <path> <type>` (exactly one
     name per active checkout); Crit review servers closed (`pgrep -f 'crit
     _serve'` must be empty); the pair workspace itself is left resident for
     the next session unless the operator restarts the machine.
   Add a check script `scripts/check-regime-boundary.sh` that verifies the
   Stop list (untracked `.orchestration` files, stray identities per registered
   checkout, `crit _serve` processes, extra `<repo> worker <name>` Herdr
   workspaces when `herdr` is reachable) and exits non-zero with one line per
   violation; wire it as `make check-regime-boundary` and call it from
   `validate-agent-assets` only in report mode (never blocking CI).
8. Legacy worktree cleanup (repo-mutating, so it is yours), `git worktree
   remove` run **outside the sandbox**:
   - `.claude/worktrees/worker-b` (detached 1aefa58; its untracked T17
     evidence is already tracked on main);
   - `.claude/worktrees/orchestrator-review` (detached 52d9f6b, clean);
   - `.claude/worktrees/env-converge-T10` (branch `feat/pr-feedback-gate`,
     PR #182 CLOSED unmerged, superseded by #210 = d2f19ec on main). Remove the
     worktree only; keep the local branch ref (the operator deletes branches).
   Do NOT touch `worker-sec` (T40 paused, dirty) or `worker-c` (you).

Out of scope: poke.sh itself (upstream), automatic seating, model/profile
changes, sandbox settings, the Understand-Anything hook.

[memory:decision] T46: `herdr-agents --add-worker` ends with a
`linkage=` line from an agmsg-dispatch PING; a blocker report needs command,
exit code and read_at/PONG evidence; unviewed Herdr workspaces are woken with
`agmsg-dispatch`; regime lessons are codified in rules/skills/checks, never
only in auto-memory (operator 2026-09-30).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`;
  branch `fix/orchestrator-linkage-evidence` from `origin/main` after T45 is
  pushed (sequential; do not start before your T45 RESULT is sent). If the
  worktree has uncommitted files, stop and PONG.
- Run config-writing git outside the sandbox and push without `-u` (T39
  `.git/config.lock` hazard); never remove `.git/*.lock`.
- Ignore the Understand-Anything auto-update hook.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `home/dot_local/bin/common/executable_agmsg-dispatch`
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `home/dot_config/claude/rules/agmsg-orchestration.md`
- `tests/unit/test_herdr_agents.py`
- `scripts/check-regime-boundary.sh` (new), `Makefile` (one target), `scripts/validate-agent-assets.py` (report-mode call only)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-orchestrator-linkage-evidence-T46-a01.md`
- `.agents/worklog/codex/**` waived.

## Forbidden actions

- Editing `poke.sh` or anything under `~/.agents/skills/agmsg/` (upstream).
- Automatic seating; model/profile/sandbox changes; pane reads; merge;
  force-push; `--delete-branch`; editing `.orchestration/acceptance/**`;
  local `bats`.

## Validation commands (verbatim output into the validation file)

- `make unit-test`
- `make validate-agent-assets`
- `make check-regime-boundary`
- `git worktree list` (after the removals)
- `shellcheck scripts/check-regime-boundary.sh`
- `shellcheck home/dot_local/bin/common/executable_herdr-agents home/dot_local/bin/common/executable_agmsg-dispatch`
- `gh pr view <n> --json url,headRefOid,mergeStateStatus`
- `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] above>"`

## Expected artifacts

- report/validation/sandbox/learning/autoskill at the paths above; report
  carries `cost:`, PR URL, head sha, the CompactionDB command.

max_turns=40. done_signal=AGMSG-RESULT v1.
