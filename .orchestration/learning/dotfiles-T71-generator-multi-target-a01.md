# Learning triage: dotfiles-T71-generator-multi-target-a01

Candidates only; nothing is promoted.

1. **Normalise a scalar-or-list config field at the point of use.** `for entry in (x if isinstance(x, list) else [x])` keeps the single-mapping manifest byte-identical while allowing lists, with no manifest migration.
2. **Base-check commands in task files can go stale.** When an earlier task changes the exact text a grep check targets, verify the base by commit ancestry instead.
