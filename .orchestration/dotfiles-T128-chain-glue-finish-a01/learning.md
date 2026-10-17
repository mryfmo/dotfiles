# Learning triage: dotfiles-T128-chain-glue-finish-a01

These are candidates only; nothing is promoted.

1. [memory:decision] macOS `/bin/bash` is 3.2, where expanding an empty array under `set -u` is an unbound-variable error. A chain script that may hold an empty optional-argument array writes `${a[@]+"${a[@]}"}`, and a test suite that runs it with `bash` from `/bin` exercises that case.
2. [memory:decision] One order log that every stub appends its name to lets a test assert the exact order of calls across several stubs, which separate per-stub logs cannot.
3. [memory:decision] A local evidence file that drives a GitHub write (a sweep JSON whose dispositions a script posts) is bound to the head it was collected for, its `head_sha` against the audited head, before the write. A later step that compares the same field does not cover an earlier write (revise round 3, `local:f20826e:1`).
4. [memory:failure] `gh pr view --json merged` fails on gh 2.102.0 (`Unknown JSON field: "merged"`); a merged PR reads `state` `MERGED` with `mergeCommit.oid`, an open one `OPEN` with `mergeCommit: null`. A script that must know a merge landed polls those two fields, since `gh pr merge` can return once a merge queue has the PR (revise round 4, PR #378 thread `4301998951`).
