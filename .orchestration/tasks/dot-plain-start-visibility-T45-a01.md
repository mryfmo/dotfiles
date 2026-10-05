# AGMSG-TASK dot-plain-start-visibility-T45-a01

## Objective

Operator finding 2026-09-30: a Claude Code session started in the repository
root from a plain shell (`mosh-server → zsh → claude`, no Herdr pane) gets no
worker, and nothing says why. Root cause is ambiguity in our own launch path,
not a broken environment (applied `home/` matches the canonical clone; Herdr
server up; hooks wired):

- `home/dot_local/bin/common/executable_herdr-agents` `--attach` exits 0
  silently when `HERDR_ENV`/`HERDR_PANE_ID`/`HERDR_WORKSPACE_ID` are unset
  (line ~1281), and the SessionStart hook definition
  (`home/dot_agents/agent-config.yaml`, matcher `"*"`) discards all output
  (`>> ~/.config/herdr/herdr-agents.log 2>&1 || true`).
- `herdr-agents --add-worker` from a pane-less orchestrator: (a) creates the
  worker workspace, then spawn fails with `herdr: HERDR_SOCKET_PATH is unset`
  (partial state: an empty workspace `dotfiles worker worker-c`, wP);
  (b) with `HERDR_SOCKET_PATH` exported it seats the worker but never calls
  `accept_claude_workspace_trust_dialog`, so a first-start claude worker sits
  on the workspace-trust dialog, spawn readiness times out at 90 s and
  `poke.sh` exits 15.

Operator decision: **no automatic seating**. The orchestrator starts the
worker and the auditor on demand and verifies linkage before delegating.
SessionStart must always say what state it found and what the next command is.

Deliver:

1. `executable_herdr-agents` `--attach` outside Herdr (the three variables
   unset): remove the silent `exit 0`. Print exactly one stdout line that
   states: not in a Herdr pane, pair not started, the on-demand commands
   (`herdr-agents --add-worker <worker_worktree> [DIR]` for the worker,
   headless `codex --profile audit review --commit <sha>` for the auditor),
   and, when a placement record exists for the identity registered at
   `worker_worktree`, that worker's name and `<socket>:<pane>` location.
   No side effects (no workspace, no spawn). Keep the quiet `exit 0` for the
   worktree-seated worker's own SessionStart (cwd == worker_worktree). The
   same single line for non-interactive runs (`claude -p`) and express E2E
   subjects.
2. `--add-worker` from a pane-less caller: when `HERDR_SOCKET_PATH` is unset,
   derive it (the herdr config/default socket path; refuse with a clear
   message if it cannot be found) **before** creating the workspace, so no
   partial workspace is left; export it for spawn.sh. After spawn returns,
   call `accept_claude_workspace_trust_dialog` on the spawned pane for a
   claude worker (pane id from the placement record or spawn output), the way
   pair mode does at line ~676. Make the readiness timeout a documented
   `--ready-timeout` passthrough (default unchanged).
3. Hook definition in `agent-config.yaml`: keep the log redirect for stderr,
   but let the one stdout summary line reach the SessionStart context (do not
   discard stdout); keep `|| true`. Regenerate
   `home/.chezmoitemplates/claude-settings-managed.json` with
   `uv run --with pyyaml scripts/generate-agent-configs.py`; `--check` green.
4. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` "Regime activation":
   add the pane-less orchestrator bring-up: `actas-claim.sh`, `herdr-agents
   --add-worker <worktree>`, verify `team.sh <team> --json` placement
   `run/spawn.*`, send `AGMSG-PING` via `poke.sh --body-file`, and dispatch no
   task before the `PONG`; auditor is headless when no pair workspace exists;
   Monitor is unavailable from a sandboxed pane-less session (pid namespace),
   so RESULTs arrive by turn delivery. README "Herdr and Ghostty agent
   workspace": one paragraph on plain-shell (mosh/ssh) starts with the same
   content.
5. Tests: `tests/unit/test_herdr_agents.py` — replace
   `test_attach_noops_without_herdr_environment` with (a) summary line
   printed, no herdr/spawn calls; (b) summary includes the seated worker when
   a placement record exists; add (c) add-worker derives the socket path and
   refuses before workspace creation when it cannot; (d) add-worker calls the
   trust-dialog helper for a claude worker (fake `herdr`/`spawn.sh` CLIs; never
   a live pane). `tests/unit/test_claude_settings_merge.py` pins the hook
   command string — update it.
6. `make unit-test`, `make validate-agent-assets` green. Open a PR (English
   title/description) from `fix/plain-start-visibility`.

Out of scope: automatic seating, `worker_kind`/`worker_profile`/model
changes, sandbox settings, the Understand-Anything hook (ignore it), the
`.git/config.lock` stub (separate task).

[memory:decision] T45: a Claude started in the repo root outside Herdr is a
pane-less orchestrator. SessionStart never exits silently: it prints one line
with the state and the on-demand commands. Workers are seated on demand with
`herdr-agents --add-worker` (which derives `HERDR_SOCKET_PATH` and accepts the
claude trust dialog), the auditor runs headless, and linkage is verified with
`AGMSG-PING`/`PONG` before any task is dispatched (operator 2026-09-30).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`;
  branch `fix/plain-start-visibility` from `origin/main` (the worktree
  currently holds `fix/sandbox-unix-sockets` at c2c1f62, PR #215, unmerged —
  leave that branch intact; switch, do not reset). If the worktree has
  uncommitted files, stop and PONG.
