# E2E leg: Claude orchestrator → codex worker (Linux)

Evidence-only leg (dotfiles-T87), recorded by the orchestrator seat `claude-remediation-dot` from the live regime of 2026-10-05 in the pair workspace wT. No seat exchange was needed: the worker of this leg is seated in the same workspace.

- `uname -s`: `Linux`
- Unattended `make update` (chezmoi source clone at 794a80db → ee0fd641, 2026-10-05 ~06:10Z and ~08:50Z): exit 0; password prompts in the log: 0 (ponytail hook-trust divergence warnings only, T82b follow-up).
- `make doctor` (09:17Z): exit 0; `Doctor summary: tools=passed; runtime=passed`; `Tool check summary: required failures: 0; optional warnings: 1` (the optional `latest-version` probe hit the GitHub rate limit).
- Worker seat: `codex-security-dot-a007` (type codex) registered at `~/Workspace/dotfiles/.claude/worktrees/worker-e`, pane `wT:p8`, delivery `turn`; orchestrator `claude-remediation-dot` at the main checkout, pane wT:p1, delivery both (`team.sh dotfiles --json`).
- Tasks driven through this seat today: dotfiles-T81b (#275 → 794a80db), dotfiles-T99 (#277 → 64167825), dotfiles-T100 (#278 → 94409ec4); each RESULT was received by turn delivery / `agmsg-dispatch` wake and answered with an `AGMSG-ACCEPTANCE`.
- `messages.db` rows (dispatch read by the worker, RESULT/PONG read by the orchestrator; `read_at` non-null):

```
1414 | claude-remediation-dot → codex-security-dot-a007 | AGMSG-TASK v1 task_id=dotfiles-T100 repo=~/Workspace/dotfiles task_fi | created 2026-10-05T06:47:34Z | read 2026-10-05T06:48:40Z
1417 | codex-security-dot-a007 → claude-remediation-dot | AGMSG-PONG v1 task_id=dotfiles-T100 status=active task_rev=verified branch=docs/ | created 2026-10-05T06:49:35Z | read 2026-10-05T06:49:43Z
1435 | codex-security-dot-a007 → claude-remediation-dot | AGMSG-RESULT v1 task_id=dotfiles-T100 status=done pr=278 head=bc001fc74e672b599d | created 2026-10-05T07:17:01Z | read 2026-10-05T07:17:46Z
```

- `make check-regime-boundary`: recorded at session end (see the closing line below).

regime-boundary check at session end (2026-10-05 10:18Z, after `herdr-agents --remove-worker` for worker-d and worker-e): `make check-regime-boundary` printed 28 `untracked .orchestration file` lines, all of them the pending evidence of this boundary (committed by the fourth boundary PR of the day), and no seat, identity, worker-tab or Crit-server line; the orchestrator seat lock holds the composite id.

## Leg 2 (Codex CompactionDB rows), 2026-10-05 18:20Z — verified after the T82b deploy

Preconditions: PR #284 (T82b) merged as 815177f3 and deployed with `make update` (17:52Z); Codex app-server `hooks/list` reports the `pre_compact`, `post_compact` and `session_end` config hooks `trusted` with hashes equal to `[hooks.state]` (see the T82b acceptance record). No operator `/hooks` step was needed: the modify scripts wrote the trust at apply time.

Attempts that did not produce compaction rows (recorded for completeness): the seated Codex worker `codex-standard-dot-a006` cannot run its own `/compact` (no self-TUI command tool; PONG 1799), and the orchestrator's `herdr pane run wT:pC '/compact'` (prompt injection, 18:14Z) left only `turn_stop` row 709 in the worker-e DB with no `pre_compact`/`post_compact` rows; whether the TUI compacted is unconfirmed (PONG 1803: no `/compact` user message visible to the agent).

Deterministic form, run by the orchestrator from the main checkout root (headless, express profile, auto-compaction forced by a low limit):

```
codex --profile express exec --sandbox read-only -c model_auto_compact_token_limit=6000 -C ~/Workspace/dotfiles -o <scratch>/codex-compact-leg2.last.md 'Read README.md in full with the shell (cat README.md), then read AGENTS.md in full, then reply with one sentence naming how many lines each file has.'
rc=0; tokens used 18,013; the transcript ends with "hook: Stop Completed"
```

Rows ingested by `contextdb-codex-notify` into the main checkout's `.claude/contextdb/state/context.db` (`select id, event_type, session_id, ingested_from from events where id>15393 and ingested_from='codex' order by id`):

```
15394|session_end|01a10d34-cd76-7830-b33a-6cf3ae168716|codex
15414|pre_compact|01a10d49-536c-74c3-8694-9a13665e9bed|codex
15415|post_compact|01a10d49-536c-74c3-8694-9a13665e9bed|codex
15416|session_end|01a10d49-536c-74c3-8694-9a13665e9bed|codex
```

Rows 15394 (17:55Z, the T82b live check) and 15416 are `session_end`; 15414/15415 are the `pre_compact`/`post_compact` pair of one session with a non-empty session id. New `unknown` rows after id 15393: 0. Leg 2: passed on Linux.
