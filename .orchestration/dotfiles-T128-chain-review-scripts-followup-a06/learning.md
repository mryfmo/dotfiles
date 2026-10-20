---
task_id: dotfiles-T128-chain-review-scripts-followup-a06
seat: claude-standard-dot-a011
---

# Learning: dotfiles-T128-chain-review-scripts-followup-a06

1. A sandbox ledger written before a gated step becomes a plan, not a record, once another seat finishes that step. Here a007 stopped at the PR-creation command, and the orchestrator and a011 ran the rest. Mechanism: when a seat stops at a gated call, its ledger row says "not run by this seat; see the RESULT or acceptance record". The seat that runs the call writes its own row with the time and outcome, as a011's ci-efficiency-a01 sandbox record did for `gh pr ready 402`.
2. GitHub attributes every action to the one shared account, so a ledger needs the bus or the regime records to name the seat. A whole-bus `history.sh` read is too slow to do this inside a task (C-53). Mechanism: an acceptance record names the acting seat and the UTC time of each gh write it makes, so reconciling the record with GitHub's timeline needs no bus read.
