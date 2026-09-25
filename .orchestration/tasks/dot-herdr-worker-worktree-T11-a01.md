# AGMSG-TASK dot-herdr-worker-worktree-T11-a01 (revision 2): give the same-cwd herdr worker its own agmsg identity through the actas flow (plan part B1)

Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/melodic-conjuring-sifakis.md` §B1.
Repo (your worktree): `/home/moriya/Workspace/dotfiles/.claude/worktrees/env-converge-T10`, branch `fix/herdr-agents-worker-actas` created with `git switch -c fix/herdr-agents-worker-actas origin/main` once the T13 branch is pushed and the tree is clean. You are `claude-standard-dot-a003`.

## Design constraints (from the repository's own definitions — read them first)

- README.md "herdr-agents" section: the managed layout is exactly two panes, `claude-orchestrator` left and `<worker_kind>-worker-${workspace_id}` right, **both in the same project cwd**; parallelism never adds panes to this workspace — one extra worktree equals one extra resident worker in its own tab/workspace (`herdr pane split ... --cwd <worktree>` + `herdr agent start`). Keep this design. Do not move the default worker out of the project cwd.
- agmsg identity resolves by (project path, agent type) (`whoami.sh` → `identities.sh`). When two same-type agents share one project path, agmsg's defined mechanism is the **actas flow**: `join.sh` the second identity on the same (project, type), `actas-claim.sh <project> <type> <name> <session_id>` from that session, and `watch.sh <session_id> <project> <type> <name>` narrowed to the claimed name (see `actas-claim.sh` and `watch.sh` headers). `whoami.sh` prints `multiple=true agents=...` when more than one identity is registered; the actas claim disambiguates per session.
- `worker_kind=claude` (the manifest default) is exactly the same-type case. Today `herdr-agents` neither registers a worker identity nor claims it, and `bootstrap_agmsg()` treats a second identity on the path as "ambiguous". Result on 2026-09-25: worker and orchestrator both resolved to `claude-remediation-dot`; the worker had to be addressed by a worktree-registered identity and told to read that inbox explicitly, and it once ran `git switch` in the orchestrator's checkout.

## Required changes

1. **Worker identity registration.** In `herdr-agents`, when starting or repairing the worker pane, ensure an identity `<worker_kind>-<worker_profile>-<suffix>` (e.g. `claude-standard-dot`; derive `<suffix>` exactly as the existing identities do — find where `-dot` comes from and reuse it) is registered on `(workdir, <worker agent type>)` via `join.sh <team> <name> <type> <workdir>`, where `<team>` is the team the orchestrator identity belongs to (from `identities.sh workdir claude-code`). Do not register anything under `$HOME`.
2. **Claim per session.** Pass the worker identity to the worker pane so its session claims it: for a claude worker, export `HERDR_AGENTS_AGMSG_IDENTITY=<name>` into the pane env (`herdr pane split --env`), and make the agmsg `session-start.sh` hook (`~/.agents/skills/agmsg/scripts/session-start.sh`, invoked from `.claude/settings.local.json` by `delivery.sh set both`) honour that variable: when set, run `actas-claim.sh <project> <type> <name> <session_id>` and start `watch.sh ... <name>` narrowed to it; when unset, keep today's behaviour. The orchestrator pane keeps its identity by the same rule (either it also claims, or the unclaimed remainder resolves to it — decide, document, and test both panes). If `session-start.sh` lives outside this repo's managed files, stop and report `blocked` with the exact path and owner; do not edit unmanaged files.
3. **Codex worker.** For `worker_kind=codex` the types differ, so no collision exists; keep behaviour unchanged but register the worker identity the same way for consistency (report if that changes any existing test expectation).
4. **bootstrap_agmsg.** Replace the "multiple identities → ambiguous" rule with: one orchestrator identity plus one worker identity on the path is healthy when the worker identity matches the `<worker_kind>-<profile>-<suffix>` pattern; anything else keeps the warning. Update the wording of the printed hints accordingly.
5. **Docs.** README herdr-agents section (identity paragraph: how the two panes get distinct agmsg identities, and that same-cwd is still the design), `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (Identity section: name the herdr-agents automation), and `home/dot_agents/README.md` policy line if one covers identities. shdoc English comments for new/changed functions.

