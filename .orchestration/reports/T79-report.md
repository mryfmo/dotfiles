# T79 report: two-tier agmsg orchestration rule

## Result

[memory:decision] The always-on Claude rule is now a 339.50-token estimated
core containing only activation, skill invocation, delegation, adversarial and
non-delegable review, zero-tail evidence sync, accepted-task decision coverage,
and mise-pair duties. The full protocol is in the on-demand
`agmsg-orchestration` skill.

No clause was deleted. The 23 original bullets were split into 87 independently
mapped subclauses in `.orchestration/validation/T79-validation.md`; every row is
kept in the core, moved to a named skill section, or identified as already
present in the skill.

## Measurement

T77 method for this English rule: character count / 4, with the documented
±20% estimator uncertainty.

- Before: 8,817 characters / 2,204.25 estimated tokens.
- After: 1,358 characters / 339.50 estimated tokens.
- Reduction: 7,459 characters / 1,864.75 estimated tokens (84.6%).
- Target: <=350 estimated tokens; PASS.

The `Message Contract v1` section hash remained
`944fbeef42549f3c77dbc455401ec29e58ec48772dee56899a41e5eb75d79038`.

## Validation

`make validate-agent-assets`, `make format`, all 336 Python unit tests,
whitespace checks, clause mapping, token budget, contract parity, changed-rule
scope, and Crit evidence gate passed. See the validation artifact for details.

## Decision memory

UUID: `4c8dac80-aa6b-48b6-88ef-4eaa2927ed03`

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T79: agmsg orchestration uses two-tier progressive disclosure: a 339.50-token estimated always-on core retains activation, delegation, adversarial and non-delegable review, zero-tail evidence sync, decision completeness, and mise-pair invariants; the full operational protocol lives in the agmsg-orchestration skill with zero mapped clause loss.'
```

## Cost

cost: n/a

## Effects

effects=none
