# T14 learning triage

## Validated observation

Run `gh auth status` before pushing in a combined push/PR task. A valid Git transport alone is insufficient when the next required operation is `gh pr create`; stopping before push avoids leaving the remote branch published without its requested PR.

## Promotion decision

No project learn entry is needed; this prerequisite is already required by the GitHub publish workflow skill.

