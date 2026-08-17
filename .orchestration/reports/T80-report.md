# T80 report

status: ready_for_review
cost: n/a
effects: none

## Result

[memory:decision] Codex's always-injected `AGENTS.md` now keeps general and
pre-skill invariants while delegating the complete plan/todo/learn file schema
and lifecycle to the existing `agmsg-orchestration` skill's `Codex worker
worklogs` section. The always-on pointer causes the skill to be read when
repository work begins.

- Inventoried 143 independently actionable clauses.
- Kept 91 clauses, moved 49, and canonicalized 3 duplicates.
- Deleted no instructional substance and left 0 clauses unmapped.
- Reduced the T77 estimate from 2,773.51 to 1,852.90 tokens: 920.62 tokens,
  or 33.19%, removed from the always-injected file.
- Left review, model/security, Ponytail, Understand-Anything, CompactionDB,
  coding, learning-at-start, and session-summary policy always-on.
- Did not modify the regular `agmsg` skill because no clause mapped there more
  naturally than the worker orchestration skill.

## Validation

- `make format`: pass.
- Unit tests: pass, 336 tests.
- `validate-agent-assets`: pass after the sandboxed first attempt encountered
  DNS while resolving its declared PyYAML dependency.
- `git diff --check`: pass.
- Clause continuity/count and token-reduction assertions: pass.
- Crit-data review gate: pass with resolved record `r_65f934` and repo-local
  receipt `.agents/worklog/codex/review/T80-receipt.md`.
- Plan-quality workflow: manual checklist passed; repository validator, Make
  target, hook, subagent definition, template, and CI entrypoint are absent.
- Full evidence: `.orchestration/validation/T80-validation.md`.

## Scope

- T80 source edits: `home/dot_config/codex/AGENTS.md` and
  `home/dot_agents/skills/agmsg-orchestration/SKILL.md`.
- Existing accepted T79 edits and orchestrator-owned planning/task artifacts
  were preserved as baseline and not reverted.
- No test fixtures, new skills, Claude-side rules, dependencies, commits,
  pushes, chezmoi apply, Bats, or real external effects.

## Decision memory

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T80 two-tiers Codex context by keeping per-session safety, review, model, and tool invariants in home/dot_config/codex/AGENTS.md while moving the complete repository worklog lifecycle and frontmatter procedure to the existing agmsg-orchestration skill; a 143-clause mapping proves zero substance deletion and the T77 estimator falls from 2773.51 to 1852.90 tokens.'
```

Recorded UUID: `d791071b-ca2e-4eea-99b5-38946e7a4edb`.
