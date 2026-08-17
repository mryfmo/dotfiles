# T79: agmsg-orchestration ルールの二層化(progressive disclosure)

task_id: T79
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-pivot.md (Phase 6)
analysis: .orchestration/validation/T77-context-diet.md (提案 1)

[memory: decision — The agmsg-orchestration rule is two-tiered per Pi's progressive-disclosure principle: a ~300-token always-on core (activation trigger, absolute invariants, skill pointer) stays in rules, and the full protocol lives solely in the agmsg-orchestration skill; no clause is deleted, only relocated, with a clause-by-clause mapping table as evidence.]

## Goal

Cut ~1,850 tok from every Claude session in every project without losing
one clause of the protocol: detail moves from the always-injected rule to
the on-demand skill.

## Work order (exact)

1. Produce a CLAUSE INVENTORY of the current
   home/dot_config/claude/rules/agmsg-orchestration.md (number every
   bullet/sub-clause).
2. Design the slim core (target <=350 tok, measure with the T77 method):
   MUST retain verbatim-or-tightened: (a) when the regime activates and
   that the skill must be invoked on activation; (b) the absolute
   invariants that must bind EVEN BEFORE the skill loads — worker
   delegation principle, review/acceptance never delegated, adversarial
   RESULT review, evidence-sync/zero-tail duty, mise-pair rule; (c) the
   pointer: "invoke the agmsg-orchestration skill for the full protocol".
   Everything else (parallel-worktree rules, identity naming, store
   rules, teardown, delivery setup, nudge policy, pi/codex specifics,
   E2E-for-live-behavior clause, effects/marker cross-refs) MOVES to
   home/dot_agents/skills/agmsg-orchestration/SKILL.md, merged into its
   existing structure without duplicating what the skill already says
   (where the skill already covers a clause, record "already present" in
   the mapping).
3. Mapping table (validation artifact): every numbered clause -> kept in
   core / moved to skill §X / already present in skill. ZERO clauses
   dropped.
4. Token re-measure of the new rule file with the T77 estimator; state
   before/after.
5. Gates: make validate-agent-assets (rules/skills parity), make format,
   unit-test.

## Allowed files

- home/dot_config/claude/rules/agmsg-orchestration.md
- home/dot_agents/skills/agmsg-orchestration/SKILL.md
- tests/unit if any rule/skill validation fixture needs updating
- Your artifact paths (T79 set)

## Forbidden actions

git commit; git push; chezmoi apply; bats; deleting any clause's
substance; changing other rules; changing message contracts.

## Completion / RESULT contract

Five artifacts; memory add; effects=none; cost line (report tokens if
observable, else n/a).
Reply `AGMSG-RESULT v1 task_id=T79`. max_turns=15.
