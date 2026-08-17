# T80: codex AGENTS.md の同型二層化(progressive disclosure)

task_id: T80
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-pivot.md (Phase 6)
depends: T79 (accepted)
analysis: .orchestration/validation/T77-context-diet.md (提案 2)

[memory: decision — Codex's always-injected AGENTS.md (home/dot_config/codex/AGENTS.md) is audited and two-tiered the same way as the Claude agmsg rule: always-on invariants stay, protocol detail that a worker only needs mid-task moves to the on-demand skills it already reads (agmsg / agmsg-orchestration), with a clause mapping table and zero clause deletion.]

## Goal

Apply the T79 pattern to the Codex side (2,773 tok measured in T77).
Codex loads ~/.agents/skills on demand, so detail belongs there.

## Work order (exact)

1. CLAUSE INVENTORY of home/dot_config/codex/AGENTS.md (number every
   bullet/sub-clause).
2. Classify each clause: (a) always-on invariant (safety, forbidden
   actions, identity/env rules that must bind before any skill loads) —
   KEEP; (b) protocol detail already or naturally covered by an
   on-demand skill the worker reads during agmsg tasks — MOVE (merge
   into the skill, no duplication); (c) covered elsewhere already —
   record "already present" and drop the duplicate copy only.
   If a clause fits no skill and is not an invariant, KEEP it — do not
   invent new skills for this task.
3. Mapping table (validation artifact): clause -> kept / moved to
   <skill §> / duplicate-of <location>. ZERO substance dropped.
4. Token re-measure (T77 method), before/after.
5. Gates: make validate-agent-assets / format / unit-test.

## Allowed files

- home/dot_config/codex/AGENTS.md
- home/dot_agents/skills/agmsg/SKILL.md
- home/dot_agents/skills/agmsg-orchestration/SKILL.md
- tests/unit fixtures if validation depends on them
- Artifact paths (T80 set)

## Forbidden actions

git commit; git push; chezmoi apply; bats; clause deletion; creating
new skills; touching Claude-side rules.

## Completion / RESULT contract

Five artifacts; memory add; effects=none; cost line (tokens if
observable, else n/a).
Reply `AGMSG-RESULT v1 task_id=T80`. max_turns=15.
