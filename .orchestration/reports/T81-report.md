# T81 report

status: ready_for_review
cost: n/a
effects: none

## Result

[memory:decision] Worker reports now include a `cost:` line containing observed
session token/cost figures when the runtime exposes them, otherwise
`cost: n/a`. This report-artifact value feeds the T76
`AGMSG-ACCEPTANCE v1` cost line; it is not a new `AGMSG-RESULT v1` field.

- Added exactly one two-sentence Worker Playbook item.
- Did not alter the Message Contract block or either slim rule file.
- Did not add fixtures because the one-line documentation invariant is covered
  by a direct delta/hash assertion.

## Validation

- `make format`: pass.
- Unit tests: pass, 336 tests.
- `validate-agent-assets`: pass.
- `git diff --check`: pass.
- T81 delta: one added line, zero removed lines.
- Message Contract SHA-256 unchanged:
  `aa48267ed63f6ef1b2a13149e6a9c74be3be73699f4dae6610d1627fe7be8700`.
- Crit-data review: finding-free resolved record `r_beed82`; final evidence
  gate passed with `.agents/worklog/codex/review/T81-receipt.md`.
- Plan-quality workflow: manual checklist passed; repository validator, Make
  target, hook, subagent definition, template, and CI entrypoint are absent.
- Full evidence: `.orchestration/validation/T81-validation.md`.

## Scope

- Source edit: `home/dot_agents/skills/agmsg-orchestration/SKILL.md` only.
- No contract fields, rule files, dependencies, commits, pushes, chezmoi apply,
  Bats, or external effects.

## Decision memory

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T81 defines worker cost reporting as report-artifact content, not an AGMSG-RESULT wire field: workers write observed runtime session token/cost figures when exposed, otherwise cost: n/a, and this value feeds the existing T76 AGMSG-ACCEPTANCE cost line.'
```

Recorded UUID: `02b024a9-c2fb-4116-b424-797b94033ea9`.
