# T76: 吸収 — send.sh 識別子文法の内蔵+ACCEPTANCE コスト欄規約

task_id: T76
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-pivot.md (Phase 3)
depends: T74 (accepted)

[memory: decision — The Pi-era boundary defenses become core: send.sh itself validates team/from/to against ^[a-z0-9][a-z0-9_-]{0,63}$ for every caller, and ACCEPTANCE records gain a cost line (worker-reported tokens/cost or n/a), porting Pi's first-class cost accounting into the orchestration contract.]

## Work order

1. home/dot*agents/skills/agmsg/scripts/executable_send.sh: validate the
   three identifier args against `^[a-z0-9]a-z0-9*-]{0,63}$` BEFORE any
   DB work; on violation print one usage-style error to stderr, exit 1.
   FIRST verify every identity currently registered in
   ~/.agents/skills/agmsg/teams/\*/config.json matches the grammar (list
   them in the report; if any legacy identity violates it, STOP and ask).
   body stays free text (already SQL-safe via T68c).
2. Tests: extend tests/unit/test_agmsg_send.py — valid identifiers pass;
   quote/space/metachar identifiers exit 1 without touching the DB;
   quote-bearing BODY still round-trips (regression).
3. home/dot_agents/skills/agmsg-orchestration/SKILL.md +
   home/dot_config/claude/rules/agmsg-orchestration.md: one line each —
   ACCEPTANCE records include a cost line: worker-reported token/cost
   figures when available, otherwise `cost: n/a` (Pi-derived first-class
   cost accounting).
4. Gates: make format / bash -n / shellcheck / unit-test /
   validate-agent-assets.

## Allowed files

The four files above + tests/unit + artifact paths (T76 set).

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; grammar
looser or tighter than specified; body validation.

## Completion / RESULT contract

Five artifacts; memory add with the decision fact; effects=none.
Reply `AGMSG-RESULT v1 task_id=T76`. max_turns=15.
