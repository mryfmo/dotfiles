# AGMSG-TASK dot-orchestrator-delivery-sandbox-T49-a01

## Objective

Operator correction 2026-10-01: the orchestrator must receive worker
messages without being prompted. In session e7734322 (Herdr pair wN,
Claude Code 2.1.284 with the T39 sandbox active) both delivery paths were dead
and the orchestrator found every RESULT (msgs 546–564) by reading
`messages.db` directly. Root causes, verified in that session:

1. **Monitor path.** The SessionStart directive starts
   `watch.sh <sid>.<pid> <repo> claude-code` through the Monitor tool, which
   runs the command inside the Bash sandbox. The sandbox has its own pid
   namespace (4 processes visible; the shell is pid 2), so `kill -0 <claude pid>`
   fails with ESRCH and `agmsg_instance_alive` reports the session dead;
   `watch.sh` exits at once with "session … is no longer alive; stopping". The
   stale pidfiles it leaves hold the namespace pid `4`.
2. **Turn path.** `actas-claim.sh … <sid>` run from sandboxed Bash cannot
   resolve the claude pid ("instance-id falling back to bare session_id") and
   writes the **bare** sid as the lock owner. The Stop hook
   (`check-inbox.sh`, run by Claude Code outside the sandbox) normalises the
   payload's `session_id` to the **composite** `<sid>.<pid>`, so
   `actas_lock_state` returns `other:<bare sid>` and the hook exits 97 silently:
   it ran at every turn end (the `.lastcheck-<agent>` marker was touched) and
   delivered nothing. Re-creating the lock with the composite id made the same
   hook deliver the backlog (`decision: block` with 2 messages).

`~/.agents/skills/agmsg/**` is upstream and out of scope. Fix it in this
repository's launcher, docs and checks:

1. `home/dot_local/bin/common/executable_herdr-agents`: when it starts the
   orchestrator pane (full mode and the `--attach` heal), and when the
   SessionStart `--attach` runs inside the pane, claim the orchestrator seat
   **outside any sandbox** with the composite instance id: resolve the claude
   pid of the pane (the `herdr agent start` result / `herdr agent list` session
   mapping, or `pgrep` on the pane's process tree — verify which the real CLI
   offers with a safe command, not `--help` alone) and run
   `actas-claim.sh <repo> claude-code <orchestrator identity> <sid>.<pid>`. If
   the pid cannot be resolved, print one line `seat_claim=unresolved` and do
   not write a bare-sid lock. Print `seat_claim=ok owner=<sid>.<pid>` on success.
2. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` and
   `home/dot_config/claude/rules/agmsg-orchestration.md`: one bullet each —
   the orchestrator seat lock must carry the composite id; a claim from
   sandboxed Bash writes a bare id and makes turn delivery skip silently; the
   check is `lock owner == <sid>.<pid>` (`cat ~/.agents/skills/agmsg/run/actas.<team>__<name>.session`),
   and a `watch.sh` Monitor cannot run under a pid-namespaced sandbox (it exits
   "no longer alive"); until upstream accepts a liveness override, turn
   delivery is the working path and an idle orchestrator is woken by the
   worker's `agmsg-dispatch` to the orchestrator pane, which the worker SKILL
   section must say (RESULT/PONG to a herdr-paned orchestrator go through
   `agmsg-dispatch <team> <worker> <orchestrator> <socket>:<pane>`, not bare
   `send.sh`).
3. `scripts/check-regime-boundary.sh` (T46 creates it; if T46 is not merged
   yet, add the check to `scripts/check-agent-runtime.py` doctor output
   instead): WARN when an orchestrator actas lock for the registered identity
   holds a bare session id (no `.<pid>` suffix) while a live claude session
   exists for that project.
4. Tests: `tests/unit/test_herdr_agents.py` — the pane start emits
   `seat_claim=…` with a fake `actas-claim.sh` capturing the composite id
   (one test ok, one unresolved); doctor/boundary check test for the bare-id
   WARN.
5. `make unit-test`, `make validate-agent-assets` green; PR (English) from
   `fix/orchestrator-delivery-sandbox`.

Out of scope: upstream agmsg (`watch.sh`, `check-inbox.sh`,
`actas-claim.sh`), the Claude Code sandbox manifest (a pid-namespace opt-out
is a T39 follow-up for the operator), model/profile values.

[memory:decision] T49: the orchestrator seat lock must hold the composite
`<sid>.<pid>`; a claim from sandboxed Bash writes a bare sid and the Stop-hook
delivery then skips silently (`other:`), and a `watch.sh` Monitor cannot run
under the pid-namespaced sandbox — herdr-agents claims the seat outside the
sandbox at pane start and a herdr-paned orchestrator is woken by worker
`agmsg-dispatch` (operator correction 2026-10-01).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`,
  sequentially after the task in flight there; branch
  `fix/orchestrator-delivery-sandbox` from `origin/main` (`git fetch` first).
- Sandbox deny-mount stubs are not dirt; explicit-path `git add`; push without
  `-u`; never remove `.git/*.lock`; ignore the Understand-Anything hook.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `home/dot_config/claude/rules/agmsg-orchestration.md`
- `scripts/check-regime-boundary.sh` (if present) or `scripts/check-agent-runtime.py`
- `tests/unit/test_herdr_agents.py`, `tests/unit/test_check_agent_runtime.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-orchestrator-delivery-sandbox-T49-a01.md` (main checkout)
- `.agents/worklog/codex/**` waived.

## Forbidden actions

- Editing anything under `~/.agents/skills/agmsg/`; sandbox settings;
  model/profile values; pane reads; merge; force-push; `--delete-branch`;
  `.orchestration/acceptance/**`; local `bats`; claiming or touching the live
  orchestrator lock (`run/actas.dotfiles__claude-remediation-dot.session`).
- Escalating outside the sandbox/allowlist for approval: fail, PONG blocked
  with the exact command and boundary.

## Validation commands (verbatim output into the validation file)

- `make unit-test`
- `make validate-agent-assets`
- `shellcheck home/dot_local/bin/common/executable_herdr-agents`
- the real-CLI probe you used to resolve the pane's claude pid (safe form)
- `gh pr view <n> --json url,headRefOid,mergeStateStatus`
- `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] above>"`

## Expected artifacts

- report/validation/sandbox/learning/autoskill at the paths above; report
  carries `cost:`, PR URL, head sha, the CompactionDB command.

max_turns=40. done_signal=AGMSG-RESULT v1.
