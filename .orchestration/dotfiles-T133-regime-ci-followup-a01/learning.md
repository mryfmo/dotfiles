---
task_id: dotfiles-T133-regime-ci-followup-a01
seat: claude-standard-dot-a011
---

# Learning: dotfiles-T133-regime-ci-followup-a01

1. A `closed` threat row is only as strong as the tests that fail when each claimed check is disabled. Naming one test for a seven-part control left four parts unguarded on paper. Mechanism: a mutation table, in which each claimed check is disabled in a scratch copy and the named tests are run, shows exactly which selector closes which claim. A threat row that claims several checks should name every test the table marks red.
2. Evidence about the head that carries the evidence is circular. A record cannot hold its own commit's id or CI. Mechanism: bootstrap the code head, put the evidence in one later commit that touches only `.orchestration/<task>/`, state both identities, and let the RESULT carry the final head's diff and CI.
3. Worktrees share refs, so `origin/main` moved under this branch, to PR #422's merge, while the task ran. Mechanism: a validation generator reads the base sha at run time (`git rev-parse origin/main`) and records what moved since the branch point, so the bootstrap uses the base the CI job would use.
4. A records-only task can gain a code row mid-task. The orchestrator added `ci:39185982423:1` by PING after dispatch, because the task reads its rows from the record. Mechanism: re-read the record's `Owned by` section before the first push. Record the code head and the evidence head as two identities from the start, so a late code commit only moves the code head.
5. A test written for a fix that changes no verifier code passes before the fix, so it is a characterization test, and its fixture can miss the incident's shape. The first moved-base test kept the dispatched text at the merge base too, so a verifier that read the policy there would still pass. Mechanism: build the fixture from the incident (PR #420: the policy only on the moved tip), and prove it with a mutation of the claim it guards, recorded beside the red run (validation §3).