## Tests (red → green, evidence verbatim)

- `tests/unit/test_herdr_agents.py`: worker identity name derivation for claude and codex; `join.sh` called with `(team, name, type, workdir)`; `--env HERDR_AGENTS_AGMSG_IDENTITY=` present on the worker pane split; bootstrap accepts orchestrator+worker pair and still warns on a third name. Follow the file's existing fake-herdr style.
- The bats file that covers herdr-agents/agmsg bootstrap: one case for the accepted pair. No local bats.
- `uv run --with pyyaml scripts/validate-agent-assets.py` passes (this is how CI invokes it).

## Live E2E (required; verbatim)

Scratch repo under the scratchpad with a bare `origin`, run the modified `herdr-agents <dir>` from your worktree with `HERDR_AGENTS_WORKER_KIND=claude` and express-profile args (`MODEL_PROFILE_EXPRESS_CLAUDE_ARGS`; never ad-hoc `--model`). Show for a fresh session and for `--attach` on a restored session: `identities.sh <dir> claude-code` lists exactly the orchestrator and worker names; `whoami.sh <dir> claude-code` prints `multiple=true` (expected) while each pane's own `watch.sh`/claim resolves to its own name (show the claim `status=ok` lines from both panes' logs); a message sent to the worker name is read by the worker pane and not by the orchestrator pane. Teardown: `delivery.sh set off`, `leave.sh` for both scratch identities, close the scratch workspace, remove scratch dirs; `identities.sh <dir> claude-code` returns nothing. Do not touch the live `wE` workspace or the `dotfiles` team.

## Commit / PR

`fix(herdr-agents): register and claim a distinct agmsg identity for the same-cwd worker` (+ docs/test commits as needed). Push `fix/herdr-agents-worker-actas`, PR in English (problem, the actas design, E2E evidence; end with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`), `gh pr checks --watch`, final table verbatim.

## allowed_files

`home/dot_local/bin/common/executable_herdr-agents`, the agmsg `session-start.sh` **only if it is a file managed in this repository** (name it), `tests/unit/test_herdr_agents.py`, the bats file you name, `README.md`, `home/dot_agents/README.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, and the five artefact files.

## forbidden_actions

moving the default worker pane out of the project cwd; creating sibling worktrees; editing files outside the repository; merging the PR; `make update`; `chezmoi apply`; touching the live `wE` workspace or `dotfiles` team registrations; local bats; force-push; ad-hoc `--model` flags.

## Artefacts (in `/home/moriya/Workspace/dotfiles`)

report `.orchestration/reports/dot-herdr-worker-worktree-T11-a01.md` (per-function decisions, E2E table, PR URL, `[memory:decision]`: "same-cwd herdr worker gets a distinct agmsg identity via join + actas-claim in its own session; layout stays two panes in one cwd"), validation, sandbox, learning, autoskill (same basename). `contextdb_cli.py memory add` from the main checkout; paste command and output.

## Done signal

`AGMSG-RESULT v1 task_id=dot-herdr-worker-worktree-T11-a01 status=ready_for_review|blocked pr=<n> report=... validation=... sandbox=... learning=... autoskill=...` via `send.sh dotfiles claude-standard-dot-a003 claude-remediation-dot "<message>"`. max_turns=40.

## SUPERSEDED (2026-09-25)

Never dispatched. Replaced by the remediation plan `.agents/worklog/claude/remediation-plan-20260925.md` Phase 3 (upstream agmsg role/seat model, all four kind combinations) and Phase 1.3 (temporary same-type guard, task dot-worker-kind-guard-T14-a01).
