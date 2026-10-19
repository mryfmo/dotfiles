# Learning triage: dotfiles-T133-verdict-audit-pool-a03

These are candidates only; nothing is promoted.

1. [memory:failure] `git switch -C … --track` from the worker sandbox moves the branch ref, the index and the working tree, then fails on the upstream write to `.git/config`, which the sandbox denies. That leaves HEAD on the old branch, with every file staged as a difference.
   - **Recovery:** `git symbolic-ref HEAD refs/heads/<branch>`, after checking that the index equals the target commit.
   - **Prevention:** in the sandbox, switch without `--track` and push with an explicit refspec.
2. [memory:decision] A cap that counts data files is met honestly by changing their format, never their content.
   - Reformat a JSON schema, and assert that the parsed document equals the predecessor's.
   - When moving code from one file to another, run both copies on the same cases and compare their exit status and message, rather than relying on reading.
3. [memory:failure] A guard that runs before an effect only proves that the guard exists, not that the effect waits for it.
   - The regression has to observe the effect itself: dispatch or merge called or not, and the written verdict.
   - It also needs a zero-exit control that pins the order: gate, then dispatch, then merge.
