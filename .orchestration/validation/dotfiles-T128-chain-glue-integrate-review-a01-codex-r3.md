[P1] high .orchestration/tasks/dotfiles-T128-chain-glue-integrate-a01.md:19 The review-worktree control still specifies exit 2, contradicting the round-3 contract that reserves 1 for failed steps and 10–15 for the chain’s refusals.

[P1] high .orchestration/tasks/dotfiles-T128-chain-glue-integrate-a01.md:91 The script uses the task and owner arguments in writable paths and acceptance-record content without requiring task-id validation, permitting path traversal or record injection instead of failing closed.

Task-file verdict: dotfiles-T128-chain-glue-integrate-a01: revise