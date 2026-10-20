---
task_id: dotfiles-T128-chain-review-scripts-followup-a07
seat: claude-standard-dot-a011
---

# Learning: dotfiles-T128-chain-review-scripts-followup-a07

1. A record the task reads at dispatch can change while the task runs. The a06 acceptance record had no `## Owned by …-a07` section when this seat first read it; the orchestrator wrote one about 8 minutes after dispatch (04:13:45Z to 04:22Z). Mechanism: the validation reads the owned rows again when it is generated and pastes what it finds, so the evidence shows the record as it stands at the RESULT, and the report says when each reading happened.
2. A new external call in a script is a new binary on PATH for every test that runs the script. Adding `gh` broke two tests whose mise stub answered any name with a path, a `gh` that did not exist. Mechanism: when a script gains a resolved binary, grep its tests for every mise or PATH stub and make each answer only for tools that exist, so the new name falls back the way production does.
3. A mutant's name has to describe what the replacement does. A draft mutant labelled "the refusal after the checkout" replaced the base after the checkout instead, which tests something else. Mechanism: before running a mutation, write down which line of the change it undoes, and name the mutant after that line.
4. A finding names one vector; its class can hold more. The review reproduced a planted replace ref; a graft in `info/grafts` does the same to the merge base, and the variable that disables replacement leaves grafts alone. Mechanism: for a finding about state an attacker can plant, list the other ways git lets the same state be planted, measure each in a scratch repository before the fix, and give each its own subtest and mutant.