- Ignore the Understand-Anything auto-update hook during this task.
- Run config-writing git (`switch -c`, `push`) outside the sandbox and push
  without `-u` (T39 `.git/config.lock` hazard); never remove `.git/*.lock`.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `home/dot_agents/agent-config.yaml`
- `home/.chezmoitemplates/claude-settings-managed.json` (generated)
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `README.md`
- `tests/unit/test_herdr_agents.py`
- `tests/unit/test_claude_settings_merge.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-plain-start-visibility-T45-a01.md`
- `.agents/worklog/codex/**` is waived for this task.

## Forbidden actions

- Any automatic worker seating from SessionStart.
- Changing `worker_kind`, `worker_profile`, model profiles, or sandbox settings.
- Reading other agents' panes (`pane read`/`wait-output` on a pane you did not create in a test fake).
- Merging, force-push, `--delete-branch`, editing `.orchestration/acceptance/**`.
- Running `bats` locally (CI only).

## Validation commands (paste verbatim output into the validation file)

- `make unit-test`
- `make validate-agent-assets`
- `UV_CACHE_DIR=$TMPDIR/uv-cache uv run --with pyyaml scripts/generate-agent-configs.py --check`
- `bash home/dot_local/bin/common/executable_herdr-agents --attach` with the
  three HERDR variables unset (prints the one line, exits 0, no side effects)
- `gh pr view <n> --json url,headRefOid,mergeStateStatus` after push
- `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] above>"`

## Expected artifacts

- report: `.orchestration/reports/dot-plain-start-visibility-T45-a01.md`
  (include `cost:` line, PR URL, head sha, the CompactionDB command run)
- validation: `.orchestration/validation/dot-plain-start-visibility-T45-a01.md`
- sandbox: `.orchestration/sandboxes/dot-plain-start-visibility-T45-a01.md`
- learning: `.orchestration/learning/dot-plain-start-visibility-T45-a01.md`
- autoskill: `.orchestration/autoskill/runs/dot-plain-start-visibility-T45-a01.md` (not-used record is fine)

max_turns=40. done_signal=AGMSG-RESULT v1.

## Orchestrator amendment (2026-09-29T23:37Z, msg to worker; task_rev of the dispatched file unchanged for verification)

- Premise correction: the `herdr-agents --attach` SessionStart hook is defined
  in `home/dot_claude/modify_private_settings.json:180`, not in
  `agent-config.yaml` / `claude-settings-managed.json`.
- allowed_files += `home/dot_claude/modify_private_settings.json`.
- Deliverable 3: change only that command string so stdout reaches the
  SessionStart context (`2>> "$HOME/.config/herdr/herdr-agents.log" || true`);
  generator regen not needed; `--check` stays in validation; update the pins
  in `tests/unit/test_herdr_agents.py:1290` and
  `tests/unit/test_claude_settings_merge.py`.
- Orchestrator failure noted: allowed_files were not grounded by grep before
  dispatch (playbook step 3).

## Orchestrator amendment, resume round (2026-10-01 09:3xZ; audits of e6f350b / 89e95e4 / 0a35010 — fold into one more commit before the RESULT)

Audit of e6f350b (`…-audit-e6f350b.md`): P2 (the SessionStart hook redirected
stdout to the log) is fixed by 89e95e4; P2 at `accept_spawned_claude_trust_dialog`
is **still at the head**: when spawn.sh exits without a trust dialog, the
`while kill -0 …` loop ends with the status of its last body command
(`accept_claude_workspace_trust_dialog … && return 0` → 1), the function
returns 1, and because it is the last command of the `[[ … ]] || …` list,
`set -e` ends the launcher before `wait "${spawn_pid}"`: a successful spawn is
reported as exit 1 and a real spawn failure loses its exit code and message
(the orchestrator saw exactly this "did not signal ready" shape on 2026-09-29).
Fix: `return 0` after the loop (the dialog is optional), keep `wait` and the
`spawn_rc` reporting; tests: fake spawn exits 0 with no dialog → launcher exit
0 and the "worker added" line; fake spawn exits 3 → launcher exit 3 and the
"spawn.sh exited 3" message. 89e95e4 and 0a35010 audited correct. Then the
RESULT when CI is green on both OSes.

## Orchestrator amendment, resume round 2 (2026-10-01 10:1xZ; dispatched as AGMSG-ACCEPTANCE status=revise)

Head 9eb3e43 reviewed from git objects (summary line, hook stdout → context,
`--add-worker` socket derivation, trust-dialog watcher with `return 0`,
`--ready-timeout`); audits: e6f350b incorrect (both P2s fixed by 89e95e4 and
dfdfbe8), 89e95e4 / 0a35010 / dfdfbe8 / 9eb3e43 correct; 660 tests; CI green
on both OSes. One Codex GitHub comment on 9eb3e43 is valid (P2 `:1638`): the
derived socket honours `XDG_CONFIG_HOME`, but the managed Claude sandbox
allowlists only `~/.config/herdr/herdr.sock` (`claude-settings-managed.json`
`allowUnixSockets`), so on macOS with `XDG_CONFIG_HOME` set the existence
check passes and the later herdr calls are denied. Fix in one commit: derive
only the allowlisted path `${HOME}/.config/herdr/herdr.sock` (drop the XDG
branch; herdr's own default is that path), and keep the macOS AF_UNIX test
under the path limit with a short fake `HOME` (`/tmp/ha-*`) instead of
`XDG_CONFIG_HOME`; state in the README/SKILL sentence that the derived socket
is the allowlisted default path. Then the RESULT when CI is green on both OSes.
