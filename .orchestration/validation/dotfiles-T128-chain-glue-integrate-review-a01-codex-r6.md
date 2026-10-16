[P1] high .orchestration/tasks/dotfiles-T128-chain-glue-integrate-a01.md:106 The tests use an independently cloned review checkout and stub `local-review.sh`, so they miss that the real script requires the fetched head in the main checkout’s object database; fetch the PR head into `<main>` too or require and test a linked worktree.

Task-file verdict: dotfiles-T128-chain-glue-integrate-a01: revise