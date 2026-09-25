# AGMSG-TASK dot-agmsg-dispatch-T4-a01 — one-shot orchestrator dispatch: send + wake + verify

## Root cause (established this session)

Codex turn-mode delivery (`.codex/hooks.json` Stop hook → `check-inbox.sh`) runs only when a Codex turn ENDS, with a 60 s cooldown. A message sent to an idle worker (after it returned its RESULT and its turn ended) is therefore never delivered until something starts a new turn. Three times this session the worker sat idle 5–15 min on unread ACCEPTANCE/TASK messages until a manual `herdr pane run` nudge. The agmsg-orchestration skill already states the invariant ("after every wake verify read_at"), but nothing enforces it.

## Required outcome

Add `home/dot_local/bin/common/executable_agmsg-dispatch` (bash, shdoc comments, shfmt/shellcheck clean):

```
agmsg-dispatch <team> <from> <to> <pane_id> <message...>
```

1. `send.sh <team> <from> <to> "<message>"` and capture the new message id (query `messages.db`: max id for that team/to/from after send, or parse send.sh output if it prints the id).
2. If `herdr pane list` reports the pane's `agent_status` != `working`, run `herdr pane run <pane_id> "agmsg: new message <id> for <to> — run ~/.agents/skills/agmsg/scripts/inbox.sh <to>"`.
3. Poll `read_at` for that id every 5 s up to `AGMSG_DISPATCH_TIMEOUT` (default 120 s). Exit 0 when read; if still unread and the pane was idle, wake ONCE more, poll again; exit 1 with a clear message otherwise. Never print message bodies to stderr/logs.
4. Honor `AGMSG_STORAGE_PATH` exactly like send.sh does (do not hardcode the db path; source the same lib the scripts use).

Ponytail: one script, no new deps (bash, sqlite3, jq, herdr already present). Reuse `~/.agents/skills/agmsg/scripts/lib` helpers for db path.

Tests: `tests/unit/test_agmsg_dispatch.py` (stdlib unittest, like `test_herdr_agents.py`): fake `herdr`, fake `send.sh`, temp sqlite db with the real `messages` schema; cases: (a) idle pane → wake called once, read → exit 0; (b) working pane → no wake, read → exit 0; (c) never read → exit 1 after timeout (use a 1 s timeout env). Red-first.

Docs: one paragraph in `home/dot_agents/skills/agmsg-orchestration/SKILL.md` Orchestrator Playbook step 6 saying orchestrators send with `agmsg-dispatch` (and regenerate if that skill is rendered by `scripts/generate-agent-configs.py`; run the asset validator).

## allowed_files

`home/dot_local/bin/common/executable_agmsg-dispatch`, `tests/unit/test_agmsg_dispatch.py`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (+ its generated copies if any), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-agmsg-dispatch-T4-a01.md`.

## forbidden_actions

no git commit; no push; no PR; no local bats; no chezmoi apply / make update on operator HOME; no edits to agmsg skill scripts under `~/.agents/skills/agmsg` (they are an external asset).

## Worktree

New worktree `.claude/worktrees/agmsg-dispatch` from `origin/main`, branch `feat/agmsg-dispatch`.

## Validation (verbatim)

`make unit-test`; `shellcheck` + `shfmt -i 4 -sr -d` on the new script; `uv run --with pyyaml python scripts/validate-agent-assets.py`; `git diff --check`.

## Durable facts

- [memory:decision] Orchestrators dispatch to Codex workers with `agmsg-dispatch`, which sends, wakes an idle pane, and blocks until `read_at` is set; a bare `send.sh` to an idle worker is a protocol violation.

max_turns=30. Reply with `AGMSG-RESULT v1`.
