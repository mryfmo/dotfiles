## PR integration

- Before merging any pull request, MUST sweep all of its GitHub feedback for the final head commit with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json`, and re-run the sweep after any new push: a disposition applies only to the head commit it was written for.
- MUST give every item a disposition: `fixed:<commit>` with the root-cause fix in that commit, or `not-applicable:<reason>`. Stopgaps, suppressions, or "later" are not dispositions, and no `failure` or `warning` annotation is left undispositioned.
- MUST pass the filled JSON to the integration gate, together with the task-level audit of the final head when the change needs review, and summarise the dispositions in the acceptance record. A bot review is optional and never gated.
- The gate that judges a PR is `main`'s script, never the PR's: `make require-crit-review -C <main checkout> REVIEW_TREE=<review worktree> BASE=origin/main …`. The full gate command, its evidence rules, the boundary-PR exception and the merge procedure appear once, in the agmsg-orchestration SKILL's Orchestrator Playbook step 10.
