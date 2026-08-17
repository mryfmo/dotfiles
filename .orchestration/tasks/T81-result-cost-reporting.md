# T81: RESULT 契約へのワーカーコスト報告の規約化

task_id: T81
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-pivot.md (Phase 6)
depends: T80 (accepted)

[memory: decision — Workers report observed session token/cost figures in their RESULT report when the runtime exposes them (else state n/a), feeding the ACCEPTANCE cost line adopted in T76 — completing the Pi-derived first-class cost accounting loop across the task lifecycle.]

## Work order (exact)

1. home/dot_agents/skills/agmsg-orchestration/SKILL.md — Worker
   Playbook: add one clause: the report artifact includes a
   `cost:` line with observed session token/cost figures when the
   runtime exposes them, otherwise `cost: n/a`. Keep it to 1–2
   sentences; this is the source feeding the T76 ACCEPTANCE cost line
   (cross-reference it).
2. If T79/T80 relocated the relevant contract text, edit it where it
   now lives (skill side) — do NOT re-grow the slim rule files.
3. Gates: make validate-agent-assets / format / unit-test.

## Allowed files

home/dot_agents/skills/agmsg-orchestration/SKILL.md, tests/unit
fixtures if needed, artifact paths (T81 set).

## Forbidden actions

git commit; git push; chezmoi apply; bats; message-contract field
changes (report content convention only); rule-file growth.

## Completion / RESULT contract

Five artifacts; memory add; effects=none; cost line (practice what this
task codifies).
Reply `AGMSG-RESULT v1 task_id=T81`. max_turns=10.
